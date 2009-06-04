# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

import os, os.path
import sys

from sqlalchemy import asc, desc
from openlp.plugins.songs.lib.models import init_models, metadata, session, \
    engine, songs_table, Song, Author, Topic

import logging

class SongManager():
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """

    global log
    log = logging.getLogger('SongManager')
    log.info('Song manager loaded')

    def __init__(self, config):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        self.config = config
        log.debug('Song Initialising')
        self.db_url = u''
        db_type = self.config.get_config(u'db type', u'sqlite')
        if db_type == u'sqlite':
            self.db_url = u'sqlite:///' + self.config.get_data_path() + \
                u'/songs.sqlite'
        else:
            self.db_url = db_type + 'u://' + \
                self.config.get_config(u'db username') + u':' + \
                self.config.get_config(u'db password') + u'@' + \
                self.config.get_config(u'db hostname') + u'/' + \
                self.config.get_config(u'db database')
        self.session = init_models(self.db_url)
        if not songs_table.exists():
            metadata.create_all()
        log.debug('Song Initialised')

    def process_dialog(self, dialogobject):
        self.dialogobject = dialogobject

    def get_songs(self):
        """
        Returns the details of a song
        """
        return self.session.query(Song).order_by(title).all()

    def search_song_title(self, keywords):
        """
        Searches the song title for keywords.
        """
        return self.session.query(Song).filter(Song.search_title.like(u'%' + keywords + u'%')).order_by(Song.search_title.asc()).all()

    def search_song_lyrics(self, keywords):
        """
        Searches the song lyrics for keywords.
        """
        return self.session.query(Song).filter(Song.search_lyrics.like(u'%' + keywords + u'%')).order_by(Song.search_lyrics.asc()).all()

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
            return False

    def delete_song(self, song):
        try:
            self.session.delete(song)
            self.session.commit()
            return True
        except:
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
            log.error("Errow thrown %s", sys.exc_info()[1])
            print "Errow thrown ", sys.exc_info()[1]
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
            log.error("Errow thrown %s", sys.exc_info()[1])
            print "Errow thrown ", sys.exc_info()[1]
            return False
