# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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
        bibleImportWizard.resize(550, 386)
        bibleImportWizard.setModal(True)
        bibleImportWizard.setWizardStyle(QtGui.QWizard.ModernStyle)
        bibleImportWizard.setOptions(
            QtGui.QWizard.IndependentPages |
            QtGui.QWizard.NoBackButtonOnStartPage |
            QtGui.QWizard.NoBackButtonOnLastPage)
        # Welcome page
        self.welcomePage = QtGui.QWizardPage()
        self.welcomePage.setPixmap(QtGui.QWizard.WatermarkPixmap,
            QtGui.QPixmap(u':/wizards/wizard_importbible.bmp'))
        self.welcomePage.setObjectName(u'WelcomePage')
        self.welcomeLayout = QtGui.QVBoxLayout(self.welcomePage)
        self.welcomeLayout.setSpacing(8)
        self.welcomeLayout.setMargin(0)
        self.welcomeLayout.setObjectName(u'WelcomeLayout')
        self.titleLabel = QtGui.QLabel(self.welcomePage)
        self.titleLabel.setObjectName(u'TitleLabel')
        self.welcomeLayout.addWidget(self.titleLabel)
        spacerItem = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.welcomeLayout.addItem(spacerItem)
        self.informationLabel = QtGui.QLabel(self.welcomePage)
        self.informationLabel.setWordWrap(True)
        self.informationLabel.setMargin(10)
        self.informationLabel.setObjectName(u'InformationLabel')
        self.welcomeLayout.addWidget(self.informationLabel)
        spacerItem1 = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.welcomeLayout.addItem(spacerItem1)
        bibleImportWizard.addPage(self.welcomePage)
        # Select page
        self.selectPage = QtGui.QWizardPage()
        self.selectPage.setObjectName(u'SelectPage')
        self.selectPageLayout = QtGui.QVBoxLayout(self.selectPage)
        self.selectPageLayout.setSpacing(8)
        self.selectPageLayout.setMargin(20)
        self.selectPageLayout.setObjectName(u'selectPageLayout')
        self.formatSelectLayout = QtGui.QHBoxLayout()
        self.formatSelectLayout.setSpacing(8)
        self.formatSelectLayout.setObjectName(u'FormatSelectLayout')
        self.formatLabel = QtGui.QLabel(self.selectPage)
        self.formatLabel.setObjectName(u'FormatLabel')
        self.formatSelectLayout.addWidget(self.formatLabel)
        self.formatComboBox = QtGui.QComboBox(self.selectPage)
        self.formatComboBox.setObjectName(u'FormatComboBox')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatSelectLayout.addWidget(self.formatComboBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formatSelectLayout.addItem(spacerItem2)
        self.selectPageLayout.addLayout(self.formatSelectLayout)
        self.formatWidget = QtGui.QStackedWidget(self.selectPage)
        self.formatWidget.setObjectName(u'FormatWidget')
        generalIcon = build_icon(u':/general/general_open.png')
        self.osisPage = QtGui.QWidget()
        self.osisPage.setObjectName(u'OsisPage')
        self.osisLayout = QtGui.QFormLayout(self.osisPage)
        self.osisLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.osisLayout.setMargin(0)
        self.osisLayout.setSpacing(8)
        self.osisLayout.setObjectName(u'OsisLayout')
        self.osisLocationLabel = QtGui.QLabel(self.osisPage)
        self.osisLocationLabel.setObjectName(u'OsisLocationLabel')
        self.osisLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.osisLocationLabel)
        self.osisLocationLayout = QtGui.QHBoxLayout()
        self.osisLocationLayout.setSpacing(8)
        self.osisLocationLayout.setObjectName(u'OsisLocationLayout')
        self.OSISLocationEdit = QtGui.QLineEdit(self.osisPage)
        self.OSISLocationEdit.setObjectName(u'OSISLocationEdit')
        self.osisLocationLayout.addWidget(self.OSISLocationEdit)
        self.osisFileButton = QtGui.QToolButton(self.osisPage)
        self.osisFileButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.osisFileButton.setIcon(generalIcon)
        self.osisFileButton.setObjectName(u'OsisFileButton')
        self.osisLocationLayout.addWidget(self.osisFileButton)
        self.osisLayout.setLayout(1, QtGui.QFormLayout.FieldRole,
            self.osisLocationLayout)
        self.formatWidget.addWidget(self.osisPage)
        self.csvPage = QtGui.QWidget()
        self.csvPage.setObjectName(u'CsvPage')
        self.csvSourceLayout = QtGui.QFormLayout(self.csvPage)
        self.csvSourceLayout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.csvSourceLayout.setLabelAlignment(QtCore.Qt.AlignBottom |
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.csvSourceLayout.setFormAlignment(QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.csvSourceLayout.setMargin(0)
        self.csvSourceLayout.setSpacing(8)
        self.csvSourceLayout.setObjectName(u'CsvSourceLayout')
        self.booksLocationLabel = QtGui.QLabel(self.csvPage)
        self.booksLocationLabel.setObjectName(u'BooksLocationLabel')
        self.csvSourceLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.booksLocationLabel)
        self.csvBooksLayout = QtGui.QHBoxLayout()
        self.csvBooksLayout.setSpacing(8)
        self.csvBooksLayout.setObjectName(u'CsvBooksLayout')
        self.booksLocationEdit = QtGui.QLineEdit(self.csvPage)
        self.booksLocationEdit.setObjectName(u'BooksLocationEdit')
        self.csvBooksLayout.addWidget(self.booksLocationEdit)
        self.booksFileButton = QtGui.QToolButton(self.csvPage)
        self.booksFileButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.booksFileButton.setIcon(generalIcon)
        self.booksFileButton.setObjectName(u'BooksFileButton')
        self.csvBooksLayout.addWidget(self.booksFileButton)
        self.csvSourceLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.csvBooksLayout)
        self.verseLocationLabel = QtGui.QLabel(self.csvPage)
        self.verseLocationLabel.setObjectName(u'VerseLocationLabel')
        self.csvSourceLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.verseLocationLabel)
        self.csvVerseLayout = QtGui.QHBoxLayout()
        self.csvVerseLayout.setSpacing(8)
        self.csvVerseLayout.setObjectName(u'CsvVerseLayout')
        self.csvVerseLocationEdit = QtGui.QLineEdit(self.csvPage)
        self.csvVerseLocationEdit.setObjectName(u'CsvVerseLocationEdit')
        self.csvVerseLayout.addWidget(self.csvVerseLocationEdit)
        self.csvVersesFileButton = QtGui.QToolButton(self.csvPage)
        self.csvVersesFileButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.csvVersesFileButton.setIcon(generalIcon)
        self.csvVersesFileButton.setObjectName(u'CsvVersesFileButton')
        self.csvVerseLayout.addWidget(self.csvVersesFileButton)
        self.csvSourceLayout.setLayout(1, QtGui.QFormLayout.FieldRole,
            self.csvVerseLayout)
        self.formatWidget.addWidget(self.csvPage)
        self.openSongPage = QtGui.QWidget()
        self.openSongPage.setObjectName(u'OpenSongPage')
        self.openSongLayout = QtGui.QFormLayout(self.openSongPage)
        self.openSongLayout.setMargin(0)
        self.openSongLayout.setSpacing(8)
        self.openSongLayout.setObjectName(u'OpenSongLayout')
        self.openSongFileLabel = QtGui.QLabel(self.openSongPage)
        self.openSongFileLabel.setObjectName(u'OpenSongFileLabel')
        self.openSongLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.openSongFileLabel)
        self.openSongFileLayout = QtGui.QHBoxLayout()
        self.openSongFileLayout.setSpacing(8)
        self.openSongFileLayout.setObjectName(u'OpenSongFileLayout')
        self.openSongFileEdit = QtGui.QLineEdit(self.openSongPage)
        self.openSongFileEdit.setObjectName(u'OpenSongFileEdit')
        self.openSongFileLayout.addWidget(self.openSongFileEdit)
        self.openSongBrowseButton = QtGui.QToolButton(self.openSongPage)
        self.openSongBrowseButton.setIcon(generalIcon)
        self.openSongBrowseButton.setObjectName(u'OpenSongBrowseButton')
        self.openSongFileLayout.addWidget(self.openSongBrowseButton)
        self.openSongLayout.setLayout(0, QtGui.QFormLayout.FieldRole,
            self.openSongFileLayout)
        self.formatWidget.addWidget(self.openSongPage)
        self.webDownloadPage = QtGui.QWidget()
        self.webDownloadPage.setObjectName(u'WebDownloadPage')
        self.webDownloadLayout = QtGui.QVBoxLayout(self.webDownloadPage)
        self.webDownloadLayout.setSpacing(8)
        self.webDownloadLayout.setMargin(0)
        self.webDownloadLayout.setObjectName(u'WebDownloadLayout')
        self.webDownloadTabWidget = QtGui.QTabWidget(self.webDownloadPage)
        self.webDownloadTabWidget.setObjectName(u'WebDownloadTabWidget')
        self.downloadOptionsTab = QtGui.QWidget()
        self.downloadOptionsTab.setObjectName(u'DownloadOptionsTab')
        self.downloadOptionsLayout = QtGui.QFormLayout(self.downloadOptionsTab)
        self.downloadOptionsLayout.setMargin(8)
        self.downloadOptionsLayout.setSpacing(8)
        self.downloadOptionsLayout.setObjectName(u'DownloadOptionsLayout')
        self.locationLabel = QtGui.QLabel(self.downloadOptionsTab)
        self.locationLabel.setObjectName(u'LocationLabel')
        self.downloadOptionsLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.locationLabel)
        self.locationComboBox = QtGui.QComboBox(self.downloadOptionsTab)
        self.locationComboBox.setObjectName(u'LocationComboBox')
        self.locationComboBox.addItem(u'')
        self.locationComboBox.addItem(u'')
        self.downloadOptionsLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.locationComboBox)
        self.bibleLabel = QtGui.QLabel(self.downloadOptionsTab)
        self.bibleLabel.setObjectName(u'BibleLabel')
        self.downloadOptionsLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.bibleLabel)
        self.bibleComboBox = QtGui.QComboBox(self.downloadOptionsTab)
        self.bibleComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.bibleComboBox.setObjectName(u'BibleComboBox')
        self.bibleComboBox.addItem(u'')
        self.bibleComboBox.addItem(u'')
        self.bibleComboBox.addItem(u'')
        self.downloadOptionsLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.bibleComboBox)
        self.webDownloadTabWidget.addTab(self.downloadOptionsTab, u'')
        self.proxyServerTab = QtGui.QWidget()
        self.proxyServerTab.setObjectName(u'ProxyServerTab')
        self.proxyServerLayout = QtGui.QFormLayout(self.proxyServerTab)
        self.proxyServerLayout.setObjectName(u'ProxyServerLayout')
        self.addressLabel = QtGui.QLabel(self.proxyServerTab)
        self.addressLabel.setObjectName(u'AddressLabel')
        self.proxyServerLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.addressLabel)
        self.addressEdit = QtGui.QLineEdit(self.proxyServerTab)
        self.addressEdit.setObjectName(u'AddressEdit')
        self.proxyServerLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.addressEdit)
        self.usernameLabel = QtGui.QLabel(self.proxyServerTab)
        self.usernameLabel.setObjectName(u'UsernameLabel')
        self.proxyServerLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.usernameLabel)
        self.usernameEdit = QtGui.QLineEdit(self.proxyServerTab)
        self.usernameEdit.setObjectName(u'UsernameEdit')
        self.proxyServerLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.usernameEdit)
        self.passwordLabel = QtGui.QLabel(self.proxyServerTab)
        self.passwordLabel.setObjectName(u'PasswordLabel')
        self.proxyServerLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.passwordLabel)
        self.passwordEdit = QtGui.QLineEdit(self.proxyServerTab)
        self.passwordEdit.setObjectName(u'PasswordEdit')
        self.proxyServerLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.passwordEdit)
        self.webDownloadTabWidget.addTab(self.proxyServerTab, u'')
        self.webDownloadLayout.addWidget(self.webDownloadTabWidget)
        self.formatWidget.addWidget(self.webDownloadPage)
        self.openlp1Page = QtGui.QWidget()
        self.openlp1Page.setObjectName(u'Openlp1Page')
        self.openlp1Layout = QtGui.QFormLayout(self.openlp1Page)
        self.openlp1Layout.setFieldGrowthPolicy(
            QtGui.QFormLayout.ExpandingFieldsGrow)
        self.openlp1Layout.setMargin(0)
        self.openlp1Layout.setSpacing(8)
        self.openlp1Layout.setObjectName(u'Openlp1Layout')
        self.openlp1LocationLabel = QtGui.QLabel(self.openlp1Page)
        self.openlp1LocationLabel.setObjectName(u'Openlp1LocationLabel')
        self.openlp1Layout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.openlp1LocationLabel)
        self.openlp1LocationLayout = QtGui.QHBoxLayout()
        self.openlp1LocationLayout.setSpacing(8)
        self.openlp1LocationLayout.setObjectName(u'Openlp1LocationLayout')
        self.openlp1LocationEdit = QtGui.QLineEdit(self.openlp1Page)
        self.openlp1LocationEdit.setObjectName(u'Openlp1LocationEdit')
        self.openlp1LocationLayout.addWidget(self.openlp1LocationEdit)
        self.openlp1FileButton = QtGui.QToolButton(self.openlp1Page)
        self.openlp1FileButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.openlp1FileButton.setIcon(generalIcon)
        self.openlp1FileButton.setObjectName(u'Openlp1FileButton')
        self.openlp1LocationLayout.addWidget(self.openlp1FileButton)
        self.openlp1Layout.setLayout(1, QtGui.QFormLayout.FieldRole,
            self.openlp1LocationLayout)
        self.formatWidget.addWidget(self.openlp1Page)
        self.selectPageLayout.addWidget(self.formatWidget)
        bibleImportWizard.addPage(self.selectPage)
        # License page
        self.licenseDetailsPage = QtGui.QWizardPage()
        self.licenseDetailsPage.setObjectName(u'LicenseDetailsPage')
        self.licenseDetailsLayout = QtGui.QFormLayout(self.licenseDetailsPage)
        self.licenseDetailsLayout.setMargin(20)
        self.licenseDetailsLayout.setSpacing(8)
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
        # Progress page
        self.importPage = QtGui.QWizardPage()
        self.importPage.setObjectName(u'ImportPage')
        self.importLayout = QtGui.QVBoxLayout(self.importPage)
        self.importLayout.setSpacing(8)
        self.importLayout.setMargin(50)
        self.importLayout.setObjectName(u'ImportLayout')
        self.importProgressLabel = QtGui.QLabel(self.importPage)
        self.importProgressLabel.setObjectName(u'ImportProgressLabel')
        self.importLayout.addWidget(self.importProgressLabel)
        self.importProgressBar = QtGui.QProgressBar(self.importPage)
        self.importProgressBar.setValue(0)
        self.importProgressBar.setObjectName(u'ImportProgressBar')
        self.importLayout.addWidget(self.importProgressBar)
        bibleImportWizard.addPage(self.importPage)

        self.retranslateUi(bibleImportWizard)
        self.formatWidget.setCurrentIndex(0)
        self.webDownloadTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.formatComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.formatWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(bibleImportWizard)

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
        self.openlp1LocationLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'File location:'))
        self.osisLocationLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'File location:'))
        self.booksLocationLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Books location:'))
        self.verseLocationLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Verse location:'))
        self.openSongFileLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Bible filename:'))
        self.locationLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Location:'))
        self.locationComboBox.setItemText(0,
            translate('BiblesPlugin.ImportWizardForm', 'Crosswalk'))
        self.locationComboBox.setItemText(1,
            translate('BiblesPlugin.ImportWizardForm', 'BibleGateway'))
        self.bibleLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Bible:'))
        self.webDownloadTabWidget.setTabText(
            self.webDownloadTabWidget.indexOf(self.downloadOptionsTab),
            translate('BiblesPlugin.ImportWizardForm', 'Download Options'))
        self.addressLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Server:'))
        self.usernameLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Username:'))
        self.passwordLabel.setText(
            translate('BiblesPlugin.ImportWizardForm', 'Password:'))
        self.webDownloadTabWidget.setTabText(
            self.webDownloadTabWidget.indexOf(self.proxyServerTab),
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
