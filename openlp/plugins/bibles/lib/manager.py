# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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

import os, os.path
import sys

from bibleOSISimpl import BibleOSISImpl
from bibleCSVimpl import BibleCSVImpl
from bibleDBimpl import BibleDBImpl
from bibleHTTPimpl import BibleHTTPImpl
from openlp.plugins.bibles.lib.tables import *
from openlp.plugins.bibles.lib.classes import *

import logging

class BibleManager():
    global log
    log=logging.getLogger("BibleManager")
    log.info("Bible manager loaded")
    def __init__(self, config):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection information
        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        self.config = config
        log.debug( "Bible Initialising")
        self.bibleDBCache = None   # dict of bible database classes
        self.bibleHTTPCache = None # dict of bible http readers
        self.biblePath = self.config.get_data_path()
        self.proxyname = self.config.get_config("proxy name") #get proxy name for screen
        self.bibleSuffix = "sqlite"
        self.dialogobject = None
        self.reload_bibles()
    
    def reload_bibles(self):
        log.debug("Reload bibles")
        
        files = self.config.get_files(self.bibleSuffix)
        log.debug("Bible Files %s",  files )
        
        self.bibleDBCache = {}   
        self.bibleHTTPCache = {}
        
        for f in files:
            nme = f.split('.')
            bname = nme[0]
            self.bibleDBCache[bname] = BibleDBImpl(self.biblePath, bname, self.config)
            biblesource = self.bibleDBCache[bname].get_meta("WEB") # look to see if lazy load bible exists and get create getter.
            if biblesource:
                nhttp = BibleHTTPImpl()
                nhttp.set_bible_source(biblesource.value)  # tell The Server where to get the verses from.
                self.bibleHTTPCache[bname] = nhttp
                proxy = self.bibleDBCache[bname].get_meta("proxy") # look to see if lazy load bible exists and get create getter.
                nhttp.set_proxy(proxy)  # tell The Server where to get the verses from.
            else:
                self.bibleHTTPCache[bname] = None # makes the Full / partial code easier.
        #

        log.debug( "Bible Initialised")

    def process_dialog(self, dialogobject):
        self.dialogobject = dialogobject

    def register_http_bible(self, biblename, biblesource, mode="lazy", proxyurl=None, proxyid=None, proxypass=None):
        """
        Return a list of bibles from a given URL.
        The selected Bible can then be registered and LazyLoaded into a database
        """
        log.debug( "register_HTTP_bible %s,%s,%s,%s,%s,%s", biblename, biblesource, proxyurl,  proxyid, proxypass, mode)
        if self._is_new_bible(biblename):
            nbible = BibleDBImpl(self.biblePath, biblename, self.config) # Create new Bible
            nbible.create_tables() # Create Database
            self.bibleDBCache[biblename] = nbible

            nhttp = BibleHTTPImpl()
            nhttp.set_bible_source(biblesource)
            self.bibleHTTPCache[biblename] = nhttp
            nbible.save_meta("WEB", biblesource) # register a lazy loading interest
            if proxyurl != None:
                nbible.save_meta("proxy", proxyurl) # store the proxy URL
                nhttp.set_proxy(proxyurl)
            if proxyid != None:
                nbible.save_meta("proxyid", proxyid) # store the proxy userid
            if proxypass != None:
                nbible.save_meta("proxypass", proxypass) # store the proxy password


    def register_csv_file_bible(self, biblename, booksfile, versefile):
        """
        Method to load a bible from a set of files into a database.
        If the database exists it is deleted and the database is reloaded
        from scratch.
        """
        log.debug( "register_CSV_file_bible %s,%s,%s", biblename, booksfile, versefile)          
        if self._is_new_bible(biblename):
            nbible = BibleDBImpl(self.biblePath, biblename, self.config) # Create new Bible
            nbible.create_tables() # Create Database
            self.bibleDBCache[biblename] = nbible # cache the database for use later
            bcsv = BibleCSVImpl(nbible) # create the loader and pass in the database
            bcsv.load_data(booksfile, versefile, self.dialogobject)

    def register_osis_file_bible(self, biblename, osisfile):
        """
        Method to load a bible from a osis xml file extracted from Sword bible viewer.
        If the database exists it is deleted and the database is reloaded
        from scratch.
        """
        log.debug( "register_OSIS_file_bible %s , %s", biblename, osisfile)        
        if self._is_new_bible(biblename):
            nbible = BibleDBImpl(self.biblePath, biblename, self.config) # Create new Bible
            nbible.create_tables() # Create Database
            self.bibleDBCache[biblename] = nbible # cache the database for use later
            bcsv = BibleOSISImpl(self.biblePath, nbible) # create the loader and pass in the database
            bcsv.load_data(osisfile, self.dialogobject)

    def get_bibles(self, mode="full"):
        log.debug("get_bibles")
        """
        Returns a list of Books of the bible
        Mode "Full" - Returns all the bibles for the Queck seearch
        Mode "Partial" - Returns CSV and OSIS bbles for the Advanced Search
        """
        r=[]
        for b ,  o in self.bibleDBCache.iteritems():
            if mode == "full":
                r.append(b)
            else:
                if self.bibleHTTPCache[b] == None:  # we do not have an http bible 
                    r.append(b)
        return r

    def get_bible_books(self,bible):
        """
        Returns a list of the books of the bible from the database
        """
        log.debug("get_bible_books %s", bible)
        return self.bibleDBCache[bible].get_bible_books()

    def get_book_chapter_count(self, bible,  book):
        """
        Returns the number of Chapters for a given book
        """
        log.debug( "get_book_chapter_count %s,%s", bible, book)
        return self.bibleDBCache[bible].get_max_bible_book_chapter(book)

    def get_book_verse_count(self, bible, book, chapter):
        """
        Returns all the number of verses for a given
        book and chapterMaxBibleBookVerses
        """
        log.debug( "get_book_verse_count %s,%s,%s", bible, book,  chapter)
        return self.bibleDBCache[bible].get_max_bible_book_verses(book, chapter)

    def get_verse_from_text(self, bible, versetext):
        """
        Returns all the number of verses for a given
        book and chapterMaxBibleBookVerses
        """
        log.debug( "get_verses_from_text %s,%s", bible, versetext)
        return self.bibleDBCache[bible].get_verses_from_text(versetext)

    def save_meta_data(self, bible, version, copyright, permissions):
        """
        Saves the bibles meta data
        """
        log.debug( "save_meta data %s,%s, %s,%s", bible,  version, copyright, permissions)
        self.bibleDBCache[bible].save_meta("Version", version)
        self.bibleDBCache[bible].save_meta("Copyright", copyright)
        self.bibleDBCache[bible].save_meta("Permissions", permissions)

    def get_meta_data(self, bible, key):
        """
        Returns the meta data for a given key
        """
        log.debug( "get_meta %s,%s", bible,  key)
        return self.bibleDBCache[bible].get_meta(key)

    def get_verse_text(self, bible, bookname, schapter, echapter, sverse, everse = 0 ):
        """
        Returns a list of verses for a given Book, Chapter and ranges of verses.
        If the end verse(everse) is less then the start verse(sverse)
        then only one verse is returned
        bible        - Which bible to use.
        Rest can be guessed at !
        """
        text  = []
        bookabbrev = ""        
        log.debug( "get_verse_text %s,%s,%s,%s,%s,%s",  bible, bookname,  schapter, echapter, sverse, everse)
        if not self.bibleHTTPCache[bible] == None:
            book= self.bibleDBCache[bible].get_bible_book(bookname) # check to see if book/chapter exists
            if book == None:
                book = self.bibleDBCache[bible].create_book(bookname, bookabbrev)
            for chapter in range(schapter, echapter+1):
                v = self.bibleDBCache[bible].get_bible_chapter(book.id, chapter)
                if v == None:
                    try:
                        chaptlist = self.bibleHTTPCache[bible].get_bible_chapter(bible, book.id, bookname, chapter)
                        self.bibleDBCache[bible].create_chapter(book.id, chapter, chaptlist)
                    except :
                        log.error("Errow thrown %s", sys.exc_info()[1])                        

        if schapter == echapter:
            text = self.bibleDBCache[bible].get_bible_text(bookname, schapter, sverse, everse)
        else:
            for i in range (schapter, echapter + 1):
                if i == schapter:
                    start = sverse
                    end = self.get_book_verse_count(bible, bookname,i )[0]
                elif i == echapter:
                    start = 1
                    end = everse
                else:
                    start = 1
                    end = self.get_book_verse_count(bible, bookname,i )[0]

                txt = self.bibleDBCache[bible].get_bible_text(bookname, i, start, end)
                text.extend(txt)
        return text

    def _is_new_bible(self, name):
        """
        Check cache to see if new bible
        """
        for b ,  o in self.bibleDBCache.iteritems():
            log.debug( "Bible from cache in is_new_bible %s", b )
            if b == name :
                return False
        return True
