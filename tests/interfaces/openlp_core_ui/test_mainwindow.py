"""
Package to test the openlp.core.ui.mainwindow package.
"""
from unittest import TestCase

from PyQt4 import QtGui, QtCore

from openlp.core.common import Registry
from openlp.core.ui.mainwindow import MainWindow
from tests.interfaces import MagicMock, patch


class TestMainWindow(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.registry = Registry()
        old_app_instance = QtCore.QCoreApplication.instance()
        if old_app_instance is None:
            self.app = QtGui.QApplication([])
        else:
            self.app = old_app_instance
        # Mock cursor busy/normal methods.
        self.app.set_busy_cursor = MagicMock()
        self.app.set_normal_cursor = MagicMock()
        self.app.args = []
        Registry().register('application', self.app)
        # Mock classes and methods used by mainwindow.
        with patch('openlp.core.ui.mainwindow.SettingsForm') as mocked_settings_form, \
                patch('openlp.core.ui.mainwindow.ImageManager') as mocked_image_manager, \
                patch('openlp.core.ui.mainwindow.LiveController') as mocked_live_controller, \
                patch('openlp.core.ui.mainwindow.PreviewController') as mocked_preview_controller, \
                patch('openlp.core.ui.mainwindow.OpenLPDockWidget') as mocked_dock_widget, \
                patch('openlp.core.ui.mainwindow.QtGui.QToolBox') as mocked_q_tool_box_class, \
                patch('openlp.core.ui.mainwindow.QtGui.QMainWindow.addDockWidget') as mocked_add_dock_method, \
                patch('openlp.core.ui.mainwindow.ServiceManager') as mocked_service_manager, \
                patch('openlp.core.ui.mainwindow.ThemeManager') as mocked_theme_manager, \
                patch('openlp.core.ui.mainwindow.Renderer') as mocked_renderer:
            self.main_window = MainWindow()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.main_window

    def restore_current_media_manager_item_test(self):
        """
        Regression test for bug #1152509.
        """
        # GIVEN: Mocked Settings().value method.
        with patch('openlp.core.ui.mainwindow.Settings.value') as mocked_value:
            # save current plugin: True; current media plugin: 2
            mocked_value.side_effect = [True, 2]

            # WHEN: Call the restore method.
            self.main_window.restore_current_media_manager_item()

            # THEN: The current widget should have been set.
            self.main_window.media_tool_box.setCurrentIndex.assert_called_with(2)

