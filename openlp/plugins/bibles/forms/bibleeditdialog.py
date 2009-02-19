# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bibleeditdialog.ui'
#
# Created: Wed Feb 18 06:02:58 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(dialog)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.EditGroupBox = QtGui.QGroupBox(dialog)
        self.EditGroupBox.setObjectName("EditGroupBox")
        self.gridLayout = QtGui.QGridLayout(self.EditGroupBox)
        self.gridLayout.setMargin(8)
        self.gridLayout.setSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.VerseTextEdit = QtGui.QPlainTextEdit(self.EditGroupBox)
        self.VerseTextEdit.setObjectName("VerseTextEdit")
        self.gridLayout.addWidget(self.VerseTextEdit, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.EditGroupBox)
        self.ButtonLoayout = QtGui.QHBoxLayout()
        self.ButtonLoayout.setSpacing(8)
        self.ButtonLoayout.setMargin(8)
        self.ButtonLoayout.setObjectName("ButtonLoayout")
        self.SaveButton = QtGui.QPushButton(dialog)
        self.SaveButton.setObjectName("SaveButton")
        self.ButtonLoayout.addWidget(self.SaveButton)
        self.CancelButton = QtGui.QPushButton(dialog)
        self.CancelButton.setObjectName("CancelButton")
        self.ButtonLoayout.addWidget(self.CancelButton)
        self.verticalLayout.addLayout(self.ButtonLoayout)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        dialog.setTabOrder(self.VerseTextEdit, self.SaveButton)
        dialog.setTabOrder(self.SaveButton, self.CancelButton)

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QtGui.QApplication.translate("dialog", "Bible Edit Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.EditGroupBox.setTitle(QtGui.QApplication.translate("dialog", "Edit Verse Text", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveButton.setText(QtGui.QApplication.translate("dialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate("dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
