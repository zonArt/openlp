# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Project Folders\Personal Projects\openlp-2\trunk\openlp\resources\forms\about.ui'
#
# Created: Wed Nov 05 20:52:55 2008
#      by: PyQt4 UI code generator 4.4.4-snapshot-20080918
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

from openlp.resources import *

class AboutForm(object):
    
    def __init__(self):
        self.AboutDialog = QtGui.QDialog()
        self.setupUi()
        
    def setupUi(self):
        self.AboutDialog.setObjectName("AboutDialog")
        self.AboutDialog.resize(470, 481)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AboutDialog.setWindowIcon(icon)
        self.AboutDialogLayout = QtGui.QVBoxLayout(self.AboutDialog)
        self.AboutDialogLayout.setSpacing(8)
        self.AboutDialogLayout.setMargin(8)
        self.AboutDialogLayout.setObjectName("AboutDialogLayout")
        self.Logo = QtGui.QLabel(self.AboutDialog)
        self.Logo.setAutoFillBackground(False)
        self.Logo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Logo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Logo.setLineWidth(1)
        self.Logo.setPixmap(QtGui.QPixmap(":/graphics/about-new.bmp"))
        self.Logo.setScaledContents(False)
        self.Logo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Logo.setObjectName("Logo")
        self.AboutDialogLayout.addWidget(self.Logo)
        self.AboutNotebook = QtGui.QTabWidget(self.AboutDialog)
        self.AboutNotebook.setObjectName("AboutNotebook")
        self.LicenseTab = QtGui.QWidget()
        self.LicenseTab.setObjectName("LicenseTab")
        self.LicenseTabLayout = QtGui.QVBoxLayout(self.LicenseTab)
        self.LicenseTabLayout.setSpacing(8)
        self.LicenseTabLayout.setMargin(8)
        self.LicenseTabLayout.setObjectName("LicenseTabLayout")
        self.CopyrightLabel = QtGui.QLabel(self.LicenseTab)
        self.CopyrightLabel.setObjectName("CopyrightLabel")
        self.LicenseTabLayout.addWidget(self.CopyrightLabel)
        self.AboutAuthors = QtGui.QLabel(self.LicenseTab)
        self.AboutAuthors.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.AboutAuthors.setWordWrap(True)
        self.AboutAuthors.setObjectName("AboutAuthors")
        self.LicenseTabLayout.addWidget(self.AboutAuthors)
        self.License1Label = QtGui.QLabel(self.LicenseTab)
        self.License1Label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.License1Label.setWordWrap(True)
        self.License1Label.setObjectName("License1Label")
        self.LicenseTabLayout.addWidget(self.License1Label)
        self.License2Label = QtGui.QLabel(self.LicenseTab)
        self.License2Label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.License2Label.setWordWrap(True)
        self.License2Label.setObjectName("License2Label")
        self.LicenseTabLayout.addWidget(self.License2Label)
        self.License3Label = QtGui.QLabel(self.LicenseTab)
        self.License3Label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.License3Label.setWordWrap(True)
        self.License3Label.setObjectName("License3Label")
        self.LicenseTabLayout.addWidget(self.License3Label)
        self.AboutNotebook.addTab(self.LicenseTab, "")
        self.CreditsTab = QtGui.QWidget()
        self.CreditsTab.setObjectName("CreditsTab")
        self.CreditsTabLayout = QtGui.QVBoxLayout(self.CreditsTab)
        self.CreditsTabLayout.setObjectName("CreditsTabLayout")
        self.CreditsScrollArea = QtGui.QScrollArea(self.CreditsTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CreditsScrollArea.sizePolicy().hasHeightForWidth())
        self.CreditsScrollArea.setSizePolicy(sizePolicy)
        self.CreditsScrollArea.setSizeIncrement(QtCore.QSize(10, 10))
        self.CreditsScrollArea.setBaseSize(QtCore.QSize(372, 391))
        self.CreditsScrollArea.setMouseTracking(True)
        self.CreditsScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.CreditsScrollArea.setWidgetResizable(False)
        self.CreditsScrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.CreditsScrollArea.setObjectName("CreditsScrollArea")
        self.CreditsScrollContent = QtGui.QWidget(self.CreditsScrollArea)
        self.CreditsScrollContent.setGeometry(QtCore.QRect(6, 0, 400, 760))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CreditsScrollContent.sizePolicy().hasHeightForWidth())
        self.CreditsScrollContent.setSizePolicy(sizePolicy)
        self.CreditsScrollContent.setBaseSize(QtCore.QSize(400, 760))
        self.CreditsScrollContent.setObjectName("CreditsScrollContent")
        self.CreditsScrollContentLayout = QtGui.QVBoxLayout(self.CreditsScrollContent)
        self.CreditsScrollContentLayout.setSpacing(0)
        self.CreditsScrollContentLayout.setMargin(8)
        self.CreditsScrollContentLayout.setObjectName("CreditsScrollContentLayout")
        self.CreditsLabel = QtGui.QLabel(self.CreditsScrollContent)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CreditsLabel.sizePolicy().hasHeightForWidth())
        self.CreditsLabel.setSizePolicy(sizePolicy)
        self.CreditsLabel.setMinimumSize(QtCore.QSize(369, 391))
        self.CreditsLabel.setSizeIncrement(QtCore.QSize(10, 10))
        self.CreditsLabel.setBaseSize(QtCore.QSize(369, 760))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.CreditsLabel.setFont(font)
        self.CreditsLabel.setObjectName("CreditsLabel")
        self.CreditsScrollContentLayout.addWidget(self.CreditsLabel)
        self.CreditsScrollArea.setWidget(self.CreditsScrollContent)
        self.CreditsTabLayout.addWidget(self.CreditsScrollArea)
        self.AboutNotebook.addTab(self.CreditsTab, "")
        self.AboutDialogLayout.addWidget(self.AboutNotebook)
        self.ButtonWidget = QtGui.QWidget(self.AboutDialog)
        self.ButtonWidget.setObjectName("ButtonWidget")
        self.ButtonWidgetLayout = QtGui.QHBoxLayout(self.ButtonWidget)
        self.ButtonWidgetLayout.setSpacing(8)
        self.ButtonWidgetLayout.setMargin(0)
        self.ButtonWidgetLayout.setObjectName("ButtonWidgetLayout")
        spacerItem = QtGui.QSpacerItem(275, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ButtonWidgetLayout.addItem(spacerItem)
        self.ContributeButton = QtGui.QPushButton(self.ButtonWidget)
        self.ContributeButton.setObjectName("ContributeButton")
        self.ButtonWidgetLayout.addWidget(self.ContributeButton)
        self.CloseButton = QtGui.QPushButton(self.ButtonWidget)
        self.CloseButton.setObjectName("CloseButton")
        self.ButtonWidgetLayout.addWidget(self.CloseButton)
        self.AboutDialogLayout.addWidget(self.ButtonWidget)
        self.extContributeItem = QtGui.QAction(self.AboutDialog)
        self.extContributeItem.setObjectName("extContributeItem")

        self.retranslateUi()
        self.AboutNotebook.setCurrentIndex(1)
        QtCore.QObject.connect(self.CloseButton, QtCore.SIGNAL("clicked()"), self.AboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(self.AboutDialog)
        self.AboutDialog.setTabOrder(self.CreditsScrollArea, self.ContributeButton)
        
        QtCore.QObject.connect(self.ContributeButton, QtCore.SIGNAL("clicked()"), self.onContributeButtonClicked)

    def retranslateUi(self):
        self.AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About openlp.org", None, QtGui.QApplication.UnicodeUTF8))
        self.CopyrightLabel.setText(QtGui.QApplication.translate("AboutDialog", "Copyright © 2004-2008 openlp.org Foundation", None, QtGui.QApplication.UnicodeUTF8))
        self.AboutAuthors.setText(QtGui.QApplication.translate("AboutDialog", "openlp.org is written and maintained by volunteers. If you would like to see more free Christian software being written, please consider contributing by using the button below.", None, QtGui.QApplication.UnicodeUTF8))
        self.License1Label.setText(QtGui.QApplication.translate("AboutDialog", "This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.", None, QtGui.QApplication.UnicodeUTF8))
        self.License2Label.setText(QtGui.QApplication.translate("AboutDialog", "You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.", None, QtGui.QApplication.UnicodeUTF8))
        self.License3Label.setText(QtGui.QApplication.translate("AboutDialog", "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.", None, QtGui.QApplication.UnicodeUTF8))
        self.AboutNotebook.setTabText(self.AboutNotebook.indexOf(self.LicenseTab), QtGui.QApplication.translate("AboutDialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.CreditsLabel.setText(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><span style=\" font-size:10pt; font-weight:600; text-decoration: underline;\">openlp.org 2.0.0</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Copyright © 2004-2008 openlp.org Foundation</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-weight:600;\">- Lead Developer -</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Raoul Snyman</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-weight:600;\">- Original Development -</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Tim Ebenezer</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-weight:600;\">- Additional Development -</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Derek Scotney</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-weight:600;\">- Testing -</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Jonathan Corwin</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Scott Hileard</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Ken Marshall</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Duane Pearce</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Andrew (thealok)</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Les Norbo</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Many others in the community</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-weight:600;\">- Documentation -</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Raoul Snyman</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Hannah Snyman</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">David Bunce</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Seth Mayo</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-weight:600;\">- Components Used -</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">JCL &amp; JVCL - Project Jedi</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">Mozilla Public License</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Toolbar2000 - JR Software</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">GNU General Public License</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">TBX - Alex Denisov</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">Custom Freeware License</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Graphics 32 - Alex Denisov</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">Mozilla Public License</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Saturn Component Pack - Saturn Laboratories</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">Mozilla Public License</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-weight:600;\">- Final Credit -</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">\"For God so loved the world that He gave</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">His one and only Son, so that whoever</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">believes in Him will not perish but inherit</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"><span style=\" font-style:italic;\">eternal life.\"  -- John 3:16</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">And last but not least, final credit goes to</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">God our Father, for sending His Son to die</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">on the cross, setting us free from sin. We</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">bring this software to you for free because</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">He has set us free.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.AboutNotebook.setTabText(self.AboutNotebook.indexOf(self.CreditsTab), QtGui.QApplication.translate("AboutDialog", "Credits", None, QtGui.QApplication.UnicodeUTF8))
        self.ContributeButton.setText(QtGui.QApplication.translate("AboutDialog", "Contribute", None, QtGui.QApplication.UnicodeUTF8))
        self.CloseButton.setText(QtGui.QApplication.translate("AboutDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.extContributeItem.setText(QtGui.QApplication.translate("AboutDialog", "&Contribute", None, QtGui.QApplication.UnicodeUTF8))
        
    def show(self):
        self.AboutDialog.show()
        
    def onContributeButtonClicked(self):
        ''' This routine will open the default
            web-browser to the contribute page
            of openlp.org as did the original
            button on the About form
        '''
        import webbrowser
        url = "http://www.openlp.org/en/documentation/introduction/contributing.html"
        webbrowser.open_new(url)
