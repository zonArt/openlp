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
    ItemCapabilities, SettingsManager, context_menu_action, Receiver, translate

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
        self.background = False
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = MediaListView
        self.PreviewFunction = QtGui.QPixmap(
            u':/media/media_video.png').toImage()
        MediaManagerItem.__init__(self, parent, icon, title)
        self.singleServiceItem = False
        self.ServiceItemIconName = u':/media/media_video.png'

    def initPluginNameVisible(self):
        self.PluginNameVisible = translate(u'MediaPlugin.MediaItem', u'Media')

    def retranslateUi(self):
        self.OnNewPrompt = translate(u'MediaPlugin.MediaItem', u'Select Media')
        self.OnNewFileMasks = translate(u'MediaPlugin.MediaItem',
            u'Videos (%s);;'
            u'Audio (%s);;'
            u'All files (*)' % (self.parent.video_list, self.parent.audio_list))

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False

    def addListViewToToolBar(self):
        MediaManagerItem.addListViewToToolBar(self)
        self.ListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ListView.addAction(
            context_menu_action(self.ListView, u':/slides/slide_blank.png',
                translate(u'MediaPlugin.MediaItem', u'Replace Live Background'),
                self.onReplaceClick))

    def addEndHeaderBar(self):
        self.ImageWidget = QtGui.QWidget(self)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ImageWidget.sizePolicy().hasHeightForWidth())
        self.ImageWidget.setSizePolicy(sizePolicy)
        self.ImageWidget.setObjectName(u'ImageWidget')
        self.blankButton = self.Toolbar.addToolbarButton(
            u'Replace Background', u':/slides/slide_blank.png',
            translate(u'MediaPlugin.MediaItem', u'Replace Live Background'),
                self.onReplaceClick, False)
        # Add the song widget to the page layout
        self.PageLayout.addWidget(self.ImageWidget)

    def onReplaceClick(self):
        if self.background:
            self.background = False
            Receiver.send_message(u'videodisplay_stop')
        else:
            self.background = True
            if not self.ListView.selectedIndexes():
                QtGui.QMessageBox.information(self,
                    translate(u'MediaPlugin.MediaItem', u'No item selected'),
                    translate(u'MediaPlugin.MediaItem',
                        u'You must select one item'))
            items = self.ListView.selectedIndexes()
            for item in items:
                bitem = self.ListView.item(item.row())
                filename = unicode((bitem.data(QtCore.Qt.UserRole)).toString())
                Receiver.send_message(u'videodisplay_background', filename)

    def generateSlideData(self, service_item, item=None):
        if item is None:
            item = self.ListView.currentItem()
            if item is None:
                return False
        filename = unicode((item.data(QtCore.Qt.UserRole)).toString())
        service_item.title = unicode(
            translate(u'MediaPlugin.MediaItem', u'Media'))
        service_item.add_capability(ItemCapabilities.RequiresMedia)
        frame = u':/media/image_clapperboard.png'
        (path, name) = os.path.split(filename)
        service_item.add_from_command(path, name, frame)
        return True

    def initialise(self):
        self.ListView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.ListView.setIconSize(QtCore.QSize(88, 50))
        self.loadList(SettingsManager.load_list(self.settingsSection,
            self.settingsSection))

    def onDeleteClick(self):
        item = self.ListView.currentItem()
        if item:
            row = self.ListView.row(item)
            self.ListView.takeItem(row)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())

    def loadList(self, list):
        for file in list:
            filename = os.path.split(unicode(file))[1]
            item_name = QtGui.QListWidgetItem(filename)
            img = QtGui.QPixmap(u':/media/media_video.png').toImage()
            item_name.setIcon(build_icon(img))
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.ListView.addItem(item_name)

