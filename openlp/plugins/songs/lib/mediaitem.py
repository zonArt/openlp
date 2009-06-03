# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

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
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem,  translate,  ServiceItem

from openlp.plugins.songs.forms import EditSongForm
from openlp.plugins.songs.lib import TextListData

class SongList(QtGui.QListView):

    def __init__(self,parent=None,name=None):
        QtGui.QListView.__init__(self,parent)

    def mouseMoveEvent(self, event):
        """
        Drag and drop event does not care what data is selected
        as the recepient will use events to request the data move
        just tell it what plugin to call
        """
        if event.buttons() != QtCore.Qt.LeftButton:
            return
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        drag.setMimeData(mimeData)
        mimeData.setText(u'Song')

        dropAction = drag.start(QtCore.Qt.CopyAction)

        if dropAction == QtCore.Qt.CopyAction:
            self.close()

class SongMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Songs.
    """
    global log
    log = logging.getLogger("SongMediaItem")
    log.info("Song Media Item loaded")

    def __init__(self, parent, icon, title):
        MediaManagerItem.__init__(self, parent, icon, title)
        self.edit_song_form = EditSongForm(self.parent.songmanager)

    def setupUi(self):
        # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.addToolbarButton(translate('SongMediaItem', u'New Song'),
            translate('SongMediaItem', u'Add a new song'),
            ':/songs/song_new.png', self.onSongNewClick, 'SongNewItem')
        ## Edit Song Button ##
        self.addToolbarButton(translate('SongMediaItem', u'Edit Song'),
            translate('SongMediaItem', u'Edit the selected song'),
            ':/songs/song_edit.png', self.onSongEditClick, 'SongEditItem')
        ## Delete Song Button ##
        self.addToolbarButton(translate('SongMediaItem', u'Delete Song'),
            translate('SongMediaItem', u'Delete the selected song'),
            ':/songs/song_delete.png', self.onSongDeleteClick, 'SongDeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Song Button ##
        self.addToolbarButton(translate('SongMediaItem', u'Preview Song'),
            translate('SongMediaItem', u'Preview the selected song'),
            ':/system/system_preview.png', self.onSongPreviewClick, 'SongPreviewItem')
        ## Live Song Button ##
        self.addToolbarButton(translate('SongMediaItem', u'Go Live'),
            translate('SongMediaItem', u'Send the selected song live'),
            ':/system/system_live.png', self.onSongLiveClick, 'SongLiveItem')
        ## Add Song Button ##
        self.addToolbarButton(translate('SongMediaItem', u'Add Song To Service'),
            translate('SongMediaItem', u'Add the selected song(s) to the service'),
            ':/system/system_add.png', self.onSongAddClick, 'SongAddItem')
        ## Add the songlist widget ##
        # Create the tab widget
        self.SongWidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SongWidget.sizePolicy().hasHeightForWidth())
        self.SongWidget.setSizePolicy(sizePolicy)
        self.SongWidget.setObjectName('SongWidget')
        self.SearchLayout = QtGui.QGridLayout(self.SongWidget)
        self.SearchLayout.setObjectName('SearchLayout')
        self.SearchTypeComboBox = QtGui.QComboBox(self.SongWidget)
        self.SearchTypeComboBox.setObjectName('SearchTypeComboBox')
        self.SearchLayout.addWidget(self.SearchTypeComboBox, 0, 1, 1, 2)
        self.SearchTypeLabel = QtGui.QLabel(self.SongWidget)
        self.SearchTypeLabel.setObjectName('SearchTypeLabel')
        self.SearchLayout.addWidget(self.SearchTypeLabel, 0, 0, 1, 1)
        self.SearchTextLabel = QtGui.QLabel(self.SongWidget)
        self.SearchTextLabel.setObjectName('SearchTextLabel')
        self.SearchLayout.addWidget(self.SearchTextLabel, 2, 0, 1, 1)
        self.SearchTextEdit = QtGui.QLineEdit(self.SongWidget)
        self.SearchTextEdit.setObjectName('SearchTextEdit')
        self.SearchLayout.addWidget(self.SearchTextEdit, 2, 1, 1, 2)
        self.ClearTextButton = QtGui.QPushButton(self.SongWidget)
        self.ClearTextButton.setObjectName('ClearTextButton')
        self.SearchLayout.addWidget(self.ClearTextButton, 3, 1, 1, 1)
        self.SearchTextButton = QtGui.QPushButton(self.SongWidget)
        self.SearchTextButton.setObjectName('SearchTextButton')
        self.SearchLayout.addWidget(self.SearchTextButton, 3, 2, 1, 1)
        # Add the song widget to the page layout
        self.PageLayout.addWidget(self.SongWidget)

        self.SongListView = SongList()
        self.SongListView.setAlternatingRowColors(True)
        self.SongListData = TextListData()
        self.SongListView.setModel(self.SongListData)
        self.SongListView.setDragEnabled(True)

#        self.SongListView = QtGui.QTableWidget()
#        self.SongListView.setColumnCount(2)
#        self.SongListView.setColumnHidden(0, True)
#        self.SongListView.setColumnWidth(1, 240)
#        self.SongListView.setShowGrid(False)
#        self.SongListView.setSortingEnabled(False)
#        self.SongListView.setAlternatingRowColors(True)
#        self.SongListView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
#        self.SongListView.horizontalHeader().setVisible(False)
#        self.SongListView.verticalHeader().setVisible(False)
#        self.SongListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.SongListView.setObjectName('SongListView')

        self.PageLayout.addWidget(self.SongListView)
        self.SongListView.setDragEnabled(True)

        # Signals and slots
        QtCore.QObject.connect(self.SearchTextButton,
            QtCore.SIGNAL('pressed()'), self.onSearchTextButtonClick)
        QtCore.QObject.connect(self.ClearTextButton,
            QtCore.SIGNAL('pressed()'), self.onClearTextButtonClick)
        QtCore.QObject.connect(self.SearchTextEdit,
            QtCore.SIGNAL('textChanged(const QString&)'), self.onSearchTextEditChanged)
#        QtCore.QObject.connect(self.SongListView,
#            QtCore.SIGNAL('itemPressed(QTableWidgetItem * item)'), self.onSongSelected)
        #define and add the context menu
        self.SongListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.SongListView.addAction(self.contextMenuAction(self.SongListView,
            ':/songs/song_new.png', translate('SongMediaItem', u'&Edit Song'),
            self.onSongEditClick))
        self.SongListView.addAction(self.contextMenuSeparator(self.SongListView))
        self.SongListView.addAction(self.contextMenuAction(self.SongListView,
            ':/system/system_preview.png', translate('SongMediaItem', u'&Preview Song'),
            self.onSongPreviewClick))
        self.SongListView.addAction(self.contextMenuAction(self.SongListView,
            ':/system/system_live.png', translate('SongMediaItem', u'&Show Live'),
            self.onSongLiveClick))
        self.SongListView.addAction(self.contextMenuAction(self.SongListView,
            ':/system/system_add.png', translate('SongMediaItem', u'&Add to Service'),
            self.onSongEditClick))

    def retranslateUi(self):
        self.SearchTypeLabel.setText(translate('SongMediaItem', u'Search Type:'))
        self.SearchTextLabel.setText(translate('SongMediaItem', u'Search Text:'))
        self.ClearTextButton.setText(translate('SongMediaItem', u'Clear'))
        self.SearchTextButton.setText(translate('SongMediaItem', u'Search'))

    def initialise(self):
        self.SearchTypeComboBox.addItem(translate('SongMediaItem', u'Titles'))
        self.SearchTypeComboBox.addItem(translate('SongMediaItem', u'Lyrics'))
        self.SearchTypeComboBox.addItem(translate('SongMediaItem', u'Authors'))

    def displayResults(self, searchresults):
        log.debug("display results")
        self.SongListData.resetStore()
        #log.debug("Records returned from search %s", len(searchresults))
        for song in searchresults:
            author_list = u''
            for author in song.authors:
                if author_list != u'':
                    author_list = author_list + u', '
                author_list = author_list + author.display_name
            song_detail = str(u'%s (%s)' % (str(song.title), str(author_list)))

            self.SongListData.addRow(song.id,song_detail)

    def onClearTextButtonClick(self):
        """
        Clear the search text.
        """
        self.SearchTextEdit.clear()

    def onSearchTextEditChanged(self, text):
        search_length = 3
        if self.SearchTypeComboBox.currentIndex() == 1:
            search_length = 7
        if len(text) > search_length:  # only search if > 3 characters
            self.onSearchTextButtonClick()

    def onSearchTextButtonClick(self):
        search_keywords = str(self.SearchTextEdit.displayText())
        search_results  = []
        search_type = self.SearchTypeComboBox.currentIndex()
        if search_type == 0:
            log.debug("Titles Search")
            search_results = self.parent.songmanager.search_song_title(search_keywords)
        elif search_type == 1:
            log.debug("Lyrics Search")
            search_results = self.parent.songmanager.search_song_lyrics(search_keywords)
        elif search_type == 2:
            log.debug("Authors Search")
            #searchresults = self.songmanager.get_song_from_author(searchtext)
        self.displayResults(search_results)

    def onSongNewClick(self):
        self.edit_song_form.exec_()

    def onSongEditClick(self):
        current_row = self.SongListView.currentRow()
        id = int(self.SongListView.item(current_row, 0).text())
        self.edit_song_form.loadSong(id)
        self.edit_song_form.exec_()

    def onSongDeleteClick(self):
        indexes = self.SongListView.selectedIndexes()
        for index in indexes:
            id = self.SongListData.getId(index)
            self.parent.songmanager.delete_song(id)
            self.SongListData.deleteRow(index)

    def onSongPreviewClick(self):
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_song.png")
        self.generateSlideData(service_item)
        self.parent.preview_controller.addServiceItem(service_item)

    def generateSlideData(self, service_item):
        raw_slides =[]
        raw_footer = []
        indexes = self.SongListView.selectedIndexes()
        for index in indexes:
            id = self.SongListData.getId(index)
            song = self.parent.songmanager.get_song(id)
            if  song.theme_name == None or len(song.theme_name)  == 0:
                service_item.theme = None
            else:
                service_item.theme = song.theme_name
            verses = song.lyrics.split(u'\n\n')
            for verse in verses:
                raw_slides.append(verse)
            service_item.raw_slides = raw_slides
            service_item.title = song.title
        raw_footer.append(str(u'%s \n%s \n' % (song.title, song.copyright )))
        raw_footer.append(song.copyright)
        service_item.raw_footer = raw_footer

    def onSongLiveClick(self):
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_song.png")
        self.generateSlideData(service_item)
        self.parent.live_controller.addServiceItem(service_item)

    def onSongAddClick(self):
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_song.png")
        self.generateSlideData(service_item)
        self.parent.service_manager.addServiceItem(service_item)
