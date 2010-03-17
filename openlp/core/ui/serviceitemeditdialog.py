# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serviceitemeditdialog.ui'
#
# Created: Wed Mar 17 20:55:46 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ServiceItemEditDialog(object):
    def setupUi(self, ServiceItemEditDialog):
        ServiceItemEditDialog.setObjectName("ServiceItemEditDialog")
        ServiceItemEditDialog.resize(400, 287)
        self.widget = QtGui.QWidget(ServiceItemEditDialog)
        self.widget.setGeometry(QtCore.QRect(20, 20, 351, 241))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtGui.QListWidget(self.widget)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.upButton = QtGui.QPushButton(self.widget)
        self.upButton.setObjectName("upButton")
        self.verticalLayout.addWidget(self.upButton)
        self.downButton = QtGui.QPushButton(self.widget)
        self.downButton.setObjectName("downButton")
        self.verticalLayout.addWidget(self.downButton)
        self.deleteButton = QtGui.QPushButton(self.widget)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout.addWidget(self.deleteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ServiceItemEditDialog)
        QtCore.QMetaObject.connectSlotsByName(ServiceItemEditDialog)

    def retranslateUi(self, ServiceItemEditDialog):
        ServiceItemEditDialog.setWindowTitle(QtGui.QApplication.translate("ServiceItemEditDialog", "Service Item Maintenance", None, QtGui.QApplication.UnicodeUTF8))
        self.upButton.setText(QtGui.QApplication.translate("ServiceItemEditDialog", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.downButton.setText(QtGui.QApplication.translate("ServiceItemEditDialog", "Down", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("ServiceItemEditDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))

