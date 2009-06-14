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

class Ui_TopicsDialog(object):
    def setupUi(self, TopicsDialog):
        TopicsDialog.setObjectName(u'TopicsDialog')
        TopicsDialog.resize(387, 463)
        self.gridLayout_2 = QtGui.QGridLayout(TopicsDialog)
        self.gridLayout_2.setObjectName(u'gridLayout_2')
        self.TopicGroupBox = QtGui.QGroupBox(TopicsDialog)
        self.TopicGroupBox.setObjectName(u'TopicGroupBox')
        self.gridLayout = QtGui.QGridLayout(self.TopicGroupBox)
        self.gridLayout.setObjectName(u'gridLayout')
        self.TopicNameLabel = QtGui.QLabel(self.TopicGroupBox)
        self.TopicNameLabel.setObjectName(u'TopicNameLabel')
        self.gridLayout.addWidget(self.TopicNameLabel, 0, 0, 1, 1)
        self.TopicNameEdit = QtGui.QLineEdit(self.TopicGroupBox)
        self.TopicNameEdit.setObjectName(u'TopicNameEdit')
        self.gridLayout.addWidget(self.TopicNameEdit, 0, 1, 1, 4)
        spacerItem = QtGui.QSpacerItem(198, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.DeleteButton = QtGui.QPushButton(self.TopicGroupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/services/service_delete.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon)
        self.DeleteButton.setObjectName(u'DeleteButton')
        self.gridLayout.addWidget(self.DeleteButton, 1, 3, 1, 1)
        self.AddUpdateButton = QtGui.QPushButton(self.TopicGroupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(u':/services/service_save.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddUpdateButton.setIcon(icon1)
        self.AddUpdateButton.setObjectName(u'AddUpdateButton')
        self.gridLayout.addWidget(self.AddUpdateButton, 1, 4, 1, 1)
        self.ClearButton = QtGui.QPushButton(self.TopicGroupBox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(u':/services/service_new.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClearButton.setIcon(icon2)
        self.ClearButton.setObjectName(u'ClearButton')
        self.gridLayout.addWidget(self.ClearButton, 1, 2, 1, 1)
        self.gridLayout_2.addWidget(self.TopicGroupBox, 1, 0, 1, 1)
        self.MessageLabel = QtGui.QLabel(TopicsDialog)
        self.MessageLabel.setObjectName(u'MessageLabel')
        self.gridLayout_2.addWidget(self.MessageLabel, 3, 0, 1, 1)
        self.TopicsListWidget = QtGui.QListWidget()
        self.TopicsListWidget.setAlternatingRowColors(True)
        self.gridLayout_2.addWidget(self.TopicsListWidget, 0, 0, 1, 1)
        self.ButtonBox = QtGui.QDialogButtonBox(TopicsDialog)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.ButtonBox.setObjectName(u'ButtonBox')
        self.gridLayout_2.addWidget(self.ButtonBox, 2, 0, 1, 1)

        self.retranslateUi(TopicsDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'accepted()'), TopicsDialog.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL(u'rejected()'), TopicsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TopicsDialog)

    def retranslateUi(self, TopicsDialog):
        TopicsDialog.setWindowTitle(translate(u'TopicsDialog', u'Topic Maintenance'))
        self.TopicGroupBox.setTitle(translate(u'TopicsDialog', u'Topic'))
        self.TopicNameLabel.setText(translate(u'TopicsDialog', u'Topic Name:'))

        self.DeleteButton.setToolTip(translate(u'TopicsDialog', u'Delete Author'))
        self.DeleteButton.setText(translate(u'AuthorsDialog', u'Delete'))
        self.AddUpdateButton.setToolTip(translate(u'TopicsDialog', u'Add Update Author'))
        self.AddUpdateButton.setText(translate(u'AuthorsDialog', u'Save'))
        self.ClearButton.setToolTip(translate(u'TopicsDialog', u'Clear Selection'))
        self.ClearButton.setText(translate(u'TopicsDialog', u'Clear'))

