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
import os
import shutil

from PyQt4 import QtCore

from openlp.core.lib import Receiver

class PresentationController(object):
    """
    Base class for presentation controllers to inherit from
    Class to control interactions with presentations.
    It creates the runtime environment, loads and closes the presentation as
    well as triggering the correct activities based on the users input

    To create a new controller, take a copy of this file and name it
    so it ends in controller.py, i.e. foobarcontroller.py
    Make sure it inhetits PresentationController
    Then fill in the blanks. If possible try and make sure it loads
    on all platforms, using for example os.name checks, although
    __init__, check_available and presentation_deleted should always work.
    See impresscontroller, powerpointcontroller or pptviewcontroller
    for examples.

    **Basic Attributes**

    ``name``
        The name that appears in the options and the media manager
    
    ``enabled``
        The controller is enabled

    ``available``
        The controller is available on this machine. Set by init via
        call to check_available
        
    ``plugin``
        The presentationplugin object

    **Hook Functions**
    
    ``kill()``
        Called at system exit to clean up any running presentations

    ``check_available()``
        Returns True if presentation application is installed/can run on this machine
    
    ``presentation_deleted()``
        Deletes presentation specific files, e.g. thumbnails

    ``load_presentation(presentation)``
        Load a presentation file

    ``close_presentation()``
        Close presentation and clean up objects

    ``presentation_loaded()``
        Returns True if presentation is currently loaded

    ``is_active()``
        Returns True if a presentation is currently running
    
    ``blank_screen()``
        Blanks the screen, making it black.

    ``unblank_screen()``
        Unblanks the screen, restoring the output

    ``stop_presentation()``
        Stops the presentation, removing it from the output display

    ``start_presentation()``
        Starts the presentation from the beginning

    ``get_slide_number()``
        Returns the current slide number, from 1

    ``get_slide_count()``
        Returns total number of slides

    ``goto_slide(slide_no)``
        Jumps directly to the requested slide.

    ``next_step()``
       Triggers the next effect of slide on the running presentation

    ``previous_step()``
        Triggers the previous slide on the running presentation

    ``get_slide_preview_file(slide_no)``
        Returns a path to an image containing a preview for the requested slide

    """
    global log
    log = logging.getLogger(u'PresentationController')
    log.info(u'loaded')
    
    def __init__(self, plugin=None, name=u'PresentationController'):
        """
        This is the constructor for the presentationcontroller object.
        This provides an easy way for descendent plugins to populate common data.
        This method *must* be overridden, like so::

            class MyPresentationController(PresentationController):
                def __init__(self, plugin):
                    PresentationController.__init(self, plugin, u'My Presenter App')

        ``plugin``
            Defaults to *None*. The presentationplugin object

        ``name``
            Name of the application, to appear in the application
        """
        self.plugin = plugin
        self.name = name
        self.available = self.check_available()
        self.slidenumber = 0
        if self.available:
            self.enabled = int(plugin.config.get_config(
                name, QtCore.Qt.Unchecked)) == QtCore.Qt.Checked
        else:
            self.enabled = False
        self.thumbnailroot = os.path.join(plugin.config.get_data_path(),
            name, u'thumbnails')
        self.thumbnailprefix = u'slide'
        if not os.path.isdir(self.thumbnailroot):
            os.makedirs(self.thumbnailroot)

    def check_available(self):
        """
        Presentation app is able to run on this machine
        """
        return False

    def presentation_deleted(self, presentation):
        """
        Cleans up/deletes any controller specific files created for
        a file, e.g. thumbnails
        """
        self.store_filename(presentation)
        shutil.rmtree(self.thumbnailpath)
    
    def start_process(self):
        """
        Loads a running version of the presentation application in the background.
        """
        pass

    def kill(self):
        """
        Called at system exit to clean up any running presentations and
        close the application
        """
        log.debug(u'Kill')
        self.close_presentation()

    def load_presentation(self, presentation):
        """
        Called when a presentation is added to the SlideController.
        Loads the presentation and starts it

        ``presentation``
        The file name of the presentations to the run.

        """
        pass

    def store_filename(self, presentation):
        """
        Set properties for the filename and thumbnail paths
        """
        self.filepath = presentation
        self.filename = os.path.split(presentation)[1]
        self.thumbnailpath = os.path.join(self.thumbnailroot, self.filename)
        if not os.path.isdir(self.thumbnailpath):
            os.mkdir(self.thumbnailpath)

    def check_thumbnails(self):
        """
        Returns true if the thumbnail images look to exist and are more
        recent than the powerpoint
        """
        lastimage = self.get_slide_preview_file(self.get_slide_count())
        if not (lastimage and os.path.isfile(lastimage)):
            return False
        imgdate = os.stat(lastimage).st_mtime
        pptdate = os.stat(self.filepath).st_mtime
        return imgdate >= pptdate

    def close_presentation(self):
        """
        Close presentation and clean up objects
        Triggered by new object being added to SlideController
        """
        pass

    def is_active(self):
        """
        Returns True if a presentation is currently running
        """
        return False

    def is_loaded(self):
        """
        Returns true if a presentation is loaded
        """
        return False
    
    def blank_screen(self):
        """
        Blanks the screen, making it black.
        """
        pass

    def unblank_screen(self):
        """
        Unblanks (restores) the presentationn
        """
        pass

    def stop_presentation(self):
        """
        Stops the presentation, removing it from the output display
        """
        pass

    def start_presentation(self):
        """
        Starts the presentation from the beginning
        """
        pass

    def get_slide_number(self):
        """
        Returns the current slide number, from 1
        """
        return 0

    def get_slide_count(self):
        """
        Returns total number of slides
        """
        return 0

    def goto_slide(self, slide_no):
        """
        Jumps directly to the requested slide.

        ``slide_no``
            The slide to jump to, starting at 1
        """
        pass

    def next_step(self):
       """
       Triggers the next effect of slide on the running presentation
       This might be the next animation on the current slide, or the next slide
       """
       pass

    def previous_step(self):
        """
        Triggers the previous slide on the running presentation
        """
        pass

    def get_slide_preview_file(self, slide_no):
        """
        Returns an image path containing a preview for the requested slide

        ``slide_no``
            The slide an image is required for, starting at 1
        """
        return None

    def poll_slidenumber(self, is_live):
        """
        Check the current slide number
        """
        if not self.is_active():
            return
        current = self.get_slide_number()
        if current == self.slidenumber:
            return
        self.slidenumber = current
        if is_live:
            prefix = u'live'
        else:
            prefix = u'preview'
        Receiver().send_message(u'%s_slidecontroller_change' % prefix, 
            self.slidenumber - 1)
