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
        action1 = QtGui.QAction(parent)
        action1.setObjectName(u'action1')
        action_with_same_shortcuts1 = QtGui.QAction(parent)
        action_with_same_shortcuts1.setObjectName(u'action_with_same_shortcuts1')
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            u'shortcuts/action1': [QtGui.QKeySequence(u'a'), QtGui.QKeySequence(u'b')],
            u'shortcuts/action_with_same_shortcuts1': [QtGui.QKeySequence(u'b'), QtGui.QKeySequence(u'a')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action1, u'example_category')
        self.action_list.add_action(action_with_same_shortcuts1, u'example_category')
        # Remove the actions again.
        self.action_list.remove_action(action1, u'example_category')
        self.action_list.remove_action(action_with_same_shortcuts1, u'example_category')

        # THEN: As both actions have the same shortcuts, they should be removed from one action.
        assert len(action1.shortcuts()) == 2, u'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts1.shortcuts()) == 0, u'The action should not have a shortcut assigned.'

    def test_add_action_different_parent(self):
        """
        ActionList test - Tests the add_action method. The actions have the different parent, the same shortcuts and
        both have the QtCore.Qt.WindowShortcut shortcut context set.
        """
        # GIVEN: Two actions with the same shortcuts.
        parent = QtCore.QObject()
        action2 = QtGui.QAction(parent)
        action2.setObjectName(u'action2')
        second_parent = QtCore.QObject()
        action_with_same_shortcuts2 = QtGui.QAction(second_parent)
        action_with_same_shortcuts2.setObjectName(u'action_with_same_shortcuts2')
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            u'shortcuts/action2': [QtGui.QKeySequence(u'c'), QtGui.QKeySequence(u'd')],
            u'shortcuts/action_with_same_shortcuts2': [QtGui.QKeySequence(u'd'), QtGui.QKeySequence(u'c')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action2, u'example_category')
        self.action_list.add_action(action_with_same_shortcuts2, u'example_category')
        # Remove the actions again.
        self.action_list.remove_action(action2, u'example_category')
        self.action_list.remove_action(action_with_same_shortcuts2, u'example_category')

        # THEN: As both actions have the same shortcuts, they should be removed from one action.
        assert len(action2.shortcuts()) == 2, u'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts2.shortcuts()) == 0, u'The action should not have a shortcut assigned.'

    def test_add_action_different_context(self):
        """
        ActionList test - Tests the add_action method. The actions have the different parent, the same shortcuts and
        both have the QtCore.Qt.WidgetShortcut shortcut context set.
        """
        # GIVEN: Two actions with the same shortcuts.
        parent = QtCore.QObject()
        action3 = QtGui.QAction(parent)
        action3.setObjectName(u'action3')
        action3.setShortcutContext(QtCore.Qt.WidgetShortcut)
        second_parent = QtCore.QObject()
        action_with_same_shortcuts3 = QtGui.QAction(second_parent)
        action_with_same_shortcuts3.setObjectName(u'action_with_same_shortcuts3')
        action_with_same_shortcuts3.setShortcutContext(QtCore.Qt.WidgetShortcut)
        # Add default shortcuts to Settings class.
        default_shortcuts = {
            u'shortcuts/action3': [QtGui.QKeySequence(u'e'), QtGui.QKeySequence(u'f')],
            u'shortcuts/action_with_same_shortcuts3': [QtGui.QKeySequence(u'e'), QtGui.QKeySequence(u'f')]
        }
        Settings.extend_default_settings(default_shortcuts)

        # WHEN: Add the two actions to the action list.
        self.action_list.add_action(action3, u'example_category2')
        self.action_list.add_action(action_with_same_shortcuts3, u'example_category2')
        # Remove the actions again.
        self.action_list.remove_action(action3, u'example_category2')
        self.action_list.remove_action(action_with_same_shortcuts3, u'example_category2')

        # THEN: Both action should keep their shortcuts.
        assert len(action3.shortcuts()) == 2, u'The action should have two shortcut assigned.'
        assert len(action_with_same_shortcuts3.shortcuts()) == 2, u'The action should have two shortcuts assigned.'


