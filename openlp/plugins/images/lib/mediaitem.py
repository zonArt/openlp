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
from openlp.core.lib import MediaManagerItem, ServiceItem, translate

class ImageMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for images.
    """
    global log
    log = logging.getLogger(u'ImageMediaItem')
    log.info(u'Image Media Item loaded')

    def __init__(self, parent, icon, title):
        self.translation_context = u'ImagePlugin'
        self.plugin_text_short =u'Image'
        self.config_section=u'images'
        self.on_new_prompt=u'Select Image(s)'
        self.on_new_file_masks=u'Images (*.jpg *jpeg *.gif *.png *.bmp)'
        MediaManagerItem.__init__(self, parent, icon, title)


    def generateSlideData(self, service_item):
        indexes = self.ImageListView.selectedIndexes()
        service_item.title = u'Image(s)'
        for index in indexes:
            filename = self.ImageListData.getFilename(index)
            frame = QtGui.QImage(unicode(filename))
            (path, name) = os.path.split(filename)
            service_item.add_from_image(path,  name, frame)

