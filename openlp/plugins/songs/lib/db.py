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
"""
The :mod:`db` module provides the database and schema that is the backend for
the Songs plugin
"""

from sqlalchemy import Column, ForeignKey, Index, Table, types
from sqlalchemy.orm import mapper, relation

from openlp.core.lib.db import BaseModel, init_db

class Author(BaseModel):
    """
    Author model
    """
    pass

class Book(BaseModel):
    """
    Book model
    """
    def __repr__(self):
        return u'<Book id="%s" name="%s" publisher="%s" />' % (
            str(self.id), self.name, self.publisher)

class Song(BaseModel):
    """
    Song model
    """
    pass

class Topic(BaseModel):
    """
    Topic model
    """
    pass

def init_schema(url):
    """
    Setup the songs database connection and initialise the database schema

    ``url``
        The database to setup
    """
    session, metadata = init_db(url, auto_flush=False)

    # Definition of the "authors" table
    authors_table = Table(u'authors', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'first_name', types.Unicode(128)),
        Column(u'last_name', types.Unicode(128)),
        Column(u'display_name', types.Unicode(255), nullable=False)
    )

    # Definition of the "song_books" table
    song_books_table = Table(u'song_books', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'name', types.Unicode(128), nullable=False),
        Column(u'publisher', types.Unicode(128))
    )

    # Definition of the "songs" table
    songs_table = Table(u'songs', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'song_book_id', types.Integer,
            ForeignKey(u'song_books.id'), default=0),
        Column(u'title', types.Unicode(255), nullable=False),
        Column(u'lyrics', types.UnicodeText, nullable=False),
        Column(u'verse_order', types.Unicode(128)),
        Column(u'copyright', types.Unicode(255)),
        Column(u'comments', types.UnicodeText),
        Column(u'ccli_number', types.Unicode(64)),
        Column(u'song_number', types.Unicode(64)),
        Column(u'theme_name', types.Unicode(128)),
        Column(u'search_title', types.Unicode(255), index=True, nullable=False),
        Column(u'search_lyrics', types.UnicodeText, index=True, nullable=False)
    )

    # Definition of the "topics" table
    topics_table = Table(u'topics', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'name', types.Unicode(128), nullable=False)
    )

    # Definition of the "authors_songs" table
    authors_songs_table = Table(u'authors_songs', metadata,
        Column(u'author_id', types.Integer,
            ForeignKey(u'authors.id'), primary_key=True),
        Column(u'song_id', types.Integer,
            ForeignKey(u'songs.id'), primary_key=True)
    )

    # Definition of the "songs_topics" table
    songs_topics_table = Table(u'songs_topics', metadata,
        Column(u'song_id', types.Integer,
            ForeignKey(u'songs.id'), primary_key=True),
        Column(u'topic_id', types.Integer,
            ForeignKey(u'topics.id'), primary_key=True)
    )

    # Define table indexes
    Index(u'authors_id', authors_table.c.id)
    Index(u'authors_display_name_id', authors_table.c.display_name,
        authors_table.c.id)
    Index(u'song_books_id', song_books_table.c.id)
    Index(u'songs_id', songs_table.c.id)
    Index(u'topics_id', topics_table.c.id)
    Index(u'authors_songs_author', authors_songs_table.c.author_id,
        authors_songs_table.c.song_id)
    Index(u'authors_songs_song', authors_songs_table.c.song_id,
        authors_songs_table.c.author_id)
    Index(u'topics_song_topic', songs_topics_table.c.topic_id,
        songs_topics_table.c.song_id)
    Index(u'topics_song_song', songs_topics_table.c.song_id,
        songs_topics_table.c.topic_id)

    mapper(Author, authors_table)
    mapper(Book, song_books_table)
    mapper(Song, songs_table,
        properties={'authors': relation(Author, backref='songs',
            secondary=authors_songs_table),
            'book': relation(Book, backref='songs'),
            'topics': relation(Topic, backref='songs',
            secondary=songs_topics_table)})
    mapper(Topic, topics_table)

    metadata.create_all(checkfirst=True)
    return session