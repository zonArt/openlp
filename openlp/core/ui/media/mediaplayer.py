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
"""
The :mod:`~openlp.core.ui.media.mediaplayer` module contains the MediaPlayer class.
"""
from openlp.core.lib import Registry
from openlp.core.ui.media import MediaState


class MediaPlayer(object):
    """
    This is the base class media Player class to provide OpenLP with a
    pluggable media display framework.
    """

    def __init__(self, parent, name=u'media_player'):
        """
        Constructor
        """
        self.parent = parent
        self.name = name
        self.available = self.check_available()
        self.isActive = False
        self.canBackground = False
        self.canFolder = False
        self.state = MediaState.Off
        self.hasOwnWidget = False
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
        """
        pass

    def load(self, display):
        """
        Load a new media file and check if it is valid
        """
        return True

    def resize(self, display):
        """
        If the main display size or position is changed, the media widgets
        should also resized
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
        Do some ui related stuff (e.g. update the seek slider)
        """
        pass

    def get_media_display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        return u''

    def get_media_display_javascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return u''

    def get_media_display_html(self):
        """
        Add html code to htmlbuilder
        """
        return u''

    def get_info(self):
        """
        Returns Information about the player
        """
        return u''

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)