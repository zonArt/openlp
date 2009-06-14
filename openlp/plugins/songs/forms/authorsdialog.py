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
        AuthorsDialog.setObjectName(u'AuthorsDialog')
        AuthorsDialog.resize(410, 505)
        self.DialogLayout = QtGui.QVBoxLayout(AuthorsDialog)
        self.DialogLayout.setSpacing(8)
        self.DialogLayout.setMargin(8)
        self.DialogLayout.setObjectName(u'DialogLayout')
        self.AuthorListWidget = QtGui.QListWidget()
        self.AuthorListWidget.setAlternatingRowColors(True)
        self.DialogLayout.addWidget(self.AuthorListWidget)
        self.AuthorDetails = QtGui.QGroupBox(AuthorsDialog)
        self.AuthorDetails.setMinimumSize(QtCore.QSize(0, 0))
        self.AuthorDetails.setObjectName(u'AuthorDetails')
        self.AuthorLayout = QtGui.QVBoxLayout(self.AuthorDetails)
        self.AuthorLayout.setSpacing(8)
        self.AuthorLayout.setMargin(8)
        self.AuthorLayout.setObjectName(u'AuthorLayout')
        self.DetailsWidget = QtGui.QWidget(self.AuthorDetails)
        self.DetailsWidget.setObjectName(u'DetailsWidget')
        self.DetailsLayout = QtGui.QFormLayout(self.DetailsWidget)
        self.DetailsLayout.setMargin(0)
        self.DetailsLayout.setSpacing(8)
        self.DetailsLayout.setObjectName(u'DetailsLayout')
        self.DisplayLabel = QtGui.QLabel(self.DetailsWidget)
        self.DisplayLabel.setObjectName(u'DisplayLabel')
        self.DetailsLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.DisplayLabel)
        self.DisplayEdit = QtGui.QLineEdit(self.DetailsWidget)
        self.DisplayEdit.setObjectName(u'DisplayEdit')
        self.DetailsLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.DisplayEdit)
        self.FirstNameLabel = QtGui.QLabel(self.DetailsWidget)
        self.FirstNameLabel.setObjectName(u'FirstNameLabel')
        self.DetailsLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.FirstNameLabel)
        self.FirstNameEdit = QtGui.QLineEdit(self.DetailsWidget)
        self.FirstNameEdit.setObjectName(u'FirstNameEdit')
        self.DetailsLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.FirstNameEdit)
        self.LastNameLabel = QtGui.QLabel(self.DetailsWidget)
        self.LastNameLabel.setObjectName(u'LastNameLabel')
        self.DetailsLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.LastNameLabel)
        self.LastNameEdit = QtGui.QLineEdit(self.DetailsWidget)
        self.LastNameEdit.setObjectName(u'LastNameEdit')
        self.DetailsLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.LastNameEdit)
        self.AuthorLayout.addWidget(self.DetailsWidget)
        self.MessageLabel = QtGui.QLabel(self.AuthorDetails)
        self.MessageLabel.setObjectName(u'MessageLabel')
        self.AuthorLayout.addWidget(self.MessageLabel)
        self.ButtonWidget = QtGui.QWidget(self.AuthorDetails)
        self.ButtonWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.ButtonWidget.setObjectName(u'ButtonWidget')
        self.ButtonLayout = QtGui.QHBoxLayout(self.ButtonWidget)
        self.ButtonLayout.setSpacing(8)
        self.ButtonLayout.setMargin(0)
        self.ButtonLayout.setObjectName(u'ButtonLayout')
        spacerItem = QtGui.QSpacerItem(198, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ButtonLayout.addItem(spacerItem)
        self.ClearButton = QtGui.QPushButton(self.ButtonWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/services/service_new.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClearButton.setIcon(icon)
        self.ClearButton.setObjectName(u'ClearButton')
        self.ButtonLayout.addWidget(self.ClearButton)
        self.AddUpdateButton = QtGui.QPushButton(self.ButtonWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(u':/services/service_save.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddUpdateButton.setIcon(icon1)
        self.AddUpdateButton.setObjectName(u'AddUpdateButton')
        self.ButtonLayout.addWidget(self.AddUpdateButton)
        self.DeleteButton = QtGui.QPushButton(self.ButtonWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(u':/services/service_delete.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon2)
        self.DeleteButton.setObjectName(u'DeleteButton')
        self.ButtonLayout.addWidget(self.DeleteButton)
        self.AuthorLayout.addWidget(self.ButtonWidget)
        self.DialogLayout.addWidget(self.AuthorDetails)
        self.buttonBox = QtGui.QDialogButtonBox(AuthorsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(u'buttonBox')
        self.DialogLayout.addWidget(self.buttonBox)

        self.retranslateUi(AuthorsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'accepted()'), AuthorsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'), AuthorsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AuthorsDialog)

    def retranslateUi(self, AuthorsDialog):
        AuthorsDialog.setWindowTitle(translate(u'AuthorsDialog', u'Author Maintenance'))
        self.AuthorDetails.setTitle(translate(u'AuthorsDialog', u'Author Details'))
        self.DisplayLabel.setText(translate(u'AuthorsDialog', u'Display Name:'))
        self.FirstNameLabel.setText(translate(u'AuthorsDialog', u'First Name:'))
        self.LastNameLabel.setText(translate(u'AuthorsDialog', u'Last Name:'))
        self.ClearButton.setToolTip(translate(u'AuthorsDialog', u'Clear Selection'))
        self.ClearButton.setText(translate(u'AuthorsDialog', u'Clear'))
        self.AddUpdateButton.setToolTip(translate(u'AuthorsDialog', u'Add Update Author'))
        self.AddUpdateButton.setText(translate(u'AuthorsDialog', u'Save'))
        self.DeleteButton.setToolTip(translate(u'AuthorsDialog', u'Delete Author'))
        self.DeleteButton.setText(translate(u'AuthorsDialog', u'Delete'))
        self.buttonBox.setToolTip(translate(u'AuthorsDialog', u'Exit Screen'))
