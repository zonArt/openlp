# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
"""
Package to test the openlp.core.ui package.
"""
import os
import time
from threading import Lock

from unittest import TestCase
from PyQt4 import QtGui

from openlp.core.common import Registry
from openlp.core.lib import ImageManager, ScreenList
from openlp.core.lib.imagemanager import Priority
from tests.functional import patch
from tests.helpers.testmixin import TestMixin

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources'))


class TestImageManager(TestCase, TestMixin):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.get_application()
        ScreenList.create(self.app.desktop())
        self.image_manager = ImageManager()
        self.lock = Lock()
        self.sleep_time = 0.1

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.app

    def basic_image_manager_test(self):
        """
        Test the Image Manager setup basic functionality
        """
        # GIVEN: the an image add to the image manager
        self.image_manager.add_image(TEST_PATH, 'church.jpg', None)

        # WHEN the image is retrieved
        image = self.image_manager.get_image(TEST_PATH, 'church.jpg')

        # THEN returned record is a type of image
        self.assertEqual(isinstance(image, QtGui.QImage), True, 'The returned object should be a QImage')

        # WHEN: The image bytes are requested.
        byte_array = self.image_manager.get_image_bytes(TEST_PATH, 'church.jpg')

        # THEN: Type should be a str.
        self.assertEqual(isinstance(byte_array, str), True, 'The returned object should be a str')

        # WHEN the image is retrieved has not been loaded
        # THEN a KeyError is thrown
        with self.assertRaises(KeyError) as context:
            self.image_manager.get_image(TEST_PATH, 'church1.jpg')
        self.assertNotEquals(context.exception, '', 'KeyError exception should have been thrown for missing image')

    def process_cache_test(self):
        """
        Test the process_cache method
        """
        with patch('openlp.core.lib.imagemanager.resize_image') as mocked_resize_image, \
                patch('openlp.core.lib.imagemanager.image_to_byte') as mocked_image_to_byte:
            # GIVEN: Mocked functions
            mocked_resize_image.side_effect = self.mocked_resize_image
            mocked_image_to_byte.side_effect = self.mocked_image_to_byte
            image1 = 'church.jpg'
            image2 = 'church2.jpg'
            image3 = 'church3.jpg'
            image4 = 'church4.jpg'

            # WHEN: Add the images. Then get the lock (=queue can not be processed).
            self.lock.acquire()
            self.image_manager.add_image(TEST_PATH, image1, None)
            self.image_manager.add_image(TEST_PATH, image2, None)

            # THEN: All images have been added to the queue, and only the first image is not be in the list anymore, but
            #  is being processed (see mocked methods/functions).
            # Note: Priority.Normal means, that the resize_image() was not completed yet (because afterwards the #
            # priority is adjusted to Priority.Lowest).
            self.assertEqual(self.get_image_priority(image1), Priority.Normal,
                             "image1's priority should be 'Priority.Normal'")
            self.assertEqual(self.get_image_priority(image2), Priority.Normal,
                             "image2's priority should be 'Priority.Normal'")

            # WHEN: Add more images.
            self.image_manager.add_image(TEST_PATH, image3, None)
            self.image_manager.add_image(TEST_PATH, image4, None)
            # Allow the queue to process.
            self.lock.release()
            # Request some "data".
            image_bytes = self.image_manager.get_image_bytes(TEST_PATH, image4)
            image_object = self.image_manager.get_image(TEST_PATH, image3)
            # Now the mocked methods/functions do not have to sleep anymore.
            self.sleep_time = 0
            # Wait for the queue to finish.
            while not self.image_manager._conversion_queue.empty():
                time.sleep(0.1)
            # Because empty() is not reliable, wait a litte; just to make sure.
            time.sleep(0.1)
            # THEN: The images' priority reflect how they were processed.
            self.assertEqual(self.image_manager._conversion_queue.qsize(), 0, "The queue should be empty.")
            self.assertEqual(self.get_image_priority(image1), Priority.Lowest,
                             "The image should have not been requested (=Lowest)")
            self.assertEqual(self.get_image_priority(image2), Priority.Lowest,
                             "The image should have not been requested (=Lowest)")
            self.assertEqual(self.get_image_priority(image3), Priority.Low,
                             "Only the QImage should have been requested (=Low).")
            self.assertEqual(self.get_image_priority(image4), Priority.Urgent,
                             "The image bytes should have been requested (=Urgent).")

    def get_image_priority(self, image):
        """
        This is a help method to get the priority of the given image out of the image_manager's cache.

        NOTE: This requires, that the image has been added to the image manager using the *TEST_PATH*.

        :param image: The name of the image. E. g. ``image1``
        """
        return self.image_manager._cache[(TEST_PATH, image)].priority

    def mocked_resize_image(self, *args):
        """
        This is a mocked method, so that we can control the work flow of the image manager.
        """
        self.lock.acquire()
        self.lock.release()
        # The sleep time is adjusted in the test case.
        time.sleep(self.sleep_time)
        return QtGui.QImage()

    def mocked_image_to_byte(self, *args):
        """
        This is a mocked method, so that we can control the work flow of the image manager.
        """
        self.lock.acquire()
        self.lock.release()
        # The sleep time is adjusted in the test case.
        time.sleep(self.sleep_time)
        return ''