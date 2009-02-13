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
import logging

from openlp.plugins.bibles.lib.bibleDBimpl import BibleDBImpl
from openlp.plugins.bibles.lib.common import BibleCommon
from openlp.core.lib import Receiver


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
        
    def load_data(self, booksfile, versesfile, dialogobject=None):
        #Populate the Tables
        fbooks=open(booksfile, 'r')
        fverse=open(versesfile, 'r')

        count = 0
        for line in fbooks:
            #log.debug( line)
            p = line.split(",")
            p1 = p[1].replace('"', '')            
            p2 = p[2].replace('"', '')
            p3 = p[3].replace('"', '')            
            self.bibledb.create_book(p2, p3, int(p1))
            count += 1
            if count % 3 == 0:   #Every x verses repaint the screen
                Receiver().send_message("openlpprocessevents")                    
                count = 0
        
        count = 0
        book_ptr = None
        for line in fverse:
            #log.debug( line)
            p = line.split(",", 3) # split into 3 units and leave the rest as a single field
            p0 = p[0].replace('"', '')
            p3 =  p[3].replace('"', '')
            if book_ptr is not p0:
                book = self.bibledb.get_bible_book(p0)
                book_ptr = book.name
                dialogobject.incrementBar(book.name) # increament the progress bar
            self.bibledb.add_verse(book.id, p[1], p[2], p3)
            count += 1
            if count % 3 == 0:   #Every x verses repaint the screen
                Receiver().send_message("openlpprocessevents")                    
                count = 0
