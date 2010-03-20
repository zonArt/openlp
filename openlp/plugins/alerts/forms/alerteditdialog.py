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
        AlertEditDialog.setObjectName(u'AlertEditDialog')
        AlertEditDialog.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(AlertEditDialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 270, 173, 27))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(u'buttonBox')
        self.layoutWidget = QtGui.QWidget(AlertEditDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 251))
        self.layoutWidget.setObjectName(u'layoutWidget')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.AlertLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.AlertLineEdit.setObjectName(u'AlertLineEdit')
        self.horizontalLayout_2.addWidget(self.AlertLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.AlertListWidget = QtGui.QListWidget(self.layoutWidget)
        self.AlertListWidget.setAlternatingRowColors(True)
        self.AlertListWidget.setObjectName(u'AlertListWidget')
        self.horizontalLayout.addWidget(self.AlertListWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.SaveButton = QtGui.QPushButton(self.layoutWidget)
        self.SaveButton.setObjectName(u'SaveButton')
        self.verticalLayout.addWidget(self.SaveButton)
        self.ClearButton = QtGui.QPushButton(self.layoutWidget)
        self.ClearButton.setObjectName(u'ClearButton')
        self.verticalLayout.addWidget(self.ClearButton)
        self.AddButton = QtGui.QPushButton(self.layoutWidget)
        self.AddButton.setObjectName(u'AddButton')
        self.verticalLayout.addWidget(self.AddButton)
        self.EditButton = QtGui.QPushButton(self.layoutWidget)
        self.EditButton.setObjectName(u'EditButton')
        self.verticalLayout.addWidget(self.EditButton)
        self.DeleteButton = QtGui.QPushButton(self.layoutWidget)
        self.DeleteButton.setObjectName(u'DeleteButton')
        self.verticalLayout.addWidget(self.DeleteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(AlertEditDialog)
        QtCore.QMetaObject.connectSlotsByName(AlertEditDialog)

    def retranslateUi(self, AlertEditDialog):
        AlertEditDialog.setWindowTitle(self.trUtf8('Maintain Alerts'))
        self.SaveButton.setText(self.trUtf8('Save'))
        self.ClearButton.setText(self.trUtf8('Clear'))
        self.AddButton.setText(self.trUtf8('Add'))
        self.EditButton.setText(self.trUtf8('Edit'))
        self.DeleteButton.setText(self.trUtf8('Delete'))

