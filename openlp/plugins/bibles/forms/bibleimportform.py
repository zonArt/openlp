# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The bible import functions for OpenLP
"""
import logging
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Settings, UiStrings, translate
from openlp.core.lib.db import delete_database
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.wizard import OpenLPWizard, WizardStrings
from openlp.core.utils import AppLocation, locale_compare
from openlp.plugins.bibles.lib.manager import BibleFormat
from openlp.plugins.bibles.lib.db import BiblesResourcesDB, clean_filename

log = logging.getLogger(__name__)

class WebDownload(object):
    """
    Provides an enumeration for the web bible types available to OpenLP.
    """
    Unknown = -1
    Crosswalk = 0
    BibleGateway = 1
    Bibleserver = 2

    Names = [u'Crosswalk', u'BibleGateway', u'Bibleserver']


class BibleImportForm(OpenLPWizard):
    """
    This is the Bible Import Wizard, which allows easy importing of Bibles
    into OpenLP from other formats like OSIS, CSV and OpenSong.
    """
    log.info(u'BibleImportForm loaded')

    def __init__(self, parent, manager, bibleplugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``manager``
            The Bible manager.

        ``bibleplugin``
            The Bible plugin.
        """
        self.manager = manager
        self.web_bible_list = {}
        OpenLPWizard.__init__(self, parent, bibleplugin, u'bibleImportWizard', u':/wizards/wizard_importbible.bmp')

    def setupUi(self, image):
        """
        Set up the UI for the bible wizard.
        """
        OpenLPWizard.setupUi(self, image)
        QtCore.QObject.connect(self.formatComboBox,QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onCurrentIndexChanged)

    def onCurrentIndexChanged(self, index):
        """
        Called when the format combo box's index changed. We have to check if
        the import is available and accordingly to disable or enable the next
        button.
        """
        self.selectStack.setCurrentIndex(index)
        next_button = self.button(QtGui.QWizard.NextButton)
        next_button.setEnabled(BibleFormat.get_availability(index))

    def customInit(self):
        """
        Perform any custom initialisation for bible importing.
        """
        if BibleFormat.get_availability(BibleFormat.OpenLP1):
            self.openlp1DisabledLabel.hide()
        else:
            self.openlp1FileLabel.hide()
            self.openlp1FileEdit.hide()
            self.openlp1BrowseButton.hide()
        self.manager.set_process_dialog(self)
        self.loadWebBibles()
        self.restart()
        self.selectStack.setCurrentIndex(0)

    def customSignals(self):
        """
        Set up the signals used in the bible importer.
        """
        QtCore.QObject.connect(self.webSourceComboBox, QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onWebSourceComboBoxIndexChanged)
        QtCore.QObject.connect(self.osisBrowseButton, QtCore.SIGNAL(u'clicked()'),
            self.onOsisBrowseButtonClicked)
        QtCore.QObject.connect(self.csvBooksButton, QtCore.SIGNAL(u'clicked()'),
            self.onCsvBooksBrowseButtonClicked)
        QtCore.QObject.connect(self.csvVersesButton, QtCore.SIGNAL(u'clicked()'),
            self.onCsvVersesBrowseButtonClicked)
        QtCore.QObject.connect(self.openSongBrowseButton, QtCore.SIGNAL(u'clicked()'),
            self.onOpenSongBrowseButtonClicked)
        QtCore.QObject.connect(self.openlp1BrowseButton, QtCore.SIGNAL(u'clicked()'),
            self.onOpenlp1BrowseButtonClicked)

    def addCustomPages(self):
        """
        Add the bible import specific wizard pages.
        """
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
        self.spacer = QtGui.QSpacerItem(10, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.formatLayout.setItem(1, QtGui.QFormLayout.LabelRole, self.spacer)
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
        self.osisBrowseButton.setIcon(self.openIcon)
        self.osisBrowseButton.setObjectName(u'OsisBrowseButton')
        self.osisFileLayout.addWidget(self.osisBrowseButton)
        self.osisLayout.addRow(self.osisFileLabel, self.osisFileLayout)
        self.osisLayout.setItem(1, QtGui.QFormLayout.LabelRole, self.spacer)
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
        self.csvBooksButton.setIcon(self.openIcon)
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
        self.csvVersesButton.setIcon(self.openIcon)
        self.csvVersesButton.setObjectName(u'CsvVersesButton')
        self.csvVersesLayout.addWidget(self.csvVersesButton)
        self.csvLayout.addRow(self.csvVersesLabel, self.csvVersesLayout)
        self.csvLayout.setItem(3, QtGui.QFormLayout.LabelRole, self.spacer)
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
        self.openSongBrowseButton.setIcon(self.openIcon)
        self.openSongBrowseButton.setObjectName(u'OpenSongBrowseButton')
        self.openSongFileLayout.addWidget(self.openSongBrowseButton)
        self.openSongLayout.addRow(self.openSongFileLabel, self.openSongFileLayout)
        self.openSongLayout.setItem(1, QtGui.QFormLayout.LabelRole, self.spacer)
        self.selectStack.addWidget(self.openSongWidget)
        self.webTabWidget = QtGui.QTabWidget(self.selectPage)
        self.webTabWidget.setObjectName(u'WebTabWidget')
        self.webBibleTab = QtGui.QWidget()
        self.webBibleTab.setObjectName(u'WebBibleTab')
        self.webBibleLayout = QtGui.QFormLayout(self.webBibleTab)
        self.webBibleLayout.setObjectName(u'WebBibleLayout')
        self.webSourceLabel = QtGui.QLabel(self.webBibleTab)
        self.webSourceLabel.setObjectName(u'WebSourceLabel')
        self.webBibleLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.webSourceLabel)
        self.webSourceComboBox = QtGui.QComboBox(self.webBibleTab)
        self.webSourceComboBox.setObjectName(u'WebSourceComboBox')
        self.webSourceComboBox.addItems([u'', u'', u''])
        self.webBibleLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.webSourceComboBox)
        self.webTranslationLabel = QtGui.QLabel(self.webBibleTab)
        self.webTranslationLabel.setObjectName(u'webTranslationLabel')
        self.webBibleLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.webTranslationLabel)
        self.webTranslationComboBox = QtGui.QComboBox(self.webBibleTab)
        self.webTranslationComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.webTranslationComboBox.setObjectName(u'WebTranslationComboBox')
        self.webBibleLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.webTranslationComboBox)
        self.webTabWidget.addTab(self.webBibleTab, u'')
        self.webProxyTab = QtGui.QWidget()
        self.webProxyTab.setObjectName(u'WebProxyTab')
        self.webProxyLayout = QtGui.QFormLayout(self.webProxyTab)
        self.webProxyLayout.setObjectName(u'WebProxyLayout')
        self.webServerLabel = QtGui.QLabel(self.webProxyTab)
        self.webServerLabel.setObjectName(u'WebServerLabel')
        self.webProxyLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.webServerLabel)
        self.webServerEdit = QtGui.QLineEdit(self.webProxyTab)
        self.webServerEdit.setObjectName(u'WebServerEdit')
        self.webProxyLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.webServerEdit)
        self.webUserLabel = QtGui.QLabel(self.webProxyTab)
        self.webUserLabel.setObjectName(u'WebUserLabel')
        self.webProxyLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.webUserLabel)
        self.webUserEdit = QtGui.QLineEdit(self.webProxyTab)
        self.webUserEdit.setObjectName(u'WebUserEdit')
        self.webProxyLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.webUserEdit)
        self.webPasswordLabel = QtGui.QLabel(self.webProxyTab)
        self.webPasswordLabel.setObjectName(u'WebPasswordLabel')
        self.webProxyLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.webPasswordLabel)
        self.webPasswordEdit = QtGui.QLineEdit(self.webProxyTab)
        self.webPasswordEdit.setObjectName(u'WebPasswordEdit')
        self.webProxyLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.webPasswordEdit)
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
        self.openlp1BrowseButton.setIcon(self.openIcon)
        self.openlp1BrowseButton.setObjectName(u'Openlp1BrowseButton')
        self.openlp1FileLayout.addWidget(self.openlp1BrowseButton)
        self.openlp1Layout.addRow(self.openlp1FileLabel, self.openlp1FileLayout)
        self.openlp1DisabledLabel = QtGui.QLabel(self.openlp1Widget)
        self.openlp1DisabledLabel.setWordWrap(True)
        self.openlp1DisabledLabel.setObjectName(u'Openlp1DisabledLabel')
        self.openlp1Layout.addRow(self.openlp1DisabledLabel)
        self.openlp1Layout.setItem(1, QtGui.QFormLayout.LabelRole, self.spacer)
        self.selectStack.addWidget(self.openlp1Widget)
        self.selectPageLayout.addLayout(self.selectStack)
        self.addPage(self.selectPage)
        # License Page
        self.licenseDetailsPage = QtGui.QWizardPage()
        self.licenseDetailsPage.setObjectName(u'LicenseDetailsPage')
        self.licenseDetailsLayout = QtGui.QFormLayout(self.licenseDetailsPage)
        self.licenseDetailsLayout.setObjectName(u'LicenseDetailsLayout')
        self.versionNameLabel = QtGui.QLabel(self.licenseDetailsPage)
        self.versionNameLabel.setObjectName(u'VersionNameLabel')
        self.licenseDetailsLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.versionNameLabel)
        self.versionNameEdit = QtGui.QLineEdit(self.licenseDetailsPage)
        self.versionNameEdit.setObjectName(u'VersionNameEdit')
        self.licenseDetailsLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.versionNameEdit)
        self.copyrightLabel = QtGui.QLabel(self.licenseDetailsPage)
        self.copyrightLabel.setObjectName(u'CopyrightLabel')
        self.licenseDetailsLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.copyrightLabel)
        self.copyrightEdit = QtGui.QLineEdit(self.licenseDetailsPage)
        self.copyrightEdit.setObjectName(u'CopyrightEdit')
        self.licenseDetailsLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.copyrightEdit)
        self.permissionsLabel = QtGui.QLabel(self.licenseDetailsPage)
        self.permissionsLabel.setObjectName(u'PermissionsLabel')
        self.licenseDetailsLayout.setWidget(2, QtGui.QFormLayout.LabelRole,
            self.permissionsLabel)
        self.permissionsEdit = QtGui.QLineEdit(self.licenseDetailsPage)
        self.permissionsEdit.setObjectName(u'PermissionsEdit')
        self.licenseDetailsLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.permissionsEdit)
        self.addPage(self.licenseDetailsPage)

    def retranslateUi(self):
        """
        Allow for localisation of the bible import wizard.
        """
        self.setWindowTitle(translate('BiblesPlugin.ImportWizardForm', 'Bible Import Wizard'))
        self.titleLabel.setText(WizardStrings.HeaderStyle %
            translate('OpenLP.Ui', 'Welcome to the Bible Import Wizard'))
        self.informationLabel.setText(
            translate('BiblesPlugin.ImportWizardForm',
            'This wizard will help you to import Bibles from a variety of '
            'formats. Click the next button below to start the process by '
            'selecting a format to import from.'))
        self.selectPage.setTitle(WizardStrings.ImportSelect)
        self.selectPage.setSubTitle(WizardStrings.ImportSelectLong)
        self.formatLabel.setText(WizardStrings.FormatLabel)
        self.formatComboBox.setItemText(BibleFormat.OSIS, WizardStrings.OSIS)
        self.formatComboBox.setItemText(BibleFormat.CSV, WizardStrings.CSV)
        self.formatComboBox.setItemText(BibleFormat.OpenSong, WizardStrings.OS)
        self.formatComboBox.setItemText(BibleFormat.WebDownload,
            translate('BiblesPlugin.ImportWizardForm', 'Web Download'))
        self.formatComboBox.setItemText(BibleFormat.OpenLP1, UiStrings().OLPV1)
        self.openlp1FileLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Bible file:'))
        self.osisFileLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Bible file:'))
        self.csvBooksLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Books file:'))
        self.csvVersesLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Verses file:'))
        self.openSongFileLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Bible file:'))
        self.webSourceLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Location:'))
        self.webSourceComboBox.setItemText(WebDownload.Crosswalk,
            translate('BiblesPlugin.ImportWizardForm', 'Crosswalk'))
        self.webSourceComboBox.setItemText(WebDownload.BibleGateway,
            translate('BiblesPlugin.ImportWizardForm', 'BibleGateway'))
        self.webSourceComboBox.setItemText(WebDownload.Bibleserver,
            translate('BiblesPlugin.ImportWizardForm', 'Bibleserver'))
        self.webTranslationLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Bible:'))
        self.webTabWidget.setTabText(self.webTabWidget.indexOf(self.webBibleTab),
            translate('BiblesPlugin.ImportWizardForm', 'Download Options'))
        self.webServerLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Server:'))
        self.webUserLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Username:'))
        self.webPasswordLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Password:'))
        self.webTabWidget.setTabText(self.webTabWidget.indexOf(self.webProxyTab),
            translate('BiblesPlugin.ImportWizardForm',
            'Proxy Server (Optional)'))
        self.licenseDetailsPage.setTitle(
            translate('BiblesPlugin.ImportWizardForm', 'License Details'))
        self.licenseDetailsPage.setSubTitle(translate('BiblesPlugin.ImportWizardForm',
            'Set up the Bible\'s license details.'))
        self.versionNameLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Version name:'))
        self.copyrightLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Copyright:'))
        self.permissionsLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Permissions:'))
        self.progressPage.setTitle(WizardStrings.Importing)
        self.progressPage.setSubTitle(translate('BiblesPlugin.ImportWizardForm',
            'Please wait while your Bible is imported.'))
        self.progressLabel.setText(WizardStrings.Ready)
        self.progressBar.setFormat(u'%p%')
        self.openlp1DisabledLabel.setText(WizardStrings.NoSqlite)
        # Align all QFormLayouts towards each other.
        labelWidth = max(self.formatLabel.minimumSizeHint().width(),
            self.osisFileLabel.minimumSizeHint().width(),
            self.csvBooksLabel.minimumSizeHint().width(),
            self.csvVersesLabel.minimumSizeHint().width(),
            self.openSongFileLabel.minimumSizeHint().width(),
            self.openlp1FileLabel.minimumSizeHint().width())
        self.spacer.changeSize(labelWidth, 0, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        if self.currentPage() == self.welcomePage:
            return True
        elif self.currentPage() == self.selectPage:
            if self.field(u'source_format') == BibleFormat.OSIS:
                if not self.field(u'osis_location'):
                    critical_error_message_box(UiStrings().NFSs, WizardStrings.YouSpecifyFile % WizardStrings.OSIS)
                    self.osisFileEdit.setFocus()
                    return False
            elif self.field(u'source_format') == BibleFormat.CSV:
                if not self.field(u'csv_booksfile'):
                    critical_error_message_box(UiStrings().NFSs, translate('BiblesPlugin.ImportWizardForm',
                        'You need to specify a file with books of the Bible to use in the import.'))
                    self.csvBooksEdit.setFocus()
                    return False
                elif not self.field(u'csv_versefile'):
                    critical_error_message_box(UiStrings().NFSs,
                        translate('BiblesPlugin.ImportWizardForm',
                            'You need to specify a file of Bible verses to import.'))
                    self.csvVersesEdit.setFocus()
                    return False
            elif self.field(u'source_format') == BibleFormat.OpenSong:
                if not self.field(u'opensong_file'):
                    critical_error_message_box(UiStrings().NFSs, WizardStrings.YouSpecifyFile % WizardStrings.OS)
                    self.openSongFileEdit.setFocus()
                    return False
            elif self.field(u'source_format') == BibleFormat.WebDownload:
                self.versionNameEdit.setText(self.webTranslationComboBox.currentText())
                return True
            elif self.field(u'source_format') == BibleFormat.OpenLP1:
                if not self.field(u'openlp1_location'):
                    critical_error_message_box(UiStrings().NFSs, WizardStrings.YouSpecifyFile % UiStrings().OLPV1)
                    self.openlp1FileEdit.setFocus()
                    return False
            return True
        elif self.currentPage() == self.licenseDetailsPage:
            license_version = self.field(u'license_version')
            license_copyright = self.field(u'license_copyright')
            path = AppLocation.get_section_data_path(u'bibles')
            if not license_version:
                critical_error_message_box(UiStrings().EmptyField,
                    translate('BiblesPlugin.ImportWizardForm', 'You need to specify a version name for your Bible.'))
                self.versionNameEdit.setFocus()
                return False
            elif not license_copyright:
                critical_error_message_box(UiStrings().EmptyField,
                    translate('BiblesPlugin.ImportWizardForm', 'You need to set a copyright for your Bible. '
                        'Bibles in the Public Domain need to be marked as such.'))
                self.copyrightEdit.setFocus()
                return False
            elif self.manager.exists(license_version):
                critical_error_message_box(translate('BiblesPlugin.ImportWizardForm', 'Bible Exists'),
                    translate('BiblesPlugin.ImportWizardForm',
                        'This Bible already exists. Please import a different Bible or first delete the existing one.'))
                self.versionNameEdit.setFocus()
                return False
            elif os.path.exists(os.path.join(path, clean_filename(
                license_version))):
                critical_error_message_box(
                    translate('BiblesPlugin.ImportWizardForm', 'Bible Exists'),
                    translate('BiblesPlugin.ImportWizardForm', 'This Bible already exists. Please import '
                        'a different Bible or first delete the existing one.'))
                self.versionNameEdit.setFocus()
                return False
            return True
        if self.currentPage() == self.progressPage:
            return True

    def onWebSourceComboBoxIndexChanged(self, index):
        """
        Setup the list of Bibles when you select a different source on the web
        download page.

        ``index``
            The index of the combo box.
        """
        self.webTranslationComboBox.clear()
        bibles = self.web_bible_list[index].keys()
        bibles.sort(cmp=locale_compare)
        self.webTranslationComboBox.addItems(bibles)

    def onOsisBrowseButtonClicked(self):
        """
        Show the file open dialog for the OSIS file.
        """
        self.getFileName(WizardStrings.OpenTypeFile % WizardStrings.OSIS, self.osisFileEdit, u'last directory import')

    def onCsvBooksBrowseButtonClicked(self):
        """
        Show the file open dialog for the books CSV file.
        """
        self.getFileName(WizardStrings.OpenTypeFile % WizardStrings.CSV, self.csvBooksEdit, u'last directory import',
            u'%s (*.csv)' % translate('BiblesPlugin.ImportWizardForm', 'CSV File'))

    def onCsvVersesBrowseButtonClicked(self):
        """
        Show the file open dialog for the verses CSV file.
        """
        self.getFileName(WizardStrings.OpenTypeFile % WizardStrings.CSV, self.csvVersesEdit, u'last directory import',
            u'%s (*.csv)' % translate('BiblesPlugin.ImportWizardForm', 'CSV File'))

    def onOpenSongBrowseButtonClicked(self):
        """
        Show the file open dialog for the OpenSong file.
        """
        self.getFileName(WizardStrings.OpenTypeFile % WizardStrings.OS, self.openSongFileEdit, u'last directory import')

    def onOpenlp1BrowseButtonClicked(self):
        """
        Show the file open dialog for the openlp.org 1.x file.
        """
        self.getFileName(WizardStrings.OpenTypeFile % UiStrings().OLPV1, self.openlp1FileEdit, u'last directory import',
            u'%s (*.bible)' % translate('BiblesPlugin.ImportWizardForm', 'openlp.org 1.x Bible Files'))

    def registerFields(self):
        """
        Register the bible import wizard fields.
        """
        self.selectPage.registerField(u'source_format', self.formatComboBox)
        self.selectPage.registerField(u'osis_location', self.osisFileEdit)
        self.selectPage.registerField(u'csv_booksfile', self.csvBooksEdit)
        self.selectPage.registerField(u'csv_versefile', self.csvVersesEdit)
        self.selectPage.registerField(u'opensong_file', self.openSongFileEdit)
        self.selectPage.registerField(u'web_location', self.webSourceComboBox)
        self.selectPage.registerField(u'web_biblename', self.webTranslationComboBox)
        self.selectPage.registerField(u'proxy_server', self.webServerEdit)
        self.selectPage.registerField(u'proxy_username', self.webUserEdit)
        self.selectPage.registerField(u'proxy_password', self.webPasswordEdit)
        self.selectPage.registerField(u'openlp1_location', self.openlp1FileEdit)
        self.licenseDetailsPage.registerField(u'license_version', self.versionNameEdit)
        self.licenseDetailsPage.registerField(u'license_copyright', self.copyrightEdit)
        self.licenseDetailsPage.registerField(u'license_permissions', self.permissionsEdit)

    def setDefaults(self):
        """
        Set default values for the wizard pages.
        """
        settings = Settings()
        settings.beginGroup(self.plugin.settingsSection)
        self.restart()
        self.finishButton.setVisible(False)
        self.cancelButton.setVisible(True)
        self.setField(u'source_format', 0)
        self.setField(u'osis_location', '')
        self.setField(u'csv_booksfile', '')
        self.setField(u'csv_versefile', '')
        self.setField(u'opensong_file', '')
        self.setField(u'web_location', WebDownload.Crosswalk)
        self.setField(u'web_biblename', self.webTranslationComboBox.currentIndex())
        self.setField(u'proxy_server', settings.value(u'proxy address'))
        self.setField(u'proxy_username', settings.value(u'proxy username'))
        self.setField(u'proxy_password', settings.value(u'proxy password'))
        self.setField(u'openlp1_location', '')
        self.setField(u'license_version', self.versionNameEdit.text())
        self.setField(u'license_copyright', self.copyrightEdit.text())
        self.setField(u'license_permissions', self.permissionsEdit.text())
        self.onWebSourceComboBoxIndexChanged(WebDownload.Crosswalk)
        settings.endGroup()

    def loadWebBibles(self):
        """
        Load the lists of Crosswalk, BibleGateway and Bibleserver bibles.
        """
        # Load Crosswalk Bibles.
        self.loadBibleResource(WebDownload.Crosswalk)
        # Load BibleGateway Bibles.
        self.loadBibleResource(WebDownload.BibleGateway)
        # Load and Bibleserver Bibles.
        self.loadBibleResource(WebDownload.Bibleserver)

    def loadBibleResource(self, download_type):
        """
        Loads a web bible from bible_resources.sqlite.

        ``download_type``
            The WebDownload type e.g. bibleserver.
        """
        self.web_bible_list[download_type] = {}
        bibles = BiblesResourcesDB.get_webbibles(WebDownload.Names[download_type])
        for bible in bibles:
            version = bible[u'name']
            name = bible[u'abbreviation']
            self.web_bible_list[download_type][version] = name.strip()

    def preWizard(self):
        """
        Prepare the UI for the import.
        """
        OpenLPWizard.preWizard(self)
        bible_type = self.field(u'source_format')
        if bible_type == BibleFormat.WebDownload:
            self.progressLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Registering Bible...'))
        else:
            self.progressLabel.setText(WizardStrings.StartingImport)
        self.application.process_events()

    def performWizard(self):
        """
        Perform the actual import.
        """
        bible_type = self.field(u'source_format')
        license_version = self.field(u'license_version')
        license_copyright = self.field(u'license_copyright')
        license_permissions = self.field(u'license_permissions')
        importer = None
        if bible_type == BibleFormat.OSIS:
            # Import an OSIS bible.
            importer = self.manager.import_bible(BibleFormat.OSIS,
                name=license_version,
                filename=self.field(u'osis_location')
            )
        elif bible_type == BibleFormat.CSV:
            # Import a CSV bible.
            importer = self.manager.import_bible(BibleFormat.CSV,
                name=license_version,
                booksfile=self.field(u'csv_booksfile'),
                versefile=self.field(u'csv_versefile')
            )
        elif bible_type == BibleFormat.OpenSong:
            # Import an OpenSong bible.
            importer = self.manager.import_bible(BibleFormat.OpenSong,
                name=license_version,
                filename=self.field(u'opensong_file')
            )
        elif bible_type == BibleFormat.WebDownload:
            # Import a bible from the web.
            self.progressBar.setMaximum(1)
            download_location = self.field(u'web_location')
            bible_version = self.webTranslationComboBox.currentText()
            bible = self.web_bible_list[download_location][bible_version]
            importer = self.manager.import_bible(
                BibleFormat.WebDownload, name=license_version,
                download_source=WebDownload.Names[download_location],
                download_name=bible,
                proxy_server=self.field(u'proxy_server'),
                proxy_username=self.field(u'proxy_username'),
                proxy_password=self.field(u'proxy_password')
            )
        elif bible_type == BibleFormat.OpenLP1:
            # Import an openlp.org 1.x bible.
            importer = self.manager.import_bible(BibleFormat.OpenLP1,
                name=license_version,
                filename=self.field(u'openlp1_location')
            )
        if importer.do_import(license_version):
            self.manager.save_meta_data(license_version, license_version,
                license_copyright, license_permissions)
            self.manager.reload_bibles()
            if bible_type == BibleFormat.WebDownload:
                self.progressLabel.setText(
                    translate('BiblesPlugin.ImportWizardForm', 'Registered Bible. Please note, that verses will be '
                    'downloaded on\ndemand and thus an internet connection is required.'))
            else:
                self.progressLabel.setText(WizardStrings.FinishedImport)
        else:
            self.progressLabel.setText(translate('BiblesPlugin.ImportWizardForm', 'Your Bible import failed.'))
            del self.manager.db_cache[importer.name]
            delete_database(self.plugin.settingsSection, importer.file)
