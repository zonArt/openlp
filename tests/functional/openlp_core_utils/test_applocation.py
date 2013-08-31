"""
Functional tests to test the AppLocation class and related methods.
"""
import copy
from unittest import TestCase

from mock import patch

from openlp.core.utils import AppLocation


FILE_LIST = ['file1', 'file2', 'file3.txt', 'file4.txt', 'file5.mp3', 'file6.mp3']


class TestAppLocation(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """
    def get_data_path_test(self):
        """
        Test the AppLocation.get_data_path() method
        """
        with patch('openlp.core.utils.applocation.Settings') as mocked_class, \
                patch('openlp.core.utils.AppLocation.get_directory') as mocked_get_directory, \
                patch('openlp.core.utils.applocation.check_directory_exists') as mocked_check_directory_exists, \
                patch('openlp.core.utils.applocation.os') as mocked_os:
            # GIVEN: A mocked out Settings class and a mocked out AppLocation.get_directory()
            mocked_settings = mocked_class.return_value
            mocked_settings.contains.return_value = False
            mocked_get_directory.return_value = 'test/dir'
            mocked_check_directory_exists.return_value = True
            mocked_os.path.normpath.return_value = 'test/dir'

            # WHEN: we call AppLocation.get_data_path()
            data_path = AppLocation.get_data_path()

            # THEN: check that all the correct methods were called, and the result is correct
            mocked_settings.contains.assert_called_with('advanced/data path')
            mocked_get_directory.assert_called_with(AppLocation.DataDir)
            mocked_check_directory_exists.assert_called_with('test/dir')
            assert data_path == 'test/dir', 'Result should be "test/dir"'

    def get_data_path_with_custom_location_test(self):
        """
        Test the AppLocation.get_data_path() method when a custom location is set in the settings
        """
        with patch('openlp.core.utils.applocation.Settings') as mocked_class,\
                patch('openlp.core.utils.applocation.os') as mocked_os:
            # GIVEN: A mocked out Settings class which returns a custom data location
            mocked_settings = mocked_class.return_value
            mocked_settings.contains.return_value = True
            mocked_settings.value.return_value.toString.return_value = 'custom/dir'
            mocked_os.path.normpath.return_value = 'custom/dir'

            # WHEN: we call AppLocation.get_data_path()
            data_path = AppLocation.get_data_path()

            # THEN: the mocked Settings methods were called and the value returned was our set up value
            mocked_settings.contains.assert_called_with('advanced/data path')
            mocked_settings.value.assert_called_with('advanced/data path')
            assert data_path == 'custom/dir', 'Result should be "custom/dir"'

    def get_files_no_section_no_extension_test(self):
        """
        Test the AppLocation.get_files() method with no parameters passed.
        """
        with patch('openlp.core.utils.AppLocation.get_data_path') as mocked_get_data_path, \
                patch('openlp.core.utils.applocation.os.listdir') as mocked_listdir:
            # GIVEN: Our mocked modules/methods.
            mocked_get_data_path.return_value = 'test/dir'
            mocked_listdir.return_value = copy.deepcopy(FILE_LIST)

            # When: Get the list of files.
            result = AppLocation.get_files()

            # Then: check if the file lists are identical.
            assert result == FILE_LIST,  'The file lists should be identical.'

    def get_files_test(self):
        """
        Test the AppLocation.get_files() method with all parameters passed.
        """
        with patch('openlp.core.utils.AppLocation.get_data_path') as mocked_get_data_path, \
                patch('openlp.core.utils.applocation.os.listdir') as mocked_listdir:
            # GIVEN: Our mocked modules/methods.
            mocked_get_data_path.return_value = 'test/dir'
            mocked_listdir.return_value = copy.deepcopy(FILE_LIST)

            # When: Get the list of files.
            result = AppLocation.get_files('section', '.mp3')

            # Then: Check if the section parameter was used correctly.
            mocked_listdir.assert_called_with('test/dir/section')

            # Then: check if the file lists are identical.
            assert result == ['file5.mp3', 'file6.mp3'],  'The file lists should be identical.'

    def get_section_data_path_test(self):
        """
        Test the AppLocation.get_section_data_path() method
        """
        with patch('openlp.core.utils.AppLocation.get_data_path') as mocked_get_data_path, \
                patch('openlp.core.utils.applocation.check_directory_exists') as mocked_check_directory_exists:
            # GIVEN: A mocked out AppLocation.get_data_path()
            mocked_get_data_path.return_value = 'test/dir'
            mocked_check_directory_exists.return_value = True

            # WHEN: we call AppLocation.get_data_path()
            data_path = AppLocation.get_section_data_path('section')

            # THEN: check that all the correct methods were called, and the result is correct
            mocked_check_directory_exists.assert_called_with('test/dir/section')
            assert data_path == 'test/dir/section', 'Result should be "test/dir/section"'

    def get_directory_for_app_dir_test(self):
        """
        Test the AppLocation.get_directory() method for AppLocation.AppDir
        """
        with patch('openlp.core.utils.applocation._get_frozen_path') as mocked_get_frozen_path:
            mocked_get_frozen_path.return_value = 'app/dir'

            # WHEN: We call AppLocation.get_directory
            directory = AppLocation.get_directory(AppLocation.AppDir)

            # THEN:
            assert directory == 'app/dir', 'Directory should be "app/dir"'

    def get_directory_for_plugins_dir_test(self):
        """
        Test the AppLocation.get_directory() method for AppLocation.PluginsDir
        """
        with patch('openlp.core.utils.applocation._get_frozen_path') as mocked_get_frozen_path, \
                patch('openlp.core.utils.applocation.os.path.abspath') as mocked_abspath, \
                patch('openlp.core.utils.applocation.os.path.split') as mocked_split, \
                patch('openlp.core.utils.applocation.sys') as mocked_sys:
            mocked_abspath.return_value = 'plugins/dir'
            mocked_split.return_value = ['openlp']
            mocked_get_frozen_path.return_value = 'plugins/dir'
            mocked_sys.frozen = 1
            mocked_sys.argv = ['openlp']

            # WHEN: We call AppLocation.get_directory
            directory = AppLocation.get_directory(AppLocation.PluginsDir)

            # THEN:
            assert directory == 'plugins/dir', 'Directory should be "plugins/dir"'

