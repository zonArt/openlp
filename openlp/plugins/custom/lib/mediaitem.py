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

from openlp.core import translate
from openlp.core.lib import MediaManagerItem
from openlp.core.lib import SongXMLParser
from openlp.core.lib import ServiceItem

from openlp.plugins.custom.lib import TextListData

class CustomList(QtGui.QListView):

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
        MediaManagerItem.__init__(self, parent, icon, title)
        self.parent = parent

    def setupUi(self):
        # Add a toolbar
        self.addToolbar()
        # Create buttons for the toolbar
        ## New Custom Button ##
        self.addToolbarButton(
            translate('CustomMediaItem',u'New Custom Item'),
            translate('CustomMediaItem',u'Add a new Custom Item'),
            ':/custom/custom_new.png', self.onCustomNewClick, 'CustomNewItem')
        ## Edit Custom Button ##
        self.addToolbarButton(
            translate('CustomMediaItem',u'Edit Custom Item'),
            translate('CustomMediaItem',u'Edit the selected Custom Item'),
            ':/custom/custom_edit.png', self.onCustomEditClick, 'CustomEditItem')
        ## Delete Custom Button ##
        self.addToolbarButton(
            translate('CustomMediaItem',u'Delete Custom Item'),
            translate('CustomMediaItem',u'Delete the selected Custom Item'),
            ':/custom/custom_delete.png', self.onCustomDeleteClick, 'CustomDeleteItem')
        ## Separator Line ##
        self.addToolbarSeparator()
        ## Preview Custom Button ##
        self.addToolbarButton(
            translate('CustomMediaItem',u'Preview Custom Item'),
            translate('CustomMediaItem',u'Preview the selected Custom Item'),
            ':/system/system_preview.png', self.onCustomPreviewClick, 'CustomPreviewItem')
        ## Live Custom Button ##
        self.addToolbarButton(
            translate('CustomMediaItem',u'Go Live'),
            translate('CustomMediaItem', u'Send the selected Custom live'),
            ':/system/system_live.png', self.onCustomLiveClick, 'CustomLiveItem')
        ## Add Custom Button ##
        self.addToolbarButton(
            translate('CustomMediaItem',u'Add Custom To Service'),
            translate('CustomMediaItem',u'Add the selected Custom(s) to the service'),
            ':/system/system_add.png', self.onCustomAddClick, 'CustomAddItem')
        # Add the Customlist widget
        self.CustomWidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CustomWidget.sizePolicy().hasHeightForWidth())
        self.CustomWidget.setSizePolicy(sizePolicy)
        self.CustomWidget.setObjectName(u'CustomWidget')

#        self.SearchLayout = QtGui.QGridLayout(self.CustomWidget)
#        self.SearchLayout.setObjectName('SearchLayout')
#        self.SearchTextLabel = QtGui.QLabel(self.CustomWidget)
#        self.SearchTextLabel.setObjectName('SearchTextLabel')
#        self.SearchTextLabel.setText('Search Text:')
#        self.SearchLayout.addWidget(self.SearchTextLabel, 2, 0, 1, 1)
#        self.SearchTextEdit = QtGui.QLineEdit(self.CustomWidget)
#        self.SearchTextEdit.setObjectName('SearchTextEdit')
#        self.SearchLayout.addWidget(self.SearchTextEdit, 2, 1, 1, 2)
#
#        self.ClearTextButton = QtGui.QPushButton(self.CustomWidget)
#        self.ClearTextButton.setObjectName('ClearTextButton')
#
#        self.SearchLayout.addWidget(self.ClearTextButton, 3, 1, 1, 1)
#        self.SearchTextButton = QtGui.QPushButton(self.CustomWidget)
#        self.SearchTextButton.setObjectName('SearchTextButton')
#        self.SearchLayout.addWidget(self.SearchTextButton, 3, 2, 1, 1)
        # Add the Custom widget to the page layout
        self.PageLayout.addWidget(self.CustomWidget)

        self.CustomListView = CustomList()
        self.CustomListView.setAlternatingRowColors(True)
        self.CustomListData = TextListData()
        self.CustomListView.setModel(self.CustomListData)
        self.CustomListView.setDragEnabled(True)

        self.PageLayout.addWidget(self.CustomListView)

        # Signals
#        QtCore.QObject.connect(self.SearchTextButton,
#            QtCore.SIGNAL("pressed()"), self.onSearchTextButtonClick)
#        QtCore.QObject.connect(self.ClearTextButton,
#            QtCore.SIGNAL("pressed()"), self.onClearTextButtonClick)
#        QtCore.QObject.connect(self.SearchTextEdit,
#            QtCore.SIGNAL("textChanged(const QString&)"), self.onSearchTextEditChanged)
#        QtCore.QObject.connect(self.CustomListView,
#            QtCore.SIGNAL("itemPressed(QTableWidgetItem * item)"), self.onCustomSelected)

        #define and add the context menu
        self.CustomListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.CustomListView.addAction(self.contextMenuAction(self.CustomListView,
            ':/custom/custom_edit.png', translate('CustomMediaItem', u'&Edit Custom'),
            self.onCustomEditClick))
        self.CustomListView.addAction(self.contextMenuSeparator(self.CustomListView))
        self.CustomListView.addAction(self.contextMenuAction(
            self.CustomListView, ':/system/system_preview.png',
            translate('CustomMediaItem',u'&Preview Custom'), self.onCustomPreviewClick))
        self.CustomListView.addAction(self.contextMenuAction(
            self.CustomListView, ':/system/system_live.png',
            translate('CustomMediaItem',u'&Show Live'), self.onCustomLiveClick))
        self.CustomListView.addAction(self.contextMenuAction(
            self.CustomListView, ':/system/system_add.png',
            translate('CustomMediaItem',u'&Add to Service'), self.onCustomAddClick))

#    def retranslateUi(self):
#        self.ClearTextButton.setText(translate('CustomMediaItem', u'Clear'))
#        self.SearchTextButton.setText(translate('CustomMediaItem', u'Search'))

    def initialise(self):
        self.loadCustomList(self.parent.custommanager.get_all_slides())

    def loadCustomList(self, list):
        self.CustomListData.resetStore()
        for CustomSlide in list:
            self.CustomListData.addRow(CustomSlide.id,CustomSlide.title)

    def onClearTextButtonClick(self):
        """
        Clear the search text.
        """
        self.SearchTextEdit.clear()

    def onSearchTextEditChanged(self, text):
        if len(text) > 3:  # only search if > 3 characters
            self.onSearchTextButtonClick()

    def onSearchTextButtonClick(self):
        search_keywords = str(self.SearchTextEdit.displayText())
        search_results  = []
        search_type = self.SearchTypeComboBox.currentText()
        search_results = self.Custommanager.search_Custom_lyrics(search_keywords)
        self._display_results(search_results)

    def onCustomNewClick(self):
        self.parent.edit_custom_form.loadCustom(0)
        self.parent.edit_custom_form.exec_()
        self.initialise()

    def onCustomEditClick(self):
        indexes = self.CustomListView.selectedIndexes()
        for index in indexes:
            self.parent.edit_custom_form.loadCustom(self.CustomListData.getId(index))
            self.parent.edit_custom_form.exec_()
        self.initialise()

    def onCustomDeleteClick(self):
        indexes = self.CustomListView.selectedIndexes()
        for index in indexes:
            id = self.CustomListData.getId(index)
            self.parent.custommanager.delete_custom(id)
            self.CustomListData.deleteRow(index)

    def onCustomPreviewClick(self):
        log.debug(u'Custom Preview Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_song.png")
        service_item.render_manager = self.parent.render_manager
        self.generateSlideData(service_item)
        self.parent.preview_controller.addServiceItem(service_item)

    def onCustomLiveClick(self):
        log.debug(u'Custom Live Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_song.png")
        service_item.render_manager = self.parent.render_manager
        self.generateSlideData(service_item)
        self.parent.live_controller.addServiceItem(service_item)

    def onCustomAddClick(self):
        log.debug(u'Custom Add Requested')
        service_item = ServiceItem(self.parent)
        service_item.addIcon( ":/media/media_song.png")
        service_item.render_manager = self.parent.render_manager
        self.generateSlideData(service_item)
        self.parent.service_manager.addServiceItem(service_item)

    def generateSlideData(self, service_item):
        indexes = self.CustomListView.selectedIndexes()
        raw_slides =[]
        raw_footer = []
        slide = None
        theme = None
        for index in indexes:
            id = self.CustomListData.getId(index)
            customSlide = self.parent.custommanager.get_custom(id)
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
            service_item.raw_slides = raw_slides
            service_item.raw_footer = raw_footer
