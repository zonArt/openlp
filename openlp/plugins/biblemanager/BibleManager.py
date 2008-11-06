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
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..', '..')))

from openlp.utils import ConfigHelper
from openlp.plugins.biblemanager.BibleDBImpl import BibleDBImpl
from openlp.plugins.biblemanager.BibleHTTPImpl import BibleHTTPImpl
from openlp.plugins.plugin import Plugin

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

class BibleManager(Plugin):
    global log     
    log=logging.getLogger("BibleMgr")
    log.info("Bible manager loaded")
    def __init__(self):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection information
        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """ 
        log.debug( "Bible Initialising")
        self.bibleDBCache = {}
        self.bibleHTTPCache = {}
        self.booksOfBible = {}
        self.listOfBooks = []
        self.booksChapters = {}
        self.CWids = {}
        self.verses = {}
        self.verseData = {}
        self.biblePath = ConfigHelper.getBiblePath()
        #log.debug( self.biblePath )
        files = os.listdir(self.biblePath)
        fbibles=open("../resources/bibles_en.txt", 'r')
        fbibledata=open("../resources/bible_books.txt", 'r')
        for f in files:
            b = f.split('.')[0]
            self.bibleDBCache[b] = BibleDBImpl(b)
            biblesource = self.bibleDBCache[b].getMeta("WEB") # look to see if lazy load bible and get create getter.
            if biblesource:
               nhttp = BibleHTTPImpl()
               nhttp.setBibleSource(biblesource)
               self.bibleHTTPCache[b] = nhttp
            #   
        #Load in memory objects
        for line in fbibles:
            p = line.split(",")
            self.booksOfBible[p[0]] = p[1].replace('\n', '')
            self.listOfBooks.insert(int(p[1].replace('\n', '')),  p[0])                
        for line in fbibledata:
            p = line.split(",")
            self.booksChapters[p[0]]=p[1]
            self.CWids[p[0]]=p[2].replace('\n', '')    
            v = p[3].replace('\n', '')  
            self.verseData[p[0]] = v
        #log.debug( "\nbooks of the Bible", self.booksOfBible)
        #log.debug( "\n", self.booksChapters)
        #log.debug( "\n", self.CWids)
        #log.debug( "\n", self.verseData)

        #log.debug( self.bibleDBCache)
        #log.debug( self.bibleHTTPCache   )
        log.debug( "Bible Initialised")     

    def registerHTTPBible(self, biblename, biblesource, proxy, proxyport, proxyid, proxypass):
        """
        Return a list of bibles from a given URL.  
        The selected Bible can then be registered and LazyLoaded into a database
        """
        if self._isNewBible(biblename):
            nbible = BibleDBImpl(biblename) # Create new Bible
            nbible.createTables() # Create Database
            self.bibleDBCache[biblename] = nbible 

            nhttp = BibleHTTPImpl()
            nhttp.setBibleSource(biblesource)
            self.bibleHTTPCache[biblename] = nhttp
            nbible.loadMeta("WEB", biblesource) # register a lazy loading interest
            
    def registerFileBible(self, biblename, booksfile, versefile):
        """
        Method to load a bible from a set of files into a database.
        If the database exists it is deleted and the database is reloaded 
        from scratch.
        """
        if self._isNewBible(biblename):
            nbible = BibleDBImpl(biblename) # Create new Bible
            nbible.createTables() # Create Database
            nbible.loadData(booksfile, versefile)
            self.bibleDBCache[biblename] = nbible 
            
    def loadBible(self,biblename):
        log.debug( "loadBible %s", biblename)
        """
        Downloads all the books of the bible 
        and loads it into the database
        """        
        for bookname in self.listOfBooks:
            cptrs = self.booksChapters[ self.booksOfBible[bookname]] 
            log.debug( "book and chapter %s %s", bookname , self.booksChapters[ self.booksOfBible[bookname]] )
            for chptr in range(1 , int(cptrs)):  # loop through all the chapters in book
                c = self.bibleDBCache[biblename].getBibleChapter(bookname, chptr) # check to see if book/chapter exists
                log.debug( "got chapter %s", c)
                if not c:
                    log.debug( "missing %s,%s", bookname, chptr)
                    self._loadBook(biblename,bookname)
                    self._loadChapter(biblename, bookname, chptr)
    
    def getBibles(self):
        """
        Returns a list of Books of the bible
        """
        r=[]
        for b ,  o in self.bibleDBCache.iteritems():
            r.append(b)
        return r

    def getBibleBooks(self,bible):
        """
        Returns a list of the books of the bible
        """        
        return self.listOfBooks
        
    def getBookChapterCount(self, book):
        log.debug( "getBookChapterCount %s", book)
        """
        Returns all the number of Chapters for a given
        book
        """
        bookid = self.booksOfBible[book]
        return self.booksChapters[bookid]

    def getBookVerseCount(self, book, chapter):
        log.debug( "getBookVerseCount %s,%s", book,  chapter)
        """
        Returns all the number of verses for a given
        book and chapter
        """
        bookid = self.booksOfBible[book]
        v = self.verseData[bookid].split(":")
        log.debug( v)
        return v[chapter-1] # sub 1 for zero indexing

    def getVerseText(self, bible, bookname,  chapter, sverse, everse = 0 ):
        """
        Returns a list of verses for a given Book, Chapter and ranges of verses.
        If the end verse(everse) is less then the start verse(sverse)
        then only one verse is returned
        Bible - Which bible
        Book - full text description so needs to be converted.
        Rest can be guessed at !
        """
        #log.debug( self.bibleDBCache)
        #log.debug( self.bibleHTTPCache)
        log.debug( "getchapter %s,%s,%s,%s,%s",  bible, bookname,  chapter, sverse, everse)
        bookid = self.booksOfBible[bookname] # convert to id  ie Genesis --> 1  Revelation --> 73 
        # SORT OUT BOOKNAME BOOK ID.  
        # NAME COMES IN TO ID AND BACK TO NAME ?
        c = self.bibleDBCache[bible].getBibleChapter(bookname, chapter) # check to see if book/chapter exists
        bookabbrev = ""
        log.debug( "Bible Chapter %s", c )
        if not c:
            self._loadBook(bible,bookid, bookname, bookabbrev)
            self._loadChapter(bible, bookid,bookname, chapter)
        if everse < sverse:
            everse = sverse
        text = self.bibleDBCache[bible].getBibleText(bookname, chapter, sverse, everse)
        #log.debug( text)
        #self.bibleDBCache[bible].dumpBible()
        return text
        
    def _loadBook(self, bible, bookid, bookname, bookabbrev):
        log.debug( "loadbook %s,%s,%s,%s", bible, bookid, bookname, bookabbrev)
        cl = self.bibleDBCache[bible].getBibleBook(bookname)
        log.debug( "get bible book %s" , cl)
        if not cl :
            self.bibleDBCache[bible].createBook(bookid, bookname, bookabbrev)
        
    def _loadChapter(self, bible, bookid,bookname, chapter):
        log.debug( "loadChapter %s,%s,%s,%s", bible, bookid,bookname, chapter) 
        try :
            print self.bibleHTTPCache[bible]
            chaptlist = self.bibleHTTPCache[bible].getBibleChapter(bible, bookid,bookname, chapter)
            self.bibleDBCache[bible].createChapter(bookname, chapter, chaptlist)
        except:
            log.error("Bible %s not found in Http cache", bible)
        
    def _isNewBible(self, name):
        """
        Check cache to see if new bible
        """
        for b ,  o in self.bibleDBCache.iteritems():
            log.debug( b )
            if b == name : 
                return False
        return True
