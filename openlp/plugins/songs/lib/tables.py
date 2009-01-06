# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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

from sqlalchemy import Column, Table, MetaData, ForeignKey, types

metadata = MetaData()

# Definition of the "authors" table
authors_table = Table('authors', metadata,
    Column('id', types.Integer,  primary_key=True),
    Column('first_name', types.Unicode(128)),
    Column('last_name', types.Unicode(128)),
    Column('display_name', types.Unicode(255), nullable=False)
)

# Definition of the "song_books" table
song_books_table = Table('song_books', metadata,
    Column('id', types.Integer,  primary_key=True),
    Column('name', types.Unicode(128), nullable=False),
    Column('publisher', types.Unicode(128))
)

# Definition of the "songs" table
songs_table = Table('songs', metadata,
    Column('id', types.Integer(), primary_key=True),
    Column('song_book_id', types.Integer, ForeignKey('song_books.id'), default=0),
    Column('title', types.Unicode(255), nullable=False),
    Column('lyrics', types.UnicodeText, nullable=False),
    Column('verse_order', types.Unicode(128)),
    Column('copyright', types.Unicode(255)),
    Column('comments', types.UnicodeText),
    Column('ccli_number', types.Unicode(64)),
    Column('song_number', types.Unicode(64)),
    Column('theme_name', types.Unicode(128)),
    Column('search_title', types.Unicode(255), index=True, nullable=False),
    Column('search_lyrics', types.UnicodeText, index=True, nullable=False)
)

# Definition of the "topics" table
topics_table = Table('topics', metadata,
    Column('id', types.Integer,  primary_key=True),
    Column('name', types.Unicode(128), nullable=False)
)

# Definition of the "authors_songs" table
authors_songs_table = Table('authors_songs', metadata,
    Column('author_id', types.Integer, ForeignKey('authors.id'), primary_key=True),
    Column('song_id', types.Integer, ForeignKey('songs.id'), primary_key=True)
)

# Definition of the "songs_topics" table
songs_topics_table = Table('songs_topics', metadata,
    Column('song_id', types.Integer, ForeignKey('songs.id'), primary_key=True),
    Column('topic_id', types.Integer, ForeignKey('topics.id'), primary_key=True)
)
