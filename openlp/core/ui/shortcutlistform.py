# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
from shortcutlistdialog import Ui_ShortcutListDialog

REMOVE_AMPERSAND = re.compile(r'&{1}')

log = logging.getLogger(__name__)

class ShortcutListForm(QtGui.QDialog, Ui_ShortcutListDialog):
    """
    The shortcut list dialog
    """

    def __init__(self, parent):
        """
        Do some initialisation stuff
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.actionList = None
        self.captureShortcut = False
        QtCore.QObject.connect(self.shortcutButton,
            QtCore.SIGNAL(u'toggled(bool)'), self.onShortcutButtonClicked)

    def keyReleaseEvent(self, event):
        Qt = QtCore.Qt
        if not self.captureShortcut:
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
        existing_key = QtGui.QKeySequence(u'Ctrl+Shift+F8')
        if key_sequence == existing_key:
            QtGui.QMessageBox.warning(
                self,
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
        self.captureShortcut = False

    def exec_(self, actionList):
        self.actionList = actionList
        self.refreshActions()
        return QtGui.QDialog.exec_(self)

    def refreshActions(self):
        self.treeWidget.clear()
        for category in self.actionList.categories:
            item = QtGui.QTreeWidgetItem([category.name])
            for action in category.actions:
                actionText = REMOVE_AMPERSAND.sub('', unicode(action.text()))
                if (len(action.shortcuts()) == 2):
                    shortcutText = action.shortcuts()[0].toString()
                    alternateText = action.shortcuts()[1].toString()
                else:
                    shortcutText = action.shortcut().toString()
                    alternateText = u''
                actionItem = QtGui.QTreeWidgetItem([actionText, shortcutText, alternateText])
                actionItem.setIcon(0, action.icon())
                item.addChild(actionItem)
            item.setExpanded(True)
            self.treeWidget.addTopLevelItem(item)

    def onShortcutButtonClicked(self, toggled):
        self.captureShortcut = toggled
