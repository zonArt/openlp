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

class TestBibleManager:
      
    def setup_class(self):
        print "\nRegister BM"
        self.bm = BibleManager()

    def testRegisterBibleFiles(self):
        # Register a bible from files
        print "\ntestRegisterBibleFiles"
        self.bm.registerBible("TheMessage",'biblebooks_msg_short.csv','bibleverses_msg_short.csv')
        self.bm.registerBible("NIV",'biblebooks_niv_short.csv','bibleverses_niv_short.csv')        
        b = self.bm.getBibles()
        for b1 in b:
            print b1
            assert(b1 in b)    
            
    def testRegisterBibleHTTP(self):
        # Register a bible from files
        print "\ntestRegisterBibleHTTP"
        self.bm.registerHTTPBible("asv","Crosswalk", "", "", "", "")
        #self.bm.registerBible("NIV", "ge", 1)
        b = self.bm.getBibles()
        for b1 in b:
            print b1
            assert(b1 in b)    

            
    def testGetBibles(self):
        print "\ntestGetBibles"
        # make sure the shuffled sequence does not lose any elements
        b = self.bm.getBibles()
        for b1 in b:
            print b1
            assert(b1 in b)

    def testGetBooks(self):
        print "\ntestGetBooks"
        c = self.bm.getBibleBooks("NIV")
        for c1 in c:
            print c1
            assert(c1 in c)
            
    def testGetChapterCount(self):
        print "\ntestGetChapterCount"        
        assert(self.bm.getBookChapterCount("Matthew") == '28')

    def testGetVerseCount(self):
        print "\ntestGetVerseCount\n"        
        assert(self.bm.getBookVerseCount("Genesis", 1) == '31')
        assert(self.bm.getBookVerseCount("Genesis", 2) == '25')
        assert(self.bm.getBookVerseCount("Matthew", 1) == '25')
        assert(self.bm.getBookVerseCount("Revelation", 1) == '20')        

    def testGetVerseText(self):
        print "\ntestGetVerseText"
        c = self.bm.getVerseText("TheMessage",'Genesis',1,2, 1)
        print c
        c = self.bm.getVerseText('NIV','Genesis',1,1,2)
        print c
        c = self.bm.getVerseText('asv','re',1,1,2)
        print c
        c = self.bm.getVerseText('asv','re',1,5,9)
        print c
        
    def testLoadBible(self):
        print "\ntestLoadBible"
        self.bm.loadBible('asv')
