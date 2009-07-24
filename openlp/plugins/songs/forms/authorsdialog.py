# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
from PyQt4 import QtCore, QtGui
from openlp.core.lib import translate

class Ui_AuthorsDialog(object):
    def setupUi(self, AuthorsDialog):
        AuthorsDialog.setObjectName("AuthorsDialog")
        AuthorsDialog.resize(393, 147)
        self.AuthorsLayout = QtGui.QFormLayout(AuthorsDialog)
        self.AuthorsLayout.setMargin(8)
        self.AuthorsLayout.setSpacing(8)
        self.AuthorsLayout.setObjectName("AuthorsLayout")
        self.FirstNameLabel = QtGui.QLabel(AuthorsDialog)
        self.FirstNameLabel.setObjectName("FirstNameLabel")
        self.AuthorsLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.FirstNameLabel)
        self.FirstNameEdit = QtGui.QLineEdit(AuthorsDialog)
        self.FirstNameEdit.setObjectName("FirstNameEdit")
        self.AuthorsLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.FirstNameEdit)
        self.LastNameLabel = QtGui.QLabel(AuthorsDialog)
        self.LastNameLabel.setObjectName("LastNameLabel")
        self.AuthorsLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.LastNameLabel)
        self.LastNameEdit = QtGui.QLineEdit(AuthorsDialog)
        self.LastNameEdit.setObjectName("LastNameEdit")
        self.AuthorsLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.LastNameEdit)
        self.DisplayLabel = QtGui.QLabel(AuthorsDialog)
        self.DisplayLabel.setObjectName("DisplayLabel")
        self.AuthorsLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.DisplayLabel)
        self.DisplayEdit = QtGui.QLineEdit(AuthorsDialog)
        self.DisplayEdit.setObjectName("DisplayEdit")
        self.AuthorsLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.DisplayEdit)
        self.AuthorButtonBox = QtGui.QDialogButtonBox(AuthorsDialog)
        self.AuthorButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.AuthorButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.AuthorButtonBox.setObjectName("AuthorButtonBox")
        self.AuthorsLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.AuthorButtonBox)

        self.retranslateUi(AuthorsDialog)
        QtCore.QObject.connect(self.AuthorButtonBox, QtCore.SIGNAL("accepted()"), AuthorsDialog.accept)
        QtCore.QObject.connect(self.AuthorButtonBox, QtCore.SIGNAL("rejected()"), AuthorsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AuthorsDialog)

    def retranslateUi(self, AuthorsDialog):
        AuthorsDialog.setWindowTitle(QtGui.QApplication.translate("AuthorsDialog", "Author Maintenance", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "Display Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.FirstNameLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "First Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.AuthorButtonBox.setToolTip(QtGui.QApplication.translate("AuthorsDialog", "Exit Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.LastNameLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "Last Name:", None, QtGui.QApplication.UnicodeUTF8))
