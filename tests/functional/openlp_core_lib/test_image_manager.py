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
"""
Package to test the openlp.core.ui package.
"""
import os

from unittest import TestCase
from PyQt4 import QtGui

from openlp.core.lib import Registry, ImageManager, ScreenList

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources'))


class TestImageManager(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication.instance()
        ScreenList.create(self.app.desktop())
        self.image_manager = ImageManager()

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
        full_path = os.path.normpath(os.path.join(TEST_PATH, 'church.jpg'))
        self.image_manager.add_image(full_path, 'church.jpg', None)

        # WHEN the image is retrieved
        image = self.image_manager.get_image(full_path, 'church.jpg')

        # THEN returned record is a type of image
        self.assertEqual(isinstance(image, QtGui.QImage), True, 'The returned object should be a QImage')

        # WHEN: The image bytes are requested.
        byte_array = self.image_manager.get_image_bytes(full_path, 'church.jpg')

        # THEN: Type should be a str.
        self.assertEqual(isinstance(byte_array, str), True, 'The returned object should be a str')

        # WHEN the image is retrieved has not been loaded
        # THEN a KeyError is thrown
        with self.assertRaises(KeyError) as context:
            self.image_manager.get_image(TEST_PATH, 'church1.jpg')
        self.assertNotEquals(context.exception, '', 'KeyError exception should have been thrown for missing image')

    def different_dimension_image_test(self):
        """
        Test the Image Manager with dimensions
        """
        # GIVEN: add an image with specific dimensions
        full_path = os.path.normpath(os.path.join(TEST_PATH, 'church.jpg'))
        self.image_manager.add_image(full_path, 'church.jpg', None, '80x80')

        # WHEN: the image is retrieved
        image = self.image_manager.get_image(full_path, 'church.jpg', '80x80')

        # THEN: The return should be of type image
        self.assertEqual(isinstance(image, QtGui.QImage), True,
            'The returned object should be a QImage')
        #print(len(self.image_manager._cache))

        # WHEN: adding the same image with different dimensions
        self.image_manager.add_image(full_path, 'church.jpg', None, '100x100')

        # THEN: the cache should contain two pictures
        self.assertEqual(len(self.image_manager._cache), 2,
            'Image manager should consider two dimensions of the same picture as different')

        # WHEN: adding the same image with first dimensions
        self.image_manager.add_image(full_path, 'church.jpg', None, '80x80')

        # THEN: the cache should still contain only two pictures
        self.assertEqual(len(self.image_manager._cache), 2,
            'Same dimensions should not be added again')

        # WHEN: calling with correct image, but wrong dimensions
        with self.assertRaises(KeyError) as context:
            self.image_manager.get_image(full_path, 'church.jpg', '120x120')
        self.assertNotEquals(context.exception, '',
            'KeyError exception should have been thrown for missing dimension')

