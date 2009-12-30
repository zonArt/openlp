# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from sqlalchemy import or_
from PyQt4 import QtCore

from openlp.core.lib import Receiver
from models import *

log = logging.getLogger(__name__)

class BibleDB():
    """
    This class represents a database-bound Bible. It is used as a base class
    for all the custom importers, so that the can implement their own import
    methods, but benefit from the database methods in here via inheritance,
    rather than depending on yet another object.
    """

    def __init__(self, **kwargs):
        """
        The constructor loads up the database and creates and initialises the
        tables if the database doesn't exist.

        **Required keyword arguments:**

        ``path``
            The path to the bible database file.

        ``name``
            The name of the database. This is also used as the file name for
            SQLite databases.

        ``config``
            The configuration object, passed in from the plugin.
        """
        log.info(u'BibleDBimpl loaded')
        if u'path' not in kwargs:
            raise KeyError(u'Missing keyword argument "path".')
        if u'name' not in kwargs:
            raise KeyError(u'Missing keyword argument "name".')
        if u'config' not in kwargs:
            raise KeyError(u'Missing keyword argument "config".')
        self.stop_import = False
        self.name = kwargs[u'name']
        self.config = kwargs[u'config']
        self.db_file = os.path.join(kwargs[u'path'],
            u'%s.sqlite' % kwargs[u'name'])
        log.debug(u'Load bible %s on path %s', kwargs[u'name'], self.db_file)
        db_type = self.config.get_config(u'db type', u'sqlite')
        db_url = u''
        if db_type == u'sqlite':
            db_url = u'sqlite:///' + self.db_file
        else:
            db_url = u'%s://%s:%s@%s/%s' % \
                (db_type, self.config.get_config(u'db username'),
                    self.config.get_config(u'db password'),
                    self.config.get_config(u'db hostname'),
                    self.config.get_config(u'db database'))
        self.metadata, self.session = init_models(db_url)
        self.metadata.create_all(checkfirst=True)

    def register(self):
        """
        This method basically just initialialises the database. It is called
        from the Bible Manager when a Bible is imported. Descendant classes
        may want to override this method to supply their own custom
        initialisation as well.
        """
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlpstopimport'), self.stop_import)
        self.create_tables()
        return self.name

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        log.debug('Stopping import!')
        self.stop_import = True

    def commit(self):
        log.debug('Committing...')
        self.session.commit()

    def create_tables(self):
        log.debug(u'createTables')
        self.save_meta(u'dbversion', u'2')
        self.create_testament(u'Old Testament')
        self.create_testament(u'New Testament')
        self.create_testament(u'Apocrypha')

    def create_testament(self, testament):
        log.debug(u'%s: %s', __name__, testament)
        self.session.add(Testament.populate(name=testament))
        self.commit()

    def create_book(self, name, abbrev, testament=1):
        log.debug(u'create_book %s,%s', bookname, bookabbrev)
        book = Book.populate(name=name, abbreviation=abbrev,
            testament_id=testament)
        self.session.add(book)
        self.commit()
        return book

    def create_chapter(self, book_id, chapter, textlist):
        log.debug(u'create_chapter %s,%s', bookid, chap)
        #text list has book and chapter as first two elements of the array
        for verse_number, verse_text in textlist.iteritems():
            verse = Verse.populate(
                book_id = book_id,
                chapter = chap,
                verse = verse_number,
                text = verse_text
            )
            self.session.add(verse)
        self.commit()

    def create_verse(self, book_id, chapter, verse, text):
        verse = Verse.populate(
            book_id=book_id,
            chapter=chapter,
            verse=verse,
            text=text
        )
        self.session.add(verse)
        return verse

    def create_meta(self, key, value):
        log.debug(u'save_meta %s/%s', key, value)
        self.session.add(BibleMeta.populate(key=key, value=value))
        self.commit()

    def get_books(self):
        log.debug(__name__)
        return self.session.query(Book).order_by(Book.id).all()

    def get_book(self, book):
        log.debug(u'%s: %s', __name__, book)
        db_book = self.session.query(Book)\
            .filter_by(Book.name.like(book + u'%'))\
            .first()
        if db_book is None:
            db_book = self.session.query(Book)\
                .filter(Book.abbreviation.like(book + u'%'))\
                .first()
        return db_book

    def get_chapter(self, id, chapter):
        log.debug(u'%s: %s, %s', __name__, id, chapter)
        return self.session.query(Verse)\
            .filter_by(chapter=chapter)\
            .filter_by(book_id=id)\
            .first()

    def get_verses(self, reference_list):
        """
        This is probably the most used function. It retrieves the list of
        verses based on the user's query.

        ``reference_list``
            This is the list of references the media manager item wants. It is
            a list of tuples, with the following format::

                (book, chapter, start_verse, end_verse)

            Therefore, when you are looking for multiple items, simply break
            them up into references like this, bundle them into a list. This
            function then runs through the list, and returns an amalgamated
            list of ``Verse`` objects. For example::

                [(u'Genesis', 1, 1, 1), (u'Genesis', 2, 2, 3)]
        """
        log.debug(u'%s: %s', __name__, reference_list)
        verse_list = []
        for book, chapter, start_verse, end_verse in reference_list:
            db_book = self.get_book(book)
            if end_verse == -1:
                end_verse = self.get_chapter_count(book)
            if db_book:
                book = book.name
                log.debug(u'Book name corrected to "%s"' % book)
            verses = self.session.query(Verse)\
                .filter_by(book_id=book.id)\
                .filter_by(chapter=chapter)\
                .filter(Verse.verse >= start_verse)\
                .filter(Verse.verse <= end_verse)\
                .order_by(Verse.verse)\
                .all()
            verse_list.extend(verses)
        return verse_list

    def verse_search(self, text):
        """
        Search for verses containing text ``text``.

        ``text``
            The text to search for. If the text contains commas, it will be
            split apart and OR'd on the list of values. If the text just
            contains spaces, it will split apart and AND'd on the list of
            values.
        """
        log.debug(u'%s: %s', __name__, text)
        verses = self.session.query(Verse)
        if text.find(u',') > -1:
            or_clause = []
            keywords = [u'%%%s%%' % keyword.strip() for keyword in text.split(u',')]
            for keyword in keywords:
                or_clause.append(Verse.text.like(keyword))
            verses = verses.filter(or_(*or_clause))
        else:
            keywords = [u'%%%s%%' % keyword.strip() for keyword in text.split(u' ')]
            for keyword in keywords:
                verses = verses.filter(Verse.text.like(keyword))
        verses = verses.all()
        return verses

    def get_chapter_count(self, book):
        log.debug(u'%s: %s', __name__, book)
        count = self.session.query(Verse.chapter).join(Book)\
            .filter(Book.name==book)\
            .distinct().count()
        #verse = self.session.query(Verse).join(Book).filter(
        #    Book.name == bookname).order_by(Verse.chapter.desc()).first()
        if not count:
            return 0
        else:
            return count

    def get_verse_count(self, book, chapter):
        log.debug(u'%s: %s, %s', __name__, book, chapter)
        count = self.session.query(Verse).join(Book)\
            .filter(Book.name==book)\
            .filter(Verse.chapter==chapter)\
            .count()
        #verse = self.session.query(Verse).join(Book).filter(
        #    Book.name == bookname).filter(
        #    Verse.chapter == chapter).order_by(Verse.verse.desc()).first()
        if not count:
            return 0
        else:
            return count

    def get_meta(self, key):
        log.debug(u'get meta %s', key)
        return self.session.query(BibleMeta).get(key)

    def delete_meta(self, metakey):
        biblemeta = self.get_meta(metakey)
        try:
            self.session.delete(biblemeta)
            self.commit()
            return True
        except:
            return False

    def dump_bible(self):
        log.debug( u'.........Dumping Bible Database')
        log.debug( '...............................Books ')
        books = self.session.query(Book).all()
        log.debug(books)
        log.debug( u'...............................Verses ')
        verses = self.session.query(Verse).all()
        log.debug(verses)

