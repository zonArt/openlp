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

import logging

from ctypes import *
from ctypes.wintypes import RECT

class PptviewController(object):
    """
    Class to control interactions with PowerPOint Viewer Presentations
    It creates the runtime Environment , Loads the and Closes the Presentation
    As well as trigggering the correct activities based on the users input
    """
    global log
    log = logging.getLogger(u'PptviewController')

    def __init__(self):
        log.debug(u'Initialising')
        self.process = None
        self.document = None
        self.presentation = None
        self.pptid = None
        self.startPPTView()

    def startPPTView(self):
        """
        Loads the PPTVIEWLIB library
        """
        log.debug(u'start PPTView')
        self.presentation = cdll.LoadLibrary(r'openlp\plugins\presentations\lib\pptviewlib\pptviewlib.dll')

    def kill(self):
        """
        Called at system exit to clean up any running presentations
        """
        log.debug(u'Kill')
        self.closePresentation()

    def loadPresentation(self, presentation):
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
            self.closePresentation()
        rect = RECT(0, 0, 800, 600) # until such time I can get screen info
        filename = str(presentation.replace(u'/', u'\\'));
        try:
            tempfolder = None #r'c:\temp\pptviewlib\' + filename.split('u\\')[-1]
            self.pptid = self.presentation.OpenPPT(filename, None, rect, tempfolder)
        except:
            log.exception(u'Failed to load presentation')
        #self.slidecount = pptdll.GetSlideCount(self.pptid)

    def closePresentation(self):
        """
        Close presentation and clean up objects
        Triggerent by new object being added to SlideController orOpenLP
        being shut down
        """
        if self.pptid < 0:
            return
        self.presentation.ClosePPT(self.pptid)
        self.pptid = -1

    def nextStep(self):
        """
        Triggers the next effect of slide on the running presentation
        """
        if self.pptid < 0:
            return
        self.presentation.NextStep(self.pptid)

    def previousStep(self):
        """
        Triggers the previous slide on the running presentation
        """
        if self.pptid < 0:
            return
        self.presentation.PrevStep(self.pptid)

    def isActive(self):
        """
        Returns true if a presentation is currently active
        """
        return self.pptid >= 0

    def resume(self):
        """
        Resumes a previously paused presentation
        """
        if self.pptid < 0:
            return
        self.presentation.Resume(self.pptid)

    def pause(self):
        """
        Not implemented (pauses a presentation)
        """
        return

    def blankScreen(self):
        """
        Blanks the screen
        """
        if self.pptid < 0:
            return
        self.presentation.Blank(self.pptid)

    def unblankScreen(self):
        """
        Unblanks (restores) the presentationn
        """
        if self.pptid < 0:
            return
        self.presentation.Unblank(self.pptid)

    def stop(self):
        """
        Stops the current presentation and hides the output
        """
        if self.pptid < 0:
            return
        self.presentation.Stop(self.pptid)

    def go(self):
        """
        Starts a presentation from the beginning
        """
        if self.pptid < 0:
            return
        self.presentation.RestartShow(self.pptid)

    def getSlideNumber(self):
        """
        Returns the current slide number
        """
        if self.pptid < 0:
            return -1
        return self.presentation.GetCurrentSlide(self.pptid)

    def setSlideNumber(self, slideno):
        """
        Moves to a specific slide in the presentation
        """
        if self.pptid < 0:
            return
        self.presentation.GotoSlide(self.pptid, slideno)

    slideNumber = property(getSlideNumber, setSlideNumber)


