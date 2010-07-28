# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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
    context_menu_action, ItemCapabilities, SettingsManager, translate, \
    check_item_selected
from openlp.core.utils import AppLocation, get_images_filter

log = logging.getLogger(__name__)

# We have to explicitly create separate classes for each plugin
# in order for DnD to the Service manager to work correctly.
class ImageListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Images'
        BaseListWithDnD.__init__(self, parent)

class ImageMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for images.
    """
    log.info(u'Image Media Item loaded')

    def __init__(self, parent, icon, title):
        self.PluginNameShort = u'Image'
        self.pluginNameVisible = translate('ImagePlugin.MediaItem', 'Image')
        self.IconPath = u'images/image'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = ImageListView
        MediaManagerItem.__init__(self, parent, icon, title)

    def retranslateUi(self):
        self.OnNewPrompt = translate('ImagePlugin.MediaItem',
            'Select Image(s)')
        file_formats = get_images_filter()
        self.OnNewFileMasks = u'%s;;%s (*.*) (*)' % (file_formats,
            unicode(translate('ImagePlugin.MediaItem', 'All Files')))

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False
        self.addToServiceItem = True

    def initialise(self):
        log.debug(u'initialise')
        self.listView.clear()
        self.listView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.listView.setIconSize(QtCore.QSize(88, 50))
        self.servicePath = os.path.join(
            AppLocation.get_section_data_path(self.settingsSection),
            u'thumbnails')
        if not os.path.exists(self.servicePath):
            os.mkdir(self.servicePath)
        self.loadList(SettingsManager.load_list(
            self.settingsSection, self.settingsSection))

    def addListViewToToolBar(self):
        MediaManagerItem.addListViewToToolBar(self)
        self.listView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.listView.addAction(
            context_menu_action(
                self.listView, u':/slides/slide_blank.png',
                translate('ImagePlugin.MediaItem', 'Replace Live Background'),
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
        self.blankButton = self.toolbar.addToolbarButton(
            translate('ImagePlugin.MediaItem', 'Replace Background'),
            u':/slides/slide_blank.png',
            translate('ImagePlugin.MediaItem', 'Replace Live Background'),
            self.onReplaceClick, False)
        self.resetButton = self.toolbar.addToolbarButton(
            translate('ImagePlugin.MediaItem', u'Reset Background'),
            u':/system/system_close.png',
            translate('ImagePlugin.MediaItem', 'Reset Live Background'),
            self.onResetClick, False)
        # Add the song widget to the page layout
        self.pageLayout.addWidget(self.ImageWidget)
        self.resetButton.setVisible(False)

    def onDeleteClick(self):
        """
        Remove an image item from the list
        """
        if check_item_selected(self.listView, translate('ImagePlugin.MediaItem',
            'You must select an image to delete.')):
            row_list = [item.row() for item in self.listView.selectedIndexes()]
            row_list.sort(reverse=True)
            for row in row_list:
                text = self.listView.item(row)
                if text:
                    try:
                        os.remove(os.path.join(self.servicePath,
                            unicode(text.text())))
                    except OSError:
                        #if not present do not worry
                        pass
                self.listView.takeItem(row)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())

    def loadList(self, list):
        for file in list:
            filename = os.path.split(unicode(file))[1]
            thumb = os.path.join(self.servicePath, filename)
            if os.path.exists(thumb):
                if self.validate(file, thumb):
                    icon = build_icon(thumb)
                else:
                    icon = build_icon(u':/general/general_delete.png')
            else:
                icon = self.iconFromFile(file, thumb)
            item_name = QtGui.QListWidgetItem(filename)
            item_name.setIcon(icon)
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.listView.addItem(item_name)

    def generateSlideData(self, service_item, item=None):
        items = self.listView.selectedIndexes()
        if items:
            service_item.title = unicode(
                translate('ImagePlugin.MediaItem', 'Image(s)'))
            service_item.add_capability(ItemCapabilities.AllowsMaintain)
            service_item.add_capability(ItemCapabilities.AllowsPreview)
            service_item.add_capability(ItemCapabilities.AllowsLoop)
            service_item.add_capability(ItemCapabilities.AllowsAdditions)
            for item in items:
                bitem = self.listView.item(item.row())
                filename = unicode(bitem.data(QtCore.Qt.UserRole).toString())
                frame = QtGui.QImage(unicode(filename))
                (path, name) = os.path.split(filename)
                service_item.add_from_image(path, name, frame)
            return True
        else:
            return False

    def onResetClick(self):
        self.resetButton.setVisible(False)
        self.parent.liveController.display.resetImage()

    def onReplaceClick(self):
        if check_item_selected(self.listView,
            translate('ImagePlugin.MediaItem',
            'You must select an image to replace the background with.')):
            items = self.listView.selectedIndexes()
            for item in items:
                bitem = self.listView.item(item.row())
                filename = unicode(bitem.data(QtCore.Qt.UserRole).toString())
                frame = QtGui.QImage(unicode(filename))
                self.parent.liveController.display.image(frame)
        self.resetButton.setVisible(True)

    def onPreviewClick(self):
        MediaManagerItem.onPreviewClick(self)
