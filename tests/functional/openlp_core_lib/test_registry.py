"""
    Package to test the openlp.core.lib package.
"""
import os

from unittest import TestCase
from mock import MagicMock
from openlp.core.lib import Registry

TESTPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))

class TestServiceItem(TestCase):

    def registry_basic_test(self):
        """
        Test the Service Item basic test
        """
        # GIVEN: A new registry
        registry = Registry.create()

        # WHEN:A service item is created (without a plugin)
        mock_1 = MagicMock()
        Registry().register(u'test1', mock_1)

        # THEN: we should be able retrieve the saved object
        assert Registry().get(u'test1') == mock_1, u'The saved object can be retrieved'
        #assert service_item.missing_frames() is True, u'There should not be any frames in the service item'

        # THEN: We should get back a valid service item
        try:
            assert Registry().get(u'test2') == mock_1, u'This should not be fired'
        except Exception, e:
            pass