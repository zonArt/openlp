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

from songimportwizard import Ui_SongImportWizard
#from openlp.core.lib import Receiver
#from openlp.core.utils import AppLocation, variant_to_unicode
#from openlp.plugins.bibles.lib.manager import BibleFormat

log = logging.getLogger(__name__)

class ImportWizardForm(QtGui.QWizard, Ui_SongImportWizard):
    """
    This is the Bible Import Wizard, which allows easy importing of Bibles
    into OpenLP from other formats like OSIS, CSV and OpenSong.
    """
    log.info(u'BibleImportForm loaded')

    def __init__(self, parent, config, manager, songsplugin):
        """
        Instantiate the wizard, and run any extra setup we need to.

        ``parent``
            The QWidget-derived parent of the wizard.

        ``config``
            The configuration object for storing and retrieving settings.

        ``manager``
            The Bible manager.

        ``bibleplugin``
            The Bible plugin.
        """
        QtGui.QWizard.__init__(self, parent)
        self.setupUi(self)
        #self.registerFields()
        self.finishButton = self.button(QtGui.QWizard.FinishButton)
        self.cancelButton = self.button(QtGui.QWizard.CancelButton)
        self.manager = manager
        self.config = config
        self.songsplugin = songsplugin
        #self.manager.set_process_dialog(self)
        #self.web_bible_list = {}
        #self.loadWebBibles()
        #QtCore.QObject.connect(self.LocationComboBox,
#            QtCore.SIGNAL(u'currentIndexChanged(int)'),
#            self.onLocationComboBoxChanged)
#        QtCore.QObject.connect(self.OsisFileButton,
#            QtCore.SIGNAL(u'clicked()'),
#            self.onOsisFileButtonClicked)
#        QtCore.QObject.connect(self.BooksFileButton,
#            QtCore.SIGNAL(u'clicked()'),
#            self.onBooksFileButtonClicked)
#        QtCore.QObject.connect(self.CsvVersesFileButton,
#            QtCore.SIGNAL(u'clicked()'),
#            self.onCsvVersesFileButtonClicked)
#        QtCore.QObject.connect(self.OpenSongBrowseButton,
#            QtCore.SIGNAL(u'clicked()'),
#            self.onOpenSongBrowseButtonClicked)
        QtCore.QObject.connect(self.cancelButton,
            QtCore.SIGNAL(u'clicked(bool)'),
            self.onCancelButtonClicked)
#        QtCore.QObject.connect(self,
#            QtCore.SIGNAL(u'currentIdChanged(int)'),
#            self.onCurrentIdChanged)

    def exec_(self):
        """
        Run the wizard.
        """
        #self.setDefaults()
        return QtGui.QWizard.exec_(self)

    def validateCurrentPage(self):
        """
        Validate the current page before moving on to the next page.
        """
        return True
#        if self.currentId() == 0:
#            # Welcome page
#            return True
#        elif self.currentId() == 1:
#            # Select page
#            if self.field(u'source_format').toInt()[0] == BibleFormat.OSIS:
#                if self.field(u'osis_location').toString() == u'':
#                    QtGui.QMessageBox.critical(self,
#                        self.trUtf8('Invalid Bible Location'),
#                        self.trUtf8('You need to specify a file to import your '
#                            'Bible from.'),
#                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
#                    self.OSISLocationEdit.setFocus()
#                    return False
#            elif self.field(u'source_format').toInt()[0] == BibleFormat.CSV:
#                if self.field(u'csv_booksfile').toString() == u'':
#                    QtGui.QMessageBox.critical(self,
#                        self.trUtf8('Invalid Books File'),
#                        self.trUtf8('You need to specify a file with books of '
#                            'the Bible to use in the import.'),
#                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
#                    self.BooksLocationEdit.setFocus()
#                    return False
#                elif self.field(u'csv_versefile').toString() == u'':
#                    QtGui.QMessageBox.critical(self,
#                        self.trUtf8('Invalid Verse File'),
#                        self.trUtf8('You need to specify a file of Bible '
#                            'verses to import.'),
#                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
#                    self.CsvVerseLocationEdit.setFocus()
#                    return False
#            elif self.field(u'source_format').toInt()[0] == BibleFormat.OpenSong:
#                if self.field(u'opensong_file').toString() == u'':
#                    QtGui.QMessageBox.critical(self,
#                        self.trUtf8('Invalid OpenSong Bible'),
#                        self.trUtf8('You need to specify an OpenSong Bible '
#                            'file to import.'),
#                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
#                    self.OpenSongFileEdit.setFocus()
#                    return False
#            return True
#        elif self.currentId() == 2:
#            # License details
#            license_version = variant_to_unicode(self.field(u'license_version'))
#            license_copyright = variant_to_unicode(self.field(u'license_copyright'))
#            if license_version == u'':
#                QtGui.QMessageBox.critical(self,
#                    self.trUtf8('Empty Version Name'),
#                    self.trUtf8('You need to specify a version name for your '
#                        'Bible.'),
#                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
#                self.VersionNameEdit.setFocus()
#                return False
#            elif license_copyright == u'':
#                QtGui.QMessageBox.critical(self,
#                    self.trUtf8('Empty Copyright'),
#                    self.trUtf8('You need to set a copyright for your Bible! '
#                        'Bibles in the Public Domain need to be marked as '
#                        'such.'),
#                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
#                self.CopyrightEdit.setFocus()
#                return False
#            elif self.manager.exists(license_version):
#                QtGui.QMessageBox.critical(self,
#                    self.trUtf8('Bible Exists'),
#                    self.trUtf8('This Bible already exists! Please import '
#                        'a different Bible or first delete the existing one.'),
#                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
#                self.VersionNameEdit.setFocus()
#                return False
#            return True
#        if self.currentId() == 3:
#            # Progress page
#            return True

    def onCancelButtonClicked(self, checked):
        """
        Stop the import on pressing the cancel button.
        """
        log.debug('Cancel button pressed!')
        if self.currentId() == 3:
            Receiver.send_message(u'openlpstopimport')

#    def onCurrentIdChanged(self, id):
#        if id == 3:
#            self.preImport()
#            self.performImport()
#            self.postImport()

    def registerFields(self):
        pass
#        self.SourcePage.registerField(
#            u'source_format', self.FormatComboBox)
#        self.SourcePage.registerField(
#            u'openlyrics_filename', self.OpenLyricsFilenameEdit)
#        self.SourcePage.registerField(
#            u'openlyrics_directory', self.OpenLyricsDirectoryEdit)
#        self.SourcePage.registerField(
#            u'opensong_filename', self.OpenSongFilenameEdit)
#        self.SourcePage.registerField(
#            u'opensong_directory', self.OpenSongDirectoryEdit)
#        self.SourcePage.registerField(
#            u'csv_versefile', self.CsvVerseLocationEdit)
#        self.SourcePage.registerField(
#            u'opensong_file', self.OpenSongFileEdit)
#        self.SourcePage.registerField(
#            u'web_location', self.LocationComboBox)
#        self.SourcePage.registerField(
#            u'web_biblename', self.BibleComboBox)
#        self.SourcePage.registerField(
#            u'proxy_server', self.AddressEdit)
#        self.SourcePage.registerField(
#            u'proxy_username', self.UsernameEdit)
#        self.SourcePage.registerField(
#            u'proxy_password', self.PasswordEdit)

    def setDefaults(self):
        pass
#        self.setField(u'source_format', QtCore.QVariant(0))
#        self.setField(u'openlyrics_filename', QtCore.QVariant(''))
#        self.setField(u'openlyrics_directory', QtCore.QVariant(''))
#        self.setField(u'opensong_filename', QtCore.QVariant(''))
#        self.setField(u'opensong_directory', QtCore.QVariant(''))
#        self.setField(u'csv_versefile', QtCore.QVariant(''))
#        self.setField(u'opensong_file', QtCore.QVariant(''))
#        self.setField(u'web_location', QtCore.QVariant(WebDownload.Crosswalk))
#        self.setField(u'web_biblename', QtCore.QVariant(self.BibleComboBox))
#        self.setField(u'proxy_server',
#            QtCore.QVariant(self.config.get_config(u'proxy address', '')))
#        self.setField(u'proxy_username',
#            QtCore.QVariant(self.config.get_config(u'proxy username','')))
#        self.setField(u'proxy_password',
#            QtCore.QVariant(self.config.get_config(u'proxy password','')))
#        self.setField(u'license_version', QtCore.QVariant(self.VersionNameEdit))
#        self.setField(u'license_copyright', QtCore.QVariant(self.CopyrightEdit))
#        self.setField(u'license_permission', QtCore.QVariant(self.PermissionEdit))
#        self.onLocationComboBoxChanged(WebDownload.Crosswalk)

    def getFileName(self, title, editbox):
        filename = QtGui.QFileDialog.getOpenFileName(self, title,
            self.config.get_last_dir(1))
        if filename:
            editbox.setText(filename)
            self.config.set_last_dir(filename, 1)

    def incrementProgressBar(self, status_text):
        log.debug(u'IncrementBar %s', status_text)
        self.ImportProgressLabel.setText(status_text)
        self.ImportProgressBar.setValue(self.ImportProgressBar.value() + 1)
        Receiver.send_message(u'process_events')

    def preImport(self):
        self.finishButton.setVisible(False)
        self.ImportProgressBar.setMinimum(0)
        self.ImportProgressBar.setMaximum(1188)
        self.ImportProgressBar.setValue(0)
        self.ImportProgressLabel.setText(self.trUtf8('Starting import...'))
        Receiver.send_message(u'process_events')

    def performImport(self):
        pass
#        bible_type = self.field(u'source_format').toInt()[0]
#        license_version = variant_to_unicode(self.field(u'license_version'))
#        license_copyright = variant_to_unicode(self.field(u'license_copyright'))
#        license_permission = variant_to_unicode(self.field(u'license_permission'))
#        importer = None
#        if bible_type == BibleFormat.OSIS:
#            # Import an OSIS bible
#            importer = self.manager.import_bible(BibleFormat.OSIS,
#                name=license_version,
#                filename=variant_to_unicode(self.field(u'osis_location'))
#            )
#        elif bible_type == BibleFormat.CSV:
#            # Import a CSV bible
#            importer = self.manager.import_bible(BibleFormat.CSV,
#                name=license_version,
#                booksfile=variant_to_unicode(self.field(u'csv_booksfile')),
#                versefile=variant_to_unicode(self.field(u'csv_versefile'))
#            )
#        elif bible_type == BibleFormat.OpenSong:
#            # Import an OpenSong bible
#            importer = self.manager.import_bible(BibleFormat.OpenSong,
#                name=license_version,
#                filename=variant_to_unicode(self.field(u'opensong_file'))
#            )
#        elif bible_type == BibleFormat.WebDownload:
#            # Import a bible from the web
#            self.ImportProgressBar.setMaximum(1)
#            download_location = self.field(u'web_location').toInt()[0]
#            bible_version = self.BibleComboBox.currentText()
#            if not isinstance(bible_version, unicode):
#                bible_version = unicode(bible_version, u'utf8')
#            if download_location == WebDownload.Crosswalk:
#                bible = self.web_bible_list[WebDownload.Crosswalk][bible_version]
#            elif download_location == WebDownload.BibleGateway:
#                bible = self.web_bible_list[WebDownload.BibleGateway][bible_version]
#            importer = self.manager.import_bible(
#                BibleFormat.WebDownload,
#                name=license_version,
#                download_source=WebDownload.get_name(download_location),
#                download_name=bible,
#                proxy_server=variant_to_unicode(self.field(u'proxy_server')),
#                proxy_username=variant_to_unicode(self.field(u'proxy_username')),
#                proxy_password=variant_to_unicode(self.field(u'proxy_password'))
#            )
#        success = importer.do_import()
#        if success:
#            self.manager.save_meta_data(license_version, license_version,
#                license_copyright, license_permission)
#            self.manager.reload_bibles()
#            self.ImportProgressLabel.setText(self.trUtf8('Finished import.'))
#        else:
#            self.ImportProgressLabel.setText(
#                self.trUtf8('Your Bible import failed.'))
#            importer.delete()

    def postImport(self):
        self.ImportProgressBar.setValue(self.ImportProgressBar.maximum())
        self.finishButton.setVisible(True)
        self.cancelButton.setVisible(False)
        Receiver.send_message(u'process_events')
