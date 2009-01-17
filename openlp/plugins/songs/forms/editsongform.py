# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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
from PyQt4 import Qt, QtCore, QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignature

from authorsform import AuthorsForm
from topicsform import TopicsForm
from songbookform import SongBookForm

from editsongdialog import Ui_EditSongDialog

from openlp.plugins.songs.lib.models import Session, Song, Author, Topic

class EditSongForm(QWidget, Ui_EditSongDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, songmanager, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.songmanager = songmanager
        self.authors_form = AuthorsForm(self.songmanager)
        self.topics_form = TopicsForm(self.songmanager)
        self.song_book_form = SongBookForm(self.songmanager)
        self.initialise()

        self.AuthorsListView.setColumnCount(2)
        self.AuthorsListView.setColumnHidden(0, True)
        self.AuthorsListView.setColumnWidth(1, 200)
        self.AuthorsListView.setShowGrid(False)
        self.AuthorsListView.setSortingEnabled(False)
        self.AuthorsListView.setAlternatingRowColors(True)
        self.savebutton = self.ButtonBox.button(QtGui.QDialogButtonBox.Save)


    def initialise(self):
        list = self.songmanager.get_authors()
        self.AuthorsSelectionComboItem.clear()
        for i in list:
            self.AuthorsSelectionComboItem.addItem( i.display_name)

    def load_song(self, songid):
        if songid == None:   # We have a new Song
            self.song = Song()
        else:
            self.songid = songid
            self.song = self.songmanager.get_song(songid)
        self.TitleEditItem.setText(self.song.title)
        self.LyricsTextEdit.setText(self.song.lyrics)
        self.CopyrightEditItem.setText(self.song.copyright)

        self.AuthorsListView.clear() # clear the results
        self.AuthorsListView.setHorizontalHeaderLabels(QtCore.QStringList(["","Author"]))
        self.AuthorsListView.setVerticalHeaderLabels(QtCore.QStringList([""]))
        self.AuthorsListView.setRowCount(0)
        for author in self.song.authors:
            c = self.AuthorsListView.rowCount()
            self.AuthorsListView.setRowCount(c+1)
            twi = QtGui.QTableWidgetItem(str(author.id))
            self.AuthorsListView.setItem(c , 0, twi)
            twi = QtGui.QTableWidgetItem(str(author.display_name))
            self.AuthorsListView.setItem(c , 1, twi)
            self.AuthorsListView.setRowHeight(c, 20)
        self._validate_song()

    @pyqtSignature("")
    def on_AddAuthorsButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.authors_form.load_form()
        self.authors_form.show()

    @pyqtSignature("")
    def on_AddTopicButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.topics_form.load_form()
        self.topics_form.show()
    @pyqtSignature("")

    def on_AddSongBookButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.song_book_form.load_form()
        self.song_book_form.show()

    def _validate_song(self):
        """
        Check the validity of the form. Only display the 'save' if the data can be saved.
        """
        valid = True   # Lets be nice and assume the data is correct.
        if len(self.TitleEditItem.displayText()) == 0: #Song title missing
            valid = False
            self._color_widget(self.TitleEditItem, True)
        else:
            self._color_widget(self.TitleEditItem, False)
        if len(self.CopyrightEditItem.displayText()) == 0: #Song title missing
            valid = False
            self._color_widget(self.CopyrightEditItem, True)
        else:
            self._color_widget(self.CopyrightEditItem, False)

        if valid:
            self.ButtonBox.addButton(self.savebutton, QtGui.QDialogButtonBox.AcceptRole) # hide the save button tile screen is valid
        else:
            self.ButtonBox.removeButton(self.savebutton) # hide the save button tile screen is valid

    def _color_widget(self, slot, invalid):
        r = Qt.QPalette(slot.palette())
        if invalid == True:
            r.setColor(Qt.QPalette.Base, Qt.QColor('darkRed'))
        else:
            r.setColor(Qt.QPalette.Base, Qt.QColor('white'))
        slot.setPalette(r)
        slot.setAutoFillBackground(True)

    def on_TitleEditItem_lostFocus(self):
        self._validate_song()
    def on_CopyrightEditItem_lostFocus(self):
        self._validate_song()
