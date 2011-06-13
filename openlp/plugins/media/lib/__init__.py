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

class MediaAPI(object):
    """
    An enumeration for possible APIs.
    """
    Webkit = 0
    Phonon = 1
    Vlc = 2

class MediaState(object):
    """
    An enumeration for possible States of the Media Player
    (copied partially from Phonon::State)
    """
    Loading = 0
    Stopped = 1
    Playing = 2
    Paused = 4
    Off = 6

class MediaType(object):
    """
    """
    Audio = 0
    Video = 1
    Cd = 3
    Dvd = 4

class MediaInfo(object):
    """
    This class hold the media related infos
    """
    file_info = None
    volume = 100
    isFlash = False
    is_background = False
    length = 0
    start_time = 0
    end_time = 0
    media_type = MediaType()


class MediaAPI(object):
    """
    Specialiced Media API class
    to reflect Features of the related API
    """
    def __init__(self, parent, name=u'MediaApi'):
        self.parent = parent
        self.name = name
        self.available = self.check_available()
        self.isActive = False
        self.canBackground = False
        self.state = MediaState.Off
        self.hasOwnWidget = False
        self.audio_extensions_list = []
        self.video_extensions_list = []

    def check_available(self):
        """
        API is available on this machine
        """
        return False


    def setup(self, display):
        """
        Create the related widgets for the current display
        """
        pass

    def load(self, display):
        """
        Load a new media file and check if it is valid
        """
        return True

    def resize(self, display):
        """
        If the main display size or position is changed,
        the media widgets should also resized
        """
        pass

    def play(self, display):
        """
        Starts playing of current Media File
        """
        pass

    def pause(self, display):
        """
        Pause of current Media File
        """
        pass

    def stop(self, display):
        """
        Stop playing of current Media File
        """
        pass

    def volume(self, display, vol):
        """
        Change volume of current Media File
        """
        pass

    def seek(self, display, seekVal):
        """
        Change playing position of current Media File
        """
        pass

    def reset(self, display):
        """
        Remove the current loaded video
        """
        pass

    def set_visible(self, display, status):
        """
        Show/Hide the media widgets
        """
        pass

    def update_ui(self, display):
        """
        Do some ui related stuff
        (e.g. update the seek slider)
        """
        pass

    @staticmethod
    def is_available():
        """
        Check availability of the related API
        """
        return False

    def get_supported_file_types(self):
        """
        Returns the supported file types for
        Audio
        Video
        Locations
        """
        pass

    def display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        return u''


    def display_javascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return u''


    def display_html(self):
        """
        Add html code to htmlbuilder
        """
        return u''

from mediaitem import MediaMediaItem
from mediatab import MediaTab
from mediamanager import MediaManager

__all__ = ['MediaMediaItem']
