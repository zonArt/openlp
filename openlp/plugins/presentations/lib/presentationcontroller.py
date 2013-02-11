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

import logging
import os
import shutil

from PyQt4 import QtCore

from openlp.core.lib import Receiver, Registry, Settings, check_directory_exists, create_thumb, validate_thumb
from openlp.core.utils import AppLocation

log = logging.getLogger(__name__)

class PresentationDocument(object):
    """
    Base class for presentation documents to inherit from.
    Loads and closes the presentation as well as triggering the correct
    activities based on the users input

    **Hook Functions**

    ``load_presentation()``
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

    ``is_blank``
        Returns true if screen is blank

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

    ``get_thumbnail_path(slide_no, check_exists)``
        Returns a path to an image containing a preview for the requested slide

    """
    def __init__(self, controller, name):
        """
        Constructor for the PresentationController class
        """
        self.slidenumber = 0
        self.controller = controller
        self.filepath = name
        check_directory_exists(self.get_thumbnail_folder())

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController. Loads the
        presentation and starts it.

        Returns False if the file could not be opened
        """
        return False

    def presentation_deleted(self):
        """
        Cleans up/deletes any controller specific files created for
        a file, e.g. thumbnails
        """
        try:
            shutil.rmtree(self.get_thumbnail_folder())
            shutil.rmtree(self.get_temp_folder())
        except OSError:
            log.exception(u'Failed to delete presentation controller files')

    def get_file_name(self):
        """
        Return just the filename of the presentation, without the directory
        """
        return os.path.split(self.filepath)[1]

    def get_thumbnail_folder(self):
        """
        The location where thumbnail images will be stored
        """
        return os.path.join(
            self.controller.thumbnail_folder, self.get_file_name())

    def get_temp_folder(self):
        """
        The location where thumbnail images will be stored
        """
        return os.path.join(
            self.controller.temp_folder, self.get_file_name())

    def check_thumbnails(self):
        """
        Returns ``True`` if the thumbnail images exist and are more recent than
        the powerpoint file.
        """
        lastimage = self.get_thumbnail_path(self.get_slide_count(), True)
        if not (lastimage and os.path.isfile(lastimage)):
            return False
        return validate_thumb(self.filepath, lastimage)

    def close_presentation(self):
        """
        Close presentation and clean up objects
        Triggered by new object being added to SlideController
        """
        self.controller.close_presentation()

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
        Unblanks (restores) the presentation
        """
        pass

    def is_blank(self):
        """
        Returns true if screen is blank
        """
        return False

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

    def convert_thumbnail(self, file, idx):
        """
        Convert the slide image the application made to a standard 320x240
        .png image.
        """
        if self.check_thumbnails():
            return
        if os.path.isfile(file):
            thumb_path = self.get_thumbnail_path(idx, False)
            create_thumb(file, thumb_path, False, QtCore.QSize(320, 240))

    def get_thumbnail_path(self, slide_no, check_exists):
        """
        Returns an image path containing a preview for the requested slide

        ``slide_no``
            The slide an image is required for, starting at 1
        """
        path = os.path.join(self.get_thumbnail_folder(),
            self.controller.thumbnail_prefix + unicode(slide_no) + u'.png')
        if os.path.isfile(path) or not check_exists:
            return path
        else:
            return None

    def poll_slidenumber(self, is_live, hide_mode):
        """
        Check the current slide number
        """
        if not self.is_active():
            return
        if not hide_mode:
            current = self.get_slide_number()
            if current == self.slidenumber:
                return
            self.slidenumber = current
        if is_live:
            prefix = u'live'
        else:
            prefix = u'preview'
        Receiver.send_message(u'slidecontroller_%s_change' % prefix, self.slidenumber - 1)

    def get_slide_text(self, slide_no):
        """
        Returns the text on the slide

        ``slide_no``
        The slide the text is required for, starting at 1
        """
        return ''

    def get_slide_notes(self, slide_no):
        """
        Returns the text on the slide

        ``slide_no``
        The slide the notes are required for, starting at 1
        """
        return ''


class PresentationController(object):
    """
    This class is used to control interactions with presentation applications
    by creating a runtime environment. This is a base class for presentation
    controllers to inherit from.

    To create a new controller, take a copy of this file and name it so it ends
    with ``controller.py``, i.e. ``foobarcontroller.py``. Make sure it inherits
    :class:`~openlp.plugins.presentations.lib.presentationcontroller.PresentationController`,
    and then fill in the blanks. If possible try to make sure it loads on all
    platforms, usually by using :mod:``os.name`` checks, although
    ``__init__``, ``check_available`` and ``presentation_deleted`` should
    always be implemented.

    See :class:`~openlp.plugins.presentations.lib.impresscontroller.ImpressController`,
    :class:`~openlp.plugins.presentations.lib.powerpointcontroller.PowerpointController` or
    :class:`~openlp.plugins.presentations.lib.pptviewcontroller.PptviewController`
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

    ``supports``
        The primary native file types this application supports

    ``alsosupports``
        Other file types the application can import, although not necessarily
        the first choice due to potential incompatibilities

    **Hook Functions**

    ``kill()``
        Called at system exit to clean up any running presentations

    ``check_available()``
        Returns True if presentation application is installed/can run on this
        machine

    ``presentation_deleted()``
        Deletes presentation specific files, e.g. thumbnails

    """
    log.info(u'PresentationController loaded')

    def __init__(self, plugin=None, name=u'PresentationController',
        document_class=PresentationDocument):
        """
        This is the constructor for the presentationcontroller object. This
        provides an easy way for descendent plugins to populate common data.
        This method *must* be overridden, like so::

            class MyPresentationController(PresentationController):
                def __init__(self, plugin):
                    PresentationController.__init(
                        self, plugin, u'My Presenter App')

        ``plugin``
            Defaults to *None*. The presentationplugin object

        ``name``
            Name of the application, to appear in the application
        """
        self.supports = []
        self.alsosupports = []
        self.docs = []
        self.plugin = plugin
        self.name = name
        self.document_class = document_class
        self.settings_section = self.plugin.settingsSection
        self.available = None
        self.temp_folder = os.path.join(AppLocation.get_section_data_path(self.settings_section), name)
        self.thumbnail_folder = os.path.join(AppLocation.get_section_data_path(self.settings_section), u'thumbnails')
        self.thumbnail_prefix = u'slide'
        check_directory_exists(self.thumbnail_folder)
        check_directory_exists(self.temp_folder)

    def enabled(self):
        """
        Return whether the controller is currently enabled
        """
        if Settings().value(self.settings_section + u'/' + self.name) == QtCore.Qt.Checked:
            return self.is_available()
        else:
            return False

    def is_available(self):
        if self.available is None:
            self.available = self.check_available()
        return self.available

    def check_available(self):
        """
        Presentation app is able to run on this machine
        """
        return False

    def start_process(self):
        """
        Loads a running version of the presentation application in the
        background.
        """
        pass

    def kill(self):
        """
        Called at system exit to clean up any running presentations and
        close the application
        """
        log.debug(u'Kill')
        self.close_presentation()

    def add_document(self, name):
        """
        Called when a new presentation document is opened
        """
        document = self.document_class(self, name)
        self.docs.append(document)
        return document

    def remove_doc(self, doc=None):
        """
        Called to remove an open document from the collection
        """
        log.debug(u'remove_doc Presentation')
        if doc is None:
            return
        if doc in self.docs:
            self.docs.remove(doc)

    def close_presentation(self):
        pass

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, u'_plugin_manager'):
            self._plugin_manager = Registry().get(u'plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)
