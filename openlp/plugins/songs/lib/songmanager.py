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

from songDBimpl import SongDBImpl


import logging

class SongManager():
    global log
    log=logging.getLogger("SongManager")
    log.info("Song manager loaded")
    def __init__(self, config):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection information
        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        self.config = config
        log.debug( "Song Initialising")
        self.authorcache = None
        self.songPath = self.config.get_data_path()
        self.songSuffix = self.config.get_config("suffix name", u'olp3,sqlite')
        log.debug("Song Path %s and suffix %s",  self.songPath, self.songSuffix )
        self.dialogobject = None
        
        files = self.config.get_files()
        if len(files) > 0:
            log.debug("Song File %s",  files )
            self.songDBCache = SongDBImpl(self.songPath, self.songSuffix)

        log.debug( "Song Initialised")

    def process_dialog(self, dialogobject):
        self.dialogobject = dialogobject

    def get_song(self, songid):
        """
        Returns the details of a song
        """
        return self.songDBCache.get_song(songid)
    
    def get_authors(self, reload=False):
        """
        Returns a list of all the authors
        """
        if self.authorcache == None or reload == True:
            self.authorcache = self.songDBCache.get_authors()
        return self.authorcache
        
    def get_author(self, authorid):
        """
        Details of the Author
        """
        return self.songDBCache.get_author(authorid)

    def save_author(self, author_name, first_name, last_name, id = 0):
        """
        Save the Author and refresh the cache
        """
        if id == 0:
            self.songDBCache.add_author(author_name, first_name,  last_name)
        else: 
            self.songDBCache.update_author(id, author_name, first_name,  last_name)
        self.get_authors(True) # Updates occured refresh the cache
        return True
        
    def delete_author(self, authorid):
        """
        Delete the author and refresh the author cache
        """
        self.songDBCache.delete_author(authorid)        
        self.get_authors(True) # Updates occured refresh the cache
        return True

    def get_song_authors_for_author(self, authorid):
        """
        Returns the details of a song
        """
        return self.songDBCache.get_song_authors_for_author(authorid)        
        
    def get_song_authors_for_song(self, songid):
        """
        Returns the details of a song
        """
        return self.songDBCache.get_song_authors_for_song(songid)        

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
        log.debug( "save_meta %s,%s, %s,%s", bible,  version, copyright, permissions)
        self.bibleDBCache[bible].save_meta("Version", version)
        self.bibleDBCache[bible].save_meta("Copyright", copyright)
        self.bibleDBCache[bible].save_meta("Permissins", permissions)

    def get_meta_data(self, bible, key):
        """
        Returns the meta data for a given key
        """
        log.debug( "get_meta %s,%s", bible,  key)
        self.bibleDBCache[bible].get_meta(key)

    def get_verse_text(self, bible, bookname, schapter, echapter, sverse, everse = 0 ):
        """
        Returns a list of verses for a given Book, Chapter and ranges of verses.
        If the end verse(everse) is less then the start verse(sverse)
        then only one verse is returned
        bible        - Which bible to use.
        Rest can be guessed at !
        """
        text  = []
        #log.debug( self.bibleDBCache)
        #log.debug( self.bibleHTTPCache)
        log.debug( "get_verse_text %s,%s,%s,%s,%s,%s",  bible,bookname,  schapter,echapter, sverse, everse)
#        bookid = self.booksOfBible[bookname] # convert to id  ie Genesis --> 1  Revelation --> 73
#        # SORT OUT BOOKNAME BOOK ID.
#        # NAME COMES IN TO ID AND BACK TO NAME ?
#        c = self.bibleDBCache[bible].getBibleChapter(bookname, chapter) # check to see if book/chapter exists
#        bookabbrev = ""
#        log.debug( "Bible Chapter %s", c )
#        if not c:
#            self._loadBook(bible,bookid, bookname, bookabbrev)
#            self._loadChapter(bible, bookid,bookname, chapter)
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

    def _load_book(self, bible, bookid, bookname, bookabbrev):
        log.debug( "load_book %s,%s,%s,%s", bible, bookid, bookname, bookabbrev)
        cl = self.bibleDBCache[bible].get_bible_book(bookname)
        log.debug( "get bible book %s" , cl)
        if not cl :
            self.bibleDBCache[bible].create_book(bookid, bookname, bookabbrev)

    def _loadChapter(self, bible, bookid, bookname, chapter):
        log.debug( "load_chapter %s,%s,%s,%s", bible, bookid,bookname, chapter)
        try :
            chaptlist = self.bibleHTTPCache[bible].get_bible_chapter(bible, bookid,bookname, chapter)
            self.bibleDBCache[bible].create_chapter(bookname, chapter, chaptlist)
        except :
            log.error("Errow thrown %s", sys.exc_info()[1])

    def _is_new_bible(self, name):
        """
        Check cache to see if new bible
        """
        for b ,  o in self.bibleDBCache.iteritems():
            log.debug( b )
            if b == name :
                return False
        return True
        
    def get_song_from_title(self,searchtext):
        log.debug("get song from title %s", searchtext)
        return self.songDBCache.get_song_from_title(searchtext)
        
    def get_song_from_lyrics(self,searchtext):
        log.debug("get song from lyrics %s", searchtext)        
        return self.songDBCache.get_song_from_lyrics(searchtext) 
                
    def get_song_from_author(self,searchtext):
        log.debug("get song from author %s", searchtext)        
        return self.songDBCache.get_song_from_author(searchtext)        
        
    def dump_songs(self):
        self.songDBCache.dump_songs()
