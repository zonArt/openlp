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


class ProcessingPriority(object):
    """
    Enumeration class.

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
        self.priority = ProcessingPriority.Normal


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
        self._thread_running = False
        self._cache_dirty = False
        self._image_thread = ImageThread(self)
        self._clean_queue = Queue.PriorityQueue()

    def update_display(self):
        """
        Screen has changed size so rebuild the cache to new size
        """
        log.debug(u'update_display')
        current_screen = ScreenList.get_instance().current
        self.width = current_screen[u'size'].width()
        self.height = current_screen[u'size'].height()
        # mark the images as dirty for a rebuild
        self._clean_queue = Queue.PriorityQueue()
        for key in self._cache.keys():
            image = self._cache[key]
            image.priority = ProcessingPriority.Normal
            image.image = None
            image.image_bytes = None
            self._clean_queue.put_nowait((image.priority, image))
        self._cache_dirty = True
        # only one thread please
        if not self._thread_running:
            self._image_thread.start()

    def get_image(self, name):
        """
        Return the Qimage from the cache
        """
        print u'get_image:', name
        log.debug(u'get_image %s' % name)
        image = self._cache[name]
        if image.image is None:
            image.priority = ProcessingPriority.High
            self._clean_queue.put_nowait((image.priority, image))
            while image.image is None:
                log.debug(u'get_image - waiting')
                time.sleep(0.1)
        return image.image

    def get_image_bytes(self, name):
        """
        Returns the byte string for an image
        If not present wait for the background thread to process it.
        """
        print u'get_image_bytes:', name
        log.debug(u'get_image_bytes %s' % name)
        image = self._cache[name]
        if image.image_bytes is None:
            image.priority = ProcessingPriority.Urgent
            self._clean_queue.put_nowait((image.priority, image))
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
            self._clean_queue.put_nowait((image.priority, image))
        else:
            log.debug(u'Image in cache %s:%s' % (name, path))
        self._cache_dirty = True
        # only one thread please
        if not self._thread_running:
            self._image_thread.start()

    def _process(self):
        """
        Controls the processing called from a ``QtCore.QThread``.
        """
        log.debug(u'_process - started')
        self._thread_running = True
        self._clean_cache()
        # data loaded since we started?
        while self._cache_dirty:
            log.debug(u'_process - recycle')
            self._clean_cache()
        self._thread_running = False
        log.debug(u'_process - ended')

    def _clean_cache(self):
        """
        Actually does the work.
        """
        log.debug(u'_clean_cache')
        if self._clean_queue.empty():
            print u'empty'
            self._cache_dirty = False
            return
        image = self._clean_queue.get_nowait()[1]
        if image.image is None:
            print u'processing (image):', image.name, image.priority
            image.image = resize_image(image.path, self.width, self.height)
            self._clean_queue.task_done()
            if image.priority != ProcessingPriority.Urgent:
                if image.priority == ProcessingPriority.High:
                    image.priority = ProcessingPriority.Normal
                else:
                    image.priority = ProcessingPriority.Low
                self._clean_queue.put_nowait((image.priority, image))
            return
        if image.priority not in [ProcessingPriority.Urgent,
            ProcessingPriority.Low]:
            self._clean_queue.task_done()
            return
        if image.image_bytes is None:
            print u'processing (bytes):', image.name, image.priority
            image.image_bytes = image_to_byte(image.image)
        self._clean_queue.task_done()
