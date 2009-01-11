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
from sqlalchemy.orm import mapper, relation
from openlp.plugins.songs.lib.tables import *

class BaseModel(object):
    """
    BaseModel provides a base object with a set of generic functions
    """

    @classmethod
    def populate(cls, **kwargs):
        """
        Creates an instance of a class and populates it, returning the instance
        """
        me = cls()
        keys = kwargs.keys()
        for key in keys:
            me.__setattr__(key, kwargs[key])
        return me

class Author(BaseModel):
    """
    Author model
    """
    pass

class Book(BaseModel):
    """
    Book model
    """
    pass

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


mapper(Author, authors_table)
mapper(Book, song_books_table)
mapper(Song, songs_table,
       properties={'authors': relation(Author, backref='songs',
                                       secondary=authors_songs_table),
                   'book': relation(Book, backref='songs'),
                   'topics': relation(Topic, backref='songs',
                                      secondary=songs_topics_table)})
mapper(Topic, topics_table)   
