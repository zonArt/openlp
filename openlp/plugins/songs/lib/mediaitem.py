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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem, SongXMLParser, \
    BaseListWithDnD, Receiver, ItemCapabilities, translate
from openlp.plugins.songs.forms import EditSongForm, SongMaintenanceForm, \
    ImportWizardForm
from openlp.plugins.songs.lib.db import Song

log = logging.getLogger(__name__)

class SongListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Songs'
        BaseListWithDnD.__init__(self, parent)

class SongMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Songs.
    """
    log.info(u'Song Media Item loaded')

    def __init__(self, parent, icon, title):
        self.PluginNameShort = u'Song'
        self.IconPath = u'songs/song'
        self.ListViewWithDnD_class = SongListView
        MediaManagerItem.__init__(self, parent, icon, title)
        self.edit_song_form = EditSongForm(self, self.parent.manager)
        self.singleServiceItem = False
        #self.edit_song_form = EditSongForm(self.parent.manager, self)
        self.song_maintenance_form = SongMaintenanceForm(
            self.parent.manager, self)
        # Holds information about whether the edit is remotly triggered and
        # which Song is required.
        self.remoteSong = -1

    def initPluginNameVisible(self):
        self.PluginNameVisible = translate(u'SongsPlugin.MediaItem', u'Song')

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)

    def addEndHeaderBar(self):
        self.addToolbarSeparator()
        ## Song Maintenance Button ##
        self.addToolbarButton(
            translate(u'SongsPlugin.MediaItem', u'Song Maintenance'),
            translate(u'SongsPlugin.MediaItem',
            u'Maintain the lists of authors, topics and books'),
            ':/songs/song_maintenance.png', self.onSongMaintenanceClick)
        self.PageLayout.setSpacing(4)
        self.SearchLayout = QtGui.QFormLayout()
        self.SearchLayout.setMargin(0)
        self.SearchLayout.setSpacing(4)
        self.SearchLayout.setObjectName(u'SearchLayout')
        self.SearchTextLabel = QtGui.QLabel(self)
        self.SearchTextLabel.setAlignment(
            QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.SearchTextLabel.setObjectName(u'SearchTextLabel')
        self.SearchLayout.setWidget(
            0, QtGui.QFormLayout.LabelRole, self.SearchTextLabel)
        self.SearchTextEdit = QtGui.QLineEdit(self)
        self.SearchTextEdit.setObjectName(u'SearchTextEdit')
        self.SearchLayout.setWidget(
            0, QtGui.QFormLayout.FieldRole, self.SearchTextEdit)
        self.SearchTypeLabel = QtGui.QLabel(self)
        self.SearchTypeLabel.setAlignment(
            QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.SearchTypeLabel.setObjectName(u'SearchTypeLabel')
        self.SearchLayout.setWidget(
            1, QtGui.QFormLayout.LabelRole, self.SearchTypeLabel)
        self.SearchTypeComboBox = QtGui.QComboBox(self)
        self.SearchTypeComboBox.setObjectName(u'SearchTypeComboBox')
        self.SearchLayout.setWidget(
            1, QtGui.QFormLayout.FieldRole, self.SearchTypeComboBox)
        self.PageLayout.addLayout(self.SearchLayout)
        self.SearchButtonLayout = QtGui.QHBoxLayout()
        self.SearchButtonLayout.setMargin(0)
        self.SearchButtonLayout.setSpacing(4)
        self.SearchButtonLayout.setObjectName(u'SearchButtonLayout')
        self.SearchButtonSpacer = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.SearchButtonLayout.addItem(self.SearchButtonSpacer)
        self.SearchTextButton = QtGui.QPushButton(self)
        self.SearchTextButton.setObjectName(u'SearchTextButton')
        self.SearchButtonLayout.addWidget(self.SearchTextButton)
        self.ClearTextButton = QtGui.QPushButton(self)
        self.ClearTextButton.setObjectName(u'ClearTextButton')
        self.SearchButtonLayout.addWidget(self.ClearTextButton)
        self.PageLayout.addLayout(self.SearchButtonLayout)
        # Signals and slots
        QtCore.QObject.connect(self.SearchTextEdit,
            QtCore.SIGNAL(u'returnPressed()'), self.onSearchTextButtonClick)
        QtCore.QObject.connect(self.SearchTextButton,
            QtCore.SIGNAL(u'pressed()'), self.onSearchTextButtonClick)
        QtCore.QObject.connect(self.ClearTextButton,
            QtCore.SIGNAL(u'pressed()'), self.onClearTextButtonClick)
        QtCore.QObject.connect(self.SearchTextEdit,
            QtCore.SIGNAL(u'textChanged(const QString&)'),
            self.onSearchTextEditChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_load_list'), self.onSearchTextButtonClick)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.configUpdated)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_preview'), self.onPreviewClick)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_edit'), self.onRemoteEdit)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songs_edit_clear'), self.onRemoteEditClear)

    def configUpdated(self):
        self.searchAsYouType = QtCore.QSettings().value(
            self.settingsSection + u'/search as type',
            QtCore.QVariant(u'False')).toBool()

    def retranslateUi(self):
        self.SearchTextLabel.setText(
            translate(u'SongsPlugin.MediaItem', u'Search:'))
        self.SearchTypeLabel.setText(
            translate(u'SongsPlugin.MediaItem', u'Type:'))
        self.ClearTextButton.setText(
            translate(u'SongsPlugin.MediaItem', u'Clear'))
        self.SearchTextButton.setText(
            translate(u'SongsPlugin.MediaItem', u'Search'))

    def initialise(self):
        self.SearchTypeComboBox.addItem(
            translate(u'SongsPlugin.MediaItem', u'Titles'))
        self.SearchTypeComboBox.addItem(
            translate(u'SongsPlugin.MediaItem', u'Lyrics'))
        self.SearchTypeComboBox.addItem(
            translate(u'SongsPlugin.MediaItem', u'Authors'))
        self.configUpdated()

    def onSearchTextButtonClick(self):
        search_keywords = unicode(self.SearchTextEdit.displayText())
        search_results = []
        search_type = self.SearchTypeComboBox.currentIndex()
        if search_type == 0:
            log.debug(u'Titles Search')
            search_results = self.parent.manager.search_song_title(
                search_keywords)
            self.displayResultsSong(search_results)
        elif search_type == 1:
            log.debug(u'Lyrics Search')
            search_results = self.parent.manager.search_song_lyrics(
                search_keywords)
            self.displayResultsSong(search_results)
        elif search_type == 2:
            log.debug(u'Authors Search')
            search_results = self.parent.manager.get_song_from_author(
                search_keywords)
            self.displayResultsAuthor(search_results)
        #Called to redisplay the song list screen edith from a search
        #or from the exit of the Song edit dialog.  If remote editing is active
        #Trigger it and clean up so it will not update again.
        if self.remoteTriggered == u'L':
            self.onAddClick()
        if self.remoteTriggered == u'P':
            self.onPreviewClick()
        self.onRemoteEditClear()

    def displayResultsSong(self, searchresults):
        log.debug(u'display results Song')
        self.ListView.clear()
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
            self.ListView.addItem(song_name)

    def displayResultsAuthor(self, searchresults):
        log.debug(u'display results Author')
        self.ListView.clear()
        for author in searchresults:
            for song in author.songs:
                song_detail = unicode(
                    translate(u'SongsPlugin.MediaItem', u'%s (%s)')) % \
                    (author.display_name, song.title)
                song_name = QtGui.QListWidgetItem(song_detail)
                song_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(song.id))
                self.ListView.addItem(song_name)

    def onClearTextButtonClick(self):
        """
        Clear the search text.
        """
        self.SearchTextEdit.clear()

    def onSearchTextEditChanged(self, text):
        """
        If search as type enabled invoke the search on each key press.
        If the Lyrics are being searched do not start till 7 characters
        have been entered.
        """
        if self.searchAsYouType:
            search_length = 1
            if self.SearchTypeComboBox.currentIndex() == 1:
                search_length = 7
            if len(text) > search_length:
                self.onSearchTextButtonClick()

    def onImportClick(self):
        songimportform = ImportWizardForm(self, self.parent.manager,
            self.parent)
        songimportform.exec_()

    def onNewClick(self):
        self.edit_song_form.newSong()
        self.edit_song_form.exec_()

    def onEditAuthorClick(self):
        self.authors_form.load_form()
        self.authors_form.exec_()

    def onEditTopicClick(self):
        self.topics_form.load_form()
        self.topics_form.exec_()

    def onEditBookClick(self):
        self.song_book_form.load_form()
        self.song_book_form.exec_()

    def onSongMaintenanceClick(self):
        self.song_maintenance_form.exec_()

    def onRemoteEditClear(self):
        self.remoteTriggered = None
        self.remoteSong = -1

    def onRemoteEdit(self, songid):
        """
        Called by ServiceManager or SlideController by event passing
        the Song Id in the payload along with an indicator to say which
        type of display is required.
        """
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
        if self.checkItemSelected(translate(u'SongsPlugin.MediaItem',
            u'You must select an item to edit.')):
            item = self.ListView.currentItem()
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.edit_song_form.loadSong(item_id, False)
            self.edit_song_form.exec_()

    def onDeleteClick(self):
        """
        Remove a song from the list and database
        """
        if self.checkItemSelected(translate(u'SongsPlugin.MediaItem',
            u'You must select an item to delete.')):
            items = self.ListView.selectedIndexes()
            if len(items) == 1:
                del_message = translate(u'SongsPlugin.MediaItem',
                    u'Delete song?')
            else:
                del_message = unicode(
                    translate(u'SongsPlugin.MediaItem',
                        u'Delete %d songs?'))  % len(items)
            ans = QtGui.QMessageBox.question(self,
                translate(u'SongsPlugin.MediaItem', u'Delete Confirmation'),
                del_message,
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok|
                     QtGui.QMessageBox.Cancel),
                QtGui.QMessageBox.Ok)
            if ans == QtGui.QMessageBox.Cancel:
                return
            for item in items:
                item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
                self.parent.manager.delete_object(Song, item_id)
            self.onSearchTextButtonClick()

    def generateSlideData(self, service_item, item=None):
        raw_footer = []
        author_list = u''
        author_audit = []
        ccli = u''
        if item is None:
            if self.remoteTriggered is None:
                item = self.ListView.currentItem()
                if item is None:
                    return False
                item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            else:
                item_id = self.remoteSong
        else:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        service_item.add_capability(ItemCapabilities.AllowsEdit)
        service_item.add_capability(ItemCapabilities.AllowsPreview)
        service_item.add_capability(ItemCapabilities.AllowsLoop)
        song = self.parent.manager.get_object(Song, item_id)
        service_item.theme = song.theme_name
        service_item.editId = item_id
        if song.lyrics.startswith(u'<?xml version='):
            songXML = SongXMLParser(song.lyrics)
            verseList = songXML.get_verses()
            #no verse list or only 1 space (in error)
            if not song.verse_order or not song.verse_order.strip():
                for verse in verseList:
                    verseTag = u'%s:%s' % (
                        verse[0][u'type'], verse[0][u'label'])
                    service_item.add_from_text(
                        verse[1][:30], unicode(verse[1]), verseTag)
            else:
                #Loop through the verse list and expand the song accordingly.
                for order in song.verse_order.upper().split(u' '):
                    if len(order) == 0:
                        break
                    for verse in verseList:
                        if verse[0][u'label'] == order[1:] and \
                            verse[0][u'type'][0] == order[0]:
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
        if song.ccli_number is None or len(song.ccli_number) == 0:
            ccli = self.parent.settings_form.GeneralTab.CCLINumber
        else:
            ccli = unicode(song.ccli_number)
        raw_footer.append(song.title)
        raw_footer.append(author_list)
        raw_footer.append(song.copyright )
        raw_footer.append(unicode(
            translate(u'SongsPlugin.MediaItem', u'CCLI Licence: ') + ccli))
        service_item.raw_footer = raw_footer
        service_item.audit = [
            song.title, author_audit, song.copyright, song.ccli_number
        ]
        return True
