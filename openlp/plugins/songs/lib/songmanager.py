# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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

from sqlalchemy.orm import asc, desc, like
from openlp.plugins.songs.lib.models import init_models, metadata, session, \
    songs_table, Song, Author, Topic

import logging

class SongManager():
    """
    The Song Manager provides a central location for all database code. This
    class takes care of connecting to the database and running all the queries.
    """

    global log
    log=logging.getLogger("SongManager")
    log.info("Song manager loaded")

    def __init__(self, config):
        """
        Creates the connection to the database, and creates the tables if they
        don't exist.
        """
        self.config = config
        log.debug( "Song Initialising")
        self.db_url = u''
        db_type = self.config.get_db_type()
        if db_type == u'sqlite':
            self.db_url = u'sqlite://' + self.config.get_data_path() + \
                u'songs.sqlite'
        else:
            self.db_url = self.config.get_db_type + 'u://' + \
                self.config.get_db_username + u':' + \
                self.config.get_db_password + u'@' + \
                self.config.get_db_hostname + u'/' + \
                self.config.get_db_database
        ini_models(self.db_url)
        if not songs_table.exists():
            metadata.create_all()
        log.debug( "Song Initialised")

    def process_dialog(self, dialogobject):
        self.dialogobject = dialogobject

    def get_songs(self):
        """
        Returns the details of a song
        """
        return session.query(Song).order_by(title).all()

    def search_song_title(self, keywords):
        """
        Searches the song title for keywords.
        """
        return session.query(Song).filter(search_title.like(u'%' + keywords + u'%'))

    def search_song_lyrics(self, keywords):
        """
        Searches the song lyrics for keywords.
        """
        return session.query(Song).filter(search_lyrics.like(u'%' + keywords + u'%'))

    def get_song(self, id):
        """
        Returns the details of a song
        """
        return session.query(Song).get(id)

    def save_song(self, song):
        """
        Saves a song to the database
        """
        try:
            session.add(song)
            session.commit()
            return True
        except:
            return False

    def delete_song(self, song):
        try:
            session.delete(song)
            session.commit()
            return True
        except:
            return False

    def get_authors(self):
        """
        Returns a list of all the authors
        """
        return session.query(Author).order_by(display_name).all()

    def get_author(self, id):
        """
        Details of the Author
        """
        return session.query(Author).get(id)

    def save_author(self, author):
        """
        Save the Author and refresh the cache
        """
        try:
            session.add(author)
            session.commit()
            return True
        except:
            return False

    def delete_author(self, authorid):
        """
        Delete the author and refresh the author cache
        """
        try:
            session.delete(author)
            session.commit()
            return True
        except:
            return False
