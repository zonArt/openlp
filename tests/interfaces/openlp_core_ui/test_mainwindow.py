"""
Package to test the openlp.core.ui.mainwindow package.
"""
from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtGui

from openlp.core.lib import Registry
from openlp.core.ui.mainwindow import MainWindow


class TestMainWindow(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.registry = Registry()
        self.app = QtGui.QApplication([])
        # Mock cursor busy/normal methods.
        self.app.set_busy_cursor = MagicMock()
        self.app.set_normal_cursor = MagicMock()
        self.app.args =[]
        Registry().register('application', self.app)
        # Mock classes and methods used by mainwindow.
        with patch('openlp.core.ui.mainwindow.SettingsForm') as mocked_settings_form, \
                patch('openlp.core.ui.mainwindow.ImageManager') as mocked_image_manager, \
                patch('openlp.core.ui.mainwindow.SlideController') as mocked_slide_controller, \
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
        del self.app

    def restore_current_media_manager_item_test(self):
        """
        Regression test for bug #1152509.
        """
        # GIVEN: Mocked Settings().value method.
        with patch('openlp.core.ui.mainwindow.Settings.value') as mocked_value:
            # save current plugin: True; current media plugin: 2
            mocked_value.side_effect = [True, 2]

            # WHEN: Call the restore method.
            Registry().execute('bootstrap_post_set_up')

            # THEN: The current widget should have been set.
            self.main_window.media_tool_box.setCurrentIndex.assert_called_with(2)

