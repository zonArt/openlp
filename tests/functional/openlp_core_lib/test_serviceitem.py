"""
    Package to test the openlp.core.lib package.
"""
import os
from unittest import TestCase
from mock import MagicMock, patch

from openlp.core.lib import ItemCapabilities, ServiceItem, Registry
from tests.utils.osdinteraction import read_service_from_file
from tests.utils.constants import TEST_RESOURCES_PATH


VERSE = u'The Lord said to {r}Noah{/r}: \n'\
        'There\'s gonna be a {su}floody{/su}, {sb}floody{/sb}\n'\
        'The Lord said to {g}Noah{/g}:\n'\
        'There\'s gonna be a {st}floody{/st}, {it}floody{/it}\n'\
        'Get those children out of the muddy, muddy \n'\
        '{r}C{/r}{b}h{/b}{bl}i{/bl}{y}l{/y}{g}d{/g}{pk}'\
        'r{/pk}{o}e{/o}{pp}n{/pp} of the Lord\n'
FOOTER = [u'Arky Arky (Unknown)', u'Public Domain', u'CCLI 123456']


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

    def serviceitem_add_text_test(self):
        """
        Test the Service Item - add text test
        """
        # GIVEN: A new service item
        service_item = ServiceItem(None)

        # WHEN: adding text to a service item
        service_item.add_from_text(VERSE)
        service_item.raw_footer = FOOTER

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert service_item.missing_frames() is False, u'check frames loaded '

        # WHEN: Render called
        assert len(service_item._display_frames) == 0, u'A blank Service Item with no display frames'
        service_item.render(True)

        # THEN: We should have a page of output.
        assert len(service_item._display_frames) == 1, u'A valid rendered Service Item has 1 display frame'
        assert service_item.get_rendered_frame(0) == VERSE.split(u'\n')[0], u'A output has rendered correctly.'

    def serviceitem_add_image_test(self):
        """
        Test the Service Item - add image test
        """
        # GIVEN: A new service item and a mocked renderer
        service_item = ServiceItem(None)
        service_item.name = u'test'

        # WHEN: adding image to a service item
        test_image = os.path.join(TEST_RESOURCES_PATH, u'church.jpg')
        service_item.add_from_image(test_image, u'Image Title')

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert len(service_item._display_frames) == 0, u'The service item has no display frames'

        # THEN: We should have a page of output.
        assert len(service_item._raw_frames) == 1, u'A valid rendered Service Item has display frames'
        assert service_item.get_rendered_frame(0) == test_image

        # WHEN: adding a second image to a service item
        service_item.add_from_image(test_image, u'Image1 Title')

        # THEN: We should have an increased page of output.
        assert len(service_item._raw_frames) == 2, u'A valid rendered Service Item has display frames'
        assert service_item.get_rendered_frame(0) == test_image
        assert service_item.get_rendered_frame(0) == service_item.get_rendered_frame(1)

        # WHEN requesting a saved service item
        service = service_item.get_service_repr(True)

        # THEN: We should have two parts of the service.
        assert len(service) == 2, u'A saved service should have two parts'
        assert service[u'header'][u'name'] == u'test', u'A test plugin should have been returned'
        assert service[u'data'][0][u'title'] == u'Image Title', u'"Image Title" should be returned as the title'
        assert service[u'data'][0][u'path'] == test_image, u'The returned path should match the inputted path'
        assert service[u'data'][0][u'title'] != service[u'data'][1][u'title'], \
            u'The individual slide titles should not match'
        assert service[u'data'][0][u'path'] == service[u'data'][1][u'path'], u'The file paths should match'

        # WHEN validating a service item
        service_item.validate_item([u'jpg'])

        # THEN the service item should be valid
        assert service_item.is_valid is True, u'The new service item should be valid'

        # WHEN: adding a second image to a service item
        service_item.add_from_image(u'resources/church1.jpg', u'Image1 Title')

        # WHEN validating a service item
        service_item.validate_item([u'jpg'])

        # THEN the service item should be valid
        assert service_item.is_valid is False, u'The service item should not be valid due to validation changes'

    def serviceitem_add_command_test(self):
        """
        Test the Service Item - add command test
        """
        # GIVEN: A new service item and a mocked renderer
        service_item = ServiceItem(None)
        service_item.name = u'test'

        # WHEN: adding image to a service item
        test_file = os.path.join(TEST_RESOURCES_PATH, u'church.jpg')
        service_item.add_from_command(TEST_RESOURCES_PATH, u'church.jpg', test_file)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert len(service_item._display_frames) == 0, u'The service item should have no display frames '

        # THEN: We should have a page of output.
        assert len(service_item._raw_frames) == 1, u'A valid rendered Service Item should have one raw frame'
        assert service_item.get_rendered_frame(0) == test_file, u'The image should match the input'

        # WHEN requesting a saved service item
        service = service_item.get_service_repr(True)

        # THEN: We should have two parts of the service.
        assert len(service) == 2, u'The saved service should have two parts'
        assert service[u'header'][u'name'] == u'test', u'A test plugin should be returned'
        assert service[u'data'][0][u'title'] == u'church.jpg', u'The first title name should be "church,jpg"'
        assert service[u'data'][0][u'path'] == TEST_RESOURCES_PATH, u'The path should match the input path'
        assert service[u'data'][0][u'image'] == test_file, u'The image should match the full path to image'

        # WHEN validating a service item
        service_item.validate_item([u'jpg'])

        # THEN the service item should be valid
        assert service_item.is_valid is True, u'The service item should be valid'

        # WHEN validating a service item with a different suffix
        service_item.validate_item([u'png'])

        # THEN the service item should not be valid
        assert service_item.is_valid is False, u'The service item should not be valid'

    def serviceitem_load_custom_from_service_test(self):
        """
        Test the Service Item - adding a custom slide from a saved service
        """
        # GIVEN: A new service item
        service_item = ServiceItem(None)

        # WHEN: adding a custom from a saved Service
        service = read_service_from_file(u'serviceitem_custom_1.osd')
        service_item.set_from_service(service[0])

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
        # GIVEN: A new service item
        image_name = u'image_1.jpg'
        test_file = os.path.join(TEST_RESOURCES_PATH, image_name)
        frame_array = {u'path': test_file, u'title': image_name}

        service_item = ServiceItem(None)

        # WHEN: adding an image from a saved Service and mocked exists
        service = read_service_from_file(u'serviceitem_image_1.osd')
        with patch('os.path.exists'):
            service_item.set_from_service(service[0], TEST_RESOURCES_PATH)

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
        # GIVEN: A new service item
        image_name1 = u'image_1.jpg'
        image_name2 = u'image_2.jpg'
        test_file1 = os.path.join(u'/home/openlp', image_name1)
        test_file2 = os.path.join(u'/home/openlp', image_name2)
        frame_array1 = {u'path': test_file1, u'title': image_name1}
        frame_array2 = {u'path': test_file2, u'title': image_name2}

        service_item = ServiceItem(None)

        # WHEN: adding an image from a saved Service and mocked exists
        service = read_service_from_file(u'serviceitem_image_2.osd')
        with patch('os.path.exists'):
            service_item.set_from_service(service[0])

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert service_item.get_rendered_frame(0) == test_file1, u'The first frame should match the path to the image'
        assert service_item.get_rendered_frame(1) == test_file2, u'The Second frame should match the path to the image'
        assert service_item.get_frames()[0] == frame_array1, u'The return should match the frame array1'
        assert service_item.get_frames()[1] == frame_array2, u'The return should match the frame array2'
        assert service_item.get_frame_path(0) == test_file1, u'The frame path should match the full path to the image'
        assert service_item.get_frame_path(1) == test_file2, u'The frame path should match the full path to the image'
        assert service_item.get_frame_title(0) == image_name1, u'The 1st frame title should match the image name'
        assert service_item.get_frame_title(1) == image_name2, u'The 2nd frame title should match the image name'
        assert service_item.get_display_title().lower() == service_item.name, \
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

    def serviceitem_migrate_test_20_22(self):
        """
        Test the Service Item - migrating a media only service item from 2.0 to 2.2 format
        """
        # GIVEN: A new service item and a mocked add icon function
        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        # WHEN: adding an media from a saved Service and mocked exists
        line = read_service_from_file(u'migrate_video_20_22.osd')
        with patch('os.path.exists'):
            service_item.set_from_service(line[0], TEST_RESOURCES_PATH)

        # THEN: We should get back a converted service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert service_item.processor == u'VLC', u'The Processor should have been set'
        assert service_item.title is not None, u'The title should be set to a value'
        assert service_item.is_capable(ItemCapabilities.HasDetailedTitleDisplay) is False, \
            u'The Capability should have been removed'
