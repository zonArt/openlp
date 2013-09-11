"""
Functional tests to test the AppLocation class and related methods.
"""
from unittest import TestCase

from mock import patch

from openlp.core.utils import clean_filename, get_filesystem_encoding, _get_frozen_path, get_locale_key, \
    get_natural_key, split_filename


class TestUtils(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """
    def get_filesystem_encoding_test(self):
        """
        Test the get_filesystem_encoding() function
        """
        with patch('openlp.core.utils.sys.getfilesystemencoding') as mocked_getfilesystemencoding, \
             patch('openlp.core.utils.sys.getdefaultencoding') as mocked_getdefaultencoding:
            # GIVEN: sys.getfilesystemencoding returns "cp1252"
            mocked_getfilesystemencoding.return_value = 'cp1252'

            # WHEN: get_filesystem_encoding() is called
            result = get_filesystem_encoding()

            # THEN: getdefaultencoding should have been called
            mocked_getfilesystemencoding.assert_called_with()
            assert not mocked_getdefaultencoding.called
            assert result == 'cp1252', 'The result should be "cp1252"'

            # GIVEN: sys.getfilesystemencoding returns None and sys.getdefaultencoding returns "utf-8"
            mocked_getfilesystemencoding.return_value = None
            mocked_getdefaultencoding.return_value = 'utf-8'

            # WHEN: get_filesystem_encoding() is called
            result = get_filesystem_encoding()

            # THEN: getdefaultencoding should have been called
            mocked_getfilesystemencoding.assert_called_with()
            mocked_getdefaultencoding.assert_called_with()
            assert result == 'utf-8', 'The result should be "utf-8"'

    def get_frozen_path_test(self):
        """
        Test the _get_frozen_path() function
        """
        with patch('openlp.core.utils.sys') as mocked_sys:
            # GIVEN: The sys module "without" a "frozen" attribute
            mocked_sys.frozen = None
            # WHEN: We call _get_frozen_path() with two parameters
            # THEN: The non-frozen parameter is returned
            assert _get_frozen_path('frozen', 'not frozen') == 'not frozen', 'Should return "not frozen"'
            # GIVEN: The sys module *with* a "frozen" attribute
            mocked_sys.frozen = 1
            # WHEN: We call _get_frozen_path() with two parameters
            # THEN: The frozen parameter is returned
            assert _get_frozen_path('frozen', 'not frozen') == 'frozen', 'Should return "frozen"'

    def split_filename_with_file_path_test(self):
        """
        Test the split_filename() function with a path to a file
        """
        # GIVEN: A path to a file.
        file_path = '/home/user/myfile.txt'
        wanted_result = ('/home/user', 'myfile.txt')
        with patch('openlp.core.utils.os.path.isfile') as mocked_is_file:
            mocked_is_file.return_value = True

            # WHEN: Split the file name.
            result = split_filename(file_path)

            # THEN: A tuple should be returned.
            assert result == wanted_result, 'A tuple with the directory and file name should have been returned.'

    def split_filename_with_dir_path_test(self):
        """
        Test the split_filename() function with a path to a directory
        """
        # GIVEN: A path to a dir.
        file_path = '/home/user/mydir'
        wanted_result = ('/home/user/mydir', '')
        with patch('openlp.core.utils.os.path.isfile') as mocked_is_file:
            mocked_is_file.return_value = False

            # WHEN: Split the file name.
            result = split_filename(file_path)

            # THEN: A tuple should be returned.
            assert result == wanted_result, \
                'A two-entry tuple with the directory and file name (empty) should have been returned.'

    def clean_filename_test(self):
        """
        Test the clean_filename() function
        """
        # GIVEN: A invalid file name and the valid file name.
        invalid_name = 'A_file_with_invalid_characters_[\\/:\*\?"<>\|\+\[\]%].py'
        wanted_name = 'A_file_with_invalid_characters______________________.py'

        # WHEN: Clean the name.
        result = clean_filename(invalid_name)

        # THEN: The file name should be cleaned.
        assert result == wanted_name, 'The file name should not contain any special characters.'

    def get_locale_key_windows_test(self):
        """
        Test the get_locale_key(string) function
        """
        with patch('openlp.core.utils.languagemanager.LanguageManager.get_language') as mocked_get_language,  \
                patch('openlp.core.utils.os') as mocked_os:
            # GIVEN: The language is German
            # 0x00C3 (A with diaresis) should be sorted as "A". 0x00DF (sharp s) should be sorted as "ss".
            mocked_get_language.return_value = 'de'
            mocked_os.name = 'nt'
            unsorted_list = ['Auszug', 'Aushang', '\u00C4u\u00DFerung']
            # WHEN: We sort the list and use get_locale_key() to generate the sorting keys
            # THEN: We get a properly sorted list
            test_passes = sorted(unsorted_list, key=get_locale_key) == ['Aushang', '\u00C4u\u00DFerung', 'Auszug']
            assert test_passes, 'Strings should be sorted properly'

    def get_locale_key_linux_test(self):

        """
        Test the get_locale_key(string) function
        """
        with patch('openlp.core.utils.languagemanager.LanguageManager.get_language') as mocked_get_language,  \
                patch('openlp.core.utils.os.name') as mocked_os:
            # GIVEN: The language is German
            # 0x00C3 (A with diaresis) should be sorted as "A". 0x00DF (sharp s) should be sorted as "ss".
            mocked_get_language.return_value = 'de'
            mocked_os.name = 'linux'
            unsorted_list = ['Auszug', 'Aushang', '\u00C4u\u00DFerung']
            # WHEN: We sort the list and use get_locale_key() to generate the sorting keys
            # THEN: We get a properly sorted list
            test_passes = sorted(unsorted_list, key=get_locale_key) == ['Aushang', '\u00C4u\u00DFerung', 'Auszug']
            assert test_passes, 'Strings should be sorted properly'

    def get_natural_key_test(self):
        """
        Test the get_natural_key(string) function
        """
        with patch('openlp.core.utils.languagemanager.LanguageManager.get_language') as mocked_get_language:
            # GIVEN: The language is English (a language, which sorts digits before letters)
            mocked_get_language.return_value = 'en'
            unsorted_list = ['item 10a', 'item 3b', '1st item']
            # WHEN: We sort the list and use get_natural_key() to generate the sorting keys
            # THEN: We get a properly sorted list
            test_passes = sorted(unsorted_list, key=get_natural_key) == ['1st item', 'item 3b', 'item 10a']
            assert test_passes, 'Numbers should be sorted naturally'
