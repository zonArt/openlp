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

import logging

from PyQt4 import QtCore, QtGui

from songimportwizard import Ui_SongImportWizard
from openlp.core.lib import Receiver, SettingsManager, translate
#from openlp.core.utils import AppLocation
from openlp.plugins.songs.lib import SongFormat

log = logging.getLogger(__name__)

class ImportWizardForm(QtGui.QWizard, Ui_SongImportWizard):
    """
    This is the Bible Import Wizard, which allows easy importing of Bibles
    into OpenLP from other formats like OSIS, CSV and OpenSong.
    """
    log.info(u'BibleImportForm loaded')

    def __init__(self, parent, manager, songsplugin):
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
        self.registerFields()
        self.finishButton = self.button(QtGui.QWizard.FinishButton)
        self.cancelButton = self.button(QtGui.QWizard.CancelButton)
        self.manager = manager
        self.songsplugin = songsplugin
        #self.manager.set_process_dialog(self)
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
            source_format = self.field(u'source_format').toInt()[0]
            if source_format == SongFormat.OpenLyrics:
                if self.OpenLyricsFileListWidget.count() == 0:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.ImportWizardForm',
                            'No OpenLyrics Files Selected'),
                        translate('SongsPlugin.ImportWizardForm',
                            'You need to add at least one OpenLyrics '
                            'song file to import from.'))
                    self.OpenLyricsAddButton.setFocus()
                    return False
            elif source_format == SongFormat.OpenSong:
                if self.OpenSongFileListWidget.count() == 0:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.ImportWizardForm',
                            'No OpenSong Files Selected'),
                        translate('SongsPlugin.ImportWizardForm',
                            'You need to add at least one OpenSong '
                            'song file to import from.'))
                    self.OpenSongAddButton.setFocus()
                    return False
            elif source_format == SongFormat.CCLI:
                if self.CCLIFileListWidget.count() == 0:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.ImportWizardForm',
                            'No CCLI Files Selected'),
                        translate('SongsPlugin.ImportWizardForm',
                            'You need to add at least one CCLI file '
                            'to import from.'))
                    self.CCLIAddButton.setFocus()
                    return False
            elif source_format == SongFormat.CSV:
                if self.CSVFilenameEdit.text().isEmpty():
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.ImportWizardForm',
                            'No CSV File Selected'),
                        translate('SongsPlugin.ImportWizardForm',
                            'You need to specify a CSV file to import from.'))
                    self.CSVFilenameEdit.setFocus()
                    return False
            return True
        elif self.currentId() == 2:
            # Progress page
            return True

    def onCancelButtonClicked(self, checked):
        """
        Stop the import on pressing the cancel button.
        """
        log.debug('Cancel button pressed!')
        if self.currentId() == 3:
            Receiver.send_message(u'openlp_stop_song_import')

    def onCurrentIdChanged(self, id):
        if id == 3:
            self.preImport()
            self.performImport()
            self.postImport()

    def registerFields(self):
        self.SourcePage.registerField(u'source_format', self.FormatComboBox)

    def setDefaults(self):
        self.setField(u'source_format', QtCore.QVariant(0))
        self.OpenLyricsFileListWidget.clear()
        self.OpenSongFileListWidget.clear()
        self.CCLIFileListWidget.clear()
        self.CSVFilenameEdit.setText(u'')

    def getFileName(self, title, editbox):
        filename = QtGui.QFileDialog.getOpenFileName(self, title,
            SettingsManager.get_last_dir(self.songsplugin.settingsSection, 1))
        if filename:
            editbox.setText(filename)
            SettingsManager.set_last_dir(self.songsplugin.settingsSection,
                filename, 1)

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
        self.ImportProgressLabel.setText(
            translate('SongsPlugin.ImportWizardForm', 'Starting import...'))
        Receiver.send_message(u'process_events')

    def performImport(self):
        pass
#        source_format = self.field(u'source_format').toInt()[0]
#        importer = None
#        if bible_type == BibleFormat.OSIS:
#            # Import an OSIS bible
#            importer = self.manager.import_bible(BibleFormat.OSIS,
#                name=license_version,
#                filename=unicode(self.field(u'osis_location').toString())
#            )
#        elif bible_type == BibleFormat.CSV:
#            # Import a CSV bible
#            importer = self.manager.import_bible(BibleFormat.CSV,
#                name=license_version,
#                booksfile=unicode(self.field(u'csv_booksfile').toString()),
#                versefile=unicode(self.field(u'csv_versefile').toString())
#            )
#        elif bible_type == BibleFormat.OpenSong:
#            # Import an OpenSong bible
#            importer = self.manager.import_bible(BibleFormat.OpenSong,
#                name=license_version,
#                filename=unicode(self.field(u'opensong_file').toString())
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
#                proxy_server=unicode(self.field(u'proxy_server').toString()),
#                proxy_username=unicode(self.field(u'proxy_username').toString()),
#                proxy_password=unicode(self.field(u'proxy_password').toString())
#            )
#        success = importer.do_import()
#        if success:
#            self.manager.save_meta_data(license_version, license_version,
#                license_copyright, license_permission)
#            self.manager.reload_bibles()
#            self.ImportProgressLabel.setText(translate('SongsPlugin.SongImportForm', 'Finished import.'))
#        else:
#            self.ImportProgressLabel.setText(
#                translate('SongsPlugin.SongImportForm', 'Your Bible import failed.'))
#            importer.delete()

    def postImport(self):
        self.ImportProgressBar.setValue(self.ImportProgressBar.maximum())
        self.finishButton.setVisible(True)
        self.cancelButton.setVisible(False)
        Receiver.send_message(u'process_events')
