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
import os
import os.path
import logging

from sqlalchemy import  *
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, mapper,  scoped_session

from common import BibleCommon
from openlp.core.utils import ConfigHelper
from openlp.plugins.bibles.lib.tables import *
from openlp.plugins.bibles.lib.classes import *

class BibleDBImpl(BibleCommon):
    global log
    log=logging.getLogger(u'BibleDBImpl')
    log.info(u'BibleDBimpl loaded')

    def __init__(self, biblepath , biblename, config):
        # Connect to database
        self.config = config
        self.biblefile = os.path.join(biblepath, biblename+u'.sqlite')
        log.debug( "Load bible %s on path %s", biblename, self.biblefile)
        db_type = self.config.get_config(u'db type', u'sqlite')
        if db_type  == u'sqlite':
            self.db = create_engine("sqlite:///" + self.biblefile)
        else:
            self.db_url = u'%s://%s:%s@%s/%s' % \
                (db_type, self.config.get_config(u'db username'),
                    self.config.get_config(u'db password'),
                    self.config.get_config(u'db hostname'),
                    self.config.get_config(u'db database'))
        self.db.echo = False
        metadata.bind = self.db
        metadata.bind.echo = False
        self.session = scoped_session(sessionmaker(autoflush=True, autocommit=False))
        self.session.configure(bind=self.db)
        metadata.create_all(self.db)

    def create_tables(self):
        log.debug( u'createTables')
        self.save_meta(u'dbversion', u'2')
        self._load_testament("Old Testament")
        self._load_testament("New Testament")
        self._load_testament("Apocrypha")

    def add_verse(self, bookid, chap,  vse, text):
        #log.debug( "add_verse %s,%s,%s", bookid, chap, vse)
        metadata.bind.echo = False
        session = self.session()
        verse = Verse()
        verse.book_id = bookid
        verse.chapter = chap
        verse.verse = vse
        verse.text = text
        session.add(verse)
        session.commit()

    def create_chapter(self, bookid, chap, textlist):
        log.debug( "create_chapter %s,%s", bookid, chap)
        #log.debug("Text %s ", textlist)
        metadata.bind.echo = False
        session = self.session()
        #text list has book and chapter as first to elements of the array
        for v ,  t in textlist.iteritems():
            verse = Verse()
            verse.book_id = bookid
            verse.chapter = chap
            verse.verse = v
            verse.text = t
            session.add(verse)
        session.commit()

    def create_book(self, bookname, bookabbrev, testament = 1):
        log.debug( "create_book %s,%s", bookname, bookabbrev)
        metadata.bind.echo = False
        session = self.session()
        book = Book()
        book.testament_id = testament
        book.name = bookname
        book.abbreviation = bookabbrev
        session.add(book)
        session.commit()
        return book

    def save_meta(self, key, value):
        log.debug( "save_meta %s/%s", key, value)
        metadata.bind.echo = False
        session = self.session()
        bmeta= BibleMeta()
        bmeta.key = key
        bmeta.value = value
        session.add(bmeta)
        session.commit()

    def get_meta(self, metakey):
        log.debug( "get meta %s", metakey)
        return self.session.query(BibleMeta).filter_by(key = metakey).first()

    def delete_meta(self, metakey):
        biblemeta = self.get_meta(metakey)
        try:
            session.delete(biblemeta)
            session.commit()
            return True
        except:
            return False

    def _load_testament(self, testament):
        log.debug("load_testaments %s",  testament)
        metadata.bind.echo = False
        session = self.session()
        test = ONTestament()
        test.name = testament
        session.add(test)
        session.commit()

    def get_bible_books(self):
        log.debug( "get_bible_books ")
        return self.session.query(Book).order_by(Book.id).all()

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
        bk = self.session.query(Book).filter(Book.name.like(bookname+u"%")).first()
        if bk == None:
            bk = self.session.query(Book).filter(Book.abbreviation.like(bookname+u"%")).first()
        return bk

    def get_bible_chapter(self, id, chapter):
        log.debug( "get_bible_chapter %s,%s", id, chapter )
        metadata.bind.echo = False
        return self.session.query(Verse).filter_by(chapter = chapter ).filter_by(book_id = id).first()

    def get_bible_text(self, bookname, chapter, sverse, everse):
        log.debug( "get_bible_text %s,%s,%s,%s ", bookname, chapter, sverse, everse)
        metadata.bind.echo = False
        bookname = bookname + u"%"
        s = text (""" select name,chapter,verse.verse, verse.text FROM verse , book where verse.book_id == book.id AND verse.chapter == :c AND (verse.verse between :v1 and :v2) and (book.name like :b) """)
        return self.db.execute(s, c=chapter, v1=sverse , v2=everse, b=bookname).fetchall()

    def get_verses_from_text(self,versetext):
        log.debug( "get_verses_from_text %s",versetext)
        metadata.bind.echo = False
        versetext = "%"+versetext+"%"
        s = text (""" select book.name, verse.chapter, verse.verse, verse.text FROM verse , book where  verse.book_id == book.id  and verse.text like :t """)
        return self.db.execute(s, t=versetext).fetchall()

    def dump_bible(self):
        log.debug( u'.........Dumping Bible Database')
        log.debug( '...............................Books ')
        s = text (""" select * FROM book """)
        log.debug( self.db.execute(s).fetchall())
        log.debug( u'...............................Verses ')
        s = text (""" select * FROM verse """)
        log.debug( self.db.execute(s).fetchall())
