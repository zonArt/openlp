"""
    Package to test the openlp.core.lib package.
"""

from unittest import TestCase

from PyQt4 import QtGui

from openlp.core.common import Registry
from openlp.core.lib import ScreenList, ServiceItem, ItemCapabilities
from openlp.core.ui.mainwindow import MainWindow
from tests.interfaces import MagicMock, patch


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

        # WHEN I have set up the display
        self.service_manager.setup_ui(self.service_manager)
        # THEN the count of items should be zero
        self.assertEqual(self.service_manager.service_manager_list.topLevelItemCount(), 0,
                         'The service manager list should be empty ')

    def default_context_menu_test(self):
        """
        Test the context_menu() method with a default service item
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('PyQt4.QtGui.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('PyQt4.QtGui.QWidget.mapToGlobal'), \
                patch('PyQt4.QtGui.QMenu.exec_'):
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
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

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


    def edit_context_menu_test(self):
        """
        Test the context_menu() method with a edit service item
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('PyQt4.QtGui.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('PyQt4.QtGui.QWidget.mapToGlobal'), \
                patch('PyQt4.QtGui.QMenu.exec_'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.CanEdit)
            service_item.edit_id = 1
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

            # WHEN: Show the context menu.
            self.service_manager.context_menu(q_point)

            # THEN: The following actions should be not visible.
            self.service_manager.edit_action.setVisible.assert_called_with(True), \
                'The action should be set visible.'
            self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.maintain_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
            self.service_manager.time_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'

    def maintain_context_menu_test(self):
        """
        Test the context_menu() method with a maintain
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('PyQt4.QtGui.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('PyQt4.QtGui.QWidget.mapToGlobal'), \
                patch('PyQt4.QtGui.QMenu.exec_'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.CanMaintain)
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

            # WHEN: Show the context menu.
            self.service_manager.context_menu(q_point)

            # THEN: The following actions should be not visible.
            self.service_manager.edit_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.create_custom_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.maintain_action.setVisible.assert_called_with(True), \
                'The action should be set visible.'
            self.service_manager.notes_action.setVisible.assert_called_with(True), 'The action should be set visible.'
            self.service_manager.time_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'
            self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'

    def loopy_context_menu_test(self):
        """
        Test the context_menu() method with a loop
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('PyQt4.QtGui.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('PyQt4.QtGui.QWidget.mapToGlobal'), \
                patch('PyQt4.QtGui.QMenu.exec_'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.CanLoop)
            service_item._raw_frames.append("One")
            service_item._raw_frames.append("Two")
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

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

    def start_time_context_menu_test(self):
        """
        Test the context_menu() method with a start time
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('PyQt4.QtGui.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('PyQt4.QtGui.QWidget.mapToGlobal'), \
                patch('PyQt4.QtGui.QMenu.exec_'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.HasVariableStartTime)
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

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
            self.service_manager.time_action.setVisible.assert_called_with(True), \
                'The action should be set visible.'
            self.service_manager.auto_start_action.setVisible.assert_called_once_with(False), \
                'The action should be set invisible.'

    def auto_start_context_menu_test(self):
        """
        Test the context_menu() method with can auto start
        """
        # GIVEN: A service item added
        self.service_manager.setup_ui(self.service_manager)
        with patch('PyQt4.QtGui.QTreeWidget.itemAt') as mocked_item_at_method, \
                patch('PyQt4.QtGui.QWidget.mapToGlobal'), \
                patch('PyQt4.QtGui.QMenu.exec_'):
            mocked_item = MagicMock()
            mocked_item.parent.return_value = None
            mocked_item_at_method.return_value = mocked_item
            # We want 1 to be returned for the position
            mocked_item.data.return_value = 1
            # A service item without capabilities.
            service_item = ServiceItem()
            service_item.add_capability(ItemCapabilities.CanAutoStartForLive)
            self.service_manager.service_items = [{'service_item': service_item}]
            q_point = None
            # Mocked actions.
            self.service_manager.edit_action.setVisible = MagicMock()
            self.service_manager.create_custom_action.setVisible = MagicMock()
            self.service_manager.maintain_action.setVisible = MagicMock()
            self.service_manager.notes_action.setVisible = MagicMock()
            self.service_manager.time_action.setVisible = MagicMock()
            self.service_manager.auto_start_action.setVisible = MagicMock()

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
            self.service_manager.auto_start_action.setVisible.assert_called_with(True), \
                'The action should be set visible.'

