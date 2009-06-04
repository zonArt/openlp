# -*- coding: utf-8 -*-
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten Tinggaard

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
        self.currentRow = 0
        self.songbook = None

        QtCore.QObject.connect(self.DeleteButton,
            QtCore.SIGNAL('pressed()'), self.onDeleteButtonClick)
        QtCore.QObject.connect(self.ClearButton,
            QtCore.SIGNAL('pressed()'), self.onClearButtonClick)
        QtCore.QObject.connect(self.AddUpdateButton,
            QtCore.SIGNAL('pressed()'), self.onAddUpdateButtonClick)
        QtCore.QObject.connect(self.DisplayEdit,
            QtCore.SIGNAL('pressed()'), self.onDisplayEditLostFocus)
        QtCore.QObject.connect(self.SongBookListView,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onSongBookListViewItemClicked)

    def load_form(self):
        """
        Refresh the screen and rest fields
        """
        self.SongBookListData.resetStore()
        self.onClearButtonClick() # tidy up screen
        SongBooks = self.songmanager.get_SongBooks()
        for SongBook in SongBooks:
            self.SongBookListData.addRow(SongBook.id,SongBook.display_name)
        row_count = self.SongBookListData.rowCount(None)
        if self.currentRow > row_count:
            # in case we have delete the last row of the table
            self.currentRow = row_count
        row = self.SongBookListData.createIndex(self.currentRow, 0)
        if row.isValid():
            self.SongBookListView.selectionModel().setCurrentIndex(row, QtGui.QItemSelectionModel.SelectCurrent)
        self._validate_form()

    def onDeleteButtonClick(self):
        """
        Delete the SongBook is the SongBook is not attached to any songs
        """
        self.songmanager.delete_SongBook(self.SongBook.id)
        self.onClearButtonClick()
        self.load_form()

    def onDisplayEditLostFocus(self):
        self._validate_form()

    def onAddUpdateButtonClick(self):
        """
        Sent New or update details to the database
        """
        if self.SongBook == None:
            self.SongBook = SongBook()
        self.SongBook.display_name = unicode(self.DisplayEdit.displayText())
        self.songmanager.save_SongBook(self.SongBook)
        self.onClearButtonClick()
        self.load_form()
        self._validate_form()

    def onClearButtonClick(self):
        """
        Tidy up screen if clear button pressed
        """
        self.DisplayEdit.setText(u'')
        self.MessageLabel.setText(u'')
        self.DeleteButton.setEnabled(False)
        self.SongBook = None
        self._validate_form()

    def onSongBookListViewItemClicked(self, index):
        """
        An SongBook has been selected display it
        If the SongBook is attached to a Song prevent delete
        """
        self.currentRow = index.row()
        id = int(self.SongBookListData.getId(index))
        self.SongBook = self.songmanager.get_SongBook(id)

        self.DisplayEdit.setText(self.SongBook.display_name)
        if len(self.SongBook.songs) > 0:
            self.MessageLabel.setText("SongBook in use 'Delete' is disabled")
            self.DeleteButton.setEnabled(False)
        else:
            self.MessageLabel.setText("SongBook is not used")
            self.DeleteButton.setEnabled(True)
        self._validate_form()

    def _validate_form(self):
        if len(self.DisplayEdit.displayText()) == 0: # We need at lease a display name
            self.AddUpdateButton.setEnabled(False)
        else:
            self.AddUpdateButton.setEnabled(True)
