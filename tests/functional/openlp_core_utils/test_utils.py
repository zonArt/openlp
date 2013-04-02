"""
Functional tests to test the AppLocation class and related methods.
"""
from unittest import TestCase

from mock import patch

from openlp.core.utils import get_filesystem_encoding, _get_frozen_path, get_local_key, get_natural_key

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

    def get_local_key_test(self):
        """
        Test the get_local_key(string) function
        """
        with patch(u'openlp.core.utils.languagemanager.LanguageManager.get_language') as mocked_get_language:
            # GIVEN: The language is German
            # 0x00C3 (A with diaresis) should be sorted as "A". 0x00DF (sharp s) should be sorted as "ss".
            mocked_get_language.return_value = u'de'
            unsorted_list = [u'Auszug', u'Aushang', u'\u00C4u\u00DFerung']
            # WHEN: We sort the list and use get_locale_key() to generate the sorting keys
            # THEN: We get a properly sorted list
            assert sorted(unsorted_list, key=get_local_key) == [u'Aushang', u'\u00C4u\u00DFerung', u'Auszug'], u'Strings should be sorted properly'

    def get_natural_key_test(self):
        """
        Test the get_natural_key(string) function
        """
        with patch(u'openlp.core.utils.languagemanager.LanguageManager.get_language') as mocked_get_language:
            # GIVEN: The language is English (a language, which sorts digits before letters)
            mocked_get_language.return_value = u'en'
            unsorted_list = [u'item 10a', u'item 3b', u'1st item']
            # WHEN: We sort the list and use get_natural_key() to generate the sorting keys
            # THEN: We get a properly sorted list
            assert sorted(unsorted_list, key=get_natural_key) == [u'1st item', u'item 3b', u'item 10a'], u'Numbers should be sortet naturally'

