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
from openlp.plugins.biblemanager.BibleDBImpl import *
from openlp.plugins.biblemanager.BibleHTTPImpl import *

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
        self.biblePath = ConfigHelper.getBiblePath()
        #print self.biblePath
        files = os.listdir(self.biblePath)
        for f in files:
            b = f.split('.')[0]
            self.bibleDBCache[b] = BibleDBImpl(b)
        print self.bibleDBCache
        print self.bibleHTTPCache        

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
        return ["Gen","Exd","Matt","Mark"]

    def getBookVerseCount(self, bible, book, chapter):
        """
        Returns all the number of verses for a given
        book and chapter
        """
        return 28

    def getVerseText(self, bible, book,  chapter, sverse, everse = 0 ):
        """
        Returns a list of verses for a given Book, Chapter and ranges of verses.
        If the end verse(everse) is less then the start verse(sverse)
        then only one verse is returned
        """
        print self.bibleDBCache
        print self.bibleHTTPCache        
        c = self.bibleDBCache[bible].getBibleChapter(book, chapter) # check to see if book/chapter exists
        if not c:
            self._loadChapter(bible, book, chapter)
        if everse < sverse:
            everse = sverse
        text = self.bibleDBCache[bible].getBibleText(book, chapter, sverse, everse)
        print text
        return text

    def _loadChapter(self, bible, book, chapter):
        cl = self.bibleHTTPCache[bible].getBibleChapter(bible, book, chapter)
        for v ,  t in cl.iteritems():
            #self.bibleDBCache[bible].loadVerse(book, chapter, v, t)
            print v , t
        
    def _isNewBible(self, name):
        """
        Check cache to see if new bible
        """
        for b ,  o in self.bibleDBCache.iteritems():
            print b 
            if b == name : 
                return False
        return True
