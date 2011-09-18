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

from datetime import datetime
import logging
import os
import locale

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import MediaManagerItem, build_icon, ItemCapabilities, \
    SettingsManager, translate, check_item_selected, Receiver, MediaType
from openlp.core.lib.ui import UiStrings, critical_error_message_box

log = logging.getLogger(__name__)

CLAPPERBOARD = QtGui.QPixmap(u':/media/media_video.png').toImage()

class MediaMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Media Slides.
    """
    log.info(u'%s MediaMediaItem loaded', __name__)

    def __init__(self, parent, plugin, icon):
        self.iconPath = u'images/image'
        self.background = False
        self.previewFunction = CLAPPERBOARD
        MediaManagerItem.__init__(self, parent, plugin, icon)
        self.singleServiceItem = False
        self.hasSearch = True
        self.mediaObject = None
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'video_background_replaced'),
            self.videobackgroundReplaced)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_phonon_creation'),
            self.createPhonon)
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
        Called to reset the Live backgound with the media selected,
        """
        self.resetAction.setVisible(False)
        self.plugin.liveController.display.resetVideo()

    def videobackgroundReplaced(self):
        """
        Triggered by main display on change of serviceitem
        """
        self.resetAction.setVisible(False)

    def onReplaceClick(self):
        """
        Called to replace Live backgound with the media selected.
        """
        if check_item_selected(self.listView,
            translate('MediaPlugin.MediaItem',
            'You must select a media file to replace the background with.')):
            item = self.listView.currentItem()
            filename = unicode(item.data(QtCore.Qt.UserRole).toString())
            if os.path.exists(filename):
                (path, name) = os.path.split(filename)
                if self.plugin.liveController.display.video(filename, 0, True):
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

    def generateSlideData(self, service_item, item=None, xmlVersion=False,
        remote=False):
        if item is None:
            item = self.listView.currentItem()
            if item is None:
                return False
        filename = unicode(item.data(QtCore.Qt.UserRole).toString())
        if not os.path.exists(filename):
            if not remote:
                # File is no longer present
                critical_error_message_box(
                    translate('MediaPlugin.MediaItem', 'Missing Media File'),
                        unicode(translate('MediaPlugin.MediaItem',
                            'The file %s no longer exists.')) % filename)
            return False
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        self.mediaObject.setCurrentSource(Phonon.MediaSource(filename))
        if not self.mediaStateWait(Phonon.StoppedState):
            critical_error_message_box(UiStrings().UnsupportedFile,
                    UiStrings().UnsupportedFile)
            return False
        # File too big for processing
        if os.path.getsize(filename) <= 52428800: # 50MiB
            self.mediaObject.play()
            if not self.mediaStateWait(Phonon.PlayingState) \
                or self.mediaObject.currentSource().type() \
                == Phonon.MediaSource.Invalid:
                self.mediaObject.stop()
                critical_error_message_box(
                    translate('MediaPlugin.MediaItem', 'File Too Big'),
                    translate('MediaPlugin.MediaItem', 'The file you are '
                        'trying to load is too big. Please reduce it to less '
                        'than 50MiB.'))
                return False
            self.mediaObject.stop()
            service_item.media_length = self.mediaObject.totalTime() / 1000
            service_item.add_capability(
                ItemCapabilities.HasVariableStartTime)
        service_item.title = unicode(self.plugin.nameStrings[u'singular'])
        service_item.add_capability(ItemCapabilities.RequiresMedia)
        # force a non-existent theme
        service_item.theme = -1
        frame = u':/media/image_clapperboard.png'
        (path, name) = os.path.split(filename)
        service_item.add_from_command(path, name, frame)
        return True

    def mediaStateWait(self, mediaState):
        """
        Wait for the video to change its state
        Wait no longer than 5 seconds.
        """
        start = datetime.now()
        while self.mediaObject.state() != mediaState:
            if self.mediaObject.state() == Phonon.ErrorState:
                return False
            Receiver.send_message(u'openlp_process_events')
            if (datetime.now() - start).seconds > 5:
                return False
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

    def getList(self, type=MediaType.Audio):
        media = SettingsManager.load_list(self.settingsSection, u'media')
        media.sort(cmp=locale.strcoll,
            key=lambda filename: os.path.split(unicode(filename))[1].lower())
        ext = []
        if type == MediaType.Audio:
            ext = self.plugin.audio_extensions_list
        else:
            ext = self.plugin.video_extensions_list
        ext = map(lambda x: x[1:], ext)
        media = filter(lambda x: os.path.splitext(x)[1] in ext, media)
        return media

    def createPhonon(self):
        log.debug(u'CreatePhonon')
        if not self.mediaObject:
            self.mediaObject = Phonon.MediaObject(self)

    def search(self, string):
        files = SettingsManager.load_list(self.settingsSection, u'media')
        results = []
        string = string.lower()
        for file in files:
            filename = os.path.split(unicode(file))[1]
            if filename.lower().find(string) > -1:
                results.append([file, filename])
        return results
