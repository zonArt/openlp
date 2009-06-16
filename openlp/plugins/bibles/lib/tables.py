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
from sqlalchemy import  *
from sqlalchemy import Column, Table, MetaData, ForeignKey, schema

metadata = MetaData()
#Define the tables and indexes
meta_table = Table(u'metadata', metadata, 
    Column(u'key', String(255), primary_key=True), 
    Column(u'value', String(255)), 
)

testament_table = Table(u'testament', metadata, 
    Column(u'id', Integer, primary_key=True), 
    Column(u'name', String(30)), 
)
   
book_table = Table(u'book', metadata, 
    Column(u'id', Integer, primary_key=True), 
    Column(u'testament_id', Integer, schema.ForeignKey(u'testament.id')), 
    Column(u'name', String(30)), 
    Column(u'abbreviation', String(5)), 
)
Index(u'idx_name', book_table.c.name, book_table.c.id)
Index(u'idx_abbrev', book_table.c.abbreviation, book_table.c.id)

verse_table = Table(u'verse', metadata, 
   Column(u'id', Integer, primary_key=True), 
    Column(u'book_id', Integer , schema.ForeignKey(u'book.id')), 
    Column(u'chapter', Integer), 
    Column(u'verse', Integer), 
    Column(u'text', Text), 
)
Index(u'idx_chapter_verse_book', verse_table.c.chapter, verse_table.c.verse, verse_table.c.book_id, verse_table.c.id)
Index(u'idx_chapter_verse_text', verse_table.c.text, verse_table.c.verse, verse_table.c.book_id, verse_table.c.id)