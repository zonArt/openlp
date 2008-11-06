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

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')
                
class BibleHTTPImpl:
    global log 
    log=logging.getLogger("BibleHTTPMgr")
    log.info("BibleHTTP manager loaded") 
    def __init__(self):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection information
        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        bible = {}
        biblesoure = ""
        
    def setBibleSource(self,biblesource):
        self.biblesource = biblesource

    def getBibleChapter(self, version, bookid,bookname,  chapter):
        urlstring = "http://bible.crosswalk.com/OnlineStudyBible/bible.cgi?word="+bookname+"+"+str(chapter)+"&version="+version
        log.debug( urlstring)
        xml_string = ""
        req = urllib2.Request(urlstring)
        req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        try:
            handle = urllib2.urlopen(req)
            xml_string = handle.read()
        except IOError, e:
            if hasattr(e, 'reason'):
                log.error( 'Reason : ')
                log.error( e.reason)
        
        i= xml_string.find("NavCurrentChapter")
        xml_string = xml_string[i:len(xml_string)]
        i= xml_string.find("<TABLE")
        xml_string = xml_string[i:len(xml_string)]
        i= xml_string.find("<B>")
        xml_string = xml_string[i + 3 :len(xml_string)] #remove the <B> at the front
        i= xml_string.find("<B>") # Remove the heading for the book
        xml_string = xml_string[i + 3 :len(xml_string)] #remove the <B> at the front
        versePos = xml_string.find("<BLOCKQUOTE>") 
        #log.debug( versePos)
        bible = {}
        cleanbible = {}
        while versePos > 0:
            versePos = xml_string.find("<B><I>", versePos) + 6
            i = xml_string.find("</I></B>", versePos) 
            #log.debug( versePos, i)
            verse= xml_string[versePos:i] # Got the Chapter
            #verse = int(temp)
            #log.debug( "Chapter = " + str(temp))
            versePos = i + 8     # move the starting position to negining of the text
            i = xml_string.find("<B><I>", versePos) # fine the start of the next verse
            if i == -1:
                i = xml_string.find("</BLOCKQUOTE>",versePos)
                verseText = xml_string[versePos: i]
                versePos = 0
            else:
                #log.debug( i,  versePos)
                verseText = xml_string[versePos: i]
                versePos = i
            bible[verse] = self._cleanVerse(verseText)
            
        #log.debug( bible)
        return bible

    def _cleanVerse(self, text):
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        text = text.replace('&nbsp;', '')
        text = text.replace('<P>', '')
        text = text.replace('"', '')

        return text.rstrip()
