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
"""
The :mod:`~openlp.core.ui.media.mediaplayer` module contains the MediaPlayer class.
"""
from openlp.core.common import RegistryProperties
from openlp.core.ui.media import MediaState


class MediaPlayer(RegistryProperties):
    """
    This is the base class media Player class to provide OpenLP with a pluggable media display framework.
    """

    def __init__(self, parent, name='media_player'):
        """
        Constructor
        """
        self.parent = parent
        self.name = name
        self.available = self.check_available()
        self.is_active = False
        self.can_background = False
        self.can_folder = False
        self.state = {0: MediaState.Off, 1: MediaState.Off}
        self.has_own_widget = False
        self.audio_extensions_list = []
        self.video_extensions_list = []

    def check_available(self):
        """
        Player is available on this machine
        """
        return False

    def setup(self, display):
        """
        Create the related widgets for the current display

        :param display: The display to be updated.
        """
        pass

    def load(self, display):
        """
        Load a new media file and check if it is valid

        :param display: The display to be updated.
        """
        return True

    def resize(self, display):
        """
        If the main display size or position is changed, the media widgets
        should also resized

        :param display: The display to be updated.
        """
        pass

    def play(self, display):
        """
        Starts playing of current Media File

        :param display: The display to be updated.
        """
        pass

    def pause(self, display):
        """
        Pause of current Media File

        :param display: The display to be updated.
        """
        pass

    def stop(self, display):
        """
        Stop playing of current Media File

        :param display: The display to be updated.
        """
        pass

    def volume(self, display, volume):
        """
        Change volume of current Media File

        :param display: The display to be updated.
        :param volume: The volume to set.
        """
        pass

    def seek(self, display, seek_value):
        """
        Change playing position of current Media File

        :param display: The display to be updated.
        :param seek_value: The where to seek to.
        """
        pass

    def reset(self, display):
        """
        Remove the current loaded video

        :param display: The display to be updated.
        """
        pass

    def set_visible(self, display, status):
        """
        Show/Hide the media widgets

        :param display: The display to be updated.
        :param status: The status to be set.
        """
        pass

    def update_ui(self, display):
        """
        Do some ui related stuff (e.g. update the seek slider)

        :param display: The display to be updated.
        """
        pass

    def get_media_display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        return ''

    def get_media_display_javascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return ''

    def get_media_display_html(self):
        """
        Add html code to htmlbuilder
        """
        return ''

    def get_info(self):
        """
        Returns Information about the player
        """
        return ''

    def get_live_state(self):
        """
        Get the state of the live player
        :return: Live state
        """
        return self.state[0]

    def set_live_state(self, state):
        """
        Set the State of the Live player
        :param state: State to be set
        :return: None
        """
        self.state[0] = state

    def get_preview_state(self):
        """
        Get the state of the preview player
        :return: Preview State
        """
        return self.state[1]

    def set_preview_state(self, state):
        """
        Set the state of the Preview Player
        :param state: State to be set
        :return: None
        """
        self.state[1] = state

    def set_state(self, state, display):
        """
        Set the State based on the display being processed
        :param state: State to be set
        :param display: Identify the Display type
        :return: None
        """
        if display.controller.is_live:
            self.set_live_state(state)
        else:
            self.set_preview_state(state)
