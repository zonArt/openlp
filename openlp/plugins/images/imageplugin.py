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
import os
import os.path

from PyQt4 import QtCore, QtGui
from openlp.core.resources import *
from openlp.core.lib import Plugin, PluginUtils, MediaManagerItem, ImageServiceItem
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ListWithPreviews(QtCore.QAbstractListModel):
    """
    An abstract list of strings and the preview icon to go with them
    """
    global log
    log=logging.getLogger("ListWithPreviews")
    log.info("started")
    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        self.items=[] # will be a list of (filename, QPixmap) tuples
        self.rowheight=50
        self.maximagewidth=self.rowheight*16/9.0;
    def rowCount(self, parent):
        return len(self.items)
    def insertRow(self, row, filename):
        self.beginInsertRows(QModelIndex(),row,row)
        log.info("insert row %d:%s"%(row,filename))
        # get short filename to display next to image
        (prefix, shortfilename) = os.path.split(str(filename))
        log.info("shortfilename=%s"%(shortfilename))
        # create a preview image
        preview = QtGui.QPixmap(str(filename))
        w=self.maximagewidth;h=self.rowheight
        preview = preview.scaled(w,h, Qt.KeepAspectRatio)
        realw=preview.width(); realh=preview.height()
        # and move it to the centre of the preview space
        p=QPixmap(w,h)
        p.fill(Qt.transparent)
        painter=QPainter(p)
        painter.drawPixmap((w-realw)/2,(h-realh)/2,preview)
        # finally create the row
        self.items.insert(row, (filename, p, shortfilename))
        self.endInsertRows()
    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()
    def addRow(self, filename):
        self.insertRow(len(self.items), filename)
        
    def data(self, index, role):
        row=index.row()
        if row > len(self.items): # if the last row is selected and deleted, we then get called with an empty row!
            return QVariant()

        if role==Qt.DisplayRole:
            retval= self.items[row][2]
        elif role == Qt.DecorationRole:
            retval= self.items[row][1]
        elif role == Qt.ToolTipRole:
            retval= self.items[row][0]
        else:
            retval= QVariant()

#         log.info("Returning"+ str(retval))
        if type(retval) is not type(QVariant):
            return QVariant(retval)
        else:
            return retval
    def get_file_list(self):
        filelist=[i[0] for i in self.items];
        return filelist
class ImagePlugin(Plugin, PluginUtils):
    global log
    log=logging.getLogger("ImagePlugin")
    log.info("Image Plugin loaded")
    def __init__(self, preview_controller, live_controller):
        # Call the parent constructor
        Plugin.__init__(self, 'Images', '1.9.0', preview_controller, live_controller)
        self.weight = -7
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_image.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.preview_service_item=ImageServiceItem(preview_controller)
        self.live_service_item=ImageServiceItem(live_controller)
    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.icon, 'Images')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.MediaManagerItem.addToolbarButton('Load Image', 'Load images into openlp.org',
            ':/images/image_load.png', self.onImagesNewClick, 'ImageNewItem')
        ## Delete Song Button ##
        self.MediaManagerItem.addToolbarButton('Delete Image', 'Delete the selected image',
            ':/images/image_delete.png', self.onImageDeleteClick, 'ImageDeleteItem')
        ## Separator Line ##
        self.MediaManagerItem.addToolbarSeparator()
        ## Preview Song Button ##
        self.MediaManagerItem.addToolbarButton('Preview Song', 'Preview the selected image',
            ':/system/system_preview.png', self.onImagePreviewClick, 'ImagePreviewItem')
        ## Live Song Button ##
        self.MediaManagerItem.addToolbarButton('Go Live', 'Send the selected image live',
            ':/system/system_live.png', self.onImageLiveClick, 'ImageLiveItem')
        ## Add Song Button ##
        self.MediaManagerItem.addToolbarButton('Add Image To Service',
            'Add the selected image(s) to the service', ':/system/system_add.png',
            self.onImageAddClick, 'ImageAddItem')
        ## Add the songlist widget ##
        self.ImageListView=QtGui.QListView()
        self.ImageListView.uniformItemSizes=True
        self.ImageListData=ListWithPreviews()
        self.ImageListView.setModel(self.ImageListData)
        
        self.ImageListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.ImageListView.setObjectName("ImageListView")
        self.MediaManagerItem.PageLayout.addWidget(self.ImageListView)
        
        #define and add the context menu
        self.ImageListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.ImageListView.addAction(self.add_to_context_menu(self.ImageListView, ':/system/system_preview.png', "&Preview Image", self.onImagePreviewClick))      
        self.ImageListView.addAction(self.add_to_context_menu(self.ImageListView, ':/system/system_live.png', "&Show Live", self.onImageLiveClick))        
        self.ImageListView.addAction(self.add_to_context_menu(self.ImageListView, ':/system/system_add.png', "&Add to Service", self.onImageAddClick))

        self.ImageListPreview = QtGui.QWidget()
        self.MediaManagerItem.PageLayout.addWidget(self.ImageListPreview)
        self.ImageListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        

        return self.MediaManagerItem

    def initialise(self):
        log.info("Plugin Initialising")
        list = self._load_display_list()
        self._load_image_list(list)     
        log.info("Done")

    def onImagesNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None, "Select Image(s)", self._get_last_dir(), "Images (*.jpg *.gif *.png *.bmp)")
        log.info("New image(s)", str(files))
        if len(files) > 0:
            self._load_image_list(files)
            self._save_last_directory(files[0])
            self._save_display_list(self.ImageListData.get_file_list()) 

    def _load_image_list(self, list):
        for f in list:
            self.ImageListData.addRow(f)
            
    def onImageDeleteClick(self):
        indexes=self.ImageListView.selectedIndexes()
        for i in indexes:
            cr = i.row()
            self.ImageListData.removeRow(int(cr))

        self._save_display_list(self.ImageListData.get_file_list())     

    def onImageClick(self, where):
        cr = self.ImageListView.currentRow()
        filename = self.ImageListView.item(cr, 0).text()
        log.info("Click %s:%s"%(str(where), filename))
        where.add(filename)
        where.render()
        
    def onImagePreviewClick(self):
        self.onImageClick(self.preview_service_item)
    def onImageLiveClick(self):
        self.onImageClick(self.live_service_item)

    def onImageAddClick(self):
        pass

