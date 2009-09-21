# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import sys
import os, os.path
import sys
import time
import logging

from PyQt4 import QtCore, QtGui

from bibleimportdialog import Ui_BibleImportDialog
from openlp.core.lib import Receiver, translate


class BibleImportForm(QtGui.QDialog, Ui_BibleImportDialog):
    global log
    log=logging.getLogger(u'BibleImportForm')
    log.info(u'BibleImportForm loaded')
    """
    Class documentation goes here.
    """
    def __init__(self, config, biblemanager, bibleplugin, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.biblemanager = biblemanager
        self.config = config
        self.bibleplugin = bibleplugin
        self.bible_type = None
        self.barmax = 0
        self.tabWidget.setCurrentIndex(0)
        self.AddressEdit.setText(self.config.get_config(u'proxy_address', u''))
        self.UsernameEdit.setText(self.config.get_config(u'proxy_username',u''))
        self.PasswordEdit.setText(self.config.get_config(u'proxy_password',u''))

        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(filepath, u'..',
            u'resources',u'crosswalkbooks.csv'))
        fbibles=open(filepath, 'r')
        self.bible_versions = {}
        self.BibleComboBox.clear()
        self.BibleComboBox.addItem(u'')
        for line in fbibles:
            p = line.split(u',')
            self.bible_versions[p[0]] = p[1].replace(u'\n', u'')
            self.BibleComboBox.addItem(unicode(p[0]))

        #Combo Boxes
        QtCore.QObject.connect(self.LocationComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onLocationComboBoxSelected)
        QtCore.QObject.connect(self.BibleComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onBibleComboBoxSelected)

        #Buttons
        QtCore.QObject.connect(self.ImportButton,
            QtCore.SIGNAL(u'pressed()'), self.onImportButtonClicked)
        QtCore.QObject.connect(self.CancelButton,
            QtCore.SIGNAL(u'pressed()'), self.onCancelButtonClicked)
        QtCore.QObject.connect(self.VersesFileButton,
            QtCore.SIGNAL(u'pressed()'), self.onVersesFileButtonClicked)
        QtCore.QObject.connect(self.BooksFileButton,
            QtCore.SIGNAL(u'pressed()'), self.onBooksFileButtonClicked)
        QtCore.QObject.connect(self.OsisFileButton,
            QtCore.SIGNAL(u'pressed()'), self.onOsisFileButtonClicked)

        #Lost Focus
        QtCore.QObject.connect(self.OSISLocationEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onOSISLocationEditLostFocus)
        QtCore.QObject.connect(self.BooksLocationEdit,
            QtCore.SIGNAL(u'lostFocus()'),self.onBooksLocationEditLostFocus)
        QtCore.QObject.connect(self.VerseLocationEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onVerseLocationEditLostFocus)
        QtCore.QObject.connect(self.AddressEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onProxyAddressEditLostFocus)
        QtCore.QObject.connect(self.UsernameEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onProxyUsernameEditLostFocus)
        QtCore.QObject.connect(self.PasswordEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onProxyPasswordEditLostFocus)


    def onVersesFileButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, u'Open file',self.config.get_last_dir(1))
        if filename != u'':
            self.VerseLocationEdit.setText(filename)
            self.config.set_last_dir(filename, 1)
            self.setCsv()

    def onBooksFileButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, u'Open file',self.config.get_last_dir(2))
        if filename != u'':
            self.BooksLocationEdit.setText(filename)
            self.config.set_last_dir(filename, 2)
            self.setCsv()

    def onOsisFileButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, u'Open file',self.config.get_last_dir(3))
        if filename != u'':
            self.OSISLocationEdit.setText(filename)
            self.config.set_last_dir(filename, 3)
            self.setOsis()

    def onOSISLocationEditLostFocus(self):
        if len(self.OSISLocationEdit.displayText() ) > 0:
            self.setOsis()
        else:
            # Was OSIS and is not any more stops lostFocus running mad
            if self.bible_type == u'OSIS':
                self.bible_type = None
                self.resetScreenFieldStates()

    def onBooksLocationEditLostFocus(self):
        self.checkOsis()

    def onVerseLocationEditLostFocus(self):
        self.checkOsis()

    def onProxyAddressEditLostFocus(self):
        self.config.set_config(u'proxy_address', unicode(self.AddressEdit.displayText()))

    def onProxyUsernameEditLostFocus(self):
        self.config.set_config(u'proxy_username', unicode(self.UsernameEdit.displayText()))

    def onProxyPasswordEditLostFocus(self):
        self.config.set_config(u'proxy_password', unicode(self.PasswordEdit.displayText()))

    def onLocationComboBoxSelected(self):
        self.checkHttp()

    def onBibleComboBoxSelected(self):
        self.checkHttp()
        self.BibleNameEdit.setText(unicode(self.BibleComboBox.currentText()))

    def onCancelButtonClicked(self):
        # tell import to stop
        self.message = u'Bible import stopped'
        Receiver().send_message(u'stop_import')
        # tell bibleplugin to reload the bibles
        Receiver().send_message(u'pre_load_bibles')
        self.close()

    def onImportButtonClicked(self):
        message = u'Bible import completed'
        if self.biblemanager != None:
            if not self.bible_type == None and len(self.BibleNameEdit.displayText()) > 0:
                self.MessageLabel.setText(u'Import Started')
                self.ProgressBar.setMinimum(0)
                self.setMax(65)
                self.ProgressBar.setValue(0)
                self.biblemanager.process_dialog(self)
                status, msg = self.importBible()
                if msg is not None:
                    message = msg
                self.MessageLabel.setText(message)
                self.ProgressBar.setValue(self.barmax)
                # tell bibleplugin to reload the bibles
                Receiver().send_message(u'pre_load_bibles')
                reply = QtGui.QMessageBox.information(self,
                    translate(u'BibleMediaItem', u'Information'),
                    translate(u'BibleMediaItem', message))

    def setMax(self, max):
        log.debug(u'set Max %s', max)
        self.barmax = max
        self.ProgressBar.setMaximum(max)

    def incrementProgressBar(self, text ):
        log.debug(u'IncrementBar %s', text)
        self.MessageLabel.setText(u'Import processing ' + text)
        self.ProgressBar.setValue(self.ProgressBar.value()+1)

    def importBible(self):
        log.debug(u'Import Bible')
        message = None
        if self.bible_type == u'OSIS':
            loaded = self.biblemanager.register_osis_file_bible(
                unicode(self.BibleNameEdit.displayText()),
                self.OSISLocationEdit.displayText())
        elif self.bible_type == u'CSV':
            loaded = self.biblemanager.register_csv_file_bible(
                unicode(self.BibleNameEdit.displayText()),
                self.BooksLocationEdit.displayText(),
                self.VerseLocationEdit.displayText())
        else:
            # set a value as it will not be needed
            self.setMax(1)
            bible = self.bible_versions[
                unicode(self.BibleComboBox.currentText())]
            loaded = self.biblemanager.register_http_bible(
                unicode(self.BibleComboBox.currentText()),
                unicode(self.LocationComboBox.currentText()),
                unicode(bible), unicode(self.AddressEdit.displayText()),
                unicode(self.UsernameEdit .displayText()),
                unicode(self.PasswordEdit.displayText()))
        if loaded:
            self.biblemanager.save_meta_data(
                unicode(self.BibleNameEdit.displayText()),
                unicode(self.VersionNameEdit.displayText()),
                unicode(self.CopyrightEdit.displayText()),
                unicode(self.PermisionEdit.displayText()))
        else:
            message = u'Bible import failed'
        self.bible_type = None
        # free the screen state restrictions
        self.resetScreenFieldStates()
         # reset all the screen fields
        self.resetEntryFields()
        return loaded, message

    def checkOsis(self):
        if len(self.BooksLocationEdit.displayText()) > 0 or \
            len(self.VerseLocationEdit.displayText()) > 0:
            self.setCsv()
        else:
            # Was CSV and is not any more stops lostFocus running mad
            if self.bible_type == u'CSV':
                self.bible_type = None
                self.resetScreenFieldStates()

    def checkHttp(self):
        if self.BibleComboBox.currentIndex() != 0 :
            # First slot is blank so no bible
            self.setHttp()
        else:
            # Was HTTP and is not any more stops lostFocus running mad
            if self.bible_type == u'HTTP':
                self.bible_type = None
                self.resetScreenFieldStates()

    def blockCsv(self):
        self.BooksLocationEdit.setReadOnly(True)
        self.VerseLocationEdit.setReadOnly(True)
        self.BooksFileButton.setEnabled(False)
        self.VersesFileButton.setEnabled(False)

    def setCsv(self):
        self.bible_type = u'CSV'
        self.BooksLocationEdit.setReadOnly(False)
        self.VerseLocationEdit.setReadOnly(False)
        self.BooksFileButton.setEnabled(True)
        self.VersesFileButton.setEnabled(True)
        self.blockOsis()
        self.blockHttp()

    def setOsis(self):
        self.bible_type = u'OSIS'
        self.OSISLocationEdit.setReadOnly(False)
        self.OsisFileButton.setEnabled(True)
        self.blockCsv()
        self.blockHttp()

    def blockOsis(self):
        self.OSISLocationEdit.setReadOnly(True)
        self.OsisFileButton.setEnabled(False)

    def setHttp(self):
        self.bible_type = u'HTTP'
        self.LocationComboBox.setEnabled(True)
        self.BibleComboBox.setEnabled(True)
        self.blockCsv()
        self.blockOsis()

    def blockHttp(self):
        self.LocationComboBox.setEnabled(False)
        self.BibleComboBox.setEnabled(False)

    def resetScreenFieldStates(self):
        # only reset if no bible type set.
        if self.bible_type == None:
            self.BooksLocationEdit.setReadOnly(False)
            self.VerseLocationEdit.setReadOnly(False)
            self.BooksFileButton.setEnabled(True)
            self.VersesFileButton.setEnabled(True)
            self.OSISLocationEdit.setReadOnly(False)
            self.OsisFileButton.setEnabled(True)
            self.LocationComboBox.setEnabled(True)
            self.BibleComboBox.setEnabled(True)

    def resetEntryFields(self):
        self.BooksLocationEdit.setText(u'')
        self.VerseLocationEdit.setText(u'')
        self.OSISLocationEdit.setText(u'')
        self.BibleNameEdit.setText(u'')
        self.LocationComboBox.setCurrentIndex(0)
        self.BibleComboBox.setCurrentIndex(0)
