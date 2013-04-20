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
The :mod:`~openlp.core.ui.media` module contains classes and objects for media player integration.
"""
import logging

from openlp.core.lib import Settings

from PyQt4 import QtCore

log = logging.getLogger(__name__)


class MediaState(object):
    """
    An enumeration for possible States of the Media Player
    """
    Off = 0
    Loaded = 1
    Playing = 2
    Paused = 3
    Stopped = 4


class MediaType(object):
    """
    An enumeration of possible Media Types
    """
    Unused = 0
    Audio = 1
    Video = 2
    CD = 3
    DVD = 4
    Folder = 5


class MediaInfo(object):
    """
    This class hold the media related info
    """
    file_info = None
    volume = 100
    is_flash = False
    is_background = False
    length = 0
    start_time = 0
    end_time = 0
    media_type = MediaType()


def get_media_players():
    """
    This method extracts the configured media players and overridden player
    from the settings.
    """
    log.debug(u'get_media_players')
    saved_players = Settings().value(u'media/players')
    reg_ex = QtCore.QRegExp(".*\[(.*)\].*")
    if Settings().value(u'media/override player') == QtCore.Qt.Checked:
        if reg_ex.exactMatch(saved_players):
            overridden_player = u'%s' % reg_ex.cap(1)
        else:
            overridden_player = u'auto'
    else:
        overridden_player = u''
    saved_players_list = saved_players.replace(u'[', u'').replace(u']', u'').split(u',')
    return saved_players_list, overridden_player


def set_media_players(players_list, overridden_player=u'auto'):
    """
    This method saves the configured media players and overridden player to the
    settings

    ``players_list``
        A list with all active media players.

    ``overridden_player``
        Here an special media player is chosen for all media actions.
    """
    log.debug(u'set_media_players')
    players = u','.join(players_list)
    if Settings().value(u'media/override player') == QtCore.Qt.Checked and overridden_player != u'auto':
        players = players.replace(overridden_player, u'[%s]' % overridden_player)
    Settings().setValue(u'media/players', players)

from mediacontroller import MediaController
from playertab import PlayerTab

__all__ = [u'MediaController', u'PlayerTab']
