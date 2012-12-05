"""
Functional tests to test the AppLocation class and related methods.
"""
import sys
from unittest import TestCase

from mock import patch

from openlp.core.utils import AppLocation, _get_frozen_path

class TestAppLocation(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """
    def get_frozen_path_test(self):
        """
        Test the _get_frozen_path() function
        """
        # GIVEN: The sys module "without" a "frozen" attribute
        sys.frozen = None
        # WHEN: We call _get_frozen_path() with two parameters
        # THEN: The non-frozen parameter is returned
        assert _get_frozen_path(u'frozen', u'not frozen') == u'not frozen', u'Should return "not frozen"'
        # GIVEN: The sys module *with* a "frozen" attribute
        sys.frozen = 1
        # WHEN: We call _get_frozen_path() with two parameters
        # THEN: The frozen parameter is returned
        assert _get_frozen_path(u'frozen', u'not frozen') == u'frozen', u'Should return "frozen"'

    def get_data_path_test(self):
        """
        Test the AppLocation.get_data_path() method
        """
        with patch(u'openlp.core.utils.Settings') as mocked_class, \
             patch(u'openlp.core.utils.AppLocation.get_directory') as mocked_get_directory, \
             patch(u'openlp.core.utils.check_directory_exists') as mocked_check_directory_exists, \
             patch(u'openlp.core.utils.os') as mocked_os:
            # GIVEN: A mocked out Settings class and a mocked out AppLocation.get_directory()
            mocked_settings = mocked_class.return_value
            mocked_settings.contains.return_value = False
            mocked_get_directory.return_value = u'test/dir'
            mocked_check_directory_exists.return_value = True
            mocked_os.path.normpath.return_value = u'test/dir'
            # WHEN: we call AppLocation.get_data_path()
            data_path = AppLocation.get_data_path()
            # THEN: check that all the correct methods were called, and the result is correct
            mocked_settings.contains.assert_called_with(u'advanced/data path')
            mocked_get_directory.assert_called_with(AppLocation.DataDir)
            mocked_check_directory_exists.assert_called_with(u'test/dir')
            assert data_path == u'test/dir', u'Result should be "test/dir"'

    def get_data_path_with_custom_location_test(self):
        """
        Test the AppLocation.get_data_path() method when a custom location is set in the settings
        """
        with patch(u'openlp.core.utils.Settings') as mocked_class,\
             patch(u'openlp.core.utils.os') as mocked_os:
            # GIVEN: A mocked out Settings class which returns a custom data location
            mocked_settings = mocked_class.return_value
            mocked_settings.contains.return_value = True
            mocked_settings.value.return_value.toString.return_value = u'custom/dir'
            mocked_os.path.normpath.return_value = u'custom/dir'
            # WHEN: we call AppLocation.get_data_path()
            data_path = AppLocation.get_data_path()
            # THEN: the mocked Settings methods were called and the value returned was our set up value
            mocked_settings.contains.assert_called_with(u'advanced/data path')
            mocked_settings.value.assert_called_with(u'advanced/data path')
            mocked_settings.value.return_value.toString.assert_called_with()
            assert data_path == u'custom/dir', u'Result should be "custom/dir"'
