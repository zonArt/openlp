"""
Package to test the openlp.core.lib package.
"""
from unittest import TestCase

from openlp.core.lib import str_to_bool

class TestLibModule(TestCase):

    def str_to_bool_with_bool_test(self):
        """
        Test the str_to_bool function with boolean input
        """
        #GIVEN: A boolean value set to true
        true_boolean = True

        # WHEN: We "convert" it to a bool
        true_result = str_to_bool(true_boolean)

        # THEN: We should get back a True bool
        assert isinstance(true_result, bool), u'The result should be a boolean'
        assert true_result is True, u'The result should be True'

        #GIVEN: A boolean value set to false
        false_boolean = False

        # WHEN: We "convert" it to a bool
        false_result = str_to_bool(false_boolean)

        # THEN: We should get back a True bool
        assert isinstance(false_result, bool), u'The result should be a boolean'
        assert false_result is False, u'The result should be True'

    def str_to_bool_with_invalid_test(self):
        """
        Test the str_to_bool function with a set of invalid inputs
        """
        # GIVEN: An integer value
        int_string = 1

        # WHEN: we convert it to a bool
        int_result = str_to_bool(int_string)

        # THEN: we should get back a false
        assert int_result is False, u'The result should be False'

        # GIVEN: An string value with completely invalid input
        invalid_string = u'my feet are wet'

        # WHEN: we convert it to a bool
        str_result = str_to_bool(invalid_string)

        # THEN: we should get back a false
        assert str_result is False, u'The result should be False'

    def str_to_bool_with_false_values_test(self):
        """
        Test the str_to_bool function with a set of false inputs
        """
        # GIVEN: A string set to "false"
        false_string = u'false'

        # WHEN: we convert it to a bool
        false_result = str_to_bool(false_string)

        # THEN: we should get back a false
        assert false_result is False, u'The result should be False'

        # GIVEN: An string set to "NO"
        no_string = u'NO'

        # WHEN: we convert it to a bool
        str_result = str_to_bool(no_string)

        # THEN: we should get back a false
        assert str_result is False, u'The result should be False'

    def str_to_bool_with_true_values_test(self):
        """
        Test the str_to_bool function with a set of true inputs
        """
        # GIVEN: A string set to "True"
        true_string = u'True'

        # WHEN: we convert it to a bool
        true_result = str_to_bool(true_string)

        # THEN: we should get back a true
        assert true_result is True, u'The result should be True'

        # GIVEN: An string set to "yes"
        yes_string = u'yes'

        # WHEN: we convert it to a bool
        str_result = str_to_bool(yes_string)

        # THEN: we should get back a true
        assert str_result is True, u'The result should be True'

