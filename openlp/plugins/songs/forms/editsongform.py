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

import logging
import re

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SongXMLBuilder, SongXMLParser, Receiver
from openlp.plugins.songs.forms import EditVerseForm
from openlp.plugins.songs.lib.models import Song
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
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'),
            self.onVerseListViewPressed)
        QtCore.QObject.connect(self.SongbookCombo,
            QtCore.SIGNAL(u'activated(int)'), self.onSongBookComboChanged)
        QtCore.QObject.connect(self.ThemeSelectionComboItem,
            QtCore.SIGNAL(u'activated(int)'), self.onThemeComboChanged)
        QtCore.QObject.connect(self.ThemeAddButton,
            QtCore.SIGNAL(u'clicked()'),
            self.parent.parent.render_manager.theme_manager.onAddTheme)
        QtCore.QObject.connect(self.MaintenanceButton,
            QtCore.SIGNAL(u'clicked()'), self.onMaintenanceButtonClicked)
        QtCore.QObject.connect(self.TitleEditItem,
            QtCore.SIGNAL(u'editingFinished()'), self.onTitleEditItemLostFocus)
        QtCore.QObject.connect(self.CCLNumberEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onCCLNumberEditLostFocus)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.loadThemes)
        QtCore.QObject.connect(self.CommentsEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onCommentsEditLostFocus)
        QtCore.QObject.connect(self.VerseOrderEdit,
            QtCore.SIGNAL(u'lostFocus()'), self.onVerseOrderEditLostFocus)
        self.previewButton = QtGui.QPushButton()
        self.previewButton.setText(self.trUtf8('Save && Preview'))
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
        authors = self.songmanager.get_authors()
        authorsCompleter = QtGui.QCompleter(
            [author.display_name for author in authors],
            self.AuthorsSelectionComboItem)
        authorsCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive);
        self.AuthorsSelectionComboItem.setCompleter(authorsCompleter);
        self.AuthorsSelectionComboItem.clear()
        for author in authors:
            row = self.AuthorsSelectionComboItem.count()
            self.AuthorsSelectionComboItem.addItem(author.display_name)
            self.AuthorsSelectionComboItem.setItemData(
                row, QtCore.QVariant(author.id))

    def loadTopics(self):
        topics = self.songmanager.get_topics()
        topicsCompleter = QtGui.QCompleter(
            [topic.name for topic in topics],
            self.SongTopicCombo)
        topicsCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive);
        self.SongTopicCombo.setCompleter(topicsCompleter);
        self.SongTopicCombo.clear()
        for topic in topics:
            row = self.SongTopicCombo.count()
            self.SongTopicCombo.addItem(topic.name)
            self.SongTopicCombo.setItemData(row, QtCore.QVariant(topic.id))

    def loadBooks(self):
        books = self.songmanager.get_books()
        booksCompleter = QtGui.QCompleter(
            [book.name for book in books], self.SongbookCombo)
        booksCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive);
        self.SongbookCombo.setCompleter(booksCompleter);
        self.SongbookCombo.clear()
        self.SongbookCombo.addItem(u' ')
        for book in books:
            row = self.SongbookCombo.count()
            self.SongbookCombo.addItem(book.name)
            self.SongbookCombo.setItemData(row, QtCore.QVariant(book.id))

    def loadThemes(self, theme_list):
        themesCompleter = QtGui.QCompleter(
            [theme for theme in theme_list],
            self.ThemeSelectionComboItem)
        themesCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive);
        self.ThemeSelectionComboItem.setCompleter(themesCompleter);
        self.ThemeSelectionComboItem.clear()
        self.ThemeSelectionComboItem.addItem(u' ')
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
        self.AuthorsListView.clear()
        self.TopicsListView.clear()
        self.TitleEditItem.setFocus(QtCore.Qt.OtherFocusReason)
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()
        #it's a new song to preview is not possible
        self.previewButton.setVisible(False)

    def loadSong(self, id, preview):
        log.debug(u'Load Song')
        self.SongTabWidget.setCurrentIndex(0)
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()
        self.song = self.songmanager.get_song(id)
        self.TitleEditItem.setText(self.song.title)
        title = self.song.search_title.split(u'@')
        if self.song.song_book_id != 0:
            book_name = self.songmanager.get_book(self.song.song_book_id)
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
        if len(title) > 1:
            self.AlternativeEdit.setText(title[1])
        if self.song.copyright:
            self.CopyrightEditItem.setText(self.song.copyright)
        else:
            self.CopyrightEditItem.setText(u'')
        self.VerseListWidget.clear()
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
        #lazy xml migration for now
        if self.song.lyrics.startswith(u'<?xml version='):
            songXML = SongXMLParser(self.song.lyrics)
            verseList = songXML.get_verses()
            for verse in verseList:
                variant = u'%s:%s' % (verse[0][u'type'], verse[0][u'label'])
                item = QtGui.QListWidgetItem(verse[1])
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(variant))
                self.VerseListWidget.addItem(item)
        else:
            verses = self.song.lyrics.split(u'\n\n')
            for count, verse in enumerate(verses):
                item = QtGui.QListWidgetItem(verse)
                variant = u'Verse:%s' % unicode(count + 1)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(variant))
                self.VerseListWidget.addItem(item)
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
        self._validate_song()
        self.TitleEditItem.setFocus(QtCore.Qt.OtherFocusReason)
        #if not preview hide the preview button
        self.previewButton.setVisible(False)
        if preview:
            self.previewButton.setVisible(True)

    def onAuthorAddButtonClicked(self):
        item = int(self.AuthorsSelectionComboItem.currentIndex())
        if item > -1:
            item_id = (self.AuthorsSelectionComboItem.itemData(item)).toInt()[0]
            author = self.songmanager.get_author(item_id)
            self.song.authors.append(author)
            author_item = QtGui.QListWidgetItem(unicode(author.display_name))
            author_item.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListView.addItem(author_item)

    def onAuthorsListViewPressed(self):
        if self.AuthorsListView.count() > 1:
            self.AuthorRemoveButton.setEnabled(True)

    def onAuthorRemoveButtonClicked(self):
        self.AuthorRemoveButton.setEnabled(False)
        item = self.AuthorsListView.currentItem()
        author_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        author = self.songmanager.get_author(author_id)
        self.song.authors.remove(author)
        row = self.AuthorsListView.row(item)
        self.AuthorsListView.takeItem(row)

    def onTopicAddButtonClicked(self):
        item = int(self.SongTopicCombo.currentIndex())
        if item > -1:
            item_id = (self.SongTopicCombo.itemData(item)).toInt()[0]
            topic = self.songmanager.get_topic(item_id)
            self.song.topics.append(topic)
            topic_item = QtGui.QListWidgetItem(unicode(topic.name))
            topic_item.setData(QtCore.Qt.UserRole, QtCore.QVariant(topic.id))
            self.TopicsListView.addItem(topic_item)

    def onTopicListViewPressed(self):
        self.TopicRemoveButton.setEnabled(True)

    def onTopicRemoveButtonClicked(self):
        self.TopicRemoveButton.setEnabled(False)
        item = self.TopicsListView.currentItem()
        topic_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        topic = self.songmanager.get_topic(topic_id)
        self.song.topics.remove(topic)
        row = self.TopicsListView.row(item)
        self.TopicsListView.takeItem(row)

    def onSongBookComboChanged(self, item):
        if item == 0:
            self.song.song_book_id = 0
        else:
            item = int(self.SongbookCombo.currentIndex())
            self.song.song_book_id = \
                (self.SongbookCombo.itemData(item)).toInt()[0]

    def onThemeComboChanged(self, item):
        if item == 0:
            #None means no Theme
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
            item = QtGui.QListWidgetItem(afterText)
            item.setData(QtCore.Qt.UserRole, QtCore.QVariant(data))
            item.setText(afterText)
            self.VerseListWidget.addItem(item)

    def onVerseEditButtonClicked(self):
        item = self.VerseListWidget.currentItem()
        if item:
            tempText = item.text()
            verseId = unicode((item.data(QtCore.Qt.UserRole)).toString())
            self.verse_form.setVerse(tempText, True, verseId)
            if self.verse_form.exec_():
                afterText, verse, subVerse = self.verse_form.getVerse()
                data = u'%s:%s' % (verse, subVerse)
                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(data))
                item.setText(afterText)
                #number of lines has change so repaint the list moving the data
                if len(tempText.split(u'\n')) != len(afterText.split(u'\n')):
                    tempList = {}
                    tempId = {}
                    for row in range(0, self.VerseListWidget.count()):
                        tempList[row] = self.VerseListWidget.item(row).text()
                        tempId[row] = self.VerseListWidget.item(row).\
                            data(QtCore.Qt.UserRole)
                    self.VerseListWidget.clear()
                    for row in range (0, len(tempList)):
                        item = QtGui.QListWidgetItem(tempList[row])
                        item.setData(QtCore.Qt.UserRole, tempId[row])
                        self.VerseListWidget.addItem(item)
                    self.VerseListWidget.repaint()
        self.VerseEditButton.setEnabled(False)
        self.VerseDeleteButton.setEnabled(False)

    def onVerseEditAllButtonClicked(self):
        verse_list = u''
        if self.VerseListWidget.count() > 0:
            for row in range(0, self.VerseListWidget.count()):
                item = self.VerseListWidget.item(row)
                field = unicode((item.data(QtCore.Qt.UserRole)).toString())
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
            for row in self.findVerseSplit.split(verse_list):
                for match in row.split(u'---['):
                    for count, parts in enumerate(match.split(u']---\n')):
                        if len(parts) > 1:
                            if count == 0:
                                #make sure the tag is correctly cased
                                variant = u'%s%s' % \
                                    (parts[0:1].upper(), parts[1:].lower())
                            else:
                                if parts.endswith(u'\n'):
                                    parts = parts.rstrip(u'\n')
                                item = QtGui.QListWidgetItem(parts)
                                item.setData(QtCore.Qt.UserRole, QtCore.QVariant(variant))
                                self.VerseListWidget.addItem(item)
        self.VerseListWidget.repaint()

    def onVerseDeleteButtonClicked(self):
        self.VerseListWidget.takeItem(self.VerseListWidget.currentRow())
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
            return False, self.trUtf8('You need to enter a song title.')
        if self.VerseListWidget.count() == 0:
            self.SongTabWidget.setCurrentIndex(0)
            self.VerseListWidget.setFocus()
            return False, self.trUtf8('You need to enter some verses.')
        if self.AuthorsListView.count() == 0:
            self.SongTabWidget.setCurrentIndex(2)
            self.AuthorsListView.setFocus()
        #split the verse list by space and mark lower case for testing
        taglist = unicode(self.trUtf8(' bitped'))
        for verse in unicode(self.VerseOrderEdit.text()).lower().split(u' '):
            if len(verse) > 1:
                if (verse[0:1] == u'%s' % self.trUtf8('v') or
                    verse[0:1] == u'%s' % self.trUtf8('c')) \
                    and verse[1:].isdigit():
                    pass
                else:
                    self.SongTabWidget.setCurrentIndex(0)
                    self.VerseOrderEdit.setFocus()
                    return False, \
                        self.trUtf8('Invalid verse entry - Vx or Cx')
            else:
                if taglist.find(verse) > -1:
                    pass
                else:
                    self.SongTabWidget.setCurrentIndex(0)
                    self.VerseOrderEdit.setFocus()
                    return False, \
                        self.trUtf8(\
                        'Invalid verse entry, values must be I,B,T,P,E,O,Vx,Cx')
        return True, u''

    def onTitleEditItemLostFocus(self):
        self.song.title = self.TitleEditItem.text()

    def onVerseOrderEditLostFocus(self):
        self.song.verse_order = self.VerseOrderEdit.text()

    def onCommentsEditLostFocus(self):
        self.song.comments = self.CommentsEdit.text()

    def onCCLNumberEditLostFocus(self):
        self.song.ccli_number = self.CCLNumberEdit.text()

    def onCopyrightInsertButtonTriggered(self):
        text = self.CopyrightEditItem.displayText()
        pos = self.CopyrightEditItem.cursorPosition()
        text = text[:pos] + u'©' + text[pos:]
        self.CopyrightEditItem.setText(text)
        self.CopyrightEditItem.setFocus()
        self.CopyrightEditItem.setCursorPosition(pos + 1)

    def onMaintenanceButtonClicked(self):
        self.parent.song_maintenance_form.exec_()
        self.loadAuthors()
        self.loadBooks()
        self.loadTopics()

    def onPreview(self, button):
        log.debug(u'onPreview')
        if button.text() == unicode(self.trUtf8('Save && Preview')) \
            and self.saveSong():
            Receiver.send_message(u'songs_preview')

    def closePressed(self):
        Receiver.send_message(u'songs_edit_clear')
        self.close()

    def accept(self):
        log.debug(u'accept')
        if self.saveSong():
            Receiver.send_message(u'songs_load_list')
            self.close()

    def saveSong(self):
        valid, message = self._validate_song()
        if not valid:
            QtGui.QMessageBox.critical(
                self, self.trUtf8('Error'), message,
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok))
            return False
        self.song.title = unicode(self.TitleEditItem.displayText())
        self.song.copyright = unicode(self.CopyrightEditItem.displayText())
        self.song.search_title = unicode(self.TitleEditItem.displayText()) + \
            u'@'+ unicode(self.AlternativeEdit.displayText())
        self.song.comments = unicode(self.CommentsEdit.toPlainText())
        self.song.verse_order = unicode(self.VerseOrderEdit.text())
        self.song.ccli_number = unicode(self.CCLNumberEdit.displayText())
        self.processLyrics()
        self.processTitle()
        self.songmanager.save_song(self.song)
        return True

    def processLyrics(self):
        log.debug(u'processLyrics')
        try:
            sxml = SongXMLBuilder()
            sxml.new_document()
            sxml.add_lyrics_to_song()
            text = u' '
            for i in range (0, self.VerseListWidget.count()):
                item = self.VerseListWidget.item(i)
                verseId = unicode((item.data(QtCore.Qt.UserRole)).toString())
                bits = verseId.split(u':')
                sxml.add_verse_to_lyrics(bits[0], bits[1], unicode(item.text()))
                text = text + unicode(self.VerseListWidget.item(i).text()) + u' '
            text = text.replace(u'\'', u'')
            text = text.replace(u',', u'')
            text = text.replace(u';', u'')
            text = text.replace(u':', u'')
            text = text.replace(u'(', u'')
            text = text.replace(u')', u'')
            text = text.replace(u'{', u'')
            text = text.replace(u'}', u'')
            text = text.replace(u'?', u'')
            self.song.search_lyrics = unicode(text)
            self.song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        except:
            log.exception(u'Problem processing song Lyrics \n%s',
                sxml.dump_xml())

    def processTitle(self):
        log.debug(u'processTitle')
        self.song.search_title = self.song.search_title.replace(u'\'', u'')
        self.song.search_title = self.song.search_title.replace(u'\"', u'')
        self.song.search_title = self.song.search_title.replace(u'`', u'')
        self.song.search_title = self.song.search_title.replace(u',', u'')
        self.song.search_title = self.song.search_title.replace(u';', u'')
        self.song.search_title = self.song.search_title.replace(u':', u'')
        self.song.search_title = self.song.search_title.replace(u'(', u'')
        self.song.search_title = self.song.search_title.replace(u')', u'')
        self.song.search_title = self.song.search_title.replace(u'{', u'')
        self.song.search_title = self.song.search_title.replace(u'}', u'')
        self.song.search_title = self.song.search_title.replace(u'?', u'')
        self.song.search_title = unicode(self.song.search_title)


