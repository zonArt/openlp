# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

import csv
import logging
import os
import os.path

from PyQt4 import QtCore, QtGui

from bibleimportwizard import Ui_BibleImportWizard
from openlp.core.lib import Receiver, SettingsManager
from openlp.core.utils import AppLocation, variant_to_unicode
from openlp.plugins.bibles.lib.manager import BibleFormat

log = logging.getLogger(__name__)

class WebDownload(object):
    Unknown = -1
    Crosswalk = 0
    BibleGateway = 1

    Names = {
        0: u'Crosswalk',
        1: u'BibleGateway'
    }

    @classmethod
    def get_name(cls, id):
        return cls.Names[id]


class ImportWizardForm(QtGui.QWizard, Ui_BibleImportWizard):
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
        QtGui.QWizard.__init__(self, parent)
        self.setupUi(self)
        self.registerFields()
        self.finishButton = self.button(QtGui.QWizard.FinishButton)
        self.cancelButton = self.button(QtGui.QWizard.CancelButton)
        self.manager = manager
        self.bibleplugin = bibleplugin
        self.manager.set_process_dialog(self)
        self.web_bible_list = {}
        self.loadWebBibles()
        QtCore.QObject.connect(self.LocationComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onLocationComboBoxChanged)
        QtCore.QObject.connect(self.OsisFileButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onOsisFileButtonClicked)
        QtCore.QObject.connect(self.BooksFileButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onBooksFileButtonClicked)
        QtCore.QObject.connect(self.CsvVersesFileButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onCsvVersesFileButtonClicked)
        QtCore.QObject.connect(self.OpenSongBrowseButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onOpenSongBrowseButtonClicked)
        QtCore.QObject.connect(self.cancelButton,
            QtCore.SIGNAL(u'clicked(bool)'),
            self.onCancelButtonClicked)
        QtCore.QObject.connect(self,
            QtCore.SIGNAL(u'currentIdChanged(int)'),
            self.onCurrentIdChanged)

    def exec_(self):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        if self.currentId() == 0:
            # Welcome page
            return True
        elif self.currentId() == 1:
            # Select page
            if self.field(u'source_format').toInt()[0] == BibleFormat.OSIS:
                if self.field(u'osis_location').toString() == u'':
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid Bible Location'),
                        self.trUtf8('You need to specify a file to import your '
                            'Bible from.'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.OSISLocationEdit.setFocus()
                    return False
            elif self.field(u'source_format').toInt()[0] == BibleFormat.CSV:
                if self.field(u'csv_booksfile').toString() == u'':
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid Books File'),
                        self.trUtf8('You need to specify a file with books of '
                            'the Bible to use in the import.'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.BooksLocationEdit.setFocus()
                    return False
                elif self.field(u'csv_versefile').toString() == u'':
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid Verse File'),
                        self.trUtf8('You need to specify a file of Bible '
                            'verses to import.'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.CsvVerseLocationEdit.setFocus()
                    return False
            elif self.field(u'source_format').toInt()[0] == BibleFormat.OpenSong:
                if self.field(u'opensong_file').toString() == u'':
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid OpenSong Bible'),
                        self.trUtf8('You need to specify an OpenSong Bible '
                            'file to import.'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.OpenSongFileEdit.setFocus()
                    return False
            return True
        elif self.currentId() == 2:
            # License details
            license_version = variant_to_unicode(self.field(u'license_version'))
            license_copyright = variant_to_unicode(self.field(u'license_copyright'))
            if license_version == u'':
                QtGui.QMessageBox.critical(self,
                    self.trUtf8('Empty Version Name'),
                    self.trUtf8('You need to specify a version name for your '
                        'Bible.'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                self.VersionNameEdit.setFocus()
                return False
            elif license_copyright == u'':
                QtGui.QMessageBox.critical(self,
                    self.trUtf8('Empty Copyright'),
                    self.trUtf8('You need to set a copyright for your Bible! '
                        'Bibles in the Public Domain need to be marked as '
                        'such.'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                self.CopyrightEdit.setFocus()
                return False
            elif self.manager.exists(license_version):
                QtGui.QMessageBox.critical(self,
                    self.trUtf8('Bible Exists'),
                    self.trUtf8('This Bible already exists! Please import '
                        'a different Bible or first delete the existing one.'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                self.VersionNameEdit.setFocus()
                return False
            return True
        if self.currentId() == 3:
            # Progress page
            return True

    def onLocationComboBoxChanged(self, index):
        """
        Setup the list of Bibles when you select a different source on the web
        download page.

        ``index``
            The index of the combo box.
        """
        self.BibleComboBox.clear()
        for bible in self.web_bible_list[index].keys():
            self.BibleComboBox.addItem(unicode(self.trUtf8(bible)))

    def onOsisFileButtonClicked(self):
        """
        Show the file open dialog for the OSIS file.
        """
        self.getFileName(self.trUtf8('Open OSIS File'),
            self.OSISLocationEdit)

    def onBooksFileButtonClicked(self):
        """
        Show the file open dialog for the books CSV file.
        """
        self.getFileName(self.trUtf8('Open Books CSV File'),
            self.BooksLocationEdit)

    def onCsvVersesFileButtonClicked(self):
        """
        Show the file open dialog for the verses CSV file.
        """
        self.getFileName(self.trUtf8('Open Verses CSV File'),
            self.CsvVerseLocationEdit)

    def onOpenSongBrowseButtonClicked(self):
        """
        Show the file open dialog for the OpenSong file.
        """
        self.getFileName(self.trUtf8('Open OpenSong Bible'),
            self.OpenSongFileEdit)

    def onCancelButtonClicked(self, checked):
        """
        Stop the import on pressing the cancel button.
        """
        log.debug('Cancel button pressed!')
        if self.currentId() == 3:
            Receiver.send_message(u'bibles_stop_import')

    def onCurrentIdChanged(self, id):
        if id == 3:
            self.preImport()
            self.performImport()
            self.postImport()

    def registerFields(self):
        self.SelectPage.registerField(
            u'source_format', self.FormatComboBox)
        self.SelectPage.registerField(
            u'osis_location', self.OSISLocationEdit)
        self.SelectPage.registerField(
            u'csv_booksfile', self.BooksLocationEdit)
        self.SelectPage.registerField(
            u'csv_versefile', self.CsvVerseLocationEdit)
        self.SelectPage.registerField(
            u'opensong_file', self.OpenSongFileEdit)
        self.SelectPage.registerField(
            u'web_location', self.LocationComboBox)
        self.SelectPage.registerField(
            u'web_biblename', self.BibleComboBox)
        self.SelectPage.registerField(
            u'proxy_server', self.AddressEdit)
        self.SelectPage.registerField(
            u'proxy_username', self.UsernameEdit)
        self.SelectPage.registerField(
            u'proxy_password', self.PasswordEdit)
        self.LicenseDetailsPage.registerField(
            u'license_version', self.VersionNameEdit)
        self.LicenseDetailsPage.registerField(
            u'license_copyright', self.CopyrightEdit)
        self.LicenseDetailsPage.registerField(
            u'license_permission', self.PermissionEdit)

    def setDefaults(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.bibleplugin.settingsSection)
        self.setField(u'source_format', QtCore.QVariant(0))
        self.setField(u'osis_location', QtCore.QVariant(''))
        self.setField(u'csv_booksfile', QtCore.QVariant(''))
        self.setField(u'csv_versefile', QtCore.QVariant(''))
        self.setField(u'opensong_file', QtCore.QVariant(''))
        self.setField(u'web_location', QtCore.QVariant(WebDownload.Crosswalk))
        self.setField(u'web_biblename', QtCore.QVariant(self.BibleComboBox))
        self.setField(u'proxy_server',
            settings.value(u'proxy address', QtCore.QVariant(u'')))
        self.setField(u'proxy_username',
            settings.value(u'proxy username', QtCore.QVariant(u'')))
        self.setField(u'proxy_password',
            settings.value(u'proxy password', QtCore.QVariant(u'')))
        self.setField(u'license_version', QtCore.QVariant(self.VersionNameEdit))
        self.setField(u'license_copyright', QtCore.QVariant(self.CopyrightEdit))
        self.setField(u'license_permission',
            QtCore.QVariant(self.PermissionEdit))
        self.onLocationComboBoxChanged(WebDownload.Crosswalk)
        settings.endGroup()

    def loadWebBibles(self):
        """
        Load the list of Crosswalk and BibleGateway bibles.
        """
        #Load and store Crosswalk Bibles
        filepath = AppLocation.get_directory(AppLocation.PluginsDir)
        filepath = os.path.join(filepath, u'bibles', u'resources')
        try:
            self.web_bible_list[WebDownload.Crosswalk] = {}
            books_file = open(
                os.path.join(filepath, u'crosswalkbooks.csv'), 'r')
            dialect = csv.Sniffer().sniff(books_file.read(1024))
            books_file.seek(0)
            books_reader = csv.reader(books_file, dialect)
            for line in books_reader:
                ver = line[0]
                name = line[1]
                if not isinstance(ver, unicode):
                    ver = unicode(ver, u'utf8')
                if not isinstance(name, unicode):
                    name = unicode(name, u'utf8')
                self.web_bible_list[WebDownload.Crosswalk][ver] = name.strip()
        except:
            log.exception(u'Crosswalk resources missing')
        finally:
            if books_file:
                books_file.close()
        #Load and store BibleGateway Bibles
        try:
            self.web_bible_list[WebDownload.BibleGateway] = {}
            books_file = open(os.path.join(filepath, u'biblegateway.csv'), 'r')
            dialect = csv.Sniffer().sniff(books_file.read(1024))
            books_file.seek(0)
            books_reader = csv.reader(books_file, dialect)
            for line in books_reader:
                ver = line[0]
                name = line[1]
                if not isinstance(ver, unicode):
                    ver = unicode(ver, u'utf8')
                if not isinstance(name, unicode):
                    name = unicode(name, u'utf8')
                self.web_bible_list[WebDownload.BibleGateway][ver] = name.strip()
        except:
            log.exception(u'Biblegateway resources missing')
        finally:
            if books_file:
                books_file.close()

    def getFileName(self, title, editbox):
        filename = QtGui.QFileDialog.getOpenFileName(self, title,
            SettingsManager.get_last_dir(self.bibleplugin.settingsSection, 1))
        if filename:
            editbox.setText(filename)
            SettingsManager.set_last_dir(
                self.bibleplugin.settingsSection, filename, 1)

    def incrementProgressBar(self, status_text):
        log.debug(u'IncrementBar %s', status_text)
        self.ImportProgressLabel.setText(status_text)
        self.ImportProgressBar.setValue(self.ImportProgressBar.value() + 1)
        Receiver.send_message(u'openlp_process_events')

    def preImport(self):
        self.finishButton.setVisible(False)
        self.ImportProgressBar.setMinimum(0)
        self.ImportProgressBar.setMaximum(1188)
        self.ImportProgressBar.setValue(0)
        self.ImportProgressLabel.setText(self.trUtf8('Starting import...'))
        Receiver.send_message(u'openlp_process_events')

    def performImport(self):
        bible_type = self.field(u'source_format').toInt()[0]
        license_version = variant_to_unicode(self.field(u'license_version'))
        license_copyright = variant_to_unicode(self.field(u'license_copyright'))
        license_permission = variant_to_unicode(
            self.field(u'license_permission'))
        importer = None
        if bible_type == BibleFormat.OSIS:
            # Import an OSIS bible
            importer = self.manager.import_bible(BibleFormat.OSIS,
                name=license_version,
                filename=variant_to_unicode(self.field(u'osis_location'))
            )
        elif bible_type == BibleFormat.CSV:
            # Import a CSV bible
            importer = self.manager.import_bible(BibleFormat.CSV,
                name=license_version,
                booksfile=variant_to_unicode(self.field(u'csv_booksfile')),
                versefile=variant_to_unicode(self.field(u'csv_versefile'))
            )
        elif bible_type == BibleFormat.OpenSong:
            # Import an OpenSong bible
            importer = self.manager.import_bible(BibleFormat.OpenSong,
                name=license_version,
                filename=variant_to_unicode(self.field(u'opensong_file'))
            )
        elif bible_type == BibleFormat.WebDownload:
            # Import a bible from the web
            self.ImportProgressBar.setMaximum(1)
            download_location = self.field(u'web_location').toInt()[0]
            bible_version = self.BibleComboBox.currentText()
            if not isinstance(bible_version, unicode):
                bible_version = unicode(bible_version, u'utf8')
            if download_location == WebDownload.Crosswalk:
                bible = self.web_bible_list[WebDownload.Crosswalk][bible_version]
            elif download_location == WebDownload.BibleGateway:
                bible = self.web_bible_list[WebDownload.BibleGateway][bible_version]
            importer = self.manager.import_bible(
                BibleFormat.WebDownload,
                name=license_version,
                download_source=WebDownload.get_name(download_location),
                download_name=bible,
                proxy_server=variant_to_unicode(self.field(u'proxy_server')),
                proxy_username=variant_to_unicode(self.field(u'proxy_username')),
                proxy_password=variant_to_unicode(self.field(u'proxy_password'))
            )
        success = importer.do_import()
        if success:
            self.manager.save_meta_data(license_version, license_version,
                license_copyright, license_permission)
            self.manager.reload_bibles()
            self.ImportProgressLabel.setText(self.trUtf8('Finished import.'))
        else:
            self.ImportProgressLabel.setText(
                self.trUtf8('Your Bible import failed.'))
            importer.delete()

    def postImport(self):
        self.ImportProgressBar.setValue(self.ImportProgressBar.maximum())
        self.finishButton.setVisible(True)
        self.cancelButton.setVisible(False)
        Receiver.send_message(u'openlp_process_events')
