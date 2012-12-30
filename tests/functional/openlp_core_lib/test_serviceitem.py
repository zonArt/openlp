"""
    Package to test the openlp.core.lib package.
"""
from unittest import TestCase
from mock import MagicMock
from openlp.core.lib import ServiceItem

VERSE = u'The Lord said to {r}Noah{/r}: \n'\
        'There\'s gonna be a {su}floody{/su}, {sb}floody{/sb}\n'\
        'The Lord said to {g}Noah{/g}:\n'\
        'There\'s gonna be a {st}floody{/st}, {it}floody{/it}\n'\
        'Get those children out of the muddy, muddy \n'\
        '{r}C{/r}{b}h{/b}{bl}i{/bl}{y}l{/y}{g}d{/g}{pk}'\
        'r{/pk}{o}e{/o}{pp}n{/pp} of the Lord\n'
FOOTER = [u'Arky Arky (Unknown)', u'Public Domain', u'CCLI 123456']

class TestServiceItem(TestCase):

    def serviceitem_basic_test(self):
        """
        Test the Service Item
        """
        #GIVEN: A new service item

        # WHEN:A service item is created (without a plugin)
        service_item = ServiceItem(None)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'A valid Service Item'
        assert service_item.missing_frames() is True, u'No frames loaded yet'

    def serviceitem_add_text_test(self):
        """
        Test the Service Item
        """
        #GIVEN: A new service item
        service_item = ServiceItem(None)

        # WHEN: adding text to a service item
        service_item.add_from_text(VERSE)
        service_item.raw_footer = FOOTER

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'A valid Service Item'
        assert service_item.missing_frames() is False, u'frames loaded '

        #GIVEN: A service item with text
        mocked_renderer =  MagicMock()
        mocked_renderer.format_slide.return_value = [VERSE]
        service_item.renderer = mocked_renderer

        #WHEN: Render called
        assert len(service_item._display_frames) is 0, u'A blank Service Item'
        service_item.render(True)

        #THEN: We should should have a page of output.
        assert len(service_item._display_frames) is 1, u'A valid rendered Service Item has display frames'
        assert service_item.get_rendered_frame(0) == VERSE.split(u'\n')[0], u'A valid render'

    def serviceitem_add_image_test(self):
        """
        Test the Service Item
        """
        #GIVEN: A new service item and a mocked renderer
        service_item = ServiceItem(None)
        service_item.name = u'test'
        mocked_renderer =  MagicMock()
        service_item.renderer = mocked_renderer

        # WHEN: adding image to a service item
        service_item.add_from_image(u'resources/church.jpg', u'Image Title')

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'A valid Service Item'
        assert service_item.missing_frames() is False, u'frames loaded '
        assert len(service_item._display_frames) is 0, u'A blank Service Item'

        #THEN: We should should have a page of output.
        assert len(service_item._raw_frames) is 1, u'A valid rendered Service Item has display frames'
        assert service_item.get_rendered_frame(0) == u'resources/church.jpg'

        # WHEN: adding a second image to a service item
        service_item.add_from_image(u'resources/church.jpg', u'Image1 Title')

        #THEN: We should should have an increased page of output.
        assert len(service_item._raw_frames) is 2, u'A valid rendered Service Item has display frames'
        assert service_item.get_rendered_frame(0) == u'resources/church.jpg'
        assert service_item.get_rendered_frame(0) == service_item.get_rendered_frame(1)

        #When requesting a saved service item
        service = service_item.get_service_repr(True)

        #THEN: We should should have two parts of the service.
        assert len(service) is 2, u'A saved service has two parts'
        assert service[u'header'][u'name']  == u'test' , u'A test plugin'
        assert service[u'data'][0][u'title'] == u'Image Title' , u'The first title name '
        assert service[u'data'][0][u'path'] == u'resources/church.jpg' , u'The first image name'
        assert service[u'data'][0][u'title'] != service[u'data'][1][u'title'], u'The titles should not match'
        assert service[u'data'][0][u'path'] == service[u'data'][1][u'path'], u'The files should match'

        #When validating a service item
        service_item.validate_item([u'jpg'])

        #Then the service item should be valid
        assert service_item.is_valid is True, u'The service item is valid'

    def serviceitem_add_command_test(self):
        """
        Test the Service Item
        """
        #GIVEN: A new service item and a mocked renderer
        service_item = ServiceItem(None)
        service_item.name = u'test'
        mocked_renderer =  MagicMock()
        service_item.renderer = mocked_renderer

        # WHEN: adding image to a service item
        service_item.add_from_command(u'resources', u'church.jpg', u'resources/church.jpg')

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'A valid Service Item'
        assert service_item.missing_frames() is False, u'frames loaded '
        assert len(service_item._display_frames) is 0, u'A blank Service Item'

        #THEN: We should should have a page of output.
        assert len(service_item._raw_frames) is 1, u'A valid rendered Service Item has display frames'
        assert service_item.get_rendered_frame(0) == u'resources/church.jpg'

        #When requesting a saved service item
        service = service_item.get_service_repr(True)

        #THEN: We should should have two parts of the service.
        assert len(service) is 2, u'A saved service has two parts'
        assert service[u'header'][u'name']  == u'test' , u'A test plugin'
        assert service[u'data'][0][u'title'] == u'church.jpg' , u'The first title name '
        assert service[u'data'][0][u'path'] == u'resources' , u'The first image name'
        assert service[u'data'][0][u'image'] == u'resources/church.jpg' , u'The first image name'

        #When validating a service item
        service_item.validate_item([u'jpg'])

        #Then the service item should be valid
        assert service_item.is_valid is True, u'The service item is valid'