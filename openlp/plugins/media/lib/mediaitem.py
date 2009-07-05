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
import tempfile
try:
    import gst
except:
    log = logging.getLogger(u'MediaMediaItemSetup')
    log.warning(u'Can\'t generate Videos previews - import gst failed');

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem, translate

from openlp.plugins.media.lib import MediaTab
from openlp.plugins.media.lib import FileListData
# from listwithpreviews import ListWithPreviews
from openlp.core.lib import MediaManagerItem, ServiceItem, translate, BaseListWithDnD, buildIcon

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
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False
        self.IconPath = u'images/image'
        self.PluginTextShort = u'Media'
        self.ConfigSection = u'images'
        self.OnNewPrompt = u'Select Media(s)'
        self.OnNewFileMasks = u'Videos (*.avi *.mpeg *.mpg *.mp4);;Audio (*.ogg *.mp3 *.wma);;All files (*)'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = MediaListView
        #self.ServiceItemIconName = u':/media/media_image.png'
        self.PreviewFunction = self.video_get_preview
        MediaManagerItem.__init__(self, parent, icon, title)

    def video_get_preview(self, filename):
        """Gets a preview of the first frame of a video file using
        GSTREAMER (non-portable??? - Can't figure out how to do with
        Phonon - returns a QImage"""
        try:
            # Define your pipeline, just as you would at the command prompt.
            # This is much easier than trying to create and link each gstreamer element in Python.
            # This is great for pipelines that end with a filesink (i.e. there is no audible or visual output)
            log.info ("Video preview %s"%( filename))
            outfile=tempfile.NamedTemporaryFile(suffix='.png')
            cmd=u'filesrc location="%s" ! decodebin ! ffmpegcolorspace ! pngenc ! filesink location="%s"'% (filename, outfile.name)
            pipe = gst.parse_launch(cmd)
            # Get a reference to the pipeline's bus
            bus = pipe.get_bus()

            # Set the pipeline's state to PLAYING
            pipe.set_state(gst.STATE_PLAYING)

            # Listen to the pipeline's bus indefinitely until we receive a EOS (end of stream) message.
            # This is a super important step, or the pipeline might not work as expected.  For example,
            # in my example pipeline above, the pngenc will not export an actual image unless you have
            # this line of code.  It just exports a 0 byte png file.  So... don't forget this step.
            bus.poll(gst.MESSAGE_EOS, -1)
            img = QtGui.QImage(outfile.name)
            outfile.close()
#             os.unlink(outfile.name)
            pipe.set_state(gst.STATE_NULL)
            return img
        except:
            log.info("Can't generate video preview for some reason");
            import sys
            print sys.exc_info()
            return None

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
        items = self.ListView.selectedIndexes()
        for item in items:
            text = self.ListData.getValue(item)
            print text

    def onMediaLiveClick(self):
        log.debug(u'Media Live Button pressed')
        pass

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
            img = self.video_get_preview(file)
            #item_name.setIcon(buildIcon(file))
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.ListView.addItem(item_name)

#     def onMediaAddClick(self):
#         log.debug(u'Media Add Button pressed')
#         pass
