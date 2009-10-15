# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from presentationcontroller import PresentationController

# PPT API documentation:
# http://msdn.microsoft.com/en-us/library/aa269321(office.10).aspx

class PowerpointController(PresentationController):
    """
    Class to control interactions with PowerPoint Presentations
    It creates the runtime Environment , Loads the and Closes the Presentation
    As well as triggering the correct activities based on the users input
    """
    global log
    log = logging.getLogger(u'PowerpointController')
    log.info(u'loaded')
    
    def __init__(self, plugin):
        """
        Initialise the class
        """
        log.debug(u'Initialising')
        PresentationController.__init__(self, plugin, u'Powerpoint')
        self.process = None
        self.presentation = None
 
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
            if self.process is None:
                return
            try:
                self.process.Quit()
            except:
                pass
            self.process = None

        def load_presentation(self, presentation):
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
            self.store_filename(presentation)
            try:
                if not self.process.Visible:
                    self.start_process()
            except:
                self.start_process()
            try:
                self.process.Presentations.Open(presentation, False, False, True)
            except:
                return
            self.presentation = self.process.Presentations(self.process.Presentations.Count)
            self.create_thumbnails()
            self.start_presentation()

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
            if self.presentation == None:
                return
            try:
                self.presentation.Close()
            except:
                pass
            self.presentation = None

        def is_active(self):
            """
            Returns true if a presentation is currently active
            """
            if not self.is_loaded():
                return False
            try:
                if self.presentation.SlideShowWindow == None:
                    return False
                if self.presentation.SlideShowWindow.View == None:
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
            rendermanager = self.plugin.render_manager
            rect = rendermanager.screen_list[rendermanager.current_display][u'size']
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
            return os.path.join(self.thumbnailpath,
                self.thumbnailprefix + unicode(slide_no) + u'.png')
