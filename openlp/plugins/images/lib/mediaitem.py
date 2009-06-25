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

# from openlp.plugins.images.lib import ListWithPreviews
from listwithpreviews import ListWithPreviews
from openlp.core.lib import MediaManagerItem, ServiceItem, translate, BaseListWithDnD

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
        self.OnNewPrompt = u'Select Image(s)'
        self.OnNewFileMasks = u'Images (*.jpg *jpeg *.gif *.png *.bmp)'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = ImageListView 
        MediaManagerItem.__init__(self, parent, icon, title)


    def generateSlideData(self, service_item):
        indexes = self.ListView.selectedIndexes()
        service_item.title = u'Image(s)'
        for index in indexes:
            filename = self.ListData.getFilename(index)
            frame = QtGui.QImage(unicode(filename))
            (path, name) = os.path.split(filename)
            service_item.add_from_image(path,  name, frame)

