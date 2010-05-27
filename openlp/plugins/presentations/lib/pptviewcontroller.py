# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
    from ctypes import *
    from ctypes.wintypes import RECT

from presentationcontroller import PresentationController, PresentationDocument

log = logging.getLogger(__name__)

class PptviewController(PresentationController):
    """
    Class to control interactions with PowerPOint Viewer Presentations
    It creates the runtime Environment , Loads the and Closes the Presentation
    As well as triggering the correct activities based on the users input
    """
    log.info(u'PPTViewController loaded')

    def __init__(self, plugin):
        """
        Initialise the class
        """
        log.debug(u'Initialising')
        self.process = None
        PresentationController.__init__(self, plugin, u'Powerpoint Viewer')
        self.supports = [u'.ppt', u'.pps', u'.pptx', u'.ppsx']

    def check_available(self):
        """
        PPT Viewer is able to run on this machine
        """
        log.debug(u'check_available')
        if os.name != u'nt':
            return False
        try:
            return self.check_installed()
        except:
            return False

    if os.name == u'nt':
        def check_installed(self):
            """
            Check the viewer is installed
            """
            log.debug(u'Check installed')
            try:
                self.start_process()
                return self.process.CheckInstalled()
            except:
                return False

        def start_process(self):
            """
            Loads the PPTVIEWLIB library
            """
            if self.process:
                return
            log.debug(u'start PPTView')
            self.process = cdll.LoadLibrary(
                r'openlp\plugins\presentations\lib\pptviewlib\pptviewlib.dll')

        def kill(self):
            """
            Called at system exit to clean up any running presentations
            """
            log.debug(u'Kill pptviewer')
            while self.docs:
                self.docs[0].close_presentation()

        def add_doc(self, name):
            log.debug(u'Add Doc PPTView')
            doc = PptviewDocument(self, name)
            self.docs.append(doc)
            return doc

class PptviewDocument(PresentationDocument):
    def __init__(self, controller, presentation):
        log.debug(u'Init Presentation PowerPoint')
        self.presentation = None
        self.pptid = None
        self.blanked = False
        self.controller = controller
        self.store_filename(presentation)

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController.
        It builds the environment, starts communcations with the background
        PptView task started earlier.

        ``presentation``
        The file name of the presentations to run.
        """
        log.debug(u'LoadPresentation')
        #if self.pptid >= 0:
        #    self.close_presentation()
        rendermanager = self.controller.plugin.render_manager
        rect = rendermanager.screens.current[u'size']
        rect = RECT(rect.x(), rect.y(), rect.right(), rect.bottom())
        filepath = str(self.filepath.replace(u'/', u'\\'))
        try:
            self.pptid = self.controller.process.OpenPPT(filepath, None, rect,
                str(os.path.join(self.thumbnailpath, self.controller.thumbnailprefix)))
            self.stop_presentation()
        except:
            log.exception(u'Failed to load presentation')

    def close_presentation(self):
        """
        Close presentation and clean up objects
        Triggerent by new object being added to SlideController orOpenLP
        being shut down
        """
        log.debug(u'ClosePresentation')
        self.controller.process.ClosePPT(self.pptid)
        self.pptid = -1
        self.controller.remove_doc(self)

    def is_loaded(self):
        """
        Returns true if a presentation is loaded
        """
        if self.pptid < 0:
            return False
        if self.get_slide_count() < 0:
            return False
        return True

    def is_active(self):
        """
        Returns true if a presentation is currently active
        """
        return self.is_loaded()

    def blank_screen(self):
        """
        Blanks the screen
        """
        self.controller.process.Blank(self.pptid)
        self.blanked = True

    def unblank_screen(self):
        """
        Unblanks (restores) the presentationn
        """
        self.controller.process.Unblank(self.pptid)
        self.blanked = False

    def is_blank(self):
        """
        Returns true if screen is blank
        """
        log.debug(u'is blank OpenOffice')
        return self.blanked

    def stop_presentation(self):
        """
        Stops the current presentation and hides the output
        """
        self.controller.process.Stop(self.pptid)

    def start_presentation(self):
        """
        Starts a presentation from the beginning
        """
        self.controller.process.RestartShow(self.pptid)

    def get_slide_number(self):
        """
        Returns the current slide number
        """
        return self.controller.process.GetCurrentSlide(self.pptid)

    def get_slide_count(self):
        """
        Returns total number of slides
        """
        return self.controller.process.GetSlideCount(self.pptid)

    def goto_slide(self, slideno):
        """
        Moves to a specific slide in the presentation
        """
        self.controller.process.GotoSlide(self.pptid, slideno)

    def next_step(self):
        """
        Triggers the next effect of slide on the running presentation
        """
        self.controller.process.NextStep(self.pptid)

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation
        """
        self.controller.process.PrevStep(self.pptid)

    def get_slide_preview_file(self, slide_no):
        """
        Returns an image path containing a preview for the requested slide

        ``slide_no``
            The slide an image is required for, starting at 1
        """
        path = os.path.join(self.thumbnailpath,
            self.controller.thumbnailprefix + unicode(slide_no) + u'.bmp')
        if os.path.isfile(path):
            return path
        else:
            return None
