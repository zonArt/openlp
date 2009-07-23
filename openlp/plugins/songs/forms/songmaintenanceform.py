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
from openlp.plugins.songs.forms import SongBookForm
from openlp.plugins.songs.lib.classes import Author, Book, Topic
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
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer,
            QtCore.SIGNAL(u'timeout()'), self._hideErrors)
        QtCore.QObject.connect(self.AuthorDeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onAuthorDeleteButtonClick)
        QtCore.QObject.connect(self.TopicDeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onTopicDeleteButtonClick)
        QtCore.QObject.connect(self.BookDeleteButton,
            QtCore.SIGNAL(u'pressed()'), self.onBookDeleteButtonClick)

    def exec_(self):
        self.resetAuthors()
        self.resetTopics()
        self.resetBooks()
        return QtGui.QDialog.exec_(self)

    def _getCurrentItemId(self, ListWidget):
        item = ListWidget.currentItem()
        print item
        if item is not None:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            return item_id
        else:
            return -1

    def _showError(self, error):
        self.AuthorsErrorLabel.setSize(QtCore.QSize(0, 32))
        self.AuthorsErrorLabel.setText(error)
        self.TopicsErrorLabel.setMaximumHeight(32)
        self.TopicsErrorLabel.setMinimumHeight(32)
        self.TopicsErrorLabel.setText(error)
        self.BooksErrorLabel.setMaximumHeight(32)
        self.BooksErrorLabel.setMinimumHeight(32)
        self.BooksErrorLabel.setText(error)
        self.timer.start(2000)

    def _hideErrors(self):
        self.timer.stop()
        self.AuthorsErrorLabel.setMaximumHeight(0)
        self.AuthorsErrorLabel.setMinimumHeight(0)
        self.AuthorsErrorLabel.clear()
        self.TopicsErrorLabel.setMaximumHeight(0)
        self.TopicsErrorLabel.setMinimumHeight(0)
        self.TopicsErrorLabel.clear()
        self.BooksErrorLabel.setMaximumHeight(0)
        self.BooksErrorLabel.setMinimumHeight(0)
        self.BooksErrorLabel.clear()

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

    def onAuthorDeleteButtonClick(self):
        """
        Delete the author if the author is not attached to any songs
        """
        author_id = self._getCurrentItemId(self.AuthorsListWidget)
        if author_id != -1:
            author = self.songmanager.get_author(author_id)
            if QtGui.QMessageBox.warning(None,
                    translate(u'SongMaintenanceForm', u'Delete Author'),
                    translate(u'SongMaintenanceForm', u'Are you sure you want to delete the selected author?'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                    ) == QtGui.QMessageBox.Yes:
                if len(author.songs) == 0:
                    self.songmanager.delete_author(author.id)
                    self.resetAuthors()
                else:
                    QtGui.QMessageBox.critical(None,
                        translate(u'SongMaintenanceForm', u'Delete Author'),
                        translate(u'SongMaintenanceForm', u'This author can\'t be deleted, they are currently assigned to at least one song!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
        else:
            self._showError(translate(u'SongMaintenanceForm', u'No author selected!'))

    def onTopicDeleteButtonClick(self):
        """
        Delete the Book is the Book is not attached to any songs
        """
        topic_id = self._getCurrentItemId(self.TopicsListWidget)
        if topic_id != -1:
            topic = self.songmanager.get_topic(topic_id)
            if QtGui.QMessageBox.warning(None,
                    translate(u'SongMaintenanceForm', u'Delete Topic'),
                    translate(u'SongMaintenanceForm', u'Are you sure you want to delete the selected topic?'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                    ) == QtGui.QMessageBox.Yes:
                if len(topic.songs) == 0:
                    self.songmanager.delete_topic(topic.id)
                    self.resetTopics()
                else:
                    #QtGui.QMessageBox.critical(None,
                    #    translate(u'SongMaintenanceForm', u'Delete Topic'),
                    #    translate(u'SongMaintenanceForm', u'This topic can\'t be deleted, it is currently assigned to at least one song!'),
                    #    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
                    self._showError(translate(u'SongMaintenanceForm', u'This topic can\'t be deleted, it is currently assigned to at least one song!'))
        else:
            self._showError(translate(u'SongMaintenanceForm', u'No topic selected!'))

    def onBookDeleteButtonClick(self):
        """
        Delete the Book is the Book is not attached to any songs
        """
        book_id = self._getCurrentItemId(self.BooksListWidget)
        if book_id != -1:
            book = self.songmanager.get_book(book_id)
            if QtGui.QMessageBox.warning(None,
                    translate(u'SongMaintenanceForm', u'Delete Book'),
                    translate(u'SongMaintenanceForm', u'Are you sure you want to delete the selected book?'),
                    QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                    ) == QtGui.QMessageBox.Yes:
                if len(book.songs) == 0:
                    self.songmanager.delete_book(book.id)
                    self.resetBooks()
                else:
                    QtGui.QMessageBox.critical(None,
                        translate(u'SongMaintenanceForm', u'Delete Book'),
                        translate(u'SongMaintenanceForm', u'This book can\'t be deleted, it is currently assigned to at least one song!'),
                        QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
        else:
            self._showError(translate(u'SongMaintenanceForm', u'No book selected!'))
