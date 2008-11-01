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
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..', '..')))

from openlp.utils import ConfigHelper

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

metadata = MetaData()
#Define the tables and indexes
meta_table = Table('meta', metadata, 
    Column('key', String(255), primary_key=True), 
    Column('value', String(255)), 
)

testament_table = Table('testament', metadata, 
    Column('id', Integer, primary_key=True), 
    Column('name', String(30)), 
)
   
book_table = Table('book', metadata, 
    Column('id', Integer, primary_key=True), 
    Column('testament_id', None , ForeignKey('testament.id')), 
    Column('name', String(30)), 
    Column('abbrev', String(30)), 
)
Index('idx_name', book_table.c.name, book_table.c.id)
Index('idx_abbrev', book_table.c.abbrev, book_table.c.id)
    
verse_table = Table('verse', metadata, 
   Column('id', Integer, primary_key=True), 
    Column('book_id', None, ForeignKey('book.id')), 
    Column('chapter', Integer), 
    Column('verse', Integer), 
    Column('text', Text), 
)
Index('idx_chapter_verse_book', verse_table.c.chapter, verse_table.c.verse, verse_table.c.book_id, verse_table.c.id)

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

class BibleDBImpl:
    def __init__(self, biblename):   
        # Connect to database 
        path = ConfigHelper.getBiblePath()
        #print path
        #print biblename
        self.biblefile = os.path.join(path, biblename+".bible")
        #print self.biblefile
        self.db = create_engine("sqlite:///"+self.biblefile)
        self.db.echo = False
        #self.metadata = metaData()
        metadata.bind = self.db
        metadata.bind.echo = False
        self.Session = sessionmaker()
        self.Session.configure(bind=self.db)
        
    def createTables(self):
        if os.path.exists(self.biblefile):   # delete bible file and set it up again
            os.remove(self.biblefile)
        meta_table.create()
        testament_table.create()
        book_table.create()
        verse_table.create()
        self.loadMeta("dbversion", "0.1")

    def createChapter(self, bk, chap, textlist):
        print "createChapter ", bk, chap, textlist
        metadata.bind.echo = False
        session = self.Session()
        s = text (""" select id FROM book where book.name == :b """)
        data = self.db.execute(s, b=bk).fetchone()
        id = data[0]    # id is first record in list.
        #print "id = " , id
        for v ,  t in textlist.iteritems():
            versemeta = Verse(book_id=id,  chapter=int(chap), verse=int(v), text=(t))
            session.add(versemeta)
        session.commit()
        
    def createBook(self, bk):
        print "createBook ", bk
        metadata.bind.echo = False       
        session = self.Session()
        bookmeta = Book(int(5), bk, bk)
        session.add(bookmeta)
        session.commit()
        
    def loadMeta(self, key, value):
        metadata.bind.echo = False                
        session = self.Session()
        bmeta= BibleMeta(key, value)
        session.add(bmeta)
        session.commit()

    def getMeta(self, key):
        s = text (""" select value FROM meta where key == :k """)
        return self.db.execute(s, k=key).fetchone()

    def _loadTestaments(self):
        metadata.bind.echo = False                
        session = self.Session()    
        testmeta = ONTestament(name="Old Testament")
        session.add(testmeta)
        testmeta = ONTestament(name="New Testament")
        session.add(testmeta)
        session.commit()
    

    def loadData(self, booksfile, versesfile):
        self.loadMeta("version", "Bible Version")
        self.loadMeta("Copyright", "(c) Some Bible company")
        self.loadMeta("Permission", "You Have Some")
        
        self._loadTestaments()
        session = self.Session()

        #Populate the Tables
        fbooks=open(booksfile, 'r')
        fverse=open(versesfile, 'r')

        for line in fbooks:
            #print line
            p = line.split(",")
            p[2] = self._cleanText(p[2])
            p[3] = self._cleanText(p[3])
            bookmeta = Book(int(p[1]), p[2], p[3])
            session.add(bookmeta)
        session.commit()

        book_ptr = ""
        for line in fverse:
            #print line
            p = line.split(",", 3) # split into 3 units and leave the rest as a single field
            p[0] = self._cleanText(p[0])
            p[3] = self._cleanText(p[3])
            if book_ptr is not p[0]:
                query =  session.query(Book).filter(Book.name==p[0])
                #print query
                #print query.first()
                #print query.first().id
                book_ptr = p[0]
                #print text
            versemeta = Verse(book_id=query.first().id,  chapter=int(p[1]), verse=int(p[2]), text=(p[3]))
            session.add(versemeta)
        session.commit()
            
    def getBibleBook(self, bookname):
        print "getBibleBook ", bookname        
        metadata.bind.echo = False        
        s = text (""" select name FROM book where book.name == :b """)
        return self.db.execute(s, b=bookname).fetchone()
        
    def getBibleChapter(self, bookname, chapter):
        print "getBibleChapter ", bookname, chapter                
        metadata.bind.echo = False
        s = text (""" select book.name FROM verse,book where verse.book_id == book.id AND verse.chapter == :c and book.name == :b """)
        print s
        print self.db.execute(s, c=chapter, b=bookname).fetchone()        
        return self.db.execute(s, c=chapter, b=bookname).fetchone()
        
    def getBibleText(self, bookname, chapter, sverse, everse):
        print "getBibleText ", bookname, chapter, sverse, everse
        metadata.bind.echo = False
        s = text (""" select verse.verse, verse.text FROM verse,book where verse.book_id == book.id AND verse.chapter == :c AND (verse.verse between :v1 and :v2) and book.name == :b """)
        return self.db.execute(s, c=chapter, v1=sverse , v2=everse, b=bookname).fetchall()
        
    def dumpBible(self):
        print ".........Dumping Bible Database"
        print "...............................Books "        
        s = text (""" select * FROM book """)
        print self.db.execute(s).fetchall()
        print "...............................Verses "                
        s = text (""" select * FROM verse """)
        print self.db.execute(s).fetchall()         

    def _cleanText(self, text):
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        text = text.replace('"', '')
        return text
