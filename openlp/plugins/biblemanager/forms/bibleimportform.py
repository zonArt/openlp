# -*- coding: utf-8 -*-

"""
Module implementing BibleImportDialog.
"""
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from bibleimportdialog import Ui_BibleImportDialog

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


class runner(QtGui.QApplication):

    def run(self):
        values = ["Genesis","Matthew","Revelation"]
        self.bim = BibleImportForm()
        self.bim.show()
        self.processEvents()
        sys.exit(app.exec_())
        
if __name__ == '__main__':
    app = runner(sys.argv)
    app.run()
