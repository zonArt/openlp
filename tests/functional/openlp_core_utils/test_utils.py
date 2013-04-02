"""
Functional tests to test the AppLocation class and related methods.
"""
from unittest import TestCase

from mock import patch

from openlp.core.utils import get_filesystem_encoding, _get_frozen_path, clean_filename, split_filename

class TestUtils(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """
    def get_filesystem_encoding_test(self):
        """
        Test the get_filesystem_encoding() function
        """
        with patch(u'openlp.core.utils.sys.getfilesystemencoding') as mocked_getfilesystemencoding, \
             patch(u'openlp.core.utils.sys.getdefaultencoding') as mocked_getdefaultencoding:
            # GIVEN: sys.getfilesystemencoding returns "cp1252"
            mocked_getfilesystemencoding.return_value = u'cp1252'

            # WHEN: get_filesystem_encoding() is called
            result = get_filesystem_encoding()

            # THEN: getdefaultencoding should have been called
            mocked_getfilesystemencoding.assert_called_with()
            assert not mocked_getdefaultencoding.called
            assert result == u'cp1252', u'The result should be "cp1252"'

            # GIVEN: sys.getfilesystemencoding returns None and sys.getdefaultencoding returns "utf-8"
            mocked_getfilesystemencoding.return_value = None
            mocked_getdefaultencoding.return_value = u'utf-8'

            # WHEN: get_filesystem_encoding() is called
            result = get_filesystem_encoding()

            # THEN: getdefaultencoding should have been called
            mocked_getfilesystemencoding.assert_called_with()
            mocked_getdefaultencoding.assert_called_with()
            assert result == u'utf-8', u'The result should be "utf-8"'

    def get_frozen_path_test(self):
        """
        Test the _get_frozen_path() function
        """
        with patch(u'openlp.core.utils.sys') as mocked_sys:
            # GIVEN: The sys module "without" a "frozen" attribute
            mocked_sys.frozen = None
            # WHEN: We call _get_frozen_path() with two parameters
            # THEN: The non-frozen parameter is returned
            assert _get_frozen_path(u'frozen', u'not frozen') == u'not frozen', u'Should return "not frozen"'
            # GIVEN: The sys module *with* a "frozen" attribute
            mocked_sys.frozen = 1
            # WHEN: We call _get_frozen_path() with two parameters
            # THEN: The frozen parameter is returned
            assert _get_frozen_path(u'frozen', u'not frozen') == u'frozen', u'Should return "frozen"'

    def split_filename_with_file_path_test(self):
        """
        Test the split_filename() function with a path to a file
        """
        # GIVEN: A path to a file.
        file_path = u'/home/user/myfile.txt'
        wanted_result = (u'/home/user', u'myfile.txt')
        with patch(u'openlp.core.utils.os.path.isfile') as mocked_is_file:
            mocked_is_file.return_value = True

            # WHEN: Split the file name.
            result = split_filename(file_path)

            # THEN: A tuple should be returned.
            assert result == wanted_result, u'A tuple with the directory and file should have been returned.'

    def split_filename_with_dir_path_test(self):
        """
        Test the split_filename() function with a path to a directory.
        """
        # GIVEN: A path to a dir.
        file_path = u'/home/user/mydir'
        wanted_result = (u'/home/user/mydir', u'')
        with patch(u'openlp.core.utils.os.path.isfile') as mocked_is_file:
            mocked_is_file.return_value = False

            # WHEN: Split the file name.
            result = split_filename(file_path)

            # THEN: A tuple should be returned.
            assert result == wanted_result, \
                u'A two-entry tuple with the directory and file (empty) should have been returned.'


    def clean_filename_test(self):
        """
        Test the clean_filename() function
        """
        # GIVEN: A invalid file name and the valid file name.
        invalid_name = u'A_file_with_invalid_characters_[\\/:\*\?"<>\|\+\[\]%].py'
        wanted_name = u'A_file_with_invalid_characters______________________.py'

        # WHEN: Clean the name.
        result = clean_filename(invalid_name)

        # THEN: The file name should be cleaned.
        assert result == wanted_name, u'The file name should not contain any special characters.'
