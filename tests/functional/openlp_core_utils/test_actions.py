"""
Package to test the openlp.core.utils.actions package.
"""
import os
from tempfile import mkstemp
from unittest import TestCase

from PyQt4 import QtGui, QtCore

from openlp.core.lib import Settings
from openlp.core.utils import ActionList


class TestActionList(TestCase):

    def setUp(self):
        """
        Prepare the tests
        """
        self.action_list = ActionList.get_instance()
        self.settings = Settings()
        fd, self.ini_file = mkstemp('.ini')
        self.settings.set_filename(self.ini_file)
        self.settings.beginGroup('shortcuts')

    def tearDown(self):
        """
        Clean up
        """
        self.settings.endGroup()
        os.unlink(self.ini_file)

    def test_add_action_same_parent(self):
        """
        ActionList test - Tests the add_action method. The actions have the same parent, the same shortcuts and both
        have the QtCore.Qt.WindowShortcut shortcut context set.
        """
        # GIVEN: Two actions with the same shortcuts.
        parent = QtCore.QObject()
        action1 = QtGui.QAction(parent)
        action1.setObjectName('action1')
        action_with_same_shortcuts1 = QtGui.QAction(parent)
        action_with_same_shortcuts1.setObjectName('action_with_same_shortcuts1')
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            'shortcuts/action1': [QtGui.QKeySequence('a'), QtGui.QKeySequence('b')],
            'shortcuts/action_with_same_shortcuts1': [QtGui.QKeySequence('b'), QtGui.QKeySequence('a')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action1, 'example_category')
        self.action_list.add_action(action_with_same_shortcuts1, 'example_category')
        # Remove the actions again.
        self.action_list.remove_action(action1, 'example_category')
        self.action_list.remove_action(action_with_same_shortcuts1, 'example_category')

        # THEN: As both actions have the same shortcuts, they should be removed from one action.
        assert len(action1.shortcuts()) == 2, 'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts1.shortcuts()) == 0, 'The action should not have a shortcut assigned.'

    def test_add_action_different_parent(self):
        """
        ActionList test - Tests the add_action method. The actions have the different parent, the same shortcuts and
        both have the QtCore.Qt.WindowShortcut shortcut context set.
        """
        # GIVEN: Two actions with the same shortcuts.
        parent = QtCore.QObject()
        action2 = QtGui.QAction(parent)
        action2.setObjectName('action2')
        second_parent = QtCore.QObject()
        action_with_same_shortcuts2 = QtGui.QAction(second_parent)
        action_with_same_shortcuts2.setObjectName('action_with_same_shortcuts2')
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            'shortcuts/action2': [QtGui.QKeySequence('c'), QtGui.QKeySequence('d')],
            'shortcuts/action_with_same_shortcuts2': [QtGui.QKeySequence('d'), QtGui.QKeySequence('c')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action2, 'example_category')
        self.action_list.add_action(action_with_same_shortcuts2, 'example_category')
        # Remove the actions again.
        self.action_list.remove_action(action2, 'example_category')
        self.action_list.remove_action(action_with_same_shortcuts2, 'example_category')

        # THEN: As both actions have the same shortcuts, they should be removed from one action.
        assert len(action2.shortcuts()) == 2, 'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts2.shortcuts()) == 0, 'The action should not have a shortcut assigned.'

    def test_add_action_different_context(self):
        """
        ActionList test - Tests the add_action method. The actions have the different parent, the same shortcuts and
        both have the QtCore.Qt.WidgetShortcut shortcut context set.
        """
        # GIVEN: Two actions with the same shortcuts.
        parent = QtCore.QObject()
        action3 = QtGui.QAction(parent)
        action3.setObjectName('action3')
        action3.setShortcutContext(QtCore.Qt.WidgetShortcut)
        second_parent = QtCore.QObject()
        action_with_same_shortcuts3 = QtGui.QAction(second_parent)
        action_with_same_shortcuts3.setObjectName('action_with_same_shortcuts3')
        action_with_same_shortcuts3.setShortcutContext(QtCore.Qt.WidgetShortcut)
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            'shortcuts/action3': [QtGui.QKeySequence('e'), QtGui.QKeySequence('f')],
            'shortcuts/action_with_same_shortcuts3': [QtGui.QKeySequence('e'), QtGui.QKeySequence('f')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action3, 'example_category2')
        self.action_list.add_action(action_with_same_shortcuts3, 'example_category2')
        # Remove the actions again.
        self.action_list.remove_action(action3, 'example_category2')
        self.action_list.remove_action(action_with_same_shortcuts3, 'example_category2')

        # THEN: Both action should keep their shortcuts.
        assert len(action3.shortcuts()) == 2, 'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts3.shortcuts()) == 2, 'The action should have two shortcuts assigned.'


