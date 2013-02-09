"""
    Package to test the openlp.core.lib package.
"""
import os

from unittest import TestCase
from mock import MagicMock
from openlp.core.lib import Registry

TESTPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))

class TestRegistry(TestCase):

    def registry_service_test(self):
        """
        Test the registry creation and its usage
        """
        # GIVEN: A new registry
        Registry.create()

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

    def registry_function_test(self):
        """
        Test the registry function creation and their usages
        """
        # GIVEN: An existing registry register a function
        Registry.create()
        Registry().register_function(u'test1', self.dummy_function_1)

        # WHEN: I execute the function
        return_value = Registry().execute(u'test1')

        # THEN: I expect then function to have been called and a return given
        self.assertEqual(return_value[0], u'function_1', u'A return value is provided and matches')

        # WHEN: I execute the a function with the same reference and execute the function
        Registry().register_function(u'test1', self.dummy_function_1)
        return_value = Registry().execute(u'test1')

        # THEN: I expect then function to have been called and a return given
        self.assertEqual(return_value, [u'function_1', u'function_1'], u'A return value list is provided and matches')

        # WHEN: I execute the a 2nd function with the different reference and execute the function
        Registry().register_function(u'test2', self.dummy_function_2)
        return_value = Registry().execute(u'test2')

        # THEN: I expect then function to have been called and a return given
        self.assertEqual(return_value[0], u'function_2', u'A return value is provided and matches')

    def dummy_function_1(self):
        return "function_1"

    def dummy_function_2(self):
        return "function_2"