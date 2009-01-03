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
        self.candelete = False
        self.currentrow = 0
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
            #twi.setFlags(Not QtCore.Qt.ItemIsSelectable & QtCore.Qt.ItemIsEnabled) 
            twi.setFlags(QtCore.Qt.ItemIsSelectable)
            self.AuthorListView.setItem(c , 1, twi)              
            self.AuthorListView.setRowHeight(c, 20)
        c = self.AuthorListView.rowCount()
        if self.currentrow > c: # incase we have delete the last row of the table
           self.currentrow = c 
        self.AuthorListView.selectRow(self.currentrow)
    
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
    def on_DeleteButton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.candelete == True:
            self.songmanager.delete_author(self.authorid)
            self.on_ClearButton_clicked()
            self.load_form()            
    
    @pyqtSignature("")
    def on_AddUpdateButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.songmanager.save_author(str(self.DisplayEdit.displayText()),str(self.FirstNameEdit.displayText()) ,str(self.LastNameEdit.displayText()) , self.authorid)
        self.on_ClearButton_clicked()
        self.load_form()
        
        
    @pyqtSignature("")
    def on_ClearButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.authorid = 0
        self.DisplayEdit.setText("")
        self.FirstNameEdit.setText("")
        self.LastNameEdit.setText("")
        self.candelete = True
    
    @pyqtSignature("QTableWidgetItem*")
    def on_AuthorListView_itemClicked(self, item):
        """
        Slot documentation goes here.
        """
        self.currentrow = self.AuthorListView.currentRow()
        id = int(self.AuthorListView.item(self.currentrow, 0).text())
        author = self.songmanager.get_author(id)
        self.authorid = author[0]
        self.DisplayEdit.setText(author[1])
        self.FirstNameEdit.setText(author[2])
        self.LastNameEdit.setText(author[3])
        songs = self.songmanager.get_song_authors_for_author(id)
        if len(songs) > 0:
            self.MessageLabel.setText("Author is attached to Songs")
            self.candelete = False
        else:
            self.MessageLabel.setText("Author is not used")
            self.candelete = True

