"""
Package to test the openlp.core.lib.pluginmanager package.
"""
import os
import sys
import shutil
from tempfile import mkstemp, mkdtemp
from unittest import TestCase

from mock import MagicMock
from PyQt4 import QtGui

from openlp.core.lib.pluginmanager import PluginManager
from openlp.core.lib import Registry, Settings


class TestPluginManager(TestCase):
    """
    Test the PluginManager class
    """

    def setUp(self):
        """
        Some pre-test setup required.
        """
        fd, self.ini_file = mkstemp('.ini')
        self.temp_dir = mkdtemp('openlp')
        Settings().set_filename(self.ini_file)
        Settings().setValue('advanced/data path', self.temp_dir)
        Registry.create()
        Registry().register('service_list', MagicMock())
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register('main_window', self.main_window)

    def tearDown(self):
        del self.app
        del self.main_window
        Settings().remove('advanced/data path')
        shutil.rmtree(self.temp_dir)
        os.unlink(self.ini_file)

    def find_plugins_test(self):
        """
        Test the find_plugins() method to ensure it imports the correct plugins
        """
        # GIVEN: A plugin manager
        plugin_manager = PluginManager()

        # WHEN: We mock out sys.platform to make it return "darwin" and then find the plugins
        old_platform = sys.platform
        sys.platform = 'darwin'
        plugin_manager.find_plugins()
        sys.platform = old_platform

        # THEN: We should find the "Songs", "Bibles", etc in the plugins list
        plugin_names = [plugin.name for plugin in plugin_manager.plugins]
        assert 'songs' in plugin_names, 'There should be a "songs" plugin.'
        assert 'bibles' in plugin_names, 'There should be a "bibles" plugin.'
        assert 'presentations' not in plugin_names, 'There should NOT be a "presentations" plugin.'
        assert 'images' in plugin_names, 'There should be a "images" plugin.'
        assert 'media' in plugin_names, 'There should be a "media" plugin.'
        assert 'custom' in plugin_names, 'There should be a "custom" plugin.'
        assert 'songusage' in plugin_names, 'There should be a "songusage" plugin.'
        assert 'alerts' in plugin_names, 'There should be a "alerts" plugin.'
        assert 'remotes' in plugin_names, 'There should be a "remotes" plugin.'
