# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import sys
import os, os.path
import sys
import time
import logging

from openlp.core.resources import *

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from bibleimportdialog import Ui_BibleImportDialog
from openlp.core.lib import PluginUtils, Receiver


class BibleImportForm(QDialog, Ui_BibleImportDialog, PluginUtils):
    global log
    log=logging.getLogger("BibleImportForm")
    log.info("BibleImportForm loaded")    
    """
    Class documentation goes here.
    """
    def __init__(self, config, biblemanager , bibleplugin, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.biblemanager = biblemanager
        self.config = config
        self.bibleplugin = bibleplugin
        self.bible_type = None
        self.barmax = 0
        self.AddressEdit.setText(self.config.get_config("proxy_address", ""))
        self.UsernameEdit.setText(self.config.get_config("proxy_username", ""))
        self.PasswordEdit.setText(self.config.get_config("proxy_password",""))
        
        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(filepath, '..', 'resources','crosswalkbooks.csv')) 
        fbibles=open(filepath, 'r')
        self.bible_versions = {}
        self.BibleComboBox.clear()
        self.BibleComboBox.addItem("")
        for line in fbibles:
            p = line.split(",")
            self.bible_versions[p[0]] = p[1].replace('\n', '')
            self.BibleComboBox.addItem(str(p[0]))
   
        ###############   Combo Boxes
        QtCore.QObject.connect(self.LocationComboBox, QtCore.SIGNAL("activated(int)"), self.onLocationComboBoxSelected)
        QtCore.QObject.connect(self.BibleComboBox, QtCore.SIGNAL("activated(int)"), self.onBibleComboBoxSelected)

        ###############   Buttons 
        QtCore.QObject.connect(self.ImportButton, QtCore.SIGNAL("pressed()"), self.onImportButtonClicked)        
        QtCore.QObject.connect(self.CancelButton, QtCore.SIGNAL("pressed()"), self.onCancelButtonClicked)
        QtCore.QObject.connect(self.VersesFileButton, QtCore.SIGNAL("pressed()"), self.onVersesFileButtonClicked)
        QtCore.QObject.connect(self.BooksFileButton, QtCore.SIGNAL("pressed()"), self.onBooksFileButtonClicked)
        QtCore.QObject.connect(self.OsisFileButton, QtCore.SIGNAL("pressed()"), self.onOsisFileButtonClicked)        
        
        ###############   Lost Focus
        QtCore.QObject.connect(self.OSISLocationEdit, QtCore.SIGNAL("lostFocus()"), self.onOSISLocationEditLostFocus)
        QtCore.QObject.connect(self.BooksLocationEdit, QtCore.SIGNAL("lostFocus()"),self.onBooksLocationEditLostFocus)
        QtCore.QObject.connect(self.VerseLocationEdit, QtCore.SIGNAL("lostFocus()"), self.onVerseLocationEditLostFocus)
        QtCore.QObject.connect(self.AddressEdit, QtCore.SIGNAL("lostFocus()"), self.onProxyAddressEditLostFocus)
        QtCore.QObject.connect(self.UsernameEdit, QtCore.SIGNAL("lostFocus()"), self.onProxyUsernameEditLostFocus)
        QtCore.QObject.connect(self.PasswordEdit, QtCore.SIGNAL("lostFocus()"), self.onProxyPasswordEditLostFocus)        


    def onVersesFileButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir(1))
        if filename != "":
            self.VerseLocationEdit.setText(filename)            
            self._save_last_directory(filename, 1)
            self.set_cvs()        
        
    def onBooksFileButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir(2))
        if filename != "": 
            self.BooksLocationEdit.setText(filename)            
            self._save_last_directory(filename, 2)
            self.set_cvs()                
    
    def onOsisFileButtonClicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir(3))
        if filename != "":        
            self.OSISLocationEdit.setText(filename)
            self._save_last_directory(filename, 3)
            self.set_osis()
 
    def onOSISLocationEditLostFocus(self):
        if len(self.OSISLocationEdit.displayText() ) > 0:
            self.set_osis()
        else:
            if self.bible_type == "OSIS": # Was OSIS and is not any more stops lostFocus running mad
                self.bible_type = None        
                self.free_all()
            
    def onBooksLocationEditLostFocus(self):
        self.check_osis()
        
    def onVerseLocationEditLostFocus(self):
        self.check_osis()
        
    def onProxyAddressEditLostFocus(self):
        self.config.set_config("proxy_address", str(self.AddressEdit.displayText()))

    def onProxyUsernameEditLostFocus(self):
        self.config.set_config("proxy_username", str(self.UsernameEdit.displayText()))
    
    def onProxyPasswordEditLostFocus(self):
        self.config.set_config("proxy_password", str(self.PasswordEdit.displayText()))
        
    def onLocationComboBoxSelected(self):
        self.check_http()        
        
    def onBibleComboBoxSelected(self):
        self.check_http()
        self.BibleNameEdit.setText(str(self.BibleComboBox.currentText()))
        
    def onCancelButtonClicked(self):
        Receiver().send_message("openlpstopimport") 
        self.close() 
        
    def onImportButtonClicked(self):
        if self.biblemanager != None:
            if not self.bible_type == None and len(self.BibleNameEdit.displayText()) > 0:
                self.MessageLabel.setText("Import Started")
                self.ProgressBar.setMinimum(0) 
                self.setMax(65)
                self.ProgressBar.setValue(0)
                self.biblemanager.process_dialog(self)
                self._import_bible()
                self.MessageLabel.setText("Import Complete")
                self.ProgressBar.setValue(self.barmax) 
                Receiver().send_message("openlpreloadbibles") # tell bibleplugin to reload the bibles

    def set_max(self, max):
        log.debug("set Max %s", max)        
        self.barmax = max
        self.ProgressBar.setMaximum(max)        

    def increment_progress_bar(self, text ):
        log.debug("IncrementBar %s", text)
        self.MessageLabel.setText("Import processing " + text)
        self.ProgressBar.setValue(self.ProgressBar.value()+1)
                
    def _import_bible(self):
        log.debug("Import Bible ")
        if self.bible_type == "OSIS":
            self.biblemanager.register_osis_file_bible(str(self.BibleNameEdit.displayText()), self.OSISLocationEdit.displayText())
        elif self.bible_type == "CSV":
            self.biblemanager.register_csv_file_bible(str(self.BibleNameEdit.displayText()), self.BooksLocationEdit.displayText(), self.VerseLocationEdit.displayText())
        else:
            self.setMax(1) # set a value as it will not be needed
            bible = self.bible_versions[str(self.BibleComboBox.currentText())]
            self.biblemanager.register_http_bible(str(self.BibleComboBox.currentText()), \
                                                                                     str(self.LocationComboBox.currentText()),  \
                                                                                     str(bible), \
                                                                                     str(self.AddressEdit.displayText()),  \
                                                                                     str(self.UsernameEdit .displayText()),  \
                                                                                     str(self.PasswordEdit.displayText())) 
        self.biblemanager.save_meta_data(str(self.BibleNameEdit.displayText()), str(self.VersionNameEdit.displayText()), str(self.CopyrightEdit.displayText()), str(self.PermisionEdit.displayText()))
        self.bible_type = None
        self.free_all() # free the screen state restrictions
        self.reset_all() # reset all the screen fields

    def check_osis(self):
        if len(self.BooksLocationEdit.displayText()) > 0 or len(self.VerseLocationEdit.displayText()) > 0:
            self.set_cvs()
        else:
            if self.bible_type == "CSV": # Was CSV and is not any more stops lostFocus running mad
                self.bible_type = None        
                self.free_all()
        
    def check_http(self):
        if self.BibleComboBox.currentIndex() != 0 :  # First slot is blank so no bible
            self.set_http()
        else:
            if self.bible_type == "HTTP": # Was HTTP and is not any more stops lostFocus running mad
                self.bible_type = None        
                self.free_all()


    def block_csv(self):
        self.BooksLocationEdit.setReadOnly(True)
        self.VerseLocationEdit.setReadOnly(True)
        self.BooksFileButton.setEnabled(False)
        self.VersesFileButton.setEnabled(False)
        
    def set_cvs(self):
        self.bible_type = "CSV" 
        self.BooksLocationEdit.setReadOnly(False)
        self.VerseLocationEdit.setReadOnly(False) 
        self.BooksFileButton.setEnabled(True)
        self.VersesFileButton.setEnabled(True)
        self.block_osis()
        self.block_http()        
        
    def set_osis(self):
        self.bible_type = "OSIS"         
        self.OSISLocationEdit.setReadOnly(False)
        self.OsisFileButton.setEnabled(True)        
        self.block_csv()
        self.block_http()        
 
    def block_osis(self):
        self.OSISLocationEdit.setReadOnly(True)
        self.OsisFileButton.setEnabled(False)
        
    def set_http(self):
        self.bible_type = "HTTP"         
        self.LocationComboBox.setEnabled(True)
        self.BibleComboBox.setEnabled(True)        
        self.block_csv()
        self.block_osis()        
 
    def block_http(self):
        self.LocationComboBox.setEnabled(False)        
        self.BibleComboBox.setEnabled(False)                
        
    def free_all(self):
        if self.bible_type == None:  # only reset if no bible type set.  
            self.BooksLocationEdit.setReadOnly(False)
            self.VerseLocationEdit.setReadOnly(False) 
            self.BooksFileButton.setEnabled(True)
            self.VersesFileButton.setEnabled(True)
            self.OSISLocationEdit.setReadOnly(False)
            self.OsisFileButton.setEnabled(True) 
            self.LocationComboBox.setEnabled(True)
            self.BibleComboBox.setEnabled(True)        

    def reset_all(self):
        self.BooksLocationEdit.setText("")
        self.VerseLocationEdit.setText("")
        self.OSISLocationEdit.setText("")
        self.BibleNameEdit.setText("")
        self.LocationComboBox.setCurrentIndex(0)
        self.BibleComboBox.setCurrentIndex(0)
