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
from openlp.plugins.songs.lib.classes import Author, Book, Topic
from songmaintenancedialog import Ui_SongMaintenanceDialog
from authorsform import AuthorsForm
from topicsform import TopicsForm
from songbookform import SongBookForm

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
        if item is not None:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            return item_id
        else:
            return -1

    def _deleteItem(self, list_widget, get_func, del_func, reset_func,
                    dlg_title, del_text, err_text, sel_text):
        item_id = self._getCurrentItemId(list_widget)
        if item_id != -1:
            item = get_func(item_id)
            if QtGui.QMessageBox.warning(self, dlg_title, del_text,
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                    ) == QtGui.QMessageBox.Yes:
                if item is not None and len(item.songs) == 0:
                    del_func(item.id)
                    reset_func()
                else:
                    QtGui.QMessageBox.critical(self, dlg_title, err_text,
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
        else:
            QtGui.QMessageBox.critical(self, dlg_title, sel_text,
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))

    def resetAuthors(self):
        self.AuthorsListWidget.clear()
        authors = self.songmanager.get_authors()
        for author in authors:
            if author.display_name is not None and author.display_name != u'':
                author_name = QtGui.QListWidgetItem(author.display_name)
            else:
                author_name = QtGui.QListWidgetItem(
                    u'%s %s' % (author.first_name, author.last_name))
            author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListWidget.addItem(author_name)

    def resetTopics(self):
        self.TopicsListWidget.clear()
        topics = self.songmanager.get_topics()
        for topic in topics:
            topic_name = QtGui.QListWidgetItem(topic.name)
            topic_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(topic.id))
            self.TopicsListWidget.addItem(topic_name)

    def resetBooks(self):
        self.BooksListWidget.clear()
        books = self.songmanager.get_books()
        for book in books:
            book_name = QtGui.QListWidgetItem(book.name)
            book_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(book.id))
            self.BooksListWidget.addItem(book_name)

    def onAuthorAddButtonClick(self):
        self.authorform.setAutoDisplayName(True)
        if self.authorform.exec_():
            author = Author.populate(
                first_name=unicode(self.authorform.FirstNameEdit.text(), u'utf-8'),
                last_name=unicode(self.authorform.LastNameEdit.text(), u'utf-8'),
                display_name=unicode(self.authorform.DisplayEdit.text(), u'utf-8'))
            if self.songmanager.save_author(author):
                self.resetAuthors()
            else:
                QtGui.QMessageBox.critical(self,
                    translate(u'SongMaintenanceForm', u'Error'),
                    translate(u'SongMaintenanceForm', u'Couldn\'t add your author!'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))

    def onTopicAddButtonClick(self):
        if self.topicform.exec_():
            topic = Topic.populate(name=unicode(self.topicform.NameEdit.text(), u'utf-8'))
            if self.songmanager.save_topic(topic):
                self.resetTopics()
            else:
                QtGui.QMessageBox.critical(self,
                    translate(u'SongMaintenanceForm', u'Error'),
                    translate(u'SongMaintenanceForm', u'Couldn\'t add your topic!'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))

    def onBookAddButtonClick(self):
        if self.bookform.exec_():
            book = Book.populate(name=unicode(self.bookform.NameEdit.text(), u'utf-8'),
                publisher=unicode(self.bookform.PublisherEdit.text(), u'utf-8'))
            if self.songmanager.save_book(book):
                self.resetBooks()
            else:
                QtGui.QMessageBox.critical(self,
                    translate(u'SongMaintenanceForm', u'Error'),
                    translate(u'SongMaintenanceForm', u'Couldn\'t add your book!'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))

    def onAuthorEditButtonClick(self):
        author_id = self._getCurrentItemId(self.AuthorsListWidget)
        if author_id != -1:
            author = self.songmanager.get_author(author_id)
            self.authorform.setAutoDisplayName(False)
            self.authorform.FirstNameEdit.setText(author.first_name)
            self.authorform.LastNameEdit.setText(author.last_name)
            self.authorform.DisplayEdit.setText(author.display_name)
            if self.authorform.exec_(False):
                author.first_name = unicode(self.authorform.FirstNameEdit.text(), u'utf-8')
                author.last_name = unicode(self.authorform.LastNameEdit.text(), u'utf-8')
                author.display_name = unicode(self.authorform.DisplayEdit.text(), u'utf-8')
                if self.songmanager.save_author(author):
                    self.resetAuthors()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate(u'SongMaintenanceForm', u'Error'),
                        translate(u'SongMaintenanceForm', u'Couldn\'t save your author!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))

    def onTopicEditButtonClick(self):
        topic_id = self._getCurrentItemId(self.TopicsListWidget)
        if topic_id != -1:
            topic = self.songmanager.get_topic(topic_id)
            self.topicform.NameEdit.setText(topic.name)
            if self.topicform.exec_(False):
                topic.name = unicode(self.topicform.NameEdit.text(), u'utf-8')
                if self.songmanager.save_topic(topic):
                    self.resetTopics()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate(u'SongMaintenanceForm', u'Error'),
                        translate(u'SongMaintenanceForm', u'Couldn\'t save your topic!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))

    def onBookEditButtonClick(self):
        book_id = self._getCurrentItemId(self.BooksListWidget)
        if book_id != -1:
            book = self.songmanager.get_book(book_id)
            self.bookform.NameEdit.setText(book.name)
            self.bookform.PublisherEdit.setText(book.publisher)
            if self.bookform.exec_(False):
                book.name = unicode(self.bookform.NameEdit.text(), u'utf-8')
                book.publisher = unicode(self.bookform.PublisherEdit.text(), u'utf-8')
                if self.songmanager.save_book(book):
                    self.resetBooks()
                else:
                    QtGui.QMessageBox.critical(self,
                        translate(u'SongMaintenanceForm', u'Error'),
                        translate(u'SongMaintenanceForm', u'Couldn\'t save your book!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))

    def onAuthorDeleteButtonClick(self):
        """
        Delete the author if the author is not attached to any songs
        """
        self._deleteItem(self.AuthorsListWidget, self.songmanager.get_author,
            self.songmanager.delete_author, self.resetAuthors,
            translate(u'SongMaintenanceForm', u'Delete Author'),
            translate(u'SongMaintenanceForm', u'Are you sure you want to delete the selected author?'),
            translate(u'SongMaintenanceForm', u'This author can\'t be deleted, they are currently assigned to at least one song!'),
            translate(u'SongMaintenanceForm', u'No author selected!'))

    def onTopicDeleteButtonClick(self):
        """
        Delete the Book is the Book is not attached to any songs
        """
        self._deleteItem(self.TopicsListWidget, self.songmanager.get_topic,
            self.songmanager.delete_topic, self.resetTopics,
            translate(u'SongMaintenanceForm', u'Delete Topic'),
            translate(u'SongMaintenanceForm', u'Are you sure you want to delete the selected topic?'),
            translate(u'SongMaintenanceForm', u'This topic can\'t be deleted, it is currently assigned to at least one song!'),
            translate(u'SongMaintenanceForm', u'No topic selected!'))

    def onBookDeleteButtonClick(self):
        """
        Delete the Book is the Book is not attached to any songs
        """
        self._deleteItem(self.BooksListWidget, self.songmanager.get_book,
            self.songmanager.delete_book, self.resetBooks,
            translate(u'SongMaintenanceForm', u'Delete Book'),
            translate(u'SongMaintenanceForm', u'Are you sure you want to delete the selected book?'),
            translate(u'SongMaintenanceForm', u'This book can\'t be deleted, it is currently assigned to at least one song!'),
            translate(u'SongMaintenanceForm', u'No book selected!'))
