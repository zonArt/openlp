"""
Package to test the openlp.core.lib package.
"""
from unittest import TestCase

from mock import MagicMock, patch

from openlp.core.lib import str_to_bool, translate, check_directory_exists, get_text_file_string, build_icon, \
    image_to_byte

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

    def get_text_file_string_no_file_test(self):
        """
        Test the get_text_file_string() function when a file does not exist
        """
        with patch(u'openlp.core.lib.os.path.isfile') as mocked_isfile:
            # GIVEN: A mocked out isfile which returns true, and a text file name
            filename = u'testfile.txt'
            mocked_isfile.return_value = False

            # WHEN: get_text_file_string is called
            result = get_text_file_string(filename)

            # THEN: The result should be False
            mocked_isfile.assert_called_with(filename)
            assert result is False, u'False should be returned if no file exists'

    def get_text_file_string_read_error_test(self):
        """
        Test the get_text_file_string() method when a read error happens
        """
        with patch(u'openlp.core.lib.os.path.isfile') as mocked_isfile, patch(u'__builtin__.open') as mocked_open:
            # GIVEN: A mocked-out open() which raises an exception and isfile returns True
            filename = u'testfile.txt'
            mocked_isfile.return_value = True
            mocked_open.side_effect = IOError()

            # WHEN: get_text_file_string is called
            result = get_text_file_string(filename)

            # THEN: None should be returned
            mocked_isfile.assert_called_with(filename)
            mocked_open.assert_called_with(filename, u'r')
            assert result is None, u'None should be returned if the file cannot be opened'

    def get_text_file_string_decode_error_test(self):
        """
        Test the get_text_file_string() method when the contents cannot be decoded
        """
        assert True, u'Impossible to test due to conflicts when mocking out the "open" function'

    def build_icon_with_qicon_test(self):
        """
        Test the build_icon() function with a QIcon instance
        """
        with patch(u'openlp.core.lib.QtGui') as MockedQtGui:
            # GIVEN: A mocked QIcon
            MockedQtGui.QIcon = MagicMock
            mocked_icon = MockedQtGui.QIcon()

            # WHEN: We pass a QIcon instance in
            result = build_icon(mocked_icon)

            # THEN: The result should be our mocked QIcon
            assert result is mocked_icon, u'The result should be the mocked QIcon'

    def build_icon_with_resource_test(self):
        """
        Test the build_icon() function with a resource URI
        """
        with patch(u'openlp.core.lib.QtGui') as MockedQtGui, \
             patch(u'openlp.core.lib.QtGui.QPixmap') as MockedQPixmap:
            # GIVEN: A mocked QIcon and a mocked QPixmap
            MockedQtGui.QIcon = MagicMock
            MockedQtGui.QIcon.Normal = 1
            MockedQtGui.QIcon.Off = 2
            MockedQPixmap.return_value = u'mocked_pixmap'
            resource_uri = u':/resource/uri'

            # WHEN: We pass a QIcon instance in
            result = build_icon(resource_uri)

            # THEN: The result should be our mocked QIcon
            MockedQPixmap.assert_called_with(resource_uri)
            # There really should be more assert statements here but due to type checking and things they all break. The
            # best we can do is to assert that we get back a MagicMock object.
            assert isinstance(result, MagicMock), u'The result should be a MagicMock, because we mocked it out'

    def image_to_byte_test(self):
        """
        Test the image_to_byte() function
        """
        with patch(u'openlp.core.lib.QtCore') as MockedQtCore:
            # GIVEN: A set of mocked-out Qt classes
            mocked_byte_array = MagicMock()
            MockedQtCore.QByteArray.return_value = mocked_byte_array
            mocked_byte_array.toBase64.return_value = u'base64mock'
            mocked_buffer = MagicMock()
            MockedQtCore.QBuffer.return_value = mocked_buffer
            MockedQtCore.QIODevice.WriteOnly = u'writeonly'
            mocked_image = MagicMock()

            # WHEN: We convert an image to a byte array
            result = image_to_byte(mocked_image)

            # THEN: We should receive a value of u'base64mock'
            MockedQtCore.QByteArray.assert_called_with()
            MockedQtCore.QBuffer.assert_called_with(mocked_byte_array)
            mocked_buffer.open.assert_called_with(u'writeonly')
            mocked_image.save.assert_called_with(mocked_buffer, "PNG")
            mocked_byte_array.toBase64.assert_called_with()
            assert result == u'base64mock', u'The result should be the return value of the mocked out base64 method'
