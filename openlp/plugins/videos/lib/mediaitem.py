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

class VideoMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    global log
    log=logging.getLogger("CustomMediaItem")
    log.info("Custom Media Item loaded")

    def __init__(self, parent, icon, title):
        MediaManagerItem.__init__(self, parent, icon, title)

    def setupUi(self):        
                # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.addToolbarButton('New Video', 'Load videos into openlp.org',
            ':/videos/video_load.png', self.onVideoNewClick, 'VideoNewItem')
        ## Delete Song Button ##
        self.addToolbarButton('Delete Video', 'Delete the selected video',
            ':/videos/video_delete.png', self.onVideoDeleteClick, 'VideoDeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Song Button ##
        self.addToolbarButton('Preview Video', 'Preview the selected video',
            ':/system/system_preview.png', self.onVideoPreviewClick, 'VideoPreviewItem')
        ## Live Song Button ##
        self.addToolbarButton('Go Live', 'Send the selected video live',
            ':/system/system_live.png', self.onVideoLiveClick, 'VideoLiveItem')
        ## Add Song Button ##
        self.addToolbarButton('Add Video To Service',
            'Add the selected video(s) to the service', ':/system/system_add.png',
            self.onVideoAddClick, 'VideoAddItem')
        ## Add the videolist widget ##
        self.VideoListView = QtGui.QTableWidget()
        self.VideoListView.setColumnCount(2)
        self.VideoListView.setColumnHidden(0, True)
        self.VideoListView.setColumnWidth(1, 275)
        self.VideoListView.setShowGrid(False)
        self.VideoListView.setSortingEnabled(False)
        self.VideoListView.setAlternatingRowColors(True)
        self.VideoListView.verticalHeader().setVisible(False)
        self.VideoListView.horizontalHeader().setVisible(False)
        self.VideoListView.setAlternatingRowColors(True)
        self.VideoListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.VideoListView.setObjectName("VideoListView")
        self.PageLayout.addWidget(self.VideoListView)

        #define and add the context menu
        self.VideoListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.VideoListView.addAction(self.contextMenuAction(self.VideoListView, ':/system/system_preview.png', "&Preview Video", self.onVideoPreviewClick))
        self.VideoListView.addAction(self.contextMenuAction(self.VideoListView, ':/system/system_live.png', "&Show Live", self.onVideoLiveClick))
        self.VideoListView.addAction(self.contextMenuAction(self.VideoListView, ':/system/system_add.png', "&Add to Service", self.onVideoAddClick))
        
    def initialise(self):
        list = self.parent.config.load_list('videos')
        self.loadVideoList(list)

    def onVideoNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None, "Select Image(s)", 
            self.parent.config.get_last_dir(), "Images (*.avi *.mpeg)")
        if len(files) > 0:
            self.loadVideoList(files)
            print files[0]
            dir, filename = os.path.split(str(files[0]))
            print dir ,  filename
            self.parent.config.set_last_dir(dir)
            #self.parent.config.set_list('videos', self.getFileList())
            
    def getFileList(self):
        filelist = [item[0] for item in self.VideoListView];
        return filelist            

    def loadVideoList(self, list):
        for f in list:
            file_path ,  file_name = os.path.split(str(f))
            count = self.VideoListView.rowCount()
            self.VideoListView.setRowCount(count+1)
            row_item = QtGui.QTableWidgetItem(str(f))
            self.VideoListView.setItem(count , 0, row_item)
            row_item = QtGui.QTableWidgetItem(str(file_name))
            self.VideoListView.setItem(count , 1, row_item)
            self.VideoListView.setRowHeight(count, 20)

    def onVideoDeleteClick(self):
        cr = self.VideoListView.currentRow()
        self.VideoListView.removeRow(int(cr))
        self._save_display_list(self.VideoListView)

    def onVideoPreviewClick(self):
        pass

    def onVideoLiveClick(self):
        pass

    def onVideoAddClick(self):
        pass        
