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
from openlp.core.lib import MediaManagerItem,  translate
from openlp.plugins.presentations.lib import FileListData

class PresentationMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    global log
    log=logging.getLogger(u'PresentationsMediaItem')
    log.info(u'Presentations Media Item loaded')

    def __init__(self, parent, icon, title):
        MediaManagerItem.__init__(self, parent, icon, title)

    def setupUi(self):
                # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Presentation Button ##
        self.addToolbarButton(
            translate('PresentationsMediaItem',u'New presentations'),
            translate('PresentationsMediaItem',u'Load presentations into openlp.org'),
            ':/presentations/presentation_load.png', self.onPresentationNewClick, 'PresentationNewItem')
        ## Delete Presentation Button ##
        self.addToolbarButton(
            translate('PresentationsMediaItem',u'Delete Presentation'),
            translate('PresentationsMediaItem',u'Delete the selected presentation'),
            ':/presentations/presentation_delete.png', self.onPresentationDeleteClick, 'PresentationDeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Presentation Button ##
        self.addToolbarButton(
            translate('PresentationsMediaItem',u'Preview Presentation'),
            translate('PresentationsMediaItem',u'Preview the selected Presentation'),
            ':/system/system_preview.png', self.onPresentationPreviewClick, 'PresentationPreviewItem')
        ## Live Presentation Button ##
        self.addToolbarButton(
            translate('PresentationsMediaItem',u'Go Live'),
            translate('PresentationsMediaItem',u'Send the selected presentation live'),
            ':/system/system_live.png', self.onPresentationLiveClick, 'PresentationLiveItem')
        ## Add Presentation Button ##
        self.addToolbarButton(
            translate('PresentationsMediaItem',u'Add Presentation To Service'),
            translate('PresentationsMediaItem',u'Add the selected Presentations(s) to the service'),
            ':/system/system_add.png',self.onPresentationAddClick, 'PresentationsAddItem')
        ## Add the Presentationlist widget ##

        self.PresentationWidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PresentationWidget.sizePolicy().hasHeightForWidth())
        self.PresentationWidget.setSizePolicy(sizePolicy)
        self.PresentationWidget.setObjectName('PresentationWidget')
        self.DisplayLayout = QtGui.QGridLayout(self.PresentationWidget)
        self.DisplayLayout.setObjectName('DisplayLayout')
        self.DisplayTypeComboBox = QtGui.QComboBox(self.PresentationWidget)
        self.DisplayTypeComboBox.setObjectName('DisplayTypeComboBox')
        self.DisplayLayout.addWidget(self.DisplayTypeComboBox, 0, 1, 1, 2)
        self.DisplayTypeLabel = QtGui.QLabel(self.PresentationWidget)
        self.DisplayTypeLabel.setObjectName('SearchTypeLabel')
        self.DisplayLayout.addWidget(self.DisplayTypeLabel, 0, 0, 1, 1)

        self.DisplayTypeLabel.setText(translate('PresentationMediaItem', u'Present using:'))

        # Add the song widget to the page layout
        self.PageLayout.addWidget(self.PresentationWidget)

        self.PresentationsListView = QtGui.QListView()
        self.PresentationsListView.setAlternatingRowColors(True)
        self.PresentationsListData = FileListData()
        self.PresentationsListView.setModel(self.PresentationsListData)

        self.PageLayout.addWidget(self.PresentationsListView)

        #define and add the context menu
        self.PresentationsListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.PresentationsListView.addAction(self.contextMenuAction(
            self.PresentationsListView, ':/system/system_preview.png',
            translate('PresentationsMediaItem',u'&Preview presentations'), self.onPresentationPreviewClick))
        self.PresentationsListView.addAction(self.contextMenuAction(
            self.PresentationsListView, ':/system/system_live.png',
            translate('PresentationsMediaItem',u'&Show Live'), self.onPresentationLiveClick))
        self.PresentationsListView.addAction(self.contextMenuAction(
            self.PresentationsListView, ':/system/system_add.png',
            translate('PresentationsMediaItem',u'&Add to Service'), self.onPresentationAddClick))

    def initialise(self):
        list = self.parent.config.load_list(u'presentations')
        self.loadPresentationList(list)
        self.DisplayTypeComboBox.addItem(u'Impress')
        self.DisplayTypeComboBox.addItem(u'Powerpoint')
        self.DisplayTypeComboBox.addItem(u'Keynote')

    def onPresentationNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None,
            translate('PresentationsMediaItem', u'Select presentations(s)'),
            self.parent.config.get_last_dir(), u'Presentations (*.ppt *.pps *.odp)')
        if len(files) > 0:
            self.loadPresentationList(files)
            dir, filename = os.path.split(str(files[0]))
            self.parent.config.set_last_dir(dir)
            self.parent.config.set_list(u'Presentations', self.PresentationsListData.getFileList())

    def getFileList(self):
        filelist = [item[0] for item in self.PresentationsListView];
        return filelist

    def loadPresentationList(self, list):
        for files in list:
            self.PresentationsListData.addRow(files)

    def onPresentationDeleteClick(self):
        indexes = self.PresentationsListView.selectedIndexes()
        for index in indexes:
            current_row = int(index.row())
            self.PresentationsListData.removeRow(current_row)
        self.parent.config.set_list(u'Presentations', self.PresentationsListData.getFileList())

    def onPresentationPreviewClick(self):
        pass

    def onPresentationLiveClick(self):
        pass

    def onPresentationAddClick(self):
        pass
