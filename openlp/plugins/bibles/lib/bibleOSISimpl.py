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
    log = logging.getLogger(u'BibleOSISImpl')
    log.info(u'BibleOSISImpl loaded')

    def __init__(self, biblepath, bibledb):
        self.bibledb = bibledb
        self.booksOfBible = {} # books of the bible linked to bibleid  {osis , name}
        self.abbrevOfBible = {} # books of the bible linked to bibleid  {osis ,Abbrev }

        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(filepath, u'..', u'resources',u'osisbooks.csv'))
        fbibles=open(filepath, u'r')
        for line in fbibles:
            p = line.split(u',')
            self.booksOfBible[p[0]] = p[1].replace(u'\n', '')
            self.abbrevOfBible[p[0]] = p[2].replace(u'\n', '')
        self.loadbible = True
        QtCore.QObject.connect(Receiver().get_receiver(),QtCore.SIGNAL(u'openlpstopimport'),self.stop_import)

    def stop_import(self):
        self.loadbible= False

    def load_data(self, osisfile, dialogobject=None):
        osis=open(osisfile, u'r')

        book_ptr = None
        id = 0
        count = 0
        verseText = u'<verse osisID='
        testament = 1
        for file in osis.readlines():
            # cancel pressed on UI
            if self.loadbible == False:
                break
#            print file
            pos = file.find(verseText)
            if pos > -1: # we have a verse
                epos= file.find(u'>', pos)
                ref =  file[pos+15:epos-1]  # Book Reference

                #lets find the bible text only
                pos = epos + 1 # find start of text
                epos = file.find(u'</verse>', pos) # end  of text
                text = unicode(file[pos : epos], u'utf8')
                #print pos, e, f[pos:e] # Found Basic Text

                #remove tags of extra information
                text = self.remove_block(u'<title', u'</title>', text)
                text = self.remove_block(u'<note', u'</note>', text)
                text = self.remove_block(u'<divineName', u'</divineName>', text)

                text = self.remove_tag(u'<lb',  text)
                text = self.remove_tag(u'<q',  text)
                text = self.remove_tag(u'<l',  text)
                text = self.remove_tag(u'<lg',  text)

                # Strange tags where the end is not the same as the start
                # The must be in this order as at least one bible has them
                # crossing and the removal does not work.
                pos = text.find(u'<FI>')
                while pos > -1:
                    epos = text.find(u'<Fi>', pos)
                    if epos == -1: # TODO
                        #print "Y", search_text, e
                        pos = -1
                    else:
                        text =  text[:pos] + text[epos + 4: ]
                        pos = text.find(u'<FI>')

                pos = text.find(u'<RF>')
                while pos > -1:
                    epos = text.find(u'<Rf>', pos)
                    text =  text[:pos] + text[epos + 4: ]
                    #print "X", pos, epos, text
                    pos = text.find(u'<RF>')

                p = ref.split(u'.', 3)  # split up the reference
                #print p, ">>>", text

                if book_ptr != p[0]:
                    if book_ptr == None:  # first time through
                        if p[0]  == u'Gen':  # set the max book size depending on the first book read
                            dialogobject.setMax(65)
                        else:
                            dialogobject.setMax(27)
                    if  p[0] == u'Matt': # First book of NT
                        testament += 1
                    book_ptr = p[0]
                    book = self.bibledb.create_book(self.booksOfBible[p[0]] , self.abbrevOfBible[p[0]], testament)
                    dialogobject.incrementProgressBar(self.booksOfBible[p[0]] )
                    Receiver().send_message(u'openlpprocessevents')
                    count = 0
                self.bibledb.add_verse(book.id, p[1], p[2], text)
                count += 1
                if count % 3 == 0:   #Every 3 verses repaint the screen
                    Receiver().send_message(u'openlpprocessevents')
                    count = 0

    def remove_block(self, start_tag, end_tag,  text):
        """
        removes a block of text between two tags
        <tag attrib=xvf > Some not wanted text  </tag>
        """
        pos = text.find(start_tag)
        while pos > -1:
            epos = text.find(end_tag, pos)
            if epos == -1: # TODO
                #print "Y", pos, epos
                pos = -1
            else:
                text =  text[:pos] + text[epos + len(end_tag): ]
                pos = text.find(start_tag)
        return text

    def remove_tag(self, start_tag,  text):
        """
        removes a single tag
        <tag  attrib1=fajkdf attrib2=fajkdf attrib2=fajkdf  />
        """
        pos = text.find(start_tag)
        while pos > -1:
            epos = text.find(u'/>', pos)
            text =  text[:pos] + text[epos + 2: ]
            pos = text.find(start_tag)
        return text
