# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4
"""
This module contains tests for the lib submodule of the Images plugin.
"""

from unittest import TestCase

from mock import MagicMock, patch

from openlp.core.lib import Registry
from openlp.plugins.images.lib.db import ImageFilenames, ImageGroups
from openlp.plugins.images.lib.mediaitem import ImageMediaItem


class TestImageMediaItem(TestCase):
    """
    This is a test case to test various methods in the ImageMediaItem class.
    """

    def setUp(self):
        self.mocked_main_window = MagicMock()
        Registry.create()
        Registry().register('service_list', MagicMock())
        Registry().register('main_window', self.mocked_main_window)
        Registry().register('live_controller', MagicMock())
        mocked_parent = MagicMock()
        mocked_plugin = MagicMock()
        with patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.__init__') as mocked_init:
            mocked_init.return_value = None
            self.media_item = ImageMediaItem(mocked_parent, mocked_plugin)

    def save_new_images_list_empty_list_test(self):
        """
        Test that the save_new_images_list() method handles empty lists gracefully
        """
        # GIVEN: An empty image_list
        image_list = []
        with patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list') as mocked_load_full_list:
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with the empty list
            self.media_item.save_new_images_list(image_list)

            # THEN: The save_object() method should not have been called
            assert self.media_item.manager.save_object.call_count == 0, \
                'The save_object() method should not have been called'

    def save_new_images_list_single_image_with_reload_test(self):
        """
        Test that the save_new_images_list() calls load_full_list() when reload_list is set to True
        """
        # GIVEN: A list with 1 image
        image_list = [ 'test_image.jpg' ]
        with patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list') as mocked_load_full_list:
            ImageFilenames.filename = ''
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with reload_list=True
            self.media_item.save_new_images_list(image_list, reload_list=True)

            # THEN: load_full_list() should have been called
            assert mocked_load_full_list.call_count == 1, 'load_full_list() should have been called'

            # CLEANUP: Remove added attribute from ImageFilenames
            delattr(ImageFilenames, 'filename')

    def save_new_images_list_single_image_without_reload_test(self):
        """
        Test that the save_new_images_list() doesn't call load_full_list() when reload_list is set to False
        """
        # GIVEN: A list with 1 image
        image_list = [ 'test_image.jpg' ]
        with patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list') as mocked_load_full_list:
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with reload_list=False
            self.media_item.save_new_images_list(image_list, reload_list=False)

            # THEN: load_full_list() should not have been called
            assert mocked_load_full_list.call_count == 0, 'load_full_list() should not have been called'

    def save_new_images_list_multiple_images_test(self):
        """
        Test that the save_new_images_list() saves all images in the list
        """
        # GIVEN: A list with 3 images
        image_list = [ 'test_image_1.jpg', 'test_image_2.jpg', 'test_image_3.jpg' ]
        with patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list') as mocked_load_full_list:
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with the list of 3 images
            self.media_item.save_new_images_list(image_list, reload_list=False)

            # THEN: load_full_list() should not have been called
            assert self.media_item.manager.save_object.call_count == 3, \
                'load_full_list() should have been called three times'

    def save_new_images_list_other_objects_in_list_test(self):
        """
        Test that the save_new_images_list() ignores everything in the provided list except strings
        """
        # GIVEN: A list with images and objects
        image_list = [ 'test_image_1.jpg', None, True, ImageFilenames(), 'test_image_2.jpg' ]
        with patch('openlp.plugins.images.lib.mediaitem.ImageMediaItem.load_full_list') as mocked_load_full_list:
            self.media_item.manager = MagicMock()

            # WHEN: We run save_new_images_list with the list of images and objects
            self.media_item.save_new_images_list(image_list, reload_list=False)

            # THEN: load_full_list() should not have been called
            assert self.media_item.manager.save_object.call_count == 2, \
                'load_full_list() should have been called only once'

    def on_reset_click_test(self):
        """
        Test that on_reset_click() actually resets the background
        """
        # GIVEN: A mocked version of reset_action
        self.media_item.reset_action = MagicMock()

        # WHEN: on_reset_click is called
        self.media_item.on_reset_click()

        # THEN: the reset_action should be set visible, and the image should be reset
        self.media_item.reset_action.setVisible.assert_called_with(False)
        self.media_item.live_controller.display.reset_image.assert_called_with()

    def _recursively_delete_group_side_effect(*args, **kwargs):
        """
        Side effect method that creates custom retun values for the recursively_delete_group method
        """
        if args[1] == ImageFilenames and args[2]:
            # Create some fake objects that should be removed
            returned_object1 = ImageFilenames()
            returned_object1.id = 1
            returned_object1.filename = '/tmp/test_file_1.jpg'
            returned_object2 = ImageFilenames()
            returned_object2.id = 2
            returned_object2.filename = '/tmp/test_file_2.jpg'
            returned_object3 = ImageFilenames()
            returned_object3.id = 3
            returned_object3.filename = '/tmp/test_file_3.jpg'
            return [returned_object1, returned_object2, returned_object3]
        if args[1] == ImageGroups and args[2]:
            # Change the parent_id that is matched so we don't get into an endless loop
            ImageGroups.parent_id = 0
            # Create a fake group that will be used in the next run
            returned_object1 = ImageGroups()
            returned_object1.id = 1
            return [returned_object1]
        return []

    def recursively_delete_group_test(self):
        """
        Test that recursively_delete_group() works
        """
        # GIVEN: An ImageGroups object and mocked functions
        with patch('openlp.core.utils.delete_file') as mocked_delete_file:
            ImageFilenames.group_id = 1
            ImageGroups.parent_id = 1
            self.media_item.manager = MagicMock()
            self.media_item.manager.get_all_objects.side_effect = self._recursively_delete_group_side_effect
            self.media_item.servicePath = ""
            test_group = ImageGroups()
            test_group.id = 1

            # WHEN: recursively_delete_group() is called
            self.media_item.recursively_delete_group(test_group)

            # THEN:
            assert mocked_delete_file.call_count == 0, 'delete_file() should not be called'
            assert self.media_item.manager.delete_object.call_count == 7, \
                'manager.delete_object() should be called exactly 7 times'

            # CLEANUP: Remove added attribute from ImageFilenames and ImageGroups
            delattr(ImageFilenames, 'group_id')
            delattr(ImageGroups, 'parent_id')
