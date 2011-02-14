# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import MediaManagerItem, Receiver, ItemCapabilities, \
    translate, check_item_selected
from openlp.plugins.custom.lib import CustomXMLParser
from openlp.plugins.custom.lib.db import CustomSlide

log = logging.getLogger(__name__)

class CustomMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    log.info(u'Custom Media Item loaded')

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'custom/custom'
        MediaManagerItem.__init__(self, parent, self, icon)
        self.singleServiceItem = False
        # Holds information about whether the edit is remotly triggered and
        # which Custom is required.
        self.remoteCustom = -1
        self.manager = parent.manager

    def addEndHeaderBar(self):
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_edit'), self.onRemoteEdit)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_edit_clear' ), self.onRemoteEditClear)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_load_list'), self.initialise)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'custom_preview'), self.onPreviewClick)

    def initialise(self):
        self.loadList(self.manager.get_all_objects(
            CustomSlide, order_by_ref=CustomSlide.title))
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
        if check_item_selected(self.listView,
            translate('CustomPlugin.MediaItem',
            'You haven\'t selected an item to edit.')):
            item = self.listView.currentItem()
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.edit_custom_form.loadCustom(item_id, False)
            self.parent.edit_custom_form.exec_()
            self.initialise()

    def onDeleteClick(self):
        """
        Remove a custom item from the list and database
        """
        if check_item_selected(self.listView,
            translate('CustomPlugin.MediaItem',
            'You haven\'t selected an item to delete.')):
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
