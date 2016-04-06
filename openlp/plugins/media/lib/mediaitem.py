# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import Registry, RegistryProperties, AppLocation, Settings, check_directory_exists, UiStrings,\
    translate
from openlp.core.lib import ItemCapabilities, MediaManagerItem, MediaType, ServiceItem, ServiceItemContext, \
    build_icon, check_item_selected
from openlp.core.lib.ui import create_widget_action, critical_error_message_box, create_horizontal_adjusting_combo_box
from openlp.core.ui import DisplayControllerType
from openlp.core.ui.media import get_media_players, set_media_players, parse_optical_path, format_milliseconds
from openlp.core.common.languagemanager import get_locale_key
from openlp.core.ui.media.vlcplayer import get_vlc

if get_vlc() is not None:
    from openlp.plugins.media.forms.mediaclipselectorform import MediaClipSelectorForm


log = logging.getLogger(__name__)


CLAPPERBOARD = ':/media/slidecontroller_multimedia.png'


class MediaMediaItem(MediaManagerItem, RegistryProperties):
    """
    This is the custom media manager item for Media Slides.
    """
    media_go_live = QtCore.pyqtSignal(list)
    media_add_to_service = QtCore.pyqtSignal(list)
    log.info('%s MediaMediaItem loaded', __name__)

    def __init__(self, parent, plugin):
        self.setup()
        super(MediaMediaItem, self).__init__(parent, plugin)

    def setup(self):
        """
        Allow early setup to be mocked.
        """
        self.icon_path = 'images/image'
        self.background = False
        self.automatic = ''
        self.optical_icon = build_icon(':/media/media_optical.png')
        self.video_icon = build_icon(':/media/media_video.png')
        self.audio_icon = build_icon(':/media/media_audio.png')
        self.error_icon = build_icon(':/general/general_delete.png')

    def setup_item(self):
        """
        Do some additional setup.
        """
        self.media_go_live.connect(self.go_live_remote)
        self.media_add_to_service.connect(self.add_to_service_remote)
        self.single_service_item = False
        self.has_search = True
        self.media_object = None
        # self.display_controller = DisplayController(self.parent())
        Registry().register_function('video_background_replaced', self.video_background_replaced)
        Registry().register_function('mediaitem_media_rebuild', self.rebuild_players)
        # Allow DnD from the desktop
        self.list_view.activateDnD()

    def retranslateUi(self):
        """
        This method is called automatically to provide OpenLP with the opportunity to translate the ``MediaManagerItem``
        to another language.
        """
        self.on_new_prompt = translate('MediaPlugin.MediaItem', 'Select Media')
        self.replace_action.setText(UiStrings().ReplaceBG)
        self.replace_action_context.setText(UiStrings().ReplaceBG)
        if 'webkit' in get_media_players()[0]:
            self.replace_action.setToolTip(UiStrings().ReplaceLiveBG)
            self.replace_action_context.setToolTip(UiStrings().ReplaceLiveBG)
        else:
            self.replace_action.setToolTip(UiStrings().ReplaceLiveBGDisabled)
            self.replace_action_context.setToolTip(UiStrings().ReplaceLiveBGDisabled)
        self.reset_action.setText(UiStrings().ResetBG)
        self.reset_action.setToolTip(UiStrings().ResetLiveBG)
        self.reset_action_context.setText(UiStrings().ResetBG)
        self.reset_action_context.setToolTip(UiStrings().ResetLiveBG)
        self.automatic = UiStrings().Automatic
        self.display_type_label.setText(translate('MediaPlugin.MediaItem', 'Use Player:'))

    def required_icons(self):
        """
        Set which icons the media manager tab should show
        """
        MediaManagerItem.required_icons(self)
        self.has_file_icon = True
        self.has_new_icon = False
        self.has_edit_icon = False

    def add_list_view_to_toolbar(self):
        """
        Creates the main widget for listing items.
        """
        MediaManagerItem.add_list_view_to_toolbar(self)
        self.list_view.addAction(self.replace_action)

    def add_start_header_bar(self):
        """
        Adds buttons to the start of the header bar.
        """
        if 'vlc' in get_media_players()[0]:
            disable_optical_button_text = False
            optical_button_text = translate('MediaPlugin.MediaItem', 'Load CD/DVD')
            optical_button_tooltip = translate('MediaPlugin.MediaItem', 'Load CD/DVD')
        else:
            disable_optical_button_text = True
            optical_button_text = translate('MediaPlugin.MediaItem', 'Load CD/DVD')
            optical_button_tooltip = translate('MediaPlugin.MediaItem',
                                               'Load CD/DVD - only supported when VLC is installed and enabled')
        self.load_optical = self.toolbar.add_toolbar_action('load_optical', icon=self.optical_icon,
                                                            text=optical_button_text,
                                                            tooltip=optical_button_tooltip,
                                                            triggers=self.on_load_optical)
        if disable_optical_button_text:
            self.load_optical.setDisabled(True)

    def add_end_header_bar(self):
        """
        Adds buttons to the end of the header bar.
        """
        # Replace backgrounds do not work at present so remove functionality.
        self.replace_action = self.toolbar.add_toolbar_action('replace_action', icon=':/slides/slide_blank.png',
                                                              triggers=self.on_replace_click)
        if 'webkit' not in get_media_players()[0]:
            self.replace_action.setDisabled(True)
            self.replace_action_context.setDisabled(True)
        self.reset_action = self.toolbar.add_toolbar_action('reset_action', icon=':/system/system_close.png',
                                                            visible=False, triggers=self.on_reset_click)
        self.media_widget = QtWidgets.QWidget(self)
        self.media_widget.setObjectName('media_widget')
        self.display_layout = QtWidgets.QFormLayout(self.media_widget)
        self.display_layout.setContentsMargins(self.display_layout.spacing(), self.display_layout.spacing(),
                                               self.display_layout.spacing(), self.display_layout.spacing())
        self.display_layout.setObjectName('display_layout')
        self.display_type_label = QtWidgets.QLabel(self.media_widget)
        self.display_type_label.setObjectName('display_type_label')
        self.display_type_combo_box = create_horizontal_adjusting_combo_box(
            self.media_widget, 'display_type_combo_box')
        self.display_type_label.setBuddy(self.display_type_combo_box)
        self.display_layout.addRow(self.display_type_label, self.display_type_combo_box)
        # Add the Media widget to the page layout.
        self.page_layout.addWidget(self.media_widget)
        self.display_type_combo_box.currentIndexChanged.connect(self.override_player_changed)

    def add_custom_context_actions(self):
        create_widget_action(self.list_view, separator=True)
        self.replace_action_context = create_widget_action(
            self.list_view, text=UiStrings().ReplaceBG, icon=':/slides/slide_blank.png',
            triggers=self.on_replace_click)
        self.reset_action_context = create_widget_action(
            self.list_view, text=UiStrings().ReplaceLiveBG, icon=':/system/system_close.png',
            visible=False, triggers=self.on_reset_click)

    @staticmethod
    def override_player_changed(index):
        """
        The Player has been overridden

        :param index: Index
        """
        player = get_media_players()[0]
        if index == 0:
            set_media_players(player)
        else:
            set_media_players(player, player[index - 1])

    def on_reset_click(self):
        """
        Called to reset the Live background with the media selected,
        """
        self.media_controller.media_reset(self.live_controller)
        self.reset_action.setVisible(False)
        self.reset_action_context.setVisible(False)

    def video_background_replaced(self):
        """
        Triggered by main display on change of serviceitem.
        """
        self.reset_action.setVisible(False)
        self.reset_action_context.setVisible(False)

    def on_replace_click(self):
        """
        Called to replace Live background with the media selected.
        """
        if check_item_selected(self.list_view,
                               translate('MediaPlugin.MediaItem',
                                         'You must select a media file to replace the background with.')):
            item = self.list_view.currentItem()
            filename = item.data(QtCore.Qt.UserRole)
            if os.path.exists(filename):
                service_item = ServiceItem()
                service_item.title = 'webkit'
                service_item.processor = 'webkit'
                (path, name) = os.path.split(filename)
                service_item.add_from_command(path, name, CLAPPERBOARD)
                if self.media_controller.video(DisplayControllerType.Live, service_item, video_behind_text=True):
                    self.reset_action.setVisible(True)
                    self.reset_action_context.setVisible(True)
                else:
                    critical_error_message_box(UiStrings().LiveBGError,
                                               translate('MediaPlugin.MediaItem',
                                                         'There was no display item to amend.'))
            else:
                critical_error_message_box(UiStrings().LiveBGError,
                                           translate('MediaPlugin.MediaItem',
                                                     'There was a problem replacing your background, '
                                                     'the media file "%s" no longer exists.') % filename)

    def generate_slide_data(self, service_item, item=None, xml_version=False, remote=False,
                            context=ServiceItemContext.Service):
        """
        Generate the slide data. Needs to be implemented by the plugin.

        :param service_item: The service item to be built on
        :param item: The Song item to be used
        :param xml_version: The xml version (not used)
        :param remote: Triggered from remote
        :param context: Why is it being generated
        """
        if item is None:
            item = self.list_view.currentItem()
            if item is None:
                return False
        filename = item.data(QtCore.Qt.UserRole)
        # Special handling if the filename is a optical clip
        if filename.startswith('optical:'):
            (name, title, audio_track, subtitle_track, start, end, clip_name) = parse_optical_path(filename)
            if not os.path.exists(name):
                if not remote:
                    # Optical disc is no longer present
                    critical_error_message_box(
                        translate('MediaPlugin.MediaItem', 'Missing Media File'),
                        translate('MediaPlugin.MediaItem', 'The optical disc %s is no longer available.') % name)
                return False
            service_item.processor = self.display_type_combo_box.currentText()
            service_item.add_from_command(filename, name, CLAPPERBOARD)
            service_item.title = clip_name
            # Set the length
            self.media_controller.media_setup_optical(name, title, audio_track, subtitle_track, start, end, None, None)
            service_item.set_media_length((end - start) / 1000)
            service_item.start_time = start / 1000
            service_item.end_time = end / 1000
            service_item.add_capability(ItemCapabilities.IsOptical)
        else:
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
            if not self.media_controller.media_length(service_item):
                return False
        service_item.add_capability(ItemCapabilities.CanAutoStartForLive)
        service_item.add_capability(ItemCapabilities.CanEditTitle)
        service_item.add_capability(ItemCapabilities.RequiresMedia)
        if Settings().value(self.settings_section + '/media auto start') == QtCore.Qt.Checked:
            service_item.will_auto_start = True
        # force a non-existent theme
        service_item.theme = -1
        return True

    def initialise(self):
        """
        Initialize media item.
        """
        self.list_view.clear()
        self.service_path = os.path.join(AppLocation.get_section_data_path(self.settings_section), 'thumbnails')
        check_directory_exists(self.service_path)
        self.load_list(Settings().value(self.settings_section + '/media files'))
        self.rebuild_players()

    def rebuild_players(self):
        """
        Rebuild the tab in the media manager when changes are made in the settings.
        """
        self.populate_display_types()
        self.on_new_file_masks = translate('MediaPlugin.MediaItem', 'Videos (%s);;Audio (%s);;%s (*)') % (
            ' '.join(self.media_controller.video_extensions_list),
            ' '.join(self.media_controller.audio_extensions_list), UiStrings().AllFiles)

    def populate_display_types(self):
        """
        Load the combobox with the enabled media players,  allowing user to select a specific player if settings allow.
        """
        # block signals to avoid unnecessary override_player_changed Signals while combo box creation
        self.display_type_combo_box.blockSignals(True)
        self.display_type_combo_box.clear()
        used_players, override_player = get_media_players()
        media_players = self.media_controller.media_players
        current_index = 0
        for player in used_players:
            # load the drop down selection
            self.display_type_combo_box.addItem(media_players[player].original_name)
            if override_player == player:
                current_index = len(self.display_type_combo_box)
        if self.display_type_combo_box.count() > 1:
            self.display_type_combo_box.insertItem(0, self.automatic)
            self.display_type_combo_box.setCurrentIndex(current_index)
        if override_player:
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
        """
        Load the media list

        :param media: The media
        :param target_group:
        """
        media.sort(key=lambda file_name: get_locale_key(os.path.split(str(file_name))[1]))
        for track in media:
            track_info = QtCore.QFileInfo(track)
            item_name = None
            if track.startswith('optical:'):
                # Handle optical based item
                (file_name, title, audio_track, subtitle_track, start, end, clip_name) = parse_optical_path(track)
                item_name = QtWidgets.QListWidgetItem(clip_name)
                item_name.setIcon(self.optical_icon)
                item_name.setData(QtCore.Qt.UserRole, track)
                item_name.setToolTip('%s@%s-%s' % (file_name, format_milliseconds(start), format_milliseconds(end)))
            elif not os.path.exists(track):
                # File doesn't exist, mark as error.
                file_name = os.path.split(str(track))[1]
                item_name = QtWidgets.QListWidgetItem(file_name)
                item_name.setIcon(self.error_icon)
                item_name.setData(QtCore.Qt.UserRole, track)
                item_name.setToolTip(track)
            elif track_info.isFile():
                # Normal media file handling.
                file_name = os.path.split(str(track))[1]
                item_name = QtWidgets.QListWidgetItem(file_name)
                if '*.%s' % (file_name.split('.')[-1].lower()) in self.media_controller.audio_extensions_list:
                    item_name.setIcon(self.audio_icon)
                else:
                    item_name.setIcon(self.video_icon)
                item_name.setData(QtCore.Qt.UserRole, track)
                item_name.setToolTip(track)
            if item_name:
                self.list_view.addItem(item_name)

    def get_list(self, media_type=MediaType.Audio):
        """
        Get the list of media, optional select media type.

        :param media_type: Type to get, defaults to audio.
        :return: The media list
        """
        media = Settings().value(self.settings_section + '/media files')
        media.sort(key=lambda filename: get_locale_key(os.path.split(str(filename))[1]))
        if media_type == MediaType.Audio:
            extension = self.media_controller.audio_extensions_list
        else:
            extension = self.media_controller.video_extensions_list
        extension = [x[1:] for x in extension]
        media = [x for x in media if os.path.splitext(x)[1] in extension]
        return media

    def search(self, string, show_error):
        """
        Performs a search for items containing ``string``

        :param string: String to be displayed
        :param show_error: Should the error be shown (True)
        :return: The search result.
        """
        files = Settings().value(self.settings_section + '/media files')
        results = []
        string = string.lower()
        for file in files:
            filename = os.path.split(str(file))[1]
            if filename.lower().find(string) > -1:
                results.append([file, filename])
        return results

    def on_load_optical(self):
        """
        When the load optical button is clicked, open the clip selector window.
        """
        # self.media_clip_selector_form.exec()
        if get_vlc():
            media_clip_selector_form = MediaClipSelectorForm(self, self.main_window, None)
            media_clip_selector_form.exec()
            del media_clip_selector_form
        else:
            QtWidgets.QMessageBox.critical(self, 'VLC is not available', 'VLC is not available')

    def add_optical_clip(self, optical):
        """
        Add a optical based clip to the mediamanager, called from media_clip_selector_form.

        :param optical: The clip to add.
        """
        full_list = self.get_file_list()
        # If the clip already is in the media list it isn't added and an error message is displayed.
        if optical in full_list:
            critical_error_message_box(translate('MediaPlugin.MediaItem', 'Mediaclip already saved'),
                                       translate('MediaPlugin.MediaItem', 'This mediaclip has already been saved'))
            return
        # Append the optical string to the media list
        full_list.append(optical)
        self.load_list([optical])
        Settings().setValue(self.settings_section + '/media files', self.get_file_list())
