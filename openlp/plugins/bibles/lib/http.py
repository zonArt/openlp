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
import urllib2

from BeautifulSoup import BeautifulSoup

from common import BibleCommon, SearchResults
from db import BibleDB
from openlp.plugins.bibles.lib.models import Book

class BGExtract(BibleCommon):
    global log
    log = logging.getLogger(u'BibleHTTPMgr(BG_extract)')
    log.info(u'BG_extract loaded')

    def __init__(self, proxyurl=None):
        log.debug(u'init %s', proxyurl)
        self.proxyurl = proxyurl

    def get_chapter(self, version, bookname, chapter) :
        """
        Access and decode bibles via the BibleGateway website

        ``Version``
            The version of the bible like 31 for New International version

        ``bookname``
            Name of the Book

        ``chapter``
            Chapter number
        """
        log.debug(u'get_bible_chapter %s, %s, %s', version, bookname, chapter)
        urlstring = u'http://www.biblegateway.com/passage/?search=%s+%s' \
            u'&version=%s' % (bookname, chapter, version)
        log.debug(u'BibleGateway url = %s' % urlstring)
        xml_string = self._get_web_text(urlstring, self.proxyurl)
        verseSearch = u'<sup class=\"versenum'
        verseFootnote = u'<sup class=\'footnote'
        verse = 1
        i = xml_string.find(u'result-text-style-normal') + 26
        xml_string = xml_string[i:len(xml_string)]
        versePos = xml_string.find(verseSearch)
        bible = {}
        while versePos > -1:
            # clear out string
            verseText = u''
            versePos = xml_string.find(u'</sup>', versePos) + 6
            i = xml_string.find(verseSearch, versePos + 1)
            # Not sure if this is needed now
            if i == -1:
                i = xml_string.find(u'</div', versePos + 1)
                j = xml_string.find(u'<strong', versePos + 1)
                if j > 0 and j < i:
                    i = j
                verseText = xml_string[versePos + 7 : i ]
                # store the verse
                bible[verse] = self._clean_text(verseText)
                versePos = -1
            else:
                verseText = xml_string[versePos: i]
                start_tag = verseText.find(verseFootnote)
                while start_tag > -1:
                    end_tag = verseText.find(u'</sup>')
                    verseText = verseText[:start_tag] + verseText[end_tag + 6:len(verseText)]
                    start_tag = verseText.find(verseFootnote)
                # Chop off verse and start again
                xml_string = xml_string[i:]
                #look for the next verse
                versePos = xml_string.find(verseSearch)
                # store the verse
                bible[verse] = self._clean_text(verseText)
                verse += 1
        return SearchResults(bookname, chapter, bible)

class CWExtract(BibleCommon):
    log.info(u'%s loaded', __name__)

    def __init__(self, proxyurl=None):
        log.debug(u'init %s', proxyurl)
        self.proxyurl = proxyurl

    def get_bible_chapter(self, version, bookname, chapter):
        log.debug(u'%s %s, %s, %s', __name__, version, bookname, chapter)
        """
        Access and decode bibles via the Crosswalk website

        ``version``
            The version of the bible like niv for New International Version

        ``bookname``
            Text name of in english e.g. 'gen' for Genesis

        ``chapter``
            Chapter number
        """
        log.debug(u'get_bible_chapter %s,%s,%s',
            version, bookname, chapter)
        bookname = bookname.replace(u' ', u'')
        page = urllib2.urlopen(u'http://www.biblestudytools.com/%s/%s/%s.html' % \
            (version, bookname.lower(), chapter))
        soup = BeautifulSoup(page)
        htmlverses = soup.findAll(u'span', u'versetext')
        verses = {}
        for verse in htmlverses:
            versenumber = int(verse.contents[0].contents[0])
            versetext = u''
            for part in verse.contents:
                if str(part)[0] != u'<':
                    versetext = versetext + part
            versetext = versetext.strip(u'\n\r\t ')
            verses[versenumber] = versetext
        return SearchResults(bookname, chapter, verses)


class HTTPBible(BibleDB):
    log.info(u'%s loaded', __name__)

    def __init__(self, **kwargs):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection
        information

        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        BibleDB.__init__(self, **kwargs)
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
                db_book = self.create_book(book_details[u'name'],
                    book_details[u'abbr'], book_details[u'test'])
            book = db_book.name
            if self.get_verse_count(book, reference[1]) == 0:
                search_results = self.get_chapter(self.name, book, reference[1])
                if search_results and search_results.has_verselist():
                    ## We have found a book of the bible lets check to see
                    ## if it was there.  By reusing the returned book name
                    ## we get a correct book.  For example it is possible
                    ## to request ac and get Acts back.
                    bookname = search_results.get_book()
                    # check to see if book/chapter exists
                    db_book = self.get_book(bookname)
                    self.create_chapter(db_book.id, search_results.get_chapter(),
                        search_results.get_verselist())
        return BibleDB.get_verses(self, reference_list)

    def get_chapter(self, version, book, chapter):
        """
        Receive the request and call the relevant handler methods
        """
        log.debug(u'get_chapter %s, %s, %s', version, book, chapter)
        log.debug(u'source = %s', self.download_source)
        try:
            if self.download_source.lower() == u'crosswalk':
                ev = CWExtract(self.proxy_server)
            else:
                ev = BGExtract(self.proxy_server)
            return ev.get_bible_chapter(self.download_name, book, chapter)
        except:
            log.exception("Failed to get bible chapter")
            return None

    def get_books(self):
        return [Book.populate(name=self.books[book]['name']) for book in self.books]

    def get_chapter_count(self, book):
        return self.books[book][u'chap']

    def set_proxy_server(self, server):
        self.proxy_server = server

    def set_books(self, books):
        self.books = books

    def lookup_book(self, book):
        log.debug('Looking up "%s" in %s', (book, self.books))
        if book in self.books:
            return self.books[book]
        else:
            for details in self.books:
                if details[u'abbr'] == book:
                    return details
            return None

