# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alerteditdialog.ui'
#
# Created: Sat Feb 13 08:20:09 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AlertList(object):
    def setupUi(self, AlertList):
        AlertList.setObjectName("AlertList")
        AlertList.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(AlertList)
        self.buttonBox.setGeometry(QtCore.QRect(220, 270, 173, 27))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtGui.QWidget(AlertList)
        self.widget.setGeometry(QtCore.QRect(20, 10, 361, 251))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.SaveButton = QtGui.QPushButton(self.widget)
        self.SaveButton.setObjectName("SaveButton")
        self.horizontalLayout_2.addWidget(self.SaveButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QtGui.QListWidget(self.widget)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout.addWidget(self.listWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.AddButton = QtGui.QPushButton(self.widget)
        self.AddButton.setObjectName("AddButton")
        self.verticalLayout.addWidget(self.AddButton)
        self.EdirButton = QtGui.QPushButton(self.widget)
        self.EdirButton.setObjectName("EdirButton")
        self.verticalLayout.addWidget(self.EdirButton)
        self.DeleteButton = QtGui.QPushButton(self.widget)
        self.DeleteButton.setObjectName("DeleteButton")
        self.verticalLayout.addWidget(self.DeleteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(AlertList)
        QtCore.QMetaObject.connectSlotsByName(AlertList)

    def retranslateUi(self, AlertList):
        AlertList.setWindowTitle(QtGui.QApplication.translate("AlertList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveButton.setText(QtGui.QApplication.translate("AlertList", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.AddButton.setText(QtGui.QApplication.translate("AlertList", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.EdirButton.setText(QtGui.QApplication.translate("AlertList", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setText(QtGui.QApplication.translate("AlertList", "Delete", None, QtGui.QApplication.UnicodeUTF8))

