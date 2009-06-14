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

class Ui_SongBookDialog(object):
    def setupUi(self, SongBookDialog):
        SongBookDialog.setObjectName(u'SongBookDialog')
        SongBookDialog.resize(387, 531)
        self.DialogLayout = QtGui.QVBoxLayout(SongBookDialog)
        self.DialogLayout.setSpacing(8)
        self.DialogLayout.setMargin(8)
        self.DialogLayout.setObjectName(u'DialogLayout')
        self.BookSongListWidget = QtGui.QListWidget()
        self.BookSongListWidget.setAlternatingRowColors(True)
        self.DialogLayout.addWidget(self.BookSongListWidget)
        self.DialogLayout.addWidget(self.BookSongListWidget)
        self.SongBookGroup = QtGui.QGroupBox(SongBookDialog)
        self.SongBookGroup.setMinimumSize(QtCore.QSize(0, 200))
        self.SongBookGroup.setObjectName(u'SongBookGroup')
        self.SongBookLayout = QtGui.QVBoxLayout(self.SongBookGroup)
        self.SongBookLayout.setSpacing(8)
        self.SongBookLayout.setMargin(8)
        self.SongBookLayout.setObjectName(u'SongBookLayout')
        self.DetailsWidget = QtGui.QWidget(self.SongBookGroup)
        self.DetailsWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.DetailsWidget.setObjectName(u'DetailsWidget')
        self.DetailsLayout = QtGui.QFormLayout(self.DetailsWidget)
        self.DetailsLayout.setMargin(0)
        self.DetailsLayout.setSpacing(8)
        self.DetailsLayout.setObjectName(u'DetailsLayout')
        self.NameLabel = QtGui.QLabel(self.DetailsWidget)
        self.NameLabel.setObjectName(u'NameLabel')
        self.DetailsLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.NameLabel)
        self.NameEdit = QtGui.QLineEdit(self.DetailsWidget)
        self.NameEdit.setObjectName(u'NameEdit')
        self.DetailsLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.NameEdit)
        self.PublisherLabel = QtGui.QLabel(self.DetailsWidget)
        self.PublisherLabel.setObjectName(u'PublisherLabel')
        self.DetailsLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.PublisherLabel)
        self.PublisherEdit = QtGui.QLineEdit(self.DetailsWidget)
        self.PublisherEdit.setObjectName(u'PublisherEdit')
        self.DetailsLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.PublisherEdit)
        self.SongBookLayout.addWidget(self.DetailsWidget)
        self.MessageLabel = QtGui.QLabel(self.SongBookGroup)
        self.MessageLabel.setObjectName(u'MessageLabel')
        self.SongBookLayout.addWidget(self.MessageLabel)
        self.ButtonWidget = QtGui.QWidget(self.SongBookGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonWidget.sizePolicy().hasHeightForWidth())
        self.ButtonWidget.setSizePolicy(sizePolicy)
        self.ButtonWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.ButtonWidget.setObjectName(u'ButtonWidget')
        self.ButtonLayout = QtGui.QHBoxLayout(self.ButtonWidget)
        self.ButtonLayout.setSpacing(8)
        self.ButtonLayout.setMargin(0)
        self.ButtonLayout.setObjectName(u'ButtonLayout')
        spacerItem = QtGui.QSpacerItem(61, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
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
        self.SongBookLayout.addWidget(self.ButtonWidget)
        self.DialogLayout.addWidget(self.SongBookGroup)
        self.ButtonBox = QtGui.QDialogButtonBox(SongBookDialog)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.ButtonBox.setObjectName(u'ButtonBox')
        self.DialogLayout.addWidget(self.ButtonBox)
        self.retranslateUi(SongBookDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'accepted()'), SongBookDialog.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'rejected()'), SongBookDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SongBookDialog)

    def retranslateUi(self, SongBookDialog):
        SongBookDialog.setWindowTitle(translate(u'SongBookDialog', u'Book Song Maintenance'))
        self.SongBookGroup.setTitle(translate(u'SongBookDialog', u'Song Book'))
        self.NameLabel.setText(translate(u'SongBookDialog', u'Name:'))
        self.PublisherLabel.setText(translate(u'SongBookDialog', u'Publisher:'))
        self.ClearButton.setToolTip(translate(u'SongBookDialog', u'Clear Selection'))
        self.ClearButton.setText(translate(u'SongBookDialog', u'Clear'))
        self.AddUpdateButton.setToolTip(translate(u'SongBookDialog', u'Add Update Author'))
        self.AddUpdateButton.setText(translate(u'SongBookDialog', u'Save'))
        self.DeleteButton.setToolTip(translate(u'SongBookDialog', u'Delete Author'))
        self.DeleteButton.setText(translate(u'SongBookDialog', u'Delete'))
