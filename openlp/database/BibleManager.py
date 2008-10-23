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
sys.path.insert(0,(os.path.join(mypath, '..', '..')))

from openlp.utils import ConfigHelper
from openlp.database.BibleImpl import *

class BibleManager:
    def __init__(self):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection information
        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        #if bible != "niv" and bible !="message":
        #    raise Exception('Unsupported bible requested ' + bible)

        self.biblelist = {}
        self.biblePath = ConfigHelper.getBiblePath()
        #print self.biblePath
        files = os.listdir(self.biblePath)
        for f in files:
            b = f.split('.')[0]
            self.biblelist[b] = BibleImpl(b)
        #print self.biblelist



    def getBibles(self):
        """
        Returns a list of Books of the bible
        """
        r=[]
        for b ,  o in self.biblelist.iteritems():
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

    def getVerseText(self, bible,book,  chapter, sverse, everse):
        """
        Returns a list of verses for a given Book, Chapter and ranges of verses.
        If the end verse(everse) is less then the start verse(sverse)
        then only one verse is returned
        """

        if everse < sverse:
            print "adjusted end verse"
            everse = sverse
        return ["In the Beginning was the Word","God made the world as saw it was good"]
