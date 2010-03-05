# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import os
import logging

if os.name == u'nt':
    from win32com.client import Dispatch
    import _winreg
    import win32ui

from presentationcontroller import PresentationController,  PresentationDocument

log = logging.getLogger(__name__)

# PPT API documentation:
# http://msdn.microsoft.com/en-us/library/aa269321(office.10).aspx

class PowerpointController(PresentationController):
    """
    Class to control interactions with PowerPoint Presentations
    It creates the runtime Environment , Loads the and Closes the Presentation
    As well as triggering the correct activities based on the users input
    """
    log.info(u'PowerpointController loaded')

    def __init__(self, plugin):
        """
        Initialise the class
        """
        log.debug(u'Initialising')
        PresentationController.__init__(self, plugin, u'Powerpoint')
        self.supports = [u'.ppt', u'.pps', u'.pptx', u'.ppsx']
        self.process = None

    def check_available(self):
        """
        PowerPoint is able to run on this machine
        """
        log.debug(u'check_available')
        if os.name == u'nt':
            try:
                _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, u'PowerPoint.Application').Close()
                return True
            except:
                pass
        return False

    if os.name == u'nt':
        def start_process(self):
            """
            Loads PowerPoint process
            """
            self.process = Dispatch(u'PowerPoint.Application')
            self.process.Visible = True
            self.process.WindowState = 2

        def is_loaded(self):
            """
            Returns true if a presentation is loaded
            """
            try:
                if not self.process.Visible:
                    return False
                if self.process.Windows.Count == 0:
                    return False
                if self.process.Presentations.Count == 0:
                    return False
            except:
                return False
            return True

        def kill(self):
            """
            Called at system exit to clean up any running presentations
            """
            for doc in self.docs:
                doc.close_presentation()
            if self.process is None:
                return
            if self.process.Presentations.Count > 0:
                return
            try:
                self.process.Quit()
            except:
                pass
            self.process = None

        def add_doc(self, name):
            log.debug(u'Add Doc PowerPoint')
            doc = PowerpointDocument(self,  name)
            self.docs.append(doc)
            return doc

class PowerpointDocument(PresentationDocument):

    def __init__(self,  controller,  presentation):
        log.debug(u'Init Presentation Powerpoint')
        self.presentation = None
        self.controller = controller
        self.store_filename(presentation)

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController.
        It builds the environment, starts communcations with the background
        OpenOffice task started earlier.  If OpenOffice is not present is is
        started.  Once the environment is available the presentation is loaded
        and started.

        ``presentation``
        The file name of the presentations to run.
        """
        log.debug(u'LoadPresentation')
        #try:
        if not self.controller.process.Visible:
            self.controller.start_process()
        #except:
        #   self.controller.start_process()
        #try:
        self.controller.process.Presentations.Open(self.filepath, False, False, True)
        #except:
        #    return
        self.presentation = self.controller.process.Presentations(
            self.controller.process.Presentations.Count)
        self.create_thumbnails()

    def create_thumbnails(self):
        """
        Create the thumbnail images for the current presentation.
        Note an alternative and quicker method would be do
            self.presentation.Slides[n].Copy()
            thumbnail = QApplication.clipboard.image()
        But for now we want a physical file since it makes
        life easier elsewhere
        """
        if self.check_thumbnails():
            return
        self.presentation.Export(os.path.join(self.thumbnailpath, '')
                                 , 'png', 600, 480)

    def close_presentation(self):
        """
        Close presentation and clean up objects
        Triggerent by new object being added to SlideController orOpenLP
        being shut down
        """
        if self.presentation is None:
            return
        try:
            self.presentation.Close()
        except:
            pass
        self.presentation = None
        self.controller.remove_doc(self)

    def is_active(self):
        """
        Returns true if a presentation is currently active
        """
        if not self.controller.is_loaded():
            return False
        try:
            if self.presentation.SlideShowWindow is None:
                return False
            if self.presentation.SlideShowWindow.View is None:
                return False
        except:
            return False
        return True

    def unblank_screen(self):
        """
        Unblanks (restores) the presentationn
        """
        self.presentation.SlideShowSettings.Run()
        self.presentation.SlideShowWindow.View.State = 1
        self.presentation.SlideShowWindow.Activate()

    def blank_screen(self):
        """
        Blanks the screen
        """
        self.presentation.SlideShowWindow.View.State = 3

    def stop_presentation(self):
        """
        Stops the current presentation and hides the output
        """
        self.presentation.SlideShowWindow.View.Exit()

    if os.name == u'nt':
        def start_presentation(self):
            """
            Starts a presentation from the beginning
            """
            #SlideShowWindow measures its size/position by points, not pixels
            try:
                dpi = win32ui.GetActiveWindow().GetDC().GetDeviceCaps(88)
            except:
                try:
                    dpi = win32ui.GetForegroundWindow().GetDC().GetDeviceCaps(88)
                except:
                    dpi = 96
            self.presentation.SlideShowSettings.Run()
            self.presentation.SlideShowWindow.View.GotoSlide(1)
            rendermanager = self.controller.plugin.render_manager
            rect = rendermanager.screens.current[u'size']
            self.presentation.SlideShowWindow.Top = rect.y() * 72 / dpi
            self.presentation.SlideShowWindow.Height = rect.height() * 72 / dpi
            self.presentation.SlideShowWindow.Left = rect.x() * 72 / dpi
            self.presentation.SlideShowWindow.Width = rect.width() * 72 / dpi

    def get_slide_number(self):
        """
        Returns the current slide number
        """
        return self.presentation.SlideShowWindow.View.CurrentShowPosition

    def get_slide_count(self):
        """
        Returns total number of slides
        """
        return self.presentation.Slides.Count

    def goto_slide(self, slideno):
        """
        Moves to a specific slide in the presentation
        """
        self.presentation.SlideShowWindow.View.GotoSlide(slideno)

    def next_step(self):
        """
        Triggers the next effect of slide on the running presentation
        """
        self.presentation.SlideShowWindow.View.Next()

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation
        """
        self.presentation.SlideShowWindow.View.Previous()

    def get_slide_preview_file(self, slide_no):
        """
        Returns an image path containing a preview for the requested slide

        ``slide_no``
        The slide an image is required for, starting at 1
        """
        path = os.path.join(self.thumbnailpath,
            self.controller.thumbnailprefix + unicode(slide_no) + u'.png')
        if os.path.isfile(path):
            return path
        else:
            return None
