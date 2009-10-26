# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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
from openlp.core.lib import MediaManagerItem, BaseListWithDnD, buildIcon

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
    global log
    log = logging.getLogger(u'ImageMediaItem')
    log.info(u'Image Media Item loaded')

    def __init__(self, parent, icon, title):
        self.TranslationContext = u'ImagePlugin'
        self.PluginTextShort = u'Image'
        self.ConfigSection = u'images'
        self.IconPath = u'images/image'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = ImageListView
        self.ServiceItemIconName = u':/media/media_image.png'
        self.servicePath = None
        MediaManagerItem.__init__(self, parent, icon, title)
        self.overrideActive = False

    def retranslateUi(self):
        self.OnNewPrompt = self.trUtf8(u'Select Image(s)')
        self.OnNewFileMasks = \
            self.trUtf8(u'Images (*.jpg *jpeg *.gif *.png *.bmp)')

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False

    def initialise(self):
        log.debug(u'initialise')
        self.ListView.clear()
        self.ListView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.ListView.setIconSize(QtCore.QSize(88,50))
        self.servicePath = os.path.join(
            self.parent.config.get_data_path(), u'.thumbnails')
        if os.path.exists(self.servicePath) == False:
            os.mkdir(self.servicePath)
        self.loadList(self.parent.config.load_list(self.ConfigSection))

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
        self.OverrideLayout = QtGui.QVBoxLayout(self.ImageWidget)
        self.OverrideLayout.setMargin(5)
        self.OverrideLayout.setSpacing(4)
        self.OverrideLayout.setObjectName(u'OverrideLayout')
        self.OverrideCheckBox = QtGui.QCheckBox(self.ImageWidget)
        self.OverrideCheckBox.setObjectName(u'OverrideCheckBox')
        self.OverrideCheckBox.setCheckable(True)
        self.OverrideCheckBox.setChecked(False)
        self.OverrideCheckBox.setText(self.trUtf8(u'Override background'))
        self.OverrideCheckBox.setStatusTip(
            self.trUtf8(u'Allow background of live slide to be overridden'))
        self.OverrideLayout.addWidget(self.OverrideCheckBox)
        self.OverrideLabel = QtGui.QLabel(self.ImageWidget)
        self.OverrideLabel.setObjectName(u'OverrideLabel')
        self.OverrideLayout.addWidget(self.OverrideLabel)
        # Add the song widget to the page layout
        self.PageLayout.addWidget(self.ImageWidget)
        QtCore.QObject.connect(self.OverrideCheckBox,
            QtCore.SIGNAL(u'stateChanged(int)'),
            self.toggleOverrideState)

    def onDeleteClick(self):
        item = self.ListView.currentItem()
        if item is not None:
            try:
                os.remove(os.path.join(self.servicePath, unicode(item.text())))
            except:
                #if not present do not worry
                pass
            row = self.ListView.row(item)
            self.ListView.takeItem(row)
            self.parent.config.set_list(self.ConfigSection, self.getFileList())

    def loadList(self, list):
        for file in list:
            (path, filename) = os.path.split(unicode(file))
            thumb = os.path.join(self.servicePath, filename)
            if os.path.exists(thumb):
                icon = buildIcon(thumb)
            else:
                icon = buildIcon(unicode(file))
                pixmap = icon.pixmap(QtCore.QSize(88,50))
                ext = os.path.splitext(thumb)[1].lower()
                pixmap.save(thumb, ext[1:])
            item_name = QtGui.QListWidgetItem(filename)
            item_name.setIcon(icon)
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.ListView.addItem(item_name)

    def generateSlideData(self, service_item):
        items = self.ListView.selectedIndexes()
        if len(items) == 0:
            return False
        service_item.title = self.trUtf8(u'Image(s)')
        for item in items:
            bitem = self.ListView.item(item.row())
            filename = unicode((bitem.data(QtCore.Qt.UserRole)).toString())
            frame = QtGui.QImage(unicode(filename))
            (path, name) = os.path.split(filename)
            service_item.add_from_image(path, name, frame)
        return True

    def toggleOverrideState(self):
        self.overrideActive = not self.overrideActive
        if not self.overrideActive:
            self.OverrideLabel.setText(u'')
            self.parent.render_manager.override_background = None

    def onPreviewClick(self):
        if self.overrideActive:
            items = self.ListView.selectedIndexes()
            if len(items) == 0:
                return False
            for item in items:
                bitem = self.ListView.item(item.row())
                filename = unicode((bitem.data(QtCore.Qt.UserRole)).toString())
                self.OverrideLabel.setText(bitem.text())
                frame = QtGui.QImage(unicode(filename))
                self.parent.render_manager.override_background = frame
                self.parent.render_manager.override_background_changed = True
        else:
            MediaManagerItem.onPreviewClick(self)
