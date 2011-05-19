# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import logging

from PyQt4 import QtCore, QtGui
from sqlalchemy.sql import or_, func

from openlp.core.lib import MediaManagerItem, Receiver, ItemCapabilities, \
    check_item_selected, translate
from openlp.core.lib.searchedit import SearchEdit
from openlp.core.lib.ui import UiStrings
from openlp.plugins.custom.lib import CustomXMLParser
from openlp.plugins.custom.lib.db import CustomSlide

log = logging.getLogger(__name__)

class CustomSearch(object):
    """
    An enumeration for custom search methods.
    """
    Titles = 1
    Themes = 2


class CustomMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    log.info(u'Custom Media Item loaded')

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'custom/custom'
        MediaManagerItem.__init__(self, parent, self, icon)
        self.singleServiceItem = False
        self.quickPreviewAllowed = True
        self.hasSearch = True
        # Holds information about whether the edit is remotly triggered and
        # which Custom is required.
        self.remoteCustom = -1
        self.manager = parent.manager
        self.setAutoSelectItem()

    def addEndHeaderBar(self):
        self.addToolbarSeparator()
        self.searchWidget = QtGui.QWidget(self)
        self.searchWidget.setObjectName(u'searchWidget')
        self.searchLayout = QtGui.QVBoxLayout(self.searchWidget)
        self.searchLayout.setObjectName(u'searchLayout')
        self.searchTextLayout = QtGui.QFormLayout()
        self.searchTextLayout.setObjectName(u'searchTextLayout')
        self.searchTextLabel = QtGui.QLabel(self.searchWidget)
        self.searchTextLabel.setObjectName(u'searchTextLabel')
        self.searchTextEdit = SearchEdit(self.searchWidget)
        self.searchTextEdit.setObjectName(u'searchTextEdit')
        self.searchTextLabel.setBuddy(self.searchTextEdit)
        self.searchTextLayout.addRow(self.searchTextLabel, self.searchTextEdit)
        self.searchLayout.addLayout(self.searchTextLayout)
        self.searchButtonLayout = QtGui.QHBoxLayout()
        self.searchButtonLayout.setObjectName(u'searchButtonLayout')
        self.searchButtonLayout.addStretch()
        self.searchTextButton = QtGui.QPushButton(self.searchWidget)
        self.searchTextButton.setObjectName(u'searchTextButton')
        self.searchButtonLayout.addWidget(self.searchTextButton)
        self.searchLayout.addLayout(self.searchButtonLayout)
        self.pageLayout.addWidget(self.searchWidget)
        # Signals and slots
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'returnPressed()'), self.onSearchTextButtonClick)
        QtCore.QObject.connect(self.searchTextButton,
            QtCore.SIGNAL(u'pressed()'), self.onSearchTextButtonClick)
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'textChanged(const QString&)'),
            self.onSearchTextEditChanged)
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'cleared()'), self.onClearTextButtonClick)
        QtCore.QObject.connect(self.searchTextEdit,
            QtCore.SIGNAL(u'searchTypeChanged(int)'),
            self.onSearchTextButtonClick)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_edit'), self.onRemoteEdit)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_edit_clear'), self.onRemoteEditClear)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_load_list'), self.initialise)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_set_autoselect_item'),
            self.setAutoSelectItem)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_preview'), self.onPreviewClick)

    def retranslateUi(self):
        self.searchTextLabel.setText(u'%s:' % UiStrings().Search)
        self.searchTextButton.setText(UiStrings().Search)

    def initialise(self):
        self.searchTextEdit.setSearchTypes([
            (CustomSearch.Titles, u':/songs/song_search_title.png',
                translate('SongsPlugin.MediaItem', 'Titles')),
            (CustomSearch.Themes, u':/slides/slide_theme.png',
                UiStrings().Themes)
        ])
        self.loadList(self.manager.get_all_objects(
            CustomSlide, order_by_ref=CustomSlide.title))
        self.searchTextEdit.setCurrentSearchType(QtCore.QSettings().value(
            u'%s/last search type' % self.settingsSection,
            QtCore.QVariant(CustomSearch.Titles)).toInt()[0])
        # Called to redisplay the custom list screen edith from a search
        # or from the exit of the Custom edit dialog. If remote editing is
        # active trigger it and clean up so it will not update again.
        if self.remoteTriggered == u'L':
            self.onAddClick()
        if self.remoteTriggered == u'P':
            self.onPreviewClick()
        self.onRemoteEditClear()

    def loadList(self, list):
        self.listView.clear()
        for customSlide in list:
            custom_name = QtGui.QListWidgetItem(customSlide.title)
            custom_name.setData(
                QtCore.Qt.UserRole, QtCore.QVariant(customSlide.id))
            self.listView.addItem(custom_name)
            # Auto-select the item if name has been set
            if customSlide.title == self.autoSelectItem :
                self.listView.setCurrentItem(custom_name)

    def setAutoSelectItem(self,itemToSelect="*"):
        self.autoSelectItem = itemToSelect

    def onNewClick(self):
        self.parent.edit_custom_form.loadCustom(0)
        self.parent.edit_custom_form.exec_()
        self.initialise()

    def onRemoteEditClear(self):
        self.remoteTriggered = None
        self.remoteCustom = -1

    def onRemoteEdit(self, customid):
        """
        Called by ServiceManager or SlideController by event passing
        the Song Id in the payload along with an indicator to say which
        type of display is required.
        """
        fields = customid.split(u':')
        valid = self.manager.get_object(CustomSlide, fields[1])
        if valid:
            self.remoteCustom = fields[1]
            self.remoteTriggered = fields[0]
            self.parent.edit_custom_form.loadCustom(fields[1],
                (fields[0] == u'P'))
            self.parent.edit_custom_form.exec_()

    def onEditClick(self):
        """
        Edit a custom item
        """
        if check_item_selected(self.listView, UiStrings().SelectEdit):
            item = self.listView.currentItem()
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.edit_custom_form.loadCustom(item_id, False)
            self.parent.edit_custom_form.exec_()
            self.initialise()

    def onDeleteClick(self):
        """
        Remove a custom item from the list and database
        """
        if check_item_selected(self.listView, UiStrings().SelectDelete):
            row_list = [item.row() for item in self.listView.selectedIndexes()]
            row_list.sort(reverse=True)
            id_list = [(item.data(QtCore.Qt.UserRole)).toInt()[0]
                for item in self.listView.selectedIndexes()]
            for id in id_list:
                self.parent.manager.delete_object(CustomSlide, id)
            for row in row_list:
                self.listView.takeItem(row)

    def generateSlideData(self, service_item, item=None, xmlVersion=False):
        raw_slides = []
        raw_footer = []
        slide = None
        theme = None
        item_id = self._getIdOfItemToGenerate(item, self.remoteCustom)
        service_item.add_capability(ItemCapabilities.AllowsEdit)
        service_item.add_capability(ItemCapabilities.AllowsPreview)
        service_item.add_capability(ItemCapabilities.AllowsLoop)
        service_item.add_capability(ItemCapabilities.AllowsVirtualSplit)
        customSlide = self.parent.manager.get_object(CustomSlide, item_id)
        title = customSlide.title
        credit = customSlide.credits
        service_item.edit_id = item_id
        theme = customSlide.theme_name
        if theme:
            service_item.theme = theme
        customXML = CustomXMLParser(customSlide.text)
        verseList = customXML.get_verses()
        for verse in verseList:
            raw_slides.append(verse[1])
        service_item.title = title
        for slide in raw_slides:
            service_item.add_from_text(slide[:30], slide)
        if QtCore.QSettings().value(self.settingsSection + u'/display footer',
            QtCore.QVariant(True)).toBool() or credit:
            raw_footer.append(title + u' ' + credit)
        else:
            raw_footer.append(u'')
        service_item.raw_footer = raw_footer
        return True

    def onSearchTextButtonClick(self):
        # Save the current search type to the configuration.
        QtCore.QSettings().setValue(u'%s/last search type' %
            self.settingsSection,
            QtCore.QVariant(self.searchTextEdit.currentSearchType()))
        # Reload the list considering the new search type.
        search_keywords = unicode(self.searchTextEdit.displayText())
        search_results = []
        search_type = self.searchTextEdit.currentSearchType()
        if search_type == CustomSearch.Titles:
            log.debug(u'Titles Search')
            search_results = self.parent.manager.get_all_objects(CustomSlide,
                CustomSlide.title.like(u'%' + self.whitespace.sub(u' ',
                search_keywords) + u'%'), order_by_ref=CustomSlide.title)
            self.loadList(search_results)
        elif search_type == CustomSearch.Themes:
            log.debug(u'Theme Search')
            search_results = self.parent.manager.get_all_objects(CustomSlide,
                CustomSlide.theme_name.like(u'%' + self.whitespace.sub(u' ',
                search_keywords) + u'%'), order_by_ref=CustomSlide.title)
            self.loadList(search_results)
        self.check_search_result()

    def onSearchTextEditChanged(self, text):
        """
        If search as type enabled invoke the search on each key press.
        If the Title is being searched do not start till 2 characters
        have been entered.
        """
        search_length = 2
        if len(text) > search_length:
            self.onSearchTextButtonClick()
        elif len(text) == 0:
            self.onClearTextButtonClick()

    def onClearTextButtonClick(self):
        """
        Clear the search text.
        """
        self.searchTextEdit.clear()
        self.onSearchTextButtonClick()

    def search(self, string):
        search_results = self.manager.get_all_objects(CustomSlide,
            or_(func.lower(CustomSlide.title).like(u'%' +
            string.lower() + u'%'),
            func.lower(CustomSlide.text).like(u'%' +
            string.lower() + u'%')),
            order_by_ref=CustomSlide.title)
        results = []
        for custom in search_results:
            results.append([custom.id, custom.title])
        return results

