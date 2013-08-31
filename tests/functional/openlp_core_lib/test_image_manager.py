"""
    Package to test the openlp.core.ui package.
"""

import os
from unittest import TestCase

from PyQt4 import QtCore, QtGui

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
