"""
Package to test the openlp.core.lib package.
"""
from unittest import TestCase

from mock import MagicMock, patch

from openlp.core.lib import str_to_bool, translate, check_directory_exists

class TestLib(TestCase):

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

    def translate_test(self):
        """
        Test the translate() function
        """
        # GIVEN: A string to translate and a mocked Qt translate function
        context = u'OpenLP.Tests'
        text = u'Untranslated string'
        comment = u'A comment'
        encoding = 1
        n = 1
        mocked_translate = MagicMock(return_value=u'Translated string')

        # WHEN: we call the translate function
        result = translate(context, text, comment, encoding, n, mocked_translate)

        # THEN: the translated string should be returned, and the mocked function should have been called
        mocked_translate.assert_called_with(context, text, comment, encoding, n)
        assert result == u'Translated string', u'The translated string should have been returned'

    def check_directory_exists_test(self):
        """
        Test the check_directory_exists() function
        """
        with patch(u'openlp.core.lib.os.path.exists') as mocked_exists, \
             patch(u'openlp.core.lib.os.makedirs') as mocked_makedirs:
            # GIVEN: A directory to check and a mocked out os.makedirs and os.path.exists
            directory_to_check = u'existing/directory'

            # WHEN: os.path.exists returns True and we check to see if the directory exists
            mocked_exists.return_value = True
            check_directory_exists(directory_to_check)

            # THEN: Only os.path.exists should have been called
            mocked_exists.assert_called_with(directory_to_check)
            assert not mocked_makedirs.called, u'os.makedirs should not have been called'

            # WHEN: os.path.exists returns False and we check the directory exists
            mocked_exists.return_value = False
            check_directory_exists(directory_to_check)

            # THEN: Both the mocked functions should have been called
            mocked_exists.assert_called_with(directory_to_check)
            mocked_makedirs.assert_called_with(directory_to_check)

            # WHEN: os.path.exists raises an IOError
            mocked_exists.side_effect = IOError()
            check_directory_exists(directory_to_check)

            # THEN: We shouldn't get an exception though the mocked exists has been called
            mocked_exists.assert_called_with(directory_to_check)

            # WHEN: Some other exception is raised
            mocked_exists.side_effect = ValueError()

            # THEN: check_directory_exists raises an exception
            mocked_exists.assert_called_with(directory_to_check)
            self.assertRaises(ValueError, check_directory_exists, directory_to_check)
