# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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
import locale
import re

from PyQt4 import QtCore, QtGui
from sqlalchemy.sql import or_

from openlp.core.lib import MediaManagerItem, Receiver, ItemCapabilities, \
    translate, check_item_selected, PluginStatus
from openlp.core.lib.ui import UiStrings
from openlp.plugins.songs.forms import EditSongForm, SongMaintenanceForm, \
    SongImportForm
from openlp.plugins.songs.lib import OpenLyrics, SongXML
from openlp.plugins.songs.lib.db import Author, Song
from openlp.core.lib.searchedit import SearchEdit

log = logging.getLogger(__name__)

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
        self.searchTextLabel.setText(
            translate('SongsPlugin.MediaItem', 'Search:'))
        self.searchTextButton.setText(
            translate('SongsPlugin.MediaItem', 'Search'))
        self.maintenanceAction.setText(
            translate('SongsPlugin.MediaItem', 'Song Maintenance'))
        self.maintenanceAction.setToolTip(translate('SongsPlugin.MediaItem',
            'Maintain the lists of authors, topics and books'))

    def initialise(self):
        self.searchTextEdit.setSearchTypes([
            (1, u':/songs/song_search_all.png',
                translate('SongsPlugin.MediaItem', 'Entire Song')),
            (2, u':/songs/song_search_title.png',
                translate('SongsPlugin.MediaItem', 'Titles')),
            (3, u':/songs/song_search_lyrics.png',
                translate('SongsPlugin.MediaItem', 'Lyrics')),
            (4, u':/songs/song_search_author.png', UiStrings.Authors),
            (5, u':/slides/slide_theme.png', UiStrings.Themes)
        ])
        self.configUpdated()

    def onSearchTextButtonClick(self):
        search_keywords = unicode(self.searchTextEdit.displayText())
        search_results = []
        # search_type = self.searchTypeComboBox.currentIndex()
        search_type = self.searchTextEdit.currentSearchType()
        if search_type == 1:
            log.debug(u'Entire Song Search')
            search_results = self.parent.manager.get_all_objects(Song,
                or_(Song.search_title.like(u'%' + self.whitespace.sub(u' ',
                search_keywords.lower()) + u'%'),
                Song.search_lyrics.like(u'%' + search_keywords.lower() + \
                u'%')), Song.search_title.asc())
            self.displayResultsSong(search_results)
        if search_type == 2:
            log.debug(u'Titles Search')
            search_results = self.parent.manager.get_all_objects(Song,
                Song.search_title.like(u'%' + self.whitespace.sub(u' ',
                search_keywords.lower()) + u'%'), Song.search_title.asc())
            self.displayResultsSong(search_results)
        elif search_type == 3:
            log.debug(u'Lyrics Search')
            search_results = self.parent.manager.get_all_objects(Song,
                Song.search_lyrics.like(u'%' + search_keywords.lower() + u'%'),
                Song.search_lyrics.asc())
            self.displayResultsSong(search_results)
        elif search_type == 4:
            log.debug(u'Authors Search')
            search_results = self.parent.manager.get_all_objects(Author,
                Author.display_name.like(u'%' + search_keywords + u'%'),
                Author.display_name.asc())
            self.displayResultsAuthor(search_results)
        elif search_type == 5:
            log.debug(u'Theme Search')
            search_results = self.parent.manager.get_all_objects(Song,
                Song.theme_name == search_keywords, Song.search_lyrics.asc())
            self.displayResultsSong(search_results)

    def onSongListLoad(self):
        """
        Handle the exit from the edit dialog and trigger remote updates
        of songs
        """
        log.debug(u'onSongListLoad')
        # Called to redisplay the song list screen edit from a search
        # or from the exit of the Song edit dialog.  If remote editing is active
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

    def displayResultsSong(self, searchresults):
        log.debug(u'display results Song')
        self.listView.clear()
        searchresults.sort(cmp=self.collateSongTitles)
        for song in searchresults:
            author_list = u''
            for author in song.authors:
                if author_list != u'':
                    author_list = author_list + u', '
                author_list = author_list + author.display_name
            song_title = unicode(song.title)
            song_detail = u'%s (%s)' % (song_title, author_list)
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
            if self.searchTextEdit.currentSearchType() == 1:
                search_length = 3
            elif self.searchTextEdit.currentSearchType() == 3:
                search_length = 7
            if len(text) > search_length:
                self.onSearchTextButtonClick()

    def onImportClick(self):
        if not hasattr(self, u'import_wizard'):
            self.import_wizard = SongImportForm(self, self.parent)
        if self.import_wizard.exec_() == QtGui.QDialog.Accepted:
            Receiver.send_message(u'songs_load_list')

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

    def onRemoteEdit(self, songid):
        """
        Called by ServiceManager or SlideController by event passing
        the Song Id in the payload along with an indicator to say which
        type of display is required.
        """
        log.debug(u'onRemoteEdit %s' % songid)
        fields = songid.split(u':')
        valid = self.parent.manager.get_object(Song, fields[1])
        if valid:
            self.remoteSong = fields[1]
            self.remoteTriggered = fields[0]
            self.edit_song_form.loadSong(fields[1], (fields[0] == u'P'))
            self.edit_song_form.exec_()

    def onEditClick(self):
        """
        Edit a song
        """
        log.debug(u'onEditClick')
        if check_item_selected(self.listView,
            translate('SongsPlugin.MediaItem',
            'You must select an item to edit.')):
            self.editItem = self.listView.currentItem()
            item_id = (self.editItem.data(QtCore.Qt.UserRole)).toInt()[0]
            self.edit_song_form.loadSong(item_id, False)
            self.edit_song_form.exec_()

    def onDeleteClick(self):
        """
        Remove a song from the list and database
        """
        if check_item_selected(self.listView,
            translate('SongsPlugin.MediaItem',
            'You must select an item to delete.')):
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
        raw_footer = []
        author_list = u''
        author_audit = []
        ccli = u''
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
            if not song.verse_order or not song.verse_order.strip():
                for verse in verseList:
                    verseTag = u'%s:%s' % (
                        verse[0][u'type'], verse[0][u'label'])
                    service_item.add_from_text(
                        verse[1][:30], unicode(verse[1]), verseTag)
            else:
                # Loop through the verse list and expand the song accordingly.
                for order in song.verse_order.upper().split():
                    if len(order) == 0:
                        break
                    for verse in verseList:
                        if verse[0][u'type'][0] == order[0] and \
                            (verse[0][u'label'] == order[1:] or not order[1:]):
                            verseTag = u'%s:%s' % \
                                (verse[0][u'type'], verse[0][u'label'])
                            service_item.add_from_text(
                                verse[1][:30], verse[1], verseTag)
        else:
            verses = song.lyrics.split(u'\n\n')
            for slide in verses:
                service_item.add_from_text(slide[:30], unicode(slide))
        service_item.title = song.title
        for author in song.authors:
            if len(author_list) > 1:
                author_list = author_list + u', '
            author_list = author_list + unicode(author.display_name)
            author_audit.append(unicode(author.display_name))
        raw_footer.append(song.title)
        raw_footer.append(author_list)
        raw_footer.append(song.copyright)
        if QtCore.QSettings().value(u'general/ccli number',
            QtCore.QVariant(u'')).toString():
            raw_footer.append(unicode(
                translate('SongsPlugin.MediaItem', 'CCLI License: ') +
                QtCore.QSettings().value(u'general/ccli number',
                QtCore.QVariant(u'')).toString()))
        service_item.raw_footer = raw_footer
        service_item.audit = [
            song.title, author_audit, song.copyright, unicode(song.ccli_number)
        ]
        service_item.data_string = {u'title': song.search_title,
            u'authors': author_list}
        service_item.xml_version = self.openLyrics.song_to_xml(song)
        return True

    def serviceLoad(self, item):
        """
        Triggered by a song being loaded by the service item
        """
        log.debug(u'serviceLoad')
        if self.plugin.status != PluginStatus.Active or not item.data_string:
            return
        search_results = self.parent.manager.get_all_objects(Song,
            Song.search_title == re.compile(r'\W+', re.UNICODE).sub(u' ',
            item.data_string[u'title'].split(u'@')[0].lower()).strip(),
            Song.search_title.asc())
        author_list = item.data_string[u'authors'].split(u', ')
        # The service item always has an author (at least it has u'' as
        # author). However, songs saved in the database do not have to have
        # an author.
        if u'' in author_list:
            author_list.remove(u'')
        editId = 0
        add_song = True
        if search_results:
            for song in search_results:
                same_authors = True
                # If the author counts are different, we do not have to do any
                # further checking. This is also important when a song does not
                # have any author (because we can not loop over an empty list).
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
        if add_song:
            if self.addSongFromService:
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
        return locale.strcoll(unicode(song_1.title), unicode(song_2.title))
