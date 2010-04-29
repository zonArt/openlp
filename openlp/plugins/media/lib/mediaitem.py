# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem, BaseListWithDnD, build_icon, \
    ItemCapabilities, SettingsManager

log = logging.getLogger(__name__)

class MediaListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Media'
        BaseListWithDnD.__init__(self, parent)

class MediaMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Media Slides.
    """
    log.info(u'%s MediaMediaItem loaded', __name__)

    def __init__(self, parent, icon, title):
        self.PluginNameShort = u'Media'
        self.IconPath = u'images/image'
        self.SettingsSection = title.lower()
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = MediaListView
        self.PreviewFunction = QtGui.QPixmap(
            u':/media/media_video.png').toImage()
        MediaManagerItem.__init__(self, parent, icon, title)
        self.singleServiceItem = False
        self.ServiceItemIconName = u':/media/media_video.png'

    def initPluginNameVisible(self):
        self.PluginNameVisible = self.trUtf8('Media')

    def retranslateUi(self):
        self.OnNewPrompt = self.trUtf8('Select Media')
        self.OnNewFileMasks = self.trUtf8('Videos (%s);;'
            'Audio (%s);;'
            'All files (*)' % (self.parent.video_list, self.parent.audio_list))

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False

    def generateSlideData(self, service_item, item=None):
        if item is None:
            item = self.ListView.currentItem()
            if item is None:
                return False
        filename = unicode((item.data(QtCore.Qt.UserRole)).toString())
        service_item.title = unicode(self.trUtf8('Media'))
        service_item.add_capability(ItemCapabilities.RequiresMedia)
        frame = u':/media/image_clapperboard.png'
        (path, name) = os.path.split(filename)
        service_item.add_from_command(path, name, frame)
        return True

    def initialise(self):
        self.ListView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.ListView.setIconSize(QtCore.QSize(88,50))
        self.loadList(SettingsManager.load_list(
            self.SettingsSection, self.SettingsSection))

    def onDeleteClick(self):
        item = self.ListView.currentItem()
        if item:
            row = self.ListView.row(item)
            self.ListView.takeItem(row)
            SettingsManager.set_list(self.SettingsSection, \
                self.SettingsSection, self.getFileList())

    def loadList(self, list):
        for file in list:
            (path, filename) = os.path.split(unicode(file))
            item_name = QtGui.QListWidgetItem(filename)
            img = QtGui.QPixmap(u':/media/media_video.png').toImage()
            item_name.setIcon(build_icon(img))
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.ListView.addItem(item_name)
