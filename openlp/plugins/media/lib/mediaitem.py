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

from openlp.core.lib import MediaManagerItem, translate

from openlp.plugins.media.lib import MediaTab
from openlp.plugins.media.lib import FileListData
# from listwithpreviews import ListWithPreviews
from openlp.core.lib import MediaManagerItem, ServiceItem, translate, BaseListWithDnD
class MediaListView(BaseListWithDnD):
    def __init__(self, parent=None):
        self.PluginName = u'Media'
        BaseListWithDnD.__init__(self, parent)

class MediaMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Media Slides.
    """
    global log
    log = logging.getLogger(u'MediaMediaItem')
    log.info(u'Media Media Item loaded')

    def __init__(self, parent, icon, title):
        self.TranslationContext = u'MediaPlugin'
        self.PluginTextShort = u'Media'
        self.ConfigSection = u'images'
        self.OnNewPrompt = u'Select Media(s)'
        self.OnNewFileMasks = u'Videos (*.avi *.mpeg *.mpg *.mp4);;Audio (*.ogg *.mp3 *.wma);;All files (*)'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = MediaListView
        self.ServiceItemIconName = u':/media/media_image.png'
        MediaManagerItem.__init__(self, parent, icon, title)


    def generateSlideData(self, service_item):
        indexes = self.ListView.selectedIndexes()
        service_item.title = u'Media'
        for index in indexes:
            filename = self.ListData.getFilename(index)
            frame = QtGui.QImage(unicode(filename))
            (path, name) = os.path.split(filename)
            service_item.add_from_image(path,  name, frame)


    def onPreviewClick(self):
        log.debug(u'Media Preview Button pressed')
        items = self.MediaListView.selectedIndexes()
        for item in items:
            text = self.MediaListData.getValue(item)
            print text

    def onMediaLiveClick(self):
        log.debug(u'Media Live Button pressed')
        pass

#     def onMediaAddClick(self):
#         log.debug(u'Media Add Button pressed')
#         pass
