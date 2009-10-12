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

import urllib2
import chardet
import logging

class SearchResults:
    """
    Encapsulate a set of search results. This is Bible-type independant.
    """
    def __init__(self, book, chapter, verselist):
        """
        Create the search result object.

        ``book``
            The book of the Bible.

        ``chapter``
            The chapter of the book.

        ``verselist``
            The list of verses for this reading
        """
        self.book = book
        self.chapter = chapter
        self.verselist = verselist

    def get_verselist(self):
        """
        Returns the list of verses.
        """
        return self.verselist

    def get_book(self):
        """
        Returns the book of the Bible.
        """
        return self.book

    def get_chapter(self):
        """
        Returns the chapter of the book.
        """
        return self.chapter

    def has_verselist(self):
        """
        Returns whether or not the verse list contains verses.
        """
        return len(self.verselist) > 0


class BibleCommon(object):
    """
    A common ancestor for bible download sites.
    """
    global log
    log = logging.getLogger(u'BibleCommon')
    log.info(u'BibleCommon')

    def __init__(self):
        """
        An empty constructor... not sure why I'm here.
        """
        pass

    def _get_web_text(self, urlstring, proxyurl):
        """
        Get the HTML from the web page.

        ``urlstring``
            The URL of the page to open.

        ``proxyurl``
            The URL of a proxy server used to access the Internet.
        """
        log.debug(u'get_web_text %s %s', proxyurl, urlstring)
        if proxyurl is not None:
            proxy_support = urllib2.ProxyHandler({'http': self.proxyurl})
            http_support = urllib2.HTTPHandler()
            opener = urllib2.build_opener(proxy_support, http_support)
            urllib2.install_opener(opener)
        xml_string = u''
        req = urllib2.Request(urlstring)
        #May us look like an IE Browser on XP to stop blocking by web site
        req.add_header(u'User-Agent', u'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
        try:
            handle = urllib2.urlopen(req)
            html = handle.read()
            details = chardet.detect(html)
            xml_string = unicode(html, details[u'encoding'])
        except IOError, e:
            if hasattr(e, u'reason'):
                log.exception(u'Reason for failure: %s', e.reason)
        return xml_string

    def _clean_text(self, text):
        """
        Clean up text and remove extra characters after been downloaded from
        the Internet.

        ``text``
            The text from the web page that needs to be cleaned up.
        """
        #return text.rstrip()
        # Remove Headings from the Text
        start_tag = text.find(u'<h')
        while start_tag > -1:
            end_tag = text.find(u'</h', start_tag)
            text = text[:(start_tag - 1)] + text[(end_tag + 4)]
            start_tag = text.find(u'<h')
        # Remove Support References from the Text
        start_tag = text.find(u'<sup>')
        while start_tag > -1:
            end_tag = text.find(u'</sup>')
            text = text[:start_tag] + text[end_tag + 6:len(text)]
            start_tag = text.find(u'<sup>')
        start_tag = text.find(u'<SUP>')
        while start_tag > -1:
            end_tag = text.find(u'</SUP>')
            text = text[:start_tag] + text[end_tag + 6:len(text)]
            start_tag = text.find(u'<SUP>')
        # Static Clean ups
        text = text.replace(u'\n', u'')
        text = text.replace(u'\r', u'')
        text = text.replace(u'&nbsp;', u'')
        text = text.replace(u'<P>', u'')
        text = text.replace(u'<I>', u'')
        text = text.replace(u'</I>', u'')
        text = text.replace(u'<P />', u'')
        text = text.replace(u'<p />', u'')
        text = text.replace(u'</P>', u'')
        text = text.replace(u'<BR>', u'')
        text = text.replace(u'<BR />', u'')
        text = text.replace(u'&quot;', u'\"')
        text = text.replace(u'&apos;', u'\'')
        # Remove some other tags
        start_tag = text.find(u'<')
        while start_tag > -1 :
            end_tag = text.find(u'>', start_tag)
            text = text[:start_tag] + text[end_tag + 1:]
            start_tag = text.find(u'<')
        text = text.replace(u'>', u'')
        return text.rstrip()

