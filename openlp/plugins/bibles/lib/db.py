# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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

import chardet
import logging
import os
import re
import sqlite3

from PyQt4 import QtCore
from sqlalchemy import Column, ForeignKey, Table, or_, types, func
from sqlalchemy.orm import class_mapper, mapper, relation
from sqlalchemy.orm.exc import UnmappedClassError

from openlp.core.lib import Receiver, Registry, translate
from openlp.core.lib.db import BaseModel, init_db, Manager
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.utils import AppLocation, clean_filename
import upgrade

log = logging.getLogger(__name__)

RESERVED_CHARACTERS = u'\\.^$*+?{}[]()'

class BibleMeta(BaseModel):
    """
    Bible Meta Data
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

    book_table = Table(u'book', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'book_reference_id', types.Integer, index=True),
        Column(u'testament_reference_id', types.Integer),
        Column(u'name', types.Unicode(50), index=True),
    )
    verse_table = Table(u'verse', metadata,
        Column(u'id', types.Integer, primary_key=True, index=True),
        Column(u'book_id', types.Integer, ForeignKey(
            u'book.id'), index=True),
        Column(u'chapter', types.Integer, index=True),
        Column(u'verse', types.Integer, index=True),
        Column(u'text', types.UnicodeText, index=True),
    )

    try:
        class_mapper(BibleMeta)
    except UnmappedClassError:
        mapper(BibleMeta, meta_table)
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
    log.info(u'BibleDB loaded')

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
            self.file = clean_filename(self.name) + u'.sqlite'
        if u'file' in kwargs:
            self.file = kwargs[u'file']
        Manager.__init__(self, u'bibles', init_schema, self.file, upgrade)
        if u'file' in kwargs:
            self.get_name()
        if u'path' in kwargs:
            self.path = kwargs[u'path']
        self.wizard = None
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'openlp_stop_wizard'), self.stop_import)

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
        version_name = self.get_object(BibleMeta, u'name')
        self.name = version_name.value if version_name else None
        return self.name

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
        return self.name

    def create_book(self, name, bk_ref_id, testament=1):
        """
        Add a book to the database.

        ``name``
            The name of the book.

        ``bk_ref_id``
            The book_reference_id from bibles_resources.sqlite of the book.

        ``testament``
            *Defaults to 1.* The testament_reference_id from
            bibles_resources.sqlite of the testament this book belongs to.
        """
        log.debug(u'BibleDB.create_book("%s", "%s")', name, bk_ref_id)
        book = Book.populate(name=name, book_reference_id=bk_ref_id, testament_reference_id=testament)
        self.save_object(book)
        return book

    def update_book(self, book):
        """
        Update a book in the database.

        ``book``
            The book object
        """
        log.debug(u'BibleDB.update_book("%s")', book.name)
        return self.save_object(book)

    def delete_book(self, db_book):
        """
        Delete a book from the database.

        ``db_book``
            The book object.
        """
        log.debug(u'BibleDB.delete_book("%s")', db_book.name)
        if self.delete_object(Book, db_book.id):
            return True
        return False

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
        log.debug(u'BibleDBcreate_chapter("%s", "%s")', book_id, chapter)
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

    def save_meta(self, key, value):
        """
        Utility method to save or update BibleMeta objects in a Bible database.

        ``key``
            The key for this instance.

        ``value``
            The value for this instance.
        """
        if not isinstance(value, unicode):
            value = unicode(value)
        log.debug(u'BibleDB.save_meta("%s/%s")', key, value)
        meta = self.get_object(BibleMeta, key)
        if meta:
            meta.value = value
            self.save_object(meta)
        else:
            self.save_object(BibleMeta.populate(key=key, value=value))

    def get_book(self, book):
        """
        Return a book object from the database.

        ``book``
            The name of the book to return.
        """
        log.debug(u'BibleDB.get_book("%s")', book)
        return self.get_object_filtered(Book, Book.name.like(book + u'%'))

    def get_books(self):
        """
        A wrapper so both local and web bibles have a get_books() method that
        manager can call. Used in the media manager advanced search tab.
        """
        log.debug(u'BibleDB.get_books()')
        return self.get_all_objects(Book, order_by_ref=Book.id)

    def get_book_by_book_ref_id(self, id):
        """
        Return a book object from the database.

        ``id``
            The reference id of the book to return.
        """
        log.debug(u'BibleDB.get_book_by_book_ref_id("%s")', id)
        return self.get_object_filtered(Book, Book.book_reference_id.like(id))

    def get_book_ref_id_by_name(self, book, maxbooks, language_id=None):
        log.debug(u'BibleDB.get_book_ref_id_by_name:("%s", "%s")', book, language_id)
        book_id = None
        if BiblesResourcesDB.get_book(book, True):
            book_temp = BiblesResourcesDB.get_book(book, True)
            book_id = book_temp[u'id']
        elif BiblesResourcesDB.get_alternative_book_name(book):
            book_id = BiblesResourcesDB.get_alternative_book_name(book)
        elif AlternativeBookNamesDB.get_book_reference_id(book):
            book_id = AlternativeBookNamesDB.get_book_reference_id(book)
        else:
            from openlp.plugins.bibles.forms import BookNameForm
            book_name = BookNameForm(self.wizard)
            if book_name.exec_(book, self.get_books(), maxbooks):
                book_id = book_name.book_id
            if book_id:
                AlternativeBookNamesDB.create_alternative_book_name(
                    book, book_id, language_id)
        return book_id

    def get_book_ref_id_by_localised_name(self, book,
        language_selection):
        """
        Return the id of a named book.

        ``book``
            The name of the book, according to the selected language.

        ``language_selection``
            The language selection the user has chosen in the settings
            section of the Bible.
        """
        log.debug(u'get_book_ref_id_by_localised_name("%s", "%s")',
            book, language_selection)
        from openlp.plugins.bibles.lib import LanguageSelection, \
            BibleStrings
        book_names = BibleStrings().BookNames
        # escape reserved characters
        book_escaped = book
        for character in RESERVED_CHARACTERS:
            book_escaped = book_escaped.replace(
                character, u'\\' + character)
        regex_book = re.compile(u'\s*%s\s*' % u'\s*'.join(
            book_escaped.split()), re.UNICODE | re.IGNORECASE)
        if language_selection == LanguageSelection.Bible:
            db_book = self.get_book(book)
            if db_book:
                return db_book.book_reference_id
        elif language_selection == LanguageSelection.Application:
            books = filter(lambda key:
                regex_book.match(unicode(book_names[key])), book_names.keys())
            books = filter(None, map(BiblesResourcesDB.get_book, books))
            for value in books:
                if self.get_book_by_book_ref_id(value[u'id']):
                    return value[u'id']
        elif language_selection == LanguageSelection.English:
            books = BiblesResourcesDB.get_books_like(book)
            if books:
                book_list = filter(
                    lambda value: regex_book.match(value[u'name']), books)
                if not book_list:
                    book_list = books
                for value in book_list:
                    if self.get_book_by_book_ref_id(value[u'id']):
                        return value[u'id']
        return False

    def get_verses(self, reference_list, show_error=True):
        """
        This is probably the most used function. It retrieves the list of
        verses based on the user's query.

        ``reference_list``
            This is the list of references the media manager item wants. It is
            a list of tuples, with the following format::

                (book_reference_id, chapter, start_verse, end_verse)

            Therefore, when you are looking for multiple items, simply break
            them up into references like this, bundle them into a list. This
            function then runs through the list, and returns an amalgamated
            list of ``Verse`` objects. For example::

                [(u'35', 1, 1, 1), (u'35', 2, 2, 3)]
        """
        log.debug(u'BibleDB.get_verses("%s")', reference_list)
        verse_list = []
        book_error = False
        for book_id, chapter, start_verse, end_verse in reference_list:
            db_book = self.get_book_by_book_ref_id(book_id)
            if db_book:
                book_id = db_book.book_reference_id
                log.debug(u'Book name corrected to "%s"', db_book.name)
                if end_verse == -1:
                    end_verse = self.get_verse_count(book_id, chapter)
                verses = self.session.query(Verse)\
                    .filter_by(book_id=db_book.id)\
                    .filter_by(chapter=chapter)\
                    .filter(Verse.verse >= start_verse)\
                    .filter(Verse.verse <= end_verse)\
                    .order_by(Verse.verse)\
                    .all()
                verse_list.extend(verses)
            else:
                log.debug(u'OpenLP failed to find book with id "%s"', book_id)
                book_error = True
        if book_error and show_error:
            critical_error_message_box(
                translate('BiblesPlugin', 'No Book Found'),
                translate('BiblesPlugin', 'No matching book '
                'could be found in this Bible. Check that you have spelled the name of the book correctly.'))
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
            The book object to get the chapter count for.
        """
        log.debug(u'BibleDB.get_chapter_count("%s")', book.name)
        count = self.session.query(func.max(Verse.chapter)).join(Book).filter(
            Book.book_reference_id==book.book_reference_id).scalar()
        if not count:
            return 0
        return count

    def get_verse_count(self, book_ref_id, chapter):
        """
        Return the number of verses in a chapter.

        ``book_ref_id``
            The book reference id.

        ``chapter``
            The chapter to get the verse count for.
        """
        log.debug(u'BibleDB.get_verse_count("%s", "%s")', book_ref_id, chapter)
        count = self.session.query(func.max(Verse.verse)).join(Book)\
            .filter(Book.book_reference_id==book_ref_id)\
            .filter(Verse.chapter==chapter)\
            .scalar()
        if not count:
            return 0
        return count

    def get_language(self, bible_name=None):
        """
        If no language is given it calls a dialog window where the user could
        select the bible language.
        Return the language id of a bible.

        ``book``
            The language the bible is.
        """
        log.debug(u'BibleDB.get_language()')
        from openlp.plugins.bibles.forms import LanguageForm
        language = None
        language_form = LanguageForm(self.wizard)
        if language_form.exec_(bible_name):
            language = unicode(language_form.languageComboBox.currentText())
        if not language:
            return False
        language = BiblesResourcesDB.get_language(language)
        language_id = language[u'id']
        self.save_meta(u'language_id', language_id)
        return language_id

    def is_old_database(self):
        """
        Returns ``True`` if it is a bible database, which has been created
        prior to 1.9.6.
        """
        try:
            self.session.query(Book).all()
        except:
            return True
        return False

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

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)


class BiblesResourcesDB(QtCore.QObject, Manager):
    """
    This class represents the database-bound Bible Resources. It provide
    some resources which are used in the Bibles plugin.
    A wrapper class around a small SQLite database which contains the download
    resources, a biblelist from the different download resources, the books,
    chapter counts and verse counts for the web download Bibles, a language
    reference, the testament reference and some alternative book names. This
    class contains a singleton "cursor" so that only one connection to the
    SQLite database is ever used.
    """
    cursor = None

    @staticmethod
    def get_cursor():
        """
        Return the cursor object. Instantiate one if it doesn't exist yet.
        """
        if BiblesResourcesDB.cursor is None:
            filepath = os.path.join(AppLocation.get_directory(AppLocation.PluginsDir),
                u'bibles', u'resources', u'bibles_resources.sqlite')
            conn = sqlite3.connect(filepath)
            BiblesResourcesDB.cursor = conn.cursor()
        return BiblesResourcesDB.cursor

    @staticmethod
    def run_sql(query, parameters=()):
        """
        Run an SQL query on the database, returning the results.

        ``query``
            The actual SQL query to run.

        ``parameters``
            Any variable parameters to add to the query.
        """
        cursor = BiblesResourcesDB.get_cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    @staticmethod
    def get_books():
        """
        Return a list of all the books of the Bible.
        """
        log.debug(u'BiblesResourcesDB.get_books()')
        books = BiblesResourcesDB.run_sql(u'SELECT id, testament_id, name, '
                u'abbreviation, chapters FROM book_reference ORDER BY id')
        return [{
            u'id': book[0],
            u'testament_id': book[1],
            u'name': unicode(book[2]),
            u'abbreviation': unicode(book[3]),
            u'chapters': book[4]
        } for book in books]

    @staticmethod
    def get_book(name, lower=False):
        """
        Return a book by name or abbreviation.

        ``name``
            The name or abbreviation of the book.

        ``lower``
            True if the comparsion should be only lowercase
        """
        log.debug(u'BiblesResourcesDB.get_book("%s")', name)
        if not isinstance(name, unicode):
            name = unicode(name)
        if lower:
            books = BiblesResourcesDB.run_sql(u'SELECT id, testament_id, name, '
                    u'abbreviation, chapters FROM book_reference WHERE '
                    u'LOWER(name) = ? OR LOWER(abbreviation) = ?',
                    (name.lower(), name.lower()))
        else:
            books = BiblesResourcesDB.run_sql(u'SELECT id, testament_id, name, '
                    u'abbreviation, chapters FROM book_reference WHERE name = ?'
                    u' OR abbreviation = ?', (name, name))
        if books:
            return {
                u'id': books[0][0],
                u'testament_id': books[0][1],
                u'name': unicode(books[0][2]),
                u'abbreviation': unicode(books[0][3]),
                u'chapters': books[0][4]
            }
        else:
            return None

    @staticmethod
    def get_books_like(string):
        """
        Return the books which include string.

        ``string``
            The string to search for in the book names or abbreviations.
        """
        log.debug(u'BiblesResourcesDB.get_book_like("%s")', string)
        if not isinstance(string, unicode):
            name = unicode(string)
        books = BiblesResourcesDB.run_sql(u'SELECT id, testament_id, name, '
                u'abbreviation, chapters FROM book_reference WHERE '
                u'LOWER(name) LIKE ? OR LOWER(abbreviation) LIKE ?',
                (u'%' + string.lower() + u'%', u'%' + string.lower() + u'%'))
        if books:
            return [{
                u'id': book[0],
                u'testament_id': book[1],
                u'name': unicode(book[2]),
                u'abbreviation': unicode(book[3]),
                u'chapters': book[4]
            } for book in books]
        else:
            return None

    @staticmethod
    def get_book_by_id(id):
        """
        Return a book by id.

        ``id``
            The id of the book.
        """
        log.debug(u'BiblesResourcesDB.get_book_by_id("%s")', id)
        if not isinstance(id, int):
            id = int(id)
        books = BiblesResourcesDB.run_sql(u'SELECT id, testament_id, name, '
                u'abbreviation, chapters FROM book_reference WHERE id = ?', (id, ))
        if books:
            return {
                u'id': books[0][0],
                u'testament_id': books[0][1],
                u'name': unicode(books[0][2]),
                u'abbreviation': unicode(books[0][3]),
                u'chapters': books[0][4]
            }
        else:
            return None

    @staticmethod
    def get_chapter(book_ref_id, chapter):
        """
        Return the chapter details for a specific chapter of a book.

        ``book_ref_id``
            The id of a book.

        ``chapter``
            The chapter number.
        """
        log.debug(u'BiblesResourcesDB.get_chapter("%s", "%s")', book_ref_id, chapter)
        if not isinstance(chapter, int):
            chapter = int(chapter)
        chapters = BiblesResourcesDB.run_sql(u'SELECT id, book_reference_id, '
            u'chapter, verse_count FROM chapters WHERE book_reference_id = ?', (book_ref_id,))
        try:
            return {
                u'id': chapters[chapter-1][0],
                u'book_reference_id': chapters[chapter-1][1],
                u'chapter': chapters[chapter-1][2],
                u'verse_count': chapters[chapter-1][3]
            }
        except (IndexError, TypeError):
            return None

    @staticmethod
    def get_chapter_count(book_ref_id):
        """
        Return the number of chapters in a book.

        ``book_ref_id``
            The id of the book.
        """
        log.debug(u'BiblesResourcesDB.get_chapter_count("%s")', book_ref_id)
        details = BiblesResourcesDB.get_book_by_id(book_ref_id)
        if details:
            return details[u'chapters']
        return 0

    @staticmethod
    def get_verse_count(book_ref_id, chapter):
        """
        Return the number of verses in a chapter.

        ``book``
            The id of the book.

        ``chapter``
            The number of the chapter.
        """
        log.debug(u'BiblesResourcesDB.get_verse_count("%s", "%s")', book_ref_id, chapter)
        details = BiblesResourcesDB.get_chapter(book_ref_id, chapter)
        if details:
            return details[u'verse_count']
        return 0

    @staticmethod
    def get_download_source(source):
        """
        Return a download_source_id by source.

        ``name``
            The name or abbreviation of the book.
        """
        log.debug(u'BiblesResourcesDB.get_download_source("%s")', source)
        if not isinstance(source, unicode):
            source = unicode(source)
        source = source.title()
        dl_source = BiblesResourcesDB.run_sql(u'SELECT id, source FROM '
                u'download_source WHERE source = ?', (source.lower(),))
        if dl_source:
            return {
                u'id': dl_source[0][0],
                u'source': dl_source[0][1]
            }
        else:
            return None

    @staticmethod
    def get_webbibles(source):
        """
        Return the bibles a webbible provide for download.

        ``source``
            The source of the webbible.
        """
        log.debug(u'BiblesResourcesDB.get_webbibles("%s")', source)
        if not isinstance(source, unicode):
            source = unicode(source)
        source = BiblesResourcesDB.get_download_source(source)
        bibles = BiblesResourcesDB.run_sql(u'SELECT id, name, abbreviation, '
            u'language_id, download_source_id FROM webbibles WHERE download_source_id = ?', (source[u'id'],))
        if bibles:
            return [{
                u'id': bible[0],
                u'name': bible[1],
                u'abbreviation': bible[2],
                u'language_id': bible[3],
                u'download_source_id': bible[4]
            } for bible in bibles]
        else:
            return None

    @staticmethod
    def get_webbible(abbreviation, source):
        """
        Return the bibles a webbible provide for download.

        ``abbreviation``
            The abbreviation of the webbible.

        ``source``
            The source of the webbible.
        """
        log.debug(u'BiblesResourcesDB.get_webbibles("%s", "%s")', abbreviation, source)
        if not isinstance(abbreviation, unicode):
            abbreviation = unicode(abbreviation)
        if not isinstance(source, unicode):
            source = unicode(source)
        source = BiblesResourcesDB.get_download_source(source)
        bible = BiblesResourcesDB.run_sql(u'SELECT id, name, abbreviation, '
            u'language_id, download_source_id FROM webbibles WHERE '
            u'download_source_id = ? AND abbreviation = ?', (source[u'id'], abbreviation))
        try:
            return {
                u'id': bible[0][0],
                u'name': bible[0][1],
                u'abbreviation': bible[0][2],
                u'language_id': bible[0][3],
                u'download_source_id': bible[0][4]
            }
        except (IndexError, TypeError):
            return None

    @staticmethod
    def get_alternative_book_name(name, language_id=None):
        """
        Return a book_reference_id if the name matches.

        ``name``
            The name to search the id.

        ``language_id``
            The language_id for which language should be searched
        """
        log.debug(u'BiblesResourcesDB.get_alternative_book_name("%s", "%s")', name, language_id)
        if language_id:
            books = BiblesResourcesDB.run_sql(u'SELECT book_reference_id, name '
                u'FROM alternative_book_names WHERE language_id = ? ORDER BY id', (language_id, ))
        else:
            books = BiblesResourcesDB.run_sql(u'SELECT book_reference_id, name FROM alternative_book_names ORDER BY id')
        for book in books:
            if book[1].lower() == name.lower():
                return book[0]
        return None

    @staticmethod
    def get_language(name):
        """
        Return a dict containing the language id, name and code by name or
        abbreviation.

        ``name``
            The name or abbreviation of the language.
        """
        log.debug(u'BiblesResourcesDB.get_language("%s")', name)
        if not isinstance(name, unicode):
            name = unicode(name)
        language = BiblesResourcesDB.run_sql(u'SELECT id, name, code FROM '
                u'language WHERE name = ? OR code = ?', (name, name.lower()))
        if language:
            return {
                u'id': language[0][0],
                u'name': unicode(language[0][1]),
                u'code': unicode(language[0][2])
            }
        else:
            return None

    @staticmethod
    def get_languages():
        """
        Return a dict containing all languages with id, name and code.
        """
        log.debug(u'BiblesResourcesDB.get_languages()')
        languages = BiblesResourcesDB.run_sql(u'SELECT id, name, code FROM language ORDER by name')
        if languages:
            return [{
                u'id': language[0],
                u'name': unicode(language[1]),
                u'code': unicode(language[2])
            } for language in languages]
        else:
            return None

    @staticmethod
    def get_testament_reference():
        """
        Return a list of all testaments and their id of the Bible.
        """
        log.debug(u'BiblesResourcesDB.get_testament_reference()')
        testaments = BiblesResourcesDB.run_sql(u'SELECT id, name FROM testament_reference ORDER BY id')
        return [
            {
            u'id': testament[0],
            u'name': unicode(testament[1])
            }
            for testament in testaments
        ]


class AlternativeBookNamesDB(QtCore.QObject, Manager):
    """
    This class represents a database-bound alternative book names system.
    """
    cursor = None
    conn = None

    @staticmethod
    def get_cursor():
        """
        Return the cursor object. Instantiate one if it doesn't exist yet.
        If necessary loads up the database and creates the tables if the
        database doesn't exist.
        """
        if AlternativeBookNamesDB.cursor is None:
            filepath = os.path.join(
                AppLocation.get_directory(AppLocation.DataDir), u'bibles', u'alternative_book_names.sqlite')
            if not os.path.exists(filepath):
                #create new DB, create table alternative_book_names
                AlternativeBookNamesDB.conn = sqlite3.connect(filepath)
                AlternativeBookNamesDB.conn.execute(u'CREATE TABLE '
                    u'alternative_book_names(id INTEGER NOT NULL, '
                    u'book_reference_id INTEGER, language_id INTEGER, name '
                    u'VARCHAR(50), PRIMARY KEY (id))')
            else:
                #use existing DB
                AlternativeBookNamesDB.conn = sqlite3.connect(filepath)
            AlternativeBookNamesDB.cursor = AlternativeBookNamesDB.conn.cursor()
        return AlternativeBookNamesDB.cursor

    @staticmethod
    def run_sql(query, parameters=(), commit=None):
        """
        Run an SQL query on the database, returning the results.

        ``query``
            The actual SQL query to run.

        ``parameters``
            Any variable parameters to add to the query

        ``commit``
            If a commit statement is necessary this should be True.
        """
        cursor = AlternativeBookNamesDB.get_cursor()
        cursor.execute(query, parameters)
        if commit:
            AlternativeBookNamesDB.conn.commit()
        return cursor.fetchall()

    @staticmethod
    def get_book_reference_id(name, language_id=None):
        """
        Return a book_reference_id if the name matches.

        ``name``
            The name to search the id.

        ``language_id``
            The language_id for which language should be searched
        """
        log.debug(u'AlternativeBookNamesDB.get_book_reference_id("%s", "%s")', name, language_id)
        if language_id:
            books = AlternativeBookNamesDB.run_sql(u'SELECT book_reference_id, '
                u'name FROM alternative_book_names WHERE language_id = ?', (language_id, ))
        else:
            books = AlternativeBookNamesDB.run_sql(u'SELECT book_reference_id, '
                u'name FROM alternative_book_names')
        for book in books:
            if book[1].lower() == name.lower():
                return book[0]
        return None

    @staticmethod
    def create_alternative_book_name(name, book_reference_id, language_id):
        """
        Add an alternative book name to the database.

        ``name``
            The name of the alternative book name.

        ``book_reference_id``
            The book_reference_id of the book.

        ``language_id``
            The language to which the alternative book name belong.
        """
        log.debug(u'AlternativeBookNamesDB.create_alternative_book_name("%s", '
            '"%s", "%s"', name, book_reference_id, language_id)
        return AlternativeBookNamesDB.run_sql(u'INSERT INTO '
            u'alternative_book_names(book_reference_id, language_id, name) '
            u'VALUES (?, ?, ?)', (book_reference_id, language_id, name), True)


class OldBibleDB(QtCore.QObject, Manager):
    """
    This class connects to the old bible databases to reimport them to the new
    database scheme.
    """
    cursor = None

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
        log.info(u'OldBibleDB loaded')
        QtCore.QObject.__init__(self)
        if u'path' not in kwargs:
            raise KeyError(u'Missing keyword argument "path".')
        if  u'file' not in kwargs:
            raise KeyError(u'Missing keyword argument "file".')
        if u'path' in kwargs:
            self.path = kwargs[u'path']
        if u'file' in kwargs:
            self.file = kwargs[u'file']

    def get_cursor(self):
        """
        Return the cursor object. Instantiate one if it doesn't exist yet.
        """
        if self.cursor is None:
            filepath = os.path.join(self.path, self.file)
            self.connection = sqlite3.connect(filepath)
            self.cursor = self.connection.cursor()
        return self.cursor

    def run_sql(self, query, parameters=()):
        """
        Run an SQL query on the database, returning the results.

        ``query``
            The actual SQL query to run.

        ``parameters``
            Any variable parameters to add to the query.
        """
        cursor = self.get_cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    def get_name(self):
        """
        Returns the version name of the Bible.
        """
        version_name = self.run_sql(u'SELECT value FROM metadata WHERE key = "name"')
        if version_name:
            self.name = version_name[0][0]
        else:
            self.name = None
        return self.name

    def get_metadata(self):
        """
        Returns the metadata of the Bible.
        """
        metadata = self.run_sql(u'SELECT key, value FROM metadata ORDER BY rowid')
        if metadata:
            return [{
                u'key': unicode(meta[0]),
                u'value': unicode(meta[1])
            } for meta in metadata]
        else:
            return None

    def get_book(self, name):
        """
        Return a book by name or abbreviation.

        ``name``
            The name or abbreviation of the book.
        """
        if not isinstance(name, unicode):
            name = unicode(name)
        books = self.run_sql(u'SELECT id, testament_id, name, '
                u'abbreviation FROM book WHERE LOWER(name) = ? OR '
                u'LOWER(abbreviation) = ?', (name.lower(), name.lower()))
        if books:
            return {
                u'id': books[0][0],
                u'testament_id': books[0][1],
                u'name': unicode(books[0][2]),
                u'abbreviation': unicode(books[0][3])
            }
        else:
            return None

    def get_books(self):
        """
        Returns the books of the Bible.
        """
        books = self.run_sql(u'SELECT name, id FROM book ORDER BY id')
        if books:
            return [{
                u'name': unicode(book[0]),
                u'id':int(book[1])
            } for book in books]
        else:
            return None

    def get_verses(self, book_id):
        """
        Returns the verses of the Bible.
        """
        verses = self.run_sql(u'SELECT book_id, chapter, verse, text FROM '
            u'verse WHERE book_id = ? ORDER BY id', (book_id, ))
        if verses:
            return [{
                u'book_id': int(verse[0]),
                u'chapter': int(verse[1]),
                u'verse': int(verse[2]),
                u'text': unicode(verse[3])
            } for verse in verses]
        else:
            return None

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
