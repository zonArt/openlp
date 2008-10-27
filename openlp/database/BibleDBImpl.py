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
sys.path.insert(0,(os.path.join(mypath, '..', '..')))

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
        
class Testament(object):
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
mapper(Testament,  testament_table)
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
        
    def createTables(self):
        if os.path.exists(self.biblefile):   # delete bible file and set it up again
            os.remove(self.biblefile)
        meta_table.create()
        testament_table.create()
        book_table.create()
        verse_table.create()
        self.Session = sessionmaker()
        self.Session.configure(bind=self.db)
#        i1 = Index('idx_name', Books.c.name, Books.c.id)
#        i1.create(bind=self.db)
#        i2 = Index('idx_abbrev', Books.c.abbrev, Books.c.id)
#        i2.create(bind=self.db)

    def loadData(self, booksfile, versesfile):
        session = self.Session()
        bmeta= BibleMeta("dbversion", "0.1")
        session.add(bmeta)
        bmeta= BibleMeta("version", "Bible Version")
        session.add(bmeta)        
        bmeta= BibleMeta("Copyright", "(c) Some Bible company")
        session.add(bmeta)        
        bmeta= BibleMeta("Permission", "You Have Some")                
        session.add(bmeta)

        
        #Populate the Tables
        testmeta = Testament(name="Old Testament")
        session.add(testmeta)
        testmeta = Testament(name="New Testament")
        session.add(testmeta)
        session.commit()

        fbooks=open(booksfile, 'r')
        fverse=open(versesfile, 'r')

        for line in fbooks:
            #print line
            p = line.split(",")
            bookmeta = Book(int(p[1]), p[2], p[3])
            session.add(bookmeta)
        session.commit()
        
#        for row in session.query(Books).all():
#           print row
        
        book_ptr = ""

        for line in fverse:
            #print line
            p = line.split(",", 3) # split into 3 units and leave the rest as a single field
            if book_ptr is not p[0]:
                query =  session.query(Book).filter(Book.name==p[0])
                #print query.first().id
                book_ptr = p[0]
            #print p[3]
            versemeta = Verse(book_id=query.first().id,  chapter=int(p[1]), verse=int(p[2]), text=p[3])
            session.add(versemeta)
        session.commit()
            

    def getBibleText(self, bookname, chapter, verse):
        s = text (""" select text FROM verse,book where verse.book_id == book.id AND verse.chapter == :c and verse.verse == :v and book.name == :b """)
        return self.db.execute(s, c=chapter, v=verse , b=bookname).fetchone()
        
    def Run_Tests(self):
        metadata.bind.echo = True
        print "test print"
        session = self.Session()
        print session.query(Book).filter(Book.name=='"John"').all()
        q = session.query(Verse).filter(Verse.book_id==8)
        print q.first().text
        
        q = session.query(Verse, Book).filter(Verse.chapter==1).filter(Verse.verse==1).filter(Book.name=='"Genesis"')
        print "--"
        print q.first()[0].text
        print q.first()[1].name
        print "----"
        ch =1 
        vs = 1
        bk = '"Genesis"'
        s = text (""" select text FROM verse,book where verse.book_id == book.id AND verse.chapter == :c and verse.verse == :v and book.name == :b """)
        print self.db.execute(s, c=ch, v=vs , b=bk).fetchall()

   
