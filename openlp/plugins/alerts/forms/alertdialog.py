# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
        AlertDialog.resize(567, 440)
        AlertDialog.setWindowIcon(build_icon(u':/icon/openlp.org-icon-32.bmp'))
        self.AlertDialogLayout = QtGui.QVBoxLayout(AlertDialog)
        self.AlertDialogLayout.setSpacing(8)
        self.AlertDialogLayout.setMargin(8)
        self.AlertDialogLayout.setObjectName(u'AlertDialogLayout')
        self.AlertTextLayout = QtGui.QFormLayout()
        self.AlertTextLayout.setContentsMargins(0, 0, -1, -1)
        self.AlertTextLayout.setSpacing(8)
        self.AlertTextLayout.setObjectName(u'AlertTextLayout')
        self.AlertEntryLabel = QtGui.QLabel(AlertDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.AlertEntryLabel.sizePolicy().hasHeightForWidth())
        self.AlertEntryLabel.setSizePolicy(sizePolicy)
        self.AlertEntryLabel.setObjectName(u'AlertEntryLabel')
        self.AlertTextLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.AlertEntryLabel)
        self.AlertParameter = QtGui.QLabel(AlertDialog)
        self.AlertParameter.setObjectName(u'AlertParameter')
        self.AlertTextLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.AlertParameter)
        self.ParameterEdit = QtGui.QLineEdit(AlertDialog)
        self.ParameterEdit.setObjectName(u'ParameterEdit')
        self.AlertTextLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.ParameterEdit)
        self.AlertTextEdit = QtGui.QLineEdit(AlertDialog)
        self.AlertTextEdit.setObjectName(u'AlertTextEdit')
        self.AlertTextLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.AlertTextEdit)
        self.AlertDialogLayout.addLayout(self.AlertTextLayout)
        self.ManagementLayout = QtGui.QHBoxLayout()
        self.ManagementLayout.setSpacing(8)
        self.ManagementLayout.setContentsMargins(-1, -1, -1, 0)
        self.ManagementLayout.setObjectName(u'ManagementLayout')
        self.AlertListWidget = QtGui.QListWidget(AlertDialog)
        self.AlertListWidget.setAlternatingRowColors(True)
        self.AlertListWidget.setObjectName(u'AlertListWidget')
        self.ManagementLayout.addWidget(self.AlertListWidget)
        self.ManageButtonLayout = QtGui.QVBoxLayout()
        self.ManageButtonLayout.setSpacing(8)
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
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Expanding)
        self.ManageButtonLayout.addItem(spacerItem)
        self.ManagementLayout.addLayout(self.ManageButtonLayout)
        self.AlertDialogLayout.addLayout(self.ManagementLayout)
        self.AlertButtonLayout = QtGui.QHBoxLayout()
        self.AlertButtonLayout.setSpacing(8)
        self.AlertButtonLayout.setObjectName(u'AlertButtonLayout')
        spacerItem1 = QtGui.QSpacerItem(181, 0, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
        self.AlertButtonLayout.addItem(spacerItem1)
        displayIcon = build_icon(u':/general/general_live.png')
        self.DisplayButton = QtGui.QPushButton(AlertDialog)
        self.DisplayButton.setIcon(displayIcon)
        self.DisplayButton.setObjectName(u'DisplayButton')
        self.AlertButtonLayout.addWidget(self.DisplayButton)
        self.DisplayCloseButton = QtGui.QPushButton(AlertDialog)
        self.DisplayCloseButton.setIcon(displayIcon)
        self.DisplayCloseButton.setObjectName(u'DisplayCloseButton')
        self.AlertButtonLayout.addWidget(self.DisplayCloseButton)
        self.CloseButton = QtGui.QPushButton(AlertDialog)
        self.CloseButton.setIcon(build_icon(u':/system/system_close.png'))
        self.CloseButton.setObjectName(u'CloseButton')
        self.AlertButtonLayout.addWidget(self.CloseButton)
        self.AlertDialogLayout.addLayout(self.AlertButtonLayout)
        self.AlertEntryLabel.setBuddy(self.AlertTextEdit)
        self.AlertParameter.setBuddy(self.ParameterEdit)

        self.retranslateUi(AlertDialog)
        QtCore.QObject.connect(self.CloseButton, QtCore.SIGNAL(u'clicked()'),
            AlertDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AlertDialog)

    def retranslateUi(self, AlertDialog):
        AlertDialog.setWindowTitle(
            translate('AlertsPlugin.AlertForm', 'Alert Message'))
        self.AlertEntryLabel.setText(
            translate('AlertsPlugin.AlertForm', 'Alert &text:'))
        self.AlertParameter.setText(
            translate('AlertsPlugin.AlertForm', '&Parameter(s):'))
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
        self.CloseButton.setText(
            translate('AlertsPlugin.AlertForm', '&Close'))
