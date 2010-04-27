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
from openlp.core.lib import translate

class Ui_AlertDialog(object):
    def setupUi(self, AlertForm):
        AlertForm.setObjectName(u'AlertDialog')
        AlertForm.resize(567, 440)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/icon/openlp.org-icon-32.bmp'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlertForm.setWindowIcon(icon)
        self.AlertFormLayout = QtGui.QVBoxLayout(AlertForm)
        self.AlertFormLayout.setSpacing(8)
        self.AlertFormLayout.setMargin(8)
        self.AlertFormLayout.setObjectName(u'AlertFormLayout')
        self.AlertTextLayout = QtGui.QFormLayout()
        self.AlertTextLayout.setContentsMargins(0, 0, -1, -1)
        self.AlertTextLayout.setSpacing(8)
        self.AlertTextLayout.setObjectName(u'AlertTextLayout')
        self.AlertEntryLabel = QtGui.QLabel(AlertForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryLabel.sizePolicy().hasHeightForWidth())
        self.AlertEntryLabel.setSizePolicy(sizePolicy)
        self.AlertEntryLabel.setObjectName(u'AlertEntryLabel')
        self.AlertTextLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.AlertEntryLabel)
        self.AlertParameter = QtGui.QLabel(AlertForm)
        self.AlertParameter.setObjectName(u'AlertParameter')
        self.AlertTextLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.AlertParameter)
        self.ParameterEdit = QtGui.QLineEdit(AlertForm)
        self.ParameterEdit.setObjectName(u'ParameterEdit')
        self.AlertTextLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ParameterEdit)
        self.AlertTextEdit = QtGui.QLineEdit(AlertForm)
        self.AlertTextEdit.setObjectName(u'AlertTextEdit')
        self.AlertTextLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.AlertTextEdit)
        self.AlertFormLayout.addLayout(self.AlertTextLayout)
        self.ManagementLayout = QtGui.QHBoxLayout()
        self.ManagementLayout.setSpacing(8)
        self.ManagementLayout.setContentsMargins(-1, -1, -1, 0)
        self.ManagementLayout.setObjectName(u'ManagementLayout')
        self.AlertListWidget = QtGui.QListWidget(AlertForm)
        self.AlertListWidget.setAlternatingRowColors(True)
        self.AlertListWidget.setObjectName(u'AlertListWidget')
        self.ManagementLayout.addWidget(self.AlertListWidget)
        self.ManageButtonLayout = QtGui.QVBoxLayout()
        self.ManageButtonLayout.setSpacing(8)
        self.ManageButtonLayout.setObjectName(u'ManageButtonLayout')
        self.NewButton = QtGui.QPushButton(AlertForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(u':/general/general_new.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NewButton.setIcon(icon1)
        self.NewButton.setObjectName(u'NewButton')
        self.ManageButtonLayout.addWidget(self.NewButton)
        self.SaveButton = QtGui.QPushButton(AlertForm)
        self.SaveButton.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(u':/general/general_save.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveButton.setIcon(icon2)
        self.SaveButton.setObjectName(u'SaveButton')
        self.ManageButtonLayout.addWidget(self.SaveButton)
        self.DeleteButton = QtGui.QPushButton(AlertForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(u':/general/general_delete.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon3)
        self.DeleteButton.setObjectName(u'DeleteButton')
        self.ManageButtonLayout.addWidget(self.DeleteButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.ManageButtonLayout.addItem(spacerItem)
        self.ManagementLayout.addLayout(self.ManageButtonLayout)
        self.AlertFormLayout.addLayout(self.ManagementLayout)
        self.AlertButtonLayout = QtGui.QHBoxLayout()
        self.AlertButtonLayout.setSpacing(8)
        self.AlertButtonLayout.setObjectName(u'AlertButtonLayout')
        spacerItem1 = QtGui.QSpacerItem(181, 0, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
        self.AlertButtonLayout.addItem(spacerItem1)
        self.DisplayButton = QtGui.QPushButton(AlertForm)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(u':/general/general_live.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DisplayButton.setIcon(icon4)
        self.DisplayButton.setObjectName(u'DisplayButton')
        self.AlertButtonLayout.addWidget(self.DisplayButton)
        self.DisplayCloseButton = QtGui.QPushButton(AlertForm)
        self.DisplayCloseButton.setIcon(icon4)
        self.DisplayCloseButton.setObjectName(u'DisplayCloseButton')
        self.AlertButtonLayout.addWidget(self.DisplayCloseButton)
        self.CloseButton = QtGui.QPushButton(AlertForm)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(u':/system/system_close.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon5)
        self.CloseButton.setObjectName(u'CloseButton')
        self.AlertButtonLayout.addWidget(self.CloseButton)
        self.AlertFormLayout.addLayout(self.AlertButtonLayout)
        self.AlertEntryLabel.setBuddy(self.AlertTextEdit)
        self.AlertParameter.setBuddy(self.ParameterEdit)

        self.retranslateUi(AlertForm)
        QtCore.QObject.connect(self.CloseButton, QtCore.SIGNAL(u'clicked()'), AlertForm.close)
        QtCore.QMetaObject.connectSlotsByName(AlertForm)
        AlertForm.setTabOrder(self.AlertTextEdit, self.ParameterEdit)
        AlertForm.setTabOrder(self.ParameterEdit, self.AlertListWidget)
        AlertForm.setTabOrder(self.AlertListWidget, self.NewButton)
        AlertForm.setTabOrder(self.NewButton, self.SaveButton)
        AlertForm.setTabOrder(self.SaveButton, self.DeleteButton)
        AlertForm.setTabOrder(self.DeleteButton, self.DisplayButton)
        AlertForm.setTabOrder(self.DisplayButton, self.DisplayCloseButton)
        AlertForm.setTabOrder(self.DisplayCloseButton, self.CloseButton)

    def retranslateUi(self, AlertForm):
        AlertForm.setWindowTitle(translate('AlertForm', 'Alert Message'))
        self.AlertEntryLabel.setText(translate('AlertForm', 'Alert &text:'))
        self.AlertParameter.setText(translate('AlertForm', '&Parameter(s):'))
        self.NewButton.setText(translate('AlertForm', '&New'))
        self.SaveButton.setText(translate('AlertForm', '&Save'))
        self.DeleteButton.setText(translate('AlertForm', '&Delete'))
        self.DisplayButton.setText(translate('AlertForm', 'Displ&ay'))
        self.DisplayCloseButton.setText(translate('AlertForm', 'Display && Cl&ose'))
        self.CloseButton.setText(translate('AlertForm', '&Close'))

