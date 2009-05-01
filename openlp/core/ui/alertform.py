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
import logging
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog

from openlp.core import translate
from openlp.core.resources import *

class AlertForm(QDialog):
    global log
    log=logging.getLogger(u'AlertForm')

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        log.info(u'Defined')

    def setupUi(self, AlertForm):
        AlertForm.setObjectName("AlertForm")
        AlertForm.resize(370, 110)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp-logo-16x16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AlertForm.setWindowIcon(icon)
        self.AlertFormLayout = QtGui.QVBoxLayout(AlertForm)
        self.AlertFormLayout.setSpacing(8)
        self.AlertFormLayout.setMargin(8)
        self.AlertFormLayout.setObjectName("AlertFormLayout")
        self.AlertEntryWidget = QtGui.QWidget(AlertForm)
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
        self.AlertEntryEditItem.setGeometry(QtCore.QRect(0, 20, 353, 26))
        self.AlertEntryEditItem.setObjectName("AlertEntryEditItem")
        self.AlertFormLayout.addWidget(self.AlertEntryWidget)
        self.ButtonBoxWidget = QtGui.QWidget(AlertForm)
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

        self.retranslateUi(AlertForm)

        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL("clicked()"), AlertForm.close)
        QtCore.QObject.connect(self.DisplayButton, QtCore.SIGNAL("clicked()"), self.onDisplayClicked)
        QtCore.QMetaObject.connectSlotsByName(AlertForm)

    def retranslateUi(self, AlertForm):
        AlertForm.setWindowTitle(translate("AlertForm", u'Alert Message'))
        self.AlertEntryLabel.setText(translate("AlertForm", u'Alert Text:'))
        self.DisplayButton.setText(translate("AlertForm", u'Display'))
        self.CancelButton.setText(translate("AlertForm", u'Cancel'))


    def load_settings(self):
        pass

    def save_settings(self):
        pass

    def onDisplayClicked(self):
        pass
