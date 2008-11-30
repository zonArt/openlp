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
from openlp.plugins.biblemanager.bibleDBImpl import BibleDBImpl

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')
               
class BibleOSISImpl():
    global log     
    log=logging.getLogger("BibleOSISImpl")
    log.info("BibleOSISImpl loaded")   
    def __init__(self, bibledb):
        self.bibledb = bibledb
        self.booksOfBible = {} # books of the bible linked to bibleid  {osis , name}
        self.abbrevOfBible = {} # books of the bible linked to bibleid  {osis ,Abbrev }  
        fbibles=open("../resources/osisbooks_en.txt", 'r')
        for line in fbibles:
            p = line.split(",")
            self.booksOfBible[p[0]] = p[1].replace('\n', '')
            self.abbrevOfBible[p[0]] = p[2].replace('\n', '')            
                
        
    def loadData(self, osisfile, dialogobject=None):
        self.bibledb.saveMeta("Version", "Bible Version")
        self.bibledb.saveMeta("Copyright", "(c) Some Bible company")
        self.bibledb.saveMeta("Permission", "You Have Some")
        dialogobject.setMax(66)
        
        osis=open(osisfile, 'r')

        book_ptr = ""
        id = 0
        verseText = "<verse osisID="
        for f in osis.readlines():
            #print f
            s = f.find(verseText)
            if s > -1: # we have a verse
                e= f.find(">", s)
                ref =  f[s+15:e-1]  # Book Reference 
                #lets find the bble text
                s = e + 1 # find start of text
                e = f.find("</verse>", s) # end  of text
                t = f[s:e] 
                #print s, e, f[s:e] # Found Basic Text
                #remove tags of extra information

                s = t.find("<FI>")
                while s > -1:
                    e = t.find("<Fi>", s)
                    if e == -1: # TODO
                        #print "Y", s, e
                        s = -1
                    else:
                        t =  t[:s] + t[e + 4: ]
                        s = t.find("<FI>") 

                s = t.find("<RF>")
                while s > -1:
                    e = t.find("<Rf>", s)
                    t =  t[:s] + t[e + 4: ]
                    #print "X", s, e, t
                    s = t.find("<RF>")
  
                p = ref.split(".", 3)  # split u[ the reference
                if book_ptr != p[0]:
                    book_ptr = p[0]
                    self.bibledb.createBook(int(p[1]), self.booksOfBible[p[0]] , self.abbrevOfBible[p[0]])
                    id = self.bibledb.getBibleBookId(self.booksOfBible[p[0]])
                    dialogobject.incrementBar()
                self.bibledb.addVerse(id[0], p[1], p[2], t)





 
