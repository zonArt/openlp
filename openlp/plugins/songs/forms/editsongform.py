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
"""
The :mod:`~openlp.plugins.songs.forms.editsongform` module contains the form
used to edit songs.
"""

import logging
import re
import os
import shutil

from PyQt4 import QtCore, QtGui

from openlp.core.lib import PluginStatus, Receiver, MediaType, Registry, UiStrings, translate, create_separated_list, \
    check_directory_exists
from openlp.core.lib.ui import set_case_insensitive_completer, critical_error_message_box, \
    find_and_set_in_combo_box
from openlp.core.utils import AppLocation
from openlp.plugins.songs.forms import EditVerseForm, MediaFilesForm
from openlp.plugins.songs.lib import SongXML, VerseType, clean_song
from openlp.plugins.songs.lib.db import Book, Song, Author, Topic, MediaFile
from openlp.plugins.songs.lib.ui import SongStrings
from openlp.plugins.songs.forms.editsongdialog import Ui_EditSongDialog

log = logging.getLogger(__name__)

class EditSongForm(QtGui.QDialog, Ui_EditSongDialog):
    """
    Class to manage the editing of a song
    """
    log.info(u'%s EditSongForm loaded', __name__)

    def __init__(self, mediaitem, parent, manager):
        """
        Constructor
        """
        super(EditSongForm, self).__init__(parent)
        self.mediaitem = mediaitem
        self.song = None
        # can this be automated?
        self.width = 400
        self.setupUi(self)
        # Connecting signals and slots
        QtCore.QObject.connect(self.authorAddButton, QtCore.SIGNAL(u'clicked()'), self.onAuthorAddButtonClicked)
        QtCore.QObject.connect(self.authorRemoveButton, QtCore.SIGNAL(u'clicked()'), self.onAuthorRemoveButtonClicked)
        QtCore.QObject.connect(self.authorsListView, QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'),
            self.onAuthorsListViewClicked)
        QtCore.QObject.connect(self.topicAddButton, QtCore.SIGNAL(u'clicked()'), self.onTopicAddButtonClicked)
        QtCore.QObject.connect(self.topicRemoveButton, QtCore.SIGNAL(u'clicked()'), self.onTopicRemoveButtonClicked)
        QtCore.QObject.connect(self.topicsListView, QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'),
            self.onTopicListViewClicked)
        QtCore.QObject.connect(self.copyrightInsertButton, QtCore.SIGNAL(u'clicked()'),
            self.onCopyrightInsertButtonTriggered)
        QtCore.QObject.connect(self.verseAddButton, QtCore.SIGNAL(u'clicked()'), self.onVerseAddButtonClicked)
        QtCore.QObject.connect(self.verseListWidget, QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.onVerseEditButtonClicked)
        QtCore.QObject.connect(self.verseEditButton, QtCore.SIGNAL(u'clicked()'), self.onVerseEditButtonClicked)
        QtCore.QObject.connect(self.verseEditAllButton, QtCore.SIGNAL(u'clicked()'), self.onVerseEditAllButtonClicked)
        QtCore.QObject.connect(self.verseDeleteButton, QtCore.SIGNAL(u'clicked()'), self.onVerseDeleteButtonClicked)
        QtCore.QObject.connect(self.verseListWidget, QtCore.SIGNAL(u'itemClicked(QTableWidgetItem*)'),
            self.onVerseListViewClicked)
        QtCore.QObject.connect(self.verseOrderEdit, QtCore.SIGNAL(u'textChanged(QString)'),
            self.onVerseOrderTextChanged)
        QtCore.QObject.connect(self.themeAddButton, QtCore.SIGNAL(u'clicked()'), self.theme_manager.onAddTheme)
        QtCore.QObject.connect(self.maintenanceButton, QtCore.SIGNAL(u'clicked()'), self.onMaintenanceButtonClicked)
        QtCore.QObject.connect(self.audioAddFromFileButton, QtCore.SIGNAL(u'clicked()'),
            self.onAudioAddFromFileButtonClicked)
        QtCore.QObject.connect(self.audioAddFromMediaButton, QtCore.SIGNAL(u'clicked()'),
            self.onAudioAddFromMediaButtonClicked)
        QtCore.QObject.connect(self.audioRemoveButton, QtCore.SIGNAL(u'clicked()'), self.onAudioRemoveButtonClicked)
        QtCore.QObject.connect(self.audioRemoveAllButton, QtCore.SIGNAL(u'clicked()'),
            self.onAudioRemoveAllButtonClicked)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_update_list'), self.loadThemes)
        self.previewButton = QtGui.QPushButton()
        self.previewButton.setObjectName(u'previewButton')
        self.previewButton.setText(UiStrings().SaveAndPreview)
        self.button_box.addButton(self.previewButton, QtGui.QDialogButtonBox.ActionRole)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(u'clicked(QAbstractButton*)'), self.onPreview)
        # Create other objects and forms
        self.manager = manager
        self.verseForm = EditVerseForm(self)
        self.mediaForm = MediaFilesForm(self)
        self.initialise()
        self.authorsListView.setSortingEnabled(False)
        self.authorsListView.setAlternatingRowColors(True)
        self.topicsListView.setSortingEnabled(False)
        self.topicsListView.setAlternatingRowColors(True)
        self.audioListWidget.setAlternatingRowColors(True)
        self.findVerseSplit = re.compile(u'---\[\]---\n', re.UNICODE)
        self.whitespace = re.compile(r'\W+', re.UNICODE)

    def initialise(self):
        """
        Set up the form for when it is displayed.
        """
        self.verseEditButton.setEnabled(False)
        self.verseDeleteButton.setEnabled(False)
        self.authorRemoveButton.setEnabled(False)
        self.topicRemoveButton.setEnabled(False)

    def loadAuthors(self):
        """
        Load the authors from the database into the combobox.
        """
        authors = self.manager.get_all_objects(Author,
            order_by_ref=Author.display_name)
        self.authorsComboBox.clear()
        self.authorsComboBox.addItem(u'')
        self.authors = []
        for author in authors:
            row = self.authorsComboBox.count()
            self.authorsComboBox.addItem(author.display_name)
            self.authorsComboBox.setItemData(row, author.id)
            self.authors.append(author.display_name)
        set_case_insensitive_completer(self.authors, self.authorsComboBox)

    def loadTopics(self):
        """
        Load the topics into the combobox.
        """
        self.topics = []
        self.__loadObjects(Topic, self.topicsComboBox, self.topics)

    def loadBooks(self):
        """
        Load the song books into the combobox
        """
        self.books = []
        self.__loadObjects(Book, self.songBookComboBox, self.books)

    def __loadObjects(self, cls, combo, cache):
        """
        Generically load a set of objects into a cache and a combobox.
        """
        objects = self.manager.get_all_objects(cls, order_by_ref=cls.name)
        combo.clear()
        combo.addItem(u'')
        for object in objects:
            row = combo.count()
            combo.addItem(object.name)
            cache.append(object.name)
            combo.setItemData(row, object.id)
        set_case_insensitive_completer(cache, combo)

    def loadThemes(self, theme_list):
        """
        Load the themes into a combobox.
        """
        self.themeComboBox.clear()
        self.themeComboBox.addItem(u'')
        self.themes = theme_list
        self.themeComboBox.addItems(theme_list)
        set_case_insensitive_completer(self.themes, self.themeComboBox)

    def loadMediaFiles(self):
        """
        Load the media files into a combobox.
        """
        self.audioAddFromMediaButton.setVisible(False)
        for plugin in self.plugin_manager.plugins:
            if plugin.name == u'media' and plugin.status == PluginStatus.Active:
                self.audioAddFromMediaButton.setVisible(True)
                self.mediaForm.populateFiles(plugin.mediaItem.getList(MediaType.Audio))
                break

    def newSong(self):
        """
        Blank the edit form out in preparation for a new song.
        """
        log.debug(u'New Song')
        self.song = None
        self.initialise()
        self.songTabWidget.setCurrentIndex(0)
        self.titleEdit.clear()
        self.alternativeEdit.clear()
        self.copyrightEdit.clear()
        self.verseOrderEdit.clear()
        self.commentsEdit.clear()
        self.CCLNumberEdit.clear()
        self.verseListWidget.clear()
        self.verseListWidget.setRowCount(0)
        self.authorsListView.clear()
        self.topicsListView.clear()
        self.audioListWidget.clear()
        self.titleEdit.setFocus()
        self.songBookNumberEdit.clear()
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()
        self.loadMediaFiles()
        self.themeComboBox.setCurrentIndex(0)
        # it's a new song to preview is not possible
        self.previewButton.setVisible(False)

    def loadSong(self, id, preview=False):
        """
        Loads a song.

        ``id``
            The song id (int).

        ``preview``
            Should be ``True`` if the song is also previewed (boolean).
        """
        log.debug(u'Load Song')
        self.initialise()
        self.songTabWidget.setCurrentIndex(0)
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()
        self.loadMediaFiles()
        self.song = self.manager.get_object(Song, id)
        self.titleEdit.setText(self.song.title)
        self.alternativeEdit.setText(
            self.song.alternate_title if self.song.alternate_title else u'')
        if self.song.song_book_id != 0:
            book_name = self.manager.get_object(Book, self.song.song_book_id)
            find_and_set_in_combo_box(self.songBookComboBox, unicode(book_name.name))
        if self.song.theme_name:
            find_and_set_in_combo_box(self.themeComboBox, unicode(self.song.theme_name))
        self.copyrightEdit.setText(self.song.copyright if self.song.copyright else u'')
        self.commentsEdit.setPlainText(self.song.comments if self.song.comments else u'')
        self.CCLNumberEdit.setText(self.song.ccli_number if self.song.ccli_number else u'')
        self.songBookNumberEdit.setText(self.song.song_number if self.song.song_number else u'')
        # lazy xml migration for now
        self.verseListWidget.clear()
        self.verseListWidget.setRowCount(0)
        # This is just because occasionally the lyrics come back as a "buffer"
        if isinstance(self.song.lyrics, buffer):
            self.song.lyrics = unicode(self.song.lyrics)
        verse_tags_translated = False
        if self.song.lyrics.startswith(u'<?xml version='):
            songXML = SongXML()
            verse_list = songXML.get_verses(self.song.lyrics)
            for count, verse in enumerate(verse_list):
                self.verseListWidget.setRowCount(
                    self.verseListWidget.rowCount() + 1)
                # This silently migrates from localized verse type markup.
                # If we trusted the database, this would be unnecessary.
                verse_tag = verse[0][u'type']
                index = None
                if len(verse_tag) > 1:
                    index = VerseType.from_translated_string(verse_tag)
                    if index is None:
                        index = VerseType.from_string(verse_tag, None)
                    else:
                        verse_tags_translated = True
                if index is None:
                    index = VerseType.from_tag(verse_tag)
                verse[0][u'type'] = VerseType.Tags[index]
                if verse[0][u'label'] == u'':
                    verse[0][u'label'] = u'1'
                verse_def = u'%s%s' % (verse[0][u'type'], verse[0][u'label'])
                item = QtGui.QTableWidgetItem(verse[1])
                item.setData(QtCore.Qt.UserRole, verse_def)
                self.verseListWidget.setItem(count, 0, item)
        else:
            verses = self.song.lyrics.split(u'\n\n')
            for count, verse in enumerate(verses):
                self.verseListWidget.setRowCount(self.verseListWidget.rowCount() + 1)
                item = QtGui.QTableWidgetItem(verse)
                verse_def = u'%s%s' % (VerseType.Tags[VerseType.Verse], unicode(count + 1))
                item.setData(QtCore.Qt.UserRole, verse_def)
                self.verseListWidget.setItem(count, 0, item)
        if self.song.verse_order:
            # we translate verse order
            translated = []
            for verse_def in self.song.verse_order.split():
                verse_index = None
                if verse_tags_translated:
                    verse_index = VerseType.from_translated_tag(verse_def[0], None)
                if verse_index is None:
                    verse_index = VerseType.from_tag(verse_def[0])
                verse_tag = VerseType.TranslatedTags[verse_index].upper()
                translated.append(u'%s%s' % (verse_tag, verse_def[1:]))
            self.verseOrderEdit.setText(u' '.join(translated))
        else:
            self.verseOrderEdit.setText(u'')
        self.tagRows()
        # clear the results
        self.authorsListView.clear()
        for author in self.song.authors:
            author_name = QtGui.QListWidgetItem(unicode(author.display_name))
            author_name.setData(QtCore.Qt.UserRole, author.id)
            self.authorsListView.addItem(author_name)
        # clear the results
        self.topicsListView.clear()
        for topic in self.song.topics:
            topic_name = QtGui.QListWidgetItem(unicode(topic.name))
            topic_name.setData(QtCore.Qt.UserRole, topic.id)
            self.topicsListView.addItem(topic_name)
        self.audioListWidget.clear()
        for media in self.song.media_files:
            media_file = QtGui.QListWidgetItem(os.path.split(media.file_name)[1])
            media_file.setData(QtCore.Qt.UserRole, media.file_name)
            self.audioListWidget.addItem(media_file)
        self.titleEdit.setFocus()
        # Hide or show the preview button.
        self.previewButton.setVisible(preview)

    def tagRows(self):
        """
        Tag the Song List rows based on the verse list
        """
        row_label = []
        for row in range(self.verseListWidget.rowCount()):
            item = self.verseListWidget.item(row, 0)
            verse_def = item.data(QtCore.Qt.UserRole)
            verse_tag = VerseType.translated_tag(verse_def[0])
            row_def = u'%s%s' % (verse_tag, verse_def[1:])
            row_label.append(row_def)
        self.verseListWidget.setVerticalHeaderLabels(row_label)
        self.verseListWidget.resizeRowsToContents()
        self.verseListWidget.repaint()

    def onAuthorAddButtonClicked(self):
        """
        Add the author to the list of authors associated with this song when the button is clicked.
        """
        item = int(self.authorsComboBox.currentIndex())
        text = self.authorsComboBox.currentText().strip(u' \r\n\t')
        # This if statement is for OS X, which doesn't seem to work well with
        # the QCompleter autocompletion class. See bug #812628.
        if text in self.authors:
            # Index 0 is a blank string, so add 1
            item = self.authors.index(text) + 1
        if item == 0 and text:
            if QtGui.QMessageBox.question(self,
                translate('SongsPlugin.EditSongForm', 'Add Author'),
                translate('SongsPlugin.EditSongForm', 'This author does not exist, do you want to add them?'),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                if text.find(u' ') == -1:
                    author = Author.populate(first_name=u'', last_name=u'', display_name=text)
                else:
                    author = Author.populate(first_name=text.rsplit(u' ', 1)[0],
                        last_name=text.rsplit(u' ', 1)[1], display_name=text)
                self.manager.save_object(author)
                self.__addAuthorToList(author)
                self.loadAuthors()
                self.authorsComboBox.setCurrentIndex(0)
            else:
                return
        elif item > 0:
            item_id = (self.authorsComboBox.itemData(item))
            author = self.manager.get_object(Author, item_id)
            if self.authorsListView.findItems(unicode(author.display_name),
                QtCore.Qt.MatchExactly):
                critical_error_message_box(
                    message=translate('SongsPlugin.EditSongForm', 'This author is already in the list.'))
            else:
                self.__addAuthorToList(author)
            self.authorsComboBox.setCurrentIndex(0)
        else:
            QtGui.QMessageBox.warning(self, UiStrings().NISs,
                translate('SongsPlugin.EditSongForm', 'You have not selected a valid author. Either select an author '
                    'from the list, or type in a new author and click the "Add Author to Song" button to add '
                    'the new author.'))

    def __addAuthorToList(self, author):
        """
        Add an author to the author list.
        """
        author_item = QtGui.QListWidgetItem(unicode(author.display_name))
        author_item.setData(QtCore.Qt.UserRole, author.id)
        self.authorsListView.addItem(author_item)

    def onAuthorsListViewClicked(self):
        """
        Run a set of actions when an author in the list is selected (mainly enable the delete button).
        """
        if self.authorsListView.count() > 1:
            self.authorRemoveButton.setEnabled(True)

    def onAuthorRemoveButtonClicked(self):
        """
        Remove the author from the list when the delete button is clicked.
        """
        self.authorRemoveButton.setEnabled(False)
        item = self.authorsListView.currentItem()
        row = self.authorsListView.row(item)
        self.authorsListView.takeItem(row)

    def onTopicAddButtonClicked(self):
        item = int(self.topicsComboBox.currentIndex())
        text = self.topicsComboBox.currentText()
        if item == 0 and text:
            if QtGui.QMessageBox.question(self, translate('SongsPlugin.EditSongForm', 'Add Topic'),
                    translate('SongsPlugin.EditSongForm', 'This topic does not exist, do you want to add it?'),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                topic = Topic.populate(name=text)
                self.manager.save_object(topic)
                topic_item = QtGui.QListWidgetItem(unicode(topic.name))
                topic_item.setData(QtCore.Qt.UserRole, topic.id)
                self.topicsListView.addItem(topic_item)
                self.loadTopics()
                self.topicsComboBox.setCurrentIndex(0)
            else:
                return
        elif item > 0:
            item_id = (self.topicsComboBox.itemData(item))
            topic = self.manager.get_object(Topic, item_id)
            if self.topicsListView.findItems(unicode(topic.name),
                QtCore.Qt.MatchExactly):
                critical_error_message_box(
                    message=translate('SongsPlugin.EditSongForm', 'This topic is already in the list.'))
            else:
                topic_item = QtGui.QListWidgetItem(unicode(topic.name))
                topic_item.setData(QtCore.Qt.UserRole, topic.id)
                self.topicsListView.addItem(topic_item)
            self.topicsComboBox.setCurrentIndex(0)
        else:
            QtGui.QMessageBox.warning(self, UiStrings().NISs,
                translate('SongsPlugin.EditSongForm', 'You have not selected a valid topic. Either select a topic '
                'from the list, or type in a new topic and click the "Add Topic to Song" button to add the new topic.'))

    def onTopicListViewClicked(self):
        self.topicRemoveButton.setEnabled(True)

    def onTopicRemoveButtonClicked(self):
        self.topicRemoveButton.setEnabled(False)
        item = self.topicsListView.currentItem()
        row = self.topicsListView.row(item)
        self.topicsListView.takeItem(row)

    def onVerseListViewClicked(self):
        self.verseEditButton.setEnabled(True)
        self.verseDeleteButton.setEnabled(True)

    def onVerseAddButtonClicked(self):
        self.verseForm.setVerse(u'', True)
        if self.verseForm.exec_():
            after_text, verse_tag, verse_num = self.verseForm.getVerse()
            verse_def = u'%s%s' % (verse_tag, verse_num)
            item = QtGui.QTableWidgetItem(after_text)
            item.setData(QtCore.Qt.UserRole, verse_def)
            item.setText(after_text)
            self.verseListWidget.setRowCount(self.verseListWidget.rowCount() + 1)
            self.verseListWidget.setItem(self.verseListWidget.rowCount() - 1, 0, item)
        self.tagRows()
        # Check if all verse tags are used.
        self.onVerseOrderTextChanged(self.verseOrderEdit.text())

    def onVerseEditButtonClicked(self):
        item = self.verseListWidget.currentItem()
        if item:
            temp_text = item.text()
            verse_id = item.data(QtCore.Qt.UserRole)
            self.verseForm.setVerse(temp_text, True, verse_id)
            if self.verseForm.exec_():
                after_text, verse_tag, verse_num = self.verseForm.getVerse()
                verse_def = u'%s%s' % (verse_tag, verse_num)
                item.setData(QtCore.Qt.UserRole, verse_def)
                item.setText(after_text)
                # number of lines has changed, repaint the list moving the data
                if len(temp_text.split(u'\n')) != len(after_text.split(u'\n')):
                    temp_list = []
                    temp_ids = []
                    for row in range(self.verseListWidget.rowCount()):
                        item = self.verseListWidget.item(row, 0)
                        temp_list.append(item.text())
                        temp_ids.append(item.data(QtCore.Qt.UserRole))
                    self.verseListWidget.clear()
                    for row, entry in enumerate(temp_list):
                        item = QtGui.QTableWidgetItem(entry, 0)
                        item.setData(QtCore.Qt.UserRole, temp_ids[row])
                        self.verseListWidget.setItem(row, 0, item)
        self.tagRows()
        # Check if all verse tags are used.
        self.onVerseOrderTextChanged(self.verseOrderEdit.text())

    def onVerseEditAllButtonClicked(self):
        verse_list = u''
        if self.verseListWidget.rowCount() > 0:
            for row in range(self.verseListWidget.rowCount()):
                item = self.verseListWidget.item(row, 0)
                field = item.data(QtCore.Qt.UserRole)
                verse_tag = VerseType.translated_name(field[0])
                verse_num = field[1:]
                verse_list += u'---[%s:%s]---\n' % (verse_tag, verse_num)
                verse_list += item.text()
                verse_list += u'\n'
            self.verseForm.setVerse(verse_list)
        else:
            self.verseForm.setVerse(u'')
        if not self.verseForm.exec_():
            return
        verse_list = self.verseForm.getVerseAll()
        verse_list = unicode(verse_list.replace(u'\r\n', u'\n'))
        self.verseListWidget.clear()
        self.verseListWidget.setRowCount(0)
        for row in self.findVerseSplit.split(verse_list):
            for match in row.split(u'---['):
                for count, parts in enumerate(match.split(u']---\n')):
                    if count == 0:
                        if len(parts) == 0:
                            continue
                        # handling carefully user inputted versetags
                        separator = parts.find(u':')
                        if separator >= 0:
                            verse_name = parts[0:separator].strip()
                            verse_num = parts[separator+1:].strip()
                        else:
                            verse_name = parts
                            verse_num = u'1'
                        verse_index = VerseType.from_loose_input(verse_name)
                        verse_tag = VerseType.Tags[verse_index]
                        # Later we need to handle v1a as well.
                        #regex = re.compile(r'(\d+\w.)')
                        regex = re.compile(r'\D*(\d+)\D*')
                        match = regex.match(verse_num)
                        if match:
                            verse_num = match.group(1)
                        else:
                            verse_num = u'1'
                        verse_def = u'%s%s' % (verse_tag, verse_num)
                    else:
                        if parts.endswith(u'\n'):
                            parts = parts.rstrip(u'\n')
                        item = QtGui.QTableWidgetItem(parts)
                        item.setData(QtCore.Qt.UserRole, verse_def)
                        self.verseListWidget.setRowCount(self.verseListWidget.rowCount() + 1)
                        self.verseListWidget.setItem(self.verseListWidget.rowCount() - 1, 0, item)
        self.tagRows()
        self.verseEditButton.setEnabled(False)
        self.verseDeleteButton.setEnabled(False)
        # Check if all verse tags are used.
        self.onVerseOrderTextChanged(self.verseOrderEdit.text())

    def onVerseDeleteButtonClicked(self):
        self.verseListWidget.removeRow(self.verseListWidget.currentRow())
        if not self.verseListWidget.selectedItems():
            self.verseEditButton.setEnabled(False)
            self.verseDeleteButton.setEnabled(False)

    def onVerseOrderTextChanged(self, text):
        verses = []
        verse_names = []
        order = self.__extractVerseOrder(text)
        for index in range(self.verseListWidget.rowCount()):
            verse = self.verseListWidget.item(index, 0)
            verse = verse.data(QtCore.Qt.UserRole)
            if verse not in verse_names:
                verses.append(verse)
                verse_names.append(u'%s%s' % (VerseType.translated_tag(verse[0]), verse[1:]))
        verses_not_used = []
        for verse in verses:
            if not verse in order:
                verses_not_used.append(verse)
        self.warningLabel.setVisible(len(verses_not_used) > 0)

    def __extractVerseOrder(self, verse_order):
        order = []
        order_names = unicode(verse_order).split()
        for item in order_names:
            if len(item) == 1:
                verse_index = VerseType.from_translated_tag(item, None)
                if verse_index is not None:
                    order.append(VerseType.Tags[verse_index] + u'1')
                else:
                    # it matches no verses anyway
                    order.append(u'')
            else:
                verse_index = VerseType.from_translated_tag(item[0], None)
                if verse_index is None:
                    # it matches no verses anyway
                    order.append(u'')
                else:
                    verse_tag = VerseType.Tags[verse_index]
                    verse_num = item[1:].lower()
                    order.append(verse_tag + verse_num)
        return order

    def __validateVerseList(self, verse_order, verse_count):
        verses = []
        invalid_verses = []
        verse_names = []
        order_names = unicode(verse_order).split()
        order = self.__extractVerseOrder(verse_order)
        for index in range(verse_count):
            verse = self.verseListWidget.item(index, 0)
            verse = verse.data(QtCore.Qt.UserRole)
            if verse not in verse_names:
                verses.append(verse)
                verse_names.append(u'%s%s' % (VerseType.translated_tag(verse[0]), verse[1:]))
        for count, item in enumerate(order):
            if item not in verses:
                invalid_verses.append(order_names[count])
        if invalid_verses:
            valid = create_separated_list(verse_names)
            if len(invalid_verses) > 1:
                critical_error_message_box(message=translate('SongsPlugin.EditSongForm',
                    'The verse order is invalid. There are no verses corresponding to %s. Valid entries are %s.') %
                    (u', '.join(invalid_verses), valid))
            else:
                critical_error_message_box(message=translate('SongsPlugin.EditSongForm',
                    'The verse order is invalid. There is no verse corresponding to %s. Valid entries are %s.') %
                    (invalid_verses[0], valid))
        return len(invalid_verses) == 0

    def __validateSong(self):
        """
        Check the validity of the song.
        """
        # This checks data in the form *not* self.song. self.song is still
        # None at this point.
        log.debug(u'Validate Song')
        # Lets be nice and assume the data is correct.
        if not self.titleEdit.text():
            self.songTabWidget.setCurrentIndex(0)
            self.titleEdit.setFocus()
            critical_error_message_box(
                message=translate('SongsPlugin.EditSongForm', 'You need to type in a song title.'))
            return False
        if self.verseListWidget.rowCount() == 0:
            self.songTabWidget.setCurrentIndex(0)
            self.verseListWidget.setFocus()
            critical_error_message_box(
                message=translate('SongsPlugin.EditSongForm', 'You need to type in at least one verse.'))
            return False
        if self.authorsListView.count() == 0:
            self.songTabWidget.setCurrentIndex(1)
            self.authorsListView.setFocus()
            critical_error_message_box(
                message=translate('SongsPlugin.EditSongForm', 'You need to have an author for this song.'))
            return False
        if self.verseOrderEdit.text():
            result = self.__validateVerseList(self.verseOrderEdit.text(),
                self.verseListWidget.rowCount())
            if not result:
                return False
        text = self.songBookComboBox.currentText()
        if self.songBookComboBox.findText(text, QtCore.Qt.MatchExactly) < 0:
            if QtGui.QMessageBox.question(self, translate('SongsPlugin.EditSongForm', 'Add Book'),
                    translate('SongsPlugin.EditSongForm', 'This song book does not exist, do you want to add it?'),
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes) == QtGui.QMessageBox.Yes:
                book = Book.populate(name=text, publisher=u'')
                self.manager.save_object(book)
            else:
                return False
        return True

    def onCopyrightInsertButtonTriggered(self):
        text = self.copyrightEdit.text()
        pos = self.copyrightEdit.cursorPosition()
        sign = SongStrings.CopyrightSymbol
        text = text[:pos] + sign + text[pos:]
        self.copyrightEdit.setText(text)
        self.copyrightEdit.setFocus()
        self.copyrightEdit.setCursorPosition(pos + len(sign))

    def onMaintenanceButtonClicked(self):
        temp_song_book = None
        item = int(self.songBookComboBox.currentIndex())
        text = self.songBookComboBox.currentText()
        if item == 0 and text:
            temp_song_book = text
        self.mediaitem.songMaintenanceForm.exec_(True)
        self.loadAuthors()
        self.loadBooks()
        self.loadTopics()
        if temp_song_book:
            self.songBookComboBox.setEditText(temp_song_book)

    def onPreview(self, button):
        """
        Save and Preview button clicked.
        The Song is valid so as the plugin to add it to preview to see.

        ``button``
            A button (QPushButton).
        """
        log.debug(u'onPreview')
        if button.objectName() == u'previewButton':
            self.saveSong(True)
            Receiver.send_message(u'songs_preview')

    def onAudioAddFromFileButtonClicked(self):
        """
        Loads file(s) from the filesystem.
        """
        filters = u'%s (*)' % UiStrings().AllFiles
        filenames = QtGui.QFileDialog.getOpenFileNames(self,
            translate('SongsPlugin.EditSongForm', 'Open File(s)'), u'', filters)
        for filename in filenames:
            item = QtGui.QListWidgetItem(os.path.split(unicode(filename))[1])
            item.setData(QtCore.Qt.UserRole, filename)
            self.audioListWidget.addItem(item)

    def onAudioAddFromMediaButtonClicked(self):
        """
        Loads file(s) from the media plugin.
        """
        if self.mediaForm.exec_():
            for filename in self.mediaForm.getSelectedFiles():
                item = QtGui.QListWidgetItem(os.path.split(unicode(filename))[1])
                item.setData(QtCore.Qt.UserRole, filename)
                self.audioListWidget.addItem(item)

    def onAudioRemoveButtonClicked(self):
        """
        Removes a file from the list.
        """
        row = self.audioListWidget.currentRow()
        if row == -1:
            return
        self.audioListWidget.takeItem(row)

    def onAudioRemoveAllButtonClicked(self):
        """
        Removes all files from the list.
        """
        self.audioListWidget.clear()

    def onUpButtonClicked(self):
        """
        Moves a file up when the user clicks the up button on the audio tab.
        """
        row = self.audioListWidget.currentRow()
        if row <= 0:
            return
        item = self.audioListWidget.takeItem(row)
        self.audioListWidget.insertItem(row - 1, item)
        self.audioListWidget.setCurrentRow(row - 1)

    def onDownButtonClicked(self):
        """
        Moves a file down when the user clicks the up button on the audio tab.
        """
        row = self.audioListWidget.currentRow()
        if row == -1 or row > self.audioListWidget.count() - 1:
            return
        item = self.audioListWidget.takeItem(row)
        self.audioListWidget.insertItem(row + 1, item)
        self.audioListWidget.setCurrentRow(row + 1)

    def clearCaches(self):
        """
        Free up autocompletion memory on dialog exit
        """
        log.debug (u'SongEditForm.clearCaches')
        self.authors = []
        self.themes = []
        self.books = []
        self.topics = []

    def reject(self):
        """
        Exit Dialog and do not save
        """
        log.debug (u'SongEditForm.reject')
        self.clearCaches()
        QtGui.QDialog.reject(self)

    def accept(self):
        """
        Exit Dialog and save song if valid
        """
        log.debug(u'SongEditForm.accept')
        self.clearCaches()
        if self.__validateSong():
            self.saveSong()
            self.song = None
            QtGui.QDialog.accept(self)

    def saveSong(self, preview=False):
        """
        Get all the data from the widgets on the form, and then save it to the
        database. The form has been validated and all reference items
        (Authors, Books and Topics) have been saved before this function is
        called.

        ``preview``
            Should be ``True`` if the song is also previewed (boolean).
        """
        # The Song() assignment. No database calls should be made while a
        # Song() is in a partially complete state.
        if not self.song:
            self.song = Song()
        self.song.title = self.titleEdit.text()
        self.song.alternate_title = self.alternativeEdit.text()
        self.song.copyright = self.copyrightEdit.text()
        # Values will be set when cleaning the song.
        self.song.search_title = u''
        self.song.search_lyrics = u''
        self.song.verse_order = u''
        self.song.comments = self.commentsEdit.toPlainText()
        ordertext = self.verseOrderEdit.text()
        order = []
        for item in ordertext.split():
            verse_tag = VerseType.Tags[VerseType.from_translated_tag(item[0])]
            verse_num = item[1:].lower()
            order.append(u'%s%s' % (verse_tag, verse_num))
        self.song.verse_order = u' '.join(order)
        self.song.ccli_number = self.CCLNumberEdit.text()
        self.song.song_number = self.songBookNumberEdit.text()
        book_name = self.songBookComboBox.currentText()
        if book_name:
            self.song.book = self.manager.get_object_filtered(Book,
                Book.name == book_name)
        else:
            self.song.book = None
        theme_name = self.themeComboBox.currentText()
        if theme_name:
            self.song.theme_name = theme_name
        else:
            self.song.theme_name = None
        self._processLyrics()
        self.song.authors = []
        for row in xrange(self.authorsListView.count()):
            item = self.authorsListView.item(row)
            authorId = (item.data(QtCore.Qt.UserRole))
            author = self.manager.get_object(Author, authorId)
            if author is not None:
                self.song.authors.append(author)
        self.song.topics = []
        for row in xrange(self.topicsListView.count()):
            item = self.topicsListView.item(row)
            topicId = (item.data(QtCore.Qt.UserRole))
            topic = self.manager.get_object(Topic, topicId)
            if topic is not None:
                self.song.topics.append(topic)
        # Save the song here because we need a valid id for the audio files.
        clean_song(self.manager, self.song)
        self.manager.save_object(self.song)
        audio_files = map(lambda a: a.file_name, self.song.media_files)
        log.debug(audio_files)
        save_path = os.path.join(AppLocation.get_section_data_path(self.mediaitem.plugin.name), 'audio',
            str(self.song.id))
        check_directory_exists(save_path)
        self.song.media_files = []
        files = []
        for row in xrange(self.audioListWidget.count()):
            item = self.audioListWidget.item(row)
            filename = item.data(QtCore.Qt.UserRole)
            if not filename.startswith(save_path):
                oldfile, filename = filename, os.path.join(save_path, os.path.split(filename)[1])
                shutil.copyfile(oldfile, filename)
            files.append(filename)
            media_file = MediaFile()
            media_file.file_name = filename
            media_file.type = u'audio'
            media_file.weight = row
            self.song.media_files.append(media_file)
        for audio in audio_files:
            if audio not in files:
                try:
                    os.remove(audio)
                except:
                    log.exception('Could not remove file: %s', audio)
        if not files:
            try:
                os.rmdir(save_path)
            except OSError:
                log.exception(u'Could not remove directory: %s', save_path)
        clean_song(self.manager, self.song)
        self.manager.save_object(self.song)
        self.mediaitem.autoSelectId = self.song.id

    def _processLyrics(self):
        """
        Process the lyric data entered by the user into the OpenLP XML format.
        """
        # This method must only be run after the self.song = Song() assignment.
        log.debug(u'_processLyrics')
        try:
            sxml = SongXML()
            multiple = []
            for i in range(self.verseListWidget.rowCount()):
                item = self.verseListWidget.item(i, 0)
                verse_id = item.data(QtCore.Qt.UserRole)
                verse_tag = verse_id[0]
                verse_num = verse_id[1:]
                sxml.add_verse_to_lyrics(verse_tag, verse_num, item.text())
                if verse_num > u'1' and verse_tag not in multiple:
                    multiple.append(verse_tag)
            self.song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
            for verse in multiple:
                self.song.verse_order = re.sub(u'([' + verse.upper() + verse.lower() + u'])(\W|$)', r'\g<1>1\2',
                    self.song.verse_order)
        except:
            log.exception(u'Problem processing song Lyrics \n%s', sxml.dump_xml())

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, u'_plugin_manager'):
            self._plugin_manager = Registry().get(u'plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)

    def _get_theme_manager(self):
        """
        Adds the theme manager to the class dynamically
        """
        if not hasattr(self, u'_theme_manager'):
            self._theme_manager = Registry().get(u'theme_manager')
        return self._theme_manager

    theme_manager = property(_get_theme_manager)

