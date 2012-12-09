"""
    Package to test the openlp.core.lib package.
"""
from unittest import TestCase
from mock import MagicMock, patch
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