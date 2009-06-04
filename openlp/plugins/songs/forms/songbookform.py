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
from songbookdialog import Ui_SongBookDialog
from openlp.plugins.songs.lib.classes import Book

class SongBookForm(QtGui.QDialog, Ui_SongBookDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, songmanager, parent = None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
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
        QtCore.QObject.connect(self.NameEdit,
            QtCore.SIGNAL('lostFocus()'), self.onBookNameEditLostFocus)
        QtCore.QObject.connect(self.BookSongListView,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onBooksListViewItemClicked)

    def load_form(self):
        """
        Refresh the screen and rest fields
        """
        self.BookSongListData.resetStore()
        self.onClearButtonClick() # tidy up screen
        Books = self.songmanager.get_books()
        for Book in Books:
            self.BookSongListData.addRow(Book.id,Book.name)
        row_count = self.BookSongListData.rowCount(None)
        if self.currentRow > row_count:
            # in case we have delete the last row of the table
            self.currentRow = row_count
        row = self.BookSongListData.createIndex(self.currentRow, 0)
        if row.isValid():
            self.BookSongListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
        self._validate_form()

    def onDeleteButtonClick(self):
        """
        Delete the Book is the Book is not attached to any songs
        """
        self.songmanager.delete_book(self.Book.id)
        self.load_form()

    def onBookNameEditLostFocus(self):
        self._validate_form()

    def onAddUpdateButtonClick(self):
        """
        Sent New or update details to the database
        """
        if self.Book == None:
            self.Book = Book()
        self.Book.name = unicode(self.NameEdit.displayText())
        self.Book.publisher = unicode(self.PublisherEdit.displayText())
        self.songmanager.save_book(self.Book)
        self.onClearButtonClick()
        self.load_form()

    def onClearButtonClick(self):
        """
        Tidy up screen if clear button pressed
        """
        self.NameEdit.setText(u'')
        self.PublisherEdit.setText(u'')
        self.MessageLabel.setText(u'')
        self.DeleteButton.setEnabled(False)
        self.AddUpdateButton.setEnabled(True)
        self.Book = None
        self._validate_form()

    def onBooksListViewItemClicked(self, index):
        """
        An Book has been selected display it
        If the Book is attached to a Song prevent delete
        """
        self.currentRow = index.row()
        id = int(self.BookSongListData.getId(index))
        self.Book = self.songmanager.get_book(id)

        self.NameEdit.setText(self.Book.name)
        self.PublisherEdit.setText(self.Book.publisher)
        if len(self.Book.songs) > 0:
            self.MessageLabel.setText("Book in use 'Delete' is disabled")
            self.DeleteButton.setEnabled(False)
        else:
            self.MessageLabel.setText("Book is not used")
            self.DeleteButton.setEnabled(True)
        self._validate_form()

    def _validate_form(self):
        if len(self.NameEdit.displayText()) == 0: # We need at lease a display name
            self.AddUpdateButton.setEnabled(False)
        else:
            self.AddUpdateButton.setEnabled(True)
