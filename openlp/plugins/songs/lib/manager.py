# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.plugins.songs.lib.models import init_models, metadata, Song, \
    Author, Topic, Book

class SongManager():
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """

    global log
    log = logging.getLogger(u'SongManager')
    log.info(u'Song manager loaded')

    def __init__(self, config):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        self.config = config
        log.debug(u'Song Initialising')
        self.db_url = u''
        db_type = self.config.get_config(u'db type', u'sqlite')
        if db_type == u'sqlite':
            self.db_url = u'sqlite:///%s/songs.sqlite' % \
                self.config.get_data_path()
        else:
            self.db_url = db_type + 'u://' + \
                self.config.get_config(u'db username') + u':' + \
                self.config.get_config(u'db password') + u'@' + \
                self.config.get_config(u'db hostname') + u'/' + \
                self.config.get_config(u'db database')
        self.session = init_models(self.db_url)
        metadata.create_all(checkfirst=True)
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
        except:
            self.session.rollback()
            log.exception(u'Could not save song to song database')
            return False

    def delete_song(self, songid):
        song = self.get_song(songid)
        try:
            self.session.delete(song)
            self.session.commit()
            return True
        except:
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

    def save_author(self, author):
        """
        Save the Author and refresh the cache
        """
        try:
            self.session.add(author)
            self.session.commit()
            return True
        except:
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
        except:
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

    def save_topic(self, topic):
        """
        Save the Topic
        """
        try:
            self.session.add(topic)
            self.session.commit()
            return True
        except:
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
        except:
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

    def save_book(self, book):
        """
        Save the Book
        """
        try:
            self.session.add(book)
            self.session.commit()
            return True
        except:
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
        except:
            self.session.rollback()
            log.exception(u'Could not delete book from song database')
            return False

