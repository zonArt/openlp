"""
Functional tests to test the AppLocation class and related methods.
"""
import sys
from unittest import TestCase

from mock import patch
from PyQt4 import QtCore

from openlp.core.utils import AppLocation, _get_frozen_path

class TestAppLocation(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """
    def get_frozen_path_test(self):
        """
        Test the _get_frozen_path() function
        """
        sys.frozen = None
        assert _get_frozen_path(u'frozen', u'not frozen') == u'not frozen', u'Should return "not frozen"'
        sys.frozen = 1
        assert _get_frozen_path(u'frozen', u'not frozen') == u'frozen', u'Should return "frozen"'

    def get_data_path_with_custom_location_test(self):
        """
        Test the AppLocation.get_data_path() method when a custom location is set in the settings
        """
        with patch(u'openlp.core.utils.Settings') as mocked_class:
            mocked_settings = mocked_class.return_value
            mocked_settings.contains.return_value = True
            mocked_settings.value.return_value.toString.return_value = u'test/dir'
            data_path = AppLocation.get_data_path()
            mocked_settings.contains.assert_called_with(u'advanced/data path')
            mocked_settings.value.assert_called_with(u'advanced/data path')
            mocked_settings.value.return_value.toString.assert_called_with()
            assert data_path == u'test/dir', u'Result should be "test/dir"'
