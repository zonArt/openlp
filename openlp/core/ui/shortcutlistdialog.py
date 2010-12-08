# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import translate, build_icon

class Ui_ShortcutListDialog(object):
    def setupUi(self, shortcutListDialog):
        shortcutListDialog.setObjectName(u'shortcutListDialog')
        shortcutListDialog.resize(500, 438)
        self.shortcutListLayout = QtGui.QVBoxLayout(shortcutListDialog)
        self.shortcutListLayout.setSpacing(8)
        self.shortcutListLayout.setMargin(8)
        self.shortcutListLayout.setObjectName(u'shortcutListLayout')
        self.shortcutListTreeWidget = QtGui.QTreeWidget(shortcutListDialog)
        self.shortcutListTreeWidget.setAlternatingRowColors(True)
        self.shortcutListTreeWidget.setObjectName(u'shortcutListTreeWidget')
        self.shortcutListTreeWidget.setColumnCount(3)
        self.shortcutListTreeWidget.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.shortcutListLayout.addWidget(self.shortcutListTreeWidget)
        self.shortcutLayout = QtGui.QVBoxLayout()
        self.shortcutLayout.setSpacing(8)
        self.shortcutLayout.setContentsMargins(0, -1, -1, -1)
        self.shortcutLayout.setObjectName(u'shortcutLayout')
        self.defaultRadioButton = QtGui.QRadioButton(shortcutListDialog)
        self.defaultRadioButton.setChecked(True)
        self.defaultRadioButton.setObjectName(u'defaultRadioButton')
        self.shortcutLayout.addWidget(self.defaultRadioButton)
        self.customShortcutLayout = QtGui.QHBoxLayout()
        self.customShortcutLayout.setSpacing(8)
        self.customShortcutLayout.setObjectName(u'customShortcutLayout')
        self.customRadioButton = QtGui.QRadioButton(shortcutListDialog)
        self.customRadioButton.setObjectName(u'customRadioButton')
        self.customShortcutLayout.addWidget(self.customRadioButton)
        self.shortcutPushButton = QtGui.QPushButton(shortcutListDialog)
        self.shortcutPushButton.setMinimumSize(QtCore.QSize(84, 0))
        self.shortcutPushButton.setIcon(
            build_icon(u':/system/system_configure_shortcuts.png'))
        self.shortcutPushButton.setCheckable(True)
        self.shortcutPushButton.setChecked(False)
        self.shortcutPushButton.setObjectName(u'shortcutPushButton')
        self.customShortcutLayout.addWidget(self.shortcutPushButton)
        self.clearShortcutToolButton = QtGui.QToolButton(shortcutListDialog)
        self.clearShortcutToolButton.setMinimumSize(QtCore.QSize(0, 16))
        self.clearShortcutToolButton.setText(u'')
        self.clearShortcutToolButton.setIcon(
            build_icon(u':/system/clear_shortcut.png'))
        self.clearShortcutToolButton.setObjectName(u'clearShortcutToolButton')
        self.customShortcutLayout.addWidget(self.clearShortcutToolButton)
        self.customShortcutSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.customShortcutLayout.addItem(self.customShortcutSpacer)
        self.shortcutLayout.addLayout(self.customShortcutLayout)
        self.shortcutListLayout.addLayout(self.shortcutLayout)
        self.shortcutListButtonBox = QtGui.QDialogButtonBox(shortcutListDialog)
        self.shortcutListButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.shortcutListButtonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok |
            QtGui.QDialogButtonBox.Reset)
        self.shortcutListButtonBox.setObjectName(u'shortcutListButtonBox')
        self.shortcutListLayout.addWidget(self.shortcutListButtonBox)

        self.retranslateUi(shortcutListDialog)
        QtCore.QObject.connect(
            self.shortcutListButtonBox,
            QtCore.SIGNAL(u'accepted()'),
            shortcutListDialog.accept
        )
        QtCore.QObject.connect(
            self.shortcutListButtonBox,
            QtCore.SIGNAL(u'rejected()'),
            shortcutListDialog.reject
        )
        QtCore.QMetaObject.connectSlotsByName(shortcutListDialog)

    def retranslateUi(self, shortcutListDialog):
        shortcutListDialog.setWindowTitle(
            translate('OpenLP.ShortcutListDialog', 'Customize Shortcuts'))
        self.shortcutListTreeWidget.setHeaderLabels([
            translate('OpenLP.ShortcutListDialog', 'Action'),
            translate('OpenLP.ShortcutListDialog', 'Shortcut'), 
            translate('OpenLP.ShortcutListDialog', 'Alternative')
        ])
        self.defaultRadioButton.setText(
            translate('OpenLP.ShortcutListDialog', 'Default: %s'))
        self.customRadioButton.setText(
            translate('OpenLP.ShortcutListDialog', 'Custom:'))
        self.shortcutPushButton.setText(
            translate('OpenLP.ShortcutListDialog', 'None'))

class Ui_ShortcutDialog(object):
    def setupUi(self, ShortcutDialog):
        ShortcutDialog.setObjectName(u'ShortcutDialog')
        ShortcutDialog.resize(539, 125)
        self.vboxlayout = QtGui.QVBoxLayout(ShortcutDialog)
        self.vboxlayout.setObjectName(u'vboxlayout')
        self.shortcutsGroup = QtGui.QGroupBox(ShortcutDialog)
        self.shortcutsGroup.setTitle(u'')
        self.shortcutsGroup.setObjectName(u'shortcutsGroup')
        self.gridlayout = QtGui.QGridLayout(self.shortcutsGroup)
        self.gridlayout.setObjectName(u'gridlayout')
        self.alternateButton = QtGui.QRadioButton(self.shortcutsGroup)
        self.alternateButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.alternateButton.setObjectName(u'alternateButton')
        self.gridlayout.addWidget(self.alternateButton, 1, 0, 1, 1)
        self.primaryClearButton = QtGui.QPushButton(self.shortcutsGroup)
        self.primaryClearButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.primaryClearButton.setObjectName(u'primaryClearButton')
        self.gridlayout.addWidget(self.primaryClearButton, 0, 1, 1, 1)
        self.alternateKeyLabel = QtGui.QLabel(self.shortcutsGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alternateKeyLabel.sizePolicy().hasHeightForWidth())
        self.alternateKeyLabel.setSizePolicy(sizePolicy)
        self.alternateKeyLabel.setToolTip(u'')
        self.alternateKeyLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.alternateKeyLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.alternateKeyLabel.setText(u'')
        self.alternateKeyLabel.setObjectName(u'alternateKeyLabel')
        self.gridlayout.addWidget(self.alternateKeyLabel, 1, 2, 1, 1)
        self.keyLabel = QtGui.QLabel(self.shortcutsGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keyLabel.sizePolicy().hasHeightForWidth())
        self.keyLabel.setSizePolicy(sizePolicy)
        self.keyLabel.setToolTip(u'')
        self.keyLabel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.keyLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.keyLabel.setText(u'')
        self.keyLabel.setObjectName(u'keyLabel')
        self.gridlayout.addWidget(self.keyLabel, 0, 2, 1, 1)
        self.primaryButton = QtGui.QRadioButton(self.shortcutsGroup)
        self.primaryButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.primaryButton.setChecked(True)
        self.primaryButton.setObjectName(u'primaryButton')
        self.gridlayout.addWidget(self.primaryButton, 0, 0, 1, 1)
        self.alternateClearButton = QtGui.QPushButton(self.shortcutsGroup)
        self.alternateClearButton.setEnabled(False)
        self.alternateClearButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.alternateClearButton.setObjectName(u'alternateClearButton')
        self.gridlayout.addWidget(self.alternateClearButton, 1, 1, 1, 1)
        self.vboxlayout.addWidget(self.shortcutsGroup)
        self.buttonBox = QtGui.QDialogButtonBox(ShortcutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ShortcutDialog)
        QtCore.QObject.connect(self.primaryButton, QtCore.SIGNAL(u'toggled(bool)'), self.primaryClearButton.setEnabled)
        QtCore.QObject.connect(self.alternateButton, QtCore.SIGNAL(u'toggled(bool)'), self.alternateClearButton.setEnabled)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'), ShortcutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ShortcutDialog)

    def retranslateUi(self, ShortcutDialog):
        ShortcutDialog.setWindowTitle(QtGui.QApplication.translate("ShortcutDialog", "Edit Shortcut", None, QtGui.QApplication.UnicodeUTF8))
        ShortcutDialog.setWhatsThis(QtGui.QApplication.translate("ShortcutDialog", "Press your shortcut keys and select OK", None, QtGui.QApplication.UnicodeUTF8))
        self.alternateButton.setToolTip(QtGui.QApplication.translate("ShortcutDialog", "Select to change the alternative keyboard shortcut", None, QtGui.QApplication.UnicodeUTF8))
        self.alternateButton.setText(QtGui.QApplication.translate("ShortcutDialog", "Alternative Shortcut:", None, QtGui.QApplication.UnicodeUTF8))
        self.primaryClearButton.setToolTip(QtGui.QApplication.translate("ShortcutDialog", "Press to clear the key sequence buffer.", None, QtGui.QApplication.UnicodeUTF8))
        self.primaryClearButton.setText(QtGui.QApplication.translate("ShortcutDialog", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.primaryButton.setToolTip(QtGui.QApplication.translate("ShortcutDialog", "Select to change the primary keyboard shortcut", None, QtGui.QApplication.UnicodeUTF8))
        self.primaryButton.setText(QtGui.QApplication.translate("ShortcutDialog", "Primary Shortcut:", None, QtGui.QApplication.UnicodeUTF8))
        self.alternateClearButton.setToolTip(QtGui.QApplication.translate("ShortcutDialog", "Press to clear the key sequence buffer.", None, QtGui.QApplication.UnicodeUTF8))
        self.alternateClearButton.setText(QtGui.QApplication.translate("ShortcutDialog", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        
