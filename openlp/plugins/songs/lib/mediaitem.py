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
import re
import os
import shutil

from PyQt4 import QtCore, QtGui
from sqlalchemy.sql import or_

from openlp.core.lib import MediaManagerItem, Receiver, ItemCapabilities, PluginStatus, ServiceItemContext, Settings, \
    UiStrings, translate, check_item_selected, create_separated_list, check_directory_exists
from openlp.core.lib.ui import create_widget_action
from openlp.core.utils import AppLocation
from openlp.plugins.songs.forms import EditSongForm, SongMaintenanceForm, SongImportForm, SongExportForm
from openlp.plugins.songs.lib import OpenLyrics, SongXML, VerseType, clean_string, natcmp
from openlp.plugins.songs.lib.db import Author, Song, Book, MediaFile
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
    Books = 5
    Themes = 6


class SongMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Songs.
    """
    log.info(u'Song Media Item loaded')

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'songs/song'
        MediaManagerItem.__init__(self, parent, plugin, icon)
        self.editSongForm = EditSongForm(self, self.main_window, self.plugin.manager)
        self.openLyrics = OpenLyrics(self.plugin.manager)
        self.singleServiceItem = False
        self.songMaintenanceForm = SongMaintenanceForm(self.plugin.manager, self)
        # Holds information about whether the edit is remotely triggered and
        # which Song is required.
        self.remoteSong = -1
        self.editItem = None
        self.quickPreviewAllowed = True
        self.hasSearch = True

    def _updateBackgroundAudio(self, song, item):
        song.media_files = []
        for i, bga in enumerate(item.background_audio):
            dest_file = os.path.join(
                AppLocation.get_section_data_path(self.plugin.name), u'audio', str(song.id), os.path.split(bga)[1])
            check_directory_exists(os.path.split(dest_file)[0])
            shutil.copyfile(os.path.join(AppLocation.get_section_data_path(u'servicemanager'), bga),
                dest_file)
            song.media_files.append(MediaFile.populate(
                weight=i, file_name=dest_file))
        self.plugin.manager.save_object(song, True)

    def addEndHeaderBar(self):
        self.toolbar.addSeparator()
        ## Song Maintenance Button ##
        self.maintenanceAction = self.toolbar.addToolbarAction('maintenanceAction',
            icon=':/songs/song_maintenance.png',
            triggers=self.onSongMaintenanceClick)
        self.addSearchToToolBar()
        # Signals and slots
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'songs_load_list'), self.onSongListLoad)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_updated'), self.configUpdated)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'songs_preview'), self.onPreviewClick)
        QtCore.QObject.connect(self.searchTextEdit, QtCore.SIGNAL(u'cleared()'), self.onClearTextButtonClick)
        QtCore.QObject.connect(self.searchTextEdit, QtCore.SIGNAL(u'searchTypeChanged(int)'),
            self.onSearchTextButtonClicked)

    def addCustomContextActions(self):
        create_widget_action(self.listView, separator=True)
        create_widget_action(self.listView,
            text=translate('OpenLP.MediaManagerItem', '&Clone'), icon=u':/general/general_clone.png',
            triggers=self.onCloneClick)

    def onFocus(self):
        self.searchTextEdit.setFocus()

    def configUpdated(self):
        self.searchAsYouType = Settings().value(self.settingsSection + u'/search as type')
        self.updateServiceOnEdit = Settings().value(self.settingsSection + u'/update service on edit')
        self.addSongFromService = Settings().value(self.settingsSection + u'/add song from service',)

    def retranslateUi(self):
        self.searchTextLabel.setText(u'%s:' % UiStrings().Search)
        self.searchTextButton.setText(UiStrings().Search)
        self.maintenanceAction.setText(SongStrings.SongMaintenance)
        self.maintenanceAction.setToolTip(translate('SongsPlugin.MediaItem',
            'Maintain the lists of authors, topics and books.'))

    def initialise(self):
        self.searchTextEdit.setSearchTypes([
            (SongSearch.Entire, u':/songs/song_search_all.png',
                translate('SongsPlugin.MediaItem', 'Entire Song'),
                translate('SongsPlugin.MediaItem', 'Search Entire Song...')),
            (SongSearch.Titles, u':/songs/song_search_title.png',
                translate('SongsPlugin.MediaItem', 'Titles'),
                translate('SongsPlugin.MediaItem', 'Search Titles...')),
            (SongSearch.Lyrics, u':/songs/song_search_lyrics.png',
                translate('SongsPlugin.MediaItem', 'Lyrics'),
                translate('SongsPlugin.MediaItem', 'Search Lyrics...')),
            (SongSearch.Authors, u':/songs/song_search_author.png', SongStrings.Authors,
                translate('SongsPlugin.MediaItem', 'Search Authors...')),
            (SongSearch.Books, u':/songs/song_book_edit.png', SongStrings.SongBooks,
                translate('SongsPlugin.MediaItem', 'Search Song Books...')),
            (SongSearch.Themes, u':/slides/slide_theme.png',
            UiStrings().Themes, UiStrings().SearchThemes)
        ])
        self.searchTextEdit.setCurrentSearchType(Settings().value(u'%s/last search type' % self.settingsSection))
        self.configUpdated()

    def onSearchTextButtonClicked(self):
        # Save the current search type to the configuration.
        Settings().setValue(u'%s/last search type' % self.settingsSection, self.searchTextEdit.currentSearchType())
        # Reload the list considering the new search type.
        search_keywords = unicode(self.searchTextEdit.displayText())
        search_results = []
        search_type = self.searchTextEdit.currentSearchType()
        if search_type == SongSearch.Entire:
            log.debug(u'Entire Song Search')
            search_results = self.searchEntire(search_keywords)
            self.displayResultsSong(search_results)
        elif search_type == SongSearch.Titles:
            log.debug(u'Titles Search')
            search_results = self.plugin.manager.get_all_objects(Song,
                Song.search_title.like(u'%' + clean_string(search_keywords) + u'%'))
            self.displayResultsSong(search_results)
        elif search_type == SongSearch.Lyrics:
            log.debug(u'Lyrics Search')
            search_results = self.plugin.manager.get_all_objects(Song,
                Song.search_lyrics.like(u'%' + clean_string(search_keywords) + u'%'))
            self.displayResultsSong(search_results)
        elif search_type == SongSearch.Authors:
            log.debug(u'Authors Search')
            search_results = self.plugin.manager.get_all_objects(Author,
                Author.display_name.like(u'%' + search_keywords + u'%'), Author.display_name.asc())
            self.displayResultsAuthor(search_results)
        elif search_type == SongSearch.Books:
            log.debug(u'Books Search')
            search_results = self.plugin.manager.get_all_objects(Book,
                Book.name.like(u'%' + search_keywords + u'%'), Book.name.asc())
            song_number = False
            if not search_results:
                search_keywords = search_keywords.rpartition(' ')
                search_results = self.plugin.manager.get_all_objects(Book,
                    Book.name.like(u'%' + search_keywords[0] + u'%'), Book.name.asc())
                song_number = re.sub(r'[^0-9]', u'', search_keywords[2])
            self.displayResultsBook(search_results, song_number)
        elif search_type == SongSearch.Themes:
            log.debug(u'Theme Search')
            search_results = self.plugin.manager.get_all_objects(Song,
                Song.theme_name.like(u'%' + search_keywords + u'%'))
            self.displayResultsSong(search_results)
        self.checkSearchResult()

    def searchEntire(self, search_keywords):
        return self.plugin.manager.get_all_objects(Song,
            or_(Song.search_title.like(u'%' + clean_string(search_keywords) + u'%'),
                Song.search_lyrics.like(u'%' + clean_string(search_keywords) + u'%'),
                Song.comments.like(u'%' + search_keywords.lower() + u'%')))

    def onSongListLoad(self):
        """
        Handle the exit from the edit dialog and trigger remote updates
        of songs
        """
        log.debug(u'onSongListLoad - start')
        # Called to redisplay the song list screen edit from a search
        # or from the exit of the Song edit dialog. If remote editing is active
        # Trigger it and clean up so it will not update again.
        # Push edits to the service manager to update items
        if self.editItem and self.updateServiceOnEdit and not self.remoteTriggered:
            item = self.buildServiceItem(self.editItem)
            self.service_manager.replace_service_item(item)
        self.onSearchTextButtonClicked()
        log.debug(u'onSongListLoad - finished')

    def displayResultsSong(self, searchresults):
        log.debug(u'display results Song')
        self.saveAutoSelectId()
        self.listView.clear()
        searchresults.sort(cmp=natcmp, key=lambda song: song.sort_key)
        for song in searchresults:
            # Do not display temporary songs
            if song.temporary:
                continue
            author_list = [author.display_name for author in song.authors]
            song_title = unicode(song.title)
            song_detail = u'%s (%s)' % (song_title, create_separated_list(author_list))
            song_name = QtGui.QListWidgetItem(song_detail)
            song_name.setData(QtCore.Qt.UserRole, song.id)
            self.listView.addItem(song_name)
            # Auto-select the item if name has been set
            if song.id == self.autoSelectId:
                self.listView.setCurrentItem(song_name)
        self.autoSelectId = -1

    def displayResultsAuthor(self, searchresults):
        log.debug(u'display results Author')
        self.listView.clear()
        for author in searchresults:
            for song in author.songs:
                # Do not display temporary songs
                if song.temporary:
                    continue
                song_detail = u'%s (%s)' % (author.display_name, song.title)
                song_name = QtGui.QListWidgetItem(song_detail)
                song_name.setData(QtCore.Qt.UserRole, song.id)
                self.listView.addItem(song_name)

    def displayResultsBook(self, searchresults, song_number=False):
        log.debug(u'display results Book')
        self.listView.clear()
        for book in searchresults:
            songs = sorted(book.songs, key=lambda song:
                int(re.match(r'[0-9]+', u'0' + song.song_number).group()))
            for song in songs:
                # Do not display temporary songs
                if song.temporary:
                    continue
                if song_number and not song_number in song.song_number:
                    continue
                song_detail = u'%s - %s (%s)' % (book.name, song.song_number, song.title)
                song_name = QtGui.QListWidgetItem(song_detail)
                song_name.setData(QtCore.Qt.UserRole, song.id)
                self.listView.addItem(song_name)

    def onClearTextButtonClick(self):
        """
        Clear the search text.
        """
        self.searchTextEdit.clear()
        self.onSearchTextButtonClicked()

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
                self.onSearchTextButtonClicked()
            elif not text:
                self.onClearTextButtonClick()

    def onImportClick(self):
        if not hasattr(self, u'importWizard'):
            self.importWizard = SongImportForm(self, self.plugin)
        self.importWizard.exec_()
        # Run song load as list may have been cancelled but some songs loaded
        Receiver.send_message(u'songs_load_list')

    def onExportClick(self):
        if not hasattr(self, u'exportWizard'):
            self.exportWizard = SongExportForm(self, self.plugin)
        self.exportWizard.exec_()

    def onNewClick(self):
        log.debug(u'onNewClick')
        self.editSongForm.newSong()
        self.editSongForm.exec_()
        self.onClearTextButtonClick()
        self.onSelectionChange()
        self.autoSelectId = -1

    def onSongMaintenanceClick(self):
        self.songMaintenanceForm.exec_()

    def onRemoteEdit(self, song_id, preview=False):
        """
        Called by ServiceManager or SlideController by event passing
        the Song Id in the payload along with an indicator to say which
        type of display is required.
        """
        log.debug(u'onRemoteEdit for song %s' % song_id)
        song_id = int(song_id)
        valid = self.plugin.manager.get_object(Song, song_id)
        if valid:
            self.editSongForm.loadSong(song_id, preview)
            if self.editSongForm.exec_() == QtGui.QDialog.Accepted:
                self.autoSelectId = -1
                self.onSongListLoad()
                self.remoteSong = song_id
                self.remoteTriggered = True
                item = self.buildServiceItem(remote=True)
                self.remoteSong = -1
                self.remoteTriggered = None
                if item:
                    return item
        return None

    def onEditClick(self):
        """
        Edit a song
        """
        log.debug(u'onEditClick')
        if check_item_selected(self.listView, UiStrings().SelectEdit):
            self.editItem = self.listView.currentItem()
            item_id = self.editItem.data(QtCore.Qt.UserRole)
            self.editSongForm.loadSong(item_id, False)
            self.editSongForm.exec_()
            self.autoSelectId = -1
            self.onSongListLoad()
        self.editItem = None

    def onDeleteClick(self):
        """
        Remove a song from the list and database
        """
        if check_item_selected(self.listView, UiStrings().SelectDelete):
            items = self.listView.selectedIndexes()
            if QtGui.QMessageBox.question(self,
                UiStrings().ConfirmDelete,
                translate('SongsPlugin.MediaItem', 'Are you sure you want to delete the %n selected song(s)?', '',
                QtCore.QCoreApplication.CodecForTr, len(items)),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No),
                QtGui.QMessageBox.Yes) == QtGui.QMessageBox.No:
                return
            self.application.set_busy_cursor()
            self.main_window.displayProgressBar(len(items))
            for item in items:
                item_id = item.data(QtCore.Qt.UserRole)
                media_files = self.plugin.manager.get_all_objects(MediaFile, MediaFile.song_id == item_id)
                for media_file in media_files:
                    try:
                        os.remove(media_file.file_name)
                    except:
                        log.exception('Could not remove file: %s', media_file.file_name)
                try:
                    save_path = os.path.join(AppLocation.get_section_data_path(self.plugin.name), 'audio', str(item_id))
                    if os.path.exists(save_path):
                        os.rmdir(save_path)
                except OSError:
                    log.exception(u'Could not remove directory: %s', save_path)
                self.plugin.manager.delete_object(Song, item_id)
                self.main_window.incrementProgressBar()
            self.main_window.finishedProgressBar()
            self.application.set_normal_cursor()
            self.onSearchTextButtonClicked()

    def onCloneClick(self):
        """
        Clone a Song
        """
        log.debug(u'onCloneClick')
        if check_item_selected(self.listView, UiStrings().SelectEdit):
            self.editItem = self.listView.currentItem()
            item_id = self.editItem.data(QtCore.Qt.UserRole)
            old_song = self.plugin.manager.get_object(Song, item_id)
            song_xml = self.openLyrics.song_to_xml(old_song)
            new_song = self.openLyrics.xml_to_song(song_xml)
            new_song.title = u'%s <%s>' % (new_song.title,
                translate('SongsPlugin.MediaItem', 'copy', 'For song cloning'))
            self.plugin.manager.save_object(new_song)
        self.onSongListLoad()

    def generateSlideData(self, service_item, item=None, xmlVersion=False,
                remote=False, context=ServiceItemContext.Service):
        log.debug(u'generateSlideData: %s, %s, %s' % (service_item, item, self.remoteSong))
        item_id = self._getIdOfItemToGenerate(item, self.remoteSong)
        service_item.add_capability(ItemCapabilities.CanEdit)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.OnLoadUpdate)
        service_item.add_capability(ItemCapabilities.AddIfNewItem)
        service_item.add_capability(ItemCapabilities.CanSoftBreak)
        song = self.plugin.manager.get_object(Song, item_id)
        service_item.theme = song.theme_name
        service_item.edit_id = item_id
        if song.lyrics.startswith(u'<?xml version='):
            verse_list = SongXML().get_verses(song.lyrics)
            # no verse list or only 1 space (in error)
            verse_tags_translated = False
            if VerseType.from_translated_string(unicode(verse_list[0][0][u'type'])) is not None:
                verse_tags_translated = True
            if not song.verse_order.strip():
                for verse in verse_list:
                    # We cannot use from_loose_input() here, because database
                    # is supposed to contain English lowercase singlechar tags.
                    verse_tag = verse[0][u'type']
                    verse_index = None
                    if len(verse_tag) > 1:
                        verse_index = VerseType.from_translated_string(verse_tag)
                        if verse_index is None:
                            verse_index = VerseType.from_string(verse_tag, None)
                    if verse_index is None:
                        verse_index = VerseType.from_tag(verse_tag)
                    verse_tag = VerseType.TranslatedTags[verse_index].upper()
                    verse_def = u'%s%s' % (verse_tag, verse[0][u'label'])
                    service_item.add_from_text(unicode(verse[1]), verse_def)
            else:
                # Loop through the verse list and expand the song accordingly.
                for order in song.verse_order.lower().split():
                    if not order:
                        break
                    for verse in verse_list:
                        if verse[0][u'type'][0].lower() == order[0] and (verse[0][u'label'].lower() == order[1:] or \
                                not order[1:]):
                            if verse_tags_translated:
                                verse_index = VerseType.from_translated_tag(verse[0][u'type'])
                            else:
                                verse_index = VerseType.from_tag(verse[0][u'type'])
                            verse_tag = VerseType.TranslatedTags[verse_index]
                            verse_def = u'%s%s' % (verse_tag, verse[0][u'label'])
                            service_item.add_from_text(verse[1], verse_def)
        else:
            verses = song.lyrics.split(u'\n\n')
            for slide in verses:
                service_item.add_from_text(unicode(slide))
        service_item.title = song.title
        author_list = [unicode(author.display_name) for author in song.authors]
        service_item.raw_footer.append(song.title)
        service_item.raw_footer.append(create_separated_list(author_list))
        service_item.raw_footer.append(song.copyright)
        if Settings().value(u'general/ccli number'):
            service_item.raw_footer.append(translate('SongsPlugin.MediaItem', 'CCLI License: ') +
                Settings().value(u'general/ccli number'))
        service_item.audit = [
            song.title, author_list, song.copyright, unicode(song.ccli_number)
        ]
        service_item.data_string = {u'title': song.search_title, u'authors': u', '.join(author_list)}
        service_item.xml_version = self.openLyrics.song_to_xml(song)
        # Add the audio file to the service item.
        if song.media_files:
            service_item.add_capability(ItemCapabilities.HasBackgroundAudio)
            service_item.background_audio = [m.file_name for m in song.media_files]
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
            search_results = self.plugin.manager.get_all_objects(Song,
                Song.search_title == (re.compile(r'\W+', re.UNICODE).sub(u' ',
                item.data_string[u'title'].strip()) + u'@').strip().lower(), Song.search_title.asc())
        else:
            search_results = self.plugin.manager.get_all_objects(Song,
                Song.search_title == item.data_string[u'title'], Song.search_title.asc())
        editId = 0
        add_song = True
        temporary = False
        if search_results:
            for song in search_results:
                author_list = item.data_string[u'authors']
                same_authors = True
                for author in song.authors:
                    if author.display_name in author_list:
                        author_list = author_list.replace(author.display_name, u'', 1)
                    else:
                        same_authors = False
                        break
                if same_authors and author_list.strip(u', ') == u'':
                    add_song = False
                    editId = song.id
                    break
                # If there's any backing tracks, copy them over.
                if item.background_audio:
                    self._updateBackgroundAudio(song, item)
        if add_song and self.addSongFromService:
            song = self.openLyrics.xml_to_song(item.xml_version)
            # If there's any backing tracks, copy them over.
            if item.background_audio:
                self._updateBackgroundAudio(song, item)
            editId = song.id
            self.onSearchTextButtonClicked()
        elif add_song and not self.addSongFromService:
            # Make sure we temporary import formatting tags.
            song = self.openLyrics.xml_to_song(item.xml_version, True)
            # If there's any backing tracks, copy them over.
            if item.background_audio:
                self._updateBackgroundAudio(song, item)
            editId = song.id
            temporary = True
        # Update service with correct song id.
        if editId:
            self.service_manager.service_item_update(editId, item.unique_identifier, temporary)

    def search(self, string, showError):
        """
        Search for some songs
        """
        search_results = self.searchEntire(string)
        return [[song.id, song.title] for song in search_results]
