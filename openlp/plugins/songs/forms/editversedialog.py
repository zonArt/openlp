# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

from PyQt4 import QtCore, QtGui

class Ui_EditVerseDialog(object):
    def setupUi(self, EditVerseDialog):
        EditVerseDialog.setObjectName("EditVerseDialog")
        EditVerseDialog.resize(492, 494)
        EditVerseDialog.setModal(True)
        self.widget = QtGui.QWidget(EditVerseDialog)
        self.widget.setGeometry(QtCore.QRect(9, 12, 471, 471))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.VerseListComboBox = QtGui.QComboBox(self.widget)
        self.VerseListComboBox.setObjectName("VerseListComboBox")
        self.VerseListComboBox.addItem("")
        self.VerseListComboBox.setItemText(0, "")
        self.VerseListComboBox.addItem("")
        self.VerseListComboBox.addItem("")
        self.VerseListComboBox.addItem("")
        self.horizontalLayout.addWidget(self.VerseListComboBox)
        self.SubVerseListComboBox = QtGui.QComboBox(self.widget)
        self.SubVerseListComboBox.setObjectName("SubVerseListComboBox")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.setItemText(0, "")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.SubVerseListComboBox.addItem("")
        self.horizontalLayout.addWidget(self.SubVerseListComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.VerseTextEdit = QtGui.QTextEdit(self.widget)
        self.VerseTextEdit.setAcceptRichText(False)
        self.VerseTextEdit.setObjectName("VerseTextEdit")
        self.verticalLayout.addWidget(self.VerseTextEdit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addVerse = QtGui.QPushButton(self.widget)
        self.addVerse.setObjectName("addVerse")
        self.horizontalLayout_2.addWidget(self.addVerse)
        self.addChorus = QtGui.QPushButton(self.widget)
        self.addChorus.setObjectName("addChorus")
        self.horizontalLayout_2.addWidget(self.addChorus)
        self.addBridge = QtGui.QPushButton(self.widget)
        self.addBridge.setObjectName("addBridge")
        self.horizontalLayout_2.addWidget(self.addBridge)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        EditVerseDialog.setWindowTitle(QtGui.QApplication.translate("EditVerseDialog", "Edit Verse", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(1, QtGui.QApplication.translate("EditVerseDialog", "Verse", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(2, QtGui.QApplication.translate("EditVerseDialog", "Chorus", None, QtGui.QApplication.UnicodeUTF8))
        self.VerseListComboBox.setItemText(3, QtGui.QApplication.translate("EditVerseDialog", "Bridge", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(1, QtGui.QApplication.translate("EditVerseDialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(2, QtGui.QApplication.translate("EditVerseDialog", "1a", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(3, QtGui.QApplication.translate("EditVerseDialog", "1b", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(4, QtGui.QApplication.translate("EditVerseDialog", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(5, QtGui.QApplication.translate("EditVerseDialog", "2a", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(6, QtGui.QApplication.translate("EditVerseDialog", "2b", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(7, QtGui.QApplication.translate("EditVerseDialog", "3", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(8, QtGui.QApplication.translate("EditVerseDialog", "4", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(9, QtGui.QApplication.translate("EditVerseDialog", "5", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(10, QtGui.QApplication.translate("EditVerseDialog", "6", None, QtGui.QApplication.UnicodeUTF8))
        self.SubVerseListComboBox.setItemText(11, QtGui.QApplication.translate("EditVerseDialog", "7", None, QtGui.QApplication.UnicodeUTF8))
        self.addVerse.setText(QtGui.QApplication.translate("EditVerseDialog", "Verse", None, QtGui.QApplication.UnicodeUTF8))
        self.addChorus.setText(QtGui.QApplication.translate("EditVerseDialog", "Chorus", None, QtGui.QApplication.UnicodeUTF8))
        self.addBridge.setText(QtGui.QApplication.translate("EditVerseDialog", "Bridge", None, QtGui.QApplication.UnicodeUTF8))
