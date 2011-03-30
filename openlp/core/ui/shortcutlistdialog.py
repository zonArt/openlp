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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, build_icon

class Ui_ShortcutListDialog(object):
    def setupUi(self, shortcutListDialog):
        shortcutListDialog.resize(440, 450)
        shortcutListDialog.setObjectName(u'shortcutListDialog')
        self.dialogLayout = QtGui.QVBoxLayout(shortcutListDialog)
        self.dialogLayout.setObjectName(u'dialogLayout')
        self.treeWidget = QtGui.QTreeWidget(shortcutListDialog)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setObjectName(u'treeWidget')
        self.treeWidget.setColumnCount(3)
        self.dialogLayout.addWidget(self.treeWidget)
        self.customLayout = QtGui.QHBoxLayout()
        self.customLayout.setObjectName(u'customLayout')
        self.shortcutButton = QtGui.QPushButton(shortcutListDialog)
        self.shortcutButton.setIcon(
            build_icon(u':/system/system_configure_shortcuts.png'))
        self.shortcutButton.setCheckable(True)
        self.shortcutButton.setObjectName(u'shortcutButton')
        self.shortcutButton.setFixedSize(150, 30)
        self.customLayout.addWidget(self.shortcutButton)
        self.clearShortcutButton = QtGui.QToolButton(shortcutListDialog)
        self.clearShortcutButton.setIcon(
            build_icon(u':/system/clear_shortcut.png'))
        self.clearShortcutButton.setAutoRaise(True)
        self.clearShortcutButton.setObjectName(u'clearShortcutButton')
        self.customLayout.addWidget(self.clearShortcutButton)
        self.customLayout.addStretch()
        self.dialogLayout.addLayout(self.customLayout)
        self.buttonBox = QtGui.QDialogButtonBox(shortcutListDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(u'buttonBox')
        self.dialogLayout.addWidget(self.buttonBox)
        self.retranslateUi(shortcutListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'accepted()'),
            shortcutListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            shortcutListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(shortcutListDialog)

    def retranslateUi(self, shortcutListDialog):
        shortcutListDialog.setWindowTitle(
            translate('OpenLP.ShortcutListDialog', 'Customize Shortcuts'))
        self.treeWidget.setHeaderLabels([
            translate('OpenLP.ShortcutListDialog', 'Action'),
            translate('OpenLP.ShortcutListDialog', 'Shortcut'),
            translate('OpenLP.ShortcutListDialog', 'Alternate')])
        self.shortcutButton.setText(
            translate('OpenLP.ShortcutListDialog', 'None'))
