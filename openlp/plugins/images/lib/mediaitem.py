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
import os

from PyQt4 import QtCore, QtGui
from openlp.core.lib import MediaManagerItem, ServiceItem, translate, BaseListWithDnD,  buildIcon
from openlp.plugins.images.lib.imagetoolbar import ImageToolbar

# We have to explicitly create separate classes for each plugin
# in order for DnD to the Service manager to work correctly.
class ImageListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Image'
        BaseListWithDnD.__init__(self, parent)

class ImageMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for images.
    """
    global log
    log = logging.getLogger(u'ImageMediaItem')
    log.info(u'Image Media Item loaded')

    def __init__(self, parent, icon, title):
        self.TranslationContext = u'ImagePlugin'
        self.PluginTextShort = u'Image'
        self.ConfigSection = u'images'
        self.IconPath = u'images/image'
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False
        self.OnNewPrompt = u'Select Image(s)'
        self.OnNewFileMasks = u'Images (*.jpg *jpeg *.gif *.png *.bmp)'
        self.slidecontroller = u'image'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = ImageListView
        self.ServiceItemIconName = u':/media/media_image.png'

        MediaManagerItem.__init__(self, parent, icon, title)
        #create and install our own slide controller toolbar
        imageToolbar = ImageToolbar(self, True)
        parent.live_controller.registerToolbar(self.ConfigSection, imageToolbar)

    def initialise(self):
        self.ListView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.ListView.setIconSize(QtCore.QSize(88,50))
        self.loadList(self.parent.config.load_list(self.ConfigSection))

    def onDeleteClick(self):
        item = self.ListView.currentItem()
        if item is not None:
            item_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
            row = self.ListView.row(item)
            self.ListView.takeItem(row)
            self.parent.config.set_list(self.ConfigSection, self.ListData.getFileList())

    def loadList(self, list):
        for file in list:
            (path, filename) = os.path.split(unicode(file))
            item_name = QtGui.QListWidgetItem(filename)
            item_name.setIcon(buildIcon(file))
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.ListView.addItem(item_name)

    def generateSlideData(self, service_item):
        items = self.ListView.selectedIndexes()
        service_item.title = u'Image(s)'
        for item in items:
            bitem =  self.ListView.item(item.row())
            filename = unicode((bitem.data(QtCore.Qt.UserRole)).toString())
            frame = QtGui.QImage(unicode(filename))
            (path, name) = os.path.split(filename)
            service_item.add_from_image(path,  name, frame)
