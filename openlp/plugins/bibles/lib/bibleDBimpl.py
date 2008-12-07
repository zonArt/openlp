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

class BibleDBException(Exception):
    pass
class BibleInvalidDatabaseError(Exception):
    pass
    
metadata = MetaData()
#Define the tables and indexes
meta_table = Table('metadata', metadata, 
    Column('key', String(255), primary_key=True), 
    Column('value', String(255)), 
)

testament_table = Table('testament', metadata, 
    Column('id', Integer, primary_key=True), 
    Column('name', String(30)), 
)
   
book_table = Table('book', metadata, 
    Column('id', Integer, primary_key=True), 
    Column('testament_id', Integer), 
    Column('name', String(30)), 
    Column('abbrev', String(5)), 
)
Index('idx_name', book_table.c.name, book_table.c.id)
Index('idx_abbrev', book_table.c.abbrev, book_table.c.id)

#Column('book_id', None, ForeignKey('book.id')), 
verse_table = Table('verse', metadata, 
   Column('id', Integer, primary_key=True), 
    Column('book_id', Integer ), 
    Column('chapter', Integer), 
    Column('verse', Integer), 
    Column('text', Text), 
)
Index('idx_chapter_verse_book', verse_table.c.chapter, verse_table.c.verse, verse_table.c.book_id, verse_table.c.id)
Index('idx_chapter_verse_text', verse_table.c.text, verse_table.c.verse, verse_table.c.book_id, verse_table.c.id)

class BibleMeta(object):
    def __init__(self, key, value):
        self.key = key
        self.value =value
        
    def __repr__(self):
        return "<biblemeta('%s','%s')>" %(self.key, self.value)
        
class ONTestament(object):
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<testament('%s')>" %(self.name)
      
class Book(object):
    def __init__(self, testament_id, name, abbrev):
        self.testament_id = testament_id
        self.name = name
        self.abbrev = abbrev        
        
    def __repr__(self):
        return "<book('%s','%s','%s','%s')>" %(self.id, self.testament_id, self.name, self.abbrev)
      
class Verse(object):
    def __init__(self, book_id, chapter, verse, text):
        self.book_id = book_id
        self.chapter = chapter
        self.verse = verse
        self.text = text                
        
    def __repr__(self):
        return "<verse('%s','%s','%s','%s')>" %(self.book_id, self.chapter, self.verse, self.text)
      
mapper(BibleMeta,  meta_table)
mapper(ONTestament,  testament_table)
mapper(Book,  book_table)
mapper(Verse,  verse_table)

class BibleDBImpl(BibleCommon):
    global log     
    log=logging.getLogger("BibleDBMgr")
    log.info("BibleDB manager loaded")   
    def __init__(self, biblepath , biblename, suffix, btype = 'sqlite'):   
        # Connect to database 
        self.biblefile = os.path.join(biblepath, biblename+"."+suffix)
        log.debug( "Load bible %s on path %s", biblename, self.biblefile)
        if btype == 'sqlite': 
            self.db = create_engine("sqlite:///"+self.biblefile)
        elif btype == 'mysql': 
            self.db = create_engine("mysql://tim:@192.168.0.100:3306/openlp_rsv_bible")
        else:
            raise BibleInvalidDatabaseError("Database not mysql or sqlite")
        self.db.echo = False
        #self.metadata = metaData()
        metadata.bind = self.db
        metadata.bind.echo = False
        self.Session = sessionmaker()
        self.Session.configure(bind=self.db)
        
    def createTables(self):
        log.debug( "createTables")        
        if os.path.exists(self.biblefile):   # delete bible file and set it up again
            os.remove(self.biblefile)
        meta_table.create()
        testament_table.create()
        book_table.create()
        verse_table.create()
        self.saveMeta("dbversion", "2")
        self._loadTestaments()
        
    def addVerse(self, bookid, chap,  verse, text):
        log.debug( "addVerse %s,%s,%s,%s", bookid, chap, verse, text)
        metadata.bind.echo = False
        session = self.Session()
        versemeta = Verse(book_id=int(bookid),  chapter=int(chap), verse=int(verse), text=(text))
        session.add(versemeta)
        session.commit()

    def createChapter(self, bookid, chap, textlist):
        log.debug( "createChapter %s,%s,%s", bookid, chap, textlist)
        metadata.bind.echo = False
        session = self.Session()
        #s = text (""" select id FROM book where book.name == :b """)
        #data = self.db.execute(s, b=bookname).fetchone()
        #id = data[0]    # id is first record in list.
        #log.debug( "id = " , id
        for v ,  t in textlist.iteritems():
            versemeta = Verse(book_id=bookid,  chapter=int(chap), verse=int(v), text=(t))
            session.add(versemeta)
        session.commit()
        
    def createBook(self, bookid, bookname, bookabbrev):
        log.debug( "createBook %s,%s,%s", bookid, bookname, bookabbrev)
        metadata.bind.echo = False       
        session = self.Session()
        bookmeta = Book(int(5), bookname, bookabbrev)
        session.add(bookmeta)
        session.commit()
        
    def saveMeta(self, key, value):
        metadata.bind.echo = False                
        session = self.Session()
        bmeta= BibleMeta(key, value)
        session.add(bmeta)
        session.commit()

    def getMeta(self, key):
        s = text (""" select value FROM metadata where key == :k """)
        return self.db.execute(s, k=key).fetchone()

    def deleteMeta(self, key):
        metadata.bind.echo = False
        s = text (""" delete FROM meta where key == :k """)
        self.db.execute(s, k=key)

    def _loadTestaments(self):
        log.debug("loadTestaments")
        metadata.bind.echo = False               
        session = self.Session()    
        testmeta = ONTestament(name="Old Testament")
        session.add(testmeta)
        testmeta = ONTestament(name="New Testament")
        session.add(testmeta)
        testmeta = ONTestament(name="Apocrypha")
        session.add(testmeta)        
        session.commit()
        
    def getBibleBooks(self):
        log.debug( "getBibleBook ") 
        metadata.bind.echo = False        
        s = text (""" select name FROM book order by id """)
        return self.db.execute(s).fetchall()
 
    def getMaxBibleBookVerses(self, bookname, chapter):
        log.debug( "getMaxBibleBookVerses %s,%s ", bookname ,  chapter) 
        metadata.bind.echo = False        
        s = text (""" select max(verse.verse) from verse,book where chapter = :c and book_id = book.id and book.name = :b """)
        return self.db.execute(s, c=chapter, b=bookname).fetchone()
        
    def getMaxBibleBookChapters(self, bookname):
        log.debug( "getMaxBibleBookChapters %s ", bookname ) 
        metadata.bind.echo = False        
        s = text (""" select max(verse.chapter) from verse,book where book_id = book.id and book.name = :b """)
        return self.db.execute(s, b=bookname).fetchone()   

    def getBibleBook(self, bookname):
        log.debug( "getBibleBook %s", bookname) 
        metadata.bind.echo = False        
        s = text (""" select name FROM book where book.name == :b """)
        return self.db.execute(s, b=bookname).fetchone()
        
    def getBibleBookId(self, bookname):
        log.debug( "getBibleBook %s", bookname) 
        metadata.bind.echo = False        
        s = text (""" select id FROM book where book.name == :b """)
        return self.db.execute(s, b=bookname).fetchone()        
        
    def getBibleChapter(self, bookname, chapter):
        log.debug( "getBibleChapter %s,%s", bookname, chapter )               
        metadata.bind.echo = False
        s = text (""" select book.name FROM verse,book where verse.book_id == book.id AND verse.chapter == :c and book.name == :b """)
        return self.db.execute(s, c=chapter, b=bookname).fetchone()
        
    def getBibleText(self, bookname, chapter, sverse, everse):
        log.debug( "getBibleText %s,%s,%s,%s ", bookname, chapter, sverse, everse)
        metadata.bind.echo = False
        s = text (""" select verse.verse, verse.text FROM verse , book where verse.book_id == book.id AND verse.chapter == :c AND (verse.verse between :v1 and :v2) and book.name == :b """)
        return self.db.execute(s, c=chapter, v1=sverse , v2=everse, b=bookname).fetchall()
        
    def getVersesFromText(self,versetext):
        log.debug( "getBibleText %s",versetext)
        metadata.bind.echo = False
        versetext = "%"+versetext+"%"
        s = text (""" select book.name, verse.chapter, verse.verse, verse.text FROM verse , book where  verse.book_id == book.id  and verse.text like :t """)
        return self.db.execute(s, t=versetext).fetchall()        
        
    def dumpBible(self):
        log.debug( ".........Dumping Bible Database")
        log.debug( "...............................Books ")     
        s = text (""" select * FROM book """)
        log.debug( self.db.execute(s).fetchall())
        log.debug( "...............................Verses ")            
        s = text (""" select * FROM verse """)
        log.debug( self.db.execute(s).fetchall())
