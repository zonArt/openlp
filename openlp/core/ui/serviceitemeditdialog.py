# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serviceitemeditdialog.ui'
#
# Created: Thu Mar 18 22:05:22 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ServiceItemEditDialog(object):
    def setupUi(self, ServiceItemEditDialog):
        ServiceItemEditDialog.setObjectName("ServiceItemEditDialog")
        ServiceItemEditDialog.resize(386, 272)
        self.layoutWidget = QtGui.QWidget(ServiceItemEditDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 351, 241))
        self.layoutWidget.setObjectName("layoutWidget")
        self.outerLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.outerLayout.setObjectName("outerLayout")
        self.topLayout = QtGui.QHBoxLayout()
        self.topLayout.setObjectName("topLayout")
        self.listWidget = QtGui.QListWidget(self.layoutWidget)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName("listWidget")
        self.topLayout.addWidget(self.listWidget)
        self.buttonLayout = QtGui.QVBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.upButton = QtGui.QPushButton(self.layoutWidget)
        self.upButton.setObjectName("upButton")
        self.buttonLayout.addWidget(self.upButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.buttonLayout.addItem(spacerItem)
        self.deleteButton = QtGui.QPushButton(self.layoutWidget)
        self.deleteButton.setObjectName("deleteButton")
        self.buttonLayout.addWidget(self.deleteButton)
        self.downButton = QtGui.QPushButton(self.layoutWidget)
        self.downButton.setObjectName("downButton")
        self.buttonLayout.addWidget(self.downButton)
        self.topLayout.addLayout(self.buttonLayout)
        self.outerLayout.addLayout(self.topLayout)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.outerLayout.addWidget(self.buttonBox)

        self.retranslateUi(ServiceItemEditDialog)
        QtCore.QMetaObject.connectSlotsByName(ServiceItemEditDialog)

    def retranslateUi(self, ServiceItemEditDialog):
        ServiceItemEditDialog.setWindowTitle(QtGui.QApplication.translate("ServiceItemEditDialog", "Service Item Maintenance", None, QtGui.QApplication.UnicodeUTF8))
        self.upButton.setText(QtGui.QApplication.translate("ServiceItemEditDialog", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("ServiceItemEditDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.downButton.setText(QtGui.QApplication.translate("ServiceItemEditDialog", "Down", None, QtGui.QApplication.UnicodeUTF8))

