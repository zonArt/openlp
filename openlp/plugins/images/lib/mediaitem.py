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
from openlp.core.lib import MediaManagerItem, BaseListWithDnD, build_icon

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
        self.ConfigSection = title
        self.IconPath = u'images/image'
        # this next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem
        self.ListViewWithDnD_class = ImageListView
        self.servicePath = None
        self.addToServiceItem = True
        MediaManagerItem.__init__(self, parent, icon, title)
        self.overrideActive = False

    def initPluginNameVisible(self):
        self.PluginNameVisible = self.trUtf8('Image')

    def retranslateUi(self):
        self.OnNewPrompt = self.trUtf8('Select Image(s)')
        self.OnNewFileMasks = \
            self.trUtf8('Images (*.jpg *.jpeg *.gif *.png *.bmp);; All files (*)')

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
        if not os.path.exists(self.servicePath):
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
        self.OverrideCheckBox.setText(self.trUtf8('Override background'))
        self.OverrideCheckBox.setStatusTip(
            self.trUtf8('Allow the background of live slide to be overridden'))
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
        if item:
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
                icon = build_icon(thumb)
            else:
                icon = build_icon(unicode(file))
                pixmap = icon.pixmap(QtCore.QSize(88,50))
                ext = os.path.splitext(thumb)[1].lower()
                pixmap.save(thumb, ext[1:])
            item_name = QtGui.QListWidgetItem(filename)
            item_name.setIcon(icon)
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(file))
            self.ListView.addItem(item_name)

    def generateSlideData(self, service_item):
        items = self.ListView.selectedIndexes()
        if items:
            service_item.title = self.trUtf8('Image(s)')
            service_item.autoPreviewAllowed = True
            service_item.maintain_allowed = True
            for item in items:
                bitem = self.ListView.item(item.row())
                filename = unicode((bitem.data(QtCore.Qt.UserRole)).toString())
                frame = QtGui.QImage(unicode(filename))
                (path, name) = os.path.split(filename)
                service_item.add_from_image(path, name, frame)
            return True
        else:
            return False

    def toggleOverrideState(self):
        self.overrideActive = not self.overrideActive
        if not self.overrideActive:
            self.OverrideLabel.setText(u'')
            self.parent.render_manager.override_background = None

    def onPreviewClick(self):
        if self.overrideActive:
            if not self.ListView.selectedIndexes():
                QtGui.QMessageBox.information(self,
                    self.trUtf8('No items selected...'),
                    self.trUtf8('You must select one or more items'))
            items = self.ListView.selectedIndexes()
            for item in items:
                bitem = self.ListView.item(item.row())
                filename = unicode((bitem.data(QtCore.Qt.UserRole)).toString())
                self.OverrideLabel.setText(bitem.text())
                frame = QtGui.QImage(unicode(filename))
                self.parent.maindisplay.addImageWithText(frame)
        else:
            MediaManagerItem.onPreviewClick(self)
