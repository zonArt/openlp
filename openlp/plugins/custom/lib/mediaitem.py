# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.core.lib import MediaManagerItem, SongXMLParser, ServiceItem, \
    translate, contextMenuAction, contextMenuSeparator, BaseListWithDnD

class CustomListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Custom'
        BaseListWithDnD.__init__(self, parent)

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
        self.IconPath = u'custom/custom'
        self.hasFileIcon = False
        self.hasNewIcon = True
        self.hasEditIcon = True
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = CustomListView
        self.ServiceItemIconName = u':/custom/custom_image.png'
        self.servicePath = None
        MediaManagerItem.__init__(self, parent, icon, title)
        self.parent = parent

    def initialise(self):
        self.loadCustomListView(self.parent.custommanager.get_all_slides())

    def loadCustomListView(self, list):
        self.ListView.clear()
        for CustomSlide in list:
            custom_name = QtGui.QListWidgetItem(CustomSlide.title)
            custom_name.setData(
                QtCore.Qt.UserRole, QtCore.QVariant(CustomSlide.id))
            self.ListView.addItem(custom_name)

    def onNewClick(self):
        self.parent.edit_custom_form.loadCustom(0)
        self.parent.edit_custom_form.exec_()
        self.initialise()

    def onEditClick(self):
        item = self.ListView.currentItem()
        if item is not None:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.edit_custom_form.loadCustom(item_id)
            self.parent.edit_custom_form.exec_()
            self.initialise()

    def onDeleteClick(self):
        item = self.ListView.currentItem()
        if item is not None:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.custommanager.delete_custom(item_id)
            row = self.ListView.row(item)
            self.ListView.takeItem(row)

    def generateSlideData(self, service_item):
        raw_slides =[]
        raw_footer = []
        slide = None
        theme = None
        item = self.ListView.currentItem()
        if item is None:
            return False
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
        return True
