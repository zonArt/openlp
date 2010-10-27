# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
import re
import sqlite3
import urllib
import urllib2
from HTMLParser import HTMLParseError

from BeautifulSoup import BeautifulSoup, NavigableString

from openlp.core.lib import Receiver
from openlp.core.utils import AppLocation
from openlp.plugins.bibles.lib import SearchResults
from openlp.plugins.bibles.lib.db import BibleDB, Book

log = logging.getLogger(__name__)

class HTTPBooks(object):
    """
    A wrapper class around a small SQLite database which contains the books,
    chapter counts and verse counts for the web download Bibles. This class
    contains a singleton "cursor" so that only one connection to the SQLite
    database is ever used.
    """
    cursor = None

    @staticmethod
    def get_cursor():
        """
        Return the cursor object. Instantiate one if it doesn't exist yet.
        """
        if HTTPBooks.cursor is None:
            filepath = os.path.join(
                AppLocation.get_directory(AppLocation.PluginsDir), u'bibles',
                u'resources', u'httpbooks.sqlite')
            conn = sqlite3.connect(filepath)
            HTTPBooks.cursor = conn.cursor()
        return HTTPBooks.cursor

    @staticmethod
    def run_sql(query, parameters=()):
        """
        Run an SQL query on the database, returning the results.

        ``query``
            The actual SQL query to run.

        ``parameters``
            Any variable parameters to add to the query.
        """
        cursor = HTTPBooks.get_cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    @staticmethod
    def get_books():
        """
        Return a list of all the books of the Bible.
        """
        books = HTTPBooks.run_sql(u'SELECT id, testament_id, name, '
                u'abbreviation, chapters FROM books ORDER BY id')
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
        if not isinstance(name, unicode):
            name = unicode(name)
        name = name.title()
        books = HTTPBooks.run_sql(u'SELECT id, testament_id, name, '
                u'abbreviation, chapters FROM books WHERE name = ? OR '
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
    def get_chapter(name, chapter):
        """
        Return the chapter details for a specific chapter of a book.

        ``name``
            The name or abbreviation of a book.

        ``chapter``
            The chapter number.
        """
        if not isinstance(name, int):
            chapter = int(chapter)
        book = HTTPBooks.get_book(name)
        chapters = HTTPBooks.run_sql(u'SELECT id, book_id, chapter, '
            u'verses FROM chapters WHERE book_id = ?', (book[u'id'],))
        if chapters:
            return {
                u'id': chapters[chapter-1][0],
                u'book_id': chapters[chapter-1][1],
                u'chapter': chapters[chapter-1][2],
                u'verses': chapters[chapter-1][3]
            }
        else:
            return None

    @staticmethod
    def get_chapter_count(book):
        """
        Return the number of chapters in a book.

        ``book``
            The name or abbreviation of the book.
        """
        details = HTTPBooks.get_book(book)
        if details:
            return details[u'chapters']
        return 0

    @staticmethod
    def get_verse_count(book, chapter):
        """
        Return the number of verses in a chapter.

        ``book``
            The name or abbreviation of the book.

        ``chapter``
            The number of the chapter.
        """
        details = HTTPBooks.get_chapter(book, chapter)
        if details:
            return details[u'verses']
        return 0


class BGExtract(object):
    """
    Extract verses from BibleGateway
    """
    def __init__(self, proxyurl=None):
        log.debug(u'init %s', proxyurl)
        self.proxyurl = proxyurl

    def get_bible_chapter(self, version, bookname, chapter):
        """
        Access and decode bibles via the BibleGateway website.

        ``version``
            The version of the bible like 31 for New International version.

        ``bookname``
            Name of the Book.

        ``chapter``
            Chapter number.
        """
        log.debug(u'get_bible_chapter %s, %s, %s', version, bookname, chapter)
        url_params = urllib.urlencode(
            {u'search': u'%s %s' % (bookname, chapter),
            u'version': u'%s' % version})
        page = None
        try:
            page = urllib2.urlopen(
                u'http://www.biblegateway.com/passage/?%s' % url_params)
            log.debug(u'BibleGateway url = %s' % page.geturl())
            Receiver.send_message(u'openlp_process_events')
        except urllib2.URLError:
            log.exception(u'The web bible page could not be downloaded.')
        finally:
            if not page:
                return None
        cleaner = [(re.compile('&nbsp;|<br />'), lambda match: '')]
        soup = None
        try:
            soup = BeautifulSoup(page, markupMassage=cleaner)
        except HTMLParseError:
            log.exception(u'BeautifulSoup could not parse the bible page.')
        finally:
            if not soup:
                return None
        Receiver.send_message(u'openlp_process_events')
        footnotes = soup.findAll(u'sup', u'footnote')
        [footnote.extract() for footnote in footnotes]
        cleanup = [(re.compile('\s+'), lambda match: ' ')]
        verses = BeautifulSoup(str(soup), markupMassage=cleanup)
        content = verses.find(u'div', u'result-text-style-normal')
        verse_count = len(verses.findAll(u'sup', u'versenum'))
        found_count = 0
        verse_list = {}
        while found_count < verse_count:
            content = content.findNext(u'sup', u'versenum')
            raw_verse_num = content.next
            raw_verse_text = raw_verse_num.next
            verse_list[int(str(raw_verse_num))] = unicode(raw_verse_text)
            found_count += 1
        return SearchResults(bookname, chapter, verse_list)


class CWExtract(object):
    """
    Extract verses from CrossWalk/BibleStudyTools
    """
    def __init__(self, proxyurl=None):
        log.debug(u'init %s', proxyurl)
        self.proxyurl = proxyurl

    def get_bible_chapter(self, version, bookname, chapter):
        """
        Access and decode bibles via the Crosswalk website

        ``version``
            The version of the bible like niv for New International Version

        ``bookname``
            Text name of in english e.g. 'gen' for Genesis

        ``chapter``
            Chapter number
        """
        log.debug(u'get_bible_chapter %s,%s,%s', version, bookname, chapter)
        urlbookname = bookname.replace(u' ', u'-')
        chapter_url = u'http://www.biblestudytools.com/%s/%s/%s.html' % \
            (version, urlbookname.lower(), chapter)
        log.debug(u'URL: %s', chapter_url)
        page = None
        try:
            page = urllib2.urlopen(chapter_url)
            Receiver.send_message(u'openlp_process_events')
        except urllib2.URLError:
            log.exception(u'The web bible page could not be downloaded.')
        finally:
            if not page:
                return None
        soup = None
        try:
            soup = BeautifulSoup(page)
        except HTMLParseError:
            log.exception(u'BeautifulSoup could not parse the bible page.')
        finally:
            if not soup:
                return None
        Receiver.send_message(u'openlp_process_events')
        htmlverses = soup.findAll(u'span', u'versetext')
        verses = {}
        reduce_spaces = re.compile(r'[ ]{2,}')
        fix_punctuation = re.compile(r'[ ]+([.,;])')
        for verse in htmlverses:
            Receiver.send_message(u'openlp_process_events')
            versenumber = int(verse.contents[0].contents[0])
            versetext = u''
            for part in verse.contents:
                Receiver.send_message(u'openlp_process_events')
                if isinstance(part, NavigableString):
                    versetext = versetext + part
                elif part and part.attrMap and \
                    (part.attrMap[u'class'] == u'WordsOfChrist' or \
                    part.attrMap[u'class'] == u'strongs'):
                    for subpart in part.contents:
                        Receiver.send_message(u'openlp_process_events')
                        if isinstance(subpart, NavigableString):
                            versetext = versetext + subpart
                        elif subpart and subpart.attrMap and \
                            subpart.attrMap[u'class'] == u'strongs':
                            for subsub in subpart.contents:
                                Receiver.send_message(u'openlp_process_events')
                                if isinstance(subsub, NavigableString):
                                    versetext = versetext + subsub
            Receiver.send_message(u'openlp_process_events')
            # Fix up leading and trailing spaces, multiple spaces, and spaces
            # between text and , and .
            versetext = versetext.strip(u'\n\r\t ')
            versetext = reduce_spaces.sub(u' ', versetext)
            versetext = fix_punctuation.sub(r'\1', versetext)
            verses[versenumber] = versetext
        return SearchResults(bookname, chapter, verses)


class HTTPBible(BibleDB):
    log.info(u'%s HTTPBible loaded' , __name__)

    def __init__(self, parent, **kwargs):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection
        information

        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        BibleDB.__init__(self, parent, **kwargs)
        if u'download_source' not in kwargs:
            raise KeyError(u'Missing keyword argument "download_source"')
        if u'download_name' not in kwargs:
            raise KeyError(u'Missing keyword argument "download_name"')
        self.download_source = kwargs[u'download_source']
        self.download_name = kwargs[u'download_name']
        if u'proxy_server' in kwargs:
            self.proxy_server = kwargs[u'proxy_server']
        else:
            self.proxy_server = None
        if u'proxy_username' in kwargs:
            self.proxy_username = kwargs[u'proxy_username']
        else:
            self.proxy_username = None
        if u'proxy_password' in kwargs:
            self.proxy_password = kwargs[u'proxy_password']
        else:
            self.proxy_password = None

    def do_import(self):
        """
        Run the import. This method overrides the parent class method. Returns
        ``True`` on success, ``False`` on failure.
        """
        self.wizard.ImportProgressBar.setMaximum(2)
        self.wizard.incrementProgressBar('Registering bible...')
        self.create_meta(u'download source', self.download_source)
        self.create_meta(u'download name', self.download_name)
        if self.proxy_server:
            self.create_meta(u'proxy server', self.proxy_server)
        if self.proxy_username:
            # store the proxy userid
            self.create_meta(u'proxy username', self.proxy_username)
        if self.proxy_password:
            # store the proxy password
            self.create_meta(u'proxy password', self.proxy_password)
        self.wizard.incrementProgressBar('Registered.')
        return True

    def get_verses(self, reference_list):
        """
        A reimplementation of the ``BibleDB.get_verses`` method, this one is
        specifically for web Bibles. It first checks to see if the particular
        chapter exists in the DB, and if not it pulls it from the web. If the
        chapter DOES exist, it simply pulls the verses from the DB using the
        ancestor method.

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
        for reference in reference_list:
            log.debug('Reference: %s', reference)
            book = reference[0]
            db_book = self.get_book(book)
            if not db_book:
                book_details = self.lookup_book(book)
                if not book_details:
                    Receiver.send_message(u'bibles_nobook')
                    return []
                db_book = self.create_book(book_details[u'name'],
                    book_details[u'abbreviation'],
                    book_details[u'testament_id'])
            book = db_book.name
            if BibleDB.get_verse_count(self, book, reference[1]) == 0:
                Receiver.send_message(u'bibles_showprogress')
                Receiver.send_message(u'openlp_process_events')
                search_results = self.get_chapter(book, reference[1])
                if search_results and search_results.has_verselist():
                    ## We have found a book of the bible lets check to see
                    ## if it was there.  By reusing the returned book name
                    ## we get a correct book.  For example it is possible
                    ## to request ac and get Acts back.
                    bookname = search_results.book
                    Receiver.send_message(u'openlp_process_events')
                    # check to see if book/chapter exists
                    db_book = self.get_book(bookname)
                    self.create_chapter(db_book.id, search_results.chapter,
                        search_results.verselist)
                    Receiver.send_message(u'openlp_process_events')
                Receiver.send_message(u'bibles_hideprogress')
            Receiver.send_message(u'openlp_process_events')
        return BibleDB.get_verses(self, reference_list)

    def get_chapter(self, book, chapter):
        """
        Receive the request and call the relevant handler methods.
        """
        log.debug(u'get_chapter %s, %s', book, chapter)
        log.debug(u'source = %s', self.download_source)
        if self.download_source.lower() == u'crosswalk':
            ev = CWExtract(self.proxy_server)
        else:
            ev = BGExtract(self.proxy_server)
        return ev.get_bible_chapter(self.download_name, book, chapter)

    def get_books(self):
        """
        Return the list of books.
        """
        return [Book.populate(name=book['name'])
            for book in HTTPBooks.get_books()]

    def lookup_book(self, book):
        """
        Look up the name of a book.
        """
        return HTTPBooks.get_book(book)

    def get_chapter_count(self, book):
        """
        Return the number of chapters in a particular book.
        """
        return HTTPBooks.get_chapter_count(book)

    def get_verse_count(self, book, chapter):
        """
        Return the number of verses for the specified chapter and book.

        ``book``
            The name of the book.

        ``chapter``
            The chapter whose verses are being counted.
        """
        return HTTPBooks.get_verse_count(book, chapter)
