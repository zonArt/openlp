# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editversedialog.ui'
#
# Created: Sun Nov 22 13:33:41 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_EditVerseDialog(object):
    def setupUi(self, EditVerseDialog):
        EditVerseDialog.setObjectName("EditVerseDialog")
        EditVerseDialog.resize(492, 494)
        EditVerseDialog.setModal(True)
        self.widget = QtGui.QWidget(EditVerseDialog)
        self.widget.setGeometry(QtCore.QRect(8, 11, 471, 461))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.VerseListComboBox = QtGui.QComboBox(self.widget)
        self.VerseListComboBox.setObjectName("VerseListComboBox")
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.setItemText(0, "")
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.VerseListComboBox.addItem(QtCore.QString())
        self.horizontalLayout.addWidget(self.VerseListComboBox)
        self.SubVerseListComboBox = QtGui.QComboBox(self.widget)
        self.SubVerseListComboBox.setObjectName("SubVerseListComboBox")
        self.SubVerseListComboBox.addItem(QtCore.QString())
        self.SubVerseListComboBox.setItemText(0, "")
        self.SubVerseListComboBox.addItem(QtCore.QString())
        self.SubVerseListComboBox.addItem(QtCore.QString())
        self.SubVerseListComboBox.addItem(QtCore.QString())
        self.SubVerseListComboBox.addItem(QtCore.QString())
        self.SubVerseListComboBox.addItem(QtCore.QString())
        self.horizontalLayout.addWidget(self.SubVerseListComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.VerseTextEdit = QtGui.QTextEdit(self.widget)
        self.VerseTextEdit.setAcceptRichText(False)
        self.VerseTextEdit.setObjectName("VerseTextEdit")
        self.verticalLayout.addWidget(self.VerseTextEdit)
        self.ButtonBox = QtGui.QDialogButtonBox(self.widget)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.ButtonBox.setObjectName("ButtonBox")
        self.verticalLayout.addWidget(self.ButtonBox)

        self.retranslateUi(EditVerseDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("accepted()"), EditVerseDialog.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("rejected()"), EditVerseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditVerseDialog)

    def retranslateUi(self, EditVerseDialog):
        EditVerseDialog.setWindowTitle(QtGui.QApplication.translate("EditVerseDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(1, QtGui.QApplication.translate("EditVerseDialog", "Chorus", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(2, QtGui.QApplication.translate("EditVerseDialog", "Bridge", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(3, QtGui.QApplication.translate("EditVerseDialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(4, QtGui.QApplication.translate("EditVerseDialog", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(5, QtGui.QApplication.translate("EditVerseDialog", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(6, QtGui.QApplication.translate("EditVerseDialog", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(7, QtGui.QApplication.translate("EditVerseDialog", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(8, QtGui.QApplication.translate("EditVerseDialog", "6", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(9, QtGui.QApplication.translate("EditVerseDialog", "7", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(11, QtGui.QApplication.translate("EditVerseDialog", "9", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(10, QtGui.QApplication.translate("EditVerseDialog", "8", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(1, QtGui.QApplication.translate("EditVerseDialog", "a", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(2, QtGui.QApplication.translate("EditVerseDialog", "b", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(3, QtGui.QApplication.translate("EditVerseDialog", "c", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(4, QtGui.QApplication.translate("EditVerseDialog", "d", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(5, QtGui.QApplication.translate("EditVerseDialog", "e", None, QtGui.QApplication.UnicodeUTF8))

