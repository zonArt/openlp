# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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

from openlp.core.lib import ItemCapabilities, MediaManagerItem,MediaType, Registry, ServiceItem, ServiceItemContext, \
    Settings, UiStrings, build_icon, check_item_selected, check_directory_exists, translate
from openlp.core.lib.ui import critical_error_message_box, create_horizontal_adjusting_combo_box
from openlp.core.ui import DisplayController, Display, DisplayControllerType
from openlp.core.ui.media import get_media_players, set_media_players
from openlp.core.utils import AppLocation, get_locale_key


log = logging.getLogger(__name__)


CLAPPERBOARD = ':/media/slidecontroller_multimedia.png'
VIDEO_ICON = build_icon(':/media/media_video.png')
AUDIO_ICON = build_icon(':/media/media_audio.png')
DVD_ICON = build_icon(':/media/media_video.png')
ERROR_ICON = build_icon(':/general/general_delete.png')


class MediaMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for Media Slides.
    """
    log.info('%s MediaMediaItem loaded', __name__)

    def __init__(self, parent, plugin):
        self.icon_path = 'images/image'
        self.background = False
        self.automatic = ''
        super(MediaMediaItem, self).__init__(parent, plugin)
        self.single_service_item = False
        self.has_search = True
        self.media_object = None
        self.display_controller = DisplayController(parent)
        self.display_controller.controller_layout = QtGui.QVBoxLayout()
        self.media_controller.register_controller(self.display_controller)
        self.media_controller.set_controls_visible(self.display_controller, False)
        self.display_controller.preview_display = Display(self.display_controller, False, self.display_controller)
        self.display_controller.preview_display.hide()
        self.display_controller.preview_display.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.display_controller.preview_display.screen = {'size': self.display_controller.preview_display.geometry()}
        self.display_controller.preview_display.setup()
        self.media_controller.setup_display(self.display_controller.preview_display, False)
        Registry().register_function('video_background_replaced', self.video_background_replaced)
        Registry().register_function('mediaitem_media_rebuild', self.rebuild_players)
        Registry().register_function('config_screen_changed', self.display_setup)
        # Allow DnD from the desktop
        self.list_view.activateDnD()

    def retranslateUi(self):
        self.on_new_prompt = translate('MediaPlugin.MediaItem', 'Select Media')
        self.replace_action.setText(UiStrings().ReplaceBG)
        self.replace_action.setToolTip(UiStrings().ReplaceLiveBG)
        self.reset_action.setText(UiStrings().ResetBG)
        self.reset_action.setToolTip(UiStrings().ResetLiveBG)
        self.automatic = UiStrings().Automatic
        self.display_type_label.setText(translate('MediaPlugin.MediaItem', 'Use Player:'))
        self.rebuild_players()

    def required_icons(self):
        """
        Set which icons the media manager tab should show
        """
        MediaManagerItem.required_icons(self)
        self.has_file_icon = True
        self.has_new_icon = False
        self.has_edit_icon = False

    def add_list_view_to_toolbar(self):
        MediaManagerItem.add_list_view_to_toolbar(self)
        self.list_view.addAction(self.replace_action)

    def add_end_header_bar(self):
        # Replace backgrounds do not work at present so remove functionality.
        self.replace_action = self.toolbar.add_toolbar_action('replace_action', icon=':/slides/slide_blank.png',
            triggers=self.onReplaceClick)
        self.reset_action = self.toolbar.add_toolbar_action('reset_action', icon=':/system/system_close.png',
            visible=False, triggers=self.onResetClick)
        self.media_widget = QtGui.QWidget(self)
        self.media_widget.setObjectName('media_widget')
        self.display_layout = QtGui.QFormLayout(self.media_widget)
        self.display_layout.setMargin(self.display_layout.spacing())
        self.display_layout.setObjectName('display_layout')
        self.display_type_label = QtGui.QLabel(self.media_widget)
        self.display_type_label.setObjectName('display_type_label')
        self.display_type_combo_box = create_horizontal_adjusting_combo_box(
            self.media_widget, 'display_type_combo_box')
        self.display_type_label.setBuddy(self.display_type_combo_box)
        self.display_layout.addRow(self.display_type_label, self.display_type_combo_box)
        # Add the Media widget to the page layout.
        self.page_layout.addWidget(self.media_widget)
        self.display_type_combo_box.currentIndexChanged.connect(self.overridePlayerChanged)

    def overridePlayerChanged(self, index):
        player = get_media_players()[0]
        if index == 0:
            set_media_players(player)
        else:
            set_media_players(player, player[index-1])

    def onResetClick(self):
        """
        Called to reset the Live background with the media selected,
        """
        self.media_controller.media_reset(self.live_controller)
        self.reset_action.setVisible(False)

    def video_background_replaced(self):
        """
        Triggered by main display on change of serviceitem.
        """
        self.reset_action.setVisible(False)

    def onReplaceClick(self):
        """
        Called to replace Live background with the media selected.
        """
        if check_item_selected(self.list_view,
                translate('MediaPlugin.MediaItem', 'You must select a media file to replace the background with.')):
            item = self.list_view.currentItem()
            filename = item.data(QtCore.Qt.UserRole)
            if os.path.exists(filename):
                service_item = ServiceItem()
                service_item.title = 'webkit'
                service_item.processor = 'webkit'
                (path, name) = os.path.split(filename)
                service_item.add_from_command(path, name,CLAPPERBOARD)
                if self.media_controller.video(DisplayControllerType.Live, service_item, video_behind_text=True):
                    self.reset_action.setVisible(True)
                else:
                    critical_error_message_box(UiStrings().LiveBGError,
                        translate('MediaPlugin.MediaItem', 'There was no display item to amend.'))
            else:
                critical_error_message_box(UiStrings().LiveBGError,
                    translate('MediaPlugin.MediaItem',
                    'There was a problem replacing your background, the media file "%s" no longer exists.') % filename)

    def generate_slide_data(self, service_item, item=None, xml_version=False, remote=False,
            context=ServiceItemContext.Live):
        """
        Generate the slide data. Needs to be implemented by the plugin.
        """
        if item is None:
            item = self.list_view.currentItem()
            if item is None:
                return False
        filename = item.data(QtCore.Qt.UserRole)
        if not os.path.exists(filename):
            if not remote:
                # File is no longer present
                critical_error_message_box(
                    translate('MediaPlugin.MediaItem', 'Missing Media File'),
                    translate('MediaPlugin.MediaItem', 'The file %s no longer exists.') % filename)
            return False
        (path, name) = os.path.split(filename)
        service_item.title = name
        service_item.processor = self.display_type_combo_box.currentText()
        service_item.add_from_command(path, name, CLAPPERBOARD)
        # Only get start and end times if going to a service
        if context == ServiceItemContext.Service:
            # Start media and obtain the length
            if not self.media_controller.media_length(service_item):
                return False
        service_item.add_capability(ItemCapabilities.CanAutoStartForLive)
        service_item.add_capability(ItemCapabilities.RequiresMedia)
        if Settings().value(self.settings_section + '/media auto start') == QtCore.Qt.Checked:
            service_item.will_auto_start = True
            # force a non-existent theme
        service_item.theme = -1
        return True

    def initialise(self):
        self.list_view.clear()
        self.list_view.setIconSize(QtCore.QSize(88, 50))
        self.servicePath = os.path.join(AppLocation.get_section_data_path(self.settings_section), 'thumbnails')
        check_directory_exists(self.servicePath)
        self.load_list(Settings().value(self.settings_section + '/media files'))
        self.populateDisplayTypes()

    def rebuild_players(self):
        """
        Rebuild the tab in the media manager when changes are made in the settings.
        """
        self.populateDisplayTypes()
        self.on_new_file_masks = translate('MediaPlugin.MediaItem', 'Videos (%s);;Audio (%s);;%s (*)') % (
            ' '.join(self.media_controller.video_extensions_list),
            ' '.join(self.media_controller.audio_extensions_list), UiStrings().AllFiles)

    def display_setup(self):
        self.media_controller.setup_display(self.display_controller.preview_display, False)

    def populateDisplayTypes(self):
        """
        Load the combobox with the enabled media players,  allowing user to select a specific player if settings allow.
        """
        # block signals to avoid unnecessary overridePlayerChanged Signals while combo box creation
        self.display_type_combo_box.blockSignals(True)
        self.display_type_combo_box.clear()
        usedPlayers, overridePlayer = get_media_players()
        media_players = self.media_controller.media_players
        currentIndex = 0
        for player in usedPlayers:
            # load the drop down selection
            self.display_type_combo_box.addItem(media_players[player].original_name)
            if overridePlayer == player:
                currentIndex = len(self.display_type_combo_box)
        if self.display_type_combo_box.count() > 1:
            self.display_type_combo_box.insertItem(0, self.automatic)
            self.display_type_combo_box.setCurrentIndex(currentIndex)
        if overridePlayer:
            self.media_widget.show()
        else:
            self.media_widget.hide()
        self.display_type_combo_box.blockSignals(False)

    def on_delete_click(self):
        """
        Remove a media item from the list.
        """
        if check_item_selected(self.list_view,
                translate('MediaPlugin.MediaItem', 'You must select a media file to delete.')):
            row_list = [item.row() for item in self.list_view.selectedIndexes()]
            row_list.sort(reverse=True)
            for row in row_list:
                self.list_view.takeItem(row)
            Settings().setValue(self.settings_section + '/media files', self.get_file_list())

    def load_list(self, media, target_group=None):
        # Sort the media by its filename considering language specific characters.
        media.sort(key=lambda filename: get_locale_key(os.path.split(str(filename))[1]))
        for track in media:
            track_info = QtCore.QFileInfo(track)
            if not os.path.exists(track):
                filename = os.path.split(str(track))[1]
                item_name = QtGui.QListWidgetItem(filename)
                item_name.setIcon(ERROR_ICON)
                item_name.setData(QtCore.Qt.UserRole, track)
            elif track_info.isFile():
                filename = os.path.split(str(track))[1]
                item_name = QtGui.QListWidgetItem(filename)
                if '*.%s' % (filename.split('.')[-1].lower()) in self.media_controller.audio_extensions_list:
                    item_name.setIcon(AUDIO_ICON)
                else:
                    item_name.setIcon(VIDEO_ICON)
                item_name.setData(QtCore.Qt.UserRole, track)
            else:
                filename = os.path.split(str(track))[1]
                item_name = QtGui.QListWidgetItem(filename)
                item_name.setIcon(build_icon(DVD_ICON))
                item_name.setData(QtCore.Qt.UserRole, track)
            item_name.setToolTip(track)
            self.list_view.addItem(item_name)

    def get_list(self, type=MediaType.Audio):
        media = Settings().value(self.settings_section + '/media files')
        media.sort(key=lambda filename: get_locale_key(os.path.split(str(filename))[1]))
        extension = []
        if type == MediaType.Audio:
            extension = self.media_controller.audio_extensions_list
        else:
            extension = self.media_controller.video_extensions_list
        extension = [x[1:] for x in extension]
        media = [x for x in media if os.path.splitext(x)[1] in extension]
        return media

    def search(self, string, showError):
        files = Settings().value(self.settings_section + '/media files')
        results = []
        string = string.lower()
        for file in files:
            filename = os.path.split(str(file))[1]
            if filename.lower().find(string) > -1:
                results.append([file, filename])
        return results
