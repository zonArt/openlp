# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection

Copyright (c) 2008 Raoul Snyman

Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley

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
import string

from sqlalchemy import Column, Table, MetaData, ForeignKey, types, \
    create_engine
from sqlalchemy.orm import mapper, relation, sessionmaker, scoped_session

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


class BibleMeta(BaseModel):
    """
    Bible Meta Data
    """
    pass


class ONTestament(BaseModel):
    """
    Bible Testaments
    """
    pass


class Book(BaseModel):
    """
    Song model
    """
    pass


class Verse(BaseModel):
    """
    Topic model
    """
    pass


def init_models(db_url):
    engine = create_engine(db_url)
    metadata.bind = engine
    session = scoped_session(sessionmaker(autoflush=True,
                                          autocommit=False,
                                          bind=engine))
    # Don't think this is needed...
    #metadata.bind.echo = False
    #Define the tables and indexes
    return metadata, session


metadata = MetaData()
meta_table = Table(u'metadata', metadata,
    Column(u'key', types.Unicode(255), primary_key=True, index=True),
    Column(u'value', types.Unicode(255)),
)
testament_table = Table(u'testament', metadata,
    Column(u'id', types.Integer, primary_key=True),
    Column(u'name', types.Unicode(50)),
)
book_table = Table(u'book', metadata,
    Column(u'id', types.Integer, primary_key=True),
    Column(u'testament_id', types.Integer, ForeignKey(u'testament.id')),
    Column(u'name', types.Unicode(50), index=True),
    Column(u'abbreviation', types.Unicode(5), index=True),
)
verse_table = Table(u'verse', metadata,
   Column(u'id', types.Integer, primary_key=True, index=True),
    Column(u'book_id', types.Integer, ForeignKey(u'book.id'), index=True),
    Column(u'chapter', types.Integer, index=True),
    Column(u'verse', types.Integer, index=True),
    Column(u'text', types.UnicodeText, index=True),
)
mapper(BibleMeta, meta_table)
mapper(ONTestament, testament_table,
    properties={'books': relation(Book, backref='testament')})
mapper(Book, book_table,
    properties={'verses': relation(Verse, backref='book')})
mapper(Verse, verse_table)
