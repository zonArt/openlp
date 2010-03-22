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

class Ui_AlertEditDialog(object):
    def setupUi(self, AlertEditDialog):
        AlertEditDialog.setObjectName(u'AlertEditDialog')
        AlertEditDialog.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(AlertEditDialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 270, 173, 27))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(u'buttonBox')
        self.layoutWidget = QtGui.QWidget(AlertEditDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 251))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.AlertLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.AlertLineEdit.setObjectName(u'AlertLineEdit')
        self.horizontalLayout_2.addWidget(self.AlertLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.AlertListWidget = QtGui.QListWidget(self.layoutWidget)
        self.AlertListWidget.setAlternatingRowColors(True)
        self.AlertListWidget.setObjectName(u'AlertListWidget')
        self.horizontalLayout.addWidget(self.AlertListWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.SaveButton = QtGui.QPushButton(self.layoutWidget)
        self.SaveButton.setObjectName(u'SaveButton')
        self.verticalLayout.addWidget(self.SaveButton)
        self.ClearButton = QtGui.QPushButton(self.layoutWidget)
        self.ClearButton.setObjectName(u'ClearButton')
        self.verticalLayout.addWidget(self.ClearButton)
        self.AddButton = QtGui.QPushButton(self.layoutWidget)
        self.AddButton.setObjectName(u'AddButton')
        self.verticalLayout.addWidget(self.AddButton)
        self.EditButton = QtGui.QPushButton(self.layoutWidget)
        self.EditButton.setObjectName(u'EditButton')
        self.verticalLayout.addWidget(self.EditButton)
        self.DeleteButton = QtGui.QPushButton(self.layoutWidget)
        self.DeleteButton.setObjectName(u'DeleteButton')
        self.verticalLayout.addWidget(self.DeleteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(AlertEditDialog)
        QtCore.QMetaObject.connectSlotsByName(AlertEditDialog)

    def retranslateUi(self, AlertEditDialog):
        AlertEditDialog.setWindowTitle(self.trUtf8('Maintain Alerts'))
        self.SaveButton.setText(self.trUtf8('Save'))
        self.ClearButton.setText(self.trUtf8('Clear'))
        self.AddButton.setText(self.trUtf8('Add'))
        self.EditButton.setText(self.trUtf8('Edit'))
        self.DeleteButton.setText(self.trUtf8('Delete'))

