# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/raoul/Projects/openlp-2/resources/forms/settings.ui'
#
# Created: Sat Feb 28 23:59:58 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(u'SettingsDialog')
        SettingsDialog.resize(724, 502)
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #SettingsDialog.setWindowIcon(icon)
        self.SettingsLayout = QtGui.QVBoxLayout(SettingsDialog)
        self.SettingsLayout.setSpacing(8)
        self.SettingsLayout.setMargin(8)
        self.SettingsLayout.setObjectName(u'SettingsLayout')
        self.SettingsTabWidget = QtGui.QTabWidget(SettingsDialog)
        self.SettingsTabWidget.setObjectName(u'SettingsTabWidget')
        self.SettingsLayout.addWidget(self.SettingsTabWidget)
        self.ButtonsBox = QtGui.QDialogButtonBox(SettingsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonsBox.sizePolicy().hasHeightForWidth())
        self.ButtonsBox.setSizePolicy(sizePolicy)
        self.ButtonsBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ButtonsBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonsBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.ButtonsBox.setObjectName("ButtonsBox")
        self.SettingsLayout.addWidget(self.ButtonsBox)

        self.retranslateUi(SettingsDialog)
        self.SettingsTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.ButtonsBox, QtCore.SIGNAL("accepted()"), SettingsDialog.accept)
        QtCore.QObject.connect(self.ButtonsBox, QtCore.SIGNAL("rejected()"), SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QtGui.QApplication.translate("SettingsDialog", "Settings", None, QtGui.QApplication.UnicodeUTF8))
