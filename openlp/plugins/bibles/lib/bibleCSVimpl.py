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
import urllib2

mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..', '..')))
from openlp.plugins.bibles.lib.bibleDBimpl import BibleDBImpl
from openlp.plugins.bibles.lib.biblecommon import BibleCommon

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')
               
class BibleCSVImpl(BibleCommon):
    global log     
    log=logging.getLogger("BibleCSVImpl")
    log.info("BibleCVSImpl loaded")   
    def __init__(self, bibledb):
        """
        Loads a Bible from a pair of CVS files passed in
        This class assumes the files contain all the information and 
        a clean bible is being loaded.
        """         
        self.bibledb = bibledb
        
    def loadData(self, booksfile, versesfile):
        self.bibledb.saveMeta("version", "Bible Version")
        self.bibledb.saveMeta("Copyright", "(c) Some Bible company")
        self.bibledb.saveMeta("Permission", "You Have Some")

        #session = self.Session()

        #Populate the Tables
        fbooks=open(booksfile, 'r')
        fverse=open(versesfile, 'r')

        for line in fbooks:
            #log.debug( line)
            p = line.split(",")
            p2 = p[2].replace('"', '')
            p3 = p[3].replace('"', '')            
            self.bibledb.createBook(int(p[1]), p2, p3)


        book_ptr = ""
        id = 0
        for line in fverse:
            #log.debug( line)
            p = line.split(",", 3) # split into 3 units and leave the rest as a single field
            p0 = p[0].replace('"', '')
            p3 =  p[3].replace('"', '')
            if book_ptr is not p0:
                cl = self.bibledb.getBibleBook(p0)
                id = self.bibledb.getBibleBookId(p0)
                book_ptr = cl
                log.debug( id )
            self.bibledb.addVerse(id[0], p[1], p[2], p3)
 
