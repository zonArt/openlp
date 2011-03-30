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
from openlp.core.utils.actions import actionList
from shortcutlistdialog import Ui_ShortcutListDialog

REMOVE_AMPERSAND = re.compile(r'&{1}')

log = logging.getLogger(__name__)

class ShortcutListForm(QtGui.QDialog, Ui_ShortcutListDialog):
    """
    The shortcut list dialog
    """
#TODO: do not close on ESC
#TODO: Fix Preview/Live controller (have the same shortcut)
#TODO: double click event
#TODO: refresh self.assingedShortcuts
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.assingedShortcuts = []
        self.column = -1
        self.shortcutButton.setText(u'')
        QtCore.QObject.connect(self.shortcutButton,
            QtCore.SIGNAL(u'toggled(bool)'), self.onShortcutButtonClicked)
        QtCore.QObject.connect(self.treeWidget,
            QtCore.SIGNAL(u'itemPressed(QTreeWidgetItem*, int)'),
            self.onItemPressed)

    def keyReleaseEvent(self, event):
        Qt = QtCore.Qt
        if not self.shortcutButton.isChecked():
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
        if key_sequence in self.assingedShortcuts:
            QtGui.QMessageBox.warning(self,
                translate('OpenLP.ShortcutListDialog', 'Duplicate Shortcut'),
                unicode(translate('OpenLP.ShortcutListDialog', 'The shortcut '
                '"%s" is already assigned to another action, please '
                'use a different shortcut.')) % key_sequence.toString(),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok),
                QtGui.QMessageBox.Ok
            )
        else:
            self.shortcutButton.setText(key_sequence.toString())
            self.shortcutButton.setChecked(False)

    def exec_(self):
        self.reloadActionList()
        return QtGui.QDialog.exec_(self)

    def reloadActionList(self):
        """
        Reload the ``treeWidget`` list to add new and remove old actions.
        """
        self.assingedShortcuts = []
        self.treeWidget.clear()
        for category in actionList.categories:
            item = QtGui.QTreeWidgetItem([category.name])
            for action in category.actions:
                self.assingedShortcuts.extend(action.shortcuts())
                actionText = REMOVE_AMPERSAND.sub('', unicode(action.text()))
                if len(action.shortcuts()) == 2:
                    shortcutText = action.shortcuts()[0].toString()
                    alternateText = action.shortcuts()[1].toString()
                else:
                    shortcutText = action.shortcut().toString()
                    alternateText = u''
                actionItem = QtGui.QTreeWidgetItem(
                    [actionText, shortcutText, alternateText])
                actionItem.setIcon(0, action.icon())
                actionItem.setData(0,
                    QtCore.Qt.UserRole, QtCore.QVariant(action))
                item.addChild(actionItem)
            item.setExpanded(True)
            self.treeWidget.addTopLevelItem(item)

    def onShortcutButtonClicked(self, toggled):
        """
        Save the new shortcut to the action if the button is unchanged.
        """
        if toggled:
            return
        item = self.treeWidget.currentItem()
        action = item.data(0, QtCore.Qt.UserRole).toPyObject()
        if action is None:
            return
        shortcuts = []
        if self.column == 1:
            # We are changing the primary shortcut.
            shortcuts.append(QtGui.QKeySequence(self.shortcutButton.text()))
            if len(action.shortcuts()) == 2:
                shortcuts.append(action.shortcuts()[1])
            else:
                shortcuts.append(0)
            item.setText(1, self.shortcutButton.text())
        elif self.column == 2:
            # We are changing the secondary shortcut.
            if len(action.shortcuts()) == 1:
                shortcuts.append(action.shortcuts()[0])
            else:
                shortcuts.append(0)
            shortcuts.append(QtGui.QKeySequence(self.shortcutButton.text()))
            item.setText(2, self.shortcutButton.text())
        else:
            return
        action.setShortcuts(shortcuts)

    def onItemPressed(self, item, column):
        """
        A item has been pressed. We adjust the button's text to the action's
        shortcut which is encapsulate in the item.
        """
        self.column = column
        item = self.treeWidget.currentItem()
        action = item.data(0, QtCore.Qt.UserRole).toPyObject()
        self.shortcutButton.setEnabled(True)
        text = u''
        if action is None or column not in [1, 2]:
            self.shortcutButton.setEnabled(False)
        elif column == 1 and len(action.shortcuts()) != 0:
            text = action.shortcuts()[0].toString()
        elif len(action.shortcuts()) == 2 and len(action.shortcuts()) != 0:
            text = action.shortcuts()[1].toString()
        self.shortcutButton.setText(text)

    def save(self):
        """
        Save the shortcuts. **Note**, that we do not have to load the shortcuts,
        as they are loaded in :class:`~openlp.core.utils.ActionList`.
        """
        settings = QtCore.QSettings()
        settings.beginGroup(u'shortcuts')
        for category in actionList.categories:
            for action in category.actions:
                settings.setValue(
                    action.objectName(), QtCore.QVariant(action.shortcuts()))
        settings.endGroup()
