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

VERSE = u'The Lord said to {r}Noah{/r}: \n'\
        'There\'s gonna be a {su}floody{/su}, {sb}floody{/sb}\n'\
        'The Lord said to {g}Noah{/g}:\n'\
        'There\'s gonna be a {st}floody{/st}, {it}floody{/it}\n'\
        'Get those children out of the muddy, muddy \n'\
        '{r}C{/r}{b}h{/b}{bl}i{/bl}{y}l{/y}{g}d{/g}{pk}'\
        'r{/pk}{o}e{/o}{pp}n{/pp} of the Lord\n'
FOOTER = [u'Arky Arky (Unknown)', u'Public Domain', u'CCLI 123456']

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))


class TestServiceItem(TestCase):

    def setUp(self):
        """
        Set up the Registry
        """
        Registry.create()
        mocked_renderer = MagicMock()
        mocked_renderer.format_slide.return_value = [VERSE]
        Registry().register(u'renderer', mocked_renderer)
        Registry().register(u'image_manager', MagicMock())

    def serviceitem_basic_test(self):
        """
        Test the Service Item - basic test
        """
        # GIVEN: A new service item

        # WHEN: A service item is created (without a plugin)
        service_item = ServiceItem(None)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert service_item.missing_frames() is True, u'There should not be any frames in the service item'

    def serviceitem_load_custom_from_service_test(self):
        """
        Test the Service Item - adding a custom slide from a saved service
        """
        # GIVEN: A new service item and a mocked add icon function
        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        # WHEN: adding a custom from a saved Service
        line = self.convert_file_service_item(u'serviceitem_custom_1.osj')
        service_item.set_from_service(line)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert len(service_item._display_frames) == 0, u'The service item should have no display frames'
        assert len(service_item.capabilities) == 5, u'There should be 5 default custom item capabilities'
        service_item.render(True)
        assert service_item.get_display_title() == u'Test Custom', u'The title should be "Test Custom"'
        assert service_item.get_frames()[0][u'text'] == VERSE[:-1], \
            u'The returned text matches the input, except the last line feed'
        assert service_item.get_rendered_frame(1) == VERSE.split(u'\n', 1)[0], u'The first line has been returned'
        assert service_item.get_frame_title(0) == u'Slide 1', u'"Slide 1" has been returned as the title'
        assert service_item.get_frame_title(1) == u'Slide 2', u'"Slide 2" has been returned as the title'
        assert service_item.get_frame_title(2) == u'', u'Blank has been returned as the title of slide 3'

    def serviceitem_load_image_from_service_test(self):
        """
        Test the Service Item - adding an image from a saved service
        """
        # GIVEN: A new service item and a mocked add icon function
        image_name = u'image_1.jpg'
        test_file = os.path.join(TEST_PATH, image_name)
        frame_array = {u'path': test_file, u'title': image_name}

        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        # WHEN: adding an image from a saved Service and mocked exists
        line = self.convert_file_service_item(u'serviceitem_image_1.osj')
        with patch(u'openlp.core.ui.servicemanager.os.path.exists') as mocked_exists:
            mocked_exists.return_value = True
            service_item.set_from_service(line, TEST_PATH)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert service_item.get_rendered_frame(0) == test_file, u'The first frame should match the path to the image'
        assert service_item.get_frames()[0] == frame_array, u'The return should match frame array1'
        assert service_item.get_frame_path(0) == test_file, u'The frame path should match the full path to the image'
        assert service_item.get_frame_title(0) == image_name, u'The frame title should match the image name'
        assert service_item.get_display_title() == image_name, u'The display title should match the first image name'
        assert service_item.is_image() is True, u'This service item should be of an "image" type'
        assert service_item.is_capable(ItemCapabilities.CanMaintain) is True, \
            u'This service item should be able to be Maintained'
        assert service_item.is_capable(ItemCapabilities.CanPreview) is True, \
            u'This service item should be able to be be Previewed'
        assert service_item.is_capable(ItemCapabilities.CanLoop) is True, \
            u'This service item should be able to be run in a can be made to Loop'
        assert service_item.is_capable(ItemCapabilities.CanAppend) is True, \
            u'This service item should be able to have new items added to it'

    def serviceitem_load_image_from_local_service_test(self):
        """
        Test the Service Item - adding an image from a saved local service
        """
        # GIVEN: A new service item and a mocked add icon function
        image_name1 = u'image_1.jpg'
        image_name2 = u'image_2.jpg'
        test_file1 = os.path.join(u'/home/openlp', image_name1)
        test_file2 = os.path.join(u'/home/openlp', image_name2)
        frame_array1 = {u'path': test_file1, u'title': image_name1}
        frame_array2 = {u'path': test_file2, u'title': image_name2}

        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        service_item2 = ServiceItem(None)
        service_item2.add_icon = MagicMock()

        # WHEN: adding an image from a saved Service and mocked exists
        line = self.convert_file_service_item(u'serviceitem_image_2.osj')
        line2 = self.convert_file_service_item(u'serviceitem_image_2.osj', 1)

        with patch(u'openlp.core.ui.servicemanager.os.path.exists') as mocked_exists:
            mocked_exists.return_value = True
            service_item2.set_from_service(line2)
            service_item.set_from_service(line)


        # THEN: We should get back a valid service item

        # This test is copied from service_item.py, but is changed since to conform to
        # new layout of service item. The layout use in serviceitem_image_2.osd is actually invalid now.
        assert service_item.is_valid is True, u'The first service item should be valid'
        assert service_item2.is_valid is True, u'The second service item should be valid'
        assert service_item.get_rendered_frame(0) == test_file1, u'The first frame should match the path to the image'
        assert service_item2.get_rendered_frame(0) == test_file2, u'The Second frame should match the path to the image'
        assert service_item.get_frames()[0] == frame_array1, u'The return should match the frame array1'
        assert service_item2.get_frames()[0] == frame_array2, u'The return should match the frame array2'
        assert service_item.get_frame_path(0) == test_file1, u'The frame path should match the full path to the image'
        assert service_item2.get_frame_path(0) == test_file2, u'The frame path should match the full path to the image'
        assert service_item.get_frame_title(0) == image_name1, u'The 1st frame title should match the image name'
        assert service_item2.get_frame_title(0) == image_name2, u'The 2nd frame title should match the image name'
        assert service_item.title.lower() == service_item.name, \
            u'The plugin name should match the display title, as there are > 1 Images'
        assert service_item.is_image() is True, u'This service item should be of an "image" type'
        assert service_item.is_capable(ItemCapabilities.CanMaintain) is True, \
            u'This service item should be able to be Maintained'
        assert service_item.is_capable(ItemCapabilities.CanPreview) is True, \
            u'This service item should be able to be be Previewed'
        assert service_item.is_capable(ItemCapabilities.CanLoop) is True, \
            u'This service item should be able to be run in a can be made to Loop'
        assert service_item.is_capable(ItemCapabilities.CanAppend) is True, \
            u'This service item should be able to have new items added to it'

    def convert_file_service_item(self, name, row=0):
        service_file = os.path.join(TEST_PATH, name)
        try:
            open_file = open(service_file, u'r')
            items = json.load(open_file)
            first_line = items[row]
        except IOError:
            first_line = u''
        finally:
            open_file.close()
        return first_line

