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
The :mod:`db` module provides the database and schema that is the backend for
the Songs plugin
"""

import re

from sqlalchemy import Column, ForeignKey, Table, types
from sqlalchemy.orm import mapper, relation, reconstructor
from sqlalchemy.sql.expression import func

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
        return u'<Book id="%s" name="%s" publisher="%s" />' % (str(self.id), self.name, self.publisher)


class MediaFile(BaseModel):
    """
    MediaFile model
    """
    pass


class Song(BaseModel):
    """
    Song model
    """
    def __init__(self):
        self.sort_key = ()

    def _try_int(self, s):
        """
        Convert to integer if possible.
        """
        try:
            return int(s)
        except:
            return s.lower()

    def _natsort_key(self, s):
        """
        Used internally to get a tuple by which s is sorted.
        """
        return map(self._try_int, re.findall(r'(\d+|\D+)', s))

    # This decorator tells sqlalchemy to call this method everytime
    # any data on this object is updated.

    @reconstructor
    def init_on_load(self):
        """
        Precompute a tuple to be used for sorting.

        Song sorting is performance sensitive operation.
        To get maximum speed lets precompute the string
        used for comparison.
        """
        # Avoid the overhead of converting string to lowercase and to QString
        # with every call to sort().
        self.sort_key = self._natsort_key(self.title)


class Topic(BaseModel):
    """
    Topic model
    """
    pass

def init_schema(url):
    """
    Setup the songs database connection and initialise the database schema.

    ``url``
        The database to setup

    The song database contains the following tables:

        * authors
        * authors_songs
        * media_files
        * media_files_songs
        * song_books
        * songs
        * songs_topics
        * topics

    **authors** Table
        This table holds the names of all the authors. It has the following
        columns:

        * id
        * first_name
        * last_name
        * display_name

    **authors_songs Table**
        This is a bridging table between the *authors* and *songs* tables, which
        serves to create a many-to-many relationship between the two tables. It
        has the following columns:

        * author_id
        * song_id

    **media_files Table**
        * id
        * file_name
        * type

    **song_books Table**
        The *song_books* table holds a list of books that a congregation gets
        their songs from, or old hymnals now no longer used. This table has the
        following columns:

        * id
        * name
        * publisher

    **songs Table**
        This table contains the songs, and each song has a list of attributes.
        The *songs* table has the following columns:

        * id
        * song_book_id
        * title
        * alternate_title
        * lyrics
        * verse_order
        * copyright
        * comments
        * ccli_number
        * song_number
        * theme_name
        * search_title
        * search_lyrics

    **songs_topics Table**
        This is a bridging table between the *songs* and *topics* tables, which
        serves to create a many-to-many relationship between the two tables. It
        has the following columns:

        * song_id
        * topic_id

    **topics Table**
        The topics table holds a selection of topics that songs can cover. This
        is useful when a worship leader wants to select songs with a certain
        theme. This table has the following columns:

        * id
        * name
    """
    session, metadata = init_db(url)

    # Definition of the "authors" table
    authors_table = Table(u'authors', metadata,
        Column(u'id', types.Integer(), primary_key=True),
        Column(u'first_name', types.Unicode(128)),
        Column(u'last_name', types.Unicode(128)),
        Column(u'display_name', types.Unicode(255), index=True, nullable=False)
    )

    # Definition of the "media_files" table
    media_files_table = Table(u'media_files', metadata,
        Column(u'id', types.Integer(), primary_key=True),
        Column(u'song_id', types.Integer(), ForeignKey(u'songs.id'),
            default=None),
        Column(u'file_name', types.Unicode(255), nullable=False),
        Column(u'type', types.Unicode(64), nullable=False, default=u'audio'),
        Column(u'weight', types.Integer(), default=0)
    )

    # Definition of the "song_books" table
    song_books_table = Table(u'song_books', metadata,
        Column(u'id', types.Integer(), primary_key=True),
        Column(u'name', types.Unicode(128), nullable=False),
        Column(u'publisher', types.Unicode(128))
    )

    # Definition of the "songs" table
    songs_table = Table(u'songs', metadata,
        Column(u'id', types.Integer(), primary_key=True),
        Column(u'song_book_id', types.Integer(),
            ForeignKey(u'song_books.id'), default=None),
        Column(u'title', types.Unicode(255), nullable=False),
        Column(u'alternate_title', types.Unicode(255)),
        Column(u'lyrics', types.UnicodeText, nullable=False),
        Column(u'verse_order', types.Unicode(128)),
        Column(u'copyright', types.Unicode(255)),
        Column(u'comments', types.UnicodeText),
        Column(u'ccli_number', types.Unicode(64)),
        Column(u'song_number', types.Unicode(64)),
        Column(u'theme_name', types.Unicode(128)),
        Column(u'search_title', types.Unicode(255), index=True, nullable=False),
        Column(u'search_lyrics', types.UnicodeText, nullable=False),
        Column(u'create_date', types.DateTime(), default=func.now()),
        Column(u'last_modified', types.DateTime(), default=func.now(),
            onupdate=func.now()),
        Column(u'temporary', types.Boolean(), default=False)
    )

    # Definition of the "topics" table
    topics_table = Table(u'topics', metadata,
        Column(u'id', types.Integer(), primary_key=True),
        Column(u'name', types.Unicode(128), index=True, nullable=False)
    )

    # Definition of the "authors_songs" table
    authors_songs_table = Table(u'authors_songs', metadata,
        Column(u'author_id', types.Integer(),
            ForeignKey(u'authors.id'), primary_key=True),
        Column(u'song_id', types.Integer(),
            ForeignKey(u'songs.id'), primary_key=True)
    )

    # Definition of the "songs_topics" table
    songs_topics_table = Table(u'songs_topics', metadata,
        Column(u'song_id', types.Integer(),
            ForeignKey(u'songs.id'), primary_key=True),
        Column(u'topic_id', types.Integer(),
            ForeignKey(u'topics.id'), primary_key=True)
    )

    mapper(Author, authors_table)
    mapper(Book, song_books_table)
    mapper(MediaFile, media_files_table)
    mapper(Song, songs_table,
        properties={
            'authors': relation(Author, backref='songs',
                secondary=authors_songs_table, lazy=False),
            'book': relation(Book, backref='songs'),
            'media_files': relation(MediaFile, backref='songs',
                order_by=media_files_table.c.weight),
            'topics': relation(Topic, backref='songs',
                secondary=songs_topics_table)
        })
    mapper(Topic, topics_table)

    metadata.create_all(checkfirst=True)
    return session
