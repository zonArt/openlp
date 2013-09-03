"""
    Package to test the openlp.core.lib package.
"""

from unittest import TestCase
from mock import MagicMock, Mock, patch

from PyQt4 import QtGui

from openlp.core.lib import Registry, ScreenList, ServiceItem
from openlp.core.ui.mainwindow import MainWindow


class TestServiceManager(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        ScreenList.create(self.app.desktop())
        Registry().register('application', MagicMock())
        with patch('openlp.core.lib.PluginManager'):
            self.main_window = MainWindow()
        self.service_manager = Registry().get('service_manager')

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
            'The service manager list should be empty ')

    def context_menu_test(self):
        """
        Test the context_menu() method.
        """
        # GIVEN: A service item added
        with patch('PyQt4.QtGui.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('PyQt4.QtGui.QWidget.mapToGlobal') as mocked_map_to_global, \
                patch('PyQt4.QtGui.QMenu.exec_') as mocked_exec:
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = Mock()
            self.service_manager.create_custom_action.setVisible = Mock()
            self.service_manager.maintain_action.setVisible = Mock()
            self.service_manager.notes_action.setVisible = Mock()
            self.service_manager.time_action.setVisible = Mock()
            self.service_manager.auto_start_action.setVisible = Mock()

            # WHEN: Show the context menu.
            self.service_manager.context_menu(q_point)

            # THEN: The following actions should be not visible.
            self.service_manager.edit_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.maintain_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
            self.service_manager.time_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
