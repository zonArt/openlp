# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'songbookdialog.ui'
#
# Created: Sun Jan  4 08:43:12 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SongBookDialog(object):
    def setupUi(self, SongBookDialog):
        SongBookDialog.setObjectName("SongBookDialog")
        SongBookDialog.resize(387, 500)
        self.gridLayout_2 = QtGui.QGridLayout(SongBookDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.BookSongListView = QtGui.QTableWidget(SongBookDialog)
        self.BookSongListView.setObjectName("BookSongListView")
        self.BookSongListView.setColumnCount(0)
        self.BookSongListView.setRowCount(0)
        self.gridLayout_2.addWidget(self.BookSongListView, 0, 0, 1, 2)
        self.SongBookGroup = QtGui.QGroupBox(SongBookDialog)
        self.SongBookGroup.setObjectName("SongBookGroup")
        self.gridLayout = QtGui.QGridLayout(self.SongBookGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.NameLabel = QtGui.QLabel(self.SongBookGroup)
        self.NameLabel.setObjectName("NameLabel")
        self.gridLayout.addWidget(self.NameLabel, 0, 0, 1, 1)
        self.NameEdit = QtGui.QLineEdit(self.SongBookGroup)
        self.NameEdit.setObjectName("NameEdit")
        self.gridLayout.addWidget(self.NameEdit, 0, 1, 1, 4)
        self.PublisherLabel = QtGui.QLabel(self.SongBookGroup)
        self.PublisherLabel.setObjectName("PublisherLabel")
        self.gridLayout.addWidget(self.PublisherLabel, 1, 0, 1, 1)
        self.PublisherEdit = QtGui.QLineEdit(self.SongBookGroup)
        self.PublisherEdit.setObjectName("PublisherEdit")
        self.gridLayout.addWidget(self.PublisherEdit, 1, 1, 1, 4)
        spacerItem = QtGui.QSpacerItem(198, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 2)
        self.DeleteButton = QtGui.QPushButton(self.SongBookGroup)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/services/service_delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon)
        self.DeleteButton.setObjectName("DeleteButton")
        self.gridLayout.addWidget(self.DeleteButton, 2, 3, 1, 1)
        self.AddUpdateButton = QtGui.QPushButton(self.SongBookGroup)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/system/system_settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddUpdateButton.setIcon(icon1)
        self.AddUpdateButton.setObjectName("AddUpdateButton")
        self.gridLayout.addWidget(self.AddUpdateButton, 2, 4, 1, 1)
        self.ClearButton = QtGui.QPushButton(self.SongBookGroup)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/songs/song_edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClearButton.setIcon(icon2)
        self.ClearButton.setObjectName("ClearButton")
        self.gridLayout.addWidget(self.ClearButton, 2, 2, 1, 1)
        self.gridLayout_2.addWidget(self.SongBookGroup, 1, 0, 1, 2)
        self.MessageLabel = QtGui.QLabel(SongBookDialog)
        self.MessageLabel.setObjectName("MessageLabel")
        self.gridLayout_2.addWidget(self.MessageLabel, 2, 0, 1, 1)
        self.ButtonBox = QtGui.QDialogButtonBox(SongBookDialog)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.ButtonBox.setObjectName("ButtonBox")
        self.gridLayout_2.addWidget(self.ButtonBox, 2, 1, 1, 1)

        self.retranslateUi(SongBookDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("accepted()"), SongBookDialog.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("rejected()"), SongBookDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SongBookDialog)

    def retranslateUi(self, SongBookDialog):
        SongBookDialog.setWindowTitle(QtGui.QApplication.translate("SongBookDialog", "Book Song Maintenance", None, QtGui.QApplication.UnicodeUTF8))
        self.SongBookGroup.setTitle(QtGui.QApplication.translate("SongBookDialog", "Song Book", None, QtGui.QApplication.UnicodeUTF8))
        self.NameLabel.setText(QtGui.QApplication.translate("SongBookDialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.PublisherLabel.setText(QtGui.QApplication.translate("SongBookDialog", "Publisher:", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setToolTip(QtGui.QApplication.translate("SongBookDialog", "Delete Author", None, QtGui.QApplication.UnicodeUTF8))
        self.AddUpdateButton.setToolTip(QtGui.QApplication.translate("SongBookDialog", "Add Update Author", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearButton.setToolTip(QtGui.QApplication.translate("SongBookDialog", "Clear Selection", None, QtGui.QApplication.UnicodeUTF8))
