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
        fd, self.ini_file = mkstemp(u'.ini')
        self.settings.set_filename(self.ini_file)
        self.settings.beginGroup(u'shortcuts')

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
        action = QtGui.QAction(parent)
        action.setObjectName(u'action')
        action_with_same_shortcuts = QtGui.QAction(parent)
        action_with_same_shortcuts.setObjectName(u'action_with_same_shortcuts')
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            u'shortcuts/action': [QtGui.QKeySequence(u'v'), QtGui.QKeySequence(u'c')],
            u'shortcuts/action_with_same_shortcuts': [QtGui.QKeySequence(u'v'), QtGui.QKeySequence(u'c')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action, u'example_category')
        self.action_list.add_action(action_with_same_shortcuts, u'example_category')
        # Remove the actions again.
        self.action_list.remove_action(action, u'example_category')
        self.action_list.remove_action(action_with_same_shortcuts, u'example_category')

        # THEN: As both actions have the same shortcuts, they should be removed from one action.
        assert len(action.shortcuts()) == 2, u'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts.shortcuts()) == 0, u'The action should not have a shortcut assigned.'

    def test_add_action_different_parent(self):
        """
        ActionList test - Tests the add_action method. The actions have the different parent, the same shortcuts and
        both have the QtCore.Qt.WindowShortcut shortcut context set.
        """
        # GIVEN: Two actions with the same shortcuts.
        parent = QtCore.QObject()
        action = QtGui.QAction(parent)
        action.setObjectName(u'action2')
        second_parent = QtCore.QObject()
        action_with_same_shortcuts = QtGui.QAction(second_parent)
        action_with_same_shortcuts.setObjectName(u'action_with_same_shortcuts2')
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            u'shortcuts/action2': [QtGui.QKeySequence(u'v'), QtGui.QKeySequence(u'c')],
            u'shortcuts/action_with_same_shortcuts2': [QtGui.QKeySequence(u'v'), QtGui.QKeySequence(u'c')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action, u'example_category')
        self.action_list.add_action(action_with_same_shortcuts, u'example_category')
        # Remove the actions again.
        self.action_list.remove_action(action, u'example_category')
        self.action_list.remove_action(action_with_same_shortcuts, u'example_category')

        # THEN: As both actions have the same shortcuts, they should be removed from one action.
        assert len(action.shortcuts()) == 2, u'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts.shortcuts()) == 0, u'The action should not have a shortcut assigned.'

    def test_add_action_different_context(self):
        """
        ActionList test - Tests the add_action method. The actions have the different parent, the same shortcuts and
        both have the QtCore.Qt.WidgetShortcut shortcut context set.
        """
        # GIVEN: Two actions with the same shortcuts.
        parent = QtCore.QObject()
        action = QtGui.QAction(parent)
        action.setObjectName(u'action3')
        action.setShortcutContext(QtCore.Qt.WidgetShortcut)
        second_parent = QtCore.QObject()
        action_with_same_shortcuts = QtGui.QAction(second_parent)
        action_with_same_shortcuts.setObjectName(u'action_with_same_shortcuts3')
        action_with_same_shortcuts.setShortcutContext(QtCore.Qt.WidgetShortcut)
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            u'shortcuts/action3': [QtGui.QKeySequence(u'1'), QtGui.QKeySequence(u'2')],
            u'shortcuts/action_with_same_shortcuts3': [QtGui.QKeySequence(u'1'), QtGui.QKeySequence(u'2')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action, u'example_category2')
        self.action_list.add_action(action_with_same_shortcuts, u'example_category2')
        # Remove the actions again.
        self.action_list.remove_action(action, u'example_category2')
        self.action_list.remove_action(action_with_same_shortcuts, u'example_category2')

        # THEN: Both action should keep their shortcuts.
        assert len(action.shortcuts()) == 2, u'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts.shortcuts()) == 2, u'The action should have two shortcuts assigned.'


