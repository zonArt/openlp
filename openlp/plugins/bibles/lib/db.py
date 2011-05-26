# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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

import logging
import chardet
import re

from PyQt4 import QtCore
from sqlalchemy import Column, ForeignKey, or_, Table, types
from sqlalchemy.orm import class_mapper, mapper, relation
from sqlalchemy.orm.exc import UnmappedClassError

from openlp.core.lib import Receiver, translate
from openlp.core.lib.db import BaseModel, init_db, Manager
from openlp.core.lib.ui import critical_error_message_box

log = logging.getLogger(__name__)

class BibleMeta(BaseModel):
    """
    Bible Meta Data
    """
    pass


class Testament(BaseModel):
    """
    Bible Testaments
    """
    pass


class Book(BaseModel):
    """
    Song model
    """
    pass


class Verse(BaseModel):
    """
    Topic model
    """
    pass


def init_schema(url):
    """
    Setup a bible database connection and initialise the database schema.

    ``url``
        The database to setup.
    """
    session, metadata = init_db(url)

    meta_table = Table(u'metadata', metadata,
        Column(u'key', types.Unicode(255), primary_key=True, index=True),
        Column(u'value', types.Unicode(255)),
    )
    testament_table = Table(u'testament', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'name', types.Unicode(50)),
    )
    book_table = Table(u'book', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'testament_id', types.Integer, ForeignKey(u'testament.id')),
        Column(u'name', types.Unicode(50), index=True),
        Column(u'abbreviation', types.Unicode(5), index=True),
    )
    verse_table = Table(u'verse', metadata,
        Column(u'id', types.Integer, primary_key=True, index=True),
        Column(u'book_id', types.Integer, ForeignKey(u'book.id'), index=True),
        Column(u'chapter', types.Integer, index=True),
        Column(u'verse', types.Integer, index=True),
        Column(u'text', types.UnicodeText, index=True),
    )

    try:
        class_mapper(BibleMeta)
    except UnmappedClassError:
        mapper(BibleMeta, meta_table)
    try:
        class_mapper(Testament)
    except UnmappedClassError:
        mapper(Testament, testament_table,
            properties={'books': relation(Book, backref='testament')})
    try:
        class_mapper(Book)
    except UnmappedClassError:
        mapper(Book, book_table,
            properties={'verses': relation(Verse, backref='book')})
    try:
        class_mapper(Verse)
    except UnmappedClassError:
        mapper(Verse, verse_table)

    metadata.create_all(checkfirst=True)
    return session


class BibleDB(QtCore.QObject, Manager):
    """
    This class represents a database-bound Bible. It is used as a base class
    for all the custom importers, so that the can implement their own import
    methods, but benefit from the database methods in here via inheritance,
    rather than depending on yet another object.
    """

    def __init__(self, parent, **kwargs):
        """
        The constructor loads up the database and creates and initialises the
        tables if the database doesn't exist.

        **Required keyword arguments:**

        ``path``
            The path to the bible database file.

        ``name``
            The name of the database. This is also used as the file name for
            SQLite databases.
        """
        log.info(u'BibleDB loaded')
        QtCore.QObject.__init__(self)
        self.bible_plugin = parent
        if u'path' not in kwargs:
            raise KeyError(u'Missing keyword argument "path".')
        if u'name' not in kwargs and u'file' not in kwargs:
            raise KeyError(u'Missing keyword argument "name" or "file".')
        self.stop_import_flag = False
        if u'name' in kwargs:
            self.name = kwargs[u'name']
            if not isinstance(self.name, unicode):
                self.name = unicode(self.name, u'utf-8')
            self.file = self.clean_filename(self.name)
        if u'file' in kwargs:
            self.file = kwargs[u'file']
        Manager.__init__(self, u'bibles', init_schema, self.file)
        if u'file' in kwargs:
            self.get_name()
        self.wizard = None
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_stop_wizard'), self.stop_import)

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        log.debug(u'Stopping import')
        self.stop_import_flag = True

    def get_name(self):
        """
        Returns the version name of the Bible.
        """
        version_name = self.get_object(BibleMeta, u'Version')
        self.name = version_name.value if version_name else None
        return self.name

    def clean_filename(self, old_filename):
        """
        Clean up the version name of the Bible and convert it into a valid
        file name.

        ``old_filename``
            The "dirty" file name or version name.
        """
        if not isinstance(old_filename, unicode):
            old_filename = unicode(old_filename, u'utf-8')
        old_filename = re.sub(r'[^\w]+', u'_', old_filename).strip(u'_')
        return old_filename + u'.sqlite'

    def register(self, wizard):
        """
        This method basically just initialialises the database. It is called
        from the Bible Manager when a Bible is imported. Descendant classes
        may want to override this method to supply their own custom
        initialisation as well.

        ``wizard``
            The actual Qt wizard form.
        """
        self.wizard = wizard
        self.create_meta(u'dbversion', u'2')
        self.setup_testaments()
        return self.name

    def setup_testaments(self):
        """
        Initialise the testaments section of a bible with suitable defaults.
        """
        self.save_object(Testament.populate(name=u'Old Testament'))
        self.save_object(Testament.populate(name=u'New Testament'))
        self.save_object(Testament.populate(name=u'Apocrypha'))

    def create_book(self, name, abbrev, testament=1):
        """
        Add a book to the database.

        ``name``
            The name of the book.

        ``abbrev``
            The abbreviation of the book.

        ``testament``
            *Defaults to 1.* The id of the testament this book belongs to.
        """
        log.debug(u'create_book %s,%s', name, abbrev)
        book = Book.populate(name=name, abbreviation=abbrev,
            testament_id=testament)
        self.save_object(book)
        return book

    def create_chapter(self, book_id, chapter, textlist):
        """
        Add a chapter and its verses to a book.

        ``book_id``
            The id of the book being appended.

        ``chapter``
            The chapter number.

        ``textlist``
            A dict of the verses to be inserted. The key is the verse number,
            and the value is the verse text.
        """
        log.debug(u'create_chapter %s,%s', book_id, chapter)
        # Text list has book and chapter as first two elements of the array.
        for verse_number, verse_text in textlist.iteritems():
            verse = Verse.populate(
                book_id=book_id,
                chapter=chapter,
                verse=verse_number,
                text=verse_text
            )
            self.session.add(verse)
        self.session.commit()

    def create_verse(self, book_id, chapter, verse, text):
        """
        Add a single verse to a chapter.

        ``book_id``
            The id of the book being appended.

        ``chapter``
            The chapter number.

        ``verse``
            The verse number.

        ``text``
            The verse text.
        """
        if not isinstance(text, unicode):
            details = chardet.detect(text)
            text = unicode(text, details[u'encoding'])
        verse = Verse.populate(
            book_id=book_id,
            chapter=chapter,
            verse=verse,
            text=text
        )
        self.session.add(verse)
        return verse

    def create_meta(self, key, value):
        """
        Utility method to save BibleMeta objects in a Bible database.

        ``key``
            The key for this instance.

        ``value``
            The value for this instance.
        """
        log.debug(u'save_meta %s/%s', key, value)
        self.save_object(BibleMeta.populate(key=key, value=value))

    def get_book(self, book):
        """
        Return a book object from the database.

        ``book``
            The name of the book to return.
        """
        log.debug(u'BibleDb.get_book("%s")', book)
        db_book = self.get_object_filtered(Book, Book.name.like(book + u'%'))
        if db_book is None:
            db_book = self.get_object_filtered(Book,
                Book.abbreviation.like(book + u'%'))
        return db_book

    def get_books(self):
        """
        A wrapper so both local and web bibles have a get_books() method that
        manager can call. Used in the media manager advanced search tab.
        """
        return self.get_all_objects(Book, order_by_ref=Book.id)

    def get_verses(self, reference_list, show_error=True):
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
        log.debug(u'BibleDB.get_verses: %s', reference_list)
        verse_list = []
        for book, chapter, start_verse, end_verse in reference_list:
            db_book = self.get_book(book)
            if db_book:
                book = db_book.name
                log.debug(u'Book name corrected to "%s"', book)
                if end_verse == -1:
                    end_verse = self.get_verse_count(book, chapter)
                verses = self.session.query(Verse)\
                    .filter_by(book_id=db_book.id)\
                    .filter_by(chapter=chapter)\
                    .filter(Verse.verse >= start_verse)\
                    .filter(Verse.verse <= end_verse)\
                    .order_by(Verse.verse)\
                    .all()
                verse_list.extend(verses)
            else:
                log.debug(u'OpenLP failed to find book %s', book)
                if show_error:
                    critical_error_message_box(
                        translate('BiblesPlugin', 'No Book Found'),
                        translate('BiblesPlugin', 'No matching book '
                        'could be found in this Bible. Check that you '
                        'have spelled the name of the book correctly.'))
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
        log.debug(u'BibleDB.verse_search("%s")', text)
        verses = self.session.query(Verse)
        if text.find(u',') > -1:
            keywords = \
                [u'%%%s%%' % keyword.strip() for keyword in text.split(u',')]
            or_clause = [Verse.text.like(keyword) for keyword in keywords]
            verses = verses.filter(or_(*or_clause))
        else:
            keywords = \
                [u'%%%s%%' % keyword.strip() for keyword in text.split(u' ')]
            for keyword in keywords:
                verses = verses.filter(Verse.text.like(keyword))
        verses = verses.all()
        return verses

    def get_chapter_count(self, book):
        """
        Return the number of chapters in a book.

        ``book``
            The book to get the chapter count for.
        """
        log.debug(u'BibleDB.get_chapter_count("%s")', book)
        count = self.session.query(Verse.chapter).join(Book)\
            .filter(Book.name == book)\
            .distinct().count()
        if not count:
            return 0
        else:
            return count

    def get_verse_count(self, book, chapter):
        """
        Return the number of verses in a chapter.

        ``book``
            The book containing the chapter.

        ``chapter``
            The chapter to get the verse count for.
        """
        log.debug(u'BibleDB.get_verse_count("%s", %s)', book, chapter)
        count = self.session.query(Verse).join(Book)\
            .filter(Book.name == book)\
            .filter(Verse.chapter == chapter)\
            .count()
        if not count:
            return 0
        else:
            return count

    def dump_bible(self):
        """
        Utility debugging method to dump the contents of a bible.
        """
        log.debug(u'.........Dumping Bible Database')
        log.debug(u'...............................Books ')
        books = self.session.query(Book).all()
        log.debug(books)
        log.debug(u'...............................Verses ')
        verses = self.session.query(Verse).all()
        log.debug(verses)
