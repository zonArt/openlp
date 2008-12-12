# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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
from openlp.core.resources import *
from openlp.core.lib import Plugin, MediaManagerItem
#from forms import EditSongForm

class PresentationPlugin(Plugin):
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Presentations', '1.9.0')
        self.Weight = -8
       

    def getMediaManagerItem(self):
        # Create the plugin icon
        self.Icon = QtGui.QIcon()
        self.Icon.addPixmap(QtGui.QPixmap(':/media/media_song.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.Icon, 'Presentations')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.MediaManagerItem.addToolbarButton('Update', 'Update Presentations',
            ':/songs/song_new.png', self.onPresentationNewClick, 'PresentationNewItem')
        ## Edit Song Button ##
        self.MediaManagerItem.addToolbarButton('Edit Song', 'Edit the selected song',
            ':/songs/song_edit.png', self.onSongEditClick, 'PresentationEditItem')
        ## Delete Song Button ##
        self.MediaManagerItem.addToolbarButton('Delete Song', 'Delete the selected song',
            ':/songs/song_delete.png', self.onSongDeleteClick, 'SongDeleteItem')
        ## Separator Line ##
        self.MediaManagerItem.addToolbarSeparator()
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
        ## Add the songlist widget ##

        self.listView = QtGui.QListWidget()
        self.listView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.listView.setObjectName("listView")
        self.MediaManagerItem.PageLayout.addWidget(self.listView)     

        self.onPresentationNewClick()
        
        return self.MediaManagerItem

    def onPresentationNewClick(self):
        files =  self.config.get_files()
        self.listView.clear()
        for f in files:
            self.listView.addItem(f)

    def onSongEditClick(self):
        self.edit_song_form.show()

    def onSongDeleteClick(self):
        pass

    def onSongPreviewClick(self):
        pass

    def onSongLiveClick(self):
        pass

    def onSongAddClick(self):
        pass
