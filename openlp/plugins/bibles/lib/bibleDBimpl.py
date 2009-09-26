# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import os
import logging

from common import BibleCommon
from openlp.plugins.bibles.lib.models import *

class BibleDBImpl(BibleCommon):
    global log
    log = logging.getLogger(u'BibleDBImpl')
    log.info(u'BibleDBimpl loaded')

    def __init__(self, biblepath, biblename, config):
        # Connect to database
        self.config = config
        self.biblefile = os.path.join(biblepath, biblename + u'.sqlite')
        log.debug(u'Load bible %s on path %s', biblename, self.biblefile)
        db_type = self.config.get_config(u'db type', u'sqlite')
        db_url = u''
        if db_type == u'sqlite':
            db_url = u'sqlite:///' + self.biblefile
        else:
            db_url = u'%s://%s:%s@%s/%s' % \
                (db_type, self.config.get_config(u'db username'),
                    self.config.get_config(u'db password'),
                    self.config.get_config(u'db hostname'),
                    self.config.get_config(u'db database'))
        self.metadata, self.session = init_models(db_url)
        self.metadata.create_all(checkfirst=True)

    def create_tables(self):
        log.debug( u'createTables')
        self.save_meta(u'dbversion', u'2')
        self._load_testament(u'Old Testament')
        self._load_testament(u'New Testament')
        self._load_testament(u'Apocrypha')

    def add_verse(self, bookid, chap, vse, text):
        #log.debug(u'add_verse %s,%s,%s", bookid, chap, vse)
        verse = Verse()
        verse.book_id = bookid
        verse.chapter = chap
        verse.verse = vse
        verse.text = text
        self.session.add(verse)
        self.session.commit()

    def create_chapter(self, bookid, chap, textlist):
        log.debug(u'create_chapter %s,%s', bookid, chap)
        #text list has book and chapter as first to elements of the array
        for verse_number, verse_text in textlist.iteritems():
            verse = Verse()
            verse.book_id = bookid
            verse.chapter = chap
            verse.verse = verse_number
            verse.text = verse_text
            self.session.add(verse)
        self.session.commit()

    def create_book(self, bookname, bookabbrev, testament=1):
        log.debug(u'create_book %s,%s', bookname, bookabbrev)
        book = Book()
        book.testament_id = testament
        book.name = bookname
        book.abbreviation = bookabbrev
        self.session.add(book)
        self.session.commit()
        return book

    def save_meta(self, key, value):
        log.debug(u'save_meta %s/%s', key, value)
        bmeta = BibleMeta()
        bmeta.key = key
        bmeta.value = value
        self.session.add(bmeta)
        self.session.commit()

    def get_meta(self, metakey):
        log.debug(u'get meta %s', metakey)
        return self.session.query(BibleMeta).filter_by(key=metakey).first()

    def delete_meta(self, metakey):
        biblemeta = self.get_meta(metakey)
        try:
            self.session.delete(biblemeta)
            self.session.commit()
            return True
        except:
            return False

    def _load_testament(self, testament):
        log.debug(u'load_testaments %s', testament)
        test = ONTestament()
        test.name = testament
        self.session.add(test)
        self.session.commit()

    def get_bible_books(self):
        log.debug(u'get_bible_books')
        return self.session.query(Book).order_by(Book.id).all()

    def get_max_bible_book_verses(self, bookname, chapter):
        log.debug(u'get_max_bible_book_verses %s, %s', bookname, chapter)
        verse = self.session.query(Verse).join(Book).filter(
            Book.name == bookname).filter(
            Verse.chapter == chapter).order_by(Verse.verse.desc()).first()
        return verse.verse

    def get_max_bible_book_chapter(self, bookname):
        log.debug(u'get_max_bible_book_chapter %s', bookname)
        verse = self.session.query(Verse).join(Book).filter(
            Book.name == bookname).order_by(Verse.chapter.desc()).first()
        return verse.chapter

    def get_bible_book(self, bookname):
        log.debug(u'get_bible_book %s', bookname)
        book = self.session.query(Book).filter(
            Book.name.like(bookname + u'%')).first()
        if book is None:
            book = self.session.query(Book).filter(
                Book.abbreviation.like(bookname + u'%')).first()
        return book

    def get_bible_chapter(self, id, chapter):
        log.debug(u'get_bible_chapter %s, %s', id, chapter)
        return self.session.query(Verse).filter_by(chapter=chapter).filter_by(
            book_id=id).first()

    def get_bible_text(self, bookname, chapter, sverse, everse):
        log.debug(u'get_bible_text %s, %s, %s, %s', bookname, chapter, sverse,
            everse)
        verses = self.session.query(Verse).join(Book).filter(
            Book.name == bookname).filter(Verse.chapter == chapter).filter(
            Verse.verse>=sverse).filter(Verse.verse<=everse).order_by(
            Verse.verse).all()
        return verses

    def get_verses_from_text(self, versetext):
        log.debug(u'get_verses_from_text %s',versetext)
        versetext = u'%%%s%%' % versetext
        verses = self.session.query(Verse).filter(
            Verse.text.like(versetext)).all()
        return verses

    def dump_bible(self):
        log.debug( u'.........Dumping Bible Database')
        log.debug( '...............................Books ')
        books = self.session.query(Book).all()
        log.debug(books)
        log.debug( u'...............................Verses ')
        verses = self.session.query(Verse).all()
        log.debug(verses)
