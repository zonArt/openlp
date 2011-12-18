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
"""
The :mod:`importer` modules provides the general song import functionality.
"""
import logging

from opensongimport import OpenSongImport
from easislidesimport import EasiSlidesImport
from olpimport import OpenLPSongImport
from openlyricsimport import OpenLyricsImport
from wowimport import WowImport
from cclifileimport import CCLIFileImport
from ewimport import EasyWorshipSongImport
from songbeamerimport import SongBeamerImport
from songshowplusimport import SongShowPlusImport
from foilpresenterimport import FoilPresenterImport
# Imports that might fail
log = logging.getLogger(__name__)
try:
    from olp1import import OpenLP1SongImport
    HAS_OPENLP1 = True
except ImportError:
    log.exception('Error importing %s', 'OpenLP1SongImport')
    HAS_OPENLP1 = False
try:
    from sofimport import SofImport
    HAS_SOF = True
except ImportError:
    log.exception('Error importing %s', 'SofImport')
    HAS_SOF = False
try:
    from oooimport import OooImport
    HAS_OOO = True
except ImportError:
    log.exception('Error importing %s', 'OooImport')
    HAS_OOO = False

class SongFormat(object):
    """
    This is a special enumeration class that holds the various types of songs,
    plus a few helper functions to facilitate generic handling of song types
    for importing.
    """
    _format_availability = {}
    Unknown = -1
    OpenLyrics = 0
    OpenLP2 = 1
    OpenLP1 = 2
    Generic = 3
    CCLI = 4
    EasiSlides = 5
    EasyWorship = 6
    FoilPresenter = 7
    OpenSong = 8
    SongBeamer = 9
    SongShowPlus = 10
    SongsOfFellowship = 11
    WordsOfWorship = 12
    #CSV = 13

    @staticmethod
    def get_class(format):
        """
        Return the appropriate imeplementation class.

        ``format``
            The song format.
        """
        if format == SongFormat.OpenLP2:
            return OpenLPSongImport
        elif format == SongFormat.OpenLP1:
            return OpenLP1SongImport
        elif format == SongFormat.OpenLyrics:
            return OpenLyricsImport
        elif format == SongFormat.OpenSong:
            return OpenSongImport
        elif format == SongFormat.SongsOfFellowship:
            return SofImport
        elif format == SongFormat.WordsOfWorship:
            return WowImport
        elif format == SongFormat.Generic:
            return OooImport
        elif format == SongFormat.CCLI:
            return CCLIFileImport
        elif format == SongFormat.EasiSlides:
            return EasiSlidesImport
        elif format == SongFormat.EasyWorship:
            return EasyWorshipSongImport
        elif format == SongFormat.SongBeamer:
            return SongBeamerImport
        elif format == SongFormat.SongShowPlus:
            return SongShowPlusImport
        elif format == SongFormat.FoilPresenter:
            return FoilPresenterImport
        return None

    @staticmethod
    def get_formats_list():
        """
        Return a list of the supported song formats.
        """
        return [
            SongFormat.OpenLyrics,
            SongFormat.OpenLP2,
            SongFormat.OpenLP1,
            SongFormat.Generic,
            SongFormat.CCLI,
            SongFormat.EasiSlides,
            SongFormat.EasyWorship,            
            SongFormat.FoilPresenter,
            SongFormat.OpenSong,
            SongFormat.SongBeamer,
            SongFormat.SongShowPlus,
            SongFormat.SongsOfFellowship,
            SongFormat.WordsOfWorship
        ]

    @staticmethod
    def set_availability(format, available):
        """
        Set the availability for a given song format.
        """
        SongFormat._format_availability[format] = available

    @staticmethod
    def get_availability(format):
        """
        Return the availability of a given song format.
        """
        return SongFormat._format_availability.get(format, True)

SongFormat.set_availability(SongFormat.OpenLP1, HAS_OPENLP1)
SongFormat.set_availability(SongFormat.SongsOfFellowship, HAS_SOF)
SongFormat.set_availability(SongFormat.Generic, HAS_OOO)

__all__ = [u'SongFormat']

