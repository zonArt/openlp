# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
"""
Provides the store and management for Images automatically caching them and
resizing them when needed.  Only one copy of each image is needed in the system.
A Thread is used to convert the image to a byte array so the user does not need
to wait for the conversion to happen.
"""
import logging
import time
import Queue

from PyQt4 import QtCore

from openlp.core.lib import resize_image, image_to_byte
from openlp.core.ui import ScreenList

log = logging.getLogger(__name__)

class ImageThread(QtCore.QThread):
    """
    A special Qt thread class to speed up the display of text based frames.
    This is threaded so it loads the frames in background
    """
    def __init__(self, manager):
        QtCore.QThread.__init__(self, None)
        self.imageManager = manager

    def run(self):
        """
        Run the thread.
        """
        self.imageManager._process()


class Priority(object):
    """
    Enumeration class for different priorities.

    ``Low``
        Only the image's byte stream has to be generated. Neither the QImage nor
        the byte stream has been requested yet.

    ``Normal``
        The image's byte stream as well as the image has to be generated.
        Neither the QImage nor the byte stream has been requested yet.

    ``High``
        The image's byte stream as well as the image has to be generated. The
        QImage for this image has been requested.

    ``Urgent``
        The image's byte stream as well as the image has to be generated. The
        byte stream for this image has been requested.
    """
    Low = 3
    Normal = 2
    High = 1
    Urgent = 0


class Image(object):
    def __init__(self, name='', path=''):
        self.name = name
        self.path = path
        self.image = None
        self.image_bytes = None
        self.priority = Priority.Normal


class PriorityQueue(Queue.PriorityQueue):
    """
    Customised ``Queue.PriorityQueue``.
    """
    def remove(self, item):
        """
        Removes the given ``item`` from the queue.

        ``item``
            The item to remove. This should be a tuple::

                ``(Priority, Image)``
        """
        if item in self.queue:
            self.queue.remove(item)


class ImageManager(QtCore.QObject):
    """
    Image Manager handles the conversion and sizing of images.
    """
    log.info(u'Image Manager loaded')

    def __init__(self):
        QtCore.QObject.__init__(self)
        current_screen = ScreenList.get_instance().current
        self.width = current_screen[u'size'].width()
        self.height = current_screen[u'size'].height()
        self._cache = {}
        self._image_thread = ImageThread(self)
        self._clean_queue = PriorityQueue()

    def update_display(self):
        """
        Screen has changed size so rebuild the cache to new size.
        """
        log.debug(u'update_display')
        current_screen = ScreenList.get_instance().current
        self.width = current_screen[u'size'].width()
        self.height = current_screen[u'size'].height()
        # Mark the images as dirty for a rebuild.
        self._clean_queue = PriorityQueue()
        for key in self._cache.keys():
            image = self._cache[key]
            image.priority = Priority.Normal
            image.image = None
            image.image_bytes = None
            self._clean_queue.put((image.priority, image))
        # We want only one thread.
        if not self._image_thread.isRunning():
            self._image_thread.start()

    def get_image(self, name):
        """
        Return the Qimage from the cache.
        """
        print u'get_image:', name
        log.debug(u'get_image %s' % name)
        image = self._cache[name]
        if image.image is None:
            self._clean_queue.remove((image.priority, image))
            image.priority = Priority.High
            self._clean_queue.put((image.priority, image))
            while image.image is None:
                log.debug(u'get_image - waiting')
                time.sleep(0.1)
        return image.image

    def get_image_bytes(self, name):
        """
        Returns the byte string for an image. If not present wait for the
        background thread to process it.
        """
        print u'get_image_bytes:', name
        log.debug(u'get_image_bytes %s' % name)
        image = self._cache[name]
        if image.image_bytes is None:
            self._clean_queue.remove((image.priority, image))
            image.priority = Priority.Urgent
            self._clean_queue.put((image.priority, image))
            while image.image_bytes is None:
                log.debug(u'get_image_bytes - waiting')
                time.sleep(0.1)
        return image.image_bytes

    def del_image(self, name):
        """
        Delete the Image from the Cache
        """
        log.debug(u'del_image %s' % name)
        if name in self._cache:
            del self._cache[name]

    def add_image(self, name, path):
        """
        Add image to cache if it is not already there
        """
        log.debug(u'add_image %s:%s' % (name, path))
        if not name in self._cache:
            image = Image(name, path)
            self._cache[name] = image
            self._clean_queue.put((image.priority, image))
        else:
            log.debug(u'Image in cache %s:%s' % (name, path))
        # We want only one thread.
        if not self._image_thread.isRunning():
            self._image_thread.start()

    def _process(self):
        """
        Controls the processing called from a ``QtCore.QThread``.
        """
        log.debug(u'_process - started')
        while not self._clean_queue.empty():
            self._clean_cache()
        print u'empty'
        log.debug(u'_process - ended')

    def _clean_cache(self):
        """
        Actually does the work.
        """
        log.debug(u'_clean_cache')
        image = self._clean_queue.get()[1]
        if image.image is None:
            print u'processing (image):', image.name, image.priority
            image.image = resize_image(image.path, self.width, self.height)
            if image.priority != Priority.Urgent:
                self._clean_queue.task_done()
                self._clean_queue.remove((image.priority, image))
                image.priority = Priority.Low
                self._clean_queue.put((image.priority, image))
                return
        if image.image_bytes is None:
            print u'processing (bytes):', image.name, image.priority
            image.image_bytes = image_to_byte(image.image)
            self._clean_queue.task_done()
