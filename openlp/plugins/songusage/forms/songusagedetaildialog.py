# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'songusagedetaildialog.ui'
#
# Created: Tue Feb  9 07:34:05 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AuditDetailDialog(object):
    def setupUi(self, AuditDetailDialog):
        AuditDetailDialog.setObjectName("AuditDetailDialog")
        AuditDetailDialog.resize(609, 413)
        self.verticalLayout = QtGui.QVBoxLayout(AuditDetailDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DateRangeGroupBox = QtGui.QGroupBox(AuditDetailDialog)
        self.DateRangeGroupBox.setObjectName("DateRangeGroupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.DateRangeGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.DateHorizontalLayout = QtGui.QHBoxLayout()
        self.DateHorizontalLayout.setObjectName("DateHorizontalLayout")
        self.FromDate = QtGui.QCalendarWidget(self.DateRangeGroupBox)
        self.FromDate.setObjectName("FromDate")
        self.DateHorizontalLayout.addWidget(self.FromDate)
        self.ToLabel = QtGui.QLabel(self.DateRangeGroupBox)
        self.ToLabel.setScaledContents(False)
        self.ToLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ToLabel.setObjectName("ToLabel")
        self.DateHorizontalLayout.addWidget(self.ToLabel)
        self.ToDate = QtGui.QCalendarWidget(self.DateRangeGroupBox)
        self.ToDate.setObjectName("ToDate")
        self.DateHorizontalLayout.addWidget(self.ToDate)
        self.verticalLayout_2.addLayout(self.DateHorizontalLayout)
        self.FileGroupBox = QtGui.QGroupBox(self.DateRangeGroupBox)
        self.FileGroupBox.setObjectName("FileGroupBox")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.FileGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.FileLineEdit = QtGui.QLineEdit(self.FileGroupBox)
        self.FileLineEdit.setObjectName("FileLineEdit")
        self.horizontalLayout.addWidget(self.FileLineEdit)
        self.SaveFilePushButton = QtGui.QPushButton(self.FileGroupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/exports/export_load.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveFilePushButton.setIcon(icon)
        self.SaveFilePushButton.setObjectName("SaveFilePushButton")
        self.horizontalLayout.addWidget(self.SaveFilePushButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.FileGroupBox)
        self.verticalLayout.addWidget(self.DateRangeGroupBox)
        self.buttonBox = QtGui.QDialogButtonBox(AuditDetailDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AuditDetailDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AuditDetailDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AuditDetailDialog.close)
        QtCore.QObject.connect(self.SaveFilePushButton, QtCore.SIGNAL("pressed()"), AuditDetailDialog.defineOutputLocation)
        QtCore.QMetaObject.connectSlotsByName(AuditDetailDialog)

    def retranslateUi(self, AuditDetailDialog):
        AuditDetailDialog.setWindowTitle(QtGui.QApplication.translate("AuditDetailDialog", "Audit Detail Extraction", None, QtGui.QApplication.UnicodeUTF8))
        self.DateRangeGroupBox.setTitle(QtGui.QApplication.translate("AuditDetailDialog", "Select Date Range", None, QtGui.QApplication.UnicodeUTF8))
        self.ToLabel.setText(QtGui.QApplication.translate("AuditDetailDialog", "to", None, QtGui.QApplication.UnicodeUTF8))
        self.FileGroupBox.setTitle(QtGui.QApplication.translate("AuditDetailDialog", "Report Location", None, QtGui.QApplication.UnicodeUTF8))

import openlp-2_rc
