# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

from PyQt4 import QtCore, QtGui

from openlp.core.resources import *

class AlertForm(object):

    def __init__(self):
        self.AlertForm = QtGui.QWidget()
        self.setupUi()

    def setupUi(self):
        self.AlertForm.setObjectName("AlertForm")
        self.AlertForm.resize(370, 105)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AlertForm.setWindowIcon(icon)
        self.AlertFormLayout = QtGui.QVBoxLayout(self.AlertForm)
        self.AlertFormLayout.setSpacing(8)
        self.AlertFormLayout.setMargin(8)
        self.AlertFormLayout.setObjectName("AlertFormLayout")
        self.AlertEntryWidget = QtGui.QWidget(self.AlertForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryWidget.sizePolicy().hasHeightForWidth())
        self.AlertEntryWidget.setSizePolicy(sizePolicy)
        self.AlertEntryWidget.setObjectName("AlertEntryWidget")
        self.AlertEntryLabel = QtGui.QLabel(self.AlertEntryWidget)
        self.AlertEntryLabel.setGeometry(QtCore.QRect(0, 0, 353, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryLabel.sizePolicy().hasHeightForWidth())
        self.AlertEntryLabel.setSizePolicy(sizePolicy)
        self.AlertEntryLabel.setObjectName("AlertEntryLabel")
        self.AlertEntryEditItem = QtGui.QLineEdit(self.AlertEntryWidget)
        self.AlertEntryEditItem.setGeometry(QtCore.QRect(0, 20, 353, 21))
        self.AlertEntryEditItem.setObjectName("AlertEntryEditItem")
        self.AlertFormLayout.addWidget(self.AlertEntryWidget)
        self.ButtonBoxWidget = QtGui.QWidget(self.AlertForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonBoxWidget.sizePolicy().hasHeightForWidth())
        self.ButtonBoxWidget.setSizePolicy(sizePolicy)
        self.ButtonBoxWidget.setObjectName("ButtonBoxWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.ButtonBoxWidget)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(267, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.DisplayButton = QtGui.QPushButton(self.ButtonBoxWidget)
        self.DisplayButton.setObjectName("DisplayButton")
        self.horizontalLayout.addWidget(self.DisplayButton)
        self.CancelButton = QtGui.QPushButton(self.ButtonBoxWidget)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.AlertFormLayout.addWidget(self.ButtonBoxWidget)

        self.retranslateUi()
        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL("clicked()"), self.AlertForm.close)
        QtCore.QMetaObject.connectSlotsByName(self.AlertForm)

    def retranslateUi(self):
        self.AlertForm.setWindowTitle(QtGui.QApplication.translate("AlertForm", "Alert Message", None, QtGui.QApplication.UnicodeUTF8))
        self.AlertEntryLabel.setText(QtGui.QApplication.translate("AlertForm", "Alert Text:", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayButton.setText(QtGui.QApplication.translate("AlertForm", "Display", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("AlertForm", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

    def show(self):
        self.AlertForm.show()
        
    def get_settings_tab_item(self):
        pass
        
    def load_settings(self):
        pass
        
    def save_settings(self):
        pass
