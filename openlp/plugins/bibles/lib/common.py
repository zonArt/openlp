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
import sys
import urllib2

import logging

class SearchResults:
    def __init__(self, book, chapter, verselist):
        self.book = book
        self.chapter = chapter
        self.verselist = verselist
    def get_verselist(self):
        return self.verselist
    def get_book(self):
        return self.book
    def get_chapter(self):
        return self.chapter
    def has_verselist(self):
        if self.verselist == {}:
            return False
        else:
            return True

class BibleCommon:
    global log
    log = logging.getLogger(u'BibleCommon')
    log.info(u'BibleCommon')
    def __init__(self):
        """
        """
    def _get_web_text(self, urlstring, proxyurl):
        log.debug(u'get_web_text %s %s', proxyurl, urlstring)
        if  not proxyurl == None:
            proxy_support = urllib2.ProxyHandler({'http':  self.proxyurl})
            http_support = urllib2.HTTPHandler()
            opener= urllib2.build_opener(proxy_support, http_support)
            urllib2.install_opener(opener)
        xml_string = u''
        req = urllib2.Request(urlstring)
        req.add_header(u'User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        try:
            handle = urllib2.urlopen(req)
            xml_string = unicode(handle.read())
        except IOError, e:
            if hasattr(e, u'reason'):
                log.error(u'Reason : ')
                log.error( e.reason)
        return xml_string

    def _clean_text(self, text):
        """
        Clean up text and remove extra characters
        after been downloaded from web
        """
        #return text.rstrip()
        # Remove Headings from the Text
        i = text.find(u'<h')
        while i > -1:
            j=text.find(u'</h', i)
            text = text[ : (i - 1)]+text[(j+4)]
            i = text.find(u'<h')

        # Remove Support References from the Text
        x = text.find(u'<sup>')
        while x > -1:
            y = text.find(u'</sup>')
            text= text[:x] + text[y + 6:len(text)]
            x = text.find(u'<sup>')

        # Static Clean ups
        text= text.replace(u'\n', u'')
        text= text.replace(u'\r', u'')
        text= text.replace(u'&nbsp;', u'')
        text= text.replace(u'<P>', u'')
        text= text.replace(u'<I>', u'')
        text= text.replace(u'</I>', u'')
        text= text.replace(u'<P />', u'')
        text= text.replace(u'<p />', u'')
        text= text.replace(u'</P>', u'')
        text= text.replace(u'<BR>', u'')
        text= text.replace(u'<BR />', u'')
        #text= text.replace(chr(189), u'1/2');print "l"
        text= text.replace(u'&quot;', "'")
        text= text.replace(u'&apos;', "'")

        i = text.find(u'<')
        while i > -1 :
            j = text.find(u'>', i)
            text= text[:i] + text[j+1:]
            i = text.find(u'<')

        text= text.replace(u'>', u'')
        return text.rstrip()
