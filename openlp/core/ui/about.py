# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

from PyQt4 import QtCore, QtGui

from openlp.core.lib import buildIcon

class AboutForm(QtGui.QDialog):
    """
    The About dialog
    """

    def __init__(self, parent, applicationVersion):
        """
        Do some initialisation stuff
        """
        QtGui.QDialog.__init__(self, parent)
        self.applicationVersion = applicationVersion
        self.setupUi(self)

    def setupUi(self, AboutForm):
        """
        Set up user interface
        """
        AboutForm.setObjectName(u'AboutForm')
        AboutForm.resize(470, 481)
        icon = buildIcon(u':/icon/openlp-logo-16x16.png')
        AboutForm.setWindowIcon(icon)
        AboutFormLayout = QtGui.QVBoxLayout(AboutForm)
        AboutFormLayout.setSpacing(8)
        AboutFormLayout.setMargin(8)
        AboutFormLayout.setObjectName(u'AboutDialogLayout')
        self.Logo = QtGui.QLabel(AboutForm)
        self.Logo.setAutoFillBackground(False)
        self.Logo.setStyleSheet(u'background-color: rgb(255, 255, 255);')
        self.Logo.setLineWidth(0)
        self.Logo.setPixmap(QtGui.QPixmap(u':/graphics/openlp-about-logo.png'))
        self.Logo.setScaledContents(False)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo.setObjectName(u'Logo')
        AboutFormLayout.addWidget(self.Logo)
        self.AboutNotebook = QtGui.QTabWidget(AboutForm)
        self.AboutNotebook.setObjectName(u'AboutNotebook')
        self.LicenseTab = QtGui.QWidget()
        self.LicenseTab.setObjectName(u'LicenseTab')
        self.LicenseTabLayout = QtGui.QVBoxLayout(self.LicenseTab)
        self.LicenseTabLayout.setSpacing(8)
        self.LicenseTabLayout.setMargin(8)
        self.LicenseTabLayout.setObjectName(u'LicenseTabLayout')
        self.CopyrightLabel = QtGui.QLabel(self.LicenseTab)
        self.CopyrightLabel.setObjectName(u'CopyrightLabel')
        self.LicenseTabLayout.addWidget(self.CopyrightLabel)
        self.AboutAuthors = QtGui.QLabel(self.LicenseTab)
        self.AboutAuthors.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.AboutAuthors.setWordWrap(True)
        self.AboutAuthors.setObjectName(u'AboutAuthors')
        self.LicenseTabLayout.addWidget(self.AboutAuthors)
        self.License1Label = QtGui.QLabel(self.LicenseTab)
        self.License1Label.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.License1Label.setWordWrap(True)
        self.License1Label.setObjectName(u'License1Label')
        self.LicenseTabLayout.addWidget(self.License1Label)
        self.License2Label = QtGui.QLabel(self.LicenseTab)
        self.License2Label.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.License2Label.setWordWrap(True)
        self.License2Label.setObjectName(u'License2Label')
        self.LicenseTabLayout.addWidget(self.License2Label)
        self.License3Label = QtGui.QLabel(self.LicenseTab)
        self.License3Label.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.License3Label.setWordWrap(True)
        self.License3Label.setObjectName(u'License3Label')
        self.LicenseTabLayout.addWidget(self.License3Label)
        self.License4Label = QtGui.QLabel(self.LicenseTab)
        self.License4Label.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.License4Label.setWordWrap(True)
        self.License4Label.setObjectName(u'License4Label')
        self.LicenseTabLayout.addWidget(self.License4Label)
        self.LicenseSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.LicenseTabLayout.addItem(self.LicenseSpacer)
        self.AboutNotebook.addTab(self.LicenseTab, u'License')
        self.CreditsTab = QtGui.QWidget()
        self.CreditsTab.setObjectName(u'CreditsTab')
        self.CreditsTabLayout = QtGui.QVBoxLayout(self.CreditsTab)
        self.CreditsTabLayout.setSpacing(0)
        self.CreditsTabLayout.setMargin(8)
        self.CreditsTabLayout.setObjectName(u'CreditsTabLayout')
        self.CreditsTextEdit = QtGui.QTextEdit(self.CreditsTab)
        self.CreditsTextEdit.setReadOnly(True)
        self.CreditsTextEdit.setObjectName(u'CreditsTextEdit')
        self.CreditsTabLayout.addWidget(self.CreditsTextEdit)
        self.AboutNotebook.addTab(self.CreditsTab, u'Credits')
        AboutFormLayout.addWidget(self.AboutNotebook)
        self.ButtonWidget = QtGui.QWidget(AboutForm)
        self.ButtonWidget.setObjectName(u'ButtonWidget')
        self.ButtonWidgetLayout = QtGui.QHBoxLayout(self.ButtonWidget)
        self.ButtonWidgetLayout.setSpacing(8)
        self.ButtonWidgetLayout.setMargin(0)
        self.ButtonWidgetLayout.setObjectName(u'ButtonWidgetLayout')
        spacerItem = QtGui.QSpacerItem(275, 20, QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Minimum)
        self.ButtonWidgetLayout.addItem(spacerItem)
        self.ContributeButton = QtGui.QPushButton(self.ButtonWidget)
        self.ContributeButton.setObjectName(u'ContributeButton')
        self.ButtonWidgetLayout.addWidget(self.ContributeButton)
        self.CloseButton = QtGui.QPushButton(self.ButtonWidget)
        self.CloseButton.setObjectName(u'CloseButton')
        self.ButtonWidgetLayout.addWidget(self.CloseButton)
        AboutFormLayout.addWidget(self.ButtonWidget)
        self.extContributeItem = QtGui.QAction(AboutForm)
        self.extContributeItem.setObjectName(u'extContributeItem')
        # Do translation
        self.retranslateUi(AboutForm)
        self.AboutNotebook.setCurrentIndex(0)
        QtCore.QObject.connect(self.CloseButton, QtCore.SIGNAL(u'clicked()'),
            AboutForm.close)
        QtCore.QObject.connect(self.ContributeButton,
            QtCore.SIGNAL(u'clicked()'), self.onContributeButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(AboutForm)

    def retranslateUi(self, AboutForm):
        """
        Set up translation
        """
        AboutForm.setWindowTitle(self.trUtf8('About openlp.org'))
        self.CopyrightLabel.setText(
            self.trUtf8('Copyright \u00a9 2004-2009 openlp.org Foundation'))
        self.AboutAuthors.setText(self.trUtf8(
            'openlp.org is written and maintained by volunteers. If you would '
            'like to see more free Christian software being written, please '
            'consider contributing by using the button below.'))
        self.License1Label.setText(self.trUtf8(
            'This program is free software; you can redistribute it and/or '
            'modify it under the terms of the GNU General Public License as '
            'published by the Free Software Foundation; either version 2 of '
            'the License, or (at your option) any later version.'))
        self.License2Label.setText(self.trUtf8(
            'You should have received a copy of the GNU General Public '
            'License along with this program; if not, write to the Free '
            'Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, '
            'MA 02111-1307 USA.'))
        self.License3Label.setText(self.trUtf8(
            'This program is distributed in the hope that it will be useful, '
            'but WITHOUT ANY WARRANTY; without even the implied warranty of '
            'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU '
            'General Public License for more details.'))
        self.License4Label.setText(unicode(self.trUtf8(
            'Software version %s, Build %s')) %
            (self.applicationVersion[u'version'], self.applicationVersion[u'build']))
        self.AboutNotebook.setTabText(
            self.AboutNotebook.indexOf(self.LicenseTab), self.trUtf8('License'))
        self.CreditsTextEdit.setPlainText(self.trUtf8(
            'Project Lead\n'
            '    Raoul \"superfly\" Snyman\n'
            '\n'
            'Developers\n'
            '    Tim \"TRB143\" Bentley\n'
            '    Jonathan \"gushie\" Corwin\n'
            '    Scott \"sguerrieri\" Guerrieri\n'
            '    Raoul \"superfly\" Snyman\n'
            '    Martin \"mijiti\" Thompson\n'
            '    Jon \"Meths\" Tibble\n'
            '    Carsten \"catini\" Tingaard'))
        self.AboutNotebook.setTabText(
            self.AboutNotebook.indexOf(self.CreditsTab), self.trUtf8('Credits'))
        self.ContributeButton.setText(self.trUtf8('Contribute'))
        self.CloseButton.setText(self.trUtf8('Close'))
        self.extContributeItem.setText(self.trUtf8('&Contribute'))

    def onContributeButtonClicked(self):
        """
        Launch a web browser and go to the contribute page on the site.
        """
        import webbrowser
        url = "http://www.openlp.org/en/documentation/introduction/contributing.html"
        webbrowser.open_new(url)
