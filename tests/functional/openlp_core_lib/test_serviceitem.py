# -*- coding: utf-8 -*-

"""
    Package to test the openlp.core.lib package.
"""
import os
import json
import tempfile
from unittest import TestCase
from mock import MagicMock, patch

from openlp.core.lib import ItemCapabilities, ServiceItem, Registry
from lxml import objectify, etree

VERSE = 'The Lord said to {r}Noah{/r}: \n'\
        'There\'s gonna be a {su}floody{/su}, {sb}floody{/sb}\n'\
        'The Lord said to {g}Noah{/g}:\n'\
        'There\'s gonna be a {st}floody{/st}, {it}floody{/it}\n'\
        'Get those children out of the muddy, muddy \n'\
        '{r}C{/r}{b}h{/b}{bl}i{/bl}{y}l{/y}{g}d{/g}{pk}'\
        'r{/pk}{o}e{/o}{pp}n{/pp} of the Lord\n'
FOOTER = ['Arky Arky (Unknown)', 'Public Domain', 'CCLI 123456']

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources'))


class TestServiceItem(TestCase):

    def setUp(self):
        """
        Set up the Registry
        """
        Registry.create()
        mocked_renderer = MagicMock()
        mocked_renderer.format_slide.return_value = [VERSE]
        Registry().register('renderer', mocked_renderer)
        Registry().register('image_manager', MagicMock())

    def serviceitem_basic_test(self):
        """
        Test the Service Item - basic test
        """
        # GIVEN: A new service item

        # WHEN: A service item is created (without a plugin)
        service_item = ServiceItem(None)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, 'The new service item should be valid'
        assert service_item.missing_frames() is True, 'There should not be any frames in the service item'

    def serviceitem_load_custom_from_service_test(self):
        """
        Test the Service Item - adding a custom slide from a saved service
        """
        # GIVEN: A new service item and a mocked add icon function
        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        # WHEN: adding a custom from a saved Service
        line = self.convert_file_service_item('serviceitem_custom_1.osj')
        service_item.set_from_service(line)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, 'The new service item should be valid'
        assert len(service_item._display_frames) == 0, 'The service item should have no display frames'
        assert len(service_item.capabilities) == 5, 'There should be 5 default custom item capabilities'
        service_item.render(True)
        assert service_item.get_display_title() == 'Test Custom', 'The title should be "Test Custom"'
        assert service_item.get_frames()[0]['text'] == VERSE[:-1], \
            'The returned text matches the input, except the last line feed'
        assert service_item.get_rendered_frame(1) == VERSE.split('\n', 1)[0], 'The first line has been returned'
        assert service_item.get_frame_title(0) == 'Slide 1', '"Slide 1" has been returned as the title'
        assert service_item.get_frame_title(1) == 'Slide 2', '"Slide 2" has been returned as the title'
        assert service_item.get_frame_title(2) == '', 'Blank has been returned as the title of slide 3'

    def serviceitem_load_image_from_service_test(self):
        """
        Test the Service Item - adding an image from a saved service
        """
        # GIVEN: A new service item and a mocked add icon function
        image_name = 'image_1.jpg'
        test_file = os.path.join(TEST_PATH, image_name)
        frame_array = {'path': test_file, 'title': image_name}

        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        # WHEN: adding an image from a saved Service and mocked exists
        line = self.convert_file_service_item('serviceitem_image_1.osj')
        with patch('openlp.core.ui.servicemanager.os.path.exists') as mocked_exists:
            mocked_exists.return_value = True
            service_item.set_from_service(line, TEST_PATH)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, 'The new service item should be valid'
        assert service_item.get_rendered_frame(0) == test_file, 'The first frame should match the path to the image'
        assert service_item.get_frames()[0] == frame_array, 'The return should match frame array1'
        assert service_item.get_frame_path(0) == test_file, 'The frame path should match the full path to the image'
        assert service_item.get_frame_title(0) == image_name, 'The frame title should match the image name'
        assert service_item.get_display_title() == image_name, 'The display title should match the first image name'
        assert service_item.is_image() is True, 'This service item should be of an "image" type'
        assert service_item.is_capable(ItemCapabilities.CanMaintain) is True, \
            'This service item should be able to be Maintained'
        assert service_item.is_capable(ItemCapabilities.CanPreview) is True, \
            'This service item should be able to be be Previewed'
        assert service_item.is_capable(ItemCapabilities.CanLoop) is True, \
            'This service item should be able to be run in a can be made to Loop'
        assert service_item.is_capable(ItemCapabilities.CanAppend) is True, \
            'This service item should be able to have new items added to it'

    def serviceitem_load_image_from_local_service_test(self):
        """
        Test the Service Item - adding an image from a saved local service
        """
        # GIVEN: A new service item and a mocked add icon function
        image_name1 = 'image_1.jpg'
        image_name2 = 'image_2.jpg'
        test_file1 = os.path.join('/home/openlp', image_name1)
        test_file2 = os.path.join('/home/openlp', image_name2)
        frame_array1 = {'path': test_file1, 'title': image_name1}
        frame_array2 = {'path': test_file2, 'title': image_name2}

        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        service_item2 = ServiceItem(None)
        service_item2.add_icon = MagicMock()

        # WHEN: adding an image from a saved Service and mocked exists
        line = self.convert_file_service_item('serviceitem_image_2.osj')
        line2 = self.convert_file_service_item('serviceitem_image_2.osj', 1)

        with patch('openlp.core.ui.servicemanager.os.path.exists') as mocked_exists:
            mocked_exists.return_value = True
            service_item2.set_from_service(line2)
            service_item.set_from_service(line)


        # THEN: We should get back a valid service item

        # This test is copied from service_item.py, but is changed since to conform to
        # new layout of service item. The layout use in serviceitem_image_2.osd is actually invalid now.
        assert service_item.is_valid is True, 'The first service item should be valid'
        assert service_item2.is_valid is True, 'The second service item should be valid'
        assert service_item.get_rendered_frame(0) == test_file1, 'The first frame should match the path to the image'
        assert service_item2.get_rendered_frame(0) == test_file2, 'The Second frame should match the path to the image'
        assert service_item.get_frames()[0] == frame_array1, 'The return should match the frame array1'
        assert service_item2.get_frames()[0] == frame_array2, 'The return should match the frame array2'
        assert service_item.get_frame_path(0) == test_file1, 'The frame path should match the full path to the image'
        assert service_item2.get_frame_path(0) == test_file2, 'The frame path should match the full path to the image'
        assert service_item.get_frame_title(0) == image_name1, 'The 1st frame title should match the image name'
        assert service_item2.get_frame_title(0) == image_name2, 'The 2nd frame title should match the image name'
        assert service_item.title.lower() == service_item.name, \
            'The plugin name should match the display title, as there are > 1 Images'
        assert service_item.is_image() is True, 'This service item should be of an "image" type'
        assert service_item.is_capable(ItemCapabilities.CanMaintain) is True, \
            'This service item should be able to be Maintained'
        assert service_item.is_capable(ItemCapabilities.CanPreview) is True, \
            'This service item should be able to be be Previewed'
        assert service_item.is_capable(ItemCapabilities.CanLoop) is True, \
            'This service item should be able to be run in a can be made to Loop'
        assert service_item.is_capable(ItemCapabilities.CanAppend) is True, \
            'This service item should be able to have new items added to it'

    def convert_file_service_item(self, name, row=0):
        service_file = os.path.join(TEST_PATH, name)
        try:
            open_file = open(service_file, 'r')
            items = json.load(open_file)
            first_line = items[row]
        except IOError:
            first_line = ''
        finally:
            open_file.close()
        return first_line

