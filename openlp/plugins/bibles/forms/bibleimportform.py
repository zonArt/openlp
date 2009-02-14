# -*- coding: utf-8 -*-

"""
Module implementing BibleImportDialog.
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
        self.bibletype = None
        self.barmax = 0
        self.AddressEdit.setText(self.config.get_config("addressedit", ""))
        self.UsernameEdit.setText(self.config.get_config("usernameedit", ""))
        self.PasswordEdit.setText(self.config.get_config("passwordedit",""))
   
        QtCore.QObject.connect(self.LocationComboBox, QtCore.SIGNAL("activated(int)"), self.onLocationComboBox)
        QtCore.QObject.connect(self.BibleComboBox, QtCore.SIGNAL("activated(int)"), self.onBibleComboBox)

    @pyqtSignature("")
    def on_VersesFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir())
        self.VerseLocationEdit.setText(filename)
        self._save_last_directory(filename)
        self.setCSV()        
        
    @pyqtSignature("")
    def on_BooksFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir(1))
        self.BooksLocationEdit.setText(filename)
        self._save_last_directory(filename, 1)
        self.setCSV()                
    
    @pyqtSignature("")
    def on_OsisFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir(2))
        self.OSISLocationEdit.setText(filename)
        self._save_last_directory(filename, 2)
        self.setOSIS()
 
    def on_OSISLocationEdit_lostFocus(self):
        if len(self.OSISLocationEdit.displayText() ) > 0:
            self.setOSIS()
        else:
            if self.bibletype == "OSIS": # Was OSIS and is not any more stops lostFocus running mad
                self.bibletype = None        
                self.freeAll()
            
    def on_BooksLocationEdit_lostFocus(self):
        self._checkcsv()
        
    def on_VerseLocationEdit_lostFocus(self):
        self._checkcsv()
        
    def _checkcsv(self):
        if len(self.BooksLocationEdit.displayText()) > 0 or len(self.VerseLocationEdit.displayText()) > 0:
            self.setCSV()
        else:
            if self.bibletype == "CSV": # Was CSV and is not any more stops lostFocus running mad
                self.bibletype = None        
                self.freeAll()

    @pyqtSignature("")
    def on_AddressEdit_lostFocus(self):
        self.config.set_config("addressedit", str(self.AddressEdit.displayText()))
      

    @pyqtSignature("")
    def on_UsernameEdit_lostFocus(self):
        self.config.set_config("usernameedit", str(self.UsernameEdit.displayText()))
    
    @pyqtSignature("")
    def on_PasswordEdit_lostFocus(self):
        self.config.set_config("passwordedit", str(self.PasswordEdit.displayText()))
        
    def onLocationComboBox(self):
        self._checkhttp()        
        
    def onBibleComboBox(self):
        self._checkhttp()
        
    def _checkhttp(self):
        if len(self.LocationComboBox.currentText()) > 0 or \
            len(self.BibleComboBox.currentText()) >0 :
            self.setHTTP()
        else:
            if self.bibletype == "HTTP": # Was HTTP and is not any more stops lostFocus running mad
                self.bibletype = None        
                self.freeAll()

    def on_CopyrightEdit_lostFocus(self):
        pass      
        
    def on_VersionNameEdit_lostFocus(self):
        pass 
        
    def on_PermisionEdit_lostFocus(self):
        pass
        
    def on_BibleNameEdit_lostFocus(self):
        pass
        
    @pyqtSignature("")
    def on_CancelButton_clicked(self):
        Receiver().send_message("openlpstopimport") 
        self.close() 
        
    @pyqtSignature("")        
    def on_ImportButton_clicked(self):
        if self.biblemanager != None:
            if not self.bibletype == None or len(self.BibleNameEdit.displayText()) > 0:
                self.MessageLabel.setText("Import Started")
                self.ProgressBar.setMinimum(0)                    
                self.ProgressBar.setValue(0)
                self.progress = 0
                self.biblemanager.process_dialog(self)
                self._import_bible()
                self.MessageLabel.setText("Import Complete")
                self.ProgressBar.setValue(self.barmax) 
                Receiver().send_message("openlpreloadbibles")

    def setMax(self, max):
        log.debug("set Max %s", max)        
        self.barmax = max
        self.ProgressBar.setMaximum(max)        

    def incrementBar(self, text ):
        log.debug("IncrementBar %s", text)
        self.MessageLabel.setText("Import processing " + text)
        self.progress +=1
        self.ProgressBar.setValue(self.progress)
        print self.ProgressBar.value()
        print text + " " + str(self.progress)
                
    def _import_bible(self):
        log.debug("Import Bible ")        
        if self.bibletype == "OSIS":
            self.biblemanager.register_osis_file_bible(str(self.BibleNameEdit.displayText()), self.OSISLocationEdit.displayText())
        elif self.bibletype == "CSV":
            self.biblemanager.register_csv_file_bible(str(self.BibleNameEdit.displayText()), self.BooksLocationEdit.displayText(), self.VerseLocationEdit.displayText())            
        else:
            self.setMax(1) # set a value as it will not be needed
            self.biblemanager.register_http_bible(str(self.BibleComboBox.currentText()), \
                                                                                     str(self.LocationComboBox.currentText()),  \
                                                                                     str(self.AddressEdit.displayText()),  \
                                                                                     str(self.UsernameEdit .displayText()),  \
                                                                                     str(self.PasswordEdit.displayText())) 
            self.BibleNameEdit.setText(str(self.BibleComboBox.currentText()))
            
        self.biblemanager.save_meta_data(str(self.BibleNameEdit.displayText()), str(self.VersionNameEdit.displayText()), str(self.CopyrightEdit.displayText()), str(self.PermisionEdit.displayText()))
        self.bibletype = None
        self.freeAll() # free the screen state restrictions
        self.resetAll() # reset all the screen fields
        
    def blockCSV(self):
        self.BooksLocationEdit.setReadOnly(True)
        self.VerseLocationEdit.setReadOnly(True)
        self.BooksFileButton.setEnabled(False)
        self.VersesFileButton.setEnabled(False)
        
    def setCSV(self):
        self.bibletype = "CSV" 
        self.BooksLocationEdit.setReadOnly(False)
        self.VerseLocationEdit.setReadOnly(False) 
        self.BooksFileButton.setEnabled(True)
        self.VersesFileButton.setEnabled(True)
        self.blockOSIS()
        self.blockHTTP()        
        
    def setOSIS(self):
        self.bibletype = "OSIS"         
        self.OSISLocationEdit.setReadOnly(False)
        self.OsisFileButton.setEnabled(True)        
        self.blockCSV()
        self.blockHTTP()        
 
    def blockOSIS(self):
        self.OSISLocationEdit.setReadOnly(True)
        self.OsisFileButton.setEnabled(False)
        
    def setHTTP(self):
        self.bibletype = "HTTP"         
        self.LocationComboBox.setEnabled(True)
        self.BibleComboBox.setEnabled(True)        
        self.blockCSV()
        self.blockOSIS()        
 
    def blockHTTP(self):
        self.LocationComboBox.setEnabled(False)        
        self.BibleComboBox.setEnabled(False)                
        
    def freeAll(self):
        if self.bibletype == None:  # only reset if no bible type set.  
            self.BooksLocationEdit.setReadOnly(False)
            self.VerseLocationEdit.setReadOnly(False) 
            self.BooksFileButton.setEnabled(True)
            self.VersesFileButton.setEnabled(True)
            self.OSISLocationEdit.setReadOnly(False)
            self.OsisFileButton.setEnabled(True) 
            self.LocationComboBox.setEnabled(True)
            self.BibleComboBox.setEnabled(True)        

    def resetAll(self):
        self.BooksLocationEdit.setText("")
        self.VerseLocationEdit.setText("")
        self.OSISLocationEdit.setText("")
        self.BibleNameEdit.setText("")
        self.LocationComboBox.setCurrentIndex(0)
        self.BibleComboBox.setCurrentIndex(0)
