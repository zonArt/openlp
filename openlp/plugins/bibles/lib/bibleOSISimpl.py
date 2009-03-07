"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 - 2009 Martin Thompson, Tim Bentley

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
import os 
import os.path
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
        
        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(filepath, '..', 'resources','osisbooks.csv')) 
        fbibles=open(filepath, 'r')
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
        for file in osis.readlines():
            if self.loadbible == False:  # cancel pressed
                break
#            print file
            pos = file.find(verseText)
            if pos > -1: # we have a verse
                epos= file.find(">", pos)
                ref =  file[pos+15:epos-1]  # Book Reference 
                #lets find the bible text
                pos = epos + 1 # find start of text
                epos = file.find("</verse>", pos) # end  of text
                text = file[pos : epos] 
                #print pos, e, f[pos:e] # Found Basic Text
                #remove tags of extra information
                
                pos = text.find("<title")
                while pos > -1:
                    epos = text.find("</title>", pos)
                    if epos == -1: # TODO
                        #print "Y", pos, epos
                        pos = -1
                    else:
                        text =  text[:pos] + text[epos + 8: ]
                        pos = text.find("<title") 
                        
                pos = text.find("<divineName")
                while pos > -1:
                    epos = text.find("</divineName>", pos)
                    if epos == -1: # TODO
                        #print "Y", pos, epos
                        pos = -1
                    else:
                        text =  text[:pos] + text[epos + 13: ]
                        pos = text.find("<divineName")                         

                pos = text.find("<note")
                while pos > -1:
                    epos = text.find("</note>", pos)
                    if epos == -1: # TODO
                        #print "Y", pos, epos
                        pos = -1
                    else:
                        text =  text[:pos] + text[epos + 7: ]
                        pos = text.find("<note")
                        
                pos = text.find("<lb")
                while pos > -1:
                    epos = text.find("/>", pos)
                    text =  text[:pos] + text[epos + 2: ]
                    pos = text.find("<lb")                         

                pos = text.find("<q")
                while pos > -1:
                    epos = text.find("/>", pos)
                    text =  text[:pos] + text[epos + 2: ]
                    pos = text.find("<q")
                    
                pos = text.find("<l")
                while pos > -1:
                    epos = text.find("/>", pos)
                    text =  text[:pos] + text[epos + 2: ]
                    pos = text.find("<l")
                    
                pos = text.find("<lg")
                while pos > -1:
                    epos = text.find("/>", pos)
                    text =  text[:pos] + text[epos + 2: ]
                    pos = text.find("<lg") 

                pos = text.find("<FI>")
                while pos > -1:
                    epos = text.find("<Fi>", pos)
                    if epos == -1: # TODO
                        #print "Y", search_text, e
                        pos = -1
                    else:
                        text =  text[:pos] + text[epos + 4: ]
                        pos = text.find("<FI>") 

                pos = text.find("<RF>")
                while pos > -1:
                    epos = text.find("<Rf>", pos)
                    text =  text[:pos] + text[epos + 4: ]
                    #print "X", pos, epos, text
                    pos = text.find("<RF>")
  
                p = ref.split(".", 3)  # split up the reference
                #print p, ">>>", text  

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
                    dialogobject.incrementProgressBar(self.booksOfBible[p[0]] )
                    Receiver().send_message("openlpprocessevents")                                        
                    count = 0
                self.bibledb.add_verse(book.id, p[1], p[2], text)
                count += 1
                if count % 3 == 0:   #Every x verses repaint the screen
                    Receiver().send_message("openlpprocessevents")                    
                    count = 0





 
