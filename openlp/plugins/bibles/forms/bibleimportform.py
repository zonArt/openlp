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
        self.validate()
        
    def on_BooksLocationEdit_lostFocus(self):
        self.validate()
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
                self.biblemanager.processDialog(bipf)
                self.biblemanager.registerOSISFileBible(str(self.BibleNameEdit.displayText()), self.OSISLocationEdit.displayText())
        elif button.text() == "Cancel":
            self.close()            



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



class runner(QtGui.QApplication):

    def run(self):
        values = ["Genesis","Matthew","Revelation"]
        self.bm = BibleManager("/home/timali/.openlp")
        self.bim = BibleImportForm()
        self.bim.show()
        self.processEvents()
        sys.exit(app.exec_())
        
if __name__ == '__main__':
    app = runner(sys.argv)
    app.run()
