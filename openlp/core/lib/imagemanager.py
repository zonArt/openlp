# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from PyQt4 import QtCore

from openlp.core.lib import resize_image, image_to_byte

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
        self.imageManager.process()


class Image(object):
    name = ''
    path = ''
    dirty = True
    image = None
    image_bytes = None


class ImageManager(QtCore.QObject):
    """
    Image Manager handles the conversion and sizing of images.
    """
    log.info(u'Image Manager loaded')

    def __init__(self):
        QtCore.QObject.__init__(self)
        self._cache = {}
        self._thread_running = False
        self._cache_dirty = False
        self.image_thread = ImageThread(self)

    def update_display(self, width, height):
        """
        Screen has changed size so rebuild the cache to new size
        """
        log.debug(u'update_display')
        self.width = width
        self.height = height
        # mark the images as dirty for a rebuild
        for key in self._cache.keys():
            image = self._cache[key]
            image.dirty = True
            image.image = resize_image(image.path, self.width, self.height)
        self._cache_dirty = True
        # only one thread please
        if not self._thread_running:
            self.image_thread.start()

    def get_image(self, name):
        """
        Return the Qimage from the cache
        """
        log.debug(u'get_image %s' % name)
        return self._cache[name].image

    def get_image_bytes(self, name):
        """
        Returns the byte string for an image
        If not present wait for the background thread to process it.
        """
        log.debug(u'get_image_bytes %s' % name)
        if not self._cache[name].image_bytes:
            while self._cache[name].dirty:
                log.debug(u'get_image_bytes - waiting')
                time.sleep(0.1)
        return self._cache[name].image_bytes

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
            image = Image()
            image.name = name
            image.path = path
            image.image = resize_image(path, self.width, self.height)
            self._cache[name] = image
        else:
            log.debug(u'Image in cache %s:%s' % (name, path))
        self._cache_dirty = True
        # only one thread please
        if not self._thread_running:
            self.image_thread.start()

    def process(self):
        """
        Controls the processing called from a QThread
        """
        log.debug(u'process - started')
        self._thread_running = True
        self.clean_cache()
        # data loaded since we started ?
        while self._cache_dirty:
            log.debug(u'process - recycle')
            self.clean_cache()
        self._thread_running = False
        log.debug(u'process - ended')

    def clean_cache(self):
        """
        Actually does the work.
        """
        log.debug(u'clean_cache')
        # we will clean the cache now
        self._cache_dirty = False
        for key in self._cache.keys():
            image = self._cache[key]
            if image.dirty:
                image.image_bytes = image_to_byte(image.image)
                image.dirty = False
