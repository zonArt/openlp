# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import build_icon, translate

class Ui_BibleImportWizard(object):
    def setupUi(self, bibleImportWizard):
        bibleImportWizard.setObjectName(u'bibleImportWizard')
        bibleImportWizard.setModal(True)
        bibleImportWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        bibleImportWizard.setOptions(
            QtGui.QWizard.IndependentPages |
            QtGui.QWizard.NoBackButtonOnStartPage |
            QtGui.QWizard.NoBackButtonOnLastPage)
        # Welcome Page
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setPixmap(QtGui.QWizard.WatermarkPixmap,
            QtGui.QPixmap(u':/wizards/wizard_importbible.bmp'))
        self.welcomePage.setObjectName(u'WelcomePage')
        self.welcomeLayout = QtGui.QVBoxLayout(self.welcomePage)
        self.welcomeLayout.setObjectName(u'WelcomeLayout')
        self.titleLabel = QtGui.QLabel(self.welcomePage)
        self.titleLabel.setObjectName(u'TitleLabel')
        self.welcomeLayout.addWidget(self.titleLabel)
        self.welcomeLayout.addSpacing(40)
        self.informationLabel = QtGui.QLabel(self.welcomePage)
        self.informationLabel.setWordWrap(True)
        self.informationLabel.setObjectName(u'InformationLabel')
        self.welcomeLayout.addWidget(self.informationLabel)
        self.welcomeLayout.addStretch()
        bibleImportWizard.addPage(self.welcomePage)
        # Select Page
        self.selectPage = QtGui.QWizardPage()
        self.selectPage.setObjectName(u'SelectPage')
        self.selectPageLayout = QtGui.QVBoxLayout(self.selectPage)
        self.selectPageLayout.setObjectName(u'SelectPageLayout')
        self.formatLayout = QtGui.QFormLayout()
        self.formatLayout.setObjectName(u'FormatLayout')
        self.formatLabel = QtGui.QLabel(self.selectPage)
        self.formatLabel.setObjectName(u'FormatLabel')
        self.formatComboBox = QtGui.QComboBox(self.selectPage)
        self.formatComboBox.addItems([u'', u'', u'', u'', u''])
        self.formatComboBox.setObjectName(u'FormatComboBox')
        self.formatLayout.addRow(self.formatLabel, self.formatComboBox)
        self.formatSpacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Minimum)
        self.formatLayout.setItem(1, QtGui.QFormLayout.LabelRole,
            self.formatSpacer)
        self.selectPageLayout.addLayout(self.formatLayout)
        self.selectStack = QtGui.QStackedLayout()
        self.selectStack.setObjectName(u'SelectStack')
        self.osisWidget = QtGui.QWidget(self.selectPage)
        self.osisWidget.setObjectName(u'OsisWidget')
        self.osisLayout = QtGui.QFormLayout(self.osisWidget)
        self.osisLayout.setMargin(0)
        self.osisLayout.setObjectName(u'OsisLayout')
        self.osisFileLabel = QtGui.QLabel(self.osisWidget)
        self.osisFileLabel.setObjectName(u'OsisFileLabel')
        self.osisFileLayout = QtGui.QHBoxLayout()
        self.osisFileLayout.setObjectName(u'OsisFileLayout')
        self.osisFileEdit = QtGui.QLineEdit(self.osisWidget)
        self.osisFileEdit.setObjectName(u'OsisFileEdit')
        self.osisFileLayout.addWidget(self.osisFileEdit)
        self.osisBrowseButton = QtGui.QToolButton(self.osisWidget)
        self.osisBrowseButton.setIcon(build_icon(u':/general/general_open.png'))
        self.osisBrowseButton.setObjectName(u'OsisBrowseButton')
        self.osisFileLayout.addWidget(self.osisBrowseButton)
        self.osisLayout.addRow(self.osisFileLabel, self.osisFileLayout)
        self.osisSpacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Minimum)
        self.osisLayout.setItem(1, QtGui.QFormLayout.LabelRole, self.osisSpacer)
        self.selectStack.addWidget(self.osisWidget)
        self.csvWidget = QtGui.QWidget(self.selectPage)
        self.csvWidget.setObjectName(u'CsvWidget')
        self.csvLayout = QtGui.QFormLayout(self.csvWidget)
        self.csvLayout.setMargin(0)
        self.csvLayout.setObjectName(u'CsvLayout')
        self.csvBooksLabel = QtGui.QLabel(self.csvWidget)
        self.csvBooksLabel.setObjectName(u'CsvBooksLabel')
        self.csvBooksLayout = QtGui.QHBoxLayout()
        self.csvBooksLayout.setObjectName(u'CsvBooksLayout')
        self.csvBooksEdit = QtGui.QLineEdit(self.csvWidget)
        self.csvBooksEdit.setObjectName(u'CsvBooksEdit')
        self.csvBooksLayout.addWidget(self.csvBooksEdit)
        self.csvBooksButton = QtGui.QToolButton(self.csvWidget)
        self.csvBooksButton.setIcon(build_icon(u':/general/general_open.png'))
        self.csvBooksButton.setObjectName(u'CsvBooksButton')
        self.csvBooksLayout.addWidget(self.csvBooksButton)
        self.csvLayout.addRow(self.csvBooksLabel, self.csvBooksLayout)
        self.csvVersesLabel = QtGui.QLabel(self.csvWidget)
        self.csvVersesLabel.setObjectName(u'CsvVersesLabel')
        self.csvVersesLayout = QtGui.QHBoxLayout()
        self.csvVersesLayout.setObjectName(u'CsvVersesLayout')
        self.csvVersesEdit = QtGui.QLineEdit(self.csvWidget)
        self.csvVersesEdit.setObjectName(u'CsvVersesEdit')
        self.csvVersesLayout.addWidget(self.csvVersesEdit)
        self.csvVersesButton = QtGui.QToolButton(self.csvWidget)
        self.csvVersesButton.setIcon(build_icon(u':/general/general_open.png'))
        self.csvVersesButton.setObjectName(u'CsvVersesButton')
        self.csvVersesLayout.addWidget(self.csvVersesButton)
        self.csvLayout.addRow(self.csvVersesLabel, self.csvVersesLayout)
        self.csvSpacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Minimum)
        self.csvLayout.setItem(2, QtGui.QFormLayout.LabelRole, self.csvSpacer)
        self.selectStack.addWidget(self.csvWidget)
        self.openSongWidget = QtGui.QWidget(self.selectPage)
        self.openSongWidget.setObjectName(u'OpenSongWidget')
        self.openSongLayout = QtGui.QFormLayout(self.openSongWidget)
        self.openSongLayout.setMargin(0)
        self.openSongLayout.setObjectName(u'OpenSongLayout')
        self.openSongFileLabel = QtGui.QLabel(self.openSongWidget)
        self.openSongFileLabel.setObjectName(u'OpenSongFileLabel')
        self.openSongFileLayout = QtGui.QHBoxLayout()
        self.openSongFileLayout.setObjectName(u'OpenSongFileLayout')
        self.openSongFileEdit = QtGui.QLineEdit(self.openSongWidget)
        self.openSongFileEdit.setObjectName(u'OpenSongFileEdit')
        self.openSongFileLayout.addWidget(self.openSongFileEdit)
        self.openSongBrowseButton = QtGui.QToolButton(self.openSongWidget)
        self.openSongBrowseButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.openSongBrowseButton.setObjectName(u'OpenSongBrowseButton')
        self.openSongFileLayout.addWidget(self.openSongBrowseButton)
        self.openSongLayout.addRow(self.openSongFileLabel,
            self.openSongFileLayout)
        self.openSongSpacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Minimum)
        self.openSongLayout.setItem(1, QtGui.QFormLayout.LabelRole,
            self.openSongSpacer)
        self.selectStack.addWidget(self.openSongWidget)
        self.webTabWidget = QtGui.QTabWidget(self.selectPage)
        self.webTabWidget.setObjectName(u'WebTabWidget')
        self.webBibleTab = QtGui.QWidget()
        self.webBibleTab.setObjectName(u'WebBibleTab')
        self.webBibleLayout = QtGui.QFormLayout(self.webBibleTab)
        self.webBibleLayout.setObjectName(u'WebBibleLayout')
        self.webSourceLabel = QtGui.QLabel(self.webBibleTab)
        self.webSourceLabel.setObjectName(u'WebSourceLabel')
        self.webBibleLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.webSourceLabel)
        self.webSourceComboBox = QtGui.QComboBox(self.webBibleTab)
        self.webSourceComboBox.setObjectName(u'WebSourceComboBox')
        self.webSourceComboBox.addItems([u'', u'', u''])
        self.webBibleLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.webSourceComboBox)
        self.webTranslationLabel = QtGui.QLabel(self.webBibleTab)
        self.webTranslationLabel.setObjectName(u'webTranslationLabel')
        self.webBibleLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.webTranslationLabel)
        self.webTranslationComboBox = QtGui.QComboBox(self.webBibleTab)
        self.webTranslationComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToContents)
        self.webTranslationComboBox.setObjectName(u'WebTranslationComboBox')
        self.webBibleLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.webTranslationComboBox)
        self.webTabWidget.addTab(self.webBibleTab, u'')
        self.webProxyTab = QtGui.QWidget()
        self.webProxyTab.setObjectName(u'WebProxyTab')
        self.webProxyLayout = QtGui.QFormLayout(self.webProxyTab)
        self.webProxyLayout.setObjectName(u'WebProxyLayout')
        self.webServerLabel = QtGui.QLabel(self.webProxyTab)
        self.webServerLabel.setObjectName(u'WebServerLabel')
        self.webProxyLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.webServerLabel)
        self.webServerEdit = QtGui.QLineEdit(self.webProxyTab)
        self.webServerEdit.setObjectName(u'WebServerEdit')
        self.webProxyLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.webServerEdit)
        self.webUserLabel = QtGui.QLabel(self.webProxyTab)
        self.webUserLabel.setObjectName(u'WebUserLabel')
        self.webProxyLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.webUserLabel)
        self.webUserEdit = QtGui.QLineEdit(self.webProxyTab)
        self.webUserEdit.setObjectName(u'WebUserEdit')
        self.webProxyLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.webUserEdit)
        self.webPasswordLabel = QtGui.QLabel(self.webProxyTab)
        self.webPasswordLabel.setObjectName(u'WebPasswordLabel')
        self.webProxyLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.webPasswordLabel)
        self.webPasswordEdit = QtGui.QLineEdit(self.webProxyTab)
        self.webPasswordEdit.setObjectName(u'WebPasswordEdit')
        self.webProxyLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.webPasswordEdit)
        self.webTabWidget.addTab(self.webProxyTab, u'')
        self.selectStack.addWidget(self.webTabWidget)
        self.openlp1Widget = QtGui.QWidget(self.selectPage)
        self.openlp1Widget.setObjectName(u'Openlp1Widget')
        self.openlp1Layout = QtGui.QFormLayout(self.openlp1Widget)
        self.openlp1Layout.setMargin(0)
        self.openlp1Layout.setObjectName(u'Openlp1Layout')
        self.openlp1FileLabel = QtGui.QLabel(self.openlp1Widget)
        self.openlp1FileLabel.setObjectName(u'Openlp1FileLabel')
        self.openlp1FileLayout = QtGui.QHBoxLayout()
        self.openlp1FileLayout.setObjectName(u'Openlp1FileLayout')
        self.openlp1FileEdit = QtGui.QLineEdit(self.openlp1Widget)
        self.openlp1FileEdit.setObjectName(u'Openlp1FileEdit')
        self.openlp1FileLayout.addWidget(self.openlp1FileEdit)
        self.openlp1BrowseButton = QtGui.QToolButton(self.openlp1Widget)
        self.openlp1BrowseButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.openlp1BrowseButton.setObjectName(u'Openlp1BrowseButton')
        self.openlp1FileLayout.addWidget(self.openlp1BrowseButton)
        self.openlp1Layout.addRow(self.openlp1FileLabel, self.openlp1FileLayout)
        self.openlp1DisabledLabel = QtGui.QLabel(self.openlp1Widget)
        self.openlp1DisabledLabel.setWordWrap(True)
        self.openlp1DisabledLabel.setObjectName(u'Openlp1DisabledLabel')
        self.openlp1Layout.addRow(self.openlp1DisabledLabel)
        self.openlp1Spacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Minimum)
        self.openlp1Layout.setItem(1, QtGui.QFormLayout.LabelRole,
            self.openlp1Spacer)
        self.selectStack.addWidget(self.openlp1Widget)
        self.selectPageLayout.addLayout(self.selectStack)
        bibleImportWizard.addPage(self.selectPage)
        # License Page
        self.licenseDetailsPage = QtGui.QWizardPage()
        self.licenseDetailsPage.setObjectName(u'LicenseDetailsPage')
        self.licenseDetailsLayout = QtGui.QFormLayout(self.licenseDetailsPage)
        self.licenseDetailsLayout.setObjectName(u'LicenseDetailsLayout')
        self.versionNameLabel = QtGui.QLabel(self.licenseDetailsPage)
        self.versionNameLabel.setObjectName(u'VersionNameLabel')
        self.licenseDetailsLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.versionNameLabel)
        self.versionNameEdit = QtGui.QLineEdit(self.licenseDetailsPage)
        self.versionNameEdit.setObjectName(u'VersionNameEdit')
        self.licenseDetailsLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.versionNameEdit)
        self.copyrightLabel = QtGui.QLabel(self.licenseDetailsPage)
        self.copyrightLabel.setObjectName(u'CopyrightLabel')
        self.licenseDetailsLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.copyrightLabel)
        self.copyrightEdit = QtGui.QLineEdit(self.licenseDetailsPage)
        self.copyrightEdit.setObjectName(u'CopyrightEdit')
        self.licenseDetailsLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.copyrightEdit)
        self.permissionsLabel = QtGui.QLabel(self.licenseDetailsPage)
        self.permissionsLabel.setObjectName(u'PermissionsLabel')
        self.licenseDetailsLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.permissionsLabel)
        self.permissionsEdit = QtGui.QLineEdit(self.licenseDetailsPage)
        self.permissionsEdit.setObjectName(u'PermissionsEdit')
        self.licenseDetailsLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.permissionsEdit)
        bibleImportWizard.addPage(self.licenseDetailsPage)
        # Progress Page
        self.importPage = QtGui.QWizardPage()
        self.importPage.setObjectName(u'ImportPage')
        self.importLayout = QtGui.QVBoxLayout(self.importPage)
        self.importLayout.setMargin(48)
        self.importLayout.setObjectName(u'ImportLayout')
        self.importProgressLabel = QtGui.QLabel(self.importPage)
        self.importProgressLabel.setObjectName(u'ImportProgressLabel')
        self.importLayout.addWidget(self.importProgressLabel)
        self.importProgressBar = QtGui.QProgressBar(self.importPage)
        self.importProgressBar.setObjectName(u'ImportProgressBar')
        self.importLayout.addWidget(self.importProgressBar)
        bibleImportWizard.addPage(self.importPage)
        self.retranslateUi(bibleImportWizard)
        QtCore.QMetaObject.connectSlotsByName(bibleImportWizard)
        QtCore.QObject.connect(self.formatComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'), self.selectStack,
            QtCore.SLOT(u'setCurrentIndex(int)'))

    def retranslateUi(self, bibleImportWizard):
        bibleImportWizard.setWindowTitle(
            translate('BiblesPlugin.ImportWizardForm', 'Bible Import Wizard'))
        self.titleLabel.setText(
            u'<span style="font-size:14pt; font-weight:600;">%s</span>' % \
            translate('BiblesPlugin.ImportWizardForm',
            'Welcome to the Bible Import Wizard'))
        self.informationLabel.setText(
            translate('BiblesPlugin.ImportWizardForm',
            'This wizard will help you to import Bibles from a '
            'variety of formats. Click the next button below to start the '
            'process by selecting a format to import from.'))
        self.selectPage.setTitle(translate('BiblesPlugin.ImportWizardForm',
            'Select Import Source'))
        self.selectPage.setSubTitle(
            translate('BiblesPlugin.ImportWizardForm',
            'Select the import format, and where to import from.'))
        self.formatLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Format:'))
        self.formatComboBox.setItemText(0,
            translate('BiblesPlugin.ImportWizardForm', 'OSIS'))
        self.formatComboBox.setItemText(1,
            translate('BiblesPlugin.ImportWizardForm', 'CSV'))
        self.formatComboBox.setItemText(2,
            translate('BiblesPlugin.ImportWizardForm', 'OpenSong'))
        self.formatComboBox.setItemText(3,
            translate('BiblesPlugin.ImportWizardForm', 'Web Download'))
        self.formatComboBox.setItemText(4,
            translate('BiblesPlugin.ImportWizardForm', 'openlp.org 1.x'))
        self.openlp1FileLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'File location:'))
        self.osisFileLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'File location:'))
        self.csvBooksLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Books location:'))
        self.csvVersesLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Verse location:'))
        self.openSongFileLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Bible filename:'))
        self.webSourceLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Location:'))
        self.webSourceComboBox.setItemText(0,
            translate('BiblesPlugin.ImportWizardForm', 'Crosswalk'))
        self.webSourceComboBox.setItemText(1,
            translate('BiblesPlugin.ImportWizardForm', 'BibleGateway'))
        self.webSourceComboBox.setItemText(2,
            translate('BiblesPlugin.ImportWizardForm', 'Bibleserver'))
        self.webTranslationLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Bible:'))
        self.webTabWidget.setTabText(
            self.webTabWidget.indexOf(self.webBibleTab),
            translate('BiblesPlugin.ImportWizardForm', 'Download Options'))
        self.webServerLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Server:'))
        self.webUserLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Username:'))
        self.webPasswordLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Password:'))
        self.webTabWidget.setTabText(
            self.webTabWidget.indexOf(self.webProxyTab),
            translate('BiblesPlugin.ImportWizardForm',
            'Proxy Server (Optional)'))
        self.licenseDetailsPage.setTitle(
            translate('BiblesPlugin.ImportWizardForm', 'License Details'))
        self.licenseDetailsPage.setSubTitle(
            translate('BiblesPlugin.ImportWizardForm',
            'Set up the Bible\'s license details.'))
        self.versionNameLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Version name:'))
        self.copyrightLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Copyright:'))
        self.permissionsLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Permissions:'))
        self.importPage.setTitle(
            translate('BiblesPlugin.ImportWizardForm', 'Importing'))
        self.importPage.setSubTitle(
            translate('BiblesPlugin.ImportWizardForm',
            'Please wait while your Bible is imported.'))
        self.importProgressLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Ready.'))
        self.importProgressBar.setFormat(u'%p%')
        self.openlp1DisabledLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'The openlp.org 1.x '
            'importer has been disabled due to a missing Python module. If '
            'you want to use this importer, you will need to install the '
            '"python-sqlite" module.'))
        # Align all QFormLayouts towards each other.
        width = max(self.formatLabel.minimumSizeHint().width(),
            self.osisFileLabel.minimumSizeHint().width())
        width = max(width, self.csvBooksLabel.minimumSizeHint().width())
        width = max(width, self.csvVersesLabel.minimumSizeHint().width())
        width = max(width, self.openSongFileLabel.minimumSizeHint().width())
        width = max(width, self.openlp1FileLabel.minimumSizeHint().width())
        self.formatSpacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        self.osisSpacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        self.csvSpacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        self.openSongSpacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        self.openlp1Spacer.changeSize(width, 0, QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
