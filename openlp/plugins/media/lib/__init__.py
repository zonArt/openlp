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

from mediaitem import MediaMediaItem
from mediatab import MediaTab
from mediaapi import MediaAPI
from mediamanager import MediaManager

__all__ = ['MediaMediaItem']
