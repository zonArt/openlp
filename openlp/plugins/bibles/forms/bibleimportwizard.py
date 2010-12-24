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
        self.welcomeLayout.setMargin(12)
        self.welcomeLayout.setSpacing(6)
        self.welcomeLayout.setObjectName(u'WelcomeLayout')
        self.titleLabel = QtGui.QLabel(self.welcomePage)
        self.titleLabel.setObjectName(u'TitleLabel')
        self.welcomeLayout.addWidget(self.titleLabel)
        self.welcomeTopSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.welcomeLayout.addItem(self.welcomeTopSpacer)
        self.informationLabel = QtGui.QLabel(self.welcomePage)
        self.informationLabel.setWordWrap(True)
        self.informationLabel.setObjectName(u'InformationLabel')
        self.welcomeLayout.addWidget(self.informationLabel)
        self.welcomeBottomSpacer = QtGui.QSpacerItem(20, 40,
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.welcomeLayout.addItem(self.welcomeBottomSpacer)
        bibleImportWizard.addPage(self.welcomePage)
        # Select page
        self.selectPage = QtGui.QWizardPage()
        self.selectPage.setObjectName(u'SelectPage')
        self.selectPageLayout = QtGui.QVBoxLayout(self.selectPage)
        self.selectPageLayout.setMargin(12)
        self.selectPageLayout.setObjectName(u'SelectPageLayout')
        self.selectFormLayout = QtGui.QFormLayout()
        self.selectFormLayout.setVerticalSpacing(6)
        self.selectFormLayout.setObjectName(u'SelectFormLayout')
        self.formatLabel = QtGui.QLabel(self.selectPage)
        self.formatLabel.setObjectName(u'FormatLabel')
        self.selectFormLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.formatLabel)
        self.formatComboBox = QtGui.QComboBox(self.selectPage)
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.addItem(u'')
        self.formatComboBox.setObjectName(u'FormatComboBox')
        self.selectFormLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.formatComboBox)
        self.osisFileLabel = QtGui.QLabel(self.selectPage)
        self.osisFileLabel.setObjectName(u'OsisFileLabel')
        self.selectFormLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.osisFileLabel)
        self.osisFileWidget = QtGui.QWidget(self.selectPage)
        self.osisFileWidget.setObjectName(u'OsisFileWidget')
        self.osisFileLayout = QtGui.QHBoxLayout(self.osisFileWidget)
        self.osisFileLayout.setMargin(0)
        self.osisFileLayout.setObjectName(u'OsisFileLayout')
        self.osisFileEdit = QtGui.QLineEdit(self.osisFileWidget)
        self.osisFileEdit.setObjectName(u'OsisFileEdit')
        self.osisFileLayout.addWidget(self.osisFileEdit)
        self.osisFileButton = QtGui.QToolButton(self.osisFileWidget)
        self.osisFileButton.setIcon(build_icon(u':/general/general_open.png'))
        self.osisFileButton.setObjectName(u'OsisFileButton')
        self.osisFileLayout.addWidget(self.osisFileButton)
        self.selectFormLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.osisFileWidget)
        self.csvBooksLabel = QtGui.QLabel(self.selectPage)
        self.csvBooksLabel.setVisible(False)
        self.csvBooksLabel.setObjectName(u'CsvBooksLabel')
        self.selectFormLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.csvBooksLabel)
        self.csvBooksWidget = QtGui.QWidget(self.selectPage)
        self.csvBooksWidget.setVisible(False)
        self.csvBooksWidget.setObjectName(u'CsvBooksWidget')
        self.csvBooksLayout = QtGui.QHBoxLayout(self.csvBooksWidget)
        self.csvBooksLayout.setMargin(0)
        self.csvBooksLayout.setObjectName(u'CsvBooksLayout')
        self.csvBooksEdit = QtGui.QLineEdit(self.csvBooksWidget)
        self.csvBooksEdit.setObjectName(u'CsvBooksEdit')
        self.csvBooksLayout.addWidget(self.csvBooksEdit)
        self.csvBooksButton = QtGui.QToolButton(self.csvBooksWidget)
        self.csvBooksButton.setIcon(build_icon(u':/general/general_open.png'))
        self.csvBooksButton.setObjectName(u'CsvBooksButton')
        self.csvBooksLayout.addWidget(self.csvBooksButton)
        self.selectFormLayout.setWidget(2, QtGui.QFormLayout.FieldRole,
            self.csvBooksWidget)
        self.csvVersesLabel = QtGui.QLabel(self.selectPage)
        self.csvVersesLabel.setVisible(False)
        self.csvVersesLabel.setObjectName(u'CsvVersesLabel')
        self.selectFormLayout.setWidget(3, QtGui.QFormLayout.LabelRole,
            self.csvVersesLabel)
        self.csvVersesWidget = QtGui.QWidget(self.selectPage)
        self.csvVersesWidget.setVisible(False)
        self.csvVersesWidget.setObjectName(u'CsvVersesWidget')
        self.csvVersesLayout = QtGui.QHBoxLayout(self.csvVersesWidget)
        self.csvVersesLayout.setMargin(0)
        self.csvVersesLayout.setObjectName(u'CsvVersesLayout')
        self.csvVersesEdit = QtGui.QLineEdit(self.csvVersesWidget)
        self.csvVersesEdit.setObjectName(u'CsvVersesEdit')
        self.csvVersesLayout.addWidget(self.csvVersesEdit)
        self.csvVersesButton = QtGui.QToolButton(self.csvVersesWidget)
        self.csvVersesButton.setIcon(build_icon(u':/general/general_open.png'))
        self.csvVersesButton.setObjectName(u'CsvVersesButton')
        self.csvVersesLayout.addWidget(self.csvVersesButton)
        self.selectFormLayout.setWidget(3, QtGui.QFormLayout.FieldRole,
            self.csvVersesWidget)
        self.openSongFileLabel = QtGui.QLabel(self.selectPage)
        self.openSongFileLabel.setVisible(False)
        self.openSongFileLabel.setObjectName(u'OpenSongFileLabel')
        self.selectFormLayout.setWidget(4, QtGui.QFormLayout.LabelRole,
            self.openSongFileLabel)
        self.openSongFileWidget = QtGui.QWidget(self.selectPage)
        self.openSongFileWidget.setVisible(False)
        self.openSongFileWidget.setObjectName(u'OpenSongFileWidget')
        self.openSongFileLayout = QtGui.QHBoxLayout(self.openSongFileWidget)
        self.openSongFileLayout.setMargin(0)
        self.openSongFileLayout.setObjectName(u'OpenSongFileLayout')
        self.openSongFileEdit = QtGui.QLineEdit(self.openSongFileWidget)
        self.openSongFileEdit.setObjectName(u'OpenSongFileEdit')
        self.openSongFileLayout.addWidget(self.openSongFileEdit)
        self.openSongFileButton = QtGui.QToolButton(self.openSongFileWidget)
        self.openSongFileButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.openSongFileButton.setObjectName(u'OpenSongFileButton')
        self.openSongFileLayout.addWidget(self.openSongFileButton)
        self.selectFormLayout.setWidget(4, QtGui.QFormLayout.FieldRole,
            self.openSongFileWidget)
        self.openlp1FileLabel = QtGui.QLabel(self.selectPage)
        self.openlp1FileLabel.setVisible(False)
        self.openlp1FileLabel.setObjectName(u'Openlp1FileLabel')
        self.selectFormLayout.setWidget(5, QtGui.QFormLayout.LabelRole,
            self.openlp1FileLabel)
        self.openlp1FileWidget = QtGui.QWidget(self.selectPage)
        self.openlp1FileWidget.setVisible(False)
        self.openlp1FileWidget.setObjectName(u'Openlp1FileWidget')
        self.openlp1FileLayout = QtGui.QHBoxLayout(self.openlp1FileWidget)
        self.openlp1FileLayout.setMargin(0)
        self.openlp1FileLayout.setObjectName(u'Openlp1FileLayout')
        self.openlp1FileEdit = QtGui.QLineEdit(self.openlp1FileWidget)
        self.openlp1FileEdit.setObjectName(u'Openlp1FileEdit')
        self.openlp1FileLayout.addWidget(self.openlp1FileEdit)
        self.openlp1FileButton = QtGui.QToolButton(self.openlp1FileWidget)
        self.openlp1FileButton.setIcon(
            build_icon(u':/general/general_open.png'))
        self.openlp1FileButton.setObjectName(u'Openlp1FileButton')
        self.openlp1FileLayout.addWidget(self.openlp1FileButton)
        self.selectFormLayout.setWidget(5, QtGui.QFormLayout.FieldRole,
            self.openlp1FileWidget)
        self.selectPageLayout.addItem(self.selectFormLayout)
        self.openlp1DisabledLabel = QtGui.QLabel(self.selectPage)
        self.openlp1DisabledLabel.setVisible(False)
        self.openlp1DisabledLabel.setObjectName(u'Openlp1DisabledLabel')
        self.selectPageLayout.addWidget(self.openlp1DisabledLabel)
        self.webTabWidget = QtGui.QTabWidget(self.selectPage)
        self.webTabWidget.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
            QtGui.QSizePolicy.MinimumExpanding)
        self.webTabWidget.setVisible(False)
        self.webTabWidget.setObjectName(u'WebTabWidget')
        self.webBibleTab = QtGui.QWidget()
        self.webBibleTab.setObjectName(u'WebBibleTab')
        self.webBibleLayout = QtGui.QFormLayout(self.webBibleTab)
        self.webBibleLayout.setVerticalSpacing(6)
        self.webBibleLayout.setObjectName(u'WebBibleLayout')
        self.webSourceLabel = QtGui.QLabel(self.webBibleTab)
        self.webSourceLabel.setObjectName(u'WebSourceLabel')
        self.webBibleLayout.setWidget(0, QtGui.QFormLayout.LabelRole,
            self.webSourceLabel)
        self.webSourceComboBox = QtGui.QComboBox(self.webBibleTab)
        self.webSourceComboBox.setObjectName(u'WebSourceComboBox')
        self.webSourceComboBox.addItem(u'')
        self.webSourceComboBox.addItem(u'')
        self.webSourceComboBox.addItem(u'')
        self.webBibleLayout.setWidget(0, QtGui.QFormLayout.FieldRole,
            self.webSourceComboBox)
        self.webTranslationLabel = QtGui.QLabel(self.webBibleTab)
        self.webTranslationLabel.setObjectName(u'webTranslationLabel')
        self.webBibleLayout.setWidget(1, QtGui.QFormLayout.LabelRole,
            self.webTranslationLabel)
        self.webTranslationComboBox = QtGui.QComboBox(self.webBibleTab)
        self.webTranslationComboBox.setObjectName(u'WebTranslationComboBox')
        self.webTranslationComboBox.addItem(u'')
        self.webTranslationComboBox.addItem(u'')
        self.webTranslationComboBox.addItem(u'')
        self.webBibleLayout.setWidget(1, QtGui.QFormLayout.FieldRole,
            self.webTranslationComboBox)
        self.webTabWidget.addTab(self.webBibleTab, u'')
        self.webProxyTab = QtGui.QWidget()
        self.webProxyTab.setObjectName(u'WebProxyTab')
        self.webProxyLayout = QtGui.QFormLayout(self.webProxyTab)
        self.webProxyLayout.setVerticalSpacing(6)
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
        self.selectPageLayout.addWidget(self.webTabWidget)
        bibleImportWizard.addPage(self.selectPage)
        # License page
        self.licenseDetailsPage = QtGui.QWizardPage()
        self.licenseDetailsPage.setObjectName(u'LicenseDetailsPage')
        self.licenseDetailsLayout = QtGui.QFormLayout(self.licenseDetailsPage)
        self.licenseDetailsLayout.setMargin(12)
        self.licenseDetailsLayout.setVerticalSpacing(6)
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
        self.importLayout.setSpacing(6)
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
        self.webTabWidget.setCurrentIndex(0)

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
