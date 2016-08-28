# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
import urllib.error
from lxml import etree

from PyQt5 import QtWidgets
try:
    from pysword import modules
    PYSWORD_AVAILABLE = True
except:
    PYSWORD_AVAILABLE = False

from openlp.core.common import AppLocation, Settings, UiStrings, trace_error_handler, translate
from openlp.core.common.languagemanager import get_locale_key
from openlp.core.lib.db import delete_database
from openlp.core.lib.exceptions import ValidationError
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui.lib.wizard import OpenLPWizard, WizardStrings
from openlp.plugins.bibles.lib.db import clean_filename
from openlp.plugins.bibles.lib.importers.http import CWExtract, BGExtract, BSExtract
from openlp.plugins.bibles.lib.manager import BibleFormat

log = logging.getLogger(__name__)


class WebDownload(object):
    """
    Provides an enumeration for the web bible types available to OpenLP.
    """
    Unknown = -1
    Crosswalk = 0
    BibleGateway = 1
    Bibleserver = 2

    Names = ['Crosswalk', 'BibleGateway', 'Bibleserver']


class BibleImportForm(OpenLPWizard):
    """
    This is the Bible Import Wizard, which allows easy importing of Bibles into OpenLP from other formats like OSIS,
    CSV and OpenSong.
    """
    log.info('BibleImportForm loaded')

    def __init__(self, parent, manager, bible_plugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        :param parent: The QWidget-derived parent of the wizard.
        :param manager: The Bible manager.
        :param bible_plugin: The Bible plugin.
        """
        self.manager = manager
        self.web_bible_list = {}
        super(BibleImportForm, self).__init__(parent, bible_plugin,
                                              'bibleImportWizard', ':/wizards/wizard_importbible.bmp')

    def setupUi(self, image):
        """
        Set up the UI for the bible wizard.
        """
        super(BibleImportForm, self).setupUi(image)
        self.format_combo_box.currentIndexChanged.connect(self.on_current_index_changed)

    def on_current_index_changed(self, index):
        """
        Called when the format combo box's index changed. We have to check if
        the import is available and accordingly to disable or enable the next
        button.
        """
        self.select_stack.setCurrentIndex(index)

    def custom_init(self):
        """
        Perform any custom initialisation for bible importing.
        """
        self.manager.set_process_dialog(self)
        self.restart()
        self.select_stack.setCurrentIndex(0)
        if PYSWORD_AVAILABLE:
            self.pysword_folder_modules = modules.SwordModules()
            try:
                self.pysword_folder_modules_json = self.pysword_folder_modules.parse_modules()
            except FileNotFoundError:
                log.debug('No installed SWORD modules found in the default location')
                self.sword_bible_combo_box.clear()
                return
            bible_keys = self.pysword_folder_modules_json.keys()
            for key in bible_keys:
                self.sword_bible_combo_box.addItem(self.pysword_folder_modules_json[key]['description'], key)
        else:
            self.sword_tab_widget.setDisabled(True)

    def custom_signals(self):
        """
        Set up the signals used in the bible importer.
        """
        self.web_source_combo_box.currentIndexChanged.connect(self.on_web_source_combo_box_index_changed)
        self.osis_browse_button.clicked.connect(self.on_osis_browse_button_clicked)
        self.csv_books_button.clicked.connect(self.on_csv_books_browse_button_clicked)
        self.csv_verses_button.clicked.connect(self.on_csv_verses_browse_button_clicked)
        self.open_song_browse_button.clicked.connect(self.on_open_song_browse_button_clicked)
        self.zefania_browse_button.clicked.connect(self.on_zefania_browse_button_clicked)
        self.web_update_button.clicked.connect(self.on_web_update_button_clicked)
        self.sword_browse_button.clicked.connect(self.on_sword_browse_button_clicked)
        self.sword_zipbrowse_button.clicked.connect(self.on_sword_zipbrowse_button_clicked)

    def add_custom_pages(self):
        """
        Add the bible import specific wizard pages.
        """
        # Select Page
        self.select_page = QtWidgets.QWizardPage()
        self.select_page.setObjectName('SelectPage')
        self.select_page_layout = QtWidgets.QVBoxLayout(self.select_page)
        self.select_page_layout.setObjectName('SelectPageLayout')
        self.format_layout = QtWidgets.QFormLayout()
        self.format_layout.setObjectName('FormatLayout')
        self.format_label = QtWidgets.QLabel(self.select_page)
        self.format_label.setObjectName('FormatLabel')
        self.format_combo_box = QtWidgets.QComboBox(self.select_page)
        self.format_combo_box.addItems(['', '', '', '', '', ''])
        self.format_combo_box.setObjectName('FormatComboBox')
        self.format_layout.addRow(self.format_label, self.format_combo_box)
        self.spacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.format_layout.setItem(1, QtWidgets.QFormLayout.LabelRole, self.spacer)
        self.select_page_layout.addLayout(self.format_layout)
        self.select_stack = QtWidgets.QStackedLayout()
        self.select_stack.setObjectName('SelectStack')
        self.osis_widget = QtWidgets.QWidget(self.select_page)
        self.osis_widget.setObjectName('OsisWidget')
        self.osis_layout = QtWidgets.QFormLayout(self.osis_widget)
        self.osis_layout.setContentsMargins(0, 0, 0, 0)
        self.osis_layout.setObjectName('OsisLayout')
        self.osis_file_label = QtWidgets.QLabel(self.osis_widget)
        self.osis_file_label.setObjectName('OsisFileLabel')
        self.osis_file_layout = QtWidgets.QHBoxLayout()
        self.osis_file_layout.setObjectName('OsisFileLayout')
        self.osis_file_edit = QtWidgets.QLineEdit(self.osis_widget)
        self.osis_file_edit.setObjectName('OsisFileEdit')
        self.osis_file_layout.addWidget(self.osis_file_edit)
        self.osis_browse_button = QtWidgets.QToolButton(self.osis_widget)
        self.osis_browse_button.setIcon(self.open_icon)
        self.osis_browse_button.setObjectName('OsisBrowseButton')
        self.osis_file_layout.addWidget(self.osis_browse_button)
        self.osis_layout.addRow(self.osis_file_label, self.osis_file_layout)
        self.osis_layout.setItem(1, QtWidgets.QFormLayout.LabelRole, self.spacer)
        self.select_stack.addWidget(self.osis_widget)
        self.csv_widget = QtWidgets.QWidget(self.select_page)
        self.csv_widget.setObjectName('CsvWidget')
        self.csv_layout = QtWidgets.QFormLayout(self.csv_widget)
        self.csv_layout.setContentsMargins(0, 0, 0, 0)
        self.csv_layout.setObjectName('CsvLayout')
        self.csv_books_label = QtWidgets.QLabel(self.csv_widget)
        self.csv_books_label.setObjectName('CsvBooksLabel')
        self.csv_books_layout = QtWidgets.QHBoxLayout()
        self.csv_books_layout.setObjectName('CsvBooksLayout')
        self.csv_books_edit = QtWidgets.QLineEdit(self.csv_widget)
        self.csv_books_edit.setObjectName('CsvBooksEdit')
        self.csv_books_layout.addWidget(self.csv_books_edit)
        self.csv_books_button = QtWidgets.QToolButton(self.csv_widget)
        self.csv_books_button.setIcon(self.open_icon)
        self.csv_books_button.setObjectName('CsvBooksButton')
        self.csv_books_layout.addWidget(self.csv_books_button)
        self.csv_layout.addRow(self.csv_books_label, self.csv_books_layout)
        self.csv_verses_label = QtWidgets.QLabel(self.csv_widget)
        self.csv_verses_label.setObjectName('CsvVersesLabel')
        self.csv_verses_layout = QtWidgets.QHBoxLayout()
        self.csv_verses_layout.setObjectName('CsvVersesLayout')
        self.csv_verses_edit = QtWidgets.QLineEdit(self.csv_widget)
        self.csv_verses_edit.setObjectName('CsvVersesEdit')
        self.csv_verses_layout.addWidget(self.csv_verses_edit)
        self.csv_verses_button = QtWidgets.QToolButton(self.csv_widget)
        self.csv_verses_button.setIcon(self.open_icon)
        self.csv_verses_button.setObjectName('CsvVersesButton')
        self.csv_verses_layout.addWidget(self.csv_verses_button)
        self.csv_layout.addRow(self.csv_verses_label, self.csv_verses_layout)
        self.csv_layout.setItem(3, QtWidgets.QFormLayout.LabelRole, self.spacer)
        self.select_stack.addWidget(self.csv_widget)
        self.open_song_widget = QtWidgets.QWidget(self.select_page)
        self.open_song_widget.setObjectName('OpenSongWidget')
        self.open_song_layout = QtWidgets.QFormLayout(self.open_song_widget)
        self.open_song_layout.setContentsMargins(0, 0, 0, 0)
        self.open_song_layout.setObjectName('OpenSongLayout')
        self.open_song_file_label = QtWidgets.QLabel(self.open_song_widget)
        self.open_song_file_label.setObjectName('OpenSongFileLabel')
        self.open_song_file_layout = QtWidgets.QHBoxLayout()
        self.open_song_file_layout.setObjectName('OpenSongFileLayout')
        self.open_song_file_edit = QtWidgets.QLineEdit(self.open_song_widget)
        self.open_song_file_edit.setObjectName('OpenSongFileEdit')
        self.open_song_file_layout.addWidget(self.open_song_file_edit)
        self.open_song_browse_button = QtWidgets.QToolButton(self.open_song_widget)
        self.open_song_browse_button.setIcon(self.open_icon)
        self.open_song_browse_button.setObjectName('OpenSongBrowseButton')
        self.open_song_file_layout.addWidget(self.open_song_browse_button)
        self.open_song_layout.addRow(self.open_song_file_label, self.open_song_file_layout)
        self.open_song_layout.setItem(1, QtWidgets.QFormLayout.LabelRole, self.spacer)
        self.select_stack.addWidget(self.open_song_widget)
        self.web_tab_widget = QtWidgets.QTabWidget(self.select_page)
        self.web_tab_widget.setObjectName('WebTabWidget')
        self.web_bible_tab = QtWidgets.QWidget()
        self.web_bible_tab.setObjectName('WebBibleTab')
        self.web_bible_layout = QtWidgets.QFormLayout(self.web_bible_tab)
        self.web_bible_layout.setObjectName('WebBibleLayout')
        self.web_update_label = QtWidgets.QLabel(self.web_bible_tab)
        self.web_update_label.setObjectName('WebUpdateLabel')
        self.web_bible_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.web_update_label)
        self.web_update_button = QtWidgets.QPushButton(self.web_bible_tab)
        self.web_update_button.setObjectName('WebUpdateButton')
        self.web_bible_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.web_update_button)
        self.web_source_label = QtWidgets.QLabel(self.web_bible_tab)
        self.web_source_label.setObjectName('WebSourceLabel')
        self.web_bible_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.web_source_label)
        self.web_source_combo_box = QtWidgets.QComboBox(self.web_bible_tab)
        self.web_source_combo_box.setObjectName('WebSourceComboBox')
        self.web_source_combo_box.addItems(['', '', ''])
        self.web_source_combo_box.setEnabled(False)
        self.web_bible_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.web_source_combo_box)
        self.web_translation_label = QtWidgets.QLabel(self.web_bible_tab)
        self.web_translation_label.setObjectName('web_translation_label')
        self.web_bible_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.web_translation_label)
        self.web_translation_combo_box = QtWidgets.QComboBox(self.web_bible_tab)
        self.web_translation_combo_box.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.web_translation_combo_box.setObjectName('WebTranslationComboBox')
        self.web_translation_combo_box.setEnabled(False)
        self.web_bible_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.web_translation_combo_box)
        self.web_progress_bar = QtWidgets.QProgressBar(self)
        self.web_progress_bar.setRange(0, 3)
        self.web_progress_bar.setObjectName('WebTranslationProgressBar')
        self.web_progress_bar.setVisible(False)
        self.web_bible_layout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.web_progress_bar)
        self.web_tab_widget.addTab(self.web_bible_tab, '')
        self.web_proxy_tab = QtWidgets.QWidget()
        self.web_proxy_tab.setObjectName('WebProxyTab')
        self.web_proxy_layout = QtWidgets.QFormLayout(self.web_proxy_tab)
        self.web_proxy_layout.setObjectName('WebProxyLayout')
        self.web_server_label = QtWidgets.QLabel(self.web_proxy_tab)
        self.web_server_label.setObjectName('WebServerLabel')
        self.web_proxy_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.web_server_label)
        self.web_server_edit = QtWidgets.QLineEdit(self.web_proxy_tab)
        self.web_server_edit.setObjectName('WebServerEdit')
        self.web_proxy_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.web_server_edit)
        self.web_user_label = QtWidgets.QLabel(self.web_proxy_tab)
        self.web_user_label.setObjectName('WebUserLabel')
        self.web_proxy_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.web_user_label)
        self.web_user_edit = QtWidgets.QLineEdit(self.web_proxy_tab)
        self.web_user_edit.setObjectName('WebUserEdit')
        self.web_proxy_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.web_user_edit)
        self.web_password_label = QtWidgets.QLabel(self.web_proxy_tab)
        self.web_password_label.setObjectName('WebPasswordLabel')
        self.web_proxy_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.web_password_label)
        self.web_password_edit = QtWidgets.QLineEdit(self.web_proxy_tab)
        self.web_password_edit.setObjectName('WebPasswordEdit')
        self.web_proxy_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.web_password_edit)
        self.web_tab_widget.addTab(self.web_proxy_tab, '')
        self.select_stack.addWidget(self.web_tab_widget)
        self.zefania_widget = QtWidgets.QWidget(self.select_page)
        self.zefania_widget.setObjectName('ZefaniaWidget')
        self.zefania_layout = QtWidgets.QFormLayout(self.zefania_widget)
        self.zefania_layout.setContentsMargins(0, 0, 0, 0)
        self.zefania_layout.setObjectName('ZefaniaLayout')
        self.zefania_file_label = QtWidgets.QLabel(self.zefania_widget)
        self.zefania_file_label.setObjectName('ZefaniaFileLabel')
        self.zefania_file_layout = QtWidgets.QHBoxLayout()
        self.zefania_file_layout.setObjectName('ZefaniaFileLayout')
        self.zefania_file_edit = QtWidgets.QLineEdit(self.zefania_widget)
        self.zefania_file_edit.setObjectName('ZefaniaFileEdit')
        self.zefania_file_layout.addWidget(self.zefania_file_edit)
        self.zefania_browse_button = QtWidgets.QToolButton(self.zefania_widget)
        self.zefania_browse_button.setIcon(self.open_icon)
        self.zefania_browse_button.setObjectName('ZefaniaBrowseButton')
        self.zefania_file_layout.addWidget(self.zefania_browse_button)
        self.zefania_layout.addRow(self.zefania_file_label, self.zefania_file_layout)
        self.zefania_layout.setItem(5, QtWidgets.QFormLayout.LabelRole, self.spacer)
        self.select_stack.addWidget(self.zefania_widget)
        self.sword_widget = QtWidgets.QWidget(self.select_page)
        self.sword_widget.setObjectName('SwordWidget')
        self.sword_layout = QtWidgets.QVBoxLayout(self.sword_widget)
        self.sword_layout.setObjectName('SwordLayout')
        self.sword_tab_widget = QtWidgets.QTabWidget(self.sword_widget)
        self.sword_tab_widget.setObjectName('SwordTabWidget')
        self.sword_folder_tab = QtWidgets.QWidget(self.sword_tab_widget)
        self.sword_folder_tab.setObjectName('SwordFolderTab')
        self.sword_folder_tab_layout = QtWidgets.QGridLayout(self.sword_folder_tab)
        self.sword_folder_tab_layout.setObjectName('SwordTabFolderLayout')
        self.sword_folder_label = QtWidgets.QLabel(self.sword_folder_tab)
        self.sword_folder_label.setObjectName('SwordSourceLabel')
        self.sword_folder_tab_layout.addWidget(self.sword_folder_label, 0, 0)
        self.sword_folder_label.setObjectName('SwordFolderLabel')
        self.sword_folder_edit = QtWidgets.QLineEdit(self.sword_folder_tab)
        self.sword_folder_edit.setObjectName('SwordFolderEdit')
        self.sword_browse_button = QtWidgets.QToolButton(self.sword_folder_tab)
        self.sword_browse_button.setIcon(self.open_icon)
        self.sword_browse_button.setObjectName('SwordBrowseButton')
        self.sword_folder_tab_layout.addWidget(self.sword_folder_edit, 0, 1)
        self.sword_folder_tab_layout.addWidget(self.sword_browse_button, 0, 2)
        self.sword_bible_label = QtWidgets.QLabel(self.sword_folder_tab)
        self.sword_bible_label.setObjectName('SwordBibleLabel')
        self.sword_folder_tab_layout.addWidget(self.sword_bible_label, 1, 0)
        self.sword_bible_combo_box = QtWidgets.QComboBox(self.sword_folder_tab)
        self.sword_bible_combo_box.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.sword_bible_combo_box.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.sword_bible_combo_box.setObjectName('SwordBibleComboBox')
        self.sword_folder_tab_layout.addWidget(self.sword_bible_combo_box, 1, 1)
        self.sword_tab_widget.addTab(self.sword_folder_tab, '')
        self.sword_zip_tab = QtWidgets.QWidget(self.sword_tab_widget)
        self.sword_zip_tab.setObjectName('SwordZipTab')
        self.sword_zip_layout = QtWidgets.QGridLayout(self.sword_zip_tab)
        self.sword_zip_layout.setObjectName('SwordZipLayout')
        self.sword_zipfile_label = QtWidgets.QLabel(self.sword_zip_tab)
        self.sword_zipfile_label.setObjectName('SwordZipFileLabel')
        self.sword_zipfile_edit = QtWidgets.QLineEdit(self.sword_zip_tab)
        self.sword_zipfile_edit.setObjectName('SwordZipFileEdit')
        self.sword_zipbrowse_button = QtWidgets.QToolButton(self.sword_zip_tab)
        self.sword_zipbrowse_button.setIcon(self.open_icon)
        self.sword_zipbrowse_button.setObjectName('SwordZipBrowseButton')
        self.sword_zipbible_label = QtWidgets.QLabel(self.sword_folder_tab)
        self.sword_zipbible_label.setObjectName('SwordZipBibleLabel')
        self.sword_zipbible_combo_box = QtWidgets.QComboBox(self.sword_zip_tab)
        self.sword_zipbible_combo_box.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.sword_zipbible_combo_box.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.sword_zipbible_combo_box.setObjectName('SwordZipBibleComboBox')
        self.sword_zip_layout.addWidget(self.sword_zipfile_label, 0, 0)
        self.sword_zip_layout.addWidget(self.sword_zipfile_edit, 0, 1)
        self.sword_zip_layout.addWidget(self.sword_zipbrowse_button, 0, 2)
        self.sword_zip_layout.addWidget(self.sword_zipbible_label, 1, 0)
        self.sword_zip_layout.addWidget(self.sword_zipbible_combo_box, 1, 1)
        self.sword_tab_widget.addTab(self.sword_zip_tab, '')
        self.sword_layout.addWidget(self.sword_tab_widget)
        self.sword_disabled_label = QtWidgets.QLabel(self.sword_widget)
        self.sword_disabled_label.setObjectName('SwordDisabledLabel')
        self.sword_layout.addWidget(self.sword_disabled_label)
        self.select_stack.addWidget(self.sword_widget)
        self.select_page_layout.addLayout(self.select_stack)
        self.addPage(self.select_page)
        # License Page
        self.license_details_page = QtWidgets.QWizardPage()
        self.license_details_page.setObjectName('LicenseDetailsPage')
        self.license_details_layout = QtWidgets.QFormLayout(self.license_details_page)
        self.license_details_layout.setObjectName('LicenseDetailsLayout')
        self.version_name_label = QtWidgets.QLabel(self.license_details_page)
        self.version_name_label.setObjectName('VersionNameLabel')
        self.license_details_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.version_name_label)
        self.version_name_edit = QtWidgets.QLineEdit(self.license_details_page)
        self.version_name_edit.setObjectName('VersionNameEdit')
        self.license_details_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.version_name_edit)
        self.copyright_label = QtWidgets.QLabel(self.license_details_page)
        self.copyright_label.setObjectName('CopyrightLabel')
        self.license_details_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.copyright_label)
        self.copyright_edit = QtWidgets.QLineEdit(self.license_details_page)
        self.copyright_edit.setObjectName('CopyrightEdit')
        self.license_details_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.copyright_edit)
        self.permissions_label = QtWidgets.QLabel(self.license_details_page)
        self.permissions_label.setObjectName('PermissionsLabel')
        self.license_details_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.permissions_label)
        self.permissions_edit = QtWidgets.QLineEdit(self.license_details_page)
        self.permissions_edit.setObjectName('PermissionsEdit')
        self.license_details_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.permissions_edit)
        self.addPage(self.license_details_page)

    def retranslateUi(self):
        """
        Allow for localisation of the bible import wizard.
        """
        self.setWindowTitle(translate('BiblesPlugin.ImportWizardForm', 'Bible Import Wizard'))
        self.title_label.setText(WizardStrings.HeaderStyle % translate('OpenLP.Ui',
                                                                       'Welcome to the Bible Import Wizard'))
        self.information_label.setText(
            translate('BiblesPlugin.ImportWizardForm',
                      'This wizard will help you to import Bibles from a variety of '
                      'formats. Click the next button below to start the process by '
                      'selecting a format to import from.'))
        self.select_page.setTitle(WizardStrings.ImportSelect)
        self.select_page.setSubTitle(WizardStrings.ImportSelectLong)
        self.format_label.setText(WizardStrings.FormatLabel)
        self.format_combo_box.setItemText(BibleFormat.OSIS, WizardStrings.OSIS)
        self.format_combo_box.setItemText(BibleFormat.CSV, WizardStrings.CSV)
        self.format_combo_box.setItemText(BibleFormat.OpenSong, WizardStrings.OS)
        self.format_combo_box.setItemText(BibleFormat.WebDownload, translate('BiblesPlugin.ImportWizardForm',
                                                                             'Web Download'))
        self.format_combo_box.setItemText(BibleFormat.Zefania, WizardStrings.ZEF)
        self.format_combo_box.setItemText(BibleFormat.SWORD, WizardStrings.SWORD)
        self.osis_file_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Bible file:'))
        self.csv_books_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Books file:'))
        self.csv_verses_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Verses file:'))
        self.open_song_file_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Bible file:'))
        self.web_source_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Location:'))
        self.zefania_file_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Bible file:'))
        self.web_update_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Click to download bible list'))
        self.web_update_button.setText(translate('BiblesPlugin.ImportWizardForm', 'Download bible list'))
        self.web_source_combo_box.setItemText(WebDownload.Crosswalk, translate('BiblesPlugin.ImportWizardForm',
                                                                               'Crosswalk'))
        self.web_source_combo_box.setItemText(WebDownload.BibleGateway, translate('BiblesPlugin.ImportWizardForm',
                                                                                  'BibleGateway'))
        self.web_source_combo_box.setItemText(WebDownload.Bibleserver, translate('BiblesPlugin.ImportWizardForm',
                                                                                 'Bibleserver'))
        self.web_translation_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Bible:'))
        self.web_tab_widget.setTabText(self.web_tab_widget.indexOf(self.web_bible_tab),
                                       translate('BiblesPlugin.ImportWizardForm', 'Download Options'))
        self.web_server_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Server:'))
        self.web_user_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Username:'))
        self.web_password_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Password:'))
        self.web_tab_widget.setTabText(
            self.web_tab_widget.indexOf(self.web_proxy_tab), translate('BiblesPlugin.ImportWizardForm',
                                                                       'Proxy Server (Optional)'))
        self.sword_bible_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Bibles:'))
        self.sword_folder_label.setText(translate('BiblesPlugin.ImportWizardForm', 'SWORD data folder:'))
        self.sword_zipfile_label.setText(translate('BiblesPlugin.ImportWizardForm', 'SWORD zip-file:'))
        self.sword_folder_edit.setPlaceholderText(translate('BiblesPlugin.ImportWizardForm',
                                                            'Defaults to the standard SWORD data folder'))
        self.sword_zipbible_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Bibles:'))
        self.sword_tab_widget.setTabText(self.sword_tab_widget.indexOf(self.sword_folder_tab),
                                         translate('BiblesPlugin.ImportWizardForm', 'Import from folder'))
        self.sword_tab_widget.setTabText(self.sword_tab_widget.indexOf(self.sword_zip_tab),
                                         translate('BiblesPlugin.ImportWizardForm', 'Import from Zip-file'))
        if PYSWORD_AVAILABLE:
            self.sword_disabled_label.setText('')
        else:
            self.sword_disabled_label.setText(translate('BiblesPlugin.ImportWizardForm',
                                                        'To import SWORD bibles the pysword python module must be '
                                                        'installed. Please read the manual for instructions.'))
        self.license_details_page.setTitle(
            translate('BiblesPlugin.ImportWizardForm', 'License Details'))
        self.license_details_page.setSubTitle(translate('BiblesPlugin.ImportWizardForm',
                                                        'Set up the Bible\'s license details.'))
        self.version_name_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Version name:'))
        self.copyright_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Copyright:'))
        self.permissions_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Permissions:'))
        self.progress_page.setTitle(WizardStrings.Importing)
        self.progress_page.setSubTitle(translate('BiblesPlugin.ImportWizardForm',
                                                 'Please wait while your Bible is imported.'))
        self.progress_label.setText(WizardStrings.Ready)
        self.progress_bar.setFormat('%p%')
        # Align all QFormLayouts towards each other.
        label_width = max(self.format_label.minimumSizeHint().width(),
                          self.osis_file_label.minimumSizeHint().width(),
                          self.csv_books_label.minimumSizeHint().width(),
                          self.csv_verses_label.minimumSizeHint().width(),
                          self.open_song_file_label.minimumSizeHint().width(),
                          self.zefania_file_label.minimumSizeHint().width())
        self.spacer.changeSize(label_width, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        if self.currentPage() == self.welcome_page:
            return True
        elif self.currentPage() == self.select_page:
            self.version_name_edit.clear()
            self.permissions_edit.clear()
            self.copyright_edit.clear()
            if self.field('source_format') == BibleFormat.OSIS:
                if not self.field('osis_location'):
                    critical_error_message_box(UiStrings().NFSs, WizardStrings.YouSpecifyFile % WizardStrings.OSIS)
                    self.osis_file_edit.setFocus()
                    return False
            elif self.field('source_format') == BibleFormat.CSV:
                if not self.field('csv_booksfile'):
                    critical_error_message_box(
                        UiStrings().NFSs, translate('BiblesPlugin.ImportWizardForm',
                                                    'You need to specify a file with books of the Bible to use in the '
                                                    'import.'))
                    self.csv_books_edit.setFocus()
                    return False
                elif not self.field('csv_versefile'):
                    critical_error_message_box(
                        UiStrings().NFSs,
                        translate('BiblesPlugin.ImportWizardForm', 'You need to specify a file of Bible verses to '
                                                                   'import.'))
                    self.csv_verses_edit.setFocus()
                    return False
            elif self.field('source_format') == BibleFormat.OpenSong:
                if not self.field('opensong_file'):
                    critical_error_message_box(UiStrings().NFSs, WizardStrings.YouSpecifyFile % WizardStrings.OS)
                    self.open_song_file_edit.setFocus()
                    return False
            elif self.field('source_format') == BibleFormat.Zefania:
                if not self.field('zefania_file'):
                    critical_error_message_box(UiStrings().NFSs, WizardStrings.YouSpecifyFile % WizardStrings.ZEF)
                    self.zefania_file_edit.setFocus()
                    return False
            elif self.field('source_format') == BibleFormat.WebDownload:
                # If count is 0 the bible list has not yet been downloaded
                if self.web_translation_combo_box.count() == 0:
                    return False
                else:
                    self.version_name_edit.setText(self.web_translation_combo_box.currentText())
            elif self.field('source_format') == BibleFormat.SWORD:
                # Test the SWORD tab that is currently active
                if self.sword_tab_widget.currentIndex() == self.sword_tab_widget.indexOf(self.sword_folder_tab):
                    if not self.field('sword_folder_path') and self.sword_bible_combo_box.count() == 0:
                        critical_error_message_box(UiStrings().NFSs,
                                                   WizardStrings.YouSpecifyFolder % WizardStrings.SWORD)
                        self.sword_folder_edit.setFocus()
                        return False
                    key = self.sword_bible_combo_box.itemData(self.sword_bible_combo_box.currentIndex())
                    if 'description' in self.pysword_folder_modules_json[key]:
                        self.version_name_edit.setText(self.pysword_folder_modules_json[key]['description'])
                    if 'distributionlicense' in self.pysword_folder_modules_json[key]:
                        self.permissions_edit.setText(self.pysword_folder_modules_json[key]['distributionlicense'])
                    if 'copyright' in self.pysword_folder_modules_json[key]:
                        self.copyright_edit.setText(self.pysword_folder_modules_json[key]['copyright'])
                elif self.sword_tab_widget.currentIndex() == self.sword_tab_widget.indexOf(self.sword_zip_tab):
                    if not self.field('sword_zip_path'):
                        critical_error_message_box(UiStrings().NFSs, WizardStrings.YouSpecifyFile % WizardStrings.SWORD)
                        self.sword_zipfile_edit.setFocus()
                        return False
                    key = self.sword_zipbible_combo_box.itemData(self.sword_zipbible_combo_box.currentIndex())
                    if 'description' in self.pysword_zip_modules_json[key]:
                        self.version_name_edit.setText(self.pysword_zip_modules_json[key]['description'])
                    if 'distributionlicense' in self.pysword_zip_modules_json[key]:
                        self.permissions_edit.setText(self.pysword_zip_modules_json[key]['distributionlicense'])
            return True
        elif self.currentPage() == self.license_details_page:
            license_version = self.field('license_version')
            license_copyright = self.field('license_copyright')
            path = AppLocation.get_section_data_path('bibles')
            if not license_version:
                critical_error_message_box(
                    UiStrings().EmptyField,
                    translate('BiblesPlugin.ImportWizardForm', 'You need to specify a version name for your Bible.'))
                self.version_name_edit.setFocus()
                return False
            elif not license_copyright:
                critical_error_message_box(
                    UiStrings().EmptyField,
                    translate('BiblesPlugin.ImportWizardForm', 'You need to set a copyright for your Bible. '
                              'Bibles in the Public Domain need to be marked as such.'))
                self.copyright_edit.setFocus()
                return False
            elif self.manager.exists(license_version):
                critical_error_message_box(
                    translate('BiblesPlugin.ImportWizardForm', 'Bible Exists'),
                    translate('BiblesPlugin.ImportWizardForm',
                              'This Bible already exists. Please import a different Bible or first delete the '
                              'existing one.'))
                self.version_name_edit.setFocus()
                return False
            elif os.path.exists(os.path.join(path, clean_filename(license_version))):
                critical_error_message_box(
                    translate('BiblesPlugin.ImportWizardForm', 'Bible Exists'),
                    translate('BiblesPlugin.ImportWizardForm', 'This Bible already exists. Please import '
                              'a different Bible or first delete the existing one.'))
                self.version_name_edit.setFocus()
                return False
            return True
        if self.currentPage() == self.progress_page:
            return True

    def on_web_source_combo_box_index_changed(self, index):
        """
        Setup the list of Bibles when you select a different source on the web download page.

        :param index: The index of the combo box.
        """
        self.web_translation_combo_box.clear()
        if self.web_bible_list and index in self.web_bible_list:
            bibles = list(self.web_bible_list[index].keys())
            bibles.sort(key=get_locale_key)
            self.web_translation_combo_box.addItems(bibles)

    def on_osis_browse_button_clicked(self):
        """
        Show the file open dialog for the OSIS file.
        """
        self.get_file_name(WizardStrings.OpenTypeFile % WizardStrings.OSIS, self.osis_file_edit,
                           'last directory import')

    def on_csv_books_browse_button_clicked(self):
        """
        Show the file open dialog for the books CSV file.
        """
        # TODO: Verify format() with varible template
        self.get_file_name(
            WizardStrings.OpenTypeFile % WizardStrings.CSV,
            self.csv_books_edit,
            'last directory import',
            '{name} (*.csv)'.format(name=translate('BiblesPlugin.ImportWizardForm', 'CSV File')))

    def on_csv_verses_browse_button_clicked(self):
        """
        Show the file open dialog for the verses CSV file.
        """
        # TODO: Verify format() with variable template
        self.get_file_name(WizardStrings.OpenTypeFile % WizardStrings.CSV, self.csv_verses_edit,
                           'last directory import',
                           '{name} (*.csv)'.format(name=translate('BiblesPlugin.ImportWizardForm', 'CSV File')))

    def on_open_song_browse_button_clicked(self):
        """
        Show the file open dialog for the OpenSong file.
        """
        # TODO: Verify format() with variable template
        self.get_file_name(WizardStrings.OpenTypeFile % WizardStrings.OS, self.open_song_file_edit,
                           'last directory import')

    def on_zefania_browse_button_clicked(self):
        """
        Show the file open dialog for the Zefania file.
        """
        # TODO: Verify format() with variable template
        self.get_file_name(WizardStrings.OpenTypeFile % WizardStrings.ZEF, self.zefania_file_edit,
                           'last directory import')

    def on_web_update_button_clicked(self):
        """
        Download list of bibles from Crosswalk, BibleServer and BibleGateway.
        """
        # Download from Crosswalk, BiblesGateway, BibleServer
        self.web_bible_list = {}
        self.web_source_combo_box.setEnabled(False)
        self.web_translation_combo_box.setEnabled(False)
        self.web_update_button.setEnabled(False)
        self.web_progress_bar.setVisible(True)
        self.web_progress_bar.setValue(0)
        proxy_server = self.field('proxy_server')
        # TODO: Where does critical_error_message_box get %s string from?
        for (download_type, extractor) in ((WebDownload.Crosswalk, CWExtract(proxy_server)),
                                           (WebDownload.BibleGateway, BGExtract(proxy_server)),
                                           (WebDownload.Bibleserver, BSExtract(proxy_server))):
            try:
                bibles = extractor.get_bibles_from_http()
            except (urllib.error.URLError, ConnectionError) as err:
                critical_error_message_box(translate('BiblesPlugin.ImportWizardForm', 'Error during download'),
                                           translate('BiblesPlugin.ImportWizardForm',
                                                     'An error occurred while downloading the list of bibles from %s.'))
                bibles = None
            if bibles:
                self.web_bible_list[download_type] = {}
                for (bible_name, bible_key, language_code) in bibles:
                    self.web_bible_list[download_type][bible_name] = (bible_key, language_code)
            self.web_progress_bar.setValue(download_type + 1)
        # Update combo box if something got into the list
        if self.web_bible_list:
            self.on_web_source_combo_box_index_changed(0)
        self.web_source_combo_box.setEnabled(True)
        self.web_translation_combo_box.setEnabled(True)
        self.web_update_button.setEnabled(True)
        self.web_progress_bar.setVisible(False)

    def on_sword_browse_button_clicked(self):
        """
        Show the file open dialog for the SWORD folder.
        """
        self.get_folder(WizardStrings.OpenTypeFolder % WizardStrings.SWORD, self.sword_folder_edit,
                        'last directory import')
        if self.sword_folder_edit.text():
            try:
                self.pysword_folder_modules = modules.SwordModules(self.sword_folder_edit.text())
                self.pysword_folder_modules_json = self.pysword_folder_modules.parse_modules()
                bible_keys = self.pysword_folder_modules_json.keys()
                self.sword_bible_combo_box.clear()
                for key in bible_keys:
                    self.sword_bible_combo_box.addItem(self.pysword_folder_modules_json[key]['description'], key)
            except:
                self.sword_bible_combo_box.clear()

    def on_sword_zipbrowse_button_clicked(self):
        """
        Show the file open dialog for a SWORD zip-file.
        """
        self.get_file_name(WizardStrings.OpenTypeFile % WizardStrings.SWORD, self.sword_zipfile_edit,
                           'last directory import')
        if self.sword_zipfile_edit.text():
            try:
                self.pysword_zip_modules = modules.SwordModules(self.sword_zipfile_edit.text())
                self.pysword_zip_modules_json = self.pysword_zip_modules.parse_modules()
                bible_keys = self.pysword_zip_modules_json.keys()
                self.sword_zipbible_combo_box.clear()
                for key in bible_keys:
                    self.sword_zipbible_combo_box.addItem(self.pysword_zip_modules_json[key]['description'], key)
            except:
                self.sword_zipbible_combo_box.clear()

    def register_fields(self):
        """
        Register the bible import wizard fields.
        """
        self.select_page.registerField('source_format', self.format_combo_box)
        self.select_page.registerField('osis_location', self.osis_file_edit)
        self.select_page.registerField('csv_booksfile', self.csv_books_edit)
        self.select_page.registerField('csv_versefile', self.csv_verses_edit)
        self.select_page.registerField('opensong_file', self.open_song_file_edit)
        self.select_page.registerField('zefania_file', self.zefania_file_edit)
        self.select_page.registerField('web_location', self.web_source_combo_box)
        self.select_page.registerField('web_biblename', self.web_translation_combo_box)
        self.select_page.registerField('sword_folder_path', self.sword_folder_edit)
        self.select_page.registerField('sword_zip_path', self.sword_zipfile_edit)
        self.select_page.registerField('proxy_server', self.web_server_edit)
        self.select_page.registerField('proxy_username', self.web_user_edit)
        self.select_page.registerField('proxy_password', self.web_password_edit)
        self.license_details_page.registerField('license_version', self.version_name_edit)
        self.license_details_page.registerField('license_copyright', self.copyright_edit)
        self.license_details_page.registerField('license_permissions', self.permissions_edit)

    def set_defaults(self):
        """
        Set default values for the wizard pages.
        """
        settings = Settings()
        settings.beginGroup(self.plugin.settings_section)
        self.restart()
        self.finish_button.setVisible(False)
        self.cancel_button.setVisible(True)
        self.setField('source_format', 0)
        self.setField('osis_location', '')
        self.setField('csv_booksfile', '')
        self.setField('csv_versefile', '')
        self.setField('opensong_file', '')
        self.setField('zefania_file', '')
        self.setField('sword_folder_path', '')
        self.setField('sword_zip_path', '')
        self.setField('web_location', WebDownload.Crosswalk)
        self.setField('web_biblename', self.web_translation_combo_box.currentIndex())
        self.setField('proxy_server', settings.value('proxy address'))
        self.setField('proxy_username', settings.value('proxy username'))
        self.setField('proxy_password', settings.value('proxy password'))
        self.setField('license_version', self.version_name_edit.text())
        self.setField('license_copyright', self.copyright_edit.text())
        self.setField('license_permissions', self.permissions_edit.text())
        self.on_web_source_combo_box_index_changed(WebDownload.Crosswalk)
        settings.endGroup()

    def pre_wizard(self):
        """
        Prepare the UI for the import.
        """
        super(BibleImportForm, self).pre_wizard()
        bible_type = self.field('source_format')
        if bible_type == BibleFormat.WebDownload:
            self.progress_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Registering Bible...'))
        else:
            self.progress_label.setText(WizardStrings.StartingImport)
        self.application.process_events()

    def perform_wizard(self):
        """
        Perform the actual import.
        """
        bible_type = self.field('source_format')
        license_version = self.field('license_version')
        license_copyright = self.field('license_copyright')
        license_permissions = self.field('license_permissions')
        importer = None
        if bible_type == BibleFormat.OSIS:
            # Import an OSIS bible.
            importer = self.manager.import_bible(BibleFormat.OSIS, name=license_version,
                                                 filename=self.field('osis_location'))
        elif bible_type == BibleFormat.CSV:
            # Import a CSV bible.
            importer = self.manager.import_bible(BibleFormat.CSV, name=license_version,
                                                 booksfile=self.field('csv_booksfile'),
                                                 versefile=self.field('csv_versefile'))
        elif bible_type == BibleFormat.OpenSong:
            # Import an OpenSong bible.
            importer = self.manager.import_bible(BibleFormat.OpenSong, name=license_version,
                                                 filename=self.field('opensong_file'))
        elif bible_type == BibleFormat.WebDownload:
            # Import a bible from the web.
            self.progress_bar.setMaximum(1)
            download_location = self.field('web_location')
            bible_version = self.web_translation_combo_box.currentText()
            (bible, language_id) = self.web_bible_list[download_location][bible_version]
            importer = self.manager.import_bible(
                BibleFormat.WebDownload, name=license_version,
                download_source=WebDownload.Names[download_location],
                download_name=bible,
                proxy_server=self.field('proxy_server'),
                proxy_username=self.field('proxy_username'),
                proxy_password=self.field('proxy_password'),
                language_id=language_id
            )
        elif bible_type == BibleFormat.Zefania:
            # Import a Zefania bible.
            importer = self.manager.import_bible(BibleFormat.Zefania, name=license_version,
                                                 filename=self.field('zefania_file'))
        elif bible_type == BibleFormat.SWORD:
            # Import a SWORD bible.
            if self.sword_tab_widget.currentIndex() == self.sword_tab_widget.indexOf(self.sword_folder_tab):
                importer = self.manager.import_bible(BibleFormat.SWORD, name=license_version,
                                                     sword_path=self.field('sword_folder_path'),
                                                     sword_key=self.sword_bible_combo_box.itemData(
                                                         self.sword_bible_combo_box.currentIndex()))
            else:
                importer = self.manager.import_bible(BibleFormat.SWORD, name=license_version,
                                                     sword_path=self.field('sword_zip_path'),
                                                     sword_key=self.sword_zipbible_combo_box.itemData(
                                                         self.sword_zipbible_combo_box.currentIndex()))

        try:
            if importer.do_import(license_version):
                self.manager.save_meta_data(license_version, license_version, license_copyright, license_permissions)
                self.manager.reload_bibles()
                if bible_type == BibleFormat.WebDownload:
                    self.progress_label.setText(
                        translate('BiblesPlugin.ImportWizardForm', 'Registered Bible. Please note, that verses will be '
                                  'downloaded on demand and thus an internet connection is required.'))
                else:
                    self.progress_label.setText(WizardStrings.FinishedImport)
                return
        except (AttributeError, ValidationError, etree.XMLSyntaxError):
            log.exception('Importing bible failed')
            trace_error_handler(log)

        self.progress_label.setText(translate('BiblesPlugin.ImportWizardForm', 'Your Bible import failed.'))
        del self.manager.db_cache[importer.name]
        delete_database(self.plugin.settings_section, importer.file)
