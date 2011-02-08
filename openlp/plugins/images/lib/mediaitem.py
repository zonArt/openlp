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
    check_directory_exists, Receiver
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.utils import AppLocation, delete_file, get_images_filter

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

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'images/image'
        # This next is a class, not an instance of a class - it will
        # be instanced by the base MediaManagerItem.
        self.ListViewWithDnD_class = ImageListView
        MediaManagerItem.__init__(self, parent, self, icon)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'live_theme_changed'), self.liveThemeChanged)

    def retranslateUi(self):
        self.OnNewPrompt = translate('ImagePlugin.MediaItem',
            'Select Image(s)')
        file_formats = get_images_filter()
        self.OnNewFileMasks = u'%s;;%s (*.*) (*)' % (file_formats,
            unicode(translate('ImagePlugin.MediaItem', 'All Files')))
        self.replaceAction.setText(
            translate('ImagePlugin.MediaItem', 'Replace Background'))
        self.replaceAction.setToolTip(
            translate('ImagePlugin.MediaItem', 'Replace Live Background'))
        self.resetAction.setText(
            translate('ImagePlugin.MediaItem', 'Reset Background'))
        self.resetAction.setToolTip(
            translate('ImagePlugin.MediaItem', 'Reset Live Background'))

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False
        self.addToServiceItem = True

    def initialise(self):
        log.debug(u'initialise')
        self.listView.clear()
        self.listView.setIconSize(QtCore.QSize(88, 50))
        self.servicePath = os.path.join(
            AppLocation.get_section_data_path(self.settingsSection),
            u'thumbnails')
        check_directory_exists(self.servicePath)
        self.loadList(SettingsManager.load_list(
            self.settingsSection, self.settingsSection))

    def addListViewToToolBar(self):
        MediaManagerItem.addListViewToToolBar(self)
        self.listView.addAction(self.replaceAction)

    def addEndHeaderBar(self):
        self.replaceAction = self.addToolbarButton(u'', u'',
            u':/slides/slide_blank.png', self.onReplaceClick, False)
        self.resetAction = self.addToolbarButton(u'', u'',
            u':/system/system_close.png', self.onResetClick, False)
        self.resetAction.setVisible(False)

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
                    delete_file(os.path.join(self.servicePath,
                        unicode(text.text())))
                self.listView.takeItem(row)
            SettingsManager.set_list(self.settingsSection,
                self.settingsSection, self.getFileList())

    def loadList(self, list):
        for imageFile in list:
            filename = os.path.split(unicode(imageFile))[1]
            thumb = os.path.join(self.servicePath, filename)
            if os.path.exists(thumb):
                if self.validate(imageFile, thumb):
                    icon = build_icon(thumb)
                else:
                    icon = build_icon(u':/general/general_delete.png')
            else:
                icon = self.iconFromFile(imageFile, thumb)
            item_name = QtGui.QListWidgetItem(filename)
            item_name.setIcon(icon)
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(imageFile))
            self.listView.addItem(item_name)

    def generateSlideData(self, service_item, item=None, xmlVersion=False):
        items = self.listView.selectedIndexes()
        if items:
            service_item.title = unicode(
                translate('ImagePlugin.MediaItem', 'Images'))
            service_item.add_capability(ItemCapabilities.AllowsMaintain)
            service_item.add_capability(ItemCapabilities.AllowsPreview)
            service_item.add_capability(ItemCapabilities.AllowsLoop)
            service_item.add_capability(ItemCapabilities.AllowsAdditions)
            # force a nonexistent theme
            service_item.theme = -1
            missing_items = []
            missing_items_filenames = []
            for item in items:
                bitem = self.listView.item(item.row())
                filename = unicode(bitem.data(QtCore.Qt.UserRole).toString())
                if not os.path.exists(filename):
                    missing_items.append(item)
                    missing_items_filenames.append(filename)
            for item in missing_items:
                items.remove(item)
            # We cannot continue, as all images do not exist.
            if not items:
                critical_error_message_box(
                    translate('ImagePlugin.MediaItem', 'Missing Image(s)'),
                    unicode(translate('ImagePlugin.MediaItem',
                    'The following image(s) no longer exist: %s')) %
                    u'\n'.join(missing_items_filenames))
                return False
            # We have missing as well as existing images. We ask what to do.
            elif missing_items and QtGui.QMessageBox.question(self,
                translate('ImagePlugin.MediaItem', 'Missing Image(s)'),
                unicode(translate('ImagePlugin.MediaItem', 'The following '
                'image(s) no longer exist: %s\nDo you want to add the other '
                'images anyway?')) % u'\n'.join(missing_items_filenames),
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.No |
                QtGui.QMessageBox.Yes)) == QtGui.QMessageBox.No:
                return False
            # Continue with the existing images.
            for item in items:
                bitem = self.listView.item(item.row())
                filename = unicode(bitem.data(QtCore.Qt.UserRole).toString())
                (path, name) = os.path.split(filename)
                service_item.add_from_image(filename, name)
            return True
        else:
            return False

    def onResetClick(self):
        """
        Called to reset the Live backgound with the image selected,
        """
        self.resetAction.setVisible(False)
        self.parent.liveController.display.resetImage()

    def liveThemeChanged(self):
        """
        Triggered by the change of theme in the slide controller
        """
        self.resetAction.setVisible(False)

    def onReplaceClick(self):
        """
        Called to replace Live backgound with the image selected.
        """
        if check_item_selected(self.listView,
            translate('ImagePlugin.MediaItem',
            'You must select an image to replace the background with.')):
            item = self.listView.selectedIndexes()[0]
            bitem = self.listView.item(item.row())
            filename = unicode(bitem.data(QtCore.Qt.UserRole).toString())
            if os.path.exists(filename):
                (path, name) = os.path.split(filename)
                self.parent.liveController.display.directImage(name, filename)
                self.resetAction.setVisible(True)
            else:
                critical_error_message_box(
                    translate('ImagePlugin.MediaItem', 'Live Background Error'),
                    unicode(translate('ImagePlugin.MediaItem',
                    'There was a problem replacing your background, '
                    'the image file "%s" no longer exists.')) % filename)
