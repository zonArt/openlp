# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Project Folders\Personal Projects\openlp-2\trunk\openlp\resources\forms\alertform.ui'
#
# Created: Wed Nov 05 20:54:20 2008
#      by: PyQt4 UI code generator 4.4.4-snapshot-20080918
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

from openlp.resources import *

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
