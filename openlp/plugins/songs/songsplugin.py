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
from forms import EditSongForm

class SongsPlugin(Plugin):
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Songs', '1.9.0')
        self.Weight = -10
        self.edit_song_form = EditSongForm()

    def getMediaManagerItem(self):
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
   
        # Create the tab widget
        self.SongGroupBox = QtGui.QGroupBox(self.MediaManagerItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SongGroupBox.sizePolicy().hasHeightForWidth())
        self.SongGroupBox.setSizePolicy(sizePolicy)
        self.SongGroupBox.setObjectName('SearchTabWidget')

        self.QuickLayout = QtGui.QGridLayout(self.SongGroupBox)
        self.QuickLayout.setObjectName('QuickLayout')
        self.SearchTypeComboBox = QtGui.QComboBox(self.SongGroupBox)
        self.SearchTypeComboBox.setObjectName('VersionComboBox')
        self.QuickLayout.addWidget(self.SearchTypeComboBox, 0, 1, 1, 2)
        self.SearchTypeLabel = QtGui.QLabel(self.SongGroupBox)
        self.SearchTypeLabel.setObjectName('SearchTypeLabel')
        self.SearchTypeLabel.setText('Search Type:')
        self.QuickLayout.addWidget(self.SearchTypeLabel, 0, 0, 1, 1)        
      

        self.SearchTextLabel = QtGui.QLabel(self.SongGroupBox)
        self.SearchTextLabel.setObjectName('SearchTextLabel')
        self.SearchTextLabel.setText('Search Text:')
        self.QuickLayout.addWidget(self.SearchTextLabel, 2, 0, 1, 1)
        self.SearchTextEdit = QtGui.QLineEdit(self.SongGroupBox)
        self.SearchTextEdit.setObjectName('SearchTextEdit')
        self.QuickLayout.addWidget(self.SearchTextEdit, 2, 1, 1, 2)
        self.SearchTextButton = QtGui.QPushButton(self.SongGroupBox)
        self.SearchTextButton.setObjectName('SearchTextButton')
        self.SearchTextButton.setText('Search')
        self.QuickLayout.addWidget(self.SearchTextButton, 3, 2, 1, 1)
        QuickSpacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.QuickLayout.addItem(QuickSpacerItem, 4, 2, 1, 1)

        # Add the search tab widget to the page layout
        self.MediaManagerItem.PageLayout.addWidget(self.SongGroupBox)

        self.listView = QtGui.QListWidget()
        self.listView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.listView.setObjectName("listView")
        self.MediaManagerItem.PageLayout.addWidget(self.listView)     
        
        return self.MediaManagerItem

    def initalise_ui(self):
        self.SearchTypeComboBox.addItem("Lyrics")
        self.SearchTypeComboBox.addItem("Titles")
        self.SearchTypeComboBox.addItem("Authors")        

    def onSongNewClick(self):
        pass

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
