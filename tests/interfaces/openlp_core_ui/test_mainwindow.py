"""
Package to test the openlp.core.ui.mainwindow package.
"""
from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtCore, QtGui, QtTest

from openlp.core.lib import Registry, ScreenList
from openlp.core.ui.mainwindow import MainWindow


class TestMainWindow(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.registry = Registry()
        ScreenList.create(MagicMock())
        self.app = QtGui.QApplication([])
        self.app.args =[]
        Registry().register(u'application', self.app)
        self.main_window = MainWindow()
        Registry().register(u'main_window', self.main_window)

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.main_window
        del self.app

    def on_search_shortcut_triggered_test(self):
        """
        """
        # GIVEN: Mocked mehtod.
        mocked_current_widget = MagicMock()
        self.main_window.media_tool_box.currentWidget = mocked_current_widget

        # WHEN: Press the shortcut

        # THEN: The on_focus method should have been called.
        mocked_current_widget.on_focus.assert_called_with()
