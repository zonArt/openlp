# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
The :mod:`~openlp.core.ui.shortcutlistform` module contains the form class"""
import logging
import re

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Registry, Settings
from openlp.core.utils import translate
from openlp.core.utils.actions import ActionList
from shortcutlistdialog import Ui_ShortcutListDialog

REMOVE_AMPERSAND = re.compile(r'&{1}')

log = logging.getLogger(__name__)


class ShortcutListForm(QtGui.QDialog, Ui_ShortcutListDialog):
    """
    The shortcut list dialog
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.changedActions = {}
        self.action_list = ActionList.get_instance()
        QtCore.QObject.connect(self.primaryPushButton, QtCore.SIGNAL(u'toggled(bool)'),
            self.onPrimaryPushButtonClicked)
        QtCore.QObject.connect(self.alternatePushButton, QtCore.SIGNAL(u'toggled(bool)'),
            self.onAlternatePushButtonClicked)
        QtCore.QObject.connect(self.treeWidget,
            QtCore.SIGNAL(u'currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)'), self.onCurrentItemChanged)
        QtCore.QObject.connect(self.treeWidget, QtCore.SIGNAL(u'itemDoubleClicked(QTreeWidgetItem*, int)'),
            self.onItemDoubleClicked)
        QtCore.QObject.connect(self.clearPrimaryButton, QtCore.SIGNAL(u'clicked(bool)'),
            self.onClearPrimaryButtonClicked)
        QtCore.QObject.connect(self.clearAlternateButton, QtCore.SIGNAL(u'clicked(bool)'),
            self.onClearAlternateButtonClicked)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(u'clicked(QAbstractButton*)'),
            self.onRestoreDefaultsClicked)
        QtCore.QObject.connect(self.defaultRadioButton, QtCore.SIGNAL(u'clicked(bool)'),
            self.onDefaultRadioButtonClicked)
        QtCore.QObject.connect(self.customRadioButton, QtCore.SIGNAL(u'clicked(bool)'),
            self.onCustomRadioButtonClicked)

    def keyPressEvent(self, event):
        """
        Respond to certain key presses
        """
        if event.key() == QtCore.Qt.Key_Space:
            self.keyReleaseEvent(event)
        elif self.primaryPushButton.isChecked() or self.alternatePushButton.isChecked():
            event.ignore()
        elif event.key() == QtCore.Qt.Key_Escape:
            event.accept()
            self.close()

    def keyReleaseEvent(self, event):
        """
        Respond to certain key presses
        """
        if not self.primaryPushButton.isChecked() and not self.alternatePushButton.isChecked():
            return
        key = event.key()
        if key == QtCore.Qt.Key_Shift or key == QtCore.Qt.Key_Control or \
            key == QtCore.Qt.Key_Meta or key == QtCore.Qt.Key_Alt:
            return
        key_string = QtGui.QKeySequence(key).toString()
        if event.modifiers() & QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier:
            key_string = u'Ctrl+' + key_string
        if event.modifiers() & QtCore.Qt.AltModifier == QtCore.Qt.AltModifier:
            key_string = u'Alt+' + key_string
        if event.modifiers() & QtCore.Qt.ShiftModifier == QtCore.Qt.ShiftModifier:
            key_string = u'Shift+' + key_string
        if event.modifiers() & QtCore.Qt.MetaModifier == QtCore.Qt.MetaModifier:
            key_string = u'Meta+' + key_string
        key_sequence = QtGui.QKeySequence(key_string)
        if self._validiate_shortcut(self._currentItemAction(), key_sequence):
            if self.primaryPushButton.isChecked():
                self._adjustButton(self.primaryPushButton,
                    False, text=key_sequence.toString())
            elif self.alternatePushButton.isChecked():
                self._adjustButton(self.alternatePushButton,
                    False, text=key_sequence.toString())

    def exec_(self):
        """
        Execute the dialog
        """
        self.changedActions = {}
        self.reloadShortcutList()
        self._adjustButton(self.primaryPushButton, False, False, u'')
        self._adjustButton(self.alternatePushButton, False, False, u'')
        return QtGui.QDialog.exec_(self)

    def reloadShortcutList(self):
        """
        Reload the ``treeWidget`` list to add new and remove old actions.
        """
        self.treeWidget.clear()
        for category in self.action_list.categories:
            # Check if the category is for internal use only.
            if category.name is None:
                continue
            item = QtGui.QTreeWidgetItem([category.name])
            for action in category.actions:
                actionText = REMOVE_AMPERSAND.sub('', action.text())
                actionItem = QtGui.QTreeWidgetItem([actionText])
                actionItem.setIcon(0, action.icon())
                actionItem.setData(0, QtCore.Qt.UserRole, action)
                item.addChild(actionItem)
            self.treeWidget.addTopLevelItem(item)
            item.setExpanded(True)
        self.refreshShortcutList()

    def refreshShortcutList(self):
        """
        This refreshes the item's shortcuts shown in the list. Note, this
        neither adds new actions nor removes old actions.
        """
        iterator = QtGui.QTreeWidgetItemIterator(self.treeWidget)
        while iterator.value():
            item = iterator.value()
            iterator += 1
            action = self._currentItemAction(item)
            if action is None:
                continue
            shortcuts = self._actionShortcuts(action)
            if not shortcuts:
                item.setText(1, u'')
                item.setText(2, u'')
            elif len(shortcuts) == 1:
                item.setText(1, shortcuts[0].toString())
                item.setText(2, u'')
            else:
                item.setText(1, shortcuts[0].toString())
                item.setText(2, shortcuts[1].toString())
        self.onCurrentItemChanged()

    def onPrimaryPushButtonClicked(self, toggled):
        """
        Save the new primary shortcut.
        """
        self.customRadioButton.setChecked(True)
        if toggled:
            self.alternatePushButton.setChecked(False)
            self.primaryPushButton.setText(u'')
            return
        action = self._currentItemAction()
        if action is None:
            return
        shortcuts = self._actionShortcuts(action)
        new_shortcuts = [QtGui.QKeySequence(self.primaryPushButton.text())]
        if len(shortcuts) == 2:
            new_shortcuts.append(shortcuts[1])
        self.changedActions[action] = new_shortcuts
        self.refreshShortcutList()

    def onAlternatePushButtonClicked(self, toggled):
        """
        Save the new alternate shortcut.
        """
        self.customRadioButton.setChecked(True)
        if toggled:
            self.primaryPushButton.setChecked(False)
            self.alternatePushButton.setText(u'')
            return
        action = self._currentItemAction()
        if action is None:
            return
        shortcuts = self._actionShortcuts(action)
        new_shortcuts = []
        if shortcuts:
            new_shortcuts.append(shortcuts[0])
        new_shortcuts.append(
            QtGui.QKeySequence(self.alternatePushButton.text()))
        self.changedActions[action] = new_shortcuts
        if not self.primaryPushButton.text():
            # When we do not have a primary shortcut, the just entered alternate
            # shortcut will automatically become the primary shortcut. That is
            # why we have to adjust the primary button's text.
            self.primaryPushButton.setText(self.alternatePushButton.text())
            self.alternatePushButton.setText(u'')
        self.refreshShortcutList()

    def onItemDoubleClicked(self, item, column):
        """
        A item has been double clicked. The ``primaryPushButton`` will be
        checked and the item's shortcut will be displayed.
        """
        action = self._currentItemAction(item)
        if action is None:
            return
        self.primaryPushButton.setChecked(column in [0, 1])
        self.alternatePushButton.setChecked(column not in [0, 1])
        if column in [0, 1]:
            self.primaryPushButton.setText(u'')
            self.primaryPushButton.setFocus()
        else:
            self.alternatePushButton.setText(u'')
            self.alternatePushButton.setFocus()

    def onCurrentItemChanged(self, item=None, previousItem=None):
        """
        A item has been pressed. We adjust the button's text to the action's
        shortcut which is encapsulate in the item.
        """
        action = self._currentItemAction(item)
        self.primaryPushButton.setEnabled(action is not None)
        self.alternatePushButton.setEnabled(action is not None)
        primary_text = u''
        alternate_text = u''
        primary_label_text = u''
        alternate_label_text = u''
        if action is None:
            self.primaryPushButton.setChecked(False)
            self.alternatePushButton.setChecked(False)
        else:
            if action.defaultShortcuts:
                primary_label_text = action.defaultShortcuts[0].toString()
                if len(action.defaultShortcuts) == 2:
                    alternate_label_text = action.defaultShortcuts[1].toString()
            shortcuts = self._actionShortcuts(action)
            # We do not want to loose pending changes, that is why we have to
            # keep the text when, this function has not been triggered by a
            # signal.
            if item is None:
                primary_text = self.primaryPushButton.text()
                alternate_text = self.alternatePushButton.text()
            elif len(shortcuts) == 1:
                primary_text = shortcuts[0].toString()
            elif len(shortcuts) == 2:
                primary_text = shortcuts[0].toString()
                alternate_text = shortcuts[1].toString()
        # When we are capturing a new shortcut, we do not want, the buttons to
        # display the current shortcut.
        if self.primaryPushButton.isChecked():
            primary_text = u''
        if self.alternatePushButton.isChecked():
            alternate_text = u''
        self.primaryPushButton.setText(primary_text)
        self.alternatePushButton.setText(alternate_text)
        self.primaryLabel.setText(primary_label_text)
        self.alternateLabel.setText(alternate_label_text)
        # We do not want to toggle and radio button, as the function has not
        # been triggered by a signal.
        if item is None:
            return
        if primary_label_text == primary_text and alternate_label_text == alternate_text:
            self.defaultRadioButton.toggle()
        else:
            self.customRadioButton.toggle()

    def onRestoreDefaultsClicked(self, button):
        """
        Restores all default shortcuts.
        """
        if self.button_box.buttonRole(button) != QtGui.QDialogButtonBox.ResetRole:
            return
        if QtGui.QMessageBox.question(self, translate('OpenLP.ShortcutListDialog', 'Restore Default Shortcuts'),
            translate('OpenLP.ShortcutListDialog', 'Do you want to restore all '
                'shortcuts to their defaults?'),
            QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)) == QtGui.QMessageBox.No:
            return
        self._adjustButton(self.primaryPushButton, False, text=u'')
        self._adjustButton(self.alternatePushButton, False, text=u'')
        for category in self.action_list.categories:
            for action in category.actions:
                self.changedActions[action] = action.defaultShortcuts
        self.refreshShortcutList()

    def onDefaultRadioButtonClicked(self, toggled):
        """
        The default radio button has been clicked, which means we have to make
        sure, that we use the default shortcuts for the action.
        """
        if not toggled:
            return
        action = self._currentItemAction()
        if action is None:
            return
        temp_shortcuts = self._actionShortcuts(action)
        self.changedActions[action] = action.defaultShortcuts
        self.refreshShortcutList()
        primary_button_text = u''
        alternate_button_text = u''
        if temp_shortcuts:
            primary_button_text = temp_shortcuts[0].toString()
        if len(temp_shortcuts) == 2:
            alternate_button_text = temp_shortcuts[1].toString()
        self.primaryPushButton.setText(primary_button_text)
        self.alternatePushButton.setText(alternate_button_text)

    def onCustomRadioButtonClicked(self, toggled):
        """
        The custom shortcut radio button was clicked, thus we have to restore
        the custom shortcuts by calling those functions triggered by button
        clicks.
        """
        if not toggled:
            return
        self.onPrimaryPushButtonClicked(False)
        self.onAlternatePushButtonClicked(False)
        self.refreshShortcutList()

    def save(self):
        """
        Save the shortcuts. **Note**, that we do not have to load the shortcuts,
        as they are loaded in :class:`~openlp.core.utils.ActionList`.
        """
        settings = Settings()
        settings.beginGroup(u'shortcuts')
        for category in self.action_list.categories:
            # Check if the category is for internal use only.
            if category.name is None:
                continue
            for action in category.actions:
                if action in self.changedActions:
                    old_shortcuts = map(unicode,
                        map(QtGui.QKeySequence.toString, action.shortcuts()))
                    action.setShortcuts(self.changedActions[action])
                    self.action_list.update_shortcut_map(action, old_shortcuts)
                settings.setValue(action.objectName(), action.shortcuts())
        settings.endGroup()

    def onClearPrimaryButtonClicked(self, toggled):
        """
        Restore the defaults of this action.
        """
        self.primaryPushButton.setChecked(False)
        action = self._currentItemAction()
        if action is None:
            return
        shortcuts = self._actionShortcuts(action)
        new_shortcuts = []
        if action.defaultShortcuts:
            new_shortcuts.append(action.defaultShortcuts[0])
            # We have to check if the primary default shortcut is available. But
            # we only have to check, if the action has a default primary
            # shortcut (an "empty" shortcut is always valid and if the action
            # does not have a default primary shortcut, then the alternative
            # shortcut (not the default one) will become primary shortcut, thus
            # the check will assume that an action were going to have the same
            # shortcut twice.
            if not self._validiate_shortcut(action, new_shortcuts[0]) and new_shortcuts[0] != shortcuts[0]:
                return
        if len(shortcuts) == 2:
            new_shortcuts.append(shortcuts[1])
        self.changedActions[action] = new_shortcuts
        self.refreshShortcutList()
        self.onCurrentItemChanged(self.treeWidget.currentItem())

    def onClearAlternateButtonClicked(self, toggled):
        """
        Restore the defaults of this action.
        """
        self.alternatePushButton.setChecked(False)
        action = self._currentItemAction()
        if action is None:
            return
        shortcuts = self._actionShortcuts(action)
        new_shortcuts = []
        if shortcuts:
            new_shortcuts.append(shortcuts[0])
        if len(action.defaultShortcuts) == 2:
            new_shortcuts.append(action.defaultShortcuts[1])
        if len(new_shortcuts) == 2:
            if not self._validiate_shortcut(action, new_shortcuts[1]):
                return
        self.changedActions[action] = new_shortcuts
        self.refreshShortcutList()
        self.onCurrentItemChanged(self.treeWidget.currentItem())

    def _validiate_shortcut(self, changing_action, key_sequence):
        """
        Checks if the given ``changing_action `` can use the given
        ``key_sequence``. Returns ``True`` if the ``key_sequence`` can be used
        by the action, otherwise displays a dialog and returns ``False``.

        ``changing_action``
            The action which wants to use the ``key_sequence``.

        ``key_sequence``
            The key sequence which the action want so use.
        """
        is_valid = True
        for category in self.action_list.categories:
            for action in category.actions:
                shortcuts = self._actionShortcuts(action)
                if key_sequence not in shortcuts:
                    continue
                if action is changing_action:
                    if self.primaryPushButton.isChecked() and shortcuts.index(key_sequence) == 0:
                        continue
                    if self.alternatePushButton.isChecked() and shortcuts.index(key_sequence) == 1:
                        continue
                # Have the same parent, thus they cannot have the same shortcut.
                if action.parent() is changing_action.parent():
                    is_valid = False
                # The new shortcut is already assigned, but if both shortcuts
                # are only valid in a different widget the new shortcut is
                # vaild, because they will not interfere.
                if action.shortcutContext() in [QtCore.Qt.WindowShortcut,
                    QtCore.Qt.ApplicationShortcut]:
                    is_valid = False
                if changing_action.shortcutContext() in [QtCore.Qt.WindowShortcut, QtCore.Qt.ApplicationShortcut]:
                    is_valid = False
        if not is_valid:
            self.main_window.warning_message( {
                u'title': translate('OpenLP.ShortcutListDialog', 'Duplicate Shortcut'),
                u'message': translate('OpenLP.ShortcutListDialog',
                    'The shortcut "%s" is already assigned to another action, '
                    'please use a different shortcut.') % key_sequence.toString()
            })
        return is_valid

    def _actionShortcuts(self, action):
        """
        This returns the shortcuts for the given ``action``, which also includes
        those shortcuts which are not saved yet but already assigned (as changes
        are applied when closing the dialog).
        """
        if action in self.changedActions:
            return self.changedActions[action]
        return action.shortcuts()

    def _currentItemAction(self, item=None):
        """
        Returns the action of the given ``item``. If no item is given, we return
        the action of the current item of the ``treeWidget``.
        """
        if item is None:
            item = self.treeWidget.currentItem()
            if item is None:
                return
        return item.data(0, QtCore.Qt.UserRole)

    def _adjustButton(self, button, checked=None, enabled=None, text=None):
        """
        Can be called to adjust more properties of the given ``button`` at once.
        """
        # Set the text before checking the button, because this emits a signal.
        if text is not None:
            button.setText(text)
        if checked is not None:
            button.setChecked(checked)
        if enabled is not None:
            button.setEnabled(enabled)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)