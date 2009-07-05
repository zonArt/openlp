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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem,  SongXMLParser,  ServiceItem,  translate, contextMenuAction, contextMenuSeparator

class CustomList(QtGui.QListWidget):

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
        mimeData.setText(u'Custom')
        dropAction = drag.start(QtCore.Qt.CopyAction)
        if dropAction == QtCore.Qt.CopyAction:
            self.close()

class CustomMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    global log
    log=logging.getLogger(u'CustomMediaItem')
    log.info(u'Custom Media Item loaded')

    def __init__(self, parent, icon, title):
        self.TranslationContext = u'CustomPlugin'
        self.PluginTextShort = u'Custom'
        self.ConfigSection = u'custom'
        MediaManagerItem.__init__(self, parent, icon, title)
        self.parent = parent

    def setupUi(self):
        # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Custom Button ##
        self.addToolbarButton(
            translate(u'CustomMediaItem',u'New Custom Item'),
            translate(u'CustomMediaItem',u'Add a new Custom Item'),
            u':/custom/custom_new.png', self.onCustomNewClick, u'CustomNewItem')
        ## Edit Custom Button ##
        self.addToolbarButton(
            translate(u'CustomMediaItem',u'Edit Custom Item'),
            translate(u'CustomMediaItem',u'Edit the selected Custom Item'),
            u':/custom/custom_edit.png', self.onCustomEditClick, u'CustomEditItem')
        ## Delete Custom Button ##
        self.addToolbarButton(
            translate(u'CustomMediaItem',u'Delete Custom Item'),
            translate(u'CustomMediaItem',u'Delete the selected Custom Item'),
            u':/custom/custom_delete.png', self.onCustomDeleteClick, u'CustomDeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Custom Button ##
        self.addToolbarButton(
            translate(u'CustomMediaItem',u'Preview Custom Item'),
            translate(u'CustomMediaItem',u'Preview the selected Custom Item'),
            u':/system/system_preview.png', self.onCustomPreviewClick, u'CustomPreviewItem')
        ## Live Custom Button ##
        self.addToolbarButton(
            translate(u'CustomMediaItem',u'Go Live'),
            translate(u'CustomMediaItem', u'Send the selected Custom live'),
            u':/system/system_live.png', self.onCustomLiveClick, u'CustomLiveItem')
        ## Add Custom Button ##
        self.addToolbarButton(
            translate(u'CustomMediaItem',u'Add Custom To Service'),
            translate(u'CustomMediaItem',u'Add the selected Custom(s) to the service'),
            u':/system/system_add.png', self.onCustomAddClick, u'CustomAddItem')
        # Add the Customlist widget
        self.CustomWidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CustomWidget.sizePolicy().hasHeightForWidth())
        self.CustomWidget.setSizePolicy(sizePolicy)
        self.CustomWidget.setObjectName(u'CustomWidget')
        # Add the Custom widget to the page layout
        self.PageLayout.addWidget(self.CustomWidget)
        self.ListView = CustomList()
        self.ListView.setAlternatingRowColors(True)
        self.ListView.setDragEnabled(True)
        self.PageLayout.addWidget(self.ListView)
        # Signals
        QtCore.QObject.connect(self.ListView,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.onCustomPreviewClick)
        #define and add the context menu
        self.ListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ListView.addAction(contextMenuAction(self.ListView,
            ':/custom/custom_edit.png', translate(u'CustomMediaItem', u'&Edit Custom'),
            self.onCustomEditClick))
        self.ListView.addAction(contextMenuSeparator(self.ListView))
        self.ListView.addAction(contextMenuAction(
            self.ListView, ':/system/system_preview.png',
            translate(u'CustomMediaItem',u'&Preview Custom'), self.onCustomPreviewClick))
        self.ListView.addAction(contextMenuAction(
            self.ListView, ':/system/system_live.png',
            translate(u'CustomMediaItem',u'&Show Live'), self.onCustomLiveClick))
        self.ListView.addAction(contextMenuAction(
            self.ListView, ':/system/system_add.png',
            translate(u'CustomMediaItem',u'&Add to Service'), self.onCustomAddClick))

    def initialise(self):
        self.loadCustomList(self.parent.custommanager.get_all_slides())

    def loadCustomList(self, list):
        self.ListView.clear()
        for CustomSlide in list:
            custom_name = QtGui.QListWidgetItem(CustomSlide.title)
            custom_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(CustomSlide.id))
            self.ListView.addItem(custom_name)

    def onCustomNewClick(self):
        self.parent.edit_custom_form.loadCustom(0)
        self.parent.edit_custom_form.exec_()
        self.initialise()

    def onCustomEditClick(self):
        item = self.ListView.currentItem()
        if item is not None:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.edit_custom_form.loadCustom(item_id)
            self.parent.edit_custom_form.exec_()
            self.initialise()

    def onCustomDeleteClick(self):
        item = self.ListView.currentItem()
        if item is not None:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.custommanager.delete_custom(item_id)
            row = self.ListView.row(item)
            self.ListView.takeItem(row)

    def onCustomPreviewClick(self):
        log.debug(u'Custom Preview Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_song.png')
        self.generateSlideData(service_item)
        self.parent.preview_controller.addServiceItem(service_item)

    def onCustomLiveClick(self):
        log.debug(u'Custom Live Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_song.png')
        self.generateSlideData(service_item)
        self.parent.live_controller.addServiceItem(service_item)

    def onCustomAddClick(self):
        log.debug(u'Custom Add Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon(u':/media/media_song.png')
        self.generateSlideData(service_item)
        self.parent.service_manager.addServiceItem(service_item)

    def generateSlideData(self, service_item):
        raw_slides =[]
        raw_footer = []
        slide = None
        theme = None
        item = self.ListView.currentItem()
        item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        customSlide = self.parent.custommanager.get_custom(item_id)
        title = customSlide.title
        credit = customSlide.credits
        theme = customSlide.theme_name
        if len(theme) is not 0 :
            service_item.theme = theme
        songXML=SongXMLParser(customSlide.text)
        verseList = songXML.get_verses()
        for verse in verseList:
            raw_slides.append(verse[1])
        raw_footer.append(title + u' '+ credit)
        if theme is not None:
            service_item.title = title
            for slide in raw_slides:
                service_item.add_from_text(slide[:30], slide)
            service_item.raw_footer = raw_footer
