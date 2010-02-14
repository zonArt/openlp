# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alertform.ui'
#
# Created: Sat Feb 13 08:19:51 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AlertDialog(object):
    def setupUi(self, AlertForm):
        AlertForm.setObjectName("AlertDialog")
        AlertForm.resize(430, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.AlertEntryWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.AlertEntryLabel = QtGui.QLabel(self.AlertEntryWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlertEntryLabel.sizePolicy().hasHeightForWidth())
        self.AlertEntryLabel.setSizePolicy(sizePolicy)
        self.AlertEntryLabel.setObjectName("AlertEntryLabel")
        self.verticalLayout.addWidget(self.AlertEntryLabel)
        self.AlertEntryEditItem = QtGui.QLineEdit(self.AlertEntryWidget)
        self.AlertEntryEditItem.setObjectName("AlertEntryEditItem")
        self.verticalLayout.addWidget(self.AlertEntryEditItem)
        self.AlertListWidget = QtGui.QListWidget(self.AlertEntryWidget)
        self.AlertListWidget.setAlternatingRowColors(True)
        self.AlertListWidget.setObjectName("AlertListWidget")
        self.verticalLayout.addWidget(self.AlertListWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(181, 38, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.DisplayButton = QtGui.QPushButton(self.AlertEntryWidget)
        self.DisplayButton.setObjectName("DisplayButton")
        self.horizontalLayout.addWidget(self.DisplayButton)
        self.CancelButton = QtGui.QPushButton(self.AlertEntryWidget)
        self.CancelButton.setObjectName("CancelButton")
        self.horizontalLayout.addWidget(self.CancelButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.AlertFormLayout.addWidget(self.AlertEntryWidget)

        self.retranslateUi(AlertForm)
        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL("clicked()"), self.close)
        QtCore.QMetaObject.connectSlotsByName(AlertForm)

    def retranslateUi(self, AlertForm):
        AlertForm.setWindowTitle(QtGui.QApplication.translate("AlertForm", "Alert Message", None, QtGui.QApplication.UnicodeUTF8))
        self.AlertEntryLabel.setText(QtGui.QApplication.translate("AlertForm", "Alert Text:", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayButton.setText(QtGui.QApplication.translate("AlertForm", "Display", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("AlertForm", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
