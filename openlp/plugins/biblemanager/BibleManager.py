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

class BibleManager:
    def __init__(self):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection information
        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """ 
        self.bibleDBCache = {}
        self.bibleHTTPCache = {}
        self.booksOfBible = {}
        self.listOfBooks = []
        self.booksChapters = {}
        self.CWids = {}
        self.verses = {}
        self.verseData = {}
        self.biblePath = ConfigHelper.getBiblePath()
        #print self.biblePath
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
            #print "\n", self.booksOfBible
            #print "\n", self.booksChapters
            #print "\n", self.CWids
            #print "\n", self.verseData

        #print self.bibleDBCache
        #print self.bibleHTTPCache        

    def registerHTTPBible(self, name, biblesource, proxy, proxyport, proxyid, proxypass):
        """
        Return a list of bibles from a given URL.  
        The selected Bible can then be registered and LazyLoaded into a database
        """
        if self._isNewBible(name):
            nbible = BibleDBImpl(name) # Create new Bible
            nbible.createTables() # Create Database
            self.bibleDBCache[name] = nbible 

            nhttp = BibleHTTPImpl()
            nhttp.setBibleSource(biblesource)
            self.bibleHTTPCache[name] = nhttp
            nbible.loadMeta("WEB", biblesource)
            
    def registerBible(self, name, booksfile, versefile):
        """
        Method to load a bible from a set of files into a database.
        If the database exists it is deleted and the database is reloaded 
        from scratch.
        """
        if self._isNewBible(name):
            nbible = BibleDBImpl(name) # Create new Bible
            nbible.createTables() # Create Database
            nbible.loadData(booksfile, versefile)
            self.bibleDBCache[name] = nbible 
    
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
        print "getBookChapterCount ", book
        """
        Returns all the number of Chapters for a given
        book
        """
        i = self.booksOfBible[book]
        return self.booksChapters[i]

    def getBookVerseCount(self, book, chapter):
        print "getBookVerseCount ", book,  chapter
        """
        Returns all the number of verses for a given
        book and chapter
        """
        i = self.booksOfBible[book]
        v = self.verseData[i].split(":")
        print v
        return v[chapter-1] # sup 1 for zero indexing

    def getVerseText(self, bible, book,  chapter, sverse, everse = 0 ):
        """
        Returns a list of verses for a given Book, Chapter and ranges of verses.
        If the end verse(everse) is less then the start verse(sverse)
        then only one verse is returned
        """
        #print self.bibleDBCache
        #print self.bibleHTTPCache
        print "getchapter ",  bible, book,  chapter, sverse, everse 
        c = self.bibleDBCache[bible].getBibleChapter(book, chapter) # check to see if book/chapter exists
        print c
        if not c:
            self._loadBook(bible,book)
            self._loadChapter(bible, book, chapter)
        if everse < sverse:
            everse = sverse
        text = self.bibleDBCache[bible].getBibleText(book, chapter, sverse, everse)
        #print text
        #self.bibleDBCache[bible].dumpBible()
        return text
        
    def _loadBook(self, bible, book):
        print "loadbook ", bible, book
        cl = self.bibleDBCache[bible].getBibleBook(book)
        #print cl
        if not cl :
            self.bibleDBCache[bible].createBook(book)
        
    def _loadChapter(self, bible, book, chapter):
        print "loadChapter ", bible, book, chapter        
        chaptlist = self.bibleHTTPCache[bible].getBibleChapter(bible, book, chapter)
        self.bibleDBCache[bible].createChapter(book, chapter, chaptlist)
        
    def _isNewBible(self, name):
        """
        Check cache to see if new bible
        """
        for b ,  o in self.bibleDBCache.iteritems():
            print b 
            if b == name : 
                return False
        return True
