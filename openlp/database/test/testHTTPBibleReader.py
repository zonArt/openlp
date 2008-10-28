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

class TestHTTPBibleReader(unittest.TestCase):

    def setUp(self):
        self.bhi = BibleHTTPImpl()

    def testGetBibleChapter(self):
        # make sure the shuffled sequence does not lose any elements
        print "testGetBibleChapter"
        print self.bhi.getBibleChapter("NIV", "ge", 1)
        print self.bhi.getBibleChapter("NIV", "re", 1)
  

if __name__ == '__main__':
    unittest.main()
