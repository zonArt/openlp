# -*- coding: utf-8 -*-

"""
Module implementing BibleImportDialog.
"""
import sys
import os, os.path
import sys
import time

mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..', '..', '..')))

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from bibleimportdialog import Ui_BibleImportDialog
from bibleimportprogressform import BibleImportProgressForm

from openlp.plugins.bibles.lib.biblemanager import BibleManager

class BibleImportForm(QDialog, Ui_BibleImportDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, biblemanager = None, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.biblemanager = biblemanager
        
   
    @pyqtSignature("")
    def on_VersesFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home')
        self.VerseLocationEdit.setText(filename) 
        
    @pyqtSignature("")
    def on_BooksFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home')
        self.BooksLocationEdit.setText(filename)
    
    @pyqtSignature("")
    def on_OsisFileButton_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home')
        self.OSISLocationEdit.setText(filename)
        
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
        print button.text()
        if button.text() == "Save":
            #bipf = BibleImportProgressForm()
            #bipf.show()
            if self.biblemanager != None:
                self.MessageLabel.setText("Import Started")
                self.ProgressBar.setValue(0)
                self.progress = 0
                self.biblemanager.processDialog(self)
                self.biblemanager.registerOSISFileBible(str(self.BibleNameEdit.displayText()), self.OSISLocationEdit.displayText())
                self.MessageLabel.setText("Import Complete")
        elif button.text() == "Cancel":
            self.close()            
        
    def setMax(self, max):
        self.ProgressBar.setMaximum(max)        

    def incrementBar(self):
        self.progress +=1
        self.ProgressBar.setValue(self.progress)  
        self.update() 

    def validate(self):
        print "validate"
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


