# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
import logging

from PyQt4 import QtGui, QtCore
from sqlalchemy.sql import and_

from openlp.core.lib import Receiver, UiStrings, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.plugins.songs.forms import AuthorsForm, TopicsForm, SongBookForm
from openlp.plugins.songs.lib.db import Author, Book, Topic, Song
from songmaintenancedialog import Ui_SongMaintenanceDialog

log = logging.getLogger(__name__)


class SongMaintenanceForm(QtGui.QDialog, Ui_SongMaintenanceDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, manager, parent=None):
        """
        Constructor
        """
        super(SongMaintenanceForm, self).__init__(parent)
        self.setupUi(self)
        self.manager = manager
        self.authorform = AuthorsForm(self)
        self.topicform = TopicsForm(self)
        self.bookform = SongBookForm(self)
        # Disable all edit and delete buttons, as there is no row selected.
        self.authorsDeleteButton.setEnabled(False)
        self.authorsEditButton.setEnabled(False)
        self.topicsDeleteButton.setEnabled(False)
        self.topicsEditButton.setEnabled(False)
        self.booksDeleteButton.setEnabled(False)
        self.booksEditButton.setEnabled(False)
        # Signals
        QtCore.QObject.connect(self.authorsAddButton, QtCore.SIGNAL(u'clicked()'), self.onAuthorAddButtonClicked)
        QtCore.QObject.connect(self.topicsAddButton, QtCore.SIGNAL(u'clicked()'), self.onTopicAddButtonClicked)
        QtCore.QObject.connect(self.booksAddButton, QtCore.SIGNAL(u'clicked()'), self.onBookAddButtonClicked)
        QtCore.QObject.connect(self.authorsEditButton, QtCore.SIGNAL(u'clicked()'), self.onAuthorEditButtonClicked)
        QtCore.QObject.connect(self.topicsEditButton, QtCore.SIGNAL(u'clicked()'), self.onTopicEditButtonClicked)
        QtCore.QObject.connect(self.booksEditButton, QtCore.SIGNAL(u'clicked()'), self.onBookEditButtonClicked)
        QtCore.QObject.connect(self.authorsDeleteButton, QtCore.SIGNAL(u'clicked()'), self.onAuthorDeleteButtonClicked)
        QtCore.QObject.connect(self.topicsDeleteButton, QtCore.SIGNAL(u'clicked()'), self.onTopicDeleteButtonClicked)
        QtCore.QObject.connect(self.booksDeleteButton, QtCore.SIGNAL(u'clicked()'), self.onBookDeleteButtonClicked)
        QtCore.QObject.connect(self.authorsListWidget, QtCore.SIGNAL(u'currentRowChanged(int)'),
            self.onAuthorsListRowChanged)
        QtCore.QObject.connect(self.topicsListWidget, QtCore.SIGNAL(u'currentRowChanged(int)'),
            self.onTopicsListRowChanged)
        QtCore.QObject.connect(self.booksListWidget, QtCore.SIGNAL(u'currentRowChanged(int)'),
            self.onBooksListRowChanged)

    def exec_(self, fromSongEdit=False):
        """
        Show the dialog.

        ``fromSongEdit``
            Indicates if the maintenance dialog has been opened from song edit
            or from the media manager. Defaults to **False**.
        """
        self.fromSongEdit = fromSongEdit
        self.typeListWidget.setCurrentRow(0)
        self.resetAuthors()
        self.resetTopics()
        self.resetBooks()
        self.typeListWidget.setFocus()
        return QtGui.QDialog.exec_(self)

    def _getCurrentItemId(self, list_widget):
        """
        Get the ID of the currently selected item.

        ``list_widget``
            The list widget to examine.
        """
        item = list_widget.currentItem()
        if item:
            item_id = (item.data(QtCore.Qt.UserRole))
            return item_id
        else:
            return -1

    def _deleteItem(self, itemClass, listWidget, resetFunc, dlgTitle, del_text, err_text):
        """
        Delete an item.
        """
        item_id = self._getCurrentItemId(listWidget)
        if item_id != -1:
            item = self.manager.get_object(itemClass, item_id)
            if item and not item.songs:
                if critical_error_message_box(dlgTitle, del_text, self, True) == QtGui.QMessageBox.Yes:
                    self.manager.delete_object(itemClass, item.id)
                    resetFunc()
            else:
                critical_error_message_box(dlgTitle, err_text)
        else:
            critical_error_message_box(dlgTitle, UiStrings().NISs)

    def resetAuthors(self):
        """
        Reloads the Authors list.
        """
        self.authorsListWidget.clear()
        authors = self.manager.get_all_objects(Author, order_by_ref=Author.display_name)
        for author in authors:
            if author.display_name:
                author_name = QtGui.QListWidgetItem(author.display_name)
            else:
                author_name = QtGui.QListWidgetItem(u' '.join([author.first_name, author.last_name]))
            author_name.setData(QtCore.Qt.UserRole, author.id)
            self.authorsListWidget.addItem(author_name)

    def resetTopics(self):
        """
        Reloads the Topics list.
        """
        self.topicsListWidget.clear()
        topics = self.manager.get_all_objects(Topic, order_by_ref=Topic.name)
        for topic in topics:
            topic_name = QtGui.QListWidgetItem(topic.name)
            topic_name.setData(QtCore.Qt.UserRole, topic.id)
            self.topicsListWidget.addItem(topic_name)

    def resetBooks(self):
        """
        Reloads the Books list.
        """
        self.booksListWidget.clear()
        books = self.manager.get_all_objects(Book, order_by_ref=Book.name)
        for book in books:
            book_name = QtGui.QListWidgetItem(u'%s (%s)' % (book.name, book.publisher))
            book_name.setData(QtCore.Qt.UserRole, book.id)
            self.booksListWidget.addItem(book_name)

    def checkAuthor(self, newAuthor, edit=False):
        """
        Returns *False* if the given Author already exists, otherwise *True*.
        """
        authors = self.manager.get_all_objects(Author,
            and_(Author.first_name == newAuthor.first_name,
                Author.last_name == newAuthor.last_name,
                Author.display_name == newAuthor.display_name))
        return self.__checkObject(authors, newAuthor, edit)

    def checkTopic(self, newTopic, edit=False):
        """
        Returns *False* if the given Topic already exists, otherwise *True*.
        """
        topics = self.manager.get_all_objects(Topic, Topic.name == newTopic.name)
        return self.__checkObject(topics, newTopic, edit)

    def checkBook(self, newBook, edit=False):
        """
        Returns *False* if the given Topic already exists, otherwise *True*.
        """
        books = self.manager.get_all_objects(Book,
            and_(Book.name == newBook.name, Book.publisher == newBook.publisher))
        return self.__checkObject(books, newBook, edit)

    def __checkObject(self, objects, newObject, edit):
        """
        Utility method to check for an existing object.

        ``edit``
            If we edit an item, this should be *True*.
        """
        if objects:
            # If we edit an existing object, we need to make sure that we do
            # not return False when nothing has changed.
            if edit:
                for object in objects:
                    if object.id != newObject.id:
                        return False
                return True
            else:
                return False
        else:
            return True

    def onAuthorAddButtonClicked(self):
        """
        Add an author to the list.
        """
        self.authorform.setAutoDisplayName(True)
        if self.authorform.exec_():
            author = Author.populate(
                first_name=self.authorform.firstNameEdit.text(),
                last_name=self.authorform.lastNameEdit.text(),
                display_name=self.authorform.displayEdit.text())
            if self.checkAuthor(author):
                if self.manager.save_object(author):
                    self.resetAuthors()
                else:
                    critical_error_message_box(
                        message=translate('SongsPlugin.SongMaintenanceForm', 'Could not add your author.'))
            else:
                critical_error_message_box(
                    message=translate('SongsPlugin.SongMaintenanceForm', 'This author already exists.'))

    def onTopicAddButtonClicked(self):
        """
        Add a topic to the list.
        """
        if self.topicform.exec_():
            topic = Topic.populate(name=self.topicform.nameEdit.text())
            if self.checkTopic(topic):
                if self.manager.save_object(topic):
                    self.resetTopics()
                else:
                    critical_error_message_box(
                        message=translate('SongsPlugin.SongMaintenanceForm', 'Could not add your topic.'))
            else:
                critical_error_message_box(
                    message=translate('SongsPlugin.SongMaintenanceForm', 'This topic already exists.'))

    def onBookAddButtonClicked(self):
        """
        Add a book to the list.
        """
        if self.bookform.exec_():
            book = Book.populate(name=self.bookform.nameEdit.text(),
                publisher=self.bookform.publisherEdit.text())
            if self.checkBook(book):
                if self.manager.save_object(book):
                    self.resetBooks()
                else:
                    critical_error_message_box(
                        message=translate('SongsPlugin.SongMaintenanceForm', 'Could not add your book.'))
            else:
                critical_error_message_box(
                    message=translate('SongsPlugin.SongMaintenanceForm', 'This book already exists.'))

    def onAuthorEditButtonClicked(self):
        """
        Edit an author.
        """
        author_id = self._getCurrentItemId(self.authorsListWidget)
        if author_id == -1:
            return
        author = self.manager.get_object(Author, author_id)
        self.authorform.setAutoDisplayName(False)
        self.authorform.firstNameEdit.setText(author.first_name)
        self.authorform.lastNameEdit.setText(author.last_name)
        self.authorform.displayEdit.setText(author.display_name)
        # Save the author's first and last name as well as the display name
        # for the case that they have to be restored.
        temp_first_name = author.first_name
        temp_last_name = author.last_name
        temp_display_name = author.display_name
        if self.authorform.exec_(False):
            author.first_name = self.authorform.firstNameEdit.text()
            author.last_name = self.authorform.lastNameEdit.text()
            author.display_name = self.authorform.displayEdit.text()
            if self.checkAuthor(author, True):
                if self.manager.save_object(author):
                    self.resetAuthors()
                    if not self.fromSongEdit:
                        Receiver.send_message(u'songs_load_list')
                else:
                    critical_error_message_box(
                        message=translate('SongsPlugin.SongMaintenanceForm', 'Could not save your changes.'))
            elif critical_error_message_box(message=translate(
                'SongsPlugin.SongMaintenanceForm', 'The author %s already exists. Would you like to make songs with '
                'author %s use the existing author %s?') %
                    (author.display_name, temp_display_name, author.display_name), parent=self, question=True) == \
                    QtGui.QMessageBox.Yes:
                self.__mergeObjects(author, self.mergeAuthors,
                    self.resetAuthors)
            else:
                # We restore the author's old first and last name as well as
                # his display name.
                author.first_name = temp_first_name
                author.last_name = temp_last_name
                author.display_name = temp_display_name
                critical_error_message_box(
                    message=translate('SongsPlugin.SongMaintenanceForm',
                    'Could not save your modified author, because the author already exists.'))

    def onTopicEditButtonClicked(self):
        """
        Edit a topic.
        """
        topic_id = self._getCurrentItemId(self.topicsListWidget)
        if topic_id == -1:
            return
        topic = self.manager.get_object(Topic, topic_id)
        self.topicform.nameEdit.setText(topic.name)
        # Save the topic's name for the case that he has to be restored.
        temp_name = topic.name
        if self.topicform.exec_(False):
            topic.name = self.topicform.nameEdit.text()
            if self.checkTopic(topic, True):
                if self.manager.save_object(topic):
                    self.resetTopics()
                else:
                    critical_error_message_box(
                        message=translate('SongsPlugin.SongMaintenanceForm', 'Could not save your changes.'))
            elif critical_error_message_box(
                message=translate('SongsPlugin.SongMaintenanceForm',
                'The topic %s already exists. Would you like to make songs with topic %s use the existing topic %s?') %
                (topic.name, temp_name, topic.name), parent=self, question=True) == QtGui.QMessageBox.Yes:
                self.__mergeObjects(topic, self.mergeTopics, self.resetTopics)
            else:
                # We restore the topics's old name.
                topic.name = temp_name
                critical_error_message_box(
                    message=translate('SongsPlugin.SongMaintenanceForm',
                    'Could not save your modified topic, because it already exists.'))

    def onBookEditButtonClicked(self):
        """
        Edit a book.
        """
        book_id = self._getCurrentItemId(self.booksListWidget)
        if book_id == -1:
            return
        book = self.manager.get_object(Book, book_id)
        if book.publisher is None:
            book.publisher = u''
        self.bookform.nameEdit.setText(book.name)
        self.bookform.publisherEdit.setText(book.publisher)
        # Save the book's name and publisher for the case that they have to
        # be restored.
        temp_name = book.name
        temp_publisher = book.publisher
        if self.bookform.exec_(False):
            book.name = self.bookform.nameEdit.text()
            book.publisher = self.bookform.publisherEdit.text()
            if self.checkBook(book, True):
                if self.manager.save_object(book):
                    self.resetBooks()
                else:
                    critical_error_message_box(
                        message=translate('SongsPlugin.SongMaintenanceForm', 'Could not save your changes.'))
            elif critical_error_message_box(
                message=translate('SongsPlugin.SongMaintenanceForm',
                    'The book %s already exists. Would you like to make songs with book %s use the existing book %s?') %
                (book.name, temp_name, book.name), parent=self, question=True) == QtGui.QMessageBox.Yes:
                self.__mergeObjects(book, self.mergeBooks, self.resetBooks)
            else:
                # We restore the book's old name and publisher.
                book.name = temp_name
                book.publisher = temp_publisher

    def __mergeObjects(self, dbObject, merge, reset):
        """
        Utility method to merge two objects to leave one in the database.
        """
        self.application.set_busy_cursor()
        merge(dbObject)
        reset()
        if not self.fromSongEdit:
            Receiver.send_message(u'songs_load_list')
        self.application.set_normal_cursor()

    def mergeAuthors(self, oldAuthor):
        """
        Merges two authors into one author.

        ``oldAuthor``
            The object, which was edited, that will be deleted
        """
        # Find the duplicate.
        existing_author = self.manager.get_object_filtered(Author,
            and_(Author.first_name == oldAuthor.first_name,
                Author.last_name == oldAuthor.last_name,
                Author.display_name == oldAuthor.display_name,
                Author.id != oldAuthor.id))
        # Find the songs, which have the oldAuthor as author.
        songs = self.manager.get_all_objects(Song,
            Song.authors.contains(oldAuthor))
        for song in songs:
            # We check if the song has already existing_author as author. If
            # that is not the case we add it.
            if existing_author not in song.authors:
                song.authors.append(existing_author)
            song.authors.remove(oldAuthor)
            self.manager.save_object(song)
        self.manager.delete_object(Author, oldAuthor.id)

    def mergeTopics(self, oldTopic):
        """
        Merges two topics into one topic.

        ``oldTopic``
            The object, which was edited, that will be deleted
        """
        # Find the duplicate.
        existing_topic = self.manager.get_object_filtered(Topic,
            and_(Topic.name == oldTopic.name, Topic.id != oldTopic.id))
        # Find the songs, which have the oldTopic as topic.
        songs = self.manager.get_all_objects(Song, Song.topics.contains(oldTopic))
        for song in songs:
            # We check if the song has already existing_topic as topic. If that
            # is not the case we add it.
            if existing_topic not in song.topics:
                song.topics.append(existing_topic)
            song.topics.remove(oldTopic)
            self.manager.save_object(song)
        self.manager.delete_object(Topic, oldTopic.id)

    def mergeBooks(self, oldBook):
        """
        Merges two books into one book.

        ``oldBook``
            The object, which was edited, that will be deleted
        """
        # Find the duplicate.
        existing_book = self.manager.get_object_filtered(Book,
            and_(Book.name == oldBook.name,
                Book.publisher == oldBook.publisher,
                Book.id != oldBook.id))
        # Find the songs, which have the oldBook as book.
        songs = self.manager.get_all_objects(Song,
            Song.song_book_id == oldBook.id)
        for song in songs:
            song.song_book_id = existing_book.id
            self.manager.save_object(song)
        self.manager.delete_object(Book, oldBook.id)

    def onAuthorDeleteButtonClicked(self):
        """
        Delete the author if the author is not attached to any songs.
        """
        self._deleteItem(Author, self.authorsListWidget, self.resetAuthors,
            translate('SongsPlugin.SongMaintenanceForm', 'Delete Author'),
            translate('SongsPlugin.SongMaintenanceForm', 'Are you sure you want to delete the selected author?'),
            translate('SongsPlugin.SongMaintenanceForm',
                'This author cannot be deleted, they are currently assigned to at least one song.'))

    def onTopicDeleteButtonClicked(self):
        """
        Delete the Book if the Book is not attached to any songs.
        """
        self._deleteItem(Topic, self.topicsListWidget, self.resetTopics,
            translate('SongsPlugin.SongMaintenanceForm', 'Delete Topic'),
            translate('SongsPlugin.SongMaintenanceForm', 'Are you sure you want to delete the selected topic?'),
            translate('SongsPlugin.SongMaintenanceForm',
                'This topic cannot be deleted, it is currently assigned to at least one song.'))

    def onBookDeleteButtonClicked(self):
        """
        Delete the Book if the Book is not attached to any songs.
        """
        self._deleteItem(Book, self.booksListWidget, self.resetBooks,
            translate('SongsPlugin.SongMaintenanceForm', 'Delete Book'),
            translate('SongsPlugin.SongMaintenanceForm', 'Are you sure you want to delete the selected book?'),
            translate('SongsPlugin.SongMaintenanceForm',
                'This book cannot be deleted, it is currently assigned to at least one song.'))

    def onAuthorsListRowChanged(self, row):
        """
        Called when the *authorsListWidget*'s current row has changed.
        """
        self.__rowChange(row, self.authorsEditButton, self.authorsDeleteButton)

    def onTopicsListRowChanged(self, row):
        """
        Called when the *topicsListWidget*'s current row has changed.
        """
        self.__rowChange(row, self.topicsEditButton, self.topicsDeleteButton)

    def onBooksListRowChanged(self, row):
        """
        Called when the *booksListWidget*'s current row has changed.
        """
        self.__rowChange(row, self.booksEditButton, self.booksDeleteButton)

    def __rowChange(self, row, editButton, deleteButton):
        """
        Utility method to toggle if buttons are enabled.

        ``row``
            The current row. If there is no current row, the value is -1.
        """
        if row == -1:
            deleteButton.setEnabled(False)
            editButton.setEnabled(False)
        else:
            deleteButton.setEnabled(True)
            editButton.setEnabled(True)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
