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
import time
import datetime
import logging
import string

from sqlalchemy import  *
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, mapper

from openlp.plugins.bibles.lib.biblecommon import BibleCommon
from openlp.core.utils import ConfigHelper

import logging

class SongDBException(Exception):
    pass
class SongInvalidDatabaseError(Exception):
    pass
    
metadata = MetaData()

author_table = Table('authors', metadata, 
    Column('authorid', Integer, primary_key=True), 
    Column('authorname', String(40)), 
    Column('first_name', String(40)), 
    Column('last_name', String(40)),     
)

class Author(object):
    def __init__(self, authorname, first_name, last_name):
        #self.authorid = authorid
        self.authorname =authorname
        self.first_name =first_name
        self.last_name =last_name                
        
    def __repr__(self):
        return "<authormeta(%s,%s,%s)>" , self.authorname, self.first_name, self.last_name
     
mapper(Author,author_table)
  
class SongDBImpl(BibleCommon):
    global log     
    log=logging.getLogger("SongDBImpl")
    log.info("SongDBImpl loaded")   
    def __init__(self, songpath , suffix, btype = 'sqlite'):   
        # Connect to database 
        self.songfile = os.path.join(songpath, "songs."+suffix)
        log.debug( "Load Song on path %s", self.songfile)

        if btype == 'sqlite': 
            self.db = create_engine("sqlite:///"+self.songfile, convert_unicode=True)
        elif btype == 'mysql': 
            self.db = create_engine("mysql://tim:@192.168.0.100:3306/openlp_rsv_bible")
        else:
            raise BibleInvalidDatabaseError("Database not mysql or sqlite")
        self.db.echo = True
        self.db.convert_unicode=False
        metadata.bind = self.db
        metadata.bind.echo = False
        self.Session = sessionmaker(autoflush=True, autocommit=False)
        self.Session.configure(bind=self.db)
        #self.authors_table = Table('authors', metadata, autoload=True)
        #self.settings = Table('settings', metadata, autoload=True)
        #self.songauthors = Table('songauthors', metadata, autoload=True)
        #self.songs = Table('songs', metadata, autoload=True)        
        
    def create_tables(self):
        log.debug( "createTables")        
        if os.path.exists(self.biblefile):   # delete bible file and set it up again
            os.remove(self.biblefile)
        meta_table.create()
        testament_table.create()
        book_table.create()
        verse_table.create()
        self.save_meta("dbversion", "2")
        self._loadTestaments()
        
    def add_author(self, author_name, first_name,  last_name):
        log.debug( "add_author %s,%s,%s", author_name, first_name, last_name)
        metadata.bind.echo = True
        session = self.Session()
        authorsmeta = Author(authorname=author_name, first_name=first_name,last_name=last_name)
        session.add(authorsmeta)
        session.commit()
      
    def save_meta(self, key, value):
        metadata.bind.echo = False                
        session = self.Session()
        bmeta= BibleMeta(key, value)
        session.add(bmeta)
        session.commit()

    def get_meta(self, key):
        s = text (""" select value FROM metadata where key == :k """)
        return self.db.execute(s, k=key).fetchone()

    def delete_meta(self, key):
        metadata.bind.echo = False
        s = text (""" delete FROM meta where key == :k """)
        self.db.execute(s, k=key)

    def get_song(self, songid):
        log.debug( "get_song ") 
        metadata.bind.echo = True
        s = text (""" select * FROM songs where songid = :c """)
        return self.db.execute(s, c=songid).fetchone()
        
    def get_authors(self):
        log.debug( "get_authors ") 
        metadata.bind.echo = False
        s = text (""" select authorid, authorname FROM authors order by authorname """)
        return self.db.execute(s).fetchall()
        
    def get_author(self, authorid):
        log.debug( "get_author %s" ,  authorid) 
        metadata.bind.echo = True
        s = text (""" select * FROM authors where authorid = :i """)
        return self.db.execute(s, i=authorid).fetchone()
        
    def delete_author(self, authorid):
        log.debug( "delete_author %s" ,  authorid) 
        metadata.bind.echo = True
        s = text (""" delete FROM authors where authorid = :i """)
        return self.db.execute(s, i=authorid)
        
    def update_author(self, authorid, author_name, first_name, last_name):
        log.debug( "update_author %s,%s,%s,%s" ,  authorid, author_name, first_name, last_name) 
        metadata.bind.echo = True
        s = text (""" update authors set authorname= :an ,first_name = :fn,last_name = :ln where authorid = :i """)
        return self.db.execute(s, an=author_name, fn=first_name, ln=last_name,  i=authorid)        

    def get_song_authors_for_author(self, authorid):
        log.debug( "get_song_authors for author %s ", authorid) 
        metadata.bind.echo = False        
        s = text (""" select * FROM songauthors where authorid = :c """)
        return self.db.execute(s, c=authorid).fetchall()

    def get_song_authors_for_song(self, songid):
        log.debug( "get_song_authors for song %s ", songid) 
        metadata.bind.echo = False        
        s = text (""" select * FROM songauthors where songid = :c """)
        return self.db.execute(s, c=songid).fetchall()
 
    def get_max_bible_book_verses(self, bookname, chapter):
        log.debug( "get_max_bible_book_verses %s,%s ", bookname ,  chapter) 
        metadata.bind.echo = False        
        s = text (""" select max(verse.verse) from verse,book where chapter = :c and book_id = book.id and book.name = :b """)
        return self.db.execute(s, c=chapter, b=bookname).fetchone()
        
    def get_max_bible_book_chapter(self, bookname):
        log.debug( "get_max_bible_book_chapter %s ", bookname ) 
        metadata.bind.echo = False        
        s = text (""" select max(verse.chapter) from verse,book where book_id = book.id and book.name = :b """)
        return self.db.execute(s, b=bookname).fetchone()   

    def get_bible_book(self, bookname):
        log.debug( "get_bible_book %s", bookname) 
        metadata.bind.echo = False        
        s = text (""" select name FROM book where book.name == :b """)
        return self.db.execute(s, b=bookname).fetchone()
        
    def get_bible_book_Id(self, bookname):
        log.debug( "get_bible_book_id %s", bookname) 
        metadata.bind.echo = False        
        s = text (""" select id FROM book where book.name == :b """)
        return self.db.execute(s, b=bookname).fetchone()        
        
    def get_bible_chapter(self, bookname, chapter):
        log.debug( "get_bible_chapter %s,%s", bookname, chapter )               
        metadata.bind.echo = False
        s = text (""" select book.name FROM verse,book where verse.book_id == book.id AND verse.chapter == :c and book.name == :b """)
        return self.db.execute(s, c=chapter, b=bookname).fetchone()
        
    def get_bible_text(self, bookname, chapter, sverse, everse):
        log.debug( "get_bible_text %s,%s,%s,%s ", bookname, chapter, sverse, everse)
        metadata.bind.echo = False
        s = text (""" select name,chapter,verse.verse, verse.text FROM verse , book where verse.book_id == book.id AND verse.chapter == :c AND (verse.verse between :v1 and :v2) and book.name == :b """)
        return self.db.execute(s, c=chapter, v1=sverse , v2=everse, b=bookname).fetchall()
        
    def get_song_from_lyrics(self,searchtext):
        log.debug( "get_song_from_lyrics %s",searchtext)
        metadata.bind.echo = False
        searchtext = "%"+searchtext+"%"
        s = text (""" SELECT s.songid AS songid, s.songtitle AS songtitle, a.authorname AS authorname FROM songs s OUTER JOIN songauthors sa ON s.songid = sa.songid OUTER JOIN authors a ON sa.authorid = a.authorid WHERE s.lyrics LIKE :t ORDER BY s.songtitle ASC """)
        return self.db.execute(s, t=searchtext).fetchall()
        
    def get_song_from_title(self,searchtext):
        log.debug( "get_song_from_title %s",searchtext)
        metadata.bind.echo = False
        searchtext = "%"+searchtext+"%"        
        s = text (""" SELECT s.songid AS songid, s.songtitle AS songtitle, a.authorname AS authorname FROM songs s OUTER JOIN songauthors sa ON s.songid = sa.songid OUTER JOIN authors a ON sa.authorid = a.authorid WHERE s.songtitle LIKE :t ORDER BY s.songtitle ASC """)
        return self.db.execute(s, t=searchtext).fetchall()
    
    def get_song_from_author(self,searchtext):
        log.debug( "get_song_from_author %s",searchtext)
        metadata.bind.echo = False
        searchtext = "%"+searchtext+"%"
        s = text (""" SELECT s.songid AS songid, s.songtitle AS songtitle, a.authorname AS authorname FROM songs s OUTER JOIN songauthors sa ON s.songid = sa.songid OUTER JOIN authors a ON sa.authorid = a.authorid WHERE a.authorname LIKE :t ORDER BY s.songtitle ASC """)
        return self.db.execute(s, t=searchtext).fetchall()         
        
        
    def dump_songs(self):
        log.debug( ".........Dumping Songs Database")
        log.debug( "...............................Books ")     
        s = text (""" select * FROM authors """)
        log.debug( self.db.execute(s).fetchall())
