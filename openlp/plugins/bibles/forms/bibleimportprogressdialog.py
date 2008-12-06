# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bibleimportprogress.ui'
#
# Created: Sun Nov 30 16:19:26 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_BibleImportProgressDialog(object):
    def setupUi(self, BibleImportProgressDialog):
        BibleImportProgressDialog.setObjectName("BibleImportProgressDialog")
        BibleImportProgressDialog.resize(505, 150)
        self.buttonBox = QtGui.QDialogButtonBox(BibleImportProgressDialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 110, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.ProgressGroupBox = QtGui.QGroupBox(BibleImportProgressDialog)
        self.ProgressGroupBox.setGeometry(QtCore.QRect(10, 10, 481, 64))
        self.ProgressGroupBox.setObjectName("ProgressGroupBox")
        self.progressBar = QtGui.QProgressBar(self.ProgressGroupBox)
        self.progressBar.setGeometry(QtCore.QRect(10, 27, 451, 28))
        self.progressBar.setProperty("value", QtCore.QVariant(24))
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(BibleImportProgressDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), BibleImportProgressDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), BibleImportProgressDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BibleImportProgressDialog)

    def retranslateUi(self, BibleImportProgressDialog):
        BibleImportProgressDialog.setWindowTitle(QtGui.QApplication.translate("BibleImportProgressDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.ProgressGroupBox.setTitle(QtGui.QApplication.translate("BibleImportProgressDialog", "Progress", None, QtGui.QApplication.UnicodeUTF8))

