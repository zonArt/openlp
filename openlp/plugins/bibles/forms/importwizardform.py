# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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
import os
import os.path

from PyQt4 import QtCore, QtGui

from bibleimportwizard import Ui_BibleImportWizard
from openlp.core.lib import Receiver

class BibleFormat(object):
    Unknown = -1
    OSIS = 0
    CSV = 1
    OpenSong = 2
    WebDownload = 3


class ImportWizardForm(QtGui.QWizard, Ui_BibleImportWizard):
    """
    This is the Bible Import Wizard, which allows easy importing of Bibles
    into OpenLP from other formats like OSIS, CSV and OpenSong.
    """

    global log
    log = logging.getLogger(u'BibleImportForm')
    log.info(u'BibleImportForm loaded')

    def __init__(self, parent, config, biblemanager, bibleplugin):
        '''
        Constructor
        '''
        QtGui.QWizard.__init__(self, parent)
        self.setupUi(self)
        self.registerFields()
        self.biblemanager = biblemanager
        self.config = config
        self.bibleplugin = bibleplugin
        self.bible_type = BibleFormat.Unknown

    def registerFields(self):
        self.SelectPage.registerField(u'source_format', self.FormatComboBox)
        self.SelectPage.registerField(u'osis_biblename', self.OsisBibleNameEdit)
        self.SelectPage.registerField(u'osis_location', self.OSISLocationEdit)
        self.SelectPage.registerField(u'csv_booksfile', self.BooksLocationEdit)
        self.SelectPage.registerField(u'csv_versefile', self.CsvVerseLocationEdit)
        self.SelectPage.registerField(u'opensong_file', self.OpenSongFileEdit)
        self.SelectPage.registerField(u'web_location', self.LocationComboBox)
        self.SelectPage.registerField(u'web_biblename', self.BibleComboBox)
        self.SelectPage.registerField(u'web_server', self.AddressEdit)
        self.SelectPage.registerField(u'web_username', self.UsernameEdit)
        self.SelectPage.registerField(u'web_password', self.PasswordEdit)
        self.LicenseDetailsPage.registerField(u'license_version', self.VersionNameEdit)
        self.LicenseDetailsPage.registerField(u'license_copyright', self.CopyrightEdit)
        self.LicenseDetailsPage.registerField(u'license_permission', self.PermissionEdit)

    def validateCurrentPage(self):
        if self.currentId() == 0:
            # Welcome page
            return True
        elif self.currentId() == 1:
            # Select page
            if self.field(u'source_format').toInt()[0] == BibleFormat.OSIS:
                if self.field(u'osis_biblename').toString() == u'':
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid Bible Name'),
                        self.trUtf8('You need to specify a name for your Bible!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.OsisBibleNameEdit.setFocus()
                    return False
                if self.field(u'osis_location').toString() == u'':
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid Bible Location'),
                        self.trUtf8('You need to specify a file to import your Bible from!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.OSISLocationEdit.setFocus()
                    return False
            elif self.field(u'source_format').toInt()[0] == BibleFormat.CSV:
                if self.field(u'csv_booksfile').toString() == QtCore.QString(u''):
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid Books File'),
                        self.trUtf8('You need to specify a file with books of the Bible to use in the import!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.BooksLocationEdit.setFocus()
                    return False
                elif self.field(u'csv_versefile').toString() == QtCore.QString(u''):
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid Verse File'),
                        self.trUtf8('You need to specify a file of Bible verses to import!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.CsvVerseLocationEdit.setFocus()
                    return False
            elif self.field(u'source_format').toInt()[0] == BibleFormat.OpenSong:
                if self.field(u'opensong_file').toString() == QtCore.QString(u''):
                    QtGui.QMessageBox.critical(self,
                        self.trUtf8('Invalid OpenSong Bible'),
                        self.trUtf8('You need to specify an OpenSong Bible file to import!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self.OpenSongFileEdit.setFocus()
                    return False
            return True

    def show(self):
        self.FormatComboBox.setCurrentIndex(0)
        self.FormatWidget.setCurrentIndex(0)
        self.WebDownloadTabWidget.setCurrentIndex(0)
        return QtGui.QWizard.show()

