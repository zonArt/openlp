# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import locale
import re

from PyQt4 import QtCore, QtGui
from sqlalchemy.sql import or_

from openlp.core.lib import MediaManagerItem, Receiver, ItemCapabilities, \
    translate, check_item_selected, PluginStatus
from openlp.core.lib.searchedit import SearchEdit
from openlp.core.lib.ui import UiStrings
from openlp.plugins.songs.forms import EditSongForm, SongMaintenanceForm, \
    SongImportForm, SongExportForm
from openlp.plugins.songs.lib import OpenLyrics, SongXML, VerseType
from openlp.plugins.songs.lib.db import Author, Song
from openlp.plugins.songs.lib.ui import SongStrings

log = logging.getLogger(__name__)

class SongSearch(object):
    """
    An enumeration for song search methods.
    """
    Entire = 1
    Titles = 2
    Lyrics = 3
    Authors = 4
    Themes = 5


class SongMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Songs.
    """
    log.info(u'Song Media Item loaded')

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'songs/song'
        MediaManagerItem.__init__(self, parent, self, icon)
        self.edit_song_form = EditSongForm(self, self.parent.manager)
        self.openLyrics = OpenLyrics(self.parent.manager)
        self.singleServiceItem = False
        self.song_maintenance_form = SongMaintenanceForm(
            self.parent.manager, self)
        # Holds information about whether the edit is remotly triggered and
        # which Song is required.
        self.remoteSong = -1
        self.editItem = None
        self.whitespace = re.compile(r'\W+', re.UNICODE)
        self.quickPreviewAllowed = True

    def addEndHeaderBar(self):
        self.addToolbarSeparator()
        ## Song Maintenance Button ##
        self.maintenanceAction = self.addToolbarButton(u'', u'',
            ':/songs/song_maintenance.png', self.onSongMaintenanceClick)
        self.searchWidget = QtGui.QWidget(self)
        self.searchWidget.setObjectName(u'searchWidget')
        self.searchLayout = QtGui.QVBoxLayout(self.searchWidget)
        self.searchLayout.setObjectName(u'searchLayout')
        self.searchTextLayout = QtGui.QFormLayout()
        self.searchTextLayout.setObjectName(u'searchTextLayout')
        self.searchTextLabel = QtGui.QLabel(self.searchWidget)
        self.searchTextLabel.setObjectName(u'searchTextLabel')
        self.searchTextEdit = SearchEdit(self.searchWidget)
        self.searchTextEdit.setObjectName(u'searchTextEdit')
        self.searchTextLabel.setBuddy(self.searchTextEdit)
        self.searchTextLayout.addRow(self.searchTextLabel, self.searchTextEdit)
        self.searchLayout.addLayout(self.searchTextLayout)
        self.searchButtonLayout = QtGui.QHBoxLayout()
        self.searchButtonLayout.setObjectName(u'searchButtonLayout')
        self.searchButtonLayout.addStretch()
        self.searchTextButton = QtGui.QPushButton(self.searchWidget)
        self.searchTextButton.setObjectName(u'searchTextButton')
        self.searchButtonLayout.addWidget(self.searchTextButton)
        self.searchLayout.addLayout(self.searchButtonLayout)
        self.pageLayout.addWidget(self.searchWidget)
        # Signals and slots
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'returnPressed()'), self.onSearchTextButtonClick)
        QtCore.QObject.connect(self.searchTextButton,
            QtCore.SIGNAL(u'pressed()'), self.onSearchTextButtonClick)
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'textChanged(const QString&)'),
            self.onSearchTextEditChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_load_list'), self.onSongListLoad)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.configUpdated)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_preview'), self.onPreviewClick)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_edit'), self.onRemoteEdit)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_edit_clear'), self.onRemoteEditClear)
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'cleared()'), self.onClearTextButtonClick)
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'searchTypeChanged(int)'),
            self.onSearchTextButtonClick)

    def configUpdated(self):
        self.searchAsYouType = QtCore.QSettings().value(
            self.settingsSection + u'/search as type',
            QtCore.QVariant(u'False')).toBool()
        self.updateServiceOnEdit = QtCore.QSettings().value(
            self.settingsSection + u'/update service on edit',
            QtCore.QVariant(u'False')).toBool()
        self.addSongFromService = QtCore.QSettings().value(
            self.settingsSection + u'/add song from service',
            QtCore.QVariant(u'True')).toBool()

    def retranslateUi(self):
        self.searchTextLabel.setText(u'%s:' % UiStrings.Search)
        self.searchTextButton.setText(UiStrings.Search)
        self.maintenanceAction.setText(SongStrings.SongMaintenance)
        self.maintenanceAction.setToolTip(translate('SongsPlugin.MediaItem',
            'Maintain the lists of authors, topics and books'))

    def initialise(self):
        self.searchTextEdit.setSearchTypes([
            (SongSearch.Entire, u':/songs/song_search_all.png',
                translate('SongsPlugin.MediaItem', 'Entire Song')),
            (SongSearch.Titles, u':/songs/song_search_title.png',
                translate('SongsPlugin.MediaItem', 'Titles')),
            (SongSearch.Lyrics, u':/songs/song_search_lyrics.png',
                translate('SongsPlugin.MediaItem', 'Lyrics')),
            (SongSearch.Authors, u':/songs/song_search_author.png',
                SongStrings.Authors),
            (SongSearch.Themes, u':/slides/slide_theme.png', UiStrings.Themes)
        ])
        self.searchTextEdit.setCurrentSearchType(QtCore.QSettings().value(
            u'%s/last search type' % self.settingsSection,
            QtCore.QVariant(SongSearch.Entire)).toInt()[0])
        self.configUpdated()

    def onSearchTextButtonClick(self):
        # Save the current search type to the configuration.
        QtCore.QSettings().setValue(u'%s/last search type' %
            self.settingsSection,
            QtCore.QVariant(self.searchTextEdit.currentSearchType()))
        # Reload the list considering the new search type.
        search_keywords = unicode(self.searchTextEdit.displayText())
        search_results = []
        search_type = self.searchTextEdit.currentSearchType()
        if search_type == SongSearch.Entire:
            log.debug(u'Entire Song Search')
            search_results = self.parent.manager.get_all_objects(Song,
                or_(Song.search_title.like(u'%' + self.whitespace.sub(u' ',
                search_keywords.lower()) + u'%'),
                Song.search_lyrics.like(u'%' + search_keywords.lower() + u'%'),
                Song.comments.like(u'%' + search_keywords.lower() + u'%')))
            self.displayResultsSong(search_results)
        elif search_type == SongSearch.Titles:
            log.debug(u'Titles Search')
            search_results = self.parent.manager.get_all_objects(Song,
                Song.search_title.like(u'%' + self.whitespace.sub(u' ',
                search_keywords.lower()) + u'%'))
            self.displayResultsSong(search_results)
        elif search_type == SongSearch.Lyrics:
            log.debug(u'Lyrics Search')
            search_results = self.parent.manager.get_all_objects(Song,
                Song.search_lyrics.like(u'%' + search_keywords.lower() + u'%'))
            self.displayResultsSong(search_results)
        elif search_type == SongSearch.Authors:
            log.debug(u'Authors Search')
            search_results = self.parent.manager.get_all_objects(Author,
                Author.display_name.like(u'%' + search_keywords + u'%'),
                Author.display_name.asc())
            self.displayResultsAuthor(search_results)
        elif search_type == SongSearch.Themes:
            log.debug(u'Theme Search')
            search_results = self.parent.manager.get_all_objects(Song,
                Song.theme_name == search_keywords)
            self.displayResultsSong(search_results)

    def onSongListLoad(self):
        """
        Handle the exit from the edit dialog and trigger remote updates
        of songs
        """
        log.debug(u'onSongListLoad - start')
        # Called to redisplay the song list screen edit from a search
        # or from the exit of the Song edit dialog. If remote editing is active
        # Trigger it and clean up so it will not update again.
        if self.remoteTriggered == u'L':
            self.onAddClick()
        if self.remoteTriggered == u'P':
            self.onPreviewClick()
        # Push edits to the service manager to update items
        if self.editItem and self.updateServiceOnEdit and \
            not self.remoteTriggered:
            item = self.buildServiceItem(self.editItem)
            self.parent.serviceManager.replaceServiceItem(item)
        self.onRemoteEditClear()
        self.onSearchTextButtonClick()
        log.debug(u'onSongListLoad - finished')

    def displayResultsSong(self, searchresults):
        log.debug(u'display results Song')
        self.listView.clear()
        searchresults.sort(cmp=self.collateSongTitles)
        for song in searchresults:
            author_list = [author.display_name for author in song.authors]
            song_title = unicode(song.title)
            song_detail = u'%s (%s)' % (song_title, u', '.join(author_list))
            song_name = QtGui.QListWidgetItem(song_detail)
            song_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(song.id))
            self.listView.addItem(song_name)

    def displayResultsAuthor(self, searchresults):
        log.debug(u'display results Author')
        self.listView.clear()
        for author in searchresults:
            for song in author.songs:
                song_detail = u'%s (%s)' % (author.display_name, song.title)
                song_name = QtGui.QListWidgetItem(song_detail)
                song_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(song.id))
                self.listView.addItem(song_name)

    def onClearTextButtonClick(self):
        """
        Clear the search text.
        """
        self.searchTextEdit.clear()
        self.onSearchTextButtonClick()

    def onSearchTextEditChanged(self, text):
        """
        If search as type enabled invoke the search on each key press.
        If the Lyrics are being searched do not start till 7 characters
        have been entered.
        """
        if self.searchAsYouType:
            search_length = 1
            if self.searchTextEdit.currentSearchType() == SongSearch.Entire:
                search_length = 4
            elif self.searchTextEdit.currentSearchType() == SongSearch.Lyrics:
                search_length = 3
            if len(text) > search_length:
                self.onSearchTextButtonClick()
            elif len(text) == 0:
                self.onClearTextButtonClick()

    def onImportClick(self):
        if not hasattr(self, u'import_wizard'):
            self.import_wizard = SongImportForm(self, self.parent)
        if self.import_wizard.exec_() == QtGui.QDialog.Accepted:
            Receiver.send_message(u'songs_load_list')

    def onExportClick(self):
        export_wizard = SongExportForm(self, self.parent)
        export_wizard.exec_()

    def onNewClick(self):
        log.debug(u'onNewClick')
        self.edit_song_form.newSong()
        self.edit_song_form.exec_()

    def onSongMaintenanceClick(self):
        self.song_maintenance_form.exec_()

    def onRemoteEditClear(self):
        log.debug(u'onRemoteEditClear')
        self.remoteTriggered = None
        self.remoteSong = -1

    def onRemoteEdit(self, message):
        """
        Called by ServiceManager or SlideController by event passing
        the Song Id in the payload along with an indicator to say which
        type of display is required.
        """
        log.debug(u'onRemoteEdit %s' % message)
        remote_type, song_id = message.split(u':')
        song_id = int(song_id)
        valid = self.parent.manager.get_object(Song, song_id)
        if valid:
            self.remoteSong = song_id
            self.remoteTriggered = remote_type
            self.edit_song_form.loadSong(song_id, (remote_type == u'P'))
            self.edit_song_form.exec_()

    def onEditClick(self):
        """
        Edit a song
        """
        log.debug(u'onEditClick')
        if check_item_selected(self.listView, UiStrings.SelectEdit):
            self.editItem = self.listView.currentItem()
            item_id = (self.editItem.data(QtCore.Qt.UserRole)).toInt()[0]
            self.edit_song_form.loadSong(item_id, False)
            self.edit_song_form.exec_()
        self.editItem = None

    def onDeleteClick(self):
        """
        Remove a song from the list and database
        """
        if check_item_selected(self.listView, UiStrings.SelectDelete):
            items = self.listView.selectedIndexes()
            if QtGui.QMessageBox.question(self,
                translate('SongsPlugin.MediaItem', 'Delete Song(s)?'),
                translate('SongsPlugin.MediaItem',
                'Are you sure you want to delete the %n selected song(s)?', '',
                QtCore.QCoreApplication.CodecForTr, len(items)),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok |
                QtGui.QMessageBox.Cancel),
                QtGui.QMessageBox.Ok) == QtGui.QMessageBox.Cancel:
                return
            for item in items:
                item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
                self.parent.manager.delete_object(Song, item_id)
            self.onSearchTextButtonClick()

    def generateSlideData(self, service_item, item=None, xmlVersion=False):
        log.debug(u'generateSlideData (%s:%s)' % (service_item, item))
        item_id = self._getIdOfItemToGenerate(item, self.remoteSong)
        service_item.add_capability(ItemCapabilities.AllowsEdit)
        service_item.add_capability(ItemCapabilities.AllowsPreview)
        service_item.add_capability(ItemCapabilities.AllowsLoop)
        service_item.add_capability(ItemCapabilities.OnLoadUpdate)
        service_item.add_capability(ItemCapabilities.AddIfNewItem)
        song = self.parent.manager.get_object(Song, item_id)
        service_item.theme = song.theme_name
        service_item.edit_id = item_id
        if song.lyrics.startswith(u'<?xml version='):
            verseList = SongXML().get_verses(song.lyrics)
            # no verse list or only 1 space (in error)
            verse_tags_translated = False
            if VerseType.from_translated_string(unicode(
                verseList[0][0][u'type'])) is not None:
                verse_tags_translated = True
            if not song.verse_order.strip():
                for verse in verseList:
                    # We cannot use from_loose_input() here, because database
                    # is supposed to contain English lowercase singlechar tags.
                    verse_tag = verse[0][u'type']
                    verse_index = None
                    if len(verse_tag) > 1:
                        verse_index = \
                            VerseType.from_translated_string(verse_tag)
                        if verse_index is None:
                            verse_index = VerseType.from_string(verse_tag)
                    if verse_index is None:
                        verse_index = VerseType.from_tag(verse_tag)
                    verse_tag = VerseType.TranslatedTags[verse_index].upper()
                    verse_def = u'%s%s' % (verse_tag, verse[0][u'label'])
                    service_item.add_from_text(
                        verse[1][:30], unicode(verse[1]), verse_def)
            else:
                # Loop through the verse list and expand the song accordingly.
                for order in song.verse_order.lower().split():
                    if len(order) == 0:
                        break
                    for verse in verseList:
                        if verse[0][u'type'][0].lower() == order[0] and \
                            (verse[0][u'label'].lower() == order[1:] or \
                            not order[1:]):
                            if verse_tags_translated:
                                verse_index = VerseType.from_translated_tag(
                                    verse[0][u'type'])
                            else:
                                verse_index = VerseType.from_tag(
                                    verse[0][u'type'])
                            if verse_index is None:
                                verse_index = VerseType.Other
                            verse_tag = VerseType.TranslatedTags[verse_index]
                            verse_def = u'%s%s' % (verse_tag,
                                verse[0][u'label'])
                            service_item.add_from_text(
                                verse[1][:30], verse[1], verse_def)
        else:
            verses = song.lyrics.split(u'\n\n')
            for slide in verses:
                service_item.add_from_text(slide[:30], unicode(slide))
        service_item.title = song.title
        author_list = [unicode(author.display_name) for author in song.authors]
        service_item.raw_footer.append(song.title)
        service_item.raw_footer.append(u', '.join(author_list))
        service_item.raw_footer.append(song.copyright)
        if QtCore.QSettings().value(u'general/ccli number',
            QtCore.QVariant(u'')).toString():
            service_item.raw_footer.append(unicode(
                translate('SongsPlugin.MediaItem', 'CCLI License: ') +
                QtCore.QSettings().value(u'general/ccli number',
                QtCore.QVariant(u'')).toString()))
        service_item.audit = [
            song.title, author_list, song.copyright, unicode(song.ccli_number)
        ]
        service_item.data_string = {u'title': song.search_title,
            u'authors': u', '.join(author_list)}
        service_item.xml_version = self.openLyrics.song_to_xml(song)
        return True

    def serviceLoad(self, item):
        """
        Triggered by a song being loaded by the service manager.
        """
        log.debug(u'serviceLoad')
        if self.plugin.status != PluginStatus.Active or not item.data_string:
            return
        if item.data_string[u'title'].find(u'@') == -1:
            # This file seems to be an old one (prior to 1.9.5), which means,
            # that the search title (data_string[u'title']) is probably wrong.
            # We add "@" to search title and hope that we do not add any
            # duplicate. This should work for songs without alternate title.
            search_results = self.parent.manager.get_all_objects(Song,
                Song.search_title == (re.compile(r'\W+', re.UNICODE).sub(u' ',
                item.data_string[u'title'].strip()) + u'@').strip().lower(),
                Song.search_title.asc())
        else:
            search_results = self.parent.manager.get_all_objects(Song,
                Song.search_title == item.data_string[u'title'],
                Song.search_title.asc())
        author_list = item.data_string[u'authors'].split(u', ')
        editId = 0
        add_song = True
        if search_results:
            for song in search_results:
                same_authors = True
                # If the author counts are different, we do not have to do any
                # further checking.
                if len(song.authors) == len(author_list):
                    for author in song.authors:
                        if author.display_name not in author_list:
                            same_authors = False
                else:
                    same_authors = False
                # All authors are the same, so we can stop here and the song
                # does not have to be saved.
                if same_authors:
                    add_song = False
                    editId = song.id
                    break
        if add_song and self.addSongFromService:
            editId = self.openLyrics.xml_to_song(item.xml_version)
            self.onSearchTextButtonClick()
        # Update service with correct song id.
        if editId:
            Receiver.send_message(u'service_item_update',
                u'%s:%s' % (editId, item._uuid))

    def collateSongTitles(self, song_1, song_2):
        """
        Locale aware collation of song titles
        """
        return locale.strcoll(unicode(song_1.title.lower()),
             unicode(song_2.title.lower()))
