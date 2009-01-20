# -*- coding: utf-8 -*-

"""
Module implementing BibleImportDialog.
"""
import sys
import os, os.path
import sys
import time

from openlp.core.resources import *

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from bibleimportdialog import Ui_BibleImportDialog
from openlp.core.lib import PluginUtils

class BibleImportForm(QDialog, Ui_BibleImportDialog, PluginUtils):
    """
    Class documentation goes here.
    """
    def __init__(self, config, biblemanager , parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.biblemanager = biblemanager
        self.config = config
   
    @pyqtSignature("")
    def on_VersesFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir())
        self.VerseLocationEdit.setText(filename)
        self._save_last_directory(filename)
        
    @pyqtSignature("")
    def on_BooksFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir())
        self.BooksLocationEdit.setText(filename)
        self._save_last_directory(filename)        
    
    @pyqtSignature("")
    def on_OsisFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',self._get_last_dir())
        self.OSISLocationEdit.setText(filename)
        self._save_last_directory(filename)        
        
    def on_OSISLocationEdit_lostFocus(self):
        if len(self.OSISLocationEdit.displayText() ) > 1:
            self.BooksLocationEdit.setReadOnly(True)
            self.VerseLocationEdit.setReadOnly(True)
        else:
            self.BooksLocationEdit.setReadOnly(False)
            self.VerseLocationEdit.setReadOnly(False)
        
    def on_BooksLocationEdit_lostFocus(self):
        if len(self.BooksLocationEdit.displayText()) > 1 or len(self.VerseLocationEdit.displayText()) > 1:
            self.OSISLocationEdit.setReadOnly(True)
        else:
            self.OSISLocationEdit.setReadOnly(False)
            
    def on_VerseLocationEdit_lostFocus(self):
        if len(self.BooksLocationEdit.displayText()) > 1 or len(self.VerseLocationEdit.displayText()) > 1:
            self.OSISLocationEdit.setReadOnly(True)
        else:
            self.OSISLocationEdit.setReadOnly(False)
            
    def on_CopyrightEdit_lostFocus(self):
        self.validate() 
        
    def on_VersionNameEdit_lostFocus(self):
        self.validate()  
        
    def on_PermisionEdit_lostFocus(self):
        self.validate()  
        
    def on_BibleNameEdit_lostFocus(self):
        self.validate()        
        
    def on_BibleImportButtonBox_clicked(self,button):
        if button.text() == "Save":
            if self.biblemanager != None:
                self.MessageLabel.setText("Import Started")
                self.ProgressBar.setValue(1)
                self.progress = 0
                self.biblemanager.process_dialog(self)
                self.biblemanager.register_osis_file_bible(str(self.BibleNameEdit.displayText()), self.OSISLocationEdit.displayText())
                self.biblemanager.save_meta_data(str(self.BibleNameEdit.displayText()), str(self.VersionNameEdit.displayText()), str(self.CopyrightEdit.displayText()), str(self.PermisionEdit.displayText()))
                self.MessageLabel.setText("Import Complete")
        elif button.text() == "Cancel":
            self.close()            

    def setMax(self, max):
        self.ProgressBar.setMaximum(max)        

    def incrementBar(self, text = None):
        if text != None:
            self.MessageLabel.setText("Import progressing with " + text)
        else:
            self.MessageLabel.setText("Import progressing")            
        self.progress +=1
        self.ProgressBar.setValue(self.progress)  
        self.update()

    def validate(self):
        valid = False
        validcount = 0
        if len(self.BibleNameEdit.displayText()) > 0:
            validcount += 1        
        if len(self.OSISLocationEdit.displayText()) > 0:
            validcount += 1
        if len(self.BooksLocationEdit.displayText()) > 0:
            validcount += 1
        if len(self.VersionNameEdit.displayText()) > 0 and len(self.CopyrightEdit.displayText()) > 0 and len(self.PermisionEdit.displayText()) > 0:
            valid = True
#        if validcount == 2  and valid:
#            self.BibleImportButtonBox.addButton(self.savebutton, QtGui.QDialogButtonBox.AcceptRole) # hide the save button tile screen is valid
#        else:
#            self.BibleImportButtonBox.removeButton(self.savebutton) # hide the save button tile screen is valid


