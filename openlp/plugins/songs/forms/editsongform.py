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

import logging
import re

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, translate
from openlp.plugins.songs.forms import EditVerseForm
from openlp.plugins.songs.lib import SongXMLBuilder, SongXMLParser, VerseType
from openlp.plugins.songs.lib.db import Book, Song, Author, Topic
from editsongdialog import Ui_EditSongDialog

log = logging.getLogger(__name__)

class EditSongForm(QtGui.QDialog, Ui_EditSongDialog):
    """
    Class to manage the editing of a song
    """
    log.info(u'%s EditSongForm loaded', __name__)

    def __init__(self, parent, songmanager):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        # can this be automated?
        self.width = 400
        self.setupUi(self)
        # Connecting signals and slots
        QtCore.QObject.connect(self.AuthorAddButton,
            QtCore.SIGNAL(u'clicked()'), self.onAuthorAddButtonClicked)
        QtCore.QObject.connect(self.AuthorRemoveButton,
            QtCore.SIGNAL(u'clicked()'), self.onAuthorRemoveButtonClicked)
        QtCore.QObject.connect(self.AuthorsListView,
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'),
            self.onAuthorsListViewPressed)
        QtCore.QObject.connect(self.TopicAddButton,
            QtCore.SIGNAL(u'clicked()'), self.onTopicAddButtonClicked)
        QtCore.QObject.connect(self.TopicRemoveButton,
            QtCore.SIGNAL(u'clicked()'), self.onTopicRemoveButtonClicked)
        QtCore.QObject.connect(self.TopicsListView,
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'),
            self.onTopicListViewPressed)
        QtCore.QObject.connect(self.CopyrightInsertButton,
            QtCore.SIGNAL(u'clicked()'), self.onCopyrightInsertButtonTriggered)
        QtCore.QObject.connect(self.VerseAddButton,
            QtCore.SIGNAL(u'clicked()'), self.onVerseAddButtonClicked)
        QtCore.QObject.connect(self.VerseListWidget,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.onVerseEditButtonClicked)
        QtCore.QObject.connect(self.VerseEditButton,
            QtCore.SIGNAL(u'clicked()'), self.onVerseEditButtonClicked)
        QtCore.QObject.connect(self.VerseEditAllButton,
            QtCore.SIGNAL(u'clicked()'), self.onVerseEditAllButtonClicked)
        QtCore.QObject.connect(self.VerseDeleteButton,
            QtCore.SIGNAL(u'clicked()'), self.onVerseDeleteButtonClicked)
        QtCore.QObject.connect(self.VerseListWidget,
            QtCore.SIGNAL(u'itemClicked(QTableWidgetItem*)'),
            self.onVerseListViewPressed)
        QtCore.QObject.connect(self.SongbookCombo,
            QtCore.SIGNAL(u'activated(int)'), self.onSongBookComboChanged)
        QtCore.QObject.connect(self.ThemeSelectionComboItem,
            QtCore.SIGNAL(u'activated(int)'), self.onThemeComboChanged)
        QtCore.QObject.connect(self.ThemeAddButton,
            QtCore.SIGNAL(u'clicked()'),
            self.parent.parent.renderManager.theme_manager.onAddTheme)
        QtCore.QObject.connect(self.MaintenanceButton,
            QtCore.SIGNAL(u'clicked()'), self.onMaintenanceButtonClicked)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.loadThemes)
        self.previewButton = QtGui.QPushButton()
        self.previewButton.setObjectName(u'previewButton')
        self.previewButton.setText(
            translate('SongsPlugin.EditSongForm', 'Save && Preview'))
        self.ButtonBox.addButton(
            self.previewButton, QtGui.QDialogButtonBox.ActionRole)
        QtCore.QObject.connect(self.ButtonBox,
            QtCore.SIGNAL(u'clicked(QAbstractButton*)'), self.onPreview)
        # Create other objects and forms
        self.songmanager = songmanager
        self.verse_form = EditVerseForm(self)
        self.initialise()
        self.AuthorsListView.setSortingEnabled(False)
        self.AuthorsListView.setAlternatingRowColors(True)
        self.TopicsListView.setSortingEnabled(False)
        self.TopicsListView.setAlternatingRowColors(True)
        self.findVerseSplit = re.compile(u'---\[\]---\n', re.UNICODE)

    def initialise(self):
        self.VerseEditButton.setEnabled(False)
        self.VerseDeleteButton.setEnabled(False)
        self.AuthorRemoveButton.setEnabled(False)
        self.TopicRemoveButton.setEnabled(False)

    def loadAuthors(self):
        authors = self.songmanager.get_all_objects(Author,
            order_by_ref=Author.display_name)
        self.AuthorsSelectionComboItem.clear()
        self.AuthorsSelectionComboItem.addItem(u'')
        for author in authors:
            row = self.AuthorsSelectionComboItem.count()
            self.AuthorsSelectionComboItem.addItem(author.display_name)
            self.AuthorsSelectionComboItem.setItemData(
                row, QtCore.QVariant(author.id))

    def loadTopics(self):
        topics = self.songmanager.get_all_objects(Topic,
            order_by_ref=Topic.name)
        self.SongTopicCombo.clear()
        self.SongTopicCombo.addItem(u'')
        for topic in topics:
            row = self.SongTopicCombo.count()
            self.SongTopicCombo.addItem(topic.name)
            self.SongTopicCombo.setItemData(row, QtCore.QVariant(topic.id))

    def loadBooks(self):
        books = self.songmanager.get_all_objects(Book, order_by_ref=Book.name)
        self.SongbookCombo.clear()
        self.SongbookCombo.addItem(u'')
        for book in books:
            row = self.SongbookCombo.count()
            self.SongbookCombo.addItem(book.name)
            self.SongbookCombo.setItemData(row, QtCore.QVariant(book.id))

    def loadThemes(self, theme_list):
        self.ThemeSelectionComboItem.clear()
        self.ThemeSelectionComboItem.addItem(u'')
        for theme in theme_list:
            self.ThemeSelectionComboItem.addItem(theme)

    def newSong(self):
        log.debug(u'New Song')
        self.SongTabWidget.setCurrentIndex(0)
        self.song = Song()
        self.TitleEditItem.setText(u'')
        self.AlternativeEdit.setText(u'')
        self.CopyrightEditItem.setText(u'')
        self.VerseOrderEdit.setText(u'')
        self.CommentsEdit.setText(u'')
        self.CCLNumberEdit.setText(u'')
        self.VerseListWidget.clear()
        self.VerseListWidget.setRowCount(0)
        self.AuthorsListView.clear()
        self.TopicsListView.clear()
        self.TitleEditItem.setFocus(QtCore.Qt.OtherFocusReason)
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()
        # it's a new song to preview is not possible
        self.previewButton.setVisible(False)

    def loadSong(self, id, preview):
        log.debug(u'Load Song')
        self.SongTabWidget.setCurrentIndex(0)
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()
        self.song = self.songmanager.get_object(Song, id)
        self.TitleEditItem.setText(self.song.title)
        if self.song.alternate_title:
            self.AlternativeEdit.setText(self.song.alternate_title)
        else:
            self.AlternativeEdit.setText(u'')
        if self.song.song_book_id != 0:
            book_name = self.songmanager.get_object(Book,
                self.song.song_book_id)
            id = self.SongbookCombo.findText(
                unicode(book_name.name), QtCore.Qt.MatchExactly)
            if id == -1:
                # Not Found
                id = 0
            self.SongbookCombo.setCurrentIndex(id)
        if self.song.theme_name:
            id = self.ThemeSelectionComboItem.findText(
                unicode(self.song.theme_name), QtCore.Qt.MatchExactly)
            if id == -1:
                # Not Found
                id = 0
                self.song.theme_name = None
            self.ThemeSelectionComboItem.setCurrentIndex(id)
        if self.song.copyright:
            self.CopyrightEditItem.setText(self.song.copyright)
        else:
            self.CopyrightEditItem.setText(u'')
        self.VerseListWidget.clear()
        self.VerseListWidget.setRowCount(0)
        if self.song.verse_order:
            self.VerseOrderEdit.setText(self.song.verse_order)
        else:
            self.VerseOrderEdit.setText(u'')
        if self.song.comments:
            self.CommentsEdit.setPlainText(self.song.comments)
        else:
            self.CommentsEdit.setPlainText(u'')
        if self.song.ccli_number:
            self.CCLNumberEdit.setText(self.song.ccli_number)
        else:
            self.CCLNumberEdit.setText(u'')
        # lazy xml migration for now
        self.VerseListWidget.clear()
        self.VerseListWidget.setRowCount(0)
        self.VerseListWidget.setColumnWidth(0, self.width)
        # This is just because occasionally the lyrics come back as a "buffer"
        if isinstance(self.song.lyrics, buffer):
            self.song.lyrics = unicode(self.song.lyrics)
        if self.song.lyrics.startswith(u'<?xml version='):
            songXML = SongXMLParser(self.song.lyrics)
            verseList = songXML.get_verses()
            for count, verse in enumerate(verseList):
                self.VerseListWidget.setRowCount(
                    self.VerseListWidget.rowCount() + 1)
                variant = u'%s:%s' % (verse[0][u'type'], verse[0][u'label'])
                item = QtGui.QTableWidgetItem(verse[1])
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(variant))
                self.VerseListWidget.setItem(count, 0, item)
        else:
            verses = self.song.lyrics.split(u'\n\n')
            for count, verse in enumerate(verses):
                self.VerseListWidget.setRowCount(
                    self.VerseListWidget.rowCount() + 1)
                item = QtGui.QTableWidgetItem(verse)
                variant = u'%s:%s' % \
                    (VerseType.to_string(VerseType.Verse), unicode(count + 1))
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(variant))
                self.VerseListWidget.setItem(count, 0, item)
        self.VerseListWidget.resizeRowsToContents()
        self.tagRows()
        # clear the results
        self.AuthorsListView.clear()
        for author in self.song.authors:
            author_name = QtGui.QListWidgetItem(unicode(author.display_name))
            author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListView.addItem(author_name)
        # clear the results
        self.TopicsListView.clear()
        for topic in self.song.topics:
            topic_name = QtGui.QListWidgetItem(unicode(topic.name))
            topic_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(topic.id))
            self.TopicsListView.addItem(topic_name)
        self.TitleEditItem.setFocus(QtCore.Qt.OtherFocusReason)
        # if not preview hide the preview button
        self.previewButton.setVisible(False)
        if preview:
            self.previewButton.setVisible(True)

    def tagRows(self):
        """
        Tag the Song List rows based on the verse list
        """
        rowLabel = []
        for row in range(0, self.VerseListWidget.rowCount()):
            item = self.VerseListWidget.item(row, 0)
            data = unicode(item.data(QtCore.Qt.UserRole).toString())
            bit = data.split(u':')
            rowTag = u'%s\n%s' % (bit[0][0:1], bit[1])
            rowLabel.append(rowTag)
        self.VerseListWidget.setVerticalHeaderLabels(rowLabel)

    def onAuthorAddButtonClicked(self):
        item = int(self.AuthorsSelectionComboItem.currentIndex())
        text = unicode(self.AuthorsSelectionComboItem.currentText())
        if item == 0 and text:
            if QtGui.QMessageBox.question(self,
                translate('SongsPlugin.EditSongForm', 'Add Author'),
                translate('SongsPlugin.EditSongForm', 'This author does not '
                'exist, do you want to add them?'),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                if text.find(u' ') == -1:
                    author = Author.populate(first_name=u'', last_name=u'',
                        display_name=text)
                else:
                    author = Author.populate(first_name=text.rsplit(u' ', 1)[0],
                        last_name=text.rsplit(u' ', 1)[1], display_name=text)
                self.songmanager.save_object(author, False)
                self.song.authors.append(author)
                author_item = QtGui.QListWidgetItem(
                    unicode(author.display_name))
                author_item.setData(QtCore.Qt.UserRole,
                    QtCore.QVariant(author.id))
                self.AuthorsListView.addItem(author_item)
                self.loadAuthors()
                self.AuthorsSelectionComboItem.setCurrentIndex(0)
            else:
                return
        elif item > 0:
            item_id = (self.AuthorsSelectionComboItem.itemData(item)).toInt()[0]
            author = self.songmanager.get_object(Author, item_id)
            if author in self.song.authors:
                QtGui.QMessageBox.warning(self,
                    translate('SongsPlugin.EditSongForm', 'Error'), 
                    translate('SongsPlugin.EditSongForm', 'This author is '
                    'already in the list.'))
            else:
                self.song.authors.append(author)
                author_item = QtGui.QListWidgetItem(unicode(
                    author.display_name))
                author_item.setData(QtCore.Qt.UserRole,
                    QtCore.QVariant(author.id))
                self.AuthorsListView.addItem(author_item)
            self.AuthorsSelectionComboItem.setCurrentIndex(0)
        else:
            QtGui.QMessageBox.warning(self,
                translate('SongsPlugin.EditSongForm', 'No Author Selected'),
                translate('SongsPlugin.EditSongForm', 'You have not selected '
                'a valid author. Either select an author from the list, '
                'or type in a new author and click the "Add Author to '
                'Song" button to add the new author.'),
                QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

    def onAuthorsListViewPressed(self):
        if self.AuthorsListView.count() > 1:
            self.AuthorRemoveButton.setEnabled(True)

    def onAuthorRemoveButtonClicked(self):
        self.AuthorRemoveButton.setEnabled(False)
        item = self.AuthorsListView.currentItem()
        author_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        author = self.songmanager.get_object(Author, author_id)
        self.song.authors.remove(author)
        row = self.AuthorsListView.row(item)
        self.AuthorsListView.takeItem(row)

    def onTopicAddButtonClicked(self):
        item = int(self.SongTopicCombo.currentIndex())
        text = unicode(self.SongTopicCombo.currentText())
        if item == 0 and text:
            if QtGui.QMessageBox.question(self,
                translate('SongsPlugin.EditSongForm', 'Add Topic'),
                translate('SongsPlugin.EditSongForm', 'This topic does not '
                'exist, do you want to add it?'),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                topic = Topic.populate(name=text)
                self.songmanager.save_object(topic, False)
                self.song.topics.append(topic)
                topic_item = QtGui.QListWidgetItem(unicode(topic.name))
                topic_item.setData(QtCore.Qt.UserRole,
                    QtCore.QVariant(topic.id))
                self.TopicsListView.addItem(topic_item)
                self.loadTopics()
                self.SongTopicCombo.setCurrentIndex(0)
            else:
                return
        elif item > 0:
            item_id = (self.SongTopicCombo.itemData(item)).toInt()[0]
            topic = self.songmanager.get_object(Topic, item_id)
            if topic in self.song.topics:
                QtGui.QMessageBox.warning(self,
                    translate('SongsPlugin.EditSongForm', 'Error'),
                    translate('SongsPlugin.EditSongForm', 'This topic is '
                    'already in the list.'))
            else:
                self.song.topics.append(topic)
                topic_item = QtGui.QListWidgetItem(unicode(topic.name))
                topic_item.setData(QtCore.Qt.UserRole,
                    QtCore.QVariant(topic.id))
                self.TopicsListView.addItem(topic_item)
            self.SongTopicCombo.setCurrentIndex(0)
        else:
            QtGui.QMessageBox.warning(self,
                translate('SongsPlugin.EditSongForm', 'No Topic Selected'),
                translate('SongsPlugin.EditSongForm', 'You have not selected '
                'a valid topic. Either select a topic from the list, or '
                'type in a new topic and click the "Add Topic to Song" '
                'button to add the new topic.'),
                QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

    def onTopicListViewPressed(self):
        self.TopicRemoveButton.setEnabled(True)

    def onTopicRemoveButtonClicked(self):
        self.TopicRemoveButton.setEnabled(False)
        item = self.TopicsListView.currentItem()
        topic_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        topic = self.songmanager.get_object(Topic, topic_id)
        self.song.topics.remove(topic)
        row = self.TopicsListView.row(item)
        self.TopicsListView.takeItem(row)

    def onSongBookComboChanged(self, item):
        if item >= 1:
            self.song.song_book_id = \
                (self.SongbookCombo.itemData(item)).toInt()[0]
        else:
            self.song.song_book_id = 0

    def onThemeComboChanged(self, item):
        if item == 0:
            # None means no Theme
            self.song.theme_name = None
        else:
            them_name = unicode(self.ThemeSelectionComboItem.itemText(item))
            self.song.theme_name = them_name

    def onVerseListViewPressed(self):
        self.VerseEditButton.setEnabled(True)
        self.VerseDeleteButton.setEnabled(True)

    def onVerseAddButtonClicked(self):
        self.verse_form.setVerse(u'', True)
        if self.verse_form.exec_():
            afterText, verse, subVerse = self.verse_form.getVerse()
            data = u'%s:%s' % (verse, subVerse)
            item = QtGui.QTableWidgetItem(afterText)
            item.setData(QtCore.Qt.UserRole, QtCore.QVariant(data))
            item.setText(afterText)
            self.VerseListWidget.setRowCount(
                self.VerseListWidget.rowCount() + 1)
            self.VerseListWidget.setItem(
                int(self.VerseListWidget.rowCount() - 1), 0, item)
        self.VerseListWidget.setColumnWidth(0, self.width)
        self.VerseListWidget.resizeRowsToContents()
        self.tagRows()

    def onVerseEditButtonClicked(self):
        item = self.VerseListWidget.currentItem()
        if item:
            tempText = item.text()
            verseId = unicode(item.data(QtCore.Qt.UserRole).toString())
            self.verse_form.setVerse(tempText, True, verseId)
            if self.verse_form.exec_():
                afterText, verse, subVerse = self.verse_form.getVerse()
                data = u'%s:%s' % (verse, subVerse)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(data))
                item.setText(afterText)
                # number of lines has change so repaint the list moving the data
                if len(tempText.split(u'\n')) != len(afterText.split(u'\n')):
                    tempList = {}
                    tempId = {}
                    for row in range(0, self.VerseListWidget.rowCount()):
                        tempList[row] = self.VerseListWidget.item(row, 0).text()
                        tempId[row] = self.VerseListWidget.item(row, 0).\
                            data(QtCore.Qt.UserRole)
                    self.VerseListWidget.clear()
                    for row in range (0, len(tempList)):
                        item = QtGui.QTableWidgetItem(tempList[row], 0)
                        item.setData(QtCore.Qt.UserRole, tempId[row])
                        self.VerseListWidget.setItem(row, 0, item)
                    self.VerseListWidget.resizeRowsToContents()
                    self.VerseListWidget.repaint()
        self.tagRows()

    def onVerseEditAllButtonClicked(self):
        verse_list = u''
        if self.VerseListWidget.rowCount() > 0:
            for row in range(0, self.VerseListWidget.rowCount()):
                item = self.VerseListWidget.item(row, 0)
                field = unicode(item.data(QtCore.Qt.UserRole).toString())
                verse_list += u'---[%s]---\n' % field
                verse_list += item.text()
                verse_list += u'\n'
            self.verse_form.setVerse(verse_list)
        else:
            self.verse_form.setVerse(u'')
        if self.verse_form.exec_():
            verse_list = self.verse_form.getVerseAll()
            verse_list = unicode(verse_list.replace(u'\r\n', u'\n'))
            self.VerseListWidget.clear()
            self.VerseListWidget.setRowCount(0)
            for row in self.findVerseSplit.split(verse_list):
                for match in row.split(u'---['):
                    for count, parts in enumerate(match.split(u']---\n')):
                        if len(parts) > 1:
                            if count == 0:
                                # make sure the tag is correctly cased
                                variant = u'%s%s' % \
                                    (parts[0:1].upper(), parts[1:].lower())
                            else:
                                if parts.endswith(u'\n'):
                                    parts = parts.rstrip(u'\n')
                                item = QtGui.QTableWidgetItem(parts)
                                item.setData(QtCore.Qt.UserRole,
                                    QtCore.QVariant(variant))
                                self.VerseListWidget.setRowCount(
                                    self.VerseListWidget.rowCount() + 1)
                                self.VerseListWidget.setItem(
                                    int(self.VerseListWidget.rowCount() - 1),
                                    0, item)
            self.VerseListWidget.setColumnWidth(0, self.width)
            self.VerseListWidget.resizeRowsToContents()
            self.VerseListWidget.repaint()
            self.tagRows()

    def onVerseDeleteButtonClicked(self):
        self.VerseListWidget.removeRow(self.VerseListWidget.currentRow())
        self.VerseEditButton.setEnabled(False)
        self.VerseDeleteButton.setEnabled(False)

    def _validate_song(self):
        """
        Check the validity of the form. Only display the 'save' if the data
        can be saved.
        """
        log.debug(u'Validate Song')
        # Lets be nice and assume the data is correct.
        if len(self.TitleEditItem.displayText()) == 0:
            self.SongTabWidget.setCurrentIndex(0)
            self.TitleEditItem.setFocus()
            QtGui.QMessageBox.critical(self,
                translate('SongsPlugin.EditSongForm', 'Error'),
                translate('SongsPlugin.EditSongForm',
                'You need to type in a song title.'))
            return False
        if self.VerseListWidget.rowCount() == 0:
            self.SongTabWidget.setCurrentIndex(0)
            self.VerseListWidget.setFocus()
            QtGui.QMessageBox.critical(self,
                translate('SongsPlugin.EditSongForm', 'Error'),
                translate('SongsPlugin.EditSongForm',
                'You need to type in at least one verse.'))
            return False
        if self.AuthorsListView.count() == 0:
            self.SongTabWidget.setCurrentIndex(1)
            self.AuthorsListView.setFocus()
            answer = QtGui.QMessageBox.warning(self,
                translate('SongsPlugin.EditSongForm', 'Warning'),
                translate('SongsPlugin.EditSongForm',
                'You have not added any authors for this song. Do you '
                'want to add an author now?'),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                return False
        if self.song.verse_order:
            order = []
            order_names = self.song.verse_order.split(u' ')
            for item in order_names:
                if len(item) == 1:
                    order.append(item.lower() + u'1')
                else:
                    order.append(item.lower())
            verses = []
            verse_names = []
            for index in range (0, self.VerseListWidget.rowCount()):
                verse = self.VerseListWidget.item(index, 0)
                verse = unicode(verse.data(QtCore.Qt.UserRole).toString())
                if verse not in verse_names:
                    verses.append(
                        re.sub(r'(.)[^:]*:(.*)', r'\1\2', verse.lower()))
                    verse_names.append(verse)
            for count, item in enumerate(order):
                if item not in verses:
                    self.SongTabWidget.setCurrentIndex(0)
                    self.VerseOrderEdit.setFocus()
                    valid = verses.pop(0)
                    for verse in verses:
                        valid = valid + u', ' + verse
                    QtGui.QMessageBox.critical(self,
                        translate('SongsPlugin.EditSongForm', 'Error'),
                        unicode(translate('SongsPlugin.EditSongForm',
                        'The verse order is invalid. There is no verse '
                        'corresponding to %s. Valid entries are %s.')) % \
                        (order_names[count], valid))
                    return False
            for count, verse in enumerate(verses):
                if verse not in order:
                    self.SongTabWidget.setCurrentIndex(0)
                    self.VerseOrderEdit.setFocus()
                    answer = QtGui.QMessageBox.warning(self,
                        translate('SongsPlugin.EditSongForm', 'Warning'),
                        unicode(translate('SongsPlugin.EditSongForm',
                        'You have not used %s anywhere in the verse '
                        'order. Are you sure you want to save the song '
                        'like this?')) % verse_names[count].replace(u':', u' '),
                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                    if answer == QtGui.QMessageBox.No:
                        return False
        return True

    def onCopyrightInsertButtonTriggered(self):
        text = self.CopyrightEditItem.text()
        pos = self.CopyrightEditItem.cursorPosition()
        text = text[:pos] + '\xa9' + text[pos:]
        self.CopyrightEditItem.setText(text)
        self.CopyrightEditItem.setFocus()
        self.CopyrightEditItem.setCursorPosition(pos + 1)

    def onMaintenanceButtonClicked(self):
        self.parent.song_maintenance_form.exec_()
        self.loadAuthors()
        self.loadBooks()
        self.loadTopics()

    def onPreview(self, button):
        """
        Save and Preview button pressed.
        The Song is valid so as the plugin to add it to preview to see.
        """
        log.debug(u'onPreview')
        if unicode(button.objectName()) == u'previewButton' and self.saveSong():
            Receiver.send_message(u'songs_preview')

    def closePressed(self):
        Receiver.send_message(u'songs_edit_clear')
        self.close()

    def accept(self):
        log.debug(u'accept')
        item = int(self.SongbookCombo.currentIndex())
        text = unicode(self.SongbookCombo.currentText())
        if item == 0 and text:
            if QtGui.QMessageBox.question(self,
                translate('SongsPlugin.EditSongForm', 'Add Book'),
                translate('SongsPlugin.EditSongForm', 'This song book does '
                'not exist, do you want to add it?'),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                book = Book.populate(name=text, publisher=u'')
                self.songmanager.save_object(book)
                self.song.book = book
                self.loadBooks()
            else:
                return
        if self.saveSong():
            Receiver.send_message(u'songs_load_list')
            self.close()

    def saveSong(self):
        self.song.title = unicode(self.TitleEditItem.text())
        self.song.alternate_title = unicode(self.AlternativeEdit.text())
        self.song.copyright = unicode(self.CopyrightEditItem.text())
        self.song.search_title = self.song.title + u'@' + \
            unicode(self.AlternativeEdit.text())
        self.song.comments = unicode(self.CommentsEdit.toPlainText())
        self.song.verse_order = unicode(self.VerseOrderEdit.text())
        self.song.ccli_number = unicode(self.CCLNumberEdit.text())
        if self._validate_song():
            self.processLyrics()
            self.processTitle()
            self.songmanager.save_object(self.song)
            return True
        return False

    def processLyrics(self):
        log.debug(u'processLyrics')
        try:
            sxml = SongXMLBuilder()
            text = u''
            multiple = []
            for i in range (0, self.VerseListWidget.rowCount()):
                item = self.VerseListWidget.item(i, 0)
                verseId = unicode(item.data(QtCore.Qt.UserRole).toString())
                bits = verseId.split(u':')
                sxml.add_verse_to_lyrics(bits[0], bits[1], unicode(item.text()))
                text = text + re.sub(r'\W+', u' ',
                    unicode(self.VerseListWidget.item(i, 0).text())) + u' '
                if (bits[1] > u'1') and (bits[0][0] not in multiple):
                    multiple.append(bits[0][0])
            self.song.search_lyrics = text
            self.song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
            for verse in multiple:
                self.song.verse_order = re.sub(u'([' + verse.upper() +
                    verse.lower() + u'])(\W|$)', r'\g<1>1\2',
                    self.song.verse_order)
        except:
            log.exception(u'Problem processing song Lyrics \n%s',
                sxml.dump_xml())

    def processTitle(self):
        log.debug(u'processTitle')
        self.song.search_title = \
            re.sub(r'[\'"`,;:(){}?]+', u'', unicode(self.song.search_title))