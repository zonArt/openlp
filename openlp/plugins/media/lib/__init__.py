# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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

class MediaBackends(object):
    """
    An enumeration for possible Backends.
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

class MediaController(object):
    """
    Specialiced MediaController class
    to reflect Features of the related backend
    """
    def __init__(self, parent):
        self.parent = parent
        self.isActive = False
        self.canBackground = False
        self.state = MediaState.Off
        self.hasOwnWidget = False
        self.audio_extensions_list = []
        self.video_extensions_list = []

    def setup(self, display, hasAudio):
        """
        Create the related widgets for the current display
        """
        pass

    def load(self, display, path, volume):
        """
        Load a new media file and check if it is valid
        """
        return True

    def resize(self, display, controller):
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

    def update_ui(self, controller, display):
        """
        Do some ui related stuff
        (e.g. update the seek slider)
        """
        pass

    @staticmethod
    def is_available():
        """
        Check availability of the related backend
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

from mediaitem import MediaMediaItem
from mediatab import MediaTab
from mediacontroller import MediaManager

__all__ = ['MediaMediaItem']
