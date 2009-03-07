# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/raoul/Projects/openlp-2/resources/forms/editversedialog.ui'
#
# Created: Sat Mar  7 11:11:49 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_EditVerseDialog(object):
    def setupUi(self, EditVerseDialog):
        EditVerseDialog.setObjectName("EditVerseDialog")
        EditVerseDialog.resize(492, 373)
        EditVerseDialog.setModal(True)
        self.DialogLayout = QtGui.QVBoxLayout(EditVerseDialog)
        self.DialogLayout.setSpacing(8)
        self.DialogLayout.setMargin(8)
        self.DialogLayout.setObjectName("DialogLayout")
        self.VerseTextEdit = QtGui.QTextEdit(EditVerseDialog)
        self.VerseTextEdit.setAcceptRichText(False)
        self.VerseTextEdit.setObjectName("VerseTextEdit")
        self.DialogLayout.addWidget(self.VerseTextEdit)
        self.ButtonBox = QtGui.QDialogButtonBox(EditVerseDialog)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.ButtonBox.setObjectName("ButtonBox")
        self.DialogLayout.addWidget(self.ButtonBox)

        self.retranslateUi(EditVerseDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("accepted()"), EditVerseDialog.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("rejected()"), EditVerseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditVerseDialog)

    def retranslateUi(self, EditVerseDialog):
        EditVerseDialog.setWindowTitle(QtGui.QApplication.translate("EditVerseDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
