# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

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
import logging
from PyQt4 import Qt, QtCore, QtGui
from openlp.core.lib import SongXMLBuilder, SongXMLParser
from openlp.plugins.songs.forms import AuthorsForm, TopicsForm, SongBookForm, \
    EditVerseForm
from openlp.plugins.songs.lib.models import Song

from editsongdialog import Ui_EditSongDialog

class EditSongForm(QtGui.QDialog, Ui_EditSongDialog):
    """
    Class to manage the editing of a song
    """
    global log
    log = logging.getLogger(u'EditSongForm')
    log.info(u'Song Editor loaded')
    def __init__(self, songmanager, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        # Connecting signals and slots
        QtCore.QObject.connect(self.AddAuthorsButton,
            QtCore.SIGNAL(u'clicked()'), self.onAddAuthorsButtonClicked)
        QtCore.QObject.connect(self.AuthorAddtoSongItem,
            QtCore.SIGNAL(u'clicked()'), self.onAuthorAddtoSongItemClicked)
        QtCore.QObject.connect(self.AuthorRemoveItem,
            QtCore.SIGNAL(u'clicked()'), self.onAuthorRemovefromSongItemClicked)
        QtCore.QObject.connect(self.AuthorsListView,
            QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.onAuthorsListViewPressed)

        QtCore.QObject.connect(self.AddTopicButton,
            QtCore.SIGNAL(u'clicked()'), self.onAddTopicButtonClicked)
        QtCore.QObject.connect(self.AddSongBookButton,
            QtCore.SIGNAL(u'clicked()'), self.onAddSongBookButtonClicked)
        QtCore.QObject.connect(self.CopyrightInsertItem,
            QtCore.SIGNAL(u'clicked()'), self.onCopyrightInsertItemTriggered)
        QtCore.QObject.connect(self.AddButton,
            QtCore.SIGNAL(u'clicked()'), self.onAddVerseButtonClicked)
        QtCore.QObject.connect(self.EditButton,
            QtCore.SIGNAL(u'clicked()'), self.onEditVerseButtonClicked)
        QtCore.QObject.connect(self.DeleteButton,
            QtCore.SIGNAL(u'clicked()'), self.onDeleteVerseButtonClicked)
        QtCore.QObject.connect(self.VerseListWidget,
            QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.onVerseListViewPressed)
        # Create other objects and forms
        self.songmanager = songmanager
        self.authors_form = AuthorsForm(self.songmanager)
        self.topics_form = TopicsForm(self.songmanager)
        self.song_book_form = SongBookForm(self.songmanager)
        self.verse_form = EditVerseForm()
        self.initialise()
        self.AuthorsListView.setSortingEnabled(False)
        self.AuthorsListView.setAlternatingRowColors(True)
        self.TopicsListView.setSortingEnabled(False)
        self.TopicsListView.setAlternatingRowColors(True)

    def initialise(self):
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()
        self.EditButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)
        self.AuthorRemoveItem.setEnabled(False)

    def loadAuthors(self):
        authors = self.songmanager.get_authors()
        self.AuthorsSelectionComboItem.clear()
        for author in authors:
            self.AuthorsSelectionComboItem.addItem(author.display_name)

    def loadTopics(self):
        topics = self.songmanager.get_topics()
        self.SongTopicCombo.clear()
        for topic in topics:
            self.SongTopicCombo.addItem(topic.name)

    def loadBooks(self):
        books = self.songmanager.get_books()
        self.SongbookCombo.clear()
        self.SongbookCombo.addItem(u' ')
        for book in books:
            self.SongbookCombo.addItem(book.name)

    def newSong(self):
        log.debug(u'New Song')
        self.song = Song()
        self.TitleEditItem.setText(u'')
        self.AlternativeEdit.setText(u'')
        self.CopyrightEditItem.setText(u'')
        self.VerseListWidget.clear()
        self.AuthorsListView.clear()
        self.TopicsListView.clear()

    def loadSong(self, id):
        log.debug(u'Load Song')
        self.song = self.songmanager.get_song(id)
        self.TitleEditItem.setText(self.song.title)
        title = self.song.search_title.split(u'@')
        if self.song.song_book_id != 0:
            book_name = self.songmanager.get_book(self.song.song_book_id)

        if len(title) > 1:
            self.AlternativeEdit.setText(title[1])
        self.CopyrightEditItem.setText(self.song.copyright)
        self.VerseListWidget.clear()
        #lazy xml migration for now
        if self.song.lyrics.startswith(u'<?xml version='):
            songXML=SongXMLParser(self.song.lyrics)
            verseList = songXML.get_verses()
            for verse in verseList:
                self.VerseListWidget.addItem(verse[1])
        else:
            verses = self.song.lyrics.split(u'\n\n')
            for verse in verses:
                self.VerseListWidget.addItem(verse)
        # clear the results
        self.AuthorsListView.clear()
        for author in self.song.authors:
            author_name = QtGui.QListWidgetItem(unicode(author.display_name))
            author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListView.addItem(author_name)
        # clear the results
        self.TopicsListView.clear()
        for topics in self.song.topics:
            author_name = QtGui.QListWidgetItem(unicode(author.display_name))
            author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListView.addItem(author_name)
        self._validate_song()

    def onAuthorAddtoSongItemClicked(self):
        author_name = unicode(self.AuthorsSelectionComboItem.currentText())
        author = self.songmanager.get_author_by_name(author_name)
        self.song.authors.append(author)
        author_name = QtGui.QListWidgetItem(unicode(author.display_name))
        author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
        self.AuthorsListView.addItem(author_name)

    def onAuthorsListViewPressed(self):
        self.AuthorRemoveItem.setEnabled(True)

    def onAuthorRemovefromSongItemClicked(self):
        self.AuthorRemoveItem.setEnabled(False)
        item = self.AuthorsListView.currentItem()
        author_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        author = self.songmanager.get_author(author_id)
        self.song.authors.remove(author)
        row = self.AuthorsListView.row(item)
        self.AuthorsListView.takeItem(row)
        self.AuthorRemoveItem.setEnabled(False)

    def onAddAuthorsButtonClicked(self):
        """
        Slot documentation goes here.
        """
        self.authors_form.load_form()
        self.authors_form.exec_()
        self.loadAuthors()

    def onAddTopicButtonClicked(self):
        """
        Slot documentation goes here.
        """
        self.topics_form.load_form()
        self.topics_form.exec_()
        self.loadTopics()

    def onAddSongBookButtonClicked(self):
        """
        Slot documentation goes here.
        """
        self.song_book_form.load_form()
        self.song_book_form.exec_()
        self.loadBooks()

    def onVerseListViewPressed(self):
        self.EditButton.setEnabled(True)
        self.DeleteButton.setEnabled(True)

    def onAddVerseButtonClicked(self):
        self.verse_form.setVerse(u'')
        self.verse_form.exec_()
        self.VerseListWidget.addItem(self.verse_form.getVerse())

    def onEditVerseButtonClicked(self):
        item = self.VerseListWidget.currentItem()
        if item is not None:
            self.verse_form.setVerse(item.text())
            self.verse_form.exec_()
            item.setText(self.verse_form.getVerse())
        self.EditButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)

    def onDeleteVerseButtonClicked(self):
        item = self.VerseListWidget.takeItem(self.VerseListWidget.currentRow())
        item = None
        self.EditButton.setEnabled(False)
        self.DeleteButton.setEnabled(False)

    def _validate_song(self):
        """
        Check the validity of the form. Only display the 'save' if the data can be saved.
        """
        log.debug(u'Validate Song')
        # Lets be nice and assume the data is correct.
        valid = True
        if len(self.TitleEditItem.displayText()) == 0:
            valid = False
        if len(self.CopyrightEditItem.displayText()) == 0:
            valid = False
        if self.VerseListWidget.count() == 0:
            valid = False
        if self.AuthorsListView.count() == 0:
            valid = False
        return valid

    def _color_widget(self, slot, invalid):
        r = Qt.QPalette(slot.palette())
        if invalid == True:
            r.setColor(Qt.QPalette.Base, Qt.QColor(u'darkRed'))
        else:
            r.setColor(Qt.QPalette.Base, Qt.QColor(u'white'))
        slot.setPalette(r)
        slot.setAutoFillBackground(True)

    def on_TitleEditItem_lostFocus(self):
        #self._validate_song()
        pass

    def onCopyrightInsertItemTriggered(self):
        text = self.CopyrightEditItem.displayText()
        pos = self.CopyrightEditItem.cursorPosition()
        text = text[:pos] + u'©' + text[pos:]
        self.CopyrightEditItem.setText(text)
        self.CopyrightEditItem.setFocus()
        self.CopyrightEditItem.setCursorPosition(pos + 1)

    def onAccept(self):
        log.debug(u'OnAccept')
        #self.song.topics.append(9) << need opject here
        if not self._validate_song():
            return
        self.song.title = unicode(self.TitleEditItem.displayText())
        self.song.copyright = unicode(self.CopyrightEditItem.displayText())
        self.song.search_title = self.TitleEditItem.displayText() + u'@'+ self.AlternativeEdit.displayText()
        self.processLyrics()
        self.processTitle()
        self.song.song_book_id = 0
#        for i in range(0, self.AuthorsListView.count()):
#            print self.AuthorsListView.item(i)
#        for i in range(0, self.TopicsListView.count()):
#            print self.TopicsListView.item(i)

        self.songmanager.save_song(self.song)
        self.close()

    def processLyrics(self):
        log.debug(u'processLyrics')
        sxml=SongXMLBuilder()
        sxml.new_document()
        sxml.add_lyrics_to_song()
        count = 1
        text = u' '
        for i in range (0, self.VerseListWidget.count()):
            sxml.add_verse_to_lyrics(u'Verse', unicode(count),  unicode(self.VerseListWidget.item(i).text()))
            text = text + unicode(self.VerseListWidget.item(i).text()) + u' '
            count += 1
        text =  text.replace("'", u'')
        text =  text.replace(u',', u'')
        text =  text.replace(u';', u'')
        text =  text.replace(u':', u'')
        text =  text.replace(u'(', u'')
        text =  text.replace(u')', u'')
        text =  text.replace(u'{', u'')
        text =  text.replace(u'}', u'')
        text =  text.replace(u'?', u'')
        self.song.search_lyrics  = unicode(text)
        self.song.lyrics = unicode(sxml.extract_xml())

    def processTitle(self):
        log.debug(u'processTitle')
        self.song.search_title =  self.song.search_title.replace("'", u'')
        self.song.search_title =  self.song.search_title.replace(u',', u'')
        self.song.search_title =  self.song.search_title.replace(u';', u'')
        self.song.search_title =  self.song.search_title.replace(u':', u'')
        self.song.search_title =  self.song.search_title.replace(u'(', u'')
        self.song.search_title =  self.song.search_title.replace(u')', u'')
        self.song.search_title =  self.song.search_title.replace(u'{', u'')
        self.song.search_title =  self.song.search_title.replace(u'}', u'')
        self.song.search_title =  self.song.search_title.replace(u'?', u'')
        self.song.search_title  = unicode(self.song.search_title)
