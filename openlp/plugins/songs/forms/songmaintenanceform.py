# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from openlp.core.lib import translate
from openlp.plugins.songs.forms import AuthorsForm, TopicsForm, SongBookForm
from openlp.plugins.songs.lib.db import Author, Book, Topic
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
                        QtGui.QMessageBox.StandardButtons(
                            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                        ) == QtGui.QMessageBox.Yes:
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
        authors = self.songmanager.get_all_objects(Author, Author.display_name)
        for author in authors:
            if author.display_name:
                author_name = QtGui.QListWidgetItem(author.display_name)
            else:
                author_name = QtGui.QListWidgetItem(
                    u'%s %s' % (author.first_name, author.last_name))
            author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListWidget.addItem(author_name)

    def resetTopics(self):
        """
        Reloads the Topics list.
        """
        self.TopicsListWidget.clear()
        topics = self.songmanager.get_all_objects(Topic, Topic.name)
        for topic in topics:
            topic_name = QtGui.QListWidgetItem(topic.name)
            topic_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(topic.id))
            self.TopicsListWidget.addItem(topic_name)

    def resetBooks(self):
        """
        Reloads the Books list.
        """
        self.BooksListWidget.clear()
        books = self.songmanager.get_all_objects(Book, Book.name)
        for book in books:
            book_name = QtGui.QListWidgetItem(u'%s (%s)' % (book.name,
                book.publisher))
            book_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(book.id))
            self.BooksListWidget.addItem(book_name)

    def checkAuthor(self, new_author, edit=False):
        """
        Returns True when the given Author is already in the list elsewise False.
        """
        authors = self.songmanager.get_all_objects(Author)
        author_exists = False
        for author in authors:
            if author.fist_name == new_author.first_name and \
                author.last_name == new_author.last_name and \
                author.display_name == new_author.display_name:
                author_exists = True
                #If we edit an exsisting Author, we need to make sure that we do
                #not return True when nothing has changed (because this would
                #cause an error message later on)
                if edit:
                    if new_author.id == author.id:
                        author_exists = False
        return author_exists

    def checkTopic(self, new_topic, edit=False):
        """
        Returns True when the given Topic is already in the list elsewise False.
        """
        topics = self.songmanager.get_all_objects(Topic)
        topic_exists = False
        for topic in topics:
            if topic.name == new_topic.name:
                topic_exists = True
                #If we edit an exsisting Topic, we need to make sure that we do
                #not return True when nothing has changed (because this would
                #cause an error message later on)
                if edit:
                    if new_topic.id == topic.id:
                        topic_exists = False
        return topic_exists

    def checkBook(self, new_book, edit=False):
        """
        Returns True when the given Book is already in the list elsewise False.
        """
        books = self.songmanager.get_all_objects(Book)
        book_exists = False
        for book in books:
            if book.publisher == new_book.publisher and \
                book.name == new_book.name:
                book_exists = True
                #If we edit an exsisting Book, we need to make sure that we do
                #not return True when nothing has changed (because this would
                #cause an error message later on)
                if edit:
                    if new_book.id == book.id:
                        book_exists = False
        return book_exists

    def onAuthorAddButtonClick(self):
        self.authorform.setAutoDisplayName(True)
        if self.authorform.exec_():
            author = Author.populate(
                first_name=unicode(self.authorform.FirstNameEdit.text()),
                last_name=unicode(self.authorform.LastNameEdit.text()),
                display_name=unicode(self.authorform.DisplayEdit.text()))
            if not self.checkAuthor(author) and \
                self.songmanager.save_object(author):
                self.resetAuthors()
            else:
                QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm',
                    'Could not add your author.'))

    def onTopicAddButtonClick(self):
        if self.topicform.exec_():
            topic = Topic.populate(name=unicode(self.topicform.NameEdit.text()))
            if  not self.checkTopic(topic) and \
                self.songmanager.save_object(topic):
                self.resetTopics()
            else:
                QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm',
                    'Could not add your topic.'))

    def onBookAddButtonClick(self):
        if self.bookform.exec_():
            book = Book.populate(
                name=unicode(self.bookform.NameEdit.text()),
                publisher=unicode(self.bookform.PublisherEdit.text()))
            if not self.checkBook(book) and self.songmanager.save_object(book):
                self.resetBooks()
            else:
                QtGui.QMessageBox.critical(self,
                    translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                    translate('SongsPlugin.SongMaintenanceForm',
                    'Could not add your book.'))

    def onAuthorEditButtonClick(self):
        author_id = self._getCurrentItemId(self.AuthorsListWidget)
        if author_id != -1:
            author = self.songmanager.get_object(Author, author_id)
            # Just make sure none of the fields is None
            if author.first_name is None:
                author.first_name = u''
            if author.last_name is None:
                author.last_name = u''
            if author.display_name is None:
                author.display_name = u''
            self.authorform.setAutoDisplayName(False)
            self.authorform.FirstNameEdit.setText(author.first_name)
            self.authorform.LastNameEdit.setText(author.last_name)
            self.authorform.DisplayEdit.setText(author.display_name)
            if self.authorform.exec_(False):
                author.first_name = unicode(
                    self.authorform.FirstNameEdit.text())
                author.last_name = unicode(self.authorform.LastNameEdit.text())
                author.display_name = unicode(
                    self.authorform.DisplayEdit.text())
                if self.checkAuthor(author, True) is False and \
                    self.songmanager.save_object(author):
                    self.resetAuthors()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                        translate('SongsPlugin.SongMaintenanceForm',
                        'Could not save your author.'))

    def onTopicEditButtonClick(self):
        topic_id = self._getCurrentItemId(self.TopicsListWidget)
        if topic_id != -1:
            topic = self.songmanager.get_object(Topic, topic_id)
            self.topicform.NameEdit.setText(topic.name)
            if self.topicform.exec_(False):
                topic.name = unicode(self.topicform.NameEdit.text())
                if self.checkTopic(topic, True) is False and \
                    self.songmanager.save_object(topic):
                    self.resetTopics()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                        translate('SongsPlugin.SongMaintenanceForm',
                        'Could not save your topic.'))

    def onBookEditButtonClick(self):
        book_id = self._getCurrentItemId(self.BooksListWidget)
        if book_id != -1:
            book = self.songmanager.get_object(Book, book_id)
            self.bookform.NameEdit.setText(book.name)
            self.bookform.PublisherEdit.setText(book.publisher)
            if self.bookform.exec_(False):
                book.name = unicode(self.bookform.NameEdit.text())
                book.publisher = unicode(self.bookform.PublisherEdit.text())
                if self.checkBook(book, True) is False and \
                    self.songmanager.save_object(book):
                    self.resetBooks()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.SongMaintenanceForm', 'Error'),
                        translate('SongsPlugin.SongMaintenanceForm',
                        'Could not save your book.'))

    def onAuthorDeleteButtonClick(self):
        """
        Delete the author if the author is not attached to any songs
        """
        self._deleteItem(Author, self.AuthorsListWidget, self.resetAuthors,
            translate('SongsPlugin.SongMaintenanceForm', 'Delete Author'),
            translate('SongsPlugin.SongMaintenanceForm',
            'Are you sure you want to delete the selected author?'),
            translate('SongsPlugin.SongMaintenanceForm',
            'This author ca not be deleted, they are currently '
            'assigned to at least one song.'),
            translate('SongsPlugin.SongMaintenanceForm', 'No author selected!'))

    def onTopicDeleteButtonClick(self):
        """
        Delete the Book is the Book is not attached to any songs
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
        Delete the Book is the Book is not attached to any songs
        """
        self._deleteItem(Book, self.BooksListWidget, self.resetBooks,
            translate('SongsPlugin.SongMaintenanceForm', 'Delete Book'),
            translate('SongsPlugin.SongMaintenanceForm',
            'Are you sure you want to delete the selected book?'),
            translate('SongsPlugin.SongMaintenanceForm',
            'This book cannot be deleted, it is currently '
            'assigned to at least one song.'),
            translate('SongsPlugin.SongMaintenanceForm', 'No book selected!'))
