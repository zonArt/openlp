# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serviceitemdialog.ui'
#
# Created: Tue Mar  2 20:17:21 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ServiceNoteEdit(object):
    def setupUi(self, ServiceNoteEdit):
        ServiceNoteEdit.setObjectName("ServiceNoteEdit")
        ServiceNoteEdit.resize(400, 243)
        self.widget = QtGui.QWidget(ServiceNoteEdit)
        self.widget.setGeometry(QtCore.QRect(20, 10, 361, 223))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtGui.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ServiceNoteEdit)
        QtCore.QMetaObject.connectSlotsByName(ServiceNoteEdit)

    def retranslateUi(self, ServiceNoteEdit):
        ServiceNoteEdit.setWindowTitle(QtGui.QApplication.translate("ServiceNoteEdit", "Service Item Notes", None, QtGui.QApplication.UnicodeUTF8))

