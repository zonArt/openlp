# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import os
import re
import sqlite3

from PyQt4 import QtCore
from sqlalchemy import Column, ForeignKey, or_, Table, types
from sqlalchemy.orm import class_mapper, mapper, relation
from sqlalchemy.orm.exc import UnmappedClassError

from openlp.core.lib import Receiver, translate
from openlp.core.lib.db import BaseModel, init_db, Manager
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.utils import AppLocation

log = logging.getLogger(__name__)

class BibleMeta(BaseModel):
    """
    Bible Meta Data
    """
    pass

#TODO: Delete unused code
'''
class Testament(BaseModel):
    """
    Bible Testaments
    """
    pass
'''

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

class AlternativeBookNames(BaseModel):
    """
    Alternative Book Names model
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
    #TODO: Delete unused code
    '''
    testament_table = Table(u'testament', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'name', types.Unicode(50)),
    )
    '''
    book_table = Table(u'book', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'book_reference_id', types.Integer),
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
    #TODO: Delete unused code
    '''
    try:
        class_mapper(Testament)
    except UnmappedClassError:
        mapper(Testament, testament_table)
    '''
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

def init_schema_alternative_book_names(url):
    """
    Setup a alternative book names database connection and initialise the 
    database schema.

    ``url``
        The database to setup.
    """
    session, metadata = init_db(url)

    alternative_book_names_table = Table(u'alternative_book_names', metadata,
        Column(u'id', types.Integer, primary_key=True),
        Column(u'book_reference_id', types.Integer),
        Column(u'language_id', types.Integer),
        Column(u'name', types.Unicode(50), index=True),
    )

    try:
        class_mapper(AlternativeBookNames)
    except UnmappedClassError:
        mapper(AlternativeBookNames, alternative_book_names_table)

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
            self.file = self.clean_filename(self.name)
        if u'file' in kwargs:
            self.file = kwargs[u'file']
        Manager.__init__(self, u'bibles/bibles', init_schema, self.file)
        if u'file' in kwargs:
            self.get_name()
        if u'path' in kwargs:
            self.path = kwargs[u'path']
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
        if version_name:
            self.name = version_name.value
        else:
            self.name = None
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
        #TODO: Delete unused code
        #self.setup_testaments()
        return self.name

    #TODO: Delete unused code
    '''
    def setup_testaments(self):
        """
        Initialise the testaments section of a bible with suitable defaults.
        """
        self.save_object(Testament.populate(name=u'Old Testament'))
        self.save_object(Testament.populate(name=u'New Testament'))
        self.save_object(Testament.populate(name=u'Apocrypha'))
    '''

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
        book = Book.populate(name=name, book_reference_id=bk_ref_id,
            testament_reference_id=testament)
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
        log.debug(u'BibleDBcreate_chapter("%s", "%s")', book_id, chapter)
        # Text list has book and chapter as first two elements of the array.
        for verse_number, verse_text in textlist.iteritems():
            verse = Verse.populate(
                book_id = book_id,
                chapter = chapter,
                verse = verse_number,
                text = verse_text
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
        if not isinstance(value, unicode):
            value = unicode(value)
        log.debug(u'BibleDB.save_meta("%s/%s")', key, value)
        self.save_object(BibleMeta.populate(key=key, value=value))

    def get_book(self, book):
        """
        Return a book object from the database.

        ``book``
            The name of the book to return.
        """
        log.debug(u'BibleDB.get_book("%s")', book)
        db_book = self.get_object_filtered(Book, Book.name.like(book + u'%'))
        return db_book

    def get_books(self):
        """
        A wrapper so both local and web bibles have a get_books() method that
        manager can call. Used in the media manager advanced search tab.
        """
        return self.get_all_objects(Book, order_by_ref=Book.id)

    def get_book_by_book_ref_id(self, id):
        """
        Return a book object from the database.

        ``id``
            The reference id of the book to return.
        """
        log.debug(u'BibleDB.get_book_by_book_ref_id("%s")', id)
        db_book = self.get_object_filtered(Book, 
            Book.book_reference_id.like(id))
        return db_book

    def get_book_ref_id_by_name(self, book, language_id=None):
        log.debug(u'BibleDB.get_book_ref_id_by_name:("%s", "%s")', book, 
            language_id)
        self.alternative_book_names_cache = AlternativeBookNamesDB(
            self.bible_plugin, path=self.path)
        if BiblesResourcesDB.get_book(book):
            book_temp = BiblesResourcesDB.get_book(book)
            book_id = book_temp[u'id']
        elif BiblesResourcesDB.get_alternative_book_name(book, language_id):
            book_id = BiblesResourcesDB.get_alternative_book_name(book, 
                language_id)
        elif self.alternative_book_names_cache.get_book_reference_id(book, 
            language_id):
            book_id = self.alternative_book_names_cache.get_book_reference_id(
                book, language_id)
        else:
            from openlp.plugins.bibles.forms import BookNameForm
            book_ref = None
            book_name = BookNameForm(self.wizard)
            if book_name.exec_(book):
                book_ref = unicode(book_name.requestComboBox.currentText())
            if not book_ref:
                return None
            else:
                book_temp = BiblesResourcesDB.get_book(book_ref)
            if book_temp:
                book_id = book_temp[u'id']
            else:
                return None
            if book_id:
                self.alternative_book_names_cache.create_alternative_book_name(
                    book, book_id, language_id)
        if book_id:
            return book_id
        else:
            return None

    def get_verses(self, reference_list):
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
                log.debug(u'OpenLP failed to find book %s', book)
                critical_error_message_box(
                    translate('BiblesPlugin', 'No Book Found'),
                    translate('BiblesPlugin', 'No matching book '
                    'could be found in this Bible. Check that you have '
                    'spelled the name of the book correctly.'))
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
            or_clause = []
            keywords = [u'%%%s%%' % keyword.strip()
                for keyword in text.split(u',')]
            for keyword in keywords:
                or_clause.append(Verse.text.like(keyword))
            verses = verses.filter(or_(*or_clause))
        else:
            keywords = [u'%%%s%%' % keyword.strip()
                for keyword in text.split(u' ')]
            for keyword in keywords:
                verses = verses.filter(Verse.text.like(keyword))
        verses = verses.all()
        return verses

    def get_chapter_count(self, book_id):
        """
        Return the number of chapters in a book.

        ``book``
            The book to get the chapter count for.
        """
        log.debug(u'BibleDB.get_chapter_count("%s")', book_id)
        count = self.session.query(Verse.chapter).join(Book)\
            .filter(Book.book_reference_id==book_id)\
            .distinct().count()
        if not count:
            return 0
        else:
            return count

    def get_verse_count(self, book_id, chapter):
        """
        Return the number of verses in a chapter.

        ``book``
            The book containing the chapter.

        ``chapter``
            The chapter to get the verse count for.
        """
        log.debug(u'BibleDB.get_verse_count("%s", "%s")', book_id, chapter)
        count = self.session.query(Verse).join(Book)\
            .filter(Book.book_reference_id==book_id)\
            .filter(Verse.chapter==chapter)\
            .count()
        if not count:
            return 0
        else:
            return count

    def get_language(self):
        """
        If no language is given it calls a dialog window where the user could 
        choose the bible language.
        Return the language id of a bible.

        ``book``
            The language the bible is.
        """
        log.debug(u'BibleDB.get_language()')
        from openlp.plugins.bibles.forms import LanguageForm
        language = None
        lang = LanguageForm(self.wizard)
        if lang.exec_():
            language = unicode(lang.requestComboBox.currentText())
        if not language:
            return False
        language = BiblesResourcesDB.get_language(language)
        language_id = language[u'id']
        self.create_meta(u'language_id', language_id)
        return language_id

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
            filepath = os.path.join(
                AppLocation.get_directory(AppLocation.PluginsDir), u'bibles',
                u'resources', u'bibles_resources.sqlite')
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
        book_list = []
        for book in books:
            book_list.append({
                u'id': book[0],
                u'testament_id': book[1],
                u'name': unicode(book[2]),
                u'abbreviation': unicode(book[3]),
                u'chapters': book[4]
            })
        return book_list

    @staticmethod
    def get_book(name):
        """
        Return a book by name or abbreviation.

        ``name``
            The name or abbreviation of the book.
        """
        log.debug(u'BiblesResourcesDB.get_book("%s")', name)
        if not isinstance(name, unicode):
            name = unicode(name)
        books = BiblesResourcesDB.run_sql(u'SELECT id, testament_id, name, '
                u'abbreviation, chapters FROM book_reference WHERE name = ? OR '
                u'abbreviation = ?', (name, name))
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
                u'abbreviation, chapters FROM book_reference WHERE id = ?', 
                (id, ))
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
    def get_chapter(book_id, chapter):
        """
        Return the chapter details for a specific chapter of a book.

        ``book_id``
            The id of a book.

        ``chapter``
            The chapter number.
        """
        log.debug(u'BiblesResourcesDB.get_chapter("%s", "%s")', book_id,  chapter)
        if not isinstance(chapter, int):
            chapter = int(chapter)
        chapters = BiblesResourcesDB.run_sql(u'SELECT id, book_reference_id, '
            u'chapter, verse_count FROM chapters WHERE book_reference_id = ?', 
            (book_id,))
        if chapters:
            return {
                u'id': chapters[chapter-1][0],
                u'book_reference_id': chapters[chapter-1][1],
                u'chapter': chapters[chapter-1][2],
                u'verse_count': chapters[chapter-1][3]
            }
        else:
            return None

    @staticmethod
    def get_chapter_count(book_id):
        """
        Return the number of chapters in a book.

        ``book_id``
            The id of the book.
        """
        log.debug(u'BiblesResourcesDB.get_chapter_count("%s")', book_id)
        details = BiblesResourcesDB.get_book_by_id(book_id)
        if details:
            return details[u'chapters']
        return 0

    @staticmethod
    def get_verse_count(book_id, chapter):
        """
        Return the number of verses in a chapter.

        ``book``
            The id of the book.

        ``chapter``
            The number of the chapter.
        """
        log.debug(u'BiblesResourcesDB.get_verse_count("%s", "%s")', book_id,  
            chapter)
        details = BiblesResourcesDB.get_chapter(book_id, chapter)
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
        if not isinstance(source,  unicode):
            source = unicode(source)
        source = BiblesResourcesDB.get_download_source(source)
        bibles = BiblesResourcesDB.run_sql(u'SELECT id, name, abbreviation, '
            u'language_id, download_source_id FROM webbibles WHERE '
            u'download_source_id = ?', (source[u'id'],))
        if bibles:
            bibles_temp = []
            for bible in bibles:
                bibles_temp.append({
                    u'id': bible[0],
                    u'name': bible[1],
                    u'abbreviation': bible[2],
                    u'language_id': bible[3], 
                    u'download_source_id': bible[4]
                    })
            return bibles_temp
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
        log.debug(u'BiblesResourcesDB.get_webbibles("%s", "%s")', abbreviation, 
            source)
        if not isinstance(abbreviation, unicode):
            abbreviation = unicode(abbreviation)
        if not isinstance(source, unicode):
            source = unicode(source)
        source = BiblesResourcesDB.get_download_source(source)
        bible = BiblesResourcesDB.run_sql(u'SELECT id, name, abbreviation, '
            u'language_id, download_source_id FROM webbibles WHERE '
            u'download_source_id = ? AND abbreviation = ?', (source[u'id'], 
            abbreviation))
        if bible:
            bibles_temp = {
                u'id': bible[0][0],
                u'name': bible[0][1],
                u'abbreviation': bible[0][2],
                u'language_id': bible[0][3], 
                u'download_source_id': bible[0][4]
                }
            return bibles_temp
        else:
            return None

    @staticmethod
    def get_alternative_book_name(name, language_id=None):
        """
        Return a book_reference_id if the name matches.
        """
        log.debug(u'BiblesResourcesDB.get_alternative_book_name("%s", "%s")', 
            name, language_id)
        if language_id:
            id = BiblesResourcesDB.run_sql(u'SELECT book_reference_id '
                u'FROM alternative_book_names WHERE name = ? and language_id '
                u'= ? ORDER BY id', (name, language_id))
        else:
            id = BiblesResourcesDB.run_sql(u'SELECT book_reference_id '
                u'FROM alternative_book_names WHERE name = ? ORDER BY id', (
                name, ))
        if id:
            return int(id[0][0])
        else:
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
        name = name.title()
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
        languages = BiblesResourcesDB.run_sql(u'SELECT id, name, code FROM '
                u'language ORDER by name')
        if languages:
            languages_temp = []
            for language in languages:
                languages_temp.append({
                    u'id': language[0],
                    u'name': unicode(language[1]),
                    u'code': unicode(language[2])
                })
            return languages_temp
        else:
            return None

    @staticmethod
    def get_testament_reference():
        """
        Return a list of all testaments and their id of the Bible.
        """
        log.debug(u'BiblesResourcesDB.get_testament_reference()')
        testaments = BiblesResourcesDB.run_sql(u'SELECT id, name FROM '
                u'testament_reference ORDER BY id')
        testament_list = []
        for testament in testaments:
            testament_list.append({
                u'id': testament[0],
                u'name': unicode(testament[1])
            })
        return testament_list

class AlternativeBookNamesDB(QtCore.QObject, Manager):
    """
    This class represents a database-bound alternative book names system. 
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
        log.info(u'AlternativeBookNamesDB loaded')
        QtCore.QObject.__init__(self)
        self.bible_plugin = parent
        if u'path' not in kwargs:
            raise KeyError(u'Missing keyword argument "path".')
        self.stop_import_flag = False
        self.name = u'alternative_book_names.sqlite'
        if not isinstance(self.name, unicode):
            self.name = unicode(self.name, u'utf-8')
        self.file = self.name
        Manager.__init__(self, u'bibles/resources', 
            init_schema_alternative_book_names, self.file)
        self.wizard = None
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_stop_wizard'), self.stop_import)

    def stop_import(self):
        """
        Stops the import of the Bible.
        """
        log.debug(u'Stopping import')
        self.stop_import_flag = True

    def get_book_reference_id(self, name,  language=None):
        """
        Return the book_reference_id of a book by name.

        ``name``
            The name to search the id.
            
        ``language``
            The language for which should be searched
        """
        log.debug(u'AlternativeBookNamesDB.get_book_reference_id("%s")', name)
        if language:
            id = self.session.query(AlternativeBookNames.book_reference_id)\
                .filter(AlternativeBookNames.name.like(name))\
                .filter(AlternativeBookNames.language_id.like(language)).first()
        else:
            id = self.get_object_filtered(AlternativeBookNames.book_reference_id,
                AlternativeBookNames.name.like(name))
        if not id:
            return None
        else:
            return id[0]

    def create_alternative_book_name(self, name, book_reference_id, 
        language_id):
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
        alternative_book_name = AlternativeBookNames.populate(name=name, 
            book_reference_id=book_reference_id, language_id=language_id)
        self.save_object(alternative_book_name)
        return alternative_book_name
