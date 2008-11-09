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
from openlp.plugins.biblemanager.BibleCommon import BibleCommon

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')
                
class BibleHTTPImpl(BibleCommon):
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
        biblesource = ""
        
    def setBibleSource(self,biblesource):
        """
        Set the source of where the bible text is comming from
        """
        log.debug("setBibleSource %s", biblesource)        
        self.biblesource = biblesource

    def getBibleChapter(self, version, bookid, bookname,  chapter):
        """
        Recieve the request and call the relevent handler methods
        """
        log.debug( "getBibleChapter %s,%s,%s,%s", version, bookid, bookname,  chapter) 
        log.debug("biblesource = %s", self.biblesource)
        if self.biblesource == 'Crosswalk':
            return self.getBibleCWChapter(version, bookid, bookname,  chapter)
        else:
            try:
                return self.getBibleBGChapter(version, bookid, bookname,  chapter)
            except:
                log.error("Error thrown = %s", sys.exc_info()[1])
            
    def getBibleBGChapter(self, version, bookid, bookname,  chapter):
        """
        Access and decode bibles via the BibleGateway website
            Version - the version of the bible like 31 for New International version
            bookid - Book id for the book of the bible - eg 1 for Genesis
            bookname - not used
            chapter - chapter number 
        
        """
        version = 49
        log.debug( "getBibleBGChapter %s,%s,%s,%s", version, bookid, bookname,  chapter)     
        urlstring = "http://www.biblegateway.com/passage/?book_id="+str(bookid)+"&chapter"+str(chapter)+"&version="+str(version)
        log.debug( "Url String %s", urlstring)
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
                
        VerseSearch = "class="+'"'+"sup"+'"'+">"
        verse = 1
        i= xml_string.find("result-text-style-normal")
        xml_string = xml_string[i:len(xml_string)]
        versePos = xml_string.find(VerseSearch)
        #print versePos
        bible = {}
        while versePos > 0:
            verseText = "" # clear out string
            versePos = xml_string.find("</span", versePos)
            i = xml_string.find(VerseSearch, versePos+1)
            #print i ,  versePos
            if i == -1:
                i = xml_string.find("</div", versePos+1)
                j = xml_string.find("<strong", versePos+1)                
                #print i ,  j
                if j > 0 and j < i:
                    i = j
                verseText = xml_string[versePos + 7 : i ] 
                #print xml_string
                print "VerseText = " + str(verse) +" "+ verseText
                bible[verse] = self._cleanText(verseText) # store the verse                
                versePos = 0 
            else:
                i = xml_string[:i].rfind("<span")+1
                verseText = xml_string[versePos + 7 : i ] # Loose the </span>
                xml_string = xml_string[i:len(xml_string)] # chop off verse 1
                versePos = xml_string.find(VerseSearch) #look for the next verse
                bible[verse] = self._cleanText(verseText) # store the verse
                verse += 1
        return bible
        
    def getBibleCWChapter(self, version, bookid, bookname,  chapter):
        """
        Access and decode bibles via the Crosswaly website
            Version - the version of the bible like niv for New International version
            bookid - not used
            bookname - text name of in english eg 'gen' for Genesis
            chapter - chapter number 
        """        
        log.debug( "getBibleCWChapter %s,%s,%s,%s", version, bookid, bookname,  chapter)         
        urlstring = "http://bible.crosswalk.com/OnlineStudyBible/bible.cgi?word="+bookname+"+"+str(chapter)+"&version="+version
        log.debug( "Url String %s", urlstring)
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
        while versePos > 0:
            verseText = "" # clear out string
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
            bible[verse] = self._cleanText(verseText)
            #bible[verse] = verseText
            
        #log.debug( bible)
        return bible

