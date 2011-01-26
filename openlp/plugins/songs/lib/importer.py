# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
from opensongimport import OpenSongImport
from easislidesimport import EasiSlidesImport
from olpimport import OpenLPSongImport
from openlyricsimport import OpenLyricsImport
from wowimport import WowImport
from cclifileimport import CCLIFileImport
from ewimport import EasyWorshipSongImport
from songbeamerimport import SongBeamerImport
# Imports that might fail
try:
    from olp1import import OpenLP1SongImport
    HAS_OPENLP1 = True
except ImportError:
    HAS_OPENLP1 = False
try:
    from sofimport import SofImport
    HAS_SOF = True
except ImportError:
    HAS_SOF = False
try:
    from oooimport import OooImport
    HAS_OOO = True
except ImportError:
    HAS_OOO = False

class SongFormat(object):
    """
    This is a special enumeration class that holds the various types of songs,
    plus a few helper functions to facilitate generic handling of song types
    for importing.
    """
    _format_availability = {}
    Unknown = -1
    OpenLP2 = 0
    OpenLP1 = 1
    OpenLyrics = 2
    OpenSong = 3
    WordsOfWorship = 4
    CCLI = 5
    SongsOfFellowship = 6
    Generic = 7
    #CSV = 8
    EasiSlides = 8
    EasyWorship = 9
    SongBeamer = 10

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
        return None

    @staticmethod
    def get_formats_list():
        """
        Return a list of the supported song formats.
        """
        return [
            SongFormat.OpenLP2,
            SongFormat.OpenLP1,
            SongFormat.OpenLyrics,
            SongFormat.OpenSong,
            SongFormat.WordsOfWorship,
            SongFormat.CCLI,
            SongFormat.SongsOfFellowship,
            SongFormat.Generic,
            SongFormat.EasiSlides,
            SongFormat.EasyWorship,
            SongFormat.SongBeamer
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

