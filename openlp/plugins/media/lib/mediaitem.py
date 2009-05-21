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

from openlp.core.lib import MediaManagerItem, translate

from openlp.plugins.media.lib import MediaTab
from openlp.plugins.media.lib import FileListData

class MediaMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Media Slides.
    """
    global log
    log=logging.getLogger(u'MediaMediaItem')
    log.info(u'Media Media Item loaded')

    def __init__(self, parent, icon, title):
        MediaManagerItem.__init__(self, parent, icon, title)

    def setupUi(self):
                # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Media Button ##
        self.addToolbarButton(
            translate('MediaMediaItem',u'New Media'),
            translate('MediaMediaItem',u'Load Media into openlp.org'),
            ':/videos/video_load.png', self.onMediaNewClick, 'MediaNewItem')
        ## Delete Media Button ##
        self.addToolbarButton(
            translate('MediaMediaItem',u'Delete Media'),
            translate('MediaMediaItem',u'Delete the selected Media item'),
            ':/videos/video_delete.png', self.onMediaDeleteClick, 'MediaDeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Media Button ##
        self.addToolbarButton(
            translate('MediaMediaItem',u'Preview Media'),
            translate('MediaMediaItem',u'Preview the selected Media item'),
            ':/system/system_preview.png', self.onMediaPreviewClick, 'MediaPreviewItem')
        ## Live Media Button ##
        self.addToolbarButton(
            translate('MediaMediaItem',u'Go Live'),
            translate('MediaMediaItem',u'Send the selected Media item live'),
            ':/system/system_live.png', self.onMediaLiveClick, 'MediaLiveItem')
        ## Add Media Button ##
        self.addToolbarButton(
            translate('MediaMediaItem',u'Add Media To Service'),
            translate('MediaMediaItem',u'Add the selected Media items(s) to the service'),
            ':/system/system_add.png',self.onMediaAddClick, 'MediaAddItem')
        ## Add the Medialist widget ##

        self.MediaListView = QtGui.QListView()
        self.MediaListView.setAlternatingRowColors(True)
        self.MediaListData = FileListData()
        self.MediaListView.setModel(self.MediaListData)

        self.PageLayout.addWidget(self.MediaListView)

        #define and add the context menu
        self.MediaListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.MediaListView.addAction(self.contextMenuAction(
            self.MediaListView, ':/system/system_preview.png',
            translate('MediaMediaItem',u'&Preview Media'), self.onMediaPreviewClick))
        self.MediaListView.addAction(self.contextMenuAction(
            self.MediaListView, ':/system/system_live.png',
            translate('MediaMediaItem',u'&Show Live'), self.onMediaLiveClick))
        self.MediaListView.addAction(self.contextMenuAction(
            self.MediaListView, ':/system/system_add.png',
            translate('MediaMediaItem',u'&Add to Service'), self.onMediaAddClick))

    def initialise(self):
        list = self.parent.config.load_list(u'Media')
        self.loadMediaList(list)

    def onMediaNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None,
            translate('MediaMediaItem', u'Select Media(s) items'),
            self.parent.config.get_last_dir(),
            u'Videos (*.avi *.mpeg);;Audio (*.mp3 *.ogg *.wma);;All files (*)')
        if len(files) > 0:
            self.loadMediaList(files)
            dir, filename = os.path.split(str(files[0]))
            self.parent.config.set_last_dir(dir)
            self.parent.config.set_list(u'media', self.MediaListData.getFileList())

    def getFileList(self):
        filelist = [item[0] for item in self.MediaListView];
        return filelist

    def loadMediaList(self, list):
        for files in list:
            self.MediaListData.addRow(files)

    def onMediaDeleteClick(self):
        indexes = self.MediaListView.selectedIndexes()
        for index in indexes:
            current_row = int(index.row())
            self.MediaListData.removeRow(current_row)
        self.parent.config.set_list(u'media', self.MediaListData.getFileList())

    def onMediaPreviewClick(self):
        log.debug(u'Media Preview Button pressed')
        items = self.MediaListView.selectedIndexes()
        for item in items:
            text = self.MediaListData.getValue(item)
            print text

    def onMediaLiveClick(self):
        pass

    def onMediaAddClick(self):
        pass
