# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4
"""
This module contains tests for the lib submodule of the Images plugin.
"""

from unittest import TestCase

from mock import MagicMock, patch

from openlp.core.lib import Registry
from openlp.plugins.images.lib.db import ImageFilenames
from openlp.plugins.images.lib.mediaitem import ImageMediaItem


class TestImageMediaItem(TestCase):
    """
    This is a test case to test various methods in the ImageMediaItem class.
    """

    def setUp(self):
        self.mocked_main_window = MagicMock()
        Registry.create()
        Registry().register(u'service_list', MagicMock())
        Registry().register(u'main_window', self.mocked_main_window)
        mocked_parent = MagicMock()
        mocked_plugin = MagicMock()
        with patch(u'openlp.plugins.images.lib.mediaitem.ImageMediaItem.__init__') as mocked_init:
            mocked_init.return_value = None
            self.media_item = ImageMediaItem(mocked_parent, mocked_plugin)

    def save_new_images_list_empty_list_test(self):
        """
        Test that the save_new_images_list() method handles empty lists gracefully
        """
        # GIVEN: An empty image_list
        image_list = []
        with patch(u'openlp.plugins.images.lib.mediaitem.ImageMediaItem.loadFullList') as mocked_loadFullList:
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with the empty list
            self.media_item.save_new_images_list(image_list)

            # THEN: The save_object() method should not have been called
            assert self.media_item.manager.save_object.call_count == 0, \
                u'The save_object() method should not have been called'

    def save_new_images_list_single_image_with_reload_test(self):
        """
        Test that the save_new_images_list() calls loadFullList() when reload_list is set to True
        """
        # GIVEN: A list with 1 image
        image_list = [ u'test_image.jpg' ]
        with patch(u'openlp.plugins.images.lib.mediaitem.ImageMediaItem.loadFullList') as mocked_loadFullList:
            ImageFilenames.filename = ''
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with reload_list=True
            self.media_item.save_new_images_list(image_list, reload_list=True)

            # THEN: loadFullList() should have been called
            assert mocked_loadFullList.call_count == 1, u'loadFullList() should have been called'

            # CLEANUP: Remove added attribute from ImageFilenames
            delattr(ImageFilenames, 'filename')

    def save_new_images_list_single_image_without_reload_test(self):
        """
        Test that the save_new_images_list() doesn't call loadFullList() when reload_list is set to False
        """
        # GIVEN: A list with 1 image
        image_list = [ u'test_image.jpg' ]
        with patch(u'openlp.plugins.images.lib.mediaitem.ImageMediaItem.loadFullList') as mocked_loadFullList:
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with reload_list=False
            self.media_item.save_new_images_list(image_list, reload_list=False)

            # THEN: loadFullList() should not have been called
            assert mocked_loadFullList.call_count == 0, u'loadFullList() should not have been called'

    def save_new_images_list_multiple_images_test(self):
        """
        Test that the save_new_images_list() saves all images in the list
        """
        # GIVEN: A list with 3 images
        image_list = [ u'test_image_1.jpg', u'test_image_2.jpg', u'test_image_3.jpg' ]
        with patch(u'openlp.plugins.images.lib.mediaitem.ImageMediaItem.loadFullList') as mocked_loadFullList:
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with the list of 3 images
            self.media_item.save_new_images_list(image_list, reload_list=False)

            # THEN: loadFullList() should not have been called
            assert self.media_item.manager.save_object.call_count == 3, \
                u'loadFullList() should have been called three times'

    def save_new_images_list_other_objects_in_list_test(self):
        """
        Test that the save_new_images_list() ignores everything in the provided list except strings
        """
        # GIVEN: A list with images and objects
        image_list = [ u'test_image_1.jpg', None, True, ImageFilenames(), 'test_image_2.jpg' ]
        with patch(u'openlp.plugins.images.lib.mediaitem.ImageMediaItem.loadFullList') as mocked_loadFullList:
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with the list of images and objects
            self.media_item.save_new_images_list(image_list, reload_list=False)

            # THEN: loadFullList() should not have been called
            assert self.media_item.manager.save_object.call_count == 2, \
                u'loadFullList() should have been called only once'
