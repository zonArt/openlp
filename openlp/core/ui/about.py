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
from PyQt4.QtGui import QDialog

from openlp.core import translate
from openlp.core.resources import *

class AboutForm(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

    def setupUi(self, AboutForm):
        AboutForm.setObjectName("AboutForm")
        AboutForm.resize(470, 481)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/openlp.org-icon-32.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutForm.setWindowIcon(icon)
        AboutFormLayout = QtGui.QVBoxLayout(AboutForm)
        AboutFormLayout.setSpacing(8)
        AboutFormLayout.setMargin(8)
        AboutFormLayout.setObjectName("AboutDialogLayout")
        self.Logo = QtGui.QLabel(AboutForm)
        self.Logo.setAutoFillBackground(False)
        self.Logo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Logo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Logo.setLineWidth(1)
        self.Logo.setPixmap(QtGui.QPixmap(":/graphics/about-new.bmp"))
        self.Logo.setScaledContents(False)
        self.Logo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Logo.setObjectName("Logo")
        AboutFormLayout.addWidget(self.Logo)
        self.AboutNotebook = QtGui.QTabWidget(AboutForm)
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
        self.AboutNotebook.addTab(self.LicenseTab, "License")
        self.CreditsTab = QtGui.QWidget()
        self.CreditsTab.setObjectName("CreditsTab")
        self.CreditsTabLayout = QtGui.QVBoxLayout(self.CreditsTab)
        self.CreditsTabLayout.setSpacing(0) #
        self.CreditsTabLayout.setMargin(8) #
        self.CreditsTabLayout.setObjectName("CreditsTabLayout")
        self.CreditsTextEdit = QtGui.QTextEdit(self.CreditsTab)
        self.CreditsTextEdit.setReadOnly(True)
        self.CreditsTextEdit.setObjectName("CreditsTextEdit")
        self.CreditsTabLayout.addWidget(self.CreditsTextEdit)
        self.AboutNotebook.addTab(self.CreditsTab, "Credits")
        AboutFormLayout.addWidget(self.AboutNotebook)
        self.ButtonWidget = QtGui.QWidget(AboutForm)
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
        AboutFormLayout.addWidget(self.ButtonWidget)
        self.extContributeItem = QtGui.QAction(AboutForm)
        self.extContributeItem.setObjectName("extContributeItem")

        self.retranslateUi(AboutForm)
        self.AboutNotebook.setCurrentIndex(0)
        QtCore.QObject.connect(self.CloseButton, QtCore.SIGNAL("clicked()"), AboutForm.close)
        QtCore.QMetaObject.connectSlotsByName(AboutForm)

        QtCore.QObject.connect(self.ContributeButton, QtCore.SIGNAL("clicked()"), self.onContributeButtonClicked)

    def retranslateUi(self, AboutForm):
        AboutForm.setWindowTitle(translate("AboutDialog", "About openlp.org",))
        self.CopyrightLabel.setText(translate("AboutDialog", "Copyright © 2004-2009 openlp.org Foundation"))
        self.AboutAuthors.setText(translate("AboutDialog", "openlp.org is written and maintained by volunteers. If you would like to see more free Christian software being written, please consider contributing by using the button below."))
        self.License1Label.setText(translate("AboutDialog", "This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version."))
        self.License2Label.setText(translate("AboutDialog", "You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA."))
        self.License3Label.setText(translate("AboutDialog", "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details."))
        self.AboutNotebook.setTabText(self.AboutNotebook.indexOf(self.LicenseTab), QtGui.QApplication.translate("AboutDialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.CreditsTextEdit.setPlainText(translate("AboutDialog", "Project Lead\n"
"    Raoul \"superfly\" Snyman\n"
"\n"
"Developers\n"
"    Tim \"TRB143\" Bentley\n"
"    Jonathan \"gushie\" Corwin\n"
"    Scott \"sguerrieri\" Guerrieri\n"
"    Raoul \"superfly\" Snyman\n"
"    Martin \"mijiti\" Thompson\n"
"    Carsten \"catini\" Tingaard"))
        self.AboutNotebook.setTabText(self.AboutNotebook.indexOf(self.CreditsTab), translate("AboutDialog", "Credits"))
        self.ContributeButton.setText(translate("AboutDialog", "Contribute"))
        self.CloseButton.setText(translate("AboutDialog", "Close"))
        self.extContributeItem.setText(translate("AboutDialog", "&Contribute"))

    def onContributeButtonClicked(self):
        ''' This routine will open the default
            web-browser to the contribute page
            of openlp.org as did the original
            button on the About form
        '''
        import webbrowser
        url = "http://www.openlp.org/en/documentation/introduction/contributing.html"
        webbrowser.open_new(url)
