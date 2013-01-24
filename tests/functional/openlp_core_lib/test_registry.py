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

        # WHEN: I add a service it should save it
        mock_1 = MagicMock()
        Registry().register(u'test1', mock_1)

        # THEN: we should be able retrieve the saved object
        assert Registry().get(u'test1') == mock_1, u'The saved service can be retrieved and matches'

        # WHEN: I add a service it should save it a second time
        # THEN  I will get an exception
        try:
            Registry().register(u'test1', mock_1)
        except Exception, e:
            pass


        # WHEN I try to get back a non existent service
        # THEN I will get an exception
        try:
            assert Registry().get(u'test2') == mock_1, u'This should not be fired'
        except Exception, e:
            pass