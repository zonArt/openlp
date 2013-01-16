# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
    import pywintypes

from presentationcontroller import PresentationController, PresentationDocument

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
        PresentationController.__init__(self, plugin, u'Powerpoint', PowerpointDocument)
        self.supports = [u'ppt', u'pps', u'pptx', u'ppsx']
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
            except WindowsError:
                pass
        return False

    if os.name == u'nt':
        def start_process(self):
            """
            Loads PowerPoint process
            """
            log.debug(u'start_process')
            if not self.process:
                self.process = Dispatch(u'PowerPoint.Application')
            self.process.Visible = True
            self.process.WindowState = 2

        def kill(self):
            """
            Called at system exit to clean up any running presentations
            """
            log.debug(u'Kill powerpoint')
            while self.docs:
                self.docs[0].close_presentation()
            if self.process is None:
                return
            try:
                if self.process.Presentations.Count > 0:
                    return
                self.process.Quit()
            except pywintypes.com_error:
                pass
            self.process = None


class PowerpointDocument(PresentationDocument):
    """
    Class which holds information and controls a single presentation
    """

    def __init__(self, controller, presentation):
        """
        Constructor, store information about the file and initialise
        """
        log.debug(u'Init Presentation Powerpoint')
        PresentationDocument.__init__(self, controller, presentation)
        self.presentation = None

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController.
        Opens the PowerPoint file using the process created earlier.
        """
        log.debug(u'load_presentation')
        if not self.controller.process or not self.controller.process.Visible:
            self.controller.start_process()
        try:
            self.controller.process.Presentations.Open(self.filepath, False, False, True)
        except pywintypes.com_error:
            log.debug(u'PPT open failed')
            return False
        self.presentation = self.controller.process.Presentations(self.controller.process.Presentations.Count)
        self.create_thumbnails()
        return True

    def create_thumbnails(self):
        """
        Create the thumbnail images for the current presentation.

        Note an alternative and quicker method would be do::

            self.presentation.Slides[n].Copy()
            thumbnail = QApplication.clipboard.image()

        However, for the moment, we want a physical file since it makes life
        easier elsewhere.
        """
        log.debug(u'create_thumbnails')
        if self.check_thumbnails():
            return
        for num in range(self.presentation.Slides.Count):
            self.presentation.Slides(num + 1).Export(os.path.join(
                self.get_thumbnail_folder(), 'slide%d.png' % (num + 1)), 'png', 320, 240)

    def close_presentation(self):
        """
        Close presentation and clean up objects. This is triggered by a new
        object being added to SlideController or OpenLP being shut down.
        """
        log.debug(u'ClosePresentation')
        if self.presentation:
            try:
                self.presentation.Close()
            except pywintypes.com_error:
                pass
        self.presentation = None
        self.controller.remove_doc(self)

    def is_loaded(self):
        """
        Returns ``True`` if a presentation is loaded.
        """
        log.debug(u'is_loaded')
        try:
            if not self.controller.process.Visible:
                return False
            if self.controller.process.Windows.Count == 0:
                return False
            if self.controller.process.Presentations.Count == 0:
                return False
        except (AttributeError, pywintypes.com_error):
            return False
        return True


    def is_active(self):
        """
        Returns ``True`` if a presentation is currently active.
        """
        log.debug(u'is_active')
        if not self.is_loaded():
            return False
        try:
            if self.presentation.SlideShowWindow is None:
                return False
            if self.presentation.SlideShowWindow.View is None:
                return False
        except (AttributeError, pywintypes.com_error):
            return False
        return True

    def unblank_screen(self):
        """
        Unblanks (restores) the presentation.
        """
        log.debug(u'unblank_screen')
        self.presentation.SlideShowSettings.Run()
        self.presentation.SlideShowWindow.View.State = 1
        self.presentation.SlideShowWindow.Activate()
        if self.presentation.Application.Version == u'14.0':
            # Unblanking is broken in PowerPoint 2010, need to redisplay
            slide = self.presentation.SlideShowWindow.View.CurrentShowPosition
            click = self.presentation.SlideShowWindow.View.GetClickIndex()
            self.presentation.SlideShowWindow.View.GotoSlide(slide)
            if click:
                self.presentation.SlideShowWindow.View.GotoClick(click)

    def blank_screen(self):
        """
        Blanks the screen.
        """
        log.debug(u'blank_screen')
        self.presentation.SlideShowWindow.View.State = 3

    def is_blank(self):
        """
        Returns ``True`` if screen is blank.
        """
        log.debug(u'is_blank')
        if self.is_active():
            return self.presentation.SlideShowWindow.View.State == 3
        else:
            return False

    def stop_presentation(self):
        """
        Stops the current presentation and hides the output.
        """
        log.debug(u'stop_presentation')
        self.presentation.SlideShowWindow.View.Exit()

    if os.name == u'nt':
        def start_presentation(self):
            """
            Starts a presentation from the beginning.
            """
            log.debug(u'start_presentation')
            #SlideShowWindow measures its size/position by points, not pixels
            try:
                dpi = win32ui.GetActiveWindow().GetDC().GetDeviceCaps(88)
            except win32ui.error:
                try:
                    dpi = win32ui.GetForegroundWindow().GetDC().GetDeviceCaps(88)
                except win32ui.error:
                    dpi = 96
            renderer = self.controller.plugin.renderer
            rect = renderer.screens.current[u'size']
            ppt_window = self.presentation.SlideShowSettings.Run()
            if not ppt_window:
                return
            ppt_window.Top = rect.y() * 72 / dpi
            ppt_window.Height = rect.height() * 72 / dpi
            ppt_window.Left = rect.x() * 72 / dpi
            ppt_window.Width = rect.width() * 72 / dpi


    def get_slide_number(self):
        """
        Returns the current slide number.
        """
        log.debug(u'get_slide_number')
        return self.presentation.SlideShowWindow.View.CurrentShowPosition

    def get_slide_count(self):
        """
        Returns total number of slides.
        """
        log.debug(u'get_slide_count')
        return self.presentation.Slides.Count

    def goto_slide(self, slideno):
        """
        Moves to a specific slide in the presentation.
        """
        log.debug(u'goto_slide')
        self.presentation.SlideShowWindow.View.GotoSlide(slideno)

    def next_step(self):
        """
        Triggers the next effect of slide on the running presentation.
        """
        log.debug(u'next_step')
        self.presentation.SlideShowWindow.View.Next()
        if self.get_slide_number() > self.get_slide_count():
            self.previous_step()

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation.
        """
        log.debug(u'previous_step')
        self.presentation.SlideShowWindow.View.Previous()

    def get_slide_text(self, slide_no):
        """
        Returns the text on the slide.

        ``slide_no``
            The slide the text is required for, starting at 1.
        """
        return _get_text_from_shapes(self.presentation.Slides(slide_no).Shapes)

    def get_slide_notes(self, slide_no):
        """
        Returns the text on the slide.

        ``slide_no``
            The slide the notes are required for, starting at 1.
        """
        return _get_text_from_shapes(self.presentation.Slides(slide_no).NotesPage.Shapes)

def _get_text_from_shapes(shapes):
    """
    Returns any text extracted from the shapes on a presentation slide.

    ``shapes``
        A set of shapes to search for text.
    """
    text = ''
    for idx in range(shapes.Count):
        shape = shapes(idx + 1)
        if shape.HasTextFrame:
            text += shape.TextFrame.TextRange.Text + '\n'
    return text
