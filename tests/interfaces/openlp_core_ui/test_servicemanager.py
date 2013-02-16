"""
    Package to test the openlp.core.lib package.
"""

from unittest import TestCase
from mock import MagicMock

from PyQt4 import QtGui

from openlp.core.lib import Registry, ScreenList
from openlp.core.ui.mainwindow import MainWindow


class TestStartNoteDialog(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        ScreenList.create(self.app.desktop())
        Registry().register(u'application', MagicMock())
        self.main_window = MainWindow()
        self.service_manager = Registry().get(u'service_manager')

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.main_window
        del self.app

    def basic_service_manager_test(self):
        """
        Test the Service Manager display functionality
        """
        # GIVEN: A New Service Manager instance

        # WHEN I have an empty display
        # THEN the count of items should be zero
        self.assertEqual(self.service_manager.service_manager_list.topLevelItemCount(), 0,
            u'The service manager list is not empty ')
