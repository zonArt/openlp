# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'authorsdialog.ui'
#
# Created: Thu Jan  1 09:41:26 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AuthorsDialog(object):
    def setupUi(self, AuthorsDialog):
        AuthorsDialog.setObjectName("AuthorsDialog")
        AuthorsDialog.resize(387, 532)
        self.buttonBox = QtGui.QDialogButtonBox(AuthorsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 490, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.AuthorDetails = QtGui.QGroupBox(AuthorsDialog)
        self.AuthorDetails.setGeometry(QtCore.QRect(20, 330, 341, 158))
        self.AuthorDetails.setObjectName("AuthorDetails")
        self.gridLayout = QtGui.QGridLayout(self.AuthorDetails)
        self.gridLayout.setObjectName("gridLayout")
        self.DisplayLabel = QtGui.QLabel(self.AuthorDetails)
        self.DisplayLabel.setObjectName("DisplayLabel")
        self.gridLayout.addWidget(self.DisplayLabel, 0, 0, 1, 1)
        self.DisplayEdit = QtGui.QLineEdit(self.AuthorDetails)
        self.DisplayEdit.setObjectName("DisplayEdit")
        self.gridLayout.addWidget(self.DisplayEdit, 0, 1, 1, 3)
        self.FirstNameLabel = QtGui.QLabel(self.AuthorDetails)
        self.FirstNameLabel.setObjectName("FirstNameLabel")
        self.gridLayout.addWidget(self.FirstNameLabel, 1, 0, 1, 1)
        self.FirstNameEdit = QtGui.QLineEdit(self.AuthorDetails)
        self.FirstNameEdit.setObjectName("FirstNameEdit")
        self.gridLayout.addWidget(self.FirstNameEdit, 1, 1, 1, 3)
        self.LastNameLabel = QtGui.QLabel(self.AuthorDetails)
        self.LastNameLabel.setObjectName("LastNameLabel")
        self.gridLayout.addWidget(self.LastNameLabel, 2, 0, 1, 1)
        self.LastNameEdit = QtGui.QLineEdit(self.AuthorDetails)
        self.LastNameEdit.setObjectName("LastNameEdit")
        self.gridLayout.addWidget(self.LastNameEdit, 2, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(198, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        self.DeleteButton = QtGui.QPushButton(self.AuthorDetails)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/services/service_delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon)
        self.DeleteButton.setObjectName("DeleteButton")
        self.gridLayout.addWidget(self.DeleteButton, 3, 2, 1, 1)
        self.AddUpdateButton = QtGui.QPushButton(self.AuthorDetails)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/system/system_settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddUpdateButton.setIcon(icon1)
        self.AddUpdateButton.setObjectName("AddUpdateButton")
        self.gridLayout.addWidget(self.AddUpdateButton, 3, 3, 1, 1)
        self.MessageLabel = QtGui.QLabel(AuthorsDialog)
        self.MessageLabel.setGeometry(QtCore.QRect(20, 500, 261, 17))
        self.MessageLabel.setObjectName("MessageLabel")
        self.AuthorListView = QtGui.QTableWidget(AuthorsDialog)
        self.AuthorListView.setGeometry(QtCore.QRect(20, 20, 341, 301))
        self.AuthorListView.setAlternatingRowColors(True)
        self.AuthorListView.setColumnCount(2)
        self.AuthorListView.setObjectName("AuthorListView")
        self.AuthorListView.setColumnCount(2)
        self.AuthorListView.setRowCount(0)

        self.retranslateUi(AuthorsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AuthorsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AuthorsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AuthorsDialog)

    def retranslateUi(self, AuthorsDialog):
        AuthorsDialog.setWindowTitle(QtGui.QApplication.translate("AuthorsDialog", "Author Maintenance", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBox.setToolTip(QtGui.QApplication.translate("AuthorsDialog", "Exit Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.AuthorDetails.setTitle(QtGui.QApplication.translate("AuthorsDialog", "Author Details", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "Display Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.FirstNameLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "First Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.LastNameLabel.setText(QtGui.QApplication.translate("AuthorsDialog", "Last Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setToolTip(QtGui.QApplication.translate("AuthorsDialog", "Delete Author", None, QtGui.QApplication.UnicodeUTF8))
        self.AddUpdateButton.setToolTip(QtGui.QApplication.translate("AuthorsDialog", "Add Update Author", None, QtGui.QApplication.UnicodeUTF8))

