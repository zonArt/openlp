"""
    Package to test the openlp.core.lib package.
"""
from unittest import TestCase
from mock import MagicMock, patch
from openlp.core.lib import ServiceItem, Renderer

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
        with patch(u'openlp.core.lib.Plugin') as mocked_plugin:
            #GIVEN: A new service item
            service_item = ServiceItem(mocked_plugin)
            #true_boolean = True
            # WHEN:
            # THEN: We should get back a valid service item
            #assert isinstance(true_result, bool), u'The result should be a boolean'
            assert service_item.is_valid is True, u'A valid Service Item'
            assert service_item.missing_frames() is False, u'No frames loaded yet'

    def serviceitem_add_text_test(self):
        """
        Test the Service Item
        """
        with patch(u'openlp.core.lib.Plugin') as mocked_plugin:
            #GIVEN: A new service item
            service_item = ServiceItem(mocked_plugin)
            #true_boolean = True
            # WHEN: adding text to a service item
            service_item.add_from_text(VERSE)
            service_item.raw_footer = FOOTER
            # THEN: We should get back a valid service item
            #assert isinstance(true_result, bool), u'The result should be a boolean'
            assert service_item.is_valid is True, u'A valid Service Item'
            assert service_item.missing_frames() is True, u'frames loaded '

            #GIVEN: A service item with text
            #WHEN: Render called
            service_item.render(TRUE)
            #THEN: ?