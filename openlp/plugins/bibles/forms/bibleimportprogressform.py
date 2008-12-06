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

from bibleimportprogressdialog import Ui_BibleImportProgressDialog
from openlp.plugins.bibles.lib.biblemanager import BibleManager

class BibleImportProgressForm(QDialog, Ui_BibleImportProgressDialog):
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
        self.progressBar.setValue(0)
        self.progress = 0
        
    def setMax(self, max):
        self.progressBar.setMaximum(max)        

    def incrementBar(self):
        self.progress +=1
        self.progressBar.setValue(self.progress)        

        
        #self.ProgressGroupBox.hide()  # not wanted until we do some processing
    def on_buttonBox_clicked(self,button):
        print button.text()
 
class runner(QtGui.QApplication):

    def run(self):
        self.bm = BibleManager()
        self.bim = BibleImportProgressForm(self.bm)
        self.bim.show()
        self.processEvents()
        sys.exit(app.exec_())
        
if __name__ == '__main__':
    app = runner(sys.argv)
    app.run()
