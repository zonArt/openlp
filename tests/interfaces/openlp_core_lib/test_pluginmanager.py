"""
Package to test the openlp.core.lib.pluginmanager package.
"""
import os
import sys
from tempfile import mkstemp
from unittest import TestCase

from mock import MagicMock, patch
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
        fd, self.ini_file = mkstemp(u'.ini')
        Settings().set_filename(self.ini_file)
        Registry.create()
        Registry().register(u'service_list', MagicMock())
        self.app = QtGui.QApplication.instance()
        self.main_window = QtGui.QMainWindow()
        Registry().register(u'main_window', self.main_window)
        self.plugins_dir = os.path.abspath(os.path.join(os.path.basename(__file__), u'..', u'openlp', u'plugins'))

    def tearDown(self):
        os.unlink(self.ini_file)

    def find_plugins_test(self):
        """
        Test the find_plugins() method to ensure it imports the correct plugins.
        """
        # GIVEN: A plugin manager
        plugin_manager = PluginManager(self.plugins_dir)

        # WHEN: We mock out sys.platform to make it return "darwin" and then find the plugins
        old_platform = sys.platform
        sys.platform = u'darwin'
        plugin_manager.find_plugins()
        sys.platform = old_platform

        # THEN: We should find the "Songs", "Bibles", etc in the plugins list
        plugin_names = [plugin.name for plugin in plugin_manager.plugins]
        assert u'songs' in plugin_names, u'There should be a "songs" plugin.'
        assert u'bibles' in plugin_names, u'There should be a "bibles" plugin.'
        assert u'presentations' not in plugin_names, u'There should NOT be a "presentations" plugin.'
        assert u'images' in plugin_names, u'There should be a "images" plugin.'
        assert u'media' in plugin_names, u'There should be a "media" plugin.'
        assert u'custom' in plugin_names, u'There should be a "custom" plugin.'
        assert u'songusage' in plugin_names, u'There should be a "songusage" plugin.'
        assert u'alerts' in plugin_names, u'There should be a "alerts" plugin.'
        assert u'remotes' in plugin_names, u'There should be a "remotes" plugin.'
