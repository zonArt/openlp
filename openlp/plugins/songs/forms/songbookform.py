# -*- coding: utf-8 -*-

"""
Module implementing SongBookForm.
"""

from openlp.core.resources import *

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
from songbookdialog import Ui_SongBookDialog

class SongBookForm(QDialog, Ui_SongBookDialog):
    """
    Class documentation goes here.
    """
    def __init__(self,songmanager,  parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.songmanager = songmanager
        
    def load_form(self):
        A = 1   

    @pyqtSignature("QTableWidgetItem*")
    def on_BookSongListView_itemClicked(self, item):
        """
        Slot documentation goes here.
        """
        print "bslv ic " + str(item)
    
    @pyqtSignature("")
    def on_DeleteButton_clicked(self):
        """
        Slot documentation goes here.
        """
        print "db c "
    
    @pyqtSignature("")
    def on_AddUpdateButton_clicked(self):
        """
        Slot documentation goes here.
        """
        print "au c "
