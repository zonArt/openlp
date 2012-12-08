"""
    Package to test the openlp.core.lib package.
"""
from unittest import TestCase
from mock import MagicMock, patch
from openlp.core.lib import ServiceItem

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
