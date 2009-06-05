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

from openlp.core.lib import MediaManagerItem,  ServiceItem,  translate
from openlp.plugins.images.lib import ListWithPreviews

class ImageList(QtGui.QListView):

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
        mimeData.setText(u'Image')

        dropAction = drag.start(QtCore.Qt.CopyAction)

        if dropAction == QtCore.Qt.CopyAction:
            self.close()

class ImageMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for images.
    """
    global log
    log=logging.getLogger(u'ImageMediaItem')
    log.info(u'Image Media Item loaded')

    def __init__(self, parent, icon, title):
        MediaManagerItem.__init__(self, parent, icon, title)

    def setupUi(self):
        # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.addToolbarButton(
            translate('ImageMediaItem', u'Load Image'),
            translate('ImageMediaItem', u'Load images into openlp.org'),
            ':/images/image_load.png', self.onImagesNewClick, 'ImageNewItem')
        ## Delete Song Button ##
        self.addToolbarButton(
            translate('ImageMediaItem', u'Delete Image'),
            translate('ImageMediaItem', u'Delete the selected image'),
            ':/images/image_delete.png', self.onImageDeleteClick, 'ImageDeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Song Button ##
        self.addToolbarButton(
            translate('ImageMediaItem', u'Preview Song'),
            translate('ImageMediaItem', u'Preview the selected image'),
            ':/system/system_preview.png', self.onImagePreviewClick, 'ImagePreviewItem')
        ## Live Song Button ##
        self.addToolbarButton(
            translate('ImageMediaItem', u'Go Live'),
            translate('ImageMediaItem', u'Send the selected image live'),
            ':/system/system_live.png', self.onImageLiveClick, 'ImageLiveItem')
        ## Add Song Button ##
        self.addToolbarButton(
            translate('ImageMediaItem', u'Add Image To Service'),
            translate('ImageMediaItem', u'Add the selected image(s) to the service'),
            ':/system/system_add.png', self.onImageAddClick, 'ImageAddItem')

        #Add the Image List widget
        self.ImageListView = ImageList()
        self.ImageListView.uniformItemSizes = True
        self.ImageListData = ListWithPreviews()
        self.ImageListView.setModel(self.ImageListData)
        self.ImageListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.ImageListView.setSpacing(1)
        self.ImageListView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.ImageListView.setAlternatingRowColors(True)
        self.ImageListView.setDragEnabled(True)
        self.ImageListView.setObjectName('ImageListView')

        self.PageLayout.addWidget(self.ImageListView)

        #define and add the context menu
        self.ImageListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.ImageListView.addAction(self.contextMenuAction(
            self.ImageListView, ':/system/system_preview.png',
            translate('ImageMediaItem', u'&Preview Image'),
            self.onImagePreviewClick))
        self.ImageListView.addAction(self.contextMenuAction(
            self.ImageListView, ':/system/system_live.png',
            translate('ImageMediaItem', u'&Show Live'),
            self.onImageLiveClick))
        self.ImageListView.addAction(self.contextMenuAction(
            self.ImageListView, ':/system/system_add.png',
            translate('ImageMediaItem', u'&Add to Service'),
            self.onImageAddClick))


    def initialise(self):
        self.loadImageList(self.parent.config.load_list(u'images'))

    def onImagesNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None,
            translate('ImageMediaItem', u'Select Image(s)'),
            self.parent.config.get_last_dir(),
            u'Images (*.jpg *.gif *.png *.bmp)')
        log.info(u'New image(s)', str(files))
        if len(files) > 0:
            self.loadImageList(files)
            dir, filename = os.path.split(str(files[0]))
            self.parent.config.set_last_dir(dir)
            self.parent.config.set_list(u'images', self.ImageListData.getFileList())

    def loadImageList(self, list):
        for image in list:
            self.ImageListData.addRow(image)

    def onImageDeleteClick(self):
        indexes = self.ImageListView.selectedIndexes()
        for index in indexes:
            current_row = int(index.row())
            self.ImageListData.removeRow(current_row)
        self.parent.config.set_list(u'images', self.ImageListData.getFileList())

    def generateSlideData(self, service_item):
        indexes = self.ImageListView.selectedIndexes()
        service_item.title = u'Images'
        for index in indexes:
            filename = self.ImageListData.getFilename(index)
            frame = QtGui.QPixmap(str(filename))
            (path, name) =os.path.split(filename)
            service_item.add_from_image(name, frame)

    def onImagePreviewClick(self):
        log.debug(u'Image Preview Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_image.png")
        self.generateSlideData(service_item)
        self.parent.preview_controller.addServiceItem(service_item)

    def onImageLiveClick(self):
        log.debug(u'Image Live Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_image.png")
        self.generateSlideData(service_item)
        self.parent.live_controller.addServiceItem(service_item)

    def onImageAddClick(self):
        log.debug(u'Image Add Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_image.png")
        self.generateSlideData(service_item)
        self.parent.service_manager.addServiceItem(service_item)
