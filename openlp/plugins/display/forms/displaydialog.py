# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'displaydialog.ui'
#
# Created: Sat Apr 24 17:20:48 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DisplaysDialog(object):
    def setupUi(self, DisplaysDialog):
        DisplaysDialog.setObjectName("DisplaysDialog")
        DisplaysDialog.resize(327, 224)
        self.OkpushButton = QtGui.QPushButton(DisplaysDialog)
        self.OkpushButton.setGeometry(QtCore.QRect(210, 200, 97, 24))
        self.OkpushButton.setObjectName("OkpushButton")
        self.widget = QtGui.QWidget(DisplaysDialog)
        self.widget.setGeometry(QtCore.QRect(10, 0, 301, 191))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CurrentGroupBox = QtGui.QGroupBox(self.widget)
        self.CurrentGroupBox.setObjectName("CurrentGroupBox")
        self.layoutWidget = QtGui.QWidget(self.CurrentGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 261, 17))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Xpos = QtGui.QLabel(self.layoutWidget)
        self.Xpos.setAlignment(QtCore.Qt.AlignCenter)
        self.Xpos.setObjectName("Xpos")
        self.horizontalLayout.addWidget(self.Xpos)
        self.Ypos = QtGui.QLabel(self.layoutWidget)
        self.Ypos.setAlignment(QtCore.Qt.AlignCenter)
        self.Ypos.setObjectName("Ypos")
        self.horizontalLayout.addWidget(self.Ypos)
        self.Height = QtGui.QLabel(self.layoutWidget)
        self.Height.setAlignment(QtCore.Qt.AlignCenter)
        self.Height.setObjectName("Height")
        self.horizontalLayout.addWidget(self.Height)
        self.Width = QtGui.QLabel(self.layoutWidget)
        self.Width.setAlignment(QtCore.Qt.AlignCenter)
        self.Width.setObjectName("Width")
        self.horizontalLayout.addWidget(self.Width)
        self.verticalLayout.addWidget(self.CurrentGroupBox)
        self.CurrentGroupBox_2 = QtGui.QGroupBox(self.widget)
        self.CurrentGroupBox_2.setObjectName("CurrentGroupBox_2")
        self.layoutWidget1 = QtGui.QWidget(self.CurrentGroupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 30, 261, 27))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.XposEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.XposEdit.setObjectName("XposEdit")
        self.horizontalLayout_2.addWidget(self.XposEdit)
        self.YposEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.YposEdit.setObjectName("YposEdit")
        self.horizontalLayout_2.addWidget(self.YposEdit)
        self.HeightEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.HeightEdit.setObjectName("HeightEdit")
        self.horizontalLayout_2.addWidget(self.HeightEdit)
        self.WidthEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.WidthEdit.setObjectName("WidthEdit")
        self.horizontalLayout_2.addWidget(self.WidthEdit)
        self.verticalLayout.addWidget(self.CurrentGroupBox_2)

        self.retranslateUi(DisplaysDialog)
        QtCore.QObject.connect(self.OkpushButton, QtCore.SIGNAL("pressed()"), DisplaysDialog.close)
        QtCore.QMetaObject.connectSlotsByName(DisplaysDialog)

    def retranslateUi(self, DisplaysDialog):
        DisplaysDialog.setWindowTitle(QtGui.QApplication.translate("DisplaysDialog", "Amend Display Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.OkpushButton.setText(QtGui.QApplication.translate("DisplaysDialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.CurrentGroupBox.setTitle(QtGui.QApplication.translate("DisplaysDialog", "Default Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.Xpos.setText(QtGui.QApplication.translate("DisplaysDialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.Ypos.setText(QtGui.QApplication.translate("DisplaysDialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.Height.setText(QtGui.QApplication.translate("DisplaysDialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.Width.setText(QtGui.QApplication.translate("DisplaysDialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.CurrentGroupBox_2.setTitle(QtGui.QApplication.translate("DisplaysDialog", "Amend Settings", None, QtGui.QApplication.UnicodeUTF8))

