"""
Package to test the openlp.core.lib.pluginmanager package.
"""
from unittest import TestCase

from mock import MagicMock

from openlp.core.lib.pluginmanager import PluginManager
from openlp.core.lib import Registry, PluginStatus


class TestPluginManager(TestCase):
    """
    Test the PluginManager class
    """

    def setUp(self):
        """
        Some pre-test setup required.
        """
        self.mocked_main_window = MagicMock()
        self.mocked_main_window.file_import_menu.return_value = None
        self.mocked_main_window.file_export_menu.return_value = None
        self.mocked_main_window.file_export_menu.return_value = None
        self.mocked_settings_form = MagicMock()
        Registry.create()
        Registry().register(u'service_list', MagicMock())
        Registry().register(u'main_window', self.mocked_main_window)
        Registry().register(u'settings_form', self.mocked_settings_form)

    def hook_media_manager_with_disabled_plugin_test(self):
        """
        Test running the hook_media_manager() method with a disabled plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_media_manager()
        plugin_manager.hook_media_manager()

        # THEN: The createMediaManagerItem() method should have been called
        assert mocked_plugin.createMediaManagerItem.call_count == 0, \
            u'The createMediaManagerItem() method should not have been called.'

    def hook_media_manager_with_active_plugin_test(self):
        """
        Test running the hook_media_manager() method with an active plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_media_manager()
        plugin_manager.hook_media_manager()

        # THEN: The createMediaManagerItem() method should have been called
        mocked_plugin.createMediaManagerItem.assert_called_with()

    def hook_settings_tabs_with_disabled_plugin_and_no_form_test(self):
        """
        Test running the hook_settings_tabs() method with a disabled plugin and no form
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_settings_tabs()
        plugin_manager.hook_settings_tabs()

        # THEN: The createSettingsTab() method should have been called
        assert mocked_plugin.createMediaManagerItem.call_count == 0, \
            u'The createMediaManagerItem() method should not have been called.'

    def hook_settings_tabs_with_disabled_plugin_and_mocked_form_test(self):
        """
        Test running the hook_settings_tabs() method with a disabled plugin and a mocked form
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]
        mocked_settings_form = MagicMock()
        # Replace the autoloaded plugin with the version for testing in real code this would error
        mocked_settings_form.plugin_manager = plugin_manager

        # WHEN: We run hook_settings_tabs()
        plugin_manager.hook_settings_tabs()

        # THEN: The createSettingsTab() method should not have been called, but the plugins lists should be the same
        assert mocked_plugin.createSettingsTab.call_count == 0, \
            u'The createMediaManagerItem() method should not have been called.'
        self.assertEqual(mocked_settings_form.plugin_manager.plugins, plugin_manager.plugins,
            u'The plugins on the settings form should be the same as the plugins in the plugin manager')

    def hook_settings_tabs_with_active_plugin_and_mocked_form_test(self):
        """
        Test running the hook_settings_tabs() method with an active plugin and a mocked settings form
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]
        mocked_settings_form = MagicMock()
        # Replace the autoloaded plugin with the version for testing in real code this would error
        mocked_settings_form.plugin_manager = plugin_manager

        # WHEN: We run hook_settings_tabs()
        plugin_manager.hook_settings_tabs()

        # THEN: The createMediaManagerItem() method should have been called with the mocked settings form
        assert mocked_plugin.createSettingsTab.call_count == 1, \
            u'The createMediaManagerItem() method should have been called once.'
        self.assertEqual(mocked_settings_form.plugin_manager.plugins, plugin_manager.plugins,
             u'The plugins on the settings form should be the same as the plugins in the plugin manager')

    def hook_settings_tabs_with_active_plugin_and_no_form_test(self):
        """
        Test running the hook_settings_tabs() method with an active plugin and no settings form
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_settings_tabs()
        plugin_manager.hook_settings_tabs()

        # THEN: The createSettingsTab() method should have been called
        mocked_plugin.createSettingsTab.assert_called_with(self.mocked_settings_form)

    def hook_import_menu_with_disabled_plugin_test(self):
        """
        Test running the hook_import_menu() method with a disabled plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_import_menu()
        plugin_manager.hook_import_menu()

        # THEN: The createMediaManagerItem() method should have been called
        assert mocked_plugin.addImportMenuItem.call_count == 0, \
            u'The addImportMenuItem() method should not have been called.'

    def hook_import_menu_with_active_plugin_test(self):
        """
        Test running the hook_import_menu() method with an active plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_import_menu()
        plugin_manager.hook_import_menu()

        # THEN: The addImportMenuItem() method should have been called
        mocked_plugin.addImportMenuItem.assert_called_with(self.mocked_main_window.file_import_menu)

    def hook_export_menu_with_disabled_plugin_test(self):
        """
        Test running the hook_export_menu() method with a disabled plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_export_menu()
        plugin_manager.hook_export_menu()

        # THEN: The addExportMenuItem() method should have been called
        assert mocked_plugin.addExportMenuItem.call_count == 0, \
            u'The addExportMenuItem() method should not have been called.'

    def hook_export_menu_with_active_plugin_test(self):
        """
        Test running the hook_export_menu() method with an active plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_export_menu()
        plugin_manager.hook_export_menu()

        # THEN: The addExportMenuItem() method should have been called
        mocked_plugin.addExportMenuItem.assert_called_with(self.mocked_main_window.file_export_menu)

    def hook_tools_menu_with_disabled_plugin_test(self):
        """
        Test running the hook_tools_menu() method with a disabled plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_tools_menu()
        plugin_manager.hook_tools_menu()

        # THEN: The addToolsMenuItem() method should have been called
        assert mocked_plugin.addToolsMenuItem.call_count == 0, \
            u'The addToolsMenuItem() method should not have been called.'

    def hook_tools_menu_with_active_plugin_test(self):
        """
        Test running the hook_tools_menu() method with an active plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run hook_tools_menu()
        plugin_manager.hook_tools_menu()

        # THEN: The addToolsMenuItem() method should have been called
        mocked_plugin.addToolsMenuItem.assert_called_with(self.mocked_main_window.tools_menu)

    def initialise_plugins_with_disabled_plugin_test(self):
        """
        Test running the initialise_plugins() method with a disabled plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        mocked_plugin.isActive.return_value = False
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run initialise_plugins()
        plugin_manager.initialise_plugins()

        # THEN: The isActive() method should have been called, and initialise() method should NOT have been called
        mocked_plugin.isActive.assert_called_with()
        assert mocked_plugin.initialise.call_count == 0, u'The initialise() method should not have been called.'

    def initialise_plugins_with_active_plugin_test(self):
        """
        Test running the initialise_plugins() method with an active plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        mocked_plugin.isActive.return_value = True
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run initialise_plugins()
        plugin_manager.initialise_plugins()

        # THEN: The isActive() and initialise() methods should have been called
        mocked_plugin.isActive.assert_called_with()
        mocked_plugin.initialise.assert_called_with()

    def finalise_plugins_with_disabled_plugin_test(self):
        """
        Test running the finalise_plugins() method with a disabled plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        mocked_plugin.isActive.return_value = False
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run finalise_plugins()
        plugin_manager.finalise_plugins()

        # THEN: The isActive() method should have been called, and initialise() method should NOT have been called
        mocked_plugin.isActive.assert_called_with()
        assert mocked_plugin.finalise.call_count == 0, u'The finalise() method should not have been called.'

    def finalise_plugins_with_active_plugin_test(self):
        """
        Test running the finalise_plugins() method with an active plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        mocked_plugin.isActive.return_value = True
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run finalise_plugins()
        plugin_manager.finalise_plugins()

        # THEN: The isActive() and finalise() methods should have been called
        mocked_plugin.isActive.assert_called_with()
        mocked_plugin.finalise.assert_called_with()

    def get_plugin_by_name_does_not_exist_test(self):
        """
        Test running the get_plugin_by_name() method to find a plugin that does not exist
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.name = 'Mocked Plugin'
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run finalise_plugins()
        result = plugin_manager.get_plugin_by_name('Missing Plugin')

        # THEN: The isActive() and finalise() methods should have been called
        self.assertIsNone(result, u'The result for get_plugin_by_name should be None')

    def get_plugin_by_name_exists_test(self):
        """
        Test running the get_plugin_by_name() method to find a plugin that exists
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.name = 'Mocked Plugin'
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run finalise_plugins()
        result = plugin_manager.get_plugin_by_name('Mocked Plugin')

        # THEN: The isActive() and finalise() methods should have been called
        self.assertEqual(result, mocked_plugin, u'The result for get_plugin_by_name should be the mocked plugin')

    def new_service_created_with_disabled_plugin_test(self):
        """
        Test running the new_service_created() method with a disabled plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Disabled
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Disabled
        mocked_plugin.isActive.return_value = False
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run finalise_plugins()
        plugin_manager.new_service_created()

        # THEN: The isActive() method should have been called, and initialise() method should NOT have been called
        mocked_plugin.isActive.assert_called_with()
        assert mocked_plugin.new_service_created.call_count == 0,\
            u'The new_service_created() method should not have been called.'

    def new_service_created_with_active_plugin_test(self):
        """
        Test running the new_service_created() method with an active plugin
        """
        # GIVEN: A PluginManager instance and a list with a mocked up plugin whose status is set to Active
        mocked_plugin = MagicMock()
        mocked_plugin.status = PluginStatus.Active
        mocked_plugin.isActive.return_value = True
        plugin_manager = PluginManager()
        plugin_manager.plugins = [mocked_plugin]

        # WHEN: We run new_service_created()
        plugin_manager.new_service_created()

        # THEN: The isActive() and finalise() methods should have been called
        mocked_plugin.isActive.assert_called_with()
        mocked_plugin.new_service_created.assert_called_with()
