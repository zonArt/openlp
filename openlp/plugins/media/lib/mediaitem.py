# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import locale

from PyQt4 import QtCore, QtGui

from openlp.core.lib import MediaManagerItem, build_icon, ItemCapabilities, \
    SettingsManager, translate, check_item_selected, Receiver
from openlp.core.lib.ui import UiStrings, critical_error_message_box
from openlp.core.ui import Controller, Display

log = logging.getLogger(__name__)

CLAPPERBOARD = QtGui.QPixmap(u':/media/media_video.png').toImage()

class MediaMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Media Slides.
    """
    log.info(u'%s MediaMediaItem loaded', __name__)

    def __init__(self, parent, plugin, icon):
        self.IconPath = u'images/image'
        self.background = False
        self.PreviewFunction = CLAPPERBOARD
        MediaManagerItem.__init__(self, parent, plugin, icon)
        self.singleServiceItem = False
        self.hasSearch = True
        self.mediaObject = None
        self.mediaController = Controller(parent)
        self.mediaController.controllerLayout = QtGui.QVBoxLayout()
        self.plugin.mediaManager.add_controller_items(self.mediaController, \
            self.mediaController.controllerLayout)
        self.plugin.mediaManager.set_controls_visible(self.mediaController, \
            False)
        self.mediaController.previewDisplay = Display(self.mediaController, \
            False, self.mediaController, self.plugin.pluginManager.plugins)
        self.mediaController.previewDisplay.setup()
        self.plugin.mediaManager.setup_display( \
            self.mediaController.previewDisplay)
        self.mediaController.previewDisplay.hide()

        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'video_background_replaced'),
            self.videobackgroundReplaced)
        # Allow DnD from the desktop
        self.listView.activateDnD()

    def retranslateUi(self):
        self.onNewPrompt = translate('MediaPlugin.MediaItem', 'Select Media')
        self.onNewFileMasks = unicode(translate('MediaPlugin.MediaItem',
            'Videos (%s);;Audio (%s);;%s (*)')) % (
            u' '.join(self.plugin.video_extensions_list),
            u' '.join(self.plugin.audio_extensions_list), UiStrings().AllFiles)
        self.replaceAction.setText(UiStrings().ReplaceBG)
        self.replaceAction.setToolTip(UiStrings().ReplaceLiveBG)
        self.resetAction.setText(UiStrings().ResetBG)
        self.resetAction.setToolTip(UiStrings().ResetLiveBG)

    def requiredIcons(self):
        MediaManagerItem.requiredIcons(self)
        self.hasFileIcon = True
        self.hasNewIcon = False
        self.hasEditIcon = False

    def addListViewToToolBar(self):
        MediaManagerItem.addListViewToToolBar(self)
        self.listView.addAction(self.replaceAction)

    def addEndHeaderBar(self):
        # Replace backgrounds do not work at present so remove functionality.
        self.replaceAction = self.addToolbarButton(u'', u'',
            u':/slides/slide_blank.png', self.onReplaceClick, False)
        self.resetAction = self.addToolbarButton(u'', u'',
            u':/system/system_close.png', self.onResetClick, False)
        self.resetAction.setVisible(False)

    def onResetClick(self):
        """
        Called to reset the Live background with the media selected,
        """
        self.plugin.liveController.mediaManager.video_reset( \
            self.plugin.liveController)
        self.resetAction.setVisible(False)

    def videobackgroundReplaced(self):
        """
        Triggered by main display on change of serviceitem
        """
        self.resetAction.setVisible(False)

    def onReplaceClick(self):
        """
        Called to replace Live background with the media selected.
        """
        if check_item_selected(self.listView,
            translate('MediaPlugin.MediaItem',
            'You must select a media file to replace the background with.')):
            item = self.listView.currentItem()
            filename = unicode(item.data(QtCore.Qt.UserRole).toString())
            if os.path.exists(filename):
                #(path, name) = os.path.split(filename)
                if self.plugin.liveController.mediaManager.video( \
                    self.plugin.liveController, filename, True, True):
                    self.resetAction.setVisible(True)
                else:
                    critical_error_message_box(UiStrings().LiveBGError,
                        translate('MediaPlugin.MediaItem',
                        'There was no display item to amend.'))
            else:
                critical_error_message_box(UiStrings().LiveBGError,
                    unicode(translate('MediaPlugin.MediaItem',
                    'There was a problem replacing your background, '
                    'the media file "%s" no longer exists.')) % filename)

    def generateSlideData(self, service_item, item=None, xmlVersion=False):
        if item is None:
            item = self.listView.currentItem()
            if item is None:
                return False
        filename = unicode(item.data(QtCore.Qt.UserRole).toString())
        if not os.path.exists(filename):
            # File is no longer present
            critical_error_message_box(
                translate('MediaPlugin.MediaItem', 'Missing Media File'),
                unicode(translate('MediaPlugin.MediaItem',
                'The file %s no longer exists.')) % filename)
            return False
        self.mediaLength = 0
        if self.plugin.mediaManager.video( \
                    self.mediaController, filename, False, False):
            self.mediaLength = self.mediaController.media_info.length
            service_item.media_length = self.mediaLength
            self.plugin.mediaManager.video_reset(self.mediaController)
            if self.mediaLength > 0:
                service_item.add_capability(
                    ItemCapabilities.AllowsVariableStartTime)
        else:
            return False
        service_item.media_length = self.mediaLength
        service_item.title = unicode(self.plugin.nameStrings[u'singular'])
        service_item.add_capability(ItemCapabilities.RequiresMedia)
        # force a non-existent theme
        service_item.theme = -1
        frame = u':/media/image_clapperboard.png'
        (path, name) = os.path.split(filename)
        service_item.add_from_command(path, name, frame)
        return True

    def initialise(self):
        self.listView.clear()
        self.listView.setIconSize(QtCore.QSize(88, 50))
        self.loadList(SettingsManager.load_list(self.settingsSection, u'media'))

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
                u'media', self.getFileList())

    def loadList(self, media):
        # Sort the themes by its filename considering language specific
        # characters. lower() is needed for windows!
        media.sort(cmp=locale.strcoll,
            key=lambda filename: os.path.split(unicode(filename))[1].lower())
        for track in media:
            filename = os.path.split(unicode(track))[1]
            item_name = QtGui.QListWidgetItem(filename)
            item_name.setIcon(build_icon(CLAPPERBOARD))
            item_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(track))
            item_name.setToolTip(track)
            self.listView.addItem(item_name)

    def search(self, string):
        files = SettingsManager.load_list(self.settingsSection, u'media')
        results = []
        string = string.lower()
        for file in files:
            filename = os.path.split(unicode(file))[1]
            if filename.lower().find(string) > -1:
                results.append([file, filename])
        return results
