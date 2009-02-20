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
from PyQt4 import QtCore, QtGui
from openlp.core.resources import *
from openlp.core.lib import Plugin, PluginUtils, MediaManagerItem, ImageServiceItem
#from forms import EditSongForm
import logging

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
#         self.layout=QtGui.QGridLayout()
#         self.ImageListView=QtGui.QWidget()
#         self.ImageListView.setLayout(self.layout)
        self.ImageListView=QtGui.QListView()
#         self.ImageListView.setColumnCount(3)
#         self.ImageListView.setColumnHidden(0, True)
#         self.ImageListView.setColumnWidth(1, 275)
#         self.ImageListView.setColumnWidth(2, 200)
#         self.ImageListView.setShowGrid(False)
#         self.ImageListView.setSortingEnabled(False)        
#         self.ImageListView.setAlternatingRowColors(True)
#         self.ImageListView.setHorizontalHeaderLabels(QtCore.QStringList(["","Name", "Preview"]))  
#         self.ImageListView.setAlternatingRowColors(True)                 
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
        if len(files) > 0:
            self._load_image_list(files)
            self._save_last_directory(files[0])
            self._save_display_list(self.ImageListView) 

    def _load_image_list(self, list):
        h=100
        self.filenames=[]
        r=0
        for f in list:
            fl ,  nm = os.path.split(str(f))
            self.filenames.append(f)
#             self.layout.addWidget(QtGui.QLabel(nm), r, 0)
            preview = QtGui.QPixmap(str(f))
#             preview = preview.scaledToHeight(h)
            label=QtGui.QLabel("")
            label.setPixmap(preview)
#             self.layout.addWidget(label, r, 1)
#             self.layout.setRowMinimumHeight(r, h)
            fl ,  nm = os.path.split(str(f))
            w=QtGui.QListWidgetItem(QtGui.QIcon(preview), nm)
#             w.setIconSize(h, h, Qt.KeepAspectRatio)
            self.ImageListView.addItem(w)
            xxx need to create an object which produces a list view of previews and use it for the controller and the selector
#             c = self.ImageListView.rowCount()
#             self.ImageListView.setRowCount(c+1)
#             twi = QtGui.QTableWidgetItem(str(f))
#             self.ImageListView.setItem(c , 0, twi)
#             twi = QtGui.QTableWidgetItem(str(nm))
#             self.ImageListView.setItem(c , 1, twi)
#             twi = QtGui.QTableWidgetItem("")
#             twi.setBackground(QtGui.QBrush(preview))
#             twi.setIcon(QtGui.QIcon(preview.scaledToHeight(h)))
#             self.ImageListView.setItem(c , 2, twi)
#             self.ImageListView.setRowHeight(c, h)
            r +=1

    def onImageDeleteClick(self):
        cr = self.ImageListView.currentRow()
        self.ImageListView.removeRow(int(cr))
        self._save_display_list(self.ImageListView)     

    def onImagePreviewClick(self):
#         cr = self.ImageListView.currentRow()
        filename = None#self.ImageListView.item(cr, 0).text()
        log.info("Preview "+str(filename))
        self.preview_service_item.add(filename)
        self.preview_service_item.render()

    def onImageLiveClick(self):
        pass

    def onImageAddClick(self):
        pass

