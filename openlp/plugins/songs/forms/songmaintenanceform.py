# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

from PyQt4 import QtGui, QtCore
from sqlalchemy.sql import and_

from openlp.core.lib import Receiver, translate
from openlp.plugins.songs.forms import AuthorsForm, TopicsForm, SongBookForm
from openlp.plugins.songs.lib.db import Author, Book, Topic, Song
from songmaintenancedialog import Ui_SongMaintenanceDialog

class SongMaintenanceForm(QtGui.QDialog, Ui_SongMaintenanceDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, songmanager, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.songmanager = songmanager
        self.authorform = AuthorsForm(self)
        self.topicform = TopicsForm(self)
        self.bookform = SongBookForm(self)
        QtCore.QObject.connect(self.AuthorAddButton,
            QtCore.SIGNAL(u'pressed()'), self.onAuthorAddButtonClick)
        QtCore.QObject.connect(self.TopicAddButton,
            QtCore.SIGNAL(u'pressed()'), self.onTopicAddButtonClick)
        QtCore.QObject.connect(self.BookAddButton,
            QtCore.SIGNAL(u'pressed()'), self.onBookAddButtonClick)
        QtCore.QObject.connect(self.AuthorEditButton,
            QtCore.SIGNAL(u'pressed()'), self.onAuthorEditButtonClick)
        QtCore.QObject.connect(self.TopicEditButton,
            QtCore.SIGNAL(u'pressed()'), self.onTopicEditButtonClick)
        QtCore.QObject.connect(self.BookEditButton,
            QtCore.SIGNAL(u'pressed()'), self.onBookEditButtonClick)
        QtCore.QObject.connect(self.AuthorDeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onAuthorDeleteButtonClick)
        QtCore.QObject.connect(self.TopicDeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onTopicDeleteButtonClick)
        QtCore.QObject.connect(self.BookDeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onBookDeleteButtonClick)

    def exec_(self):
        self.TypeListWidget.setCurrentRow(0)
        self.resetAuthors()
        self.resetTopics()
        self.resetBooks()
        self.TypeListWidget.setFocus()
        return QtGui.QDialog.exec_(self)

    def _getCurrentItemId(self, ListWidget):
        item = ListWidget.currentItem()
        if item:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            return item_id
        else:
            return -1

    def _deleteItem(self, item_class, list_widget, reset_func, dlg_title,
        del_text, err_text, sel_text):
        item_id = self._getCurrentItemId(list_widget)
        if item_id != -1:
            item = self.songmanager.get_object(item_class, item_id)
            if item and len(item.songs) == 0:
                if QtGui.QMessageBox.warning(self, dlg_title, del_text,
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No |
                    QtGui.QMessageBox.Yes)) == QtGui.QMessageBox.Yes:
                    self.songmanager.delete_object(item_class, item.id)
                    reset_func()
            else:
                QtGui.QMessageBox.critical(self, dlg_title, err_text)
        else:
            QtGui.QMessageBox.critical(self, dlg_title, sel_text)

    def resetAuthors(self):
        """
        Reloads the Authors list.
        """
        self.AuthorsListWidget.clear()
        authors = self.songmanager.get_all_objects(Author,
            order_by_ref=Author.display_name)
        for author in authors:
            if author.display_name:
                author_name = QtGui.QListWidgetItem(author.display_name)
            else:
                author_name = QtGui.QListWidgetItem(
                    u'%s %s' % (author.first_name, author.last_name))
            author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListWidget.addItem(author_name)
        if self.AuthorsListWidget.count() == 0:
            self.AuthorDeleteButton.setEnabled(False)
            self.AuthorEditButton.setEnabled(False)
        else:
            self.AuthorDeleteButton.setEnabled(True)
            self.AuthorEditButton.setEnabled(True)

    def resetTopics(self):
        """
        Reloads the Topics list.
        """
        self.TopicsListWidget.clear()
        topics = self.songmanager.get_all_objects(Topic,
            order_by_ref=Topic.name)
        for topic in topics:
            topic_name = QtGui.QListWidgetItem(topic.name)
            topic_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(topic.id))
            self.TopicsListWidget.addItem(topic_name)
        if self.TopicsListWidget.count() == 0:
            self.TopicDeleteButton.setEnabled(False)
            self.TopicEditButton.setEnabled(False)
        else:
            self.TopicDeleteButton.setEnabled(True)
            self.TopicEditButton.setEnabled(True)

    def resetBooks(self):
        """
        Reloads the Books list.
        """
        self.BooksListWidget.clear()
        books = self.songmanager.get_all_objects(Book, order_by_ref=Book.name)
        for book in books:
            book_name = QtGui.QListWidgetItem(u'%s (%s)' % (book.name,
                book.publisher))
            book_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(book.id))
            self.BooksListWidget.addItem(book_name)
        if self.BooksListWidget.count() == 0:
            self.BookDeleteButton.setEnabled(False)
            self.BookEditButton.setEnabled(False)
        else:
            self.BookDeleteButton.setEnabled(True)
            self.BookEditButton.setEnabled(True)

    def checkAuthor(self, new_author, edit=False):
        """
        Returns False if the given Author is already in the list otherwise
        True.
        """
        authors = self.songmanager.get_all_objects(Author,
            and_(Author.first_name == new_author.first_name,
                Author.last_name == new_author.last_name,
                Author.display_name == new_author.display_name))
        if len(authors) > 0:
            # If we edit an existing Author, we need to make sure that we do
            # not return False when nothing has changed (because this would
            # cause an error message later on).
            if edit:
                if authors[0].id == new_author.id:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def checkTopic(self, new_topic, edit=False):
        """
        Returns False if the given Topic is already in the list otherwise True.
        """
        topics = self.songmanager.get_all_objects(Topic,
            Topic.name == new_topic.name)
        if len(topics) > 0:
            # If we edit an existing Topic, we need to make sure that we do
            # not return False when nothing has changed (because this would
            # cause an error message later on).
            if edit:
                if topics[0].id == new_topic.id:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def checkBook(self, new_book, edit=False):
        """
        Returns False if the given Book is already in the list otherwise True.
        """
        books = self.songmanager.get_all_objects(Book,
            and_(Book.name == new_book.name,
                Book.publisher == new_book.publisher))
        if len(books) > 0:
            # If we edit an existing Book, we need to make sure that we do
            # not return False when nothing has changed (because this would
            # cause an error message later on).
            if edit:
                if books[0].id == new_book.id:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True

    def onAuthorAddButtonClick(self):
        self.authorform.setAutoDisplayName(True)
        if self.authorform.exec_():
            author = Author.populate(
                first_name=unicode(self.authorform.FirstNameEdit.text()),
                last_name=unicode(self.authorform.LastNameEdit.text()),
                display_name=unicode(self.authorform.DisplayEdit.text()))
            if self.checkAuthor(author):
                if self.songmanager.save_object(author):
                    self.resetAuthors()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                        translate('SongsPlugin.SongMaintenanceForm',
                        'Could not add your author.'))
            else:
                QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm',
                    'This author already exists.'))

    def onTopicAddButtonClick(self):
        if self.topicform.exec_():
            topic = Topic.populate(name=unicode(self.topicform.NameEdit.text()))
            if self.checkTopic(topic):
                if self.songmanager.save_object(topic):
                    self.resetTopics()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                        translate('SongsPlugin.SongMaintenanceForm',
                        'Could not add your topic.'))
            else:
                QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm',
                    'This topic already exists.'))

    def onBookAddButtonClick(self):
        if self.bookform.exec_():
            book = Book.populate(name=unicode(self.bookform.NameEdit.text()),
                publisher=unicode(self.bookform.PublisherEdit.text()))
            if self.checkBook(book):
                if self.songmanager.save_object(book):
                    self.resetBooks()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                        translate('SongsPlugin.SongMaintenanceForm',
                        'Could not add your book.'))
            else:
                QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm',
                    'This book already exists.'))

    def onAuthorEditButtonClick(self):
        author_id = self._getCurrentItemId(self.AuthorsListWidget)
        if author_id != -1:
            author = self.songmanager.get_object(Author, author_id)
            self.authorform.setAutoDisplayName(False)
            self.authorform.FirstNameEdit.setText(author.first_name)
            self.authorform.LastNameEdit.setText(author.last_name)
            self.authorform.DisplayEdit.setText(author.display_name)
            # Save the author's first and last name as well as the display name
            # for the case that they have to be restored.
            temp_first_name = author.first_name
            temp_last_name = author.last_name
            temp_display_name = author.display_name
            if self.authorform.exec_(False):
                author.first_name = unicode(
                    self.authorform.FirstNameEdit.text())
                author.last_name = unicode(self.authorform.LastNameEdit.text())
                author.display_name = unicode(
                    self.authorform.DisplayEdit.text())
                if self.checkAuthor(author, True):
                    if self.songmanager.save_object(author):
                        self.resetAuthors()
                        Receiver.send_message(u'songs_load_list')
                    else:
                        QtGui.QMessageBox.critical(self,
                            translate('SongsPlugin.SongMaintenanceForm',
                            'Error'),
                            translate('SongsPlugin.SongMaintenanceForm',
                            'Could not save your changes.'))
                elif QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm', 'The author %s'
                    ' already exists. Would you like to make songs with author '
                    '%s use the existing author %s?' % (author.display_name,
                    temp_display_name, author.display_name)),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No |
                    QtGui.QMessageBox.Yes)) == QtGui.QMessageBox.Yes:
                    self.mergeAuthors(author)
                    self.resetAuthors()
                    Receiver.send_message(u'songs_load_list')
                else:
                    # We restore the author's old first and last name as well as
                    # his display name.
                    author.first_name = temp_first_name
                    author.last_name = temp_last_name
                    author.display_name = temp_display_name
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                        translate('SongsPlugin.SongMaintenanceForm',
                        'Could not save your modified author, because he '
                        'already exists.'))

    def onTopicEditButtonClick(self):
        topic_id = self._getCurrentItemId(self.TopicsListWidget)
        if topic_id != -1:
            topic = self.songmanager.get_object(Topic, topic_id)
            self.topicform.NameEdit.setText(topic.name)
            # Save the topic's name for the case that he has to be restored.
            temp_name = topic.name
            if self.topicform.exec_(False):
                topic.name = unicode(self.topicform.NameEdit.text())
                if self.checkTopic(topic, True):
                    if self.songmanager.save_object(topic):
                        self.resetTopics()
                    else:
                        QtGui.QMessageBox.critical(self,
                            translate('SongsPlugin.SongMaintenanceForm',
                            'Error'),
                            translate('SongsPlugin.SongMaintenanceForm',
                            'Could not save your changes.'))
                elif QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm', 'The topic %s '
                    'already exists. Would you like to make songs with topic %s'
                    ' use the existing topic %s?' % (topic.name, temp_name,
                    topic.name)),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No |
                    QtGui.QMessageBox.Yes)) == QtGui.QMessageBox.Yes:
                    self.mergeTopics(topic)
                    self.resetTopics()
                else:
                    # We restore the topics's old name.
                    topic.name = temp_name
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                        translate('SongsPlugin.SongMaintenanceForm',
                        'Could not save your modified topic, because it '
                        'already exists.'))

    def onBookEditButtonClick(self):
        book_id = self._getCurrentItemId(self.BooksListWidget)
        if book_id != -1:
            book = self.songmanager.get_object(Book, book_id)
            if book.publisher is None:
                book.publisher = u''
            self.bookform.NameEdit.setText(book.name)
            self.bookform.PublisherEdit.setText(book.publisher)
            # Save the book's name and publisher for the case that they have to
            # be restored.
            temp_name = book.name
            temp_publisher = book.publisher
            if self.bookform.exec_(False):
                book.name = unicode(self.bookform.NameEdit.text())
                book.publisher = unicode(self.bookform.PublisherEdit.text())
                if self.checkBook(book, True):
                    if self.songmanager.save_object(book):
                        self.resetBooks()
                    else:
                        QtGui.QMessageBox.critical(self,
                            translate('SongsPlugin.SongMaintenanceForm',
                            'Error'),
                            translate('SongsPlugin.SongMaintenanceForm',
                            'Could not save your changes.'))
                elif QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm', 'The book %s '
                    'already exists. Would you like to make songs with book %s '
                    'use the existing book %s?' % (book.name, temp_name,
                    book.name)),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No |
                    QtGui.QMessageBox.Yes)) == QtGui.QMessageBox.Yes:
                    self.mergeBooks(book)
                    self.resetBooks()
                else:
                    # We restore the book's old name and publisher.
                    book.name = temp_name
                    book.publisher = temp_publisher

    def mergeAuthors(self, old_author):
        """
        Merges two authors into one author.
        
        ``old_author``
            The author which will be deleted afterwards.
        """
        existing_author = self.songmanager.get_object_filtered(Author,
            and_(Author.first_name == old_author.first_name,
                Author.last_name == old_author.last_name, 
                Author.display_name == old_author.display_name))
        songs = self.songmanager.get_all_objects(Song,
            Song.authors.contains(old_author))
        for song in songs:
            # We check if the song has already existing_author as author. If
            # that is not the case we add it.
            if existing_author not in song.authors:
                song.authors.append(existing_author)
            song.authors.remove(old_author)
            self.songmanager.save_object(song)
        self.songmanager.delete_object(Author, old_author.id)

    def mergeTopics(self, old_topic):
        """
        Merges two topics into one topic.
        
        ``old_topic``
            The topic which will be deleted afterwards.
        """
        existing_topic = self.songmanager.get_object_filtered(Topic,
            Topic.name == old_topic.name)
        songs = self.songmanager.get_all_objects(Song,
            Song.topics.contains(old_topic))
        for song in songs:
            # We check if the song has already existing_topic as topic. If that
            # is not the case we add it.
            if existing_topic not in song.topics:
                song.topics.append(existing_topic)
            song.topics.remove(old_topic)
            self.songmanager.save_object(song)
        self.songmanager.delete_object(Topic, old_topic.id)

    def mergeBooks(self, old_book):
        """
        Merges two books into one book.
        
        ``old_book``
            The book which will be deleted afterwards.
        """
        existing_book = self.songmanager.get_object_filtered(Book,
            and_(Book.name == old_book.name,
                Book.publisher == old_book.publisher))
        songs = self.songmanager.get_all_objects(Song,
            Song.song_book_id == old_book.id)
        for song in songs:
            song.song_book_id = existing_book.id
            self.songmanager.save_object(song)
        self.songmanager.delete_object(Book, old_book.id)

    def onAuthorDeleteButtonClick(self):
        """
        Delete the author if the author is not attached to any songs.
        """
        self._deleteItem(Author, self.AuthorsListWidget, self.resetAuthors,
            translate('SongsPlugin.SongMaintenanceForm', 'Delete Author'),
            translate('SongsPlugin.SongMaintenanceForm',
                'Are you sure you want to delete the selected author?'),
            translate('SongsPlugin.SongMaintenanceForm',
                'This author cannot be deleted, they are currently '
                'assigned to at least one song.'),
            translate('SongsPlugin.SongMaintenanceForm', 'No author selected!'))

    def onTopicDeleteButtonClick(self):
        """
        Delete the Book is the Book is not attached to any songs.
        """
        self._deleteItem(Topic, self.TopicsListWidget, self.resetTopics,
            translate('SongsPlugin.SongMaintenanceForm', 'Delete Topic'),
            translate('SongsPlugin.SongMaintenanceForm',
                'Are you sure you want to delete the selected topic?'),
            translate('SongsPlugin.SongMaintenanceForm',
                'This topic cannot be deleted, it is currently '
                'assigned to at least one song.'),
            translate('SongsPlugin.SongMaintenanceForm', 'No topic selected!'))

    def onBookDeleteButtonClick(self):
        """
        Delete the Book is the Book is not attached to any songs.
        """
        self._deleteItem(Book, self.BooksListWidget, self.resetBooks,
            translate('SongsPlugin.SongMaintenanceForm', 'Delete Book'),
            translate('SongsPlugin.SongMaintenanceForm',
                'Are you sure you want to delete the selected book?'),
            translate('SongsPlugin.SongMaintenanceForm',
                'This book cannot be deleted, it is currently '
                'assigned to at least one song.'),
            translate('SongsPlugin.SongMaintenanceForm', 'No book selected!'))
