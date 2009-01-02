# -*- coding: utf-8 -*-
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley, Carsten Tinggaard

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
from openlp.core.resources import *

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from authorsdialog import Ui_AuthorsDialog

class AuthorsForm(QDialog, Ui_AuthorsDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, songmanager, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.AuthorListView.setColumnCount(2)
        self.AuthorListView.setColumnHidden(0, True)
        self.AuthorListView.setColumnWidth(1, 300)
        self.AuthorListView.setHorizontalHeaderLabels(QtCore.QStringList([" ","Author"])) 
        self.authorid = 0 # this is the selected authorid for updates and deletes
        
        self.songmanager = songmanager
        
    def load_form(self):
        list = self.songmanager.get_authors()
        self.AuthorListView.clear() # clear the results
        self.AuthorListView.setHorizontalHeaderLabels(QtCore.QStringList([" ","Author"]))                
        self.AuthorListView.setRowCount(0)
        for id,  txt in list:
            c = self.AuthorListView.rowCount()
            self.AuthorListView.setRowCount(c+1)
            twi = QtGui.QTableWidgetItem(str(id))
            self.AuthorListView.setItem(c , 0, twi)  
            twi = QtGui.QTableWidgetItem(str(txt))
            self.AuthorListView.setItem(c , 1, twi)              
            self.AuthorListView.setRowHeight(c, 20)
    
    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        print "bb acc"
    
    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        print "bb rej" 
        
    @pyqtSignature("")
    def on_FirstNameEdit_lostFocus(self):
        """
        Slot documentation goes here.
        """
        print "fm lf"    
        
    @pyqtSignature("")
    def on_LastNameEdit_lostFocus(self):
        """
        Slot documentation goes here.
        """
        print "ln lf"
    
    @pyqtSignature("")
    def on_DeleteButton_clicked(self):
        """
        Slot documentation goes here.
        """
        print "db clicked"
    
    @pyqtSignature("")
    def on_AddUpdateButton_clicked(self):
        """
        Slot documentation goes here.
        """
        print "au cli"
    
    @pyqtSignature("QTableWidgetItem*")
    def on_AuthorListView_itemClicked(self, item):
        """
        Slot documentation goes here.
        """
        cr = self.AuthorListView.currentRow()
        id = int(self.AuthorListView.item(cr, 0).text())
        author = self.songmanager.get_author(id)
        print author
        self.authorid = author[0]
        self.DisplayEdit.setText(author[1])
        self.FirstNameEdit.setText(author[2])
        self.LastNameEdit.setText(author[3])


