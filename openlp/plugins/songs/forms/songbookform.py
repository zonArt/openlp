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
from openlp.core.lib import translate
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
            QtCore.SIGNAL(u'pressed()'), self.onDeleteButtonClick)
        QtCore.QObject.connect(self.ClearButton,
            QtCore.SIGNAL(u'pressed()'), self.onClearButtonClick)
        QtCore.QObject.connect(self.AddUpdateButton,
            QtCore.SIGNAL(u'pressed()'), self.onAddUpdateButtonClick)
        QtCore.QObject.connect(self.NameEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onBookNameEditLostFocus)
        QtCore.QObject.connect(self.BookSongListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onBooksListViewItemClicked)

    def load_form(self):
        """
        Refresh the screen and rest fields
        """
        self.BookSongListWidget.clear()
        self.onClearButtonClick() # tidy up screen
        books = self.songmanager.get_books()
        for book in books:
            book_name = QtGui.QListWidgetItem(book.name)
            book_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(book.id))
            self.BookSongListWidget.addItem(book_name)
        if self.currentRow >= self.BookSongListWidget.count() :
            self.BookSongListWidget.setCurrentRow(self.BookSongListWidget.count() - 1)
        else:
            self.BookSongListWidget.setCurrentRow(self.currentRow)
        self.onBooksListViewItemClicked()

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
        self.NameEdit.setFocus()

    def onBooksListViewItemClicked(self):
        """
        An Book has been selected display it
        If the Book is attached to a Song prevent delete
        """
        self.currentRow = self.BookSongListWidget.currentRow()
        item = self.BookSongListWidget.currentItem()
        item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        self.Book = self.songmanager.get_book(item_id)
        self.NameEdit.setText(self.Book.name)
        self.PublisherEdit.setText(self.Book.publisher)
        if len(self.Book.songs) > 0:
            self.MessageLabel.setText(translate(u'BookForm', u'Book in use "Delete" is disabled'))
            self.DeleteButton.setEnabled(False)
        else:
            self.MessageLabel.setText(translate(u'BookForm', u'Book in not used'))
            self.DeleteButton.setEnabled(True)
        self._validate_form()
        self.NameEdit.setFocus()

    def _validate_form(self):
        # We need at lease a display name
        if len(self.NameEdit.displayText()) == 0:
            self.AddUpdateButton.setEnabled(False)
        else:
            self.AddUpdateButton.setEnabled(True)
