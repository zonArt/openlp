"""
Functional tests to test the AppLocation class and related methods.
"""
from unittest import TestCase

from mock import patch

from openlp.core.utils import AppLocation

class TestAppLocation(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """
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
            assert data_path == u'custom/dir', u'Result should be "custom/dir"'

    def get_section_data_path_test(self):
        """
        Test the AppLocation.get_section_data_path() method
        """
        with patch(u'openlp.core.utils.AppLocation.get_data_path') as mocked_get_data_path, \
             patch(u'openlp.core.utils.check_directory_exists') as mocked_check_directory_exists:
            # GIVEN: A mocked out AppLocation.get_data_path()
            mocked_get_data_path.return_value = u'test/dir'
            mocked_check_directory_exists.return_value = True
            # WHEN: we call AppLocation.get_data_path()
            data_path = AppLocation.get_section_data_path(u'section')
            # THEN: check that all the correct methods were called, and the result is correct
            mocked_check_directory_exists.assert_called_with(u'test/dir/section')
            assert data_path == u'test/dir/section', u'Result should be "test/dir/section"'

    def get_directory_for_app_dir_test(self):
        """
        Test the AppLocation.get_directory() method for AppLocation.AppDir
        """
        with patch(u'openlp.core.utils._get_frozen_path') as mocked_get_frozen_path:
            mocked_get_frozen_path.return_value = u'app/dir'
            # WHEN: We call AppLocation.get_directory
            directory = AppLocation.get_directory(AppLocation.AppDir)
            # THEN:
            assert directory == u'app/dir', u'Directory should be "app/dir"'

    def get_directory_for_plugins_dir_test(self):
        """
        Test the AppLocation.get_directory() method for AppLocation.PluginsDir
        """
        with patch(u'openlp.core.utils._get_frozen_path') as mocked_get_frozen_path, \
             patch(u'openlp.core.utils.os.path.abspath') as mocked_abspath, \
             patch(u'openlp.core.utils.os.path.split') as mocked_split, \
             patch(u'openlp.core.utils.sys') as mocked_sys:
            mocked_abspath.return_value = u'plugins/dir'
            mocked_split.return_value = [u'openlp']
            mocked_get_frozen_path.return_value = u'plugins/dir'
            mocked_sys.frozen = 1
            mocked_sys.argv = ['openlp']
            # WHEN: We call AppLocation.get_directory
            directory = AppLocation.get_directory(AppLocation.PluginsDir)
            # THEN:
            assert directory == u'plugins/dir', u'Directory should be "plugins/dir"'

