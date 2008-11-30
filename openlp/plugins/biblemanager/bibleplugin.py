# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
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
from openlp.core.resources import *
from openlp.core import Plugin

from biblemanager import BibleManager
from bibleimportform import BibleImportForm

class BiblePlugin(Plugin):
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Bible', '1.9.0')
        #Register the bible Manager
        self.biblemanager = BibleManager()

        # Create the plugin icon
        self.Icon = QtGui.QIcon()
        self.Icon.addPixmap(QtGui.QPixmap(':/media/media_Bible.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.Icon, 'Bibles')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## New Bible Button ##
        self.MediaManagerItem.addToolbarButton('New Bible', 'Register a new Bible',
            ':/Bibles/Bible_new.png', self.onBibleNewClick, 'BibleNewItem')
      ## Separator Line ##
        self.MediaManagerItem.addToolbarLine()
        ## Preview Bible Button ##
        self.MediaManagerItem.addToolbarButton('Preview Bible', 'Preview the selected Bible Verse',
            ':/system/system_preview.png', self.onBiblePreviewClick, 'BiblePreviewItem')
        ## Live Bible Button ##
        self.MediaManagerItem.addToolbarButton('Go Live', 'Send the selected Bible Verse(s) live',
            ':/system/system_live.png', self.onBibleLiveClick, 'BibleLiveItem')
        ## Add Bible Button ##
        self.MediaManagerItem.addToolbarButton('Add Bible Verse(s) To Service',
            'Add the selected Bible(s) to the service', ':/system/system_add.png',
            self.onBibleAddClick, 'BibleAddItem')
        ## Spacer ##
        self.BibleSpacerItem = QtGui.QSpacerItem(40, 20,
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.MediaManagerItem.addToolbarItem(self.BibleSpacerItem)
        # Add the Biblelist widget
        self.BibleList = QtGui.QTableWidget(self.MediaManagerItem)
        self.BibleList.setObjectName("BibleList")
        self.BibleList.setColumnCount(0)
        self.BibleList.setRowCount(0)
        self.MediaManagerItem.PageLayout.addWidget(self.BibleList)

    def onBibleNewClick(self):
        self.bibleimportform(self.biblemanager)

    def onBiblePreviewClick(self):
        pass

    def onBibleLiveClick(self):
        pass

    def onBibleAddClick(self):
        pass
