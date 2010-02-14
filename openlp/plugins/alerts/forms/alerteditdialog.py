# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alerteditdialog.ui'
#
# Created: Sun Feb 14 16:45:10 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AlertEditDialog(object):
    def setupUi(self, AlertEditDialog):
        AlertEditDialog.setObjectName("AlertEditDialog")
        AlertEditDialog.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(AlertEditDialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 270, 173, 27))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtGui.QWidget(AlertEditDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 251))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.AlertLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.AlertLineEdit.setObjectName("AlertLineEdit")
        self.horizontalLayout_2.addWidget(self.AlertLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AlertListWidget = QtGui.QListWidget(self.layoutWidget)
        self.AlertListWidget.setAlternatingRowColors(True)
        self.AlertListWidget.setObjectName("AlertListWidget")
        self.horizontalLayout.addWidget(self.AlertListWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.SaveButton = QtGui.QPushButton(self.layoutWidget)
        self.SaveButton.setObjectName("SaveButton")
        self.verticalLayout.addWidget(self.SaveButton)
        self.ClearButton = QtGui.QPushButton(self.layoutWidget)
        self.ClearButton.setObjectName("ClearButton")
        self.verticalLayout.addWidget(self.ClearButton)
        self.AddButton = QtGui.QPushButton(self.layoutWidget)
        self.AddButton.setObjectName("AddButton")
        self.verticalLayout.addWidget(self.AddButton)
        self.EditButton = QtGui.QPushButton(self.layoutWidget)
        self.EditButton.setObjectName("EditButton")
        self.verticalLayout.addWidget(self.EditButton)
        self.DeleteButton = QtGui.QPushButton(self.layoutWidget)
        self.DeleteButton.setObjectName("DeleteButton")
        self.verticalLayout.addWidget(self.DeleteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(AlertEditDialog)
        QtCore.QMetaObject.connectSlotsByName(AlertEditDialog)

    def retranslateUi(self, AlertEditDialog):
        AlertEditDialog.setWindowTitle(QtGui.QApplication.translate("AlertEditDialog", "Maintain Alerts", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveButton.setText(QtGui.QApplication.translate("AlertEditDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearButton.setText(QtGui.QApplication.translate("AlertEditDialog", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.AddButton.setText(QtGui.QApplication.translate("AlertEditDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.EditButton.setText(QtGui.QApplication.translate("AlertEditDialog", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setText(QtGui.QApplication.translate("AlertEditDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))

