# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from openlp.core.lib import translate

#from openlp.plugins.songs.lib import OpenLyricsSong, OpenSongSong, CCLISong, \
#    CSVSong

class SongFormat(object):
    """
    This is a special enumeration class that holds the various types of songs,
    plus a few helper functions to facilitate generic handling of song types
    for importing.
    """
    Unknown = -1
    OpenLyrics = 0
    OpenSong = 1
    CCLI = 2
    CSV = 3

    @staticmethod
    def get_class(id):
        """
        Return the appropriate imeplementation class.

        ``id``
            The song format.
        """
#        if id == SongFormat.OpenLyrics:
#            return OpenLyricsSong
#        elif id == SongFormat.OpenSong:
#            return OpenSongSong
#        elif id == SongFormat.CCLI:
#            return CCLISong
#        elif id == SongFormat.CSV:
#            return CSVSong
#        else:
        return None

    @staticmethod
    def list():
        """
        Return a list of the supported song formats.
        """
        return [
            SongFormat.OpenLyrics,
            SongFormat.OpenSong,
            SongFormat.CCLI,
            SongFormat.CSV
        ]

class VerseType(object):
    """
    VerseType provides an enumeration for the tags that may be associated
    with verses in songs.
    """
    Verse = 0
    Chorus = 1
    Bridge = 2
    PreChorus = 3
    Intro = 4
    Ending = 5
    Other = 6

    @staticmethod
    def to_string(verse_type):
        """
        Return a string for a given VerseType

        ``verse_type``
            The type to return a string for
        """
        if verse_type == VerseType.Verse:
            return translate('VerseType', 'Verse')
        elif verse_type == VerseType.Chorus:
            return translate('VerseType', 'Chorus')
        elif verse_type == VerseType.Bridge:
            return translate('VerseType', 'Bridge')
        elif verse_type == VerseType.PreChorus:
            return translate('VerseType', 'Pre-Chorus')
        elif verse_type == VerseType.Intro:
            return translate('VerseType', 'Intro')
        elif verse_type == VerseType.Ending:
            return translate('VerseType', 'Ending')
        elif verse_type == VerseType.Other:
            return translate('VerseType', 'Other')

    @staticmethod
    def from_string(verse_type):
        """
        Return the VerseType for a given string

        ``verse_type``
            The string to return a VerseType for
        """
        verse_type = verse_type.lower()
        if verse_type == unicode(VerseType.to_string(VerseType.Verse)).lower():
            return VerseType.Verse
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Chorus)).lower():
            return VerseType.Chorus
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Bridge)).lower():
            return VerseType.Bridge
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.PreChorus)).lower():
            return VerseType.PreChorus
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Intro)).lower():
            return VerseType.Intro
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Ending)).lower():
            return VerseType.Ending
        elif verse_type == \
            unicode(VerseType.to_string(VerseType.Other)).lower():
            return VerseType.Other

from songstab import SongsTab
from mediaitem import SongMediaItem
from songimport import SongImport
try:
    from sofimport import SofImport
    from oooimport import OooImport
except ImportError:
    pass

