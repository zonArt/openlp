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
import os

from PyQt4 import QtCore, QtGui

from openlp.core import translate
from openlp.core.lib import MediaManagerItem
from openlp.core.resources import *

from openlp.plugins.videos.lib import VideoTab
from openlp.plugins.videos.lib import FileListData

class VideoMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    global log
    log=logging.getLogger(u'VideoMediaItem')
    log.info(u'Video Media Item loaded')

    def __init__(self, parent, icon, title):
        MediaManagerItem.__init__(self, parent, icon, title)

    def setupUi(self):        
                # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.addToolbarButton(
            translate('VideoMediaItem',u'New Video'), 
            translate('VideoMediaItem',u'Load videos into openlp.org'),
            ':/videos/video_load.png', self.onVideoNewClick, 'VideoNewItem')
        ## Delete Song Button ##
        self.addToolbarButton(
            translate('VideoMediaItem',u'Delete Video'), 
            translate('VideoMediaItem',u'Delete the selected video'),
            ':/videos/video_delete.png', self.onVideoDeleteClick, 'VideoDeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Song Button ##
        self.addToolbarButton(
            translate('VideoMediaItem',u'Preview Video'), 
            translate('VideoMediaItem',u'Preview the selected video'),
            ':/system/system_preview.png', self.onVideoPreviewClick, 'VideoPreviewItem')
        ## Live Song Button ##
        self.addToolbarButton(
            translate('VideoMediaItem',u'Go Live'), 
            translate('VideoMediaItem',u'Send the selected video live'),
            ':/system/system_live.png', self.onVideoLiveClick, 'VideoLiveItem')
        ## Add Song Button ##
        self.addToolbarButton(
            translate('VideoMediaItem',u'Add Video To Service'),
            translate('VideoMediaItem',u'Add the selected video(s) to the service'), 
            ':/system/system_add.png',self.onVideoAddClick, 'VideoAddItem')
        ## Add the videolist widget ##
        
        self.VideoListView = QtGui.QListView()
        self.VideoListView.setAlternatingRowColors(True)
        self.VideoListData = FileListData()
        self.VideoListView.setModel(self.VideoListData)
        
        self.PageLayout.addWidget(self.VideoListView)
        
#        self.VideoListView = QtGui.QTableWidget()
#        self.VideoListView.setColumnCount(2)
#        self.VideoListView.setColumnHidden(0, True)
#        self.VideoListView.setColumnWidth(1, 275)
#        self.VideoListView.setShowGrid(False)
#        self.VideoListView.setSortingEnabled(False)
#        self.VideoListView.setAlternatingRowColors(True)
#        self.VideoListView.verticalHeader().setVisible(False)
#        self.VideoListView.horizontalHeader().setVisible(False)
#        self.VideoListView.setAlternatingRowColors(True)
#        self.VideoListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
#        self.VideoListView.setObjectName("VideoListView")
#        self.PageLayout.addWidget(self.VideoListView)

        #define and add the context menu
        self.VideoListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.VideoListView.addAction(self.contextMenuAction(
            self.VideoListView, ':/system/system_preview.png', 
            translate('VideoMediaItem',u'&Preview Video'), self.onVideoPreviewClick))
        self.VideoListView.addAction(self.contextMenuAction(
            self.VideoListView, ':/system/system_live.png', 
            translate('VideoMediaItem',u'&Show Live'), self.onVideoLiveClick))
        self.VideoListView.addAction(self.contextMenuAction(
            self.VideoListView, ':/system/system_add.png', 
            translate('VideoMediaItem',u'&Add to Service'), self.onVideoAddClick))
        
    def initialise(self):
        list = self.parent.config.load_list(u'videos')
        self.loadVideoList(list)

    def onVideoNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None, 
            translate('VideoMediaItem', u'Select Video(s)'), 
            self.parent.config.get_last_dir(), u'Images (*.avi *.mpeg)')
        if len(files) > 0:
            self.loadVideoList(files)
            dir, filename = os.path.split(str(files[0]))
            self.parent.config.set_last_dir(dir)
            self.parent.config.set_list(u'videos', self.VideoListData.getFileList())
            
    def getFileList(self):
        filelist = [item[0] for item in self.VideoListView];
        return filelist            

    def loadVideoList(self, list):
        for files in list:
            self.VideoListData.addRow(files)
            
    def onVideoDeleteClick(self):
        indexes = self.VideoListView.selectedIndexes()
        for index in indexes:
            current_row = int(index.row())
            self.VideoListData.removeRow(current_row)
        self.parent.config.set_list(u'videos', self.VideoListData.getFileList())            

    def onVideoPreviewClick(self):
        pass

    def onVideoLiveClick(self):
        pass

    def onVideoAddClick(self):
        pass        
