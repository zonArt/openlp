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
sys.path.insert(0,(os.path.join(mypath, '..', '..','..')))

from openlp.database.BibleManager import *

class TestBibleManager(unittest.TestCase):

    def setUp(self):
        self.bm = BibleManager()

    def testRegisterBibleFiles(self):
        # make sure the shuffled sequence does not lose any elements
        print "testRegisterBibleFiles"
        self.bm.registerBible("TheMessage",'biblebooks_msg_short.csv','bibleverses_msg_short.csv')
        self.bm.registerBible("NIV",'biblebooks_niv_short.csv','bibleverses_niv_short.csv')        
        b = self.bm.getBibles()
        for b1 in b:
            print b1
            self.assert_(b1 in b)

    def testGetBibles(self):
        print "testGetBibles"
        # make sure the shuffled sequence does not lose any elements
        b = self.bm.getBibles()
        for b1 in b:
            print b1
            self.assert_(b1 in b)

    def testGetBooks(self):
        print "testGetBooks"
        c = self.bm.getBibleBooks("NIV")
        for c1 in c:
            print c1
            self.assert_(c1 in c)

    def testGetVerseCount(self):
        print "testGetVerseCount"        
        self.failUnless(self.bm.getBookVerseCount("NIV", "GEN", 1) == 28, "Wrong Book Count")

    def testGetVerseText(self):
        print "testGetVerseText"          
        c = self.bm.getVerseText("TheMessage",'"Genesis"',1,2,1)
        print c
        c = self.bm.getVerseText("NIV",'"Genesis"',1,2,1)
        print c

if __name__ == '__main__':
    unittest.main()
