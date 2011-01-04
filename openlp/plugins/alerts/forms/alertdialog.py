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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import build_icon, translate

class Ui_AlertDialog(object):
    def setupUi(self, AlertDialog):
        AlertDialog.setObjectName(u'AlertDialog')
        AlertDialog.resize(400, 300)
        AlertDialog.setWindowIcon(build_icon(u':/icon/openlp.org-icon-32.bmp'))
        self.AlertDialogLayout = QtGui.QGridLayout(AlertDialog)
        self.AlertDialogLayout.setObjectName(u'AlertDialogLayout')
        self.AlertTextLayout = QtGui.QFormLayout()
        self.AlertTextLayout.setObjectName(u'AlertTextLayout')
        self.AlertEntryLabel = QtGui.QLabel(AlertDialog)
        self.AlertEntryLabel.setObjectName(u'AlertEntryLabel')
        self.AlertTextEdit = QtGui.QLineEdit(AlertDialog)
        self.AlertTextEdit.setObjectName(u'AlertTextEdit')
        self.AlertEntryLabel.setBuddy(self.AlertTextEdit)
        self.AlertTextLayout.addRow(self.AlertEntryLabel, self.AlertTextEdit)
        self.AlertParameter = QtGui.QLabel(AlertDialog)
        self.AlertParameter.setObjectName(u'AlertParameter')
        self.ParameterEdit = QtGui.QLineEdit(AlertDialog)
        self.ParameterEdit.setObjectName(u'ParameterEdit')
        self.AlertParameter.setBuddy(self.ParameterEdit)
        self.AlertTextLayout.addRow(self.AlertParameter, self.ParameterEdit)
        self.AlertDialogLayout.addLayout(self.AlertTextLayout, 0, 0, 1, 2)
        self.AlertListWidget = QtGui.QListWidget(AlertDialog)
        self.AlertListWidget.setAlternatingRowColors(True)
        self.AlertListWidget.setObjectName(u'AlertListWidget')
        self.AlertDialogLayout.addWidget(self.AlertListWidget, 1, 0)
        self.ManageButtonLayout = QtGui.QVBoxLayout()
        self.ManageButtonLayout.setObjectName(u'ManageButtonLayout')
        self.NewButton = QtGui.QPushButton(AlertDialog)
        self.NewButton.setIcon(build_icon(u':/general/general_new.png'))
        self.NewButton.setObjectName(u'NewButton')
        self.ManageButtonLayout.addWidget(self.NewButton)
        self.SaveButton = QtGui.QPushButton(AlertDialog)
        self.SaveButton.setEnabled(False)
        self.SaveButton.setIcon(build_icon(u':/general/general_save.png'))
        self.SaveButton.setObjectName(u'SaveButton')
        self.ManageButtonLayout.addWidget(self.SaveButton)
        self.DeleteButton = QtGui.QPushButton(AlertDialog)
        self.DeleteButton.setIcon(build_icon(u':/general/general_delete.png'))
        self.DeleteButton.setObjectName(u'DeleteButton')
        self.ManageButtonLayout.addWidget(self.DeleteButton)
        self.ManageButtonLayout.addStretch()
        self.AlertDialogLayout.addLayout(self.ManageButtonLayout, 1, 1)
        self.ButtonBox = QtGui.QDialogButtonBox(AlertDialog)
        self.ButtonBox.addButton(QtGui.QDialogButtonBox.Close)
        displayIcon = build_icon(u':/general/general_live.png')
        self.DisplayButton = QtGui.QPushButton(AlertDialog)
        self.DisplayButton.setIcon(displayIcon)
        self.DisplayButton.setObjectName(u'DisplayButton')
        self.ButtonBox.addButton(self.DisplayButton,
            QtGui.QDialogButtonBox.ActionRole)
        self.DisplayCloseButton = QtGui.QPushButton(AlertDialog)
        self.DisplayCloseButton.setIcon(displayIcon)
        self.DisplayCloseButton.setObjectName(u'DisplayCloseButton')
        self.ButtonBox.addButton(self.DisplayCloseButton,
            QtGui.QDialogButtonBox.ActionRole)
        self.AlertDialogLayout.addWidget(self.ButtonBox, 2, 0, 1, 2)
        self.retranslateUi(AlertDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'rejected()'),
            AlertDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AlertDialog)

    def retranslateUi(self, AlertDialog):
        AlertDialog.setWindowTitle(
            translate('AlertsPlugin.AlertForm', 'Alert Message'))
        self.AlertEntryLabel.setText(
            translate('AlertsPlugin.AlertForm', 'Alert &text:'))
        self.AlertParameter.setText(
            translate('AlertsPlugin.AlertForm', '&Parameter:'))
        self.NewButton.setText(
            translate('AlertsPlugin.AlertForm', '&New'))
        self.SaveButton.setText(
            translate('AlertsPlugin.AlertForm', '&Save'))
        self.DeleteButton.setText(
            translate('AlertsPlugin.AlertForm', '&Delete'))
        self.DisplayButton.setText(
            translate('AlertsPlugin.AlertForm', 'Displ&ay'))
        self.DisplayCloseButton.setText(
            translate('AlertsPlugin.AlertForm', 'Display && Cl&ose'))
