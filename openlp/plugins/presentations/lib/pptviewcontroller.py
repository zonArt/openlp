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

from ctypes import *
from ctypes.wintypes import RECT

from presentationcontroller import PresentationController

class PptviewController(PresentationController):
    """
    Class to control interactions with PowerPOint Viewer Presentations
    It creates the runtime Environment , Loads the and Closes the Presentation
    As well as trigggering the correct activities based on the users input
    """
    global log
    log = logging.getLogger(u'PptviewController')

    def __init__(self, plugin):
        """
        Initialise the class
        """
        log.debug(u'Initialised')
        PresentationController.__init__(self, plugin, u'Powerpoint Viewer')
        self.process = None
        self.pptid = None
        self.thumbnailpath = os.path.join(plugin.config.get_data_path(),
            u'pptview', u'thumbnails')
        self.thumbprefix = u'slide'
        self.start_process()

    def start_process(self):
        """
        Loads the PPTVIEWLIB library
        """
        log.debug(u'start PPTView')
        self.process = cdll.LoadLibrary(r'openlp\plugins\presentations\lib\pptviewlib\pptviewlib.dll')

    def kill(self):
        """
        Called at system exit to clean up any running presentations
        """
        log.debug(u'Kill')
        self.close_presentation()

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
        if self.pptid >= 0:
            self.close_presentation()
        rendermanager = self.plugin.render_manager
        #screen = rendermanager.screen_list[rendermanager.current_display]
        # x? y?
        rect = RECT(0, 0, rendermanager.width, rendermanager.height)
        filename = str(presentation.replace(u'/', u'\\'));
        try:
            self.pptid = self.process.OpenPPT(filename, None, rect,
                                              str(self.thumbnailpath))
        except:
            log.exception(u'Failed to load presentation')


    def close_presentation(self):
        """
        Close presentation and clean up objects
        Triggerent by new object being added to SlideController orOpenLP
        being shut down
        """
        if self.pptid < 0:
            return
        self.process.ClosePPT(self.pptid)
        self.pptid = -1

    def is_active(self):
        """
        Returns true if a presentation is currently active
        """
        return self.pptid >= 0

    def resume_presentation(self):
        """
        Resumes a previously paused presentation
        """
        if self.pptid < 0:
            return
        self.process.Resume(self.pptid)

    def pause_presentation(self):
        """
        Not implemented (pauses a presentation)
        """
        return

    def blank_screen(self):
        """
        Blanks the screen
        """
        if self.pptid < 0:
            return
        self.process.Blank(self.pptid)

    def unblank_screen(self):
        """
        Unblanks (restores) the presentationn
        """
        if self.pptid < 0:
            return
        self.process.Unblank(self.pptid)

    def stop_presentation(self):
        """
        Stops the current presentation and hides the output
        """
        if self.pptid < 0:
            return
        self.process.Stop(self.pptid)

    def start_presentation(self):
        """
        Starts a presentation from the beginning
        """
        if self.pptid < 0:
            return
        self.process.RestartShow(self.pptid)

    def get_slide_number(self):
        """
        Returns the current slide number
        """
        if self.pptid < 0:
            return 0
        return self.process.GetCurrentSlide(self.pptid)

    def get_slide_count(self):
        """
        Returns total number of slides
        """
        if self.pptid < 0:
            return 0
        return self.process.GetSlideCount(self.pptid)

    def goto_slide(self, slideno):
        """
        Moves to a specific slide in the presentation
        """
        if self.pptid < 0:
            return
        self.process.GotoSlide(self.pptid, slideno)

    def next_step(self):
        """
        Triggers the next effect of slide on the running presentation
        """
        if self.pptid < 0:
            return
        self.process.NextStep(self.pptid)

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation
        """
        if self.pptid < 0:
            return
        self.process.PrevStep(self.pptid)

    def get_slide_preview_file(self, slide_no):
        """
        Returns an image path containing a preview for the requested slide

        ``slide_no``
            The slide an image is required for, starting at 1
        """
        if self.pptid < 0:
            return
        return os.path.join(self.thumbnailpath,
            self.thumbprefix + slide_no + u'.bmp')

