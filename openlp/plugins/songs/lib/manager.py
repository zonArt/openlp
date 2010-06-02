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

from PyQt4 import QtCore
from sqlalchemy.exceptions import InvalidRequestError

from openlp.core.utils import AppLocation
from openlp.plugins.songs.lib.models import init_models, metadata, Song, \
    Author, Topic, Book
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


class SongManager(object):
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
        settings = QtCore.QSettings()
        settings.beginGroup(u'songs')
        self.db_url = u''
        db_type = unicode(
            settings.value(u'songs/db type', QtCore.QVariant(u'sqlite')).toString())
        if db_type == u'sqlite':
            self.db_url = u'sqlite:///%s/songs.sqlite' % \
                AppLocation.get_section_data_path(u'songs')
        else:
            self.db_url = u'%s://%s:%s@%s/%s' % (db_type,
                unicode(settings.value(
                    u'db username', QtCore.QVariant(u'')).toString()),
                unicode(settings.value(
                    u'db password', QtCore.QVariant(u'')).toString()),
                unicode(settings.value(
                    u'db hostname', QtCore.QVariant(u'')).toString()),
                unicode(settings.value(
                    u'db database', QtCore.QVariant(u'')).toString()))
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)
        settings.endGroup()
        log.debug(u'Song Initialised')

    def get_songs(self):
        """
        Returns the details of a song
        """
        return self.session.query(Song).order_by(Song.title).all()

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

    def get_song(self, id=None):
        """
        Returns the details of a song
        """
        if id is None:
            return Song()
        else:
            return self.session.query(Song).get(id)

    def save_song(self, song):
        """
        Saves a song to the database
        """
        try:
            self.session.add(song)
            self.session.commit()
            return True
        except InvalidRequestError:
            log.exception(u'Could not save song to song database')
            self.session.rollback()
            return False

    def delete_song(self, songid):
        song = self.get_song(songid)
        try:
            self.session.delete(song)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Could not delete song from song database')
            return False

    def get_authors(self):
        """
        Returns a list of all the authors
        """
        return self.session.query(Author).order_by(Author.display_name).all()

    def get_author(self, id):
        """
        Details of the Author
        """
        return self.session.query(Author).get(id)

    def get_author_by_name(self, name):
        """
        Get author by display name
        """
        return self.session.query(Author).filter_by(display_name=name).first() 

    def save_author(self, author):
        """
        Save the Author and refresh the cache
        """
        try:
            self.session.add(author)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Could not save author to song database')
            return False

    def delete_author(self, authorid):
        """
        Delete the author
        """
        author = self.get_author(authorid)
        try:
            self.session.delete(author)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Could not delete author from song database')
            return False

    def get_topics(self):
        """
        Returns a list of all the topics
        """
        return self.session.query(Topic).order_by(Topic.name).all()

    def get_topic(self, id):
        """
        Details of the Topic
        """
        return self.session.query(Topic).get(id)

    def get_topic_by_name(self, name):
        """
        Get topic by name
        """
        return self.session.query(Topic).filter_by(name=name).first() 

    def save_topic(self, topic):
        """
        Save the Topic
        """
        try:
            self.session.add(topic)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Could not save topic to song database')
            return False

    def delete_topic(self, topicid):
        """
        Delete the topic
        """
        topic = self.get_topic(topicid)
        try:
            self.session.delete(topic)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Could not delete topic from song database')
            return False

    def get_books(self):
        """
        Returns a list of all the Books
        """
        return self.session.query(Book).order_by(Book.name).all()

    def get_book(self, id):
        """
        Details of the Books
        """
        return self.session.query(Book).get(id)

    def get_book_by_name(self, name):
        """
        Get book by name
        """
        return self.session.query(Book).filter_by(name=name).first() 

    def save_book(self, book):
        """
        Save the Book
        """
        try:
            self.session.add(book)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Could not save book to song database')
            return False

    def delete_book(self, bookid):
        """
        Delete the Book
        """
        book = self.get_book(bookid)
        try:
            self.session.delete(book)
            self.session.commit()
            return True
        except InvalidRequestError:
            self.session.rollback()
            log.exception(u'Could not delete book from song database')
            return False

    def get_songs_for_theme(self, theme):
        return self.session.query(Song).filter(Song.theme_name == theme).all()

