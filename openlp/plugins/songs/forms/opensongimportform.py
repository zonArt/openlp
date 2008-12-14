# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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

from openlp.core.resources import *

class OpenSongImportForm(object):

    def __init__(self):
        self.OpenSongImportForm = QtGui.QWidget()
        self.setupUi()

    def setupUi(self):
        self.OpenSongImportForm.setObjectName("OpenSongImportForm")
        self.OpenSongImportForm.resize(481, 153)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.OpenSongImportForm.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(self.OpenSongImportForm)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ImportFileWidget = QtGui.QWidget(self.OpenSongImportForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImportFileWidget.sizePolicy().hasHeightForWidth())
        self.ImportFileWidget.setSizePolicy(sizePolicy)
        self.ImportFileWidget.setObjectName("ImportFileWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.ImportFileWidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ImportFileLabel = QtGui.QLabel(self.ImportFileWidget)
        self.ImportFileLabel.setObjectName("ImportFileLabel")
        self.horizontalLayout.addWidget(self.ImportFileLabel)
        self.ImportFileLineEdit = QtGui.QLineEdit(self.ImportFileWidget)
        self.ImportFileLineEdit.setObjectName("ImportFileLineEdit")
        self.horizontalLayout.addWidget(self.ImportFileLineEdit)
        self.ImportFileSelectPushButton = QtGui.QPushButton(self.ImportFileWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/imports/import_load.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ImportFileSelectPushButton.setIcon(icon1)
        self.ImportFileSelectPushButton.setObjectName("ImportFileSelectPushButton")
        self.horizontalLayout.addWidget(self.ImportFileSelectPushButton)
        self.verticalLayout.addWidget(self.ImportFileWidget)
        self.ProgressGroupBox = QtGui.QGroupBox(self.OpenSongImportForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ProgressGroupBox.sizePolicy().hasHeightForWidth())
        self.ProgressGroupBox.setSizePolicy(sizePolicy)
        self.ProgressGroupBox.setObjectName("ProgressGroupBox")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.ProgressGroupBox)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setContentsMargins(6, 0, 8, 8)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ProgressLabel = QtGui.QLabel(self.ProgressGroupBox)
        self.ProgressLabel.setObjectName("ProgressLabel")
        self.verticalLayout_4.addWidget(self.ProgressLabel)
        self.ProgressBar = QtGui.QProgressBar(self.ProgressGroupBox)
        self.ProgressBar.setProperty("value", QtCore.QVariant(24))
        self.ProgressBar.setObjectName("ProgressBar")
        self.verticalLayout_4.addWidget(self.ProgressBar)
        self.verticalLayout.addWidget(self.ProgressGroupBox)
        self.ButtonBarWidget = QtGui.QWidget(self.OpenSongImportForm)
        self.ButtonBarWidget.setObjectName("ButtonBarWidget")
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.ButtonBarWidget)
        self.horizontalLayout_7.setSpacing(8)
        self.horizontalLayout_7.setMargin(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtGui.QSpacerItem(288, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.ImportPushButton = QtGui.QPushButton(self.ButtonBarWidget)
        self.ImportPushButton.setObjectName("ImportPushButton")
        self.horizontalLayout_7.addWidget(self.ImportPushButton)
        self.ClosePushButton = QtGui.QPushButton(self.ButtonBarWidget)
        self.ClosePushButton.setObjectName("ClosePushButton")
        self.horizontalLayout_7.addWidget(self.ClosePushButton)
        self.verticalLayout.addWidget(self.ButtonBarWidget)

        self.retranslateUi()
        QtCore.QObject.connect(self.ClosePushButton, QtCore.SIGNAL("clicked()"), self.OpenSongImportForm.close)
        QtCore.QMetaObject.connectSlotsByName(self.OpenSongImportForm)

    def retranslateUi(self):
        self.OpenSongImportForm.setWindowTitle(QtGui.QApplication.translate("OpenSongImportForm", "OpenSong Song Importer", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportFileLabel.setText(QtGui.QApplication.translate("OpenSongImportForm", "OpenSong Folder:", None, QtGui.QApplication.UnicodeUTF8))
        self.ProgressGroupBox.setTitle(QtGui.QApplication.translate("OpenSongImportForm", "Progress:", None, QtGui.QApplication.UnicodeUTF8))
        self.ProgressLabel.setText(QtGui.QApplication.translate("OpenSongImportForm", "Ready to import", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportPushButton.setText(QtGui.QApplication.translate("OpenSongImportForm", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.ClosePushButton.setText(QtGui.QApplication.translate("OpenSongImportForm", "Close", None, QtGui.QApplication.UnicodeUTF8))

    def show(self):
        self.OpenSongImportForm.show()
