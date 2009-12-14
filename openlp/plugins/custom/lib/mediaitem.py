# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from openlp.core.lib import MediaManagerItem, SongXMLParser, BaseListWithDnD,\
Receiver, str_to_bool

class CustomListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Custom'
        BaseListWithDnD.__init__(self, parent)

class CustomMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Custom Slides.
    """
    global log
    log = logging.getLogger(u'CustomMediaItem')
    log.info(u'Custom Media Item loaded')

    def __init__(self, parent, icon, title):
        self.PluginNameShort = u'Custom'
        self.ConfigSection = title
        self.IconPath = u'custom/custom'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = CustomListView
        self.servicePath = None
        MediaManagerItem.__init__(self, parent, icon, title)
        # Holds information about whether the edit is remotly triggered and
        # which Custom is required.
        self.remoteCustom = -1

    def addEndHeaderBar(self):
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_edit' % self.parent.name), self.onRemoteEdit)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'remote_edit_clear' ), self.onRemoteEditClear)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'load_custom_list'), self.initialise)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'preview_custom'), self.onPreviewClick)

    def initPluginNameVisible(self):
        self.PluginNameVisible = self.trUtf8('Custom')

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = False

    def initialise(self):
        self.loadCustomListView(self.parent.custommanager.get_all_slides())
        #Called to redisplay the song list screen edith from a search
        #or from the exit of the Song edit dialog.  If remote editing is active
        #Trigger it and clean up so it will not update again.
        if self.remoteTriggered == u'L':
            self.onAddClick()
        if self.remoteTriggered == u'P':
            self.onPreviewClick()
        self.onRemoteEditClear()

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
        valid = self.parent.custommanager.get_custom(fields[1])
        if valid:
            self.remoteCustom = fields[1]
            self.remoteTriggered = fields[0]
            self.parent.edit_custom_form.loadCustom(fields[1],
                (fields[0] == u'P'))
            self.parent.edit_custom_form.exec_()

    def onEditClick(self):
        item = self.ListView.currentItem()
        if item:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.edit_custom_form.loadCustom(item_id, False)
            self.parent.edit_custom_form.exec_()
            self.initialise()

    def onDeleteClick(self):
        item = self.ListView.currentItem()
        if item:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            self.parent.custommanager.delete_custom(item_id)
            row = self.ListView.row(item)
            self.ListView.takeItem(row)

    def generateSlideData(self, service_item):
        raw_slides =[]
        raw_footer = []
        slide = None
        theme = None
        if self.remoteTriggered is None:
            item = self.ListView.currentItem()
            if item is None:
                return False
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        else:
            item_id = self.remoteCustom
        customSlide = self.parent.custommanager.get_custom(item_id)
        title = customSlide.title
        credit = customSlide.credits
        service_item.edit_enabled = True
        service_item.editId = item_id
        theme = customSlide.theme_name
        if len(theme) is not 0 :
            service_item.theme = theme
        songXML = SongXMLParser(customSlide.text)
        verseList = songXML.get_verses()
        for verse in verseList:
            raw_slides.append(verse[1])
        service_item.title = title
        for slide in raw_slides:
            service_item.add_from_text(slide[:30], slide)
        if str_to_bool(self.parent.config.get_config(u'display footer', True)) or \
            len(credit) > 0:
            raw_footer.append(title + u' '+ credit)
        else:
            raw_footer.append(u'')
        service_item.raw_footer = raw_footer
        return True
