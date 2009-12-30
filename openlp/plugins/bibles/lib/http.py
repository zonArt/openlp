# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

import logging

from common import BibleCommon, SearchResults
from db import BibleDB

class BGExtract(BibleCommon):
    global log
    log = logging.getLogger(u'BibleHTTPMgr(BG_extract)')
    log.info(u'BG_extract loaded')

    def __init__(self, proxyurl=None):
        log.debug(u'init %s', proxyurl)
        self.proxyurl = proxyurl

    def get_chapter(self, version, bookname, chapter) :
        """
        Access and decode bibles via the BibleGateway website

        ``Version``
            The version of the bible like 31 for New International version

        ``bookname``
            Name of the Book

        ``chapter``
            Chapter number
        """
        log.debug(u'get_bible_chapter %s, %s, %s', version, bookname, chapter)
        urlstring = u'http://www.biblegateway.com/passage/?search=%s+%d' \
            u'&version=%s' % (bookname, chapter, version)
        log.debug(u'BibleGateway url = %s' % urlstring)
        xml_string = self._get_web_text(urlstring, self.proxyurl)
        verseSearch = u'<sup class=\"versenum'
        verseFootnote = u'<sup class=\'footnote'
        verse = 1
        i = xml_string.find(u'result-text-style-normal') + 26
        xml_string = xml_string[i:len(xml_string)]
        versePos = xml_string.find(verseSearch)
        bible = {}
        while versePos > -1:
            # clear out string
            verseText = u''
            versePos = xml_string.find(u'</sup>', versePos) + 6
            i = xml_string.find(verseSearch, versePos + 1)
            # Not sure if this is needed now
            if i == -1:
                i = xml_string.find(u'</div', versePos + 1)
                j = xml_string.find(u'<strong', versePos + 1)
                if j > 0 and j < i:
                    i = j
                verseText = xml_string[versePos + 7 : i ]
                # store the verse
                bible[verse] = self._clean_text(verseText)
                versePos = -1
            else:
                verseText = xml_string[versePos: i]
                start_tag = verseText.find(verseFootnote)
                while start_tag > -1:
                    end_tag = verseText.find(u'</sup>')
                    verseText = verseText[:start_tag] + verseText[end_tag + 6:len(verseText)]
                    start_tag = verseText.find(verseFootnote)
                # Chop off verse and start again
                xml_string = xml_string[i:]
                #look for the next verse
                versePos = xml_string.find(verseSearch)
                # store the verse
                bible[verse] = self._clean_text(verseText)
                verse += 1
        return SearchResults(bookname, chapter, bible)

class CWExtract(BibleCommon):
    global log
    log = logging.getLogger(u'BibleHTTPMgr(CWExtract)')
    log.info(u'CWExtract loaded')

    def __init__(self, proxyurl=None):
        log.debug(u'init %s', proxyurl)
        self.proxyurl = proxyurl

    def get_bible_chapter(self, version, bookname, chapter) :
        log.debug(u'getBibleChapter %s,%s,%s',
            version,bookname, chapter)
        """
        Access and decode bibles via the Crosswalk website

        ``version``
            The version of the bible like niv for New International Version

        ``bookname``
            Text name of in english e.g. 'gen' for Genesis

        ``chapter``
            Chapter number
        """
        log.debug(u'get_bible_chapter %s,%s,%s',
            version, bookname, chapter)
        bookname = bookname.replace(u' ', u'')
        urlstring = u'http://bible.crosswalk.com/OnlineStudyBible/bible.cgi?word=%s+%d&version=%s'\
            % (bookname, chapter, version)
        xml_string = self._get_web_text(urlstring, self.proxyurl)
        ## Strip Book Title from Heading to return it to system
        ##
        i = xml_string.find(u'<title>')
        j = xml_string.find(u'-', i)
        book_title = xml_string[i + 7:j]
        book_title = book_title.rstrip()
        log.debug(u'Book Title %s', book_title)
        i = book_title.rfind(u' ')
        book_chapter = book_title[i+1:len(book_title)].rstrip()
        book_title = book_title[:i].rstrip()
        log.debug(u'Book Title %s', book_title)
        log.debug(u'Book Chapter %s', book_chapter)
        # Strip Verse Data from Page and build an array

        i = xml_string.find(u'NavCurrentChapter')
        xml_string = xml_string[i:len(xml_string)]
        i = xml_string.find(u'<TABLE')
        xml_string = xml_string[i:len(xml_string)]
        i = xml_string.find(u'<B>')
        #remove the <B> at the front
        xml_string = xml_string[i + 3 :len(xml_string)]
        # Remove the heading for the book
        i = xml_string.find(u'<B>')
        #remove the <B> at the front
        xml_string = xml_string[i + 3 :len(xml_string)]
        versePos = xml_string.find(u'<BLOCKQUOTE>')
        bible = {}
        while versePos > 0:
            verseText = u''
            versePos = xml_string.find(u'<B><I>', versePos) + 6
            i = xml_string.find(u'</I></B>', versePos)
            # Got the Chapter
            verse = xml_string[versePos:i]
            # move the starting position to begining of the text
            versePos = i + 8
            # find the start of the next verse
            i = xml_string.find(u'<B><I>', versePos)
            if i == -1:
                i = xml_string.find(u'</BLOCKQUOTE>',versePos)
                verseText = xml_string[versePos: i]
                versePos = 0
            else:
                verseText = xml_string[versePos: i]
                versePos = i
            bible[verse] = self._clean_text(verseText)
        return SearchResults(book_title, book_chapter, bible)

class HTTPBible(BibleDB):
    global log
    log = logging.getLogger(u'BibleHTTPMgr')
    log.info(u'BibleHTTP manager loaded')

    def __init__(self, **kwargs):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection
        information

        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        if u'download_source' not in kwargs:
            raise KeyError(u'Missing keyword argument "download_source"')
        if u'download_name' not in kwargs:
            raise KeyError(u'Missing keyword argument "download_name"')
        self.download_source = kwargs[u'download_source']
        self.download_name = kwargs[u'download_name']
        if u'proxy_server' in kwargs:
            self.proxy_server = kwargs[u'proxy_server']
        else:
            self.proxy_server = None
        if u'proxy_username' in kwargs:
            self.proxy_username = kwargs[u'proxy_username']
        else:
            self.proxy_username = None
        if u'proxy_password' in kwargs:
            self.proxy_password = kwargs[u'proxy_password']
        else:
            self.proxy_password = None

    def register(self):
        name = BibleDB.register(self)
        self.create_meta(u'download source', self.download_source)
        self.create_meta(u'download name', self.download_name)
        if self.proxy_server:
            self.create_meta(u'proxy server', self.proxy_server)
        if self.proxy_username:
            # store the proxy userid
            self.create_meta(u'proxy username', self.proxy_username)
        if self.proxy_password:
            # store the proxy password
            self.create_meta(u'proxy password', self.proxy_password)
        return name

    def get_bible_chapter(self, version, book, chapter):
        """
        Receive the request and call the relevant handler methods
        """
        log.debug(u'get_bible_chapter %s,%s,%s',
            version, book, chapter)
        log.debug(u'biblesource = %s', self.biblesource)
        try:
            if self.biblesource.lower() == u'crosswalk':
                ev = CWExtract(self.proxyurl)
            else:
                ev = BGExtract(self.proxyurl)
            return ev.get_bible_chapter(self.bibleid, book, chapter)
        except:
            log.exception("Failed to get bible chapter")
