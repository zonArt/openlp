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
from openlp.core.lib import Receiver
from PyQt4 import QtCore

class BibleOSISImpl():
    global log     
    log=logging.getLogger("BibleOSISImpl")
    log.info("BibleOSISImpl loaded")   
    def __init__(self, biblepath, bibledb):
        self.bibledb = bibledb
        self.booksOfBible = {} # books of the bible linked to bibleid  {osis , name}
        self.abbrevOfBible = {} # books of the bible linked to bibleid  {osis ,Abbrev }  
        fbibles=open(biblepath+"/osisbooks_en.txt", 'r')
        for line in fbibles:
            p = line.split(",")
            self.booksOfBible[p[0]] = p[1].replace('\n', '')
            self.abbrevOfBible[p[0]] = p[2].replace('\n', '') 
        self.loadbible = True
        QtCore.QObject.connect(Receiver().get_receiver(),QtCore.SIGNAL("openlpstopimport"),self.stop_import)
                
    def stop_import(self):
        self.loadbible= False
        
    def load_data(self, osisfile, dialogobject=None):
        osis=open(osisfile, 'r')

        book_ptr = None
        id = 0
        count = 0
        verseText = "<verse osisID="
        testament = 1
        for f in osis.readlines():
            if self.loadbible == False:  # cancel pressed
                break
            #print f
            s = f.find(verseText)
            if s > -1: # we have a verse
                e= f.find(">", s)
                ref =  f[s+15:e-1]  # Book Reference 
                #lets find the bible text
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
  
                p = ref.split(".", 3)  # split up the reference
                if book_ptr != p[0]:
                    if book_ptr == None:  # first time through
                        if p[0]  == "Gen":  # set the max book size depending on the first book read
                            dialogobject.setMax(65)
                        else:
                            dialogobject.setMax(27)
                    if  p[0] == "Matt": # First book of NT
                        testament += 1
                    book_ptr = p[0]
                    book = self.bibledb.create_book(self.booksOfBible[p[0]] , self.abbrevOfBible[p[0]], testament)
                    dialogobject.incrementBar(self.booksOfBible[p[0]] )
                    #Receiver().send_message("openlprepaint") # send repaint message to dialog
                    Receiver().send_message("openlpprocessevents")                                        
                    count = 0
                self.bibledb.add_verse(book.id, p[1], p[2], t)
                count += 1
                if count % 1 == 0:   #Every x verses repaint the screen
                    #Receiver().send_message("openlprepaint") # send repaint message to dialog openlpprocessevents
                    Receiver().send_message("openlpprocessevents")                    
                    count = 0





 
