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

import csv
import logging
import os
import os.path

from PyQt4 import QtCore, QtGui

from bibleimportwizard import Ui_BibleImportWizard
from openlp.core.lib import Receiver, SettingsManager, translate
from openlp.core.lib.db import delete_database
from openlp.core.utils import AppLocation
from openlp.plugins.bibles.lib.manager import BibleFormat

log = logging.getLogger(__name__)

class WebDownload(object):
    Unknown = -1
    Crosswalk = 0
    BibleGateway = 1
    Bibleserver = 2

    Names = {
        0: u'Crosswalk',
        1: u'BibleGateway',
        2: u'Bibleserver'
    }

    @classmethod
    def get_name(cls, name):
        return cls.Names[name]


class BibleImportForm(QtGui.QWizard, Ui_BibleImportWizard):
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
        if not BibleFormat.get_availability(BibleFormat.OpenLP1):
            self.openlp1Page.setVisible(False)
            self.openlp1LocationLabel.setVisible(False)
            self.openlp1LocationEdit.setVisible(False)
            self.openlp1FileButton.setVisible(False)
            self.openlp1DisabledLabel.setVisible(True)
        self.finishButton = self.button(QtGui.QWizard.FinishButton)
        self.cancelButton = self.button(QtGui.QWizard.CancelButton)
        self.manager = manager
        self.bibleplugin = bibleplugin
        self.manager.set_process_dialog(self)
        self.web_bible_list = {}
        self.loadWebBibles()
        QtCore.QObject.connect(self.locationComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onLocationComboBoxChanged)
        QtCore.QObject.connect(self.osisFileButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onOsisFileButtonClicked)
        QtCore.QObject.connect(self.booksFileButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onBooksFileButtonClicked)
        QtCore.QObject.connect(self.csvVersesFileButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onCsvVersesFileButtonClicked)
        QtCore.QObject.connect(self.openSongBrowseButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onOpenSongBrowseButtonClicked)
        QtCore.QObject.connect(self.openlp1FileButton,
            QtCore.SIGNAL(u'clicked()'),
            self.onOpenlp1FileButtonClicked)
        QtCore.QObject.connect(self,
            QtCore.SIGNAL(u'currentIdChanged(int)'),
            self.onCurrentIdChanged)

    def exec_(self):
        """
        Run the wizard.
        """
        self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def reject(self):
        """
        Stop the import on cancel button, close button or ESC key.
        """
        log.debug('Import canceled by user.')
        if self.currentId() == 3:
            Receiver.send_message(u'bibles_stop_import')
        self.done(QtGui.QDialog.Rejected)

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
                if not self.field(u'osis_location').toString():
                    QtGui.QMessageBox.critical(self,
                        translate('BiblesPlugin.ImportWizardForm',
                        'Invalid Bible Location'),
                        translate('BiblesPlugin.ImportWizardForm',
                        'You need to specify a file to import your '
                        'Bible from.'))
                    self.OSISLocationEdit.setFocus()
                    return False
            elif self.field(u'source_format').toInt()[0] == BibleFormat.CSV:
                if not self.field(u'csv_booksfile').toString():
                    QtGui.QMessageBox.critical(self,
                        translate('BiblesPlugin.ImportWizardForm',
                        'Invalid Books File'),
                        translate('BiblesPlugin.ImportWizardForm',
                        'You need to specify a file with books of '
                        'the Bible to use in the import.'))
                    self.booksLocationEdit.setFocus()
                    return False
                elif not self.field(u'csv_versefile').toString():
                    QtGui.QMessageBox.critical(self,
                        translate('BiblesPlugin.ImportWizardForm',
                        'Invalid Verse File'),
                        translate('BiblesPlugin.ImportWizardForm',
                        'You need to specify a file of Bible '
                        'verses to import.'))
                    self.csvVerseLocationEdit.setFocus()
                    return False
            elif self.field(u'source_format').toInt()[0] == \
                BibleFormat.OpenSong:
                if not self.field(u'opensong_file').toString():
                    QtGui.QMessageBox.critical(self,
                        translate('BiblesPlugin.ImportWizardForm',
                        'Invalid OpenSong Bible'),
                        translate('BiblesPlugin.ImportWizardForm',
                        'You need to specify an OpenSong Bible '
                        'file to import.'))
                    self.openSongFileEdit.setFocus()
                    return False
            elif self.field(u'source_format').toInt()[0] == BibleFormat.OpenLP1:
                if not self.field(u'openlp1_location').toString():
                    QtGui.QMessageBox.critical(self,
                        translate('BiblesPlugin.ImportWizardForm',
                        'Invalid Bible Location'),
                        translate('BiblesPlugin.ImportWizardForm',
                        'You need to specify a file to import your '
                        'Bible from.'))
                    self.openlp1LocationEdit.setFocus()
                    return False
            return True
        elif self.currentId() == 2:
            # License details
            license_version = unicode(self.field(u'license_version').toString())
            license_copyright = \
                unicode(self.field(u'license_copyright').toString())
            if not license_version:
                QtGui.QMessageBox.critical(self,
                    translate('BiblesPlugin.ImportWizardForm',
                    'Empty Version Name'),
                    translate('BiblesPlugin.ImportWizardForm',
                    'You need to specify a version name for your Bible.'))
                self.versionNameEdit.setFocus()
                return False
            elif not license_copyright:
                QtGui.QMessageBox.critical(self,
                    translate('BiblesPlugin.ImportWizardForm',
                    'Empty Copyright'),
                    translate('BiblesPlugin.ImportWizardForm',
                    'You need to set a copyright for your Bible. '
                    'Bibles in the Public Domain need to be marked as such.'))
                self.copyrightEdit.setFocus()
                return False
            elif self.manager.exists(license_version):
                QtGui.QMessageBox.critical(self,
                    translate('BiblesPlugin.ImportWizardForm', 'Bible Exists'),
                    translate('BiblesPlugin.ImportWizardForm',
                    'This Bible already exists. Please import '
                    'a different Bible or first delete the existing one.'))
                self.versionNameEdit.setFocus()
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
        self.bibleComboBox.clear()
        bibles = self.web_bible_list[index].keys()
        bibles.sort()
        for bible in bibles:
            self.bibleComboBox.addItem(bible)

    def onOsisFileButtonClicked(self):
        """
        Show the file open dialog for the OSIS file.
        """
        self.getFileName(
            translate('BiblesPlugin.ImportWizardForm', 'Open OSIS File'),
            self.OSISLocationEdit)

    def onBooksFileButtonClicked(self):
        """
        Show the file open dialog for the books CSV file.
        """
        self.getFileName(
            translate('BiblesPlugin.ImportWizardForm', 'Open Books CSV File'),
            self.booksLocationEdit, u'%s (*.csv)'
            % translate('BiblesPlugin.ImportWizardForm', 'CSV File'))

    def onCsvVersesFileButtonClicked(self):
        """
        Show the file open dialog for the verses CSV file.
        """
        self.getFileName(translate('BiblesPlugin.ImportWizardForm',
            'Open Verses CSV File'), self.csvVerseLocationEdit, u'%s (*.csv)'
            % translate('BiblesPlugin.ImportWizardForm', 'CSV File'))

    def onOpenSongBrowseButtonClicked(self):
        """
        Show the file open dialog for the OpenSong file.
        """
        self.getFileName(
            translate('BiblesPlugin.ImportWizardForm', 'Open OpenSong Bible'),
            self.openSongFileEdit)

    def onOpenlp1FileButtonClicked(self):
        """
        Show the file open dialog for the openlp.org 1.x file.
        """
        self.getFileName(
            translate('BiblesPlugin.ImportWizardForm',
            'Open openlp.org 1.x Bible'), self.openlp1LocationEdit,
            u'%s (*.bible)' % translate('BiblesPlugin.ImportWizardForm',
            'openlp.org 1.x bible'))

    def onCurrentIdChanged(self, pageId):
        if pageId == 3:
            self.preImport()
            self.performImport()
            self.postImport()

    def registerFields(self):
        self.selectPage.registerField(u'source_format', self.formatComboBox)
        self.selectPage.registerField(u'osis_location', self.OSISLocationEdit)
        self.selectPage.registerField(u'csv_booksfile', self.booksLocationEdit)
        self.selectPage.registerField(
            u'csv_versefile', self.csvVerseLocationEdit)
        self.selectPage.registerField(u'opensong_file', self.openSongFileEdit)
        self.selectPage.registerField(u'web_location', self.locationComboBox)
        self.selectPage.registerField(u'web_biblename', self.bibleComboBox)
        self.selectPage.registerField(u'proxy_server', self.addressEdit)
        self.selectPage.registerField(u'proxy_username', self.usernameEdit)
        self.selectPage.registerField(u'proxy_password', self.passwordEdit)
        self.selectPage.registerField(
            u'openlp1_location', self.openlp1LocationEdit)
        self.licenseDetailsPage.registerField(
            u'license_version', self.versionNameEdit)
        self.licenseDetailsPage.registerField(
            u'license_copyright', self.copyrightEdit)
        self.licenseDetailsPage.registerField(
            u'license_permissions', self.permissionsEdit)

    def setDefaults(self):
        settings = QtCore.QSettings()
        settings.beginGroup(self.bibleplugin.settingsSection)
        self.restart()
        self.finishButton.setVisible(False)
        self.cancelButton.setVisible(True)
        self.setField(u'source_format', QtCore.QVariant(0))
        self.setField(u'osis_location', QtCore.QVariant(''))
        self.setField(u'csv_booksfile', QtCore.QVariant(''))
        self.setField(u'csv_versefile', QtCore.QVariant(''))
        self.setField(u'opensong_file', QtCore.QVariant(''))
        self.setField(u'web_location', QtCore.QVariant(WebDownload.Crosswalk))
        self.setField(u'web_biblename',
            QtCore.QVariant(self.bibleComboBox.currentIndex()))
        self.setField(u'proxy_server',
            settings.value(u'proxy address', QtCore.QVariant(u'')))
        self.setField(u'proxy_username',
            settings.value(u'proxy username', QtCore.QVariant(u'')))
        self.setField(u'proxy_password',
            settings.value(u'proxy password', QtCore.QVariant(u'')))
        self.setField(u'openlp1_location', QtCore.QVariant(''))
        self.setField(u'license_version',
            QtCore.QVariant(self.versionNameEdit.text()))
        self.setField(u'license_copyright',
            QtCore.QVariant(self.copyrightEdit.text()))
        self.setField(u'license_permissions',
            QtCore.QVariant(self.permissionsEdit.text()))
        self.onLocationComboBoxChanged(WebDownload.Crosswalk)
        settings.endGroup()

    def loadWebBibles(self):
        """
        Load the list of Crosswalk and BibleGateway bibles.
        """
        # Load Crosswalk Bibles.
        filepath = AppLocation.get_directory(AppLocation.PluginsDir)
        filepath = os.path.join(filepath, u'bibles', u'resources')
        books_file = None
        try:
            self.web_bible_list[WebDownload.Crosswalk] = {}
            books_file = open(
                os.path.join(filepath, u'crosswalkbooks.csv'), 'rb')
            dialect = csv.Sniffer().sniff(books_file.read(1024))
            books_file.seek(0)
            books_reader = csv.reader(books_file, dialect)
            for line in books_reader:
                ver = unicode(line[0], u'utf-8')
                name = unicode(line[1], u'utf-8')
                self.web_bible_list[WebDownload.Crosswalk][ver] = name.strip()
        except IOError:
            log.exception(u'Crosswalk resources missing')
        finally:
            if books_file:
                books_file.close()
        # Load BibleGateway Bibles.
        books_file = None
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
                self.web_bible_list[WebDownload.BibleGateway][ver] = \
                    name.strip()
        except IOError:
            log.exception(u'Biblegateway resources missing')
        finally:
            if books_file:
                books_file.close()
        # Load and Bibleserver Bibles.
        filepath = AppLocation.get_directory(AppLocation.PluginsDir)
        filepath = os.path.join(filepath, u'bibles', u'resources')
        books_file = None
        try:
            self.web_bible_list[WebDownload.Bibleserver] = {}
            books_file = open(
                os.path.join(filepath, u'bibleserver.csv'), 'rb')
            dialect = csv.Sniffer().sniff(books_file.read(1024))
            books_file.seek(0)
            books_reader = csv.reader(books_file, dialect)
            for line in books_reader:
                ver = unicode(line[0], u'utf-8')
                name = unicode(line[1], u'utf-8')
                self.web_bible_list[WebDownload.Bibleserver][ver] = name.strip()
        except IOError, UnicodeError:
            log.exception(u'Bibleserver resources missing')
        finally:
            if books_file:
                books_file.close()

    def getFileName(self, title, editbox, filters=u''):
        """
        Opens a QFileDialog and saves the filename to the given editbox.

        ``title``
            The title of the dialog (unicode).

        ``editbox``
            A editbox (QLineEdit).

        ``filters``
            The file extension filters. It should contain the file description as
            well as the file extension. For example::

                u'openlp.org (*.bible)'
        """
        if filters:
            filters += u';;'
        filters += u'%s (*)' % translate('BiblesPlugin.ImportWizardForm',
            'All Files')
        filename = QtGui.QFileDialog.getOpenFileName(self, title,
            os.path.dirname(SettingsManager.get_last_dir(
            self.bibleplugin.settingsSection, 1)), filters)
        if filename:
            editbox.setText(filename)
            SettingsManager.set_last_dir(
                self.bibleplugin.settingsSection, filename, 1)

    def incrementProgressBar(self, status_text):
        log.debug(u'IncrementBar %s', status_text)
        self.importProgressLabel.setText(status_text)
        self.importProgressBar.setValue(self.importProgressBar.value() + 1)
        Receiver.send_message(u'openlp_process_events')

    def preImport(self):
        """
        Prepare the UI for the import.
        """
        bible_type = self.field(u'source_format').toInt()[0]
        self.finishButton.setVisible(False)
        self.importProgressBar.setMinimum(0)
        self.importProgressBar.setMaximum(1188)
        self.importProgressBar.setValue(0)
        if bible_type == BibleFormat.WebDownload:
            self.importProgressLabel.setText(translate(
                'BiblesPlugin.ImportWizardForm',
                'Starting Registering bible...'))
        else:
            self.importProgressLabel.setText(translate(
                'BiblesPlugin.ImportWizardForm', 'Starting import...'))
        Receiver.send_message(u'openlp_process_events')

    def performImport(self):
        """
        Perform the actual import.
        """
        bible_type = self.field(u'source_format').toInt()[0]
        license_version = unicode(self.field(u'license_version').toString())
        license_copyright = unicode(self.field(u'license_copyright').toString())
        license_permissions = \
            unicode(self.field(u'license_permissions').toString())
        importer = None
        if bible_type == BibleFormat.OSIS:
            # Import an OSIS bible.
            importer = self.manager.import_bible(BibleFormat.OSIS,
                name=license_version,
                filename=unicode(self.field(u'osis_location').toString())
            )
        elif bible_type == BibleFormat.CSV:
            # Import a CSV bible.
            importer = self.manager.import_bible(BibleFormat.CSV,
                name=license_version,
                booksfile=unicode(self.field(u'csv_booksfile').toString()),
                versefile=unicode(self.field(u'csv_versefile').toString())
            )
        elif bible_type == BibleFormat.OpenSong:
            # Import an OpenSong bible.
            importer = self.manager.import_bible(BibleFormat.OpenSong,
                name=license_version,
                filename=unicode(self.field(u'opensong_file').toString())
            )
        elif bible_type == BibleFormat.WebDownload:
            # Import a bible from the web.
            self.importProgressBar.setMaximum(1)
            download_location = self.field(u'web_location').toInt()[0]
            bible_version = unicode(self.bibleComboBox.currentText())
            if download_location == WebDownload.Crosswalk:
                bible = \
                    self.web_bible_list[WebDownload.Crosswalk][bible_version]
            elif download_location == WebDownload.BibleGateway:
                bible = \
                    self.web_bible_list[WebDownload.BibleGateway][bible_version]
            elif download_location == WebDownload.Bibleserver:
                bible = \
                    self.web_bible_list[WebDownload.Bibleserver][bible_version]
            importer = self.manager.import_bible(
                BibleFormat.WebDownload,
                name=license_version,
                download_source=WebDownload.get_name(download_location),
                download_name=bible,
                proxy_server=unicode(self.field(u'proxy_server').toString()),
                proxy_username=\
                    unicode(self.field(u'proxy_username').toString()),
                proxy_password=unicode(self.field(u'proxy_password').toString())
            )
        elif bible_type == BibleFormat.OpenLP1:
            # Import an openlp.org 1.x bible.
            importer = self.manager.import_bible(BibleFormat.OpenLP1,
                name=license_version,
                filename=unicode(self.field(u'openlp1_location').toString())
            )
        if importer.do_import():
            self.manager.save_meta_data(license_version, license_version,
                license_copyright, license_permissions)
            self.manager.reload_bibles()
            if bible_type == BibleFormat.WebDownload:
                self.importProgressLabel.setText(
                    translate('BiblesPlugin.ImportWizardForm', 'Registered '
                    'bible. Please note, that verses will be downloaded on\n'
                    'demand and thus an internet connection is required.'))
            else:
                self.importProgressLabel.setText(translate(
                    'BiblesPlugin.ImportWizardForm', 'Finished import.'))
        else:
            self.importProgressLabel.setText(translate(
                'BiblesPlugin.ImportWizardForm', 'Your Bible import failed.'))
            delete_database(self.bibleplugin.settingsSection, importer.file)

    def postImport(self):
        self.importProgressBar.setValue(self.importProgressBar.maximum())
        self.finishButton.setVisible(True)
        self.cancelButton.setVisible(False)
        Receiver.send_message(u'openlp_process_events')
