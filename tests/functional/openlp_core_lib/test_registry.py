"""
    Package to test the openlp.core.lib package.
"""
import os

from unittest import TestCase
from mock import MagicMock
from openlp.core.lib import Registry

TESTPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))

class TestRegistry(TestCase):

    def registry_basic_test(self):
        """
        Test the registry creation and its usage
        """
        # GIVEN: A new registry
        registry = Registry.create()

        # WHEN: I add a component it should save it
        mock_1 = MagicMock()
        Registry().register(u'test1', mock_1)

        # THEN: we should be able retrieve the saved component
        assert Registry().get(u'test1') == mock_1, u'The saved service can be retrieved and matches'

        # WHEN: I add a component for the second time I am mad.
        # THEN  and I will get an exception
        with self.assertRaises(KeyError) as context:
            Registry().register(u'test1', mock_1)
        self.assertEqual(context.exception[0], u'Duplicate service exception test1',
            u'KeyError exception should have been thrown for duplicate service')

        # WHEN I try to get back a non existent component
        # THEN I will get an exception
        with self.assertRaises(KeyError) as context:
            temp = Registry().get(u'test2')
        self.assertEqual(context.exception[0], u'Service test2 not found in list',
            u'KeyError exception should have been thrown for missing service')

        # WHEN I try to replace a component I should be allowed (testing only)
        Registry().remove(u'test1')
        # THEN I will get an exception
        with self.assertRaises(KeyError) as context:
            temp = Registry().get(u'test1')
        self.assertEqual(context.exception[0], u'Service test1 not found in list',
            u'KeyError exception should have been thrown for deleted service')
