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

import logging

from openlp.core.lib.db import Manager
from openlp.plugins.songs.lib.db import init_schema, Song, Author, Topic, Book
#from openlp.plugins.songs.lib import OpenLyricsSong, OpenSongSong, CCLISong, \
#    CSVSong

log = logging.getLogger(__name__)

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


class SongManager(Manager):
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """
    log.info(u'Song manager loaded')

    def __init__(self):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        log.debug(u'Song Initialising')
        Manager.__init__(self, u'songs', init_schema)
        log.debug(u'Song Initialised')

    def search_song_title(self, keywords):
        """
        Searches the song title for keywords.
        """
        return self.session.query(Song).filter(
            Song.search_title.like(u'%' + keywords + u'%')).order_by(
                Song.search_title.asc()).all()

    def search_song_lyrics(self, keywords):
        """
        Searches the song lyrics for keywords.
        """
        return self.session.query(Song).filter(
            Song.search_lyrics.like(u'%' + keywords + u'%')).order_by(
                Song.search_lyrics.asc()).all()

    def get_song_from_author(self, keywords):
        """
        Searches the song authors for keywords.
        """
        return self.session.query(Author).filter(Author.display_name.like(
            u'%' + keywords + u'%')).order_by(Author.display_name.asc()).all()

    def get_author_by_name(self, name):
        """
        Get author by display name
        """
        return self.session.query(Author).filter_by(display_name=name).first() 

    def get_topic_by_name(self, name):
        """
        Get topic by name
        """
        return self.session.query(Topic).filter_by(name=name).first() 

    def get_book_by_name(self, name):
        """
        Get book by name
        """
        return self.session.query(Book).filter_by(name=name).first() 

    def get_songs_for_theme(self, theme):
        return self.session.query(Song).filter(Song.theme_name == theme).all()
