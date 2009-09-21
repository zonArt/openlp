# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import os, os.path
import sys
import urllib2

from common import BibleCommon, SearchResults

import logging

class BGExtract(BibleCommon):
    global log
    log=logging.getLogger(u'BibleHTTPMgr(BG_extract)')
    log.info(u'BG_extract loaded')

    def __init__(self, proxyurl= None):
        log.debug(u'init %s', proxyurl)
        self.proxyurl = proxyurl

    def get_bible_chapter(self, version, bookid, bookname, chapter) :
        """
        Access and decode bibles via the BibleGateway website

        ``Version``
            The version of the bible like 31 for New International version

        ``bookid``
            Book id for the book of the bible - eg 1 for Genesis

        ``bookname``
            Not used

        ``chapter``
            Chapter number
        """
        log.debug(u'get_bible_chapter %s,%s,%s,%s',
            version, bookid, bookname, chapter)
        urlstring = u'http://www.biblegateway.com/passage/?book_id=' + \
            unicode(bookid) + u'&chapter' + unicode(chapter) + u'&version=' + \
            unicode(version)
        xml_string = self._get_web_text(urlstring, self.proxyurl)
        #print xml_string
        VerseSearch = u'class=' + u'"' + u'sup' + u'"' + u'>'
        verse = 1
        i = xml_string.find(u'result-text-style-normal')
        xml_string = xml_string[i:len(xml_string)]
        versePos = xml_string.find(VerseSearch)
        #print versePos
        bible = {}
        while versePos > -1:
            verseText = '' # clear out string
            versePos = xml_string.find(u'</span', versePos)
            i = xml_string.find(VerseSearch, versePos+1)
            #print i , versePos
            if i == -1:
                i = xml_string.find(u'</div', versePos+1)
                j = xml_string.find(u'<strong', versePos+1)
                #print i , j
                if j > 0 and j < i:
                    i = j
                verseText = xml_string[versePos + 7 : i ]
                #print xml_string
                #print 'VerseText = ' + unicode(verse) +' '+ verseText
                bible[verse] = self._clean_text(verseText) # store the verse
                versePos = -1
            else:
                i = xml_string[:i].rfind(u'<span') + 1
                # Loose the </span>
                verseText = xml_string[versePos + 7 : i - 1 ]
                # Chop off verse 1
                xml_string = xml_string[i - 1 :len(xml_string)]
                versePos = xml_string.find(VerseSearch) #look for the next verse
                bible[verse] = self._clean_text(verseText) # store the verse
                verse += 1
        return bible

class CWExtract(BibleCommon):
    global log
    log=logging.getLogger(u'BibleHTTPMgr(CWExtract)')
    log.info(u'CWExtract loaded')

    def __init__(self, proxyurl=None):
        log.debug(u'init %s', proxyurl)
        self.proxyurl = proxyurl

    def get_bible_chapter(self, version, bookid, bookname, chapter) :
        log.debug(u'getBibleChapter %s,%s,%s,%s',
            version, bookid, bookname, chapter)
        """
        Access and decode bibles via the Crosswalk website

        ``version``
            The version of the bible like niv for New International Version

        ``bookid``
            Not used

        ``bookname``
            Text name of in english e.g. 'gen' for Genesis

        ``chapter``
            Chapter number
        """
        log.debug(u'get_bible_chapter %s,%s,%s,%s',
            version, bookid, bookname, chapter)
        bookname = bookname.replace(u' ', u'')
        urlstring = u'http://bible.crosswalk.com/OnlineStudyBible/bible.cgi?word=%s+%d&version=%s' % (bookname, chapter, version)
        xml_string = self._get_web_text(urlstring, self.proxyurl)
        #log.debug(u'Return data %s', xml_string)
        ## Strip Book Title from Heading to return it to system
        ##
        i= xml_string.find(u'<title>')
        j= xml_string.find(u'-', i)
        book_title = xml_string[i + 7:j]
        book_title = book_title.rstrip()
        log.debug(u'Book Title %s', book_title)
        i = book_title.rfind(u' ')
        book_chapter = book_title[i+1:len(book_title)].rstrip()
        book_title = book_title[:i].rstrip()
        log.debug(u'Book Title %s', book_title)
        log.debug(u'Book Chapter %s', book_chapter)

        ## Strip Verse Data from Page and build an array
        ##
        #log.debug(u'bible data %s', xml_string)
        #print xml_string
        i= xml_string.find(u'NavCurrentChapter')
        xml_string = xml_string[i:len(xml_string)]
        i= xml_string.find(u'<TABLE')
        xml_string = xml_string[i:len(xml_string)]
        i= xml_string.find(u'<B>')
        #remove the <B> at the front
        xml_string = xml_string[i + 3 :len(xml_string)]
        # Remove the heading for the book
        i= xml_string.find(u'<B>')
        #remove the <B> at the front
        xml_string = xml_string[i + 3 :len(xml_string)]
        versePos = xml_string.find(u'<BLOCKQUOTE>')
        #log.debug(u'verse pos %d', versePos)
        bible = {}
        while versePos > 0:
            verseText = u''
            versePos = xml_string.find(u'<B><I>', versePos) + 6
            i = xml_string.find(u'</I></B>', versePos)
            #log.debug( versePos, i)
            verse= xml_string[versePos:i] # Got the Chapter
            #log.debug( 'Chapter = %s', verse)
            # move the starting position to begining of the text
            versePos = i + 8
            # find the start of the next verse
            i = xml_string.find(u'<B><I>', versePos)
            if i == -1:
                i = xml_string.find(u'</BLOCKQUOTE>',versePos)
                verseText = xml_string[versePos: i]
                versePos = 0
            else:
                #log.debug( i, versePos)
                verseText = xml_string[versePos: i]
                versePos = i
            #print verseText
            #print self._clean_text(verseText)
            bible[verse] = self._clean_text(verseText)

        #log.debug( bible)
        return SearchResults(book_title, book_chapter, bible)

class BibleHTTPImpl():
    global log
    log=logging.getLogger(u'BibleHTTPMgr')
    log.info(u'BibleHTTP manager loaded')
    def __init__(self):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection
        information

        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        bible = {}
        biblesource = ''
        proxyurl = None
        bibleid = None

    def set_proxy(self,proxyurl):
        """
        Set the Proxy Url
        """
        log.debug(u'set_proxy %s', proxyurl)
        self.proxyurl = proxyurl

    def set_bibleid(self,bibleid):
        """
        Set the bible id.
        The shore identifier of the the bible.
        """
        log.debug(u'set_bibleid %s', bibleid)
        self.bibleid = bibleid

    def set_bible_source(self,biblesource):
        """
        Set the source of where the bible text is coming from
        """
        log.debug(u'set_bible_source %s', biblesource)
        self.biblesource = biblesource

    def get_bible_chapter(self, version, bookid, bookname, chapter):
        """
        Receive the request and call the relevant handler methods
        """
        log.debug(u'get_bible_chapter %s,%s,%s,%s',
            version, bookid, bookname, chapter)
        log.debug(u'biblesource = %s', self.biblesource)
        try:
            if self.biblesource.lower() == u'crosswalk':
                ev = CWExtract(self.proxyurl)
            else:
                ev = BGExtract(self.proxyurl)
            return ev.get_bible_chapter(self.bibleid, bookid, bookname, chapter)
        except Exception, e:
            log.error(u'Error thrown = %s', e.args[0])
            print e
