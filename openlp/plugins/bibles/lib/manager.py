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

import logging
import os

from bibleOSISimpl import BibleOSISImpl
from bibleCSVimpl import BibleCSVImpl
from bibleDBimpl import BibleDBImpl
from bibleHTTPimpl import BibleHTTPImpl

class BibleMode(object):
    Full = 1
    Partial = 2

class BibleManager(object):
    """
    The Bible manager which holds and manages all the Bibles.
    """
    global log
    log = logging.getLogger(u'BibleManager')
    log.info(u'Bible manager loaded')

    def __init__(self, config):
        """
        Finds all the bibles defined for the system and creates an
        interface object for each bible containing connection
        information. Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.

        ``config``
            The plugin's configuration object.
        """
        self.config = config
        log.debug(u'Bible Initialising')
        self.web = u'Web'
        # dict of bible database objects
        self.bible_db_cache = None
        # dict of bible http readers
        self.bible_http_cache = None
        self.biblePath = self.config.get_data_path()
        #get proxy name for screen
        self.proxyname = self.config.get_config(u'proxy name')
        self.bibleSuffix = u'sqlite'
        self.dialogobject = None
        self.reload_bibles()
        self.media = None

    def reload_bibles(self):
        log.debug(u'Reload bibles')
        files = self.config.get_files(self.bibleSuffix)
        log.debug(u'Bible Files %s', files )
        self.bible_db_cache = {}
        self.bible_http_cache = {}
        # books of the bible with testaments
        self.book_testaments = {}
        # books of the bible with chapter count
        self.book_chapters = []
        # books of the bible with abbreviation
        self.book_abbreviations = {}
        self.web_bibles_present = False
        for f in files:
            nme = f.split(u'.')
            bname = nme[0]
            self.bible_db_cache[bname] = BibleDBImpl(self.biblePath,
                bname, self.config)
            # look to see if lazy load bible exists and get create getter.
            biblesource = self.bible_db_cache[bname].get_meta(u'WEB')
            if biblesource:
                self.web_bibles_present = True
                nhttp = BibleHTTPImpl()
                # tell The Server where to get the verses from.
                nhttp.set_bible_source(biblesource.value)
                self.bible_http_cache [bname] = nhttp
                # look to see if lazy load bible exists and get create getter.
                meta = self.bible_db_cache[bname].get_meta(u'proxy')
                proxy = None
                if meta:
                    proxy = meta.value
                    # tell The Server where to get the verses from.
                nhttp.set_proxy(proxy)
                # look to see if lazy load bible exists and get create getter.
                bibleid = self.bible_db_cache[bname].get_meta(u'bibleid').value
                # tell The Server where to get the verses from.
                nhttp.set_bibleid(bibleid)
            else:
                # makes the Full / partial code easier.
                self.bible_http_cache [bname] = None
            if self.web_bibles_present:
                # books of the bible linked to bibleid {osis, name}
                self.book_testaments = {}
                # books of the bible linked to bibleid {osis, abbrev}
                self.book_abbreviations = {}
                filepath = os.path.split(os.path.abspath(__file__))[0]
                filepath = os.path.abspath(os.path.join(
                    filepath, u'..', u'resources',u'httpbooks.csv'))
                fbibles = open(filepath, u'r')
                for line in fbibles:
                    p = line.split(u',')
                    self.book_abbreviations[p[0]] = p[1].replace(u'\n', '')
                    self.book_testaments[p[0]] = p[2].replace(u'\n', '')
                    self.book_chapters.append({u'book':p[0], u'total':p[3].replace(u'\n', '')})
        log.debug(u'Bible Initialised')

    def process_dialog(self, dialogobject):
        """
        Sets the reference to the dialog with the progress bar on it.

        ``dialogobject``
            The reference to the dialog.
        """
        self.dialogobject = dialogobject

    def register_http_bible(self, biblename, biblesource, bibleid,
                            proxyurl=None, proxyid=None, proxypass=None):
        """
        Return a list of bibles from a given URL. The selected Bible
        can then be registered and LazyLoaded into a database.

        ``biblename``
            The name of the bible to register.

        ``biblesource``
            Where this Bible stores it's verses.

        ``bibleid``
            The identifier for a Bible.

        ``proxyurl``
            Defaults to *None*. An optional URL to a proxy server.

        ``proxyid``
            Defaults to *None*. A username for logging into the proxy
            server.

        ``proxypass``
            Defaults to *None*. The password to accompany the username.
        """
        log.debug(u'register_HTTP_bible %s, %s, %s, %s, %s, %s',
            biblename, biblesource, bibleid, proxyurl, proxyid, proxypass)
        if self._is_new_bible(biblename):
            # Create new Bible
            nbible = BibleDBImpl(self.biblePath, biblename, self.config)
            # Create Database
            nbible.create_tables()
            self.bible_db_cache[biblename] = nbible
            nhttp = BibleHTTPImpl()
            nhttp.set_bible_source(biblesource)
            self.bible_http_cache [biblename] = nhttp
            # register a lazy loading interest
            nbible.save_meta(u'WEB', biblesource)
            # store the web id of the bible
            nbible.save_meta(u'bibleid', bibleid)
            if proxyurl:
                # store the proxy URL
                nbible.save_meta(u'proxy', proxyurl)
                nhttp.set_proxy(proxyurl)
            if proxyid:
                # store the proxy userid
                nbible.save_meta(u'proxyid', proxyid)
            if proxypass:
                # store the proxy password
                nbible.save_meta(u'proxypass', proxypass)
            return True
        else:
            log.debug(u'register_http_file_bible %s not created already exists',
                biblename)
            return False

    def register_csv_file_bible(self, biblename, booksfile, versefile):
        """
        Method to load a bible from a set of files into a database.
        If the database exists it is deleted and the database is reloaded
        from scratch.
        """
        log.debug(u'register_CSV_file_bible %s,%s,%s',
            biblename, booksfile, versefile)
        if self._is_new_bible(biblename):
            # Create new Bible
            nbible = BibleDBImpl(self.biblePath, biblename, self.config)
            # Create database
            nbible.create_tables()
            # Cache the database for use later
            self.bible_db_cache[biblename] = nbible
            # Create the loader and pass in the database
            bcsv = BibleCSVImpl(nbible)
            bcsv.load_data(booksfile, versefile, self.dialogobject)
            return True
        else:
            log.debug(u'register_csv_file_bible %s not created already exists',
                biblename)
            return False

    def register_osis_file_bible(self, biblename, osisfile):
        """
        Method to load a bible from a osis xml file extracted from Sword bible
        viewer.  If the database exists it is deleted and the database is
        reloaded from scratch.
        """
        log.debug(u'register_OSIS_file_bible %s, %s', biblename, osisfile)
        if self._is_new_bible(biblename):
            # Create new Bible
            nbible = BibleDBImpl(self.biblePath, biblename, self.config)
            # Create Database
            nbible.create_tables()
            # Cache the database for use later
            self.bible_db_cache[biblename] = nbible
            # Create the loader and pass in the database
            bcsv = BibleOSISImpl(self.biblePath, nbible)
            bcsv.load_data(osisfile, self.dialogobject)
            return True
        else:
            log.debug(
                u'register_OSIS_file_bible %s, %s not created already exists',
                biblename, osisfile)
            return False

    def get_bibles(self, mode=BibleMode.Full):
        """
        Returns a list of Books of the bible. When ``mode`` is set to
        ``BibleMode.Full`` this method returns all the Bibles for the
        Advanced Search, and when the mode is ``BibleMode.Partial``
        this method returns all the bibles for the Quick Search.
        """
        log.debug(u'get_bibles')
        bible_list = []
        for bible_name, bible_object in self.bible_db_cache.iteritems():
            if self.bible_http_cache[bible_name]:
                bible_name = u'%s (%s)' % (bible_name, self.web)
            bible_list.append(bible_name)
        return bible_list

    def is_bible_web(self, bible):
        pos_end = bible.find(u' (%s)' % self.web)
        if pos_end != -1:
            return True, bible[:pos_end]
        return False, bible

    def get_bible_books(self):
        """
        Returns a list of the books of the bible
        """
        log.debug(u'get_bible_books')
        return self.book_chapters

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
            count = self.bible_db_cache[bible].get_max_bible_book_verses(
                    book, chapter)
            if count == 0:
                # Make sure the first chapter has been downloaded
                self.get_verse_text(bible, book, chapter, chapter, 1, 1)
                count = self.bible_db_cache[bible].get_max_bible_book_verses(
                    book, chapter)
            return count
        else:
            return self.bible_db_cache[bible].get_max_bible_book_verses(
                book, chapter)

    def get_verse_from_text(self, bible, versetext):
        """
        Returns all the number of verses for a given
        book and chapterMaxBibleBookVerses
        """
        log.debug(u'get_verses_from_text %s,%s', bible, versetext)
        web, bible = self.is_bible_web(bible)
        return self.bible_db_cache[bible].get_verses_from_text(versetext)

    def save_meta_data(self, bible, version, copyright, permissions):
        """
        Saves the bibles meta data
        """
        log.debug(u'save_meta data %s,%s, %s,%s',
            bible, version, copyright, permissions)
        self.bible_db_cache[bible].save_meta(u'Version', version)
        self.bible_db_cache[bible].save_meta(u'Copyright', copyright)
        self.bible_db_cache[bible].save_meta(u'Permissions', permissions)

    def get_meta_data(self, bible, key):
        """
        Returns the meta data for a given key
        """
        log.debug(u'get_meta %s,%s', bible, key)
        web, bible = self.is_bible_web(bible)
        return self.bible_db_cache[bible].get_meta(key)

    def get_verse_text(self, bible, bookname, schapter, echapter, sverse,
        everse=0):
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
            bible, bookname, schapter, echapter, sverse, everse)
        # check to see if book/chapter exists fow HTTP bibles and load cache
        # if necessary
        web, bible = self.is_bible_web(bible)
        if self.bible_http_cache[bible]:
            book = self.bible_db_cache[bible].get_bible_book(bookname)
            if book is None:
                log.debug(u'get_verse_text : new book')
                for chapter in range(schapter, echapter + 1):
                    self.media.setQuickMessage(
                        unicode(self.media.trUtf8(u'Downloading %s: %s')) %
                            (bookname, chapter))
                    search_results = \
                        self.bible_http_cache[bible].get_bible_chapter(
                            bible, bookname, chapter)
                    if search_results.has_verselist() :
                        ## We have found a book of the bible lets check to see
                        ## if it was there.  By reusing the returned book name
                        ## we get a correct book.  For example it is possible
                        ## to request ac and get Acts back.
                        bookname = search_results.get_book()
                        # check to see if book/chapter exists
                        book = self.bible_db_cache[bible].get_bible_book(
                            bookname)
                        if book is None:
                            ## Then create book, chapter and text
                            book = self.bible_db_cache[bible].create_book(
                                bookname, self.book_abbreviations[bookname],
                                self.book_testaments[bookname])
                            log.debug(u'New http book %s, %s, %s',
                                book, book.id, book.name)
                            self.bible_db_cache[bible].create_chapter(
                                book.id, search_results.get_chapter(),
                                search_results.get_verselist())
                        else:
                            ## Book exists check chapter and texts only.
                            v = self.bible_db_cache[bible].get_bible_chapter(
                                book.id, chapter)
                            if v is None:
                                self.media.setQuickMessage(
                                    unicode(self.media.trUtf8(u'%Downloading %s: %s'))\
                                        % (bookname, chapter))
                                self.bible_db_cache[bible].create_chapter(
                                    book.id, chapter,
                                    search_results.get_verselist())
            else:
                log.debug(u'get_verse_text : old book')
                for chapter in range(schapter, echapter + 1):
                    v = self.bible_db_cache[bible].get_bible_chapter(
                        book.id, chapter)
                    if v is None:
                        try:
                            self.media.setQuickMessage(\
                                 unicode(self.media.trUtf8(u'Downloading %s: %s'))
                                         % (bookname, chapter))
                            search_results = \
                                self.bible_http_cache[bible].get_bible_chapter(
                                    bible, bookname, chapter)
                            if search_results.has_verselist():
                                self.bible_db_cache[bible].create_chapter(
                                    book.id, search_results.get_chapter(),
                                    search_results.get_verselist())
                        except:
                            log.exception(u'Problem getting scripture online')
        #Now get verses from database
        if schapter == echapter:
            text = self.bible_db_cache[bible].get_bible_text(bookname,
                schapter, sverse, everse)
        else:
            for i in range (schapter, echapter + 1):
                if i == schapter:
                    start = sverse
                    end = self.get_book_verse_count(bible, bookname, i)
                elif i == echapter:
                    start = 1
                    end = everse
                else:
                    start = 1
                    end = self.get_book_verse_count(bible, bookname, i)

                txt = self.bible_db_cache[bible].get_bible_text(
                    bookname, i, start, end)
                text.extend(txt)
        return text

    def _is_new_bible(self, name):
        """
        Check cache to see if new bible
        """
        for bible, o in self.bible_db_cache.iteritems():
            log.debug(u'Bible from cache in is_new_bible %s', bible)
            if bible == name:
                return False
        return True
