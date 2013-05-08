"""
Package to test the openlp.core.ui.mainwindow package.
"""
from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtCore, QtGui, QtTest

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
        Registry().register(u'application', self.app)
        # Mock classes and methods used by mainwindow.
        with patch(u'openlp.core.ui.mainwindow.ImageManager') as mocked_image_manager, \
                patch(u'openlp.core.ui.mainwindow.SlideController') as mocked_slide_controller, \
                patch(u'openlp.core.ui.mainwindow.OpenLPDockWidget') as mocked_dock_widget, \
                patch(u'openlp.core.ui.mainwindow.QtGui.QToolBox') as mocked_q_tool_box_class, \
                patch(u'openlp.core.ui.mainwindow.QtGui.QMainWindow.addDockWidget') as mocked_add_dock_method, \
                patch(u'openlp.core.ui.mainwindow.ServiceManager') as mocked_slervice_manager, \
                patch(u'openlp.core.ui.mainwindow.ThemeManager') as mocked_theme_manager, \
                patch(u'openlp.core.ui.mainwindow.Renderer') as mocked_renderer:
            self.main_window = MainWindow()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.main_window
        del self.app

    def on_search_shortcut_triggered_test(self):
        """
        Test if the search edit has focus after CTRL+F has been pressed.
        """
        # GIVEN: Mocked widget.
        mocked_current_widget = MagicMock()
        self.main_window.media_tool_box.currentWidget = mocked_current_widget

        # WHEN: Press the shortcut.
        QtTest.QTest.keyPress(self.main_window, QtCore.Qt.Key_F, QtCore.Qt.ControlModifier)
        QtTest.QTest.keyRelease(self.main_window, QtCore.Qt.Key_F, QtCore.Qt.ControlModifier)

        # THEN: The on_focus method should have been called.
        mocked_current_widget.on_focus.assert_called_with()
