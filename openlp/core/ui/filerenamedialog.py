# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filerenamedialog.ui'
#
# Created: Sat Sep 25 16:20:30 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FileRenameDialog(object):
    def setupUi(self, FileRenameDialog):
        FileRenameDialog.setObjectName("FileRenameDialog")
        FileRenameDialog.resize(400, 87)
        self.buttonBox = QtGui.QDialogButtonBox(FileRenameDialog)
        self.buttonBox.setGeometry(QtCore.QRect(210, 50, 171, 25))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtGui.QWidget(FileRenameDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 381, 35))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.FileRenameLabel = QtGui.QLabel(self.widget)
        self.FileRenameLabel.setObjectName("FileRenameLabel")
        self.horizontalLayout.addWidget(self.FileRenameLabel)
        self.FileNameEdit = QtGui.QLineEdit(self.widget)
        self.FileNameEdit.setObjectName("FileNameEdit")
        self.horizontalLayout.addWidget(self.FileNameEdit)

        self.retranslateUi(FileRenameDialog)
        QtCore.QMetaObject.connectSlotsByName(FileRenameDialog)

    def retranslateUi(self, FileRenameDialog):
        FileRenameDialog.setWindowTitle(QtGui.QApplication.translate("FileRenameDialog", "File Rename", None, QtGui.QApplication.UnicodeUTF8))
        self.FileRenameLabel.setText(QtGui.QApplication.translate("FileRenameDialog", "New File Name:", None, QtGui.QApplication.UnicodeUTF8))

