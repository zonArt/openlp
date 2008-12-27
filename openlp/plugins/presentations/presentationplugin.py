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
from openlp.core.lib import Plugin, PluginUtils,  MediaManagerItem

class PresentationPlugin(Plugin, PluginUtils):
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Presentations', '1.9.0')
        self.weight = -8
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_presentation.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)


    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.icon, 'Presentations')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## Load Presentation Button ##
        self.MediaManagerItem.addToolbarButton('Load', 'Load presentations into openlp.org',
            ':/presentations/presentation_load.png', self.onPresentationLoadClick, 'PresentationLoadItem')
        ## Delete Presentation Button ##
        self.MediaManagerItem.addToolbarButton('Delete Presentation', 'Delete the selected presentation',
            ':/presentations/presentation_delete.png', self.onPresentationDeleteClick, 'PresentationDeleteItem')
        ## Separator Line ##
        self.MediaManagerItem.addToolbarSeparator()
        ## Preview Presentation Button ##
        self.MediaManagerItem.addToolbarButton('Preview Presentation', 'Preview the selected presentation',
            ':/system/system_preview.png', self.onPresentationPreviewClick, 'PresentationPreviewItem')
        ## Live Presentation Button ##
        self.MediaManagerItem.addToolbarButton('Go Live', 'Send the selected presentation live',
            ':/system/system_live.png', self.onPresentationLiveClick, 'PresentationLiveItem')
        ## Add Presentation Button ##
        self.MediaManagerItem.addToolbarButton('Add Presentation To Service',
            'Add the selected presentation(s) to the service', ':/system/system_add.png',
            self.onPresentationAddClick, 'PresentationAddItem')
        ## Add the Presentation widget ##
        self.PresentationListView = QtGui.QTableWidget()
        self.PresentationListView.setColumnCount(2)
        self.PresentationListView.setColumnHidden(0, True)
        self.PresentationListView.setColumnWidth(1, 275)
        self.PresentationListView.setShowGrid(False)
        self.PresentationListView.setSortingEnabled(False)        
        self.PresentationListView.setAlternatingRowColors(True)
        self.PresentationListView.setHorizontalHeaderLabels(QtCore.QStringList(["","Name"]))        

        self.PresentationListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.PresentationListView.setObjectName("PresentationListView")
        self.PresentationListView.setAlternatingRowColors(True)           
        self.MediaManagerItem.PageLayout.addWidget(self.PresentationListView)
        
        #define and add the context menu
        self.PresentationListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.PresentationListView.addAction(self.add_to_context_menu(self.PresentationListView, ':/system/system_preview.png', "&Preview Presentation", self.onPresentationPreviewClick))      
        self.PresentationListView.addAction(self.add_to_context_menu(self.PresentationListView, ':/system/system_live.png', "&Show Live", self.onPresentationLiveClick))        
        self.PresentationListView.addAction(self.pluginutils.add_to_context_menu(self.PresentationListView, ':/system/system_add.png', "&Add to Service", self.onPresentationAddClick))        

        return self.MediaManagerItem

    def initialise(self):
        list = self._load_display_list()
        self._load_presentation_list(list)        

    def onPresentationLoadClick(self):
        files = self.MediaManagerItem.getInputFiles("Select Presentation(s)", self._get_last_dir(), "Images (*.ppt *.pps *.odi)")
        if len(files) > 0:
            self._load_presentation_list(files)
            self._save_last_directory(files[0])
            self._save_display_list(self.PresentationListView)            

    def _load_presentation_list(self, list):
        for f in list:
            fl ,  nm = os.path.split(str(f))            
            c = self.PresentationListView.rowCount()
            self.PresentationListView.setRowCount(c+1)
            twi = QtGui.QTableWidgetItem(str(f))
            self.PresentationListView.setItem(c , 0, twi)
            twi = QtGui.QTableWidgetItem(str(nm))
            self.PresentationListView.setItem(c , 1, twi)
            self.PresentationListView.setRowHeight(c, 20)           

    def onPresentationDeleteClick(self):
        cr = self.PresentationListView.currentRow()
        self.PresentationListView.removeRow(int(cr))
        self._save_display_list(self.PresentationListView)         

    def onPresentationPreviewClick(self):
        pass

    def onPresentationLiveClick(self):
        pass

    def onPresentationAddClick(self):
        pass
