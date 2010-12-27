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
import os

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem, BaseListWithDnD, build_icon, \
    ItemCapabilities, SettingsManager, translate, check_item_selected, \
    context_menu_action

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

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'images/image'
        self.background = False
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = MediaListView
        self.PreviewFunction = QtGui.QPixmap(
            u':/media/media_video.png').toImage()
        MediaManagerItem.__init__(self, parent, self, icon)
        self.singleServiceItem = False
        self.serviceItemIconName = u':/media/image_clapperboard.png'

    def retranslateUi(self):
        self.OnNewPrompt = translate('MediaPlugin.MediaItem', 'Select Media')
        self.OnNewFileMasks = translate('MediaPlugin.MediaItem',
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
        self.listView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.listView.addAction(
            context_menu_action(self.listView, u':/slides/slide_blank.png',
                translate('MediaPlugin.MediaItem', 'Replace Live Background'),
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
        #Replace backgrounds do not work at present so remove functionality.
        self.blankButton = self.toolbar.addToolbarButton(
            translate('MediaPlugin.MediaItem', 'Replace Background'),
            u':/slides/slide_blank.png',
            translate('MediaPlugin.MediaItem', 'Replace Live Background'),
                self.onReplaceClick, False)
        self.resetButton = self.toolbar.addToolbarButton(
            u'Reset Background', u':/system/system_close.png',
            translate('ImagePlugin.MediaItem', 'Reset Live Background'),
                self.onResetClick, False)
        # Add the song widget to the page layout
        self.pageLayout.addWidget(self.ImageWidget)
        self.resetButton.setVisible(False)

    def onResetClick(self):
        self.resetButton.setVisible(False)
        self.parent.liveController.display.resetVideo()

    def onReplaceClick(self):
        if check_item_selected(self.listView,
            translate('ImagePlugin.MediaItem',
            'You must select a media file to replace the background with.')):
            item = self.listView.currentItem()
            filename = unicode(item.data(QtCore.Qt.UserRole).toString())
            self.parent.liveController.display.video(filename, 0, True)
        self.resetButton.setVisible(True)

    def generateSlideData(self, service_item, item=None, xmlVersion=False):
        if item is None:
            item = self.listView.currentItem()
            if item is None:
                return False
        filename = unicode(item.data(QtCore.Qt.UserRole).toString())
        service_item.title = unicode(
            translate('MediaPlugin.MediaItem', 'Media'))
        service_item.add_capability(ItemCapabilities.RequiresMedia)
        # force a nonexistent theme
        service_item.theme = -1
        frame = u':/media/image_clapperboard.png'
        (path, name) = os.path.split(filename)
        service_item.add_from_command(path, name, frame)
        return True

    def initialise(self):
        self.listView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.listView.setIconSize(QtCore.QSize(88, 50))
        self.loadList(SettingsManager.load_list(self.settingsSection,
            self.settingsSection))

    def onDeleteClick(self):
        """
        Remove a media item from the list
        """
        if check_item_selected(self.listView, translate('MediaPlugin.MediaItem',
            'You must select a media file to delete.')):
            row_list = [item.row() for item in self.listView.selectedIndexes()]
            row_list.sort(reverse=True)
            for row in row_list:
                self.listView.takeItem(row)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())

    def loadList(self, list):
        for file in list:
            filename = os.path.split(unicode(file))[1]
            item_name = QtGui.QListWidgetItem(filename)
            img = QtGui.QPixmap(u':/media/media_video.png').toImage()
            item_name.setIcon(build_icon(img))
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.listView.addItem(item_name)
