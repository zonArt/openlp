# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'topicsdialog.ui'
#
# Created: Sun Jan  4 08:42:59 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from openlp.plugins.songs.lib import TextListData

class Ui_TopicsDialog(object):
    def setupUi(self, TopicsDialog):
        TopicsDialog.setObjectName("TopicsDialog")
        TopicsDialog.resize(387, 463)
        self.gridLayout_2 = QtGui.QGridLayout(TopicsDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TopicGroupBox = QtGui.QGroupBox(TopicsDialog)
        self.TopicGroupBox.setObjectName("TopicGroupBox")
        self.gridLayout = QtGui.QGridLayout(self.TopicGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.TopicNameLabel = QtGui.QLabel(self.TopicGroupBox)
        self.TopicNameLabel.setObjectName("TopicNameLabel")
        self.gridLayout.addWidget(self.TopicNameLabel, 0, 0, 1, 1)
        self.TopicNameEdit = QtGui.QLineEdit(self.TopicGroupBox)
        self.TopicNameEdit.setObjectName("TopicNameEdit")
        self.gridLayout.addWidget(self.TopicNameEdit, 0, 1, 1, 4)
        spacerItem = QtGui.QSpacerItem(198, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.DeleteButton = QtGui.QPushButton(self.TopicGroupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/services/service_delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeleteButton.setIcon(icon)
        self.DeleteButton.setObjectName("DeleteButton")
        self.gridLayout.addWidget(self.DeleteButton, 1, 3, 1, 1)
        self.AddUpdateButton = QtGui.QPushButton(self.TopicGroupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/system/system_settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddUpdateButton.setIcon(icon1)
        self.AddUpdateButton.setObjectName("AddUpdateButton")
        self.gridLayout.addWidget(self.AddUpdateButton, 1, 4, 1, 1)
        self.ClearButton = QtGui.QPushButton(self.TopicGroupBox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/songs/song_edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ClearButton.setIcon(icon2)
        self.ClearButton.setObjectName("ClearButton")
        self.gridLayout.addWidget(self.ClearButton, 1, 2, 1, 1)
        self.gridLayout_2.addWidget(self.TopicGroupBox, 1, 0, 1, 1)
        self.MessageLabel = QtGui.QLabel(TopicsDialog)
        self.MessageLabel.setObjectName("MessageLabel")
        self.gridLayout_2.addWidget(self.MessageLabel, 3, 0, 1, 1)

#        self.TopicsListView = QtGui.QTableWidget(TopicsDialog)
#        self.TopicsListView.setObjectName("TopicsListView")
#        self.TopicsListView.setColumnCount(0)
#        self.TopicsListView.setRowCount(0)

        self.TopicsListView = QtGui.QListView()
        self.TopicsListView.setAlternatingRowColors(True)
        self.TopicsListData = TextListData()
        self.TopicsListView.setModel(self.TopicsListData)
        self.gridLayout_2.addWidget(self.TopicsListView, 0, 0, 1, 1)

        self.ButtonBox = QtGui.QDialogButtonBox(TopicsDialog)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.ButtonBox.setObjectName("ButtonBox")
        self.gridLayout_2.addWidget(self.ButtonBox, 2, 0, 1, 1)

        self.retranslateUi(TopicsDialog)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("accepted()"), TopicsDialog.accept)
        QtCore.QObject.connect(self.ButtonBox, QtCore.SIGNAL("rejected()"), TopicsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TopicsDialog)

    def retranslateUi(self, TopicsDialog):
        TopicsDialog.setWindowTitle(QtGui.QApplication.translate("TopicsDialog", "Topic Maintenance", None, QtGui.QApplication.UnicodeUTF8))
        self.TopicGroupBox.setTitle(QtGui.QApplication.translate("TopicsDialog", "Topic", None, QtGui.QApplication.UnicodeUTF8))
        self.TopicNameLabel.setText(QtGui.QApplication.translate("TopicsDialog", "Topic Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteButton.setToolTip(QtGui.QApplication.translate("TopicsDialog", "Delete Author", None, QtGui.QApplication.UnicodeUTF8))
        self.AddUpdateButton.setToolTip(QtGui.QApplication.translate("TopicsDialog", "Add Update Author", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearButton.setToolTip(QtGui.QApplication.translate("TopicsDialog", "Clear Selection", None, QtGui.QApplication.UnicodeUTF8))


