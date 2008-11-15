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

import random
import unittest

import os, os.path
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..','..','..')))

from openlp.plugins.biblemanager.BibleManager import BibleManager
from openlp.utils import ConfigHelper

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console=logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
log=logging.getLogger('')

logging.info("\nLogging started")

class TestBibleManager:
    log=logging.getLogger("testBibleMgr")
    def setup_class(self):
        log.debug("\n.......Register BM")
        self.bm = BibleManager()

    def testRegisterBibleFiles(self):
        # Register a bible from files
        log.debug("\n.......testRegisterBibleFiles")
        self.bm.registerFileBible("TheMessage",'biblebooks_msg_short.csv','bibleverses_msg_short.csv')
        self.bm.registerFileBible("NIV",'biblebooks_niv_short.csv','bibleverses_niv_short.csv')        
        b = self.bm.getBibles()
        for b1 in b:
            log.debug( b1)
            assert(b1 in b)    
            
    def testRegisterBibleHTTP(self):
        # Register a bible from files
        log.debug( "\n.......testRegisterBibleHTTP")
        self.bm.registerHTTPBible("asv","Crosswalk", "", "", "")
        self.bm.registerHTTPBible("nasb","Biblegateway", "", "", "")
        self.bm.registerHTTPBible("nkj","Biblegateway", "http://tigger2:3128/", "", "")                
        b = self.bm.getBibles()
        for b1 in b:
            log.debug( b1)
            assert(b1 in b)    

            
    def testGetBibles(self):
        log.debug( "\n.......testGetBibles")
        # make sure the shuffled sequence does not lose any elements
        b = self.bm.getBibles()
        for b1 in b:
            log.debug( b1)
            assert(b1 in b)

    def testGetBibleBooks(self):
        log.debug( "\n.......testGetBibleBooks")
        c = self.bm.getBibleBooks("NIV")
        for c1 in c:
            log.debug( c1)
            assert(c1 in c)
            
    def testGetBookChapterCount(self):
        log.debug( "\n.......testGetBookChapterCount")       
        assert(self.bm.getBookChapterCount("Matthew") == '28')

    def testGetBookVerseCount(self):
        log.debug( "\n.......testGetBookVerseCount")    
        assert(self.bm.getBookVerseCount("Genesis", 1) == '31')
        assert(self.bm.getBookVerseCount("Genesis", 2) == '25')
        assert(self.bm.getBookVerseCount("Matthew", 1) == '25')
        assert(self.bm.getBookVerseCount("Revelation", 1) == '20')        

    def testGetVerseText(self):
        log.debug( "\n.......testGetVerseText")
        c = self.bm.getVerseText("TheMessage",'Genesis',1,2,1)
        log.debug( c )
        c = self.bm.getVerseText('NIV','Genesis',1,1,2)
        log.debug( c ) 
        c = self.bm.getVerseText('asv','Revelation',1,1,2)
        log.debug( c )
        c = self.bm.getVerseText('asv','Revelation',1,5,9)
        log.debug( c )
        c = self.bm.getVerseText('nasb','Revelation',10,5,9)
        log.debug( c )       
        c = self.bm.getVerseText('nkj','Revelation',10,5,9)
        log.debug( c ) 
        
    def testLoadBible(self):
        log.debug( "\n.......testLoadBible")
        #self.bm.loadBible('asv')
        #self.bm.loadBible('nasb')        
        #self.bm.loadBible('nkj') 
