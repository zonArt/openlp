from sqlalchemy import  *
from sqlalchemy.sql import select

import time
import datetime
import logging
import string

import os, os.path
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..')))

from openlp.utils import ConfigHelper

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

metadata = MetaData()
#Define the tables and indexes

meta = Table('meta', metadata, 
    Column('key', String(255), primary_key=True), 
    Column('value', String(255)), 
)

testament = Table('Testament', metadata, 
    Column('id', Integer, primary_key=True), 
    Column('name', String(30)), 
)
   
books = Table('Books', metadata, 
    Column('id', Integer, primary_key=True), 
    Column('testament_id', None , ForeignKey('Testament.id')), 
    Column('name', String(30)), 
    Column('abbrev', String(30)), 
)
Index('idx_name', books.c.name, books.c.id)
Index('idx_abbrev', books.c.abbrev, books.c.id)
    
verses = Table('Verses', metadata, 
   Column('id', Integer, primary_key=True), 
    Column('book_id', None, ForeignKey('Books.id')), 
    Column('chapter', Integer), 
    Column('verse', Integer), 
    Column('text', Text), 
)
Index('idx_chapter_verse_book', verses.c.chapter, verses.c.verse, verses.c.book_id, verses.c.id)

class bible_impl:
    def __init__(self, filename):   
        # Connect to database 
        path = ConfigHelper.getBiblePath()
        print path
        biblefile = os.path.join(path, filename+".bible")
        print biblefile
        self.db = create_engine("sqlite:///"+biblefile)
        self.db.echo = False
        metadata.bind = self.db
        metadata.bind.echo = False
        
    def create_tables(self):
        meta.create()
        testament.create()
        books.create()
        verses.create()

    def Load_Data(self, booksfile, versesfile):

        metai =meta.insert()
        metai.execute(key="dbversion", value="1")
        metai.execute(key="version", value="Bible Version")
        metai.execute(key="Copyright", value="(c) Some Bible company")
        metai.execute(key="Permission", value="You have some")
        print meta.select()
        
        #Populate the Tables
        insi = testament.insert()
        insi.execute(name="Old Testament")
        insi.execute(name="New Testament")
        print testament.select()

        fbooks=open(booksfile, 'r')
        fverse=open(versesfile, 'r')

        insb = books.insert()
        for line in fbooks:
            print line
            p = line.split(",")
            insb.execute(testament_id=int(p[1]), name=p[2], abbrev=p[3])
        
        t = books.select()
        print t
        
        book_ptr = ""

        insv = verses.insert()
        #Books._connection.debug=True
        for line in fverse:
            print line
            p = line.split(",", 3) # split into 3 units and leave the rest as a single field
            if book_ptr != p[0]:
                r = self.db.execute(books.select(books.c.name==p[0])).fetchone()
                book_ptr = p[0]
                  
            print p[3]
            insv.execute(book_id=r[0],  chapter=int(p[1]), verse=int(p[2]), text=p[3])

    def Run_Tests(self):
        print "test print"
        b = self.db.execute(books.select(books.c.name=='"John"')).fetchone()
        print b
        v = self.db.execute(verses.select(verses.c.chapter==1 and verses.c.verse==1 and verses.c.book_id == b[0])).fetchone()
        print v
   
