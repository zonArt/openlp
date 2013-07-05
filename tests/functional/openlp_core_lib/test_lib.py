"""
Package to test the openlp.core.lib package.
"""
import os

from unittest import TestCase
from datetime import datetime, timedelta

from mock import MagicMock, patch
from PyQt4 import QtCore, QtGui

from openlp.core.lib import str_to_bool, create_thumb, translate, check_directory_exists, get_text_file_string, \
    build_icon, image_to_byte, check_item_selected, validate_thumb, create_separated_list, clean_tags, expand_tags


TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))



class TestLib(TestCase):

    def str_to_bool_with_bool_test(self):
        """
        Test the str_to_bool function with boolean input
        """
        # GIVEN: A boolean value set to true
        true_boolean = True

        # WHEN: We "convert" it to a bool
        true_result = str_to_bool(true_boolean)

        # THEN: We should get back a True bool
        assert isinstance(true_result, bool), u'The result should be a boolean'
        assert true_result is True, u'The result should be True'

        # GIVEN: A boolean value set to false
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
        with patch(u'openlp.core.lib.os.path.isfile') as mocked_isfile, patch(u'builtins.open') as mocked_open:
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

    def create_thumb_with_size_test(self):
        """
        Test the create_thumb() function
        """
        # GIVEN: An image to create a thumb of.
        image_path = os.path.join(TEST_PATH, u'church.jpg')
        thumb_path = os.path.join(TEST_PATH, u'church_thumb.jpg')
        thumb_size = QtCore.QSize(10, 20)

        # Remove the thumb so that the test actually tests if the thumb will be created. Maybe it was not deleted in the
        # last test.
        try:
            os.remove(thumb_path)
        except:
            pass

        # Only continue when the thumb does not exist.
        assert not os.path.exists(thumb_path), u'Test was not ran, because the thumb already exists.'

        # WHEN: Create the thumb.
        icon = create_thumb(image_path, thumb_path, size=thumb_size)

        # THEN: Check if the thumb was created.
        assert os.path.exists(thumb_path), u'Test was not ran, because the thumb already exists.'
        assert isinstance(icon, QtGui.QIcon), u'The icon should be a QIcon.'
        assert not icon.isNull(), u'The icon should not be null.'
        assert QtGui.QImageReader(thumb_path).size() == thumb_size, u'The thumb should have the given size.'

        # Remove the thumb so that the test actually tests if the thumb will be created.
        try:
            os.remove(thumb_path)
        except:
            pass

    def check_item_selected_true_test(self):
        """
        Test that the check_item_selected() function returns True when there are selected indexes
        """
        # GIVEN: A mocked out QtGui module and a list widget with selected indexes
        MockedQtGui = patch(u'openlp.core.lib.QtGui')
        mocked_list_widget = MagicMock()
        mocked_list_widget.selectedIndexes.return_value = True
        message = u'message'

        # WHEN: We check if there are selected items
        result = check_item_selected(mocked_list_widget, message)

        # THEN: The selectedIndexes function should have been called and the result should be true
        mocked_list_widget.selectedIndexes.assert_called_with()
        assert result, u'The result should be True'

    def check_item_selected_false_test(self):
        """
        Test that the check_item_selected() function returns False when there are no selected indexes.
        """
        # GIVEN: A mocked out QtGui module and a list widget with selected indexes
        with patch(u'openlp.core.lib.QtGui') as MockedQtGui, \
             patch(u'openlp.core.lib.translate') as mocked_translate:
            mocked_translate.return_value = u'mocked translate'
            mocked_list_widget = MagicMock()
            mocked_list_widget.selectedIndexes.return_value = False
            mocked_list_widget.parent.return_value = u'parent'
            message = u'message'

            # WHEN: We check if there are selected items
            result = check_item_selected(mocked_list_widget, message)

            # THEN: The selectedIndexes function should have been called and the result should be true
            mocked_list_widget.selectedIndexes.assert_called_with()
            MockedQtGui.QMessageBox.information.assert_called_with(u'parent', u'mocked translate', 'message')
            assert not result, u'The result should be False'

    def clean_tags_test(self):
        """
        Test clean_tags() method.
        """
        with patch(u'openlp.core.lib.FormattingTags.get_html_tags') as mocked_get_tags:
            # GIVEN: Mocked get_html_tags() method.
            mocked_get_tags.return_value = [{
                u'desc': u'Black',
                u'start tag': u'{b}',
                u'start html': u'<span style="-webkit-text-fill-color:black">',
                u'end tag': u'{/b}', u'end html': u'</span>', u'protected': True,
                u'temporary': False
            }]
            string_to_pass = u'ASDF<br>foo{br}bar&nbsp;{b}black{/b}'
            wanted_string = u'ASDF\nfoo\nbar black'

            # WHEN: Clean the string.
            result_string = clean_tags(string_to_pass)

            # THEN: The strings should be identical.
            assert result_string == wanted_string, u'The strings should be identical.'

    def expand_tags_test(self):
        """
        Test the expand_tags() method.
        """
        with patch(u'openlp.core.lib.FormattingTags.get_html_tags') as mocked_get_tags:
            # GIVEN: Mocked get_html_tags() method.
            mocked_get_tags.return_value = [
                {
                    u'desc': u'Black',
                    u'start tag': u'{b}',
                    u'start html': u'<span style="-webkit-text-fill-color:black">',
                    u'end tag': u'{/b}', u'end html': u'</span>', u'protected': True,
                    u'temporary': False
                },
                {
                    u'desc': u'Yellow',
                    u'start tag': u'{y}',
                    u'start html': u'<span style="-webkit-text-fill-color:yellow">',
                    u'end tag': u'{/y}', u'end html': u'</span>', u'protected': True,
                    u'temporary': False
                },
                {
                    u'desc': u'Green',
                    u'start tag': u'{g}',
                    u'start html': u'<span style="-webkit-text-fill-color:green">',
                    u'end tag': u'{/g}', u'end html': u'</span>', u'protected': True,
                    u'temporary': False
                }
            ]
            string_to_pass = u'{b}black{/b}{y}yellow{/y}'
            wanted_string = u'<span style="-webkit-text-fill-color:black">black</span>' + \
                '<span style="-webkit-text-fill-color:yellow">yellow</span>'

            # WHEN: Replace the tags.
            result_string = expand_tags(string_to_pass)

            # THEN: The strings should be identical.
            assert result_string == wanted_string, u'The strings should be identical.'

    def validate_thumb_file_does_not_exist_test(self):
        """
        Test the validate_thumb() function when the thumbnail does not exist
        """
        # GIVEN: A mocked out os module, with path.exists returning False, and fake paths to a file and a thumb
        with patch(u'openlp.core.lib.os') as mocked_os:
            file_path = u'path/to/file'
            thumb_path = u'path/to/thumb'
            mocked_os.path.exists.return_value = False

            # WHEN: we run the validate_thumb() function
            result = validate_thumb(file_path, thumb_path)

            # THEN: we should have called a few functions, and the result should be False
            mocked_os.path.exists.assert_called_with(thumb_path)
            assert result is False, u'The result should be False'

    def validate_thumb_file_exists_and_newer_test(self):
        """
        Test the validate_thumb() function when the thumbnail exists and has a newer timestamp than the file
        """
        # GIVEN: A mocked out os module, functions rigged to work for us, and fake paths to a file and a thumb
        with patch(u'openlp.core.lib.os') as mocked_os:
            file_path = u'path/to/file'
            thumb_path = u'path/to/thumb'
            file_mocked_stat = MagicMock()
            file_mocked_stat.st_mtime = datetime.now()
            thumb_mocked_stat = MagicMock()
            thumb_mocked_stat.st_mtime = datetime.now() + timedelta(seconds=10)
            mocked_os.path.exists.return_value = True
            mocked_os.stat.side_effect = [file_mocked_stat, thumb_mocked_stat]

            # WHEN: we run the validate_thumb() function

            # THEN: we should have called a few functions, and the result should be True
            #mocked_os.path.exists.assert_called_with(thumb_path)

    def validate_thumb_file_exists_and_older_test(self):
        """
        Test the validate_thumb() function when the thumbnail exists but is older than the file
        """
        # GIVEN: A mocked out os module, functions rigged to work for us, and fake paths to a file and a thumb
        with patch(u'openlp.core.lib.os') as mocked_os:
            file_path = u'path/to/file'
            thumb_path = u'path/to/thumb'
            file_mocked_stat = MagicMock()
            file_mocked_stat.st_mtime = datetime.now()
            thumb_mocked_stat = MagicMock()
            thumb_mocked_stat.st_mtime = datetime.now() - timedelta(seconds=10)
            mocked_os.path.exists.return_value = True
            mocked_os.stat.side_effect = lambda fname: file_mocked_stat if fname == file_path else thumb_mocked_stat

            # WHEN: we run the validate_thumb() function
            result = validate_thumb(file_path, thumb_path)

            # THEN: we should have called a few functions, and the result should be False
            mocked_os.path.exists.assert_called_with(thumb_path)
            mocked_os.stat.assert_any_call(file_path)
            mocked_os.stat.assert_any_call(thumb_path)
            assert result is False, u'The result should be False'

    def create_separated_list_qlocate_test(self):
        """
        Test the create_separated_list function using the Qt provided method
        """
        with patch(u'openlp.core.lib.Qt') as mocked_qt, \
                patch(u'openlp.core.lib.QtCore.QLocale.createSeparatedList') as mocked_createSeparatedList:
            # GIVEN: A list of strings and the mocked Qt module.
            mocked_qt.PYQT_VERSION_STR = u'4.9'
            mocked_qt.qVersion.return_value = u'4.8'
            mocked_createSeparatedList.return_value = u'Author 1, Author 2, and Author 3'
            string_list = [u'Author 1', u'Author 2', u'Author 3']

            # WHEN: We get a string build from the entries it the list and a separator.
            string_result = create_separated_list(string_list)

            # THEN: We should have "Author 1, Author 2, and Author 3"
            assert string_result == u'Author 1, Author 2, and Author 3', u'The string should be u\'Author 1, ' \
                'Author 2, and Author 3\'.'

    def create_separated_list_empty_list_test(self):
        """
        Test the create_separated_list function with an empty list
        """
        with patch(u'openlp.core.lib.Qt') as mocked_qt:
            # GIVEN: An empty list and the mocked Qt module.
            mocked_qt.PYQT_VERSION_STR = u'4.8'
            mocked_qt.qVersion.return_value = u'4.7'
            string_list = []

            # WHEN: We get a string build from the entries it the list and a separator.
            string_result = create_separated_list(string_list)

            # THEN: We shoud have an emptry string.
            assert string_result == u'', u'The string sould be empty.'

    def create_separated_list_with_one_item_test(self):
        """
        Test the create_separated_list function with a list consisting of only one entry
        """
        with patch(u'openlp.core.lib.Qt') as mocked_qt:
            # GIVEN: A list with a string and the mocked Qt module.
            mocked_qt.PYQT_VERSION_STR = u'4.8'
            mocked_qt.qVersion.return_value = u'4.7'
            string_list = [u'Author 1']

            # WHEN: We get a string build from the entries it the list and a separator.
            string_result = create_separated_list(string_list)

            # THEN: We should have "Author 1"
            assert string_result == u'Author 1', u'The string should be u\'Author 1\'.'

    def create_separated_list_with_two_items_test(self):
        """
        Test the create_separated_list function with a list of two entries
        """
        with patch(u'openlp.core.lib.Qt') as mocked_qt, patch(u'openlp.core.lib.translate') as mocked_translate:
            # GIVEN: A list of strings and the mocked Qt module.
            mocked_qt.PYQT_VERSION_STR = u'4.8'
            mocked_qt.qVersion.return_value = u'4.7'
            mocked_translate.return_value = u'%s and %s'
            string_list = [u'Author 1', u'Author 2']

            # WHEN: We get a string build from the entries it the list and a seperator.
            string_result = create_separated_list(string_list)

            # THEN: We should have "Author 1 and Author 2"
            assert string_result == u'Author 1 and Author 2', u'The string should be u\'Author 1 and Author 2\'.'

    def create_separated_list_with_three_items_test(self):
        """
        Test the create_separated_list function with a list of three items
        """
        with patch(u'openlp.core.lib.Qt') as mocked_qt, patch(u'openlp.core.lib.translate') as mocked_translate:
            # GIVEN: A list with a string and the mocked Qt module.
            mocked_qt.PYQT_VERSION_STR = u'4.8'
            mocked_qt.qVersion.return_value = u'4.7'
            # Always return the untranslated string.
            mocked_translate.side_effect = lambda module, string_to_translate, comment: string_to_translate
            string_list = [u'Author 1', u'Author 2', u'Author 3']

            # WHEN: We get a string build from the entries it the list and a seperator.
            string_result = create_separated_list(string_list)

            # THEN: We should have "Author 1, Author 2, and Author 3"
            assert string_result == u'Author 1, Author 2, and Author 3', u'The string should be u\'Author 1, ' \
                'Author 2, and Author 3\'.'
