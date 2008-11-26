# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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

from PyQt4 import QtCore, QtGui
from openlp.resources import *
from openlp.core import Plugin, MediaManagerItem

class SongsPlugin(Plugin):
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__('Song', '1.9.0')
        # Create the plugin icon
        self.Icon = QtGui.QIcon()
        self.Icon.addPixmap(QtGui.QPixmap(':/media/media_song.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.Icon, 'Songs')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.MediaManagerItem.addToolbarButton('New Song', 'Add a new song',
            ':/songs/song_new.png', self.onSongNewClick, 'SongNewItem')
        ## Edit Song Button ##
        self.MediaManagerItem.addToolbarButton('Edit Song', 'Edit the selected song',
            ':/songs/song_edit.png', self.onSongEditClick, 'SongEditItem')
        ## Delete Song Button ##
        self.MediaManagerItem.addToolbarButton('Delete Song', 'Delete the selected song',
            ':/songs/song_delete.png', self.onSongDeleteClick, 'SongDeleteItem')
        ## Separator Line ##
        self.MediaManagerItem.addToolbarLine()
        ## Preview Song Button ##
        self.MediaManagerItem.addToolbarButton('Preview Song', 'Preview the selected song',
            ':/system/system_preview.png', self.onSongPreviewClick, 'SongPreviewItem')
        ## Live Song Button ##
        self.MediaManagerItem.addToolbarButton('Go Live', 'Send the selected song live',
            ':/system/system_live.png', self.onSongLiveClick, 'SongLiveItem')
        ## Add Song Button ##
        self.MediaManagerItem.addToolbarButton('Add Song To Service',
            'Add the selected song(s) to the service', ':/system/system_add.png',
            self.onSongAddClick, 'SongAddItem')
        ## Spacer ##
        self.SongSpacerItem = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.MediaManagerItem.addToolbarItem(self.SongSpacerItem)
        # Add the songlist widget
        self.SongList = QtGui.QTableWidget(self.MediaManagerItem)
        self.SongList.setObjectName("SongList")
        self.SongList.setColumnCount(0)
        self.SongList.setRowCount(0)
        self.MediaManagerItem.PageLayout.addWidget(self.SongList)

    def onSongNewClick(self):
        pass

    def onSongEditClick(self):
        pass

    def onSongDeleteClick(self):
        pass

    def onSongPreviewClick(self):
        pass

    def onSongLiveClick(self):
        pass

    def onSongAddClick(self):
        pass
