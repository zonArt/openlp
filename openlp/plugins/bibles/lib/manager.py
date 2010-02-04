# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

import logging
import os
import csv

from common import parse_reference
from opensong import OpenSongBible
from osis import OSISBible
from csvbible import CSVBible
from db import BibleDB
from http import HTTPBible

class BibleMode(object):
    """
    This is basically an enumeration class which specifies the mode of a Bible.
    Mode refers to whether or not a Bible in OpenLP is a full Bible or needs to
    be downloaded from the Internet on an as-needed basis.
    """
    Full = 1
    Partial = 2


class BibleFormat(object):
    """
    This is a special enumeration class that holds the various types of Bibles,
    plus a few helper functions to facilitate generic handling of Bible types
    for importing.
    """
    Unknown = -1
    OSIS = 0
    CSV = 1
    OpenSong = 2
    WebDownload = 3

    @staticmethod
    def get_class(id):
        """
        Return the appropriate imeplementation class.
        """
        if id == BibleFormat.OSIS:
            return OSISBible
        elif id == BibleFormat.CSV:
            return CSVBible
        elif id == BibleFormat.OpenSong:
            return OpenSongBible
        elif id == BibleFormat.WebDownload:
            return HTTPBible
        else:
            return None

    @staticmethod
    def list():
        return [
            BibleFormat.OSIS,
            BibleFormat.CSV,
            BibleFormat.OpenSong,
            BibleFormat.WebDownload
        ]


class BibleManager(object):
    """
    The Bible manager which holds and manages all the Bibles.
    """
    global log
    log = logging.getLogger(u'BibleManager')
    log.info(u'Bible manager loaded')

    def __init__(self, parent, config):
        """
        Finds all the bibles defined for the system and creates an interface
        object for each bible containing connection information. Throws
        Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.

        ``config``
            The plugin's configuration object.
        """
        log.debug(u'Bible Initialising')
        self.config = config
        self.parent = parent
        self.web = u'Web'
        self.db_cache = None
        self.http_cache = None
        self.http_books = {}
        self.path = self.config.get_data_path()
        self.proxy_name = self.config.get_config(u'proxy name')
        self.suffix = u'sqlite'
        self.import_wizard = None
        self.reload_bibles()
        self.media = None

    def load_http_books(self):
        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(
            filepath, u'..', u'resources', u'httpbooks.csv'))
        books_file = None
        try:
            self.http_books = []
            books_file = open(filepath, u'r')
            dialect = csv.Sniffer().sniff(books_file.read(1024))
            books_file.seek(0)
            books_reader = csv.reader(books_file, dialect)
            for line in books_reader:
                self.http_books.append({
                    u'name': unicode(line[0]),
                    u'abbr': unicode(line[1]),
                    u'test': line[2],
                    u'chap': line[3]
                })
        except:
            log.exception(u'Failed to load http books.')
        finally:
            if books_file:
                books_file.close()

    def reload_bibles(self):
        log.debug(u'Reload bibles')
        files = self.config.get_files(self.suffix)
        log.debug(u'Bible Files %s', files)
        self.db_cache = {}
        self.http_cache = {}
        self.load_http_books()
        self.web_bibles_present = False
        for filename in files:
            name, extension = os.path.splitext(filename)
            self.db_cache[name] = BibleDB(self.parent, path=self.path, name=name, config=self.config)
            # look to see if lazy load bible exists and get create getter.
            source = self.db_cache[name].get_meta(u'download source')
            if source:
                self.web_bibles_present = True
                download_name = self.db_cache[name].get_meta(u'download name').value
                web_bible = HTTPBible(self.parent, path=self.path, name=name,
                    config=self.config, download_source=source.value,
                    download_name=download_name)
                meta_proxy = self.db_cache[name].get_meta(u'proxy url')
                if meta_proxy:
                    web_bible.set_proxy_server(meta_proxy.value)
                web_bible.set_books(self.http_books)
                del self.db_cache[name]
                self.db_cache[name] = web_bible
        log.debug(u'Bibles reloaded')

    def set_process_dialog(self, wizard):
        """
        Sets the reference to the dialog with the progress bar on it.

        ``dialog``
            The reference to the import wizard.
        """
        self.import_wizard = wizard

    def import_bible(self, type, **kwargs):
        """
        Register a bible in the bible cache, and then import the verses.

        ``type``
            What type of Bible, one of the BibleFormat values.

        ``**kwargs``
            Keyword arguments to send to the actualy importer class.
        """
        class_ = BibleFormat.get_class(type)
        kwargs['path'] = self.path
        kwargs['config'] = self.config
        importer = class_(self.parent, **kwargs)
        name = importer.register(self.import_wizard)
        self.db_cache[name] = importer
        return importer.do_import()

    def get_bibles(self, mode=BibleMode.Full):
        """
        Returns a list of Books of the bible. When ``mode`` is set to
        ``BibleMode.Full`` this method returns all the Bibles for the Advanced
        Search, and when the mode is ``BibleMode.Partial`` this method returns
        all the bibles for the Quick Search.
        """
        log.debug(u'get_bibles')
        bible_list = []
        for bible_name, bible_object in self.db_cache.iteritems():
            #if getattr(bible_object, 'download_source', None):
            #    bible_name = u'%s (%s)' % (bible_name, self.web)
            bible_list.append(bible_name)
        return bible_list

    def is_bible_web(self, bible):
        pos_end = bible.find(u' (%s)' % self.web)
        if pos_end != -1:
            return True, bible[:pos_end]
        return False, bible

    def get_bible_books(self, bible):
        """
        Returns a list of the books of the bible
        """
        log.debug(u'get_bible_books')
        return [{'name': book.name, 'total': self.db_cache[bible].get_chapter_count(book.name)} for book in self.db_cache[bible].get_books()]

    def get_book_chapter_count(self, book):
        """
        Returns the number of Chapters for a given book
        """
        log.debug(u'get_book_chapter_count %s', book)
        return self.book_chapters[book]

    def get_book_verse_count(self, bible, book, chapter):
        """
        Returns all the number of verses for a given
        book and chapterMaxBibleBookVerses
        """
        log.debug(u'get_book_verse_count %s,%s,%s', bible, book, chapter)
        web, bible = self.is_bible_web(bible)
        if web:
            count = self.db_cache[bible].get_verse_count(book, chapter)
            if count == 0:
                # Make sure the first chapter has been downloaded
                self.get_verse_text(bible, book, chapter, chapter, 1, 1)
                count = self.db_cache[bible].get_verse_count(book, chapter)
            return count
        else:
            return self.db_cache[bible].get_verse_count(book, chapter)

    def get_verses(self, bible, versetext):
        """
        Returns all the number of verses for a given
        book and chapterMaxBibleBookVerses
        """
        log.debug(u'get_verses_from_text %s,%s', bible, versetext)
        reflist = parse_reference(versetext)
        web_index = bible.find('(%s)' % self.web)
        if web_index >= 0:
            bible = bible[:web_index - 1]
            log.debug('Updated bible name: %s', bible)
        #web, bible = self.is_bible_web(bible)
        #if web:
        #    return self.http_cache[bible].get_verses(reflist)
        #else:
        return self.db_cache[bible].get_verses(reflist)

    def save_meta_data(self, bible, version, copyright, permissions):
        """
        Saves the bibles meta data
        """
        log.debug(u'save_meta data %s,%s, %s,%s',
            bible, version, copyright, permissions)
        self.db_cache[bible].create_meta(u'Version', version)
        self.db_cache[bible].create_meta(u'Copyright', copyright)
        self.db_cache[bible].create_meta(u'Permissions', permissions)

    def get_meta_data(self, bible, key):
        """
        Returns the meta data for a given key
        """
        log.debug(u'get_meta %s,%s', bible, key)
        web, bible = self.is_bible_web(bible)
        return self.db_cache[bible].get_meta(key)

    def get_verse_text(self, bible, book, schapter, echapter, sverse, everse=0):
        """
        Returns a list of verses for a given Book, Chapter and ranges of verses.
        If the end verse(everse) is less then the start verse(sverse)
        then only one verse is returned

        ``bible``
            The name of the bible to be used

        Rest can be guessed at !
        """
        text = []
        self.media.setQuickMessage(u'')
        log.debug(u'get_verse_text %s,%s,%s,%s,%s,%s',
            bible, book, schapter, echapter, sverse, everse)
        # check to see if book/chapter exists fow HTTP bibles and load cache
        # if necessary
        web, bible = self.is_bible_web(bible)
        web_bible = False
        log.debug('Web Bibles: %s', self.http_cache)
        if self.http_cache[bible]:
            web_bible = True
            db_book = self.db_cache[bible].get_book(book)
            if db_book is None:
                log.debug(u'get_verse_text: new book')
                for chapter in range(schapter, echapter + 1):
                    self.media.setQuickMessage(
                        unicode(self.media.trUtf8('Downloading %s: %s')) %
                            (book, chapter))
                    search_results = \
                        self.http_cache[bible].get_chapter(bible, book, chapter)
                    if search_results and search_results.has_verselist():
                        ## We have found a book of the bible lets check to see
                        ## if it was there.  By reusing the returned book name
                        ## we get a correct book.  For example it is possible
                        ## to request ac and get Acts back.
                        bookname = search_results.get_book()
                        # check to see if book/chapter exists
                        db_book = self.db_cache[bible].get_book(bookname)
                        if db_book is None:
                            ## Then create book, chapter and text
                            db_book = self.db_cache[bible].create_book(
                                bookname, self.book_abbreviations[bookname],
                                self.book_testaments[bookname])
                            log.debug(u'New http book %s, %s, %s',
                                db_book, db_book.id, db_book.name)
                            self.db_cache[bible].create_chapter(
                                db_book.id, search_results.get_chapter(),
                                search_results.get_verselist())
                        else:
                            ## Book exists check chapter and texts only.
                            v = self.db_cache[bible].get_chapter(
                                db_book.id, chapter)
                            if v is None:
                                self.media.setQuickMessage(
                                    unicode(self.media.trUtf8('%Downloading %s: %s'))\
                                        % (book, chapter))
                                self.db_cache[bible].create_chapter(
                                    db_book.id, chapter,
                                    search_results.get_verselist())
            else:
                log.debug(u'get_verse_text : old book')
                for chapter in range(schapter, echapter + 1):
                    v = self.db_cache[bible].get_chapter(db_book.id, chapter)
                    if v is None:
                        try:
                            self.media.setQuickMessage(\
                                 unicode(self.media.trUtf8('Downloading %s: %s'))
                                         % (book, chapter))
                            search_results = \
                                self.http_cache[bible].get_chapter(
                                    bible, bookn, chapter)
                            if search_results.has_verselist():
                                self.db_cache[bible].create_chapter(
                                    db_book.id, search_results.get_chapter(),
                                    search_results.get_verselist())
                        except:
                            log.exception(u'Problem getting scripture online')
        #Now get verses from database
        if schapter == echapter:
            text = self.db_cache[bible].get_verses(
                [(book, schapter, sverse, everse)])
        else:
            verse_list = []
            for chapter in range(schapter, echapter + 1):
                if chapter == schapter:
                    start = sverse
                    end = self.get_verse_count(bible, book, chapter)
                elif chapter == echapter:
                    start = 1
                    end = everse
                else:
                    start = 1
                    end = self.get_verse_count(bible, book, chapter)
                verse_list.append((bible, chapter, start, end))
            text = self.db_cache[bible].get_verses(verse_list)
        return text

    def exists(self, name):
        """
        Check cache to see if new bible
        """
        if not isinstance(name, unicode):
            name = unicode(name)
        for bible, db_object in self.db_cache.iteritems():
            log.debug(u'Bible from cache in is_new_bible %s', bible)
            if not isinstance(bible, unicode):
                bible = unicode(bible)
            if bible == name:
                return True
        return False

