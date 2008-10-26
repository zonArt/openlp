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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..')))

from openlp.utils import ConfigHelper

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

Base = declarative_base()
#Define the tables and indexes
class BibleMeta(Base):
    __tablename__ = "meta"
    key = Column(String(255), primary_key=True)
    value = Column(String(255))
    def __init__(self, key, value):
        self.key = key
        self.value =value
        
    def __repr__(self):
        return "<biblemeta('%s','%s')>" %(self.key, self.value)
        
class Testament(Base):
    __tablename__ = "testament"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return "<testament('%s')>" %(self.name)
      
class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    testament_id = Column(Integer)
    name = Column(String(30))
    abbrev = Column(String(30))    
    def __init__(self, testament_id, name, abbrev):
        self.testament_id = testament_id
        self.name = name
        self.abbrev = abbrev        
        
    def __repr__(self):
        return "<books('%s','%s','%s')>" %(self.testament_id, self.name, self.abbrev)
      
class Verses(Base):
    __tablename__ = "verses"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    chapter = Column(Integer) 
    verse = Column(Integer)        
    text = Column(Text)    

    def __init__(self, book_id, chapter, verse, text):
        self.book_id = book_id
        self.chapter = chapter
        self.verse = verse
        self.text = text                
        
    def __repr__(self):
        return "<verses('%s','%s','%s','%s')>" %(self.book_id, self.chapter, self.verse, self.text)
      

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
        self.metadata = MetaData()
        self.metadata = Base.metadata
        self.metadata.bind = self.db
        self.metadata.bind.echo = False
        
    def createTables(self):
        if os.path.exists(self.biblefile):   # delete bible file and set it up again
            os.remove(self.biblefile)
        self.metadata.create_all(self.db)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.db)

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
            print line
            p = line.split(",")
            bookmeta = Books(int(p[1]), p[2], p[3])
            session.add(bookmeta)
        session.commit()
        
#        for row in session.query(Books).all():
#           print row
        
        book_ptr = ""

        for line in fverse:
            print line
            p = line.split(",", 3) # split into 3 units and leave the rest as a single field
            if book_ptr is not p[0]:
                query =  session.query(Books).filter(Books.name==p[0])
                print query.first().id
                book_ptr = p[0]
            print p[3]
            versemeta = Verses(book_id=query.first().id,  chapter=int(p[1]), verse=int(p[2]), text=p[3])
            session.add(versemeta)
        session.commit()
            

    def Run_Tests(self):
        print "test print"
        session = self.Session()
        print session.query(Books).filter(Books.name=='"John"').all()
        print session.query(Verses).filter(Verses.book_id==9).all()
        #print b
        #v = self.db.execute(verses.select(verses.c.chapter==1 and verses.c.verse==1 and verses.c.book_id == b[0])).fetchone()
        #print v
   
