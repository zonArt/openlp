# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

import logging
import re

from PyQt4 import QtCore, QtGui

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
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.changedActions = {}
        QtCore.QObject.connect(self.primaryPushButton,
            QtCore.SIGNAL(u'toggled(bool)'), self.onPrimaryPushButtonClicked)
        QtCore.QObject.connect(self.alternatePushButton,
            QtCore.SIGNAL(u'toggled(bool)'), self.onAlternatePushButtonClicked)
        QtCore.QObject.connect(self.treeWidget,
            QtCore.SIGNAL(u'itemPressed(QTreeWidgetItem*, int)'),
            self.onItemPressed)
        QtCore.QObject.connect(self.treeWidget,
            QtCore.SIGNAL(u'itemDoubleClicked(QTreeWidgetItem*, int)'),
            self.onItemDoubleClicked)
        QtCore.QObject.connect(self.clearPrimaryButton,
            QtCore.SIGNAL(u'clicked(bool)'), self.onClearPrimaryButtonClicked)
        QtCore.QObject.connect(self.clearAlternateButton,
            QtCore.SIGNAL(u'clicked(bool)'), self.onClearAlternateButtonClicked)
        QtCore.QObject.connect(self.buttonBox,
            QtCore.SIGNAL(u'clicked(QAbstractButton*)'),
            self.onRestoreDefaultsClicked)

    def keyPressEvent(self, event):
        if self.primaryPushButton.isChecked() or \
            self.alternatePushButton.isChecked():
            event.ignore()
        elif event.key() == QtCore.Qt.Key_Escape:
            event.accept()
            self.close()

    def keyReleaseEvent(self, event):
        Qt = QtCore.Qt
        if not self.primaryPushButton.isChecked() and \
            not self.alternatePushButton.isChecked():
            return
        key = event.key()
        if key == Qt.Key_Shift or key == Qt.Key_Control or \
            key == Qt.Key_Meta or key == Qt.Key_Alt:
            return
        key_string = QtGui.QKeySequence(key).toString()
        if event.modifiers() & Qt.ControlModifier == Qt.ControlModifier:
            key_string = u'Ctrl+' + key_string
        if event.modifiers() & Qt.AltModifier == Qt.AltModifier:
            key_string = u'Alt+' + key_string
        if event.modifiers() & Qt.ShiftModifier == Qt.ShiftModifier:
            key_string = u'Shift+' + key_string
        key_sequence = QtGui.QKeySequence(key_string)
        # The action we are attempting to change.
        changing_action = self._currentItemAction()
        shortcut_valid = True
        for category in ActionList.categories:
            for action in category.actions:
                shortcuts = self._actionShortcuts(action)
                if key_sequence not in shortcuts:
                    continue
                if action is changing_action:
                    if self.primaryPushButton.isChecked() and \
                        shortcuts.index(key_sequence) == 0:
                        continue
                    if self.alternatePushButton.isChecked() and \
                        shortcuts.index(key_sequence) == 1:
                        continue
                # Have the same parent, thus they cannot have the same shortcut.
                if action.parent() is changing_action.parent():
                    shortcut_valid = False
                # The new shortcut is already assigned, but if both shortcuts
                # are only valid in a different widget the new shortcut is
                # vaild, because they will not interfere.
                if action.shortcutContext() in [QtCore.Qt.WindowShortcut,
                    QtCore.Qt.ApplicationShortcut]:
                    shortcut_valid = False
                if changing_action.shortcutContext() in \
                    [QtCore.Qt.WindowShortcut, QtCore.Qt.ApplicationShortcut]:
                    shortcut_valid = False
        if not shortcut_valid:
            QtGui.QMessageBox.warning(self,
                translate('OpenLP.ShortcutListDialog', 'Duplicate Shortcut'),
                unicode(translate('OpenLP.ShortcutListDialog', 'The shortcut '
                '"%s" is already assigned to another action, please '
                'use a different shortcut.')) % key_sequence.toString(),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok),
                QtGui.QMessageBox.Ok
            )
        else:
            if self.primaryPushButton.isChecked():
                self._adjustButton(self.primaryPushButton,
                    checked=False, text=key_sequence.toString())
            elif self.alternatePushButton.isChecked():
                self._adjustButton(self.alternatePushButton,
                    checked=False, text=key_sequence.toString())

    def exec_(self):
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
        for category in ActionList.categories:
            # Check if the category is for internal use only.
            if category.name is None:
                continue
            item = QtGui.QTreeWidgetItem([category.name])
            for action in category.actions:
                actionText = REMOVE_AMPERSAND.sub('', unicode(action.text()))
                actionItem = QtGui.QTreeWidgetItem([actionText])
                actionItem.setIcon(0, action.icon())
                actionItem.setData(0,
                    QtCore.Qt.UserRole, QtCore.QVariant(action))
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
            if len(shortcuts) == 0:
                item.setText(1, u'')
                item.setText(2, u'')
            elif len(shortcuts) == 1:
                item.setText(1, shortcuts[0].toString())
                item.setText(2, u'')
            else:
                item.setText(1, shortcuts[0].toString())
                item.setText(2, shortcuts[1].toString())

    def onPrimaryPushButtonClicked(self, toggled):
        """
        Save the new shortcut to the action if the button is unchanged.
        """
        if toggled:
            self.alternatePushButton.setChecked(False)
            return
        action = self._currentItemAction()
        if action is None:
            return
        shortcuts = self._actionShortcuts(action)
        new_shortcuts = []
        new_shortcuts.append(
            QtGui.QKeySequence(self.primaryPushButton.text()))
        if len(shortcuts) == 2:
            new_shortcuts.append(shortcuts[1])
        self.changedActions[action] = new_shortcuts
        self.refreshShortcutList()

    def onAlternatePushButtonClicked(self, toggled):
        """
        """
        if toggled:
            self.primaryPushButton.setChecked(False)
            return
        action = self._currentItemAction()
        if action is None:
            return
        shortcuts = self._actionShortcuts(action)
        new_shortcuts = []
        if len(shortcuts) != 0:
            new_shortcuts.append(shortcuts[0])
        new_shortcuts.append(
            QtGui.QKeySequence(self.alternatePushButton.text()))
        self.changedActions[action] = new_shortcuts
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
            self.primaryPushButton.setFocus(QtCore.Qt.OtherFocusReason)
        else:
            self.alternatePushButton.setFocus(QtCore.Qt.OtherFocusReason)
        self.onItemPressed()

    def onItemPressed(self, item=None, column=-1):
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
            if len(action.defaultShortcuts) != 0:
                primary_label_text = action.defaultShortcuts[0].toString()
                if len(action.defaultShortcuts) == 2:
                    alternate_label_text = action.defaultShortcuts[1].toString()
            shortcuts = self._actionShortcuts(action)
            if shortcuts != action.defaultShortcuts:
                self.customRadioButton.setChecked(True)
                if len(shortcuts) == 1:
                    primary_text = shortcuts[0].toString()
                elif len(shortcuts) == 2:
                    primary_text = shortcuts[0].toString()
                    alternate_text = shortcuts[1].toString()
            else:
                self.defaultRadioButton.setChecked(True)
        self.primaryPushButton.setText(primary_text)
        self.alternatePushButton.setText(alternate_text)
        self.primaryLabel.setText(primary_label_text)
        self.alternateLabel.setText(alternate_label_text)

    def onRestoreDefaultsClicked(self, button):
        """
        Restores all default shortcuts.
        """
        if self.buttonBox.buttonRole(button) != QtGui.QDialogButtonBox.ResetRole:
            return
        if QtGui.QMessageBox.question(self,
            translate('OpenLP.ShortcutListDialog', 'Restore Default Shortcuts'),
            translate('OpenLP.ShortcutListDialog', 'Do you want to restore all '
            'shortcuts to their defaults?'), QtGui.QMessageBox.StandardButtons(
            QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No)) == QtGui.QMessageBox.No:
            return
        self._adjustButton(self.primaryPushButton, False, text=u'')
        self._adjustButton(self.alternatePushButton, False, text=u'')
        for category in ActionList.categories:
            for action in category.actions:
                self.changedActions[action] = action.defaultShortcuts
        self.refreshShortcutList()

    def save(self):
        """
        Save the shortcuts. **Note**, that we do not have to load the shortcuts,
        as they are loaded in :class:`~openlp.core.utils.ActionList`.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(u'shortcuts')
        for category in ActionList.categories:
            # Check if the category is for internal use only.
            if category.name is None:
                continue
            for action in category.actions:
                if self.changedActions .has_key(action):
                    action.setShortcuts(self.changedActions[action])
                settings.setValue(
                    action.objectName(), QtCore.QVariant(action.shortcuts()))
        settings.endGroup()

    def onClearPrimaryButtonClicked(self, toggled):
        """
        Restore the defaults of this action.
        """
        self._clearButtonClicked(self.primaryPushButton)

    def onClearAlternateButtonClicked(self, toggled):
        """
        Restore the defaults of this action.
        """
        self._clearButtonClicked(self.alternatePushButton)

    def _clearButtonClicked(self, button):
        """
        Restore the defaults of this action. The given ``button`` will be
        unchecked.
        """
        button.setChecked(False)
        action = self._currentItemAction()
        if action is None:
            return
        self.changedActions[action] = action.defaultShortcuts
        self.refreshShortcutList()
        self.onItemPressed()

    def _actionShortcuts(self, action):
        """
        This returns the shortcuts for the given ``action``, which also includes
        those shortcuts which are not saved yet but already assigned (as changes
        are applied when closing the dialog).
        """
        if self.changedActions.has_key(action):
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
        return item.data(0, QtCore.Qt.UserRole).toPyObject()

    def _adjustButton(self, button, checked=None, enabled=None, text=None):
        """
        Can be called to adjust more properties of the given ``button`` at once.
        """
        if checked is not None:
            button.setChecked(checked)
        if enabled is not None:
            button.setEnabled(enabled)
        if text is not None:
            button.setText(text)
