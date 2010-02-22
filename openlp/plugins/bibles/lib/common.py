# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

import urllib2
import chardet
import logging
import re

only_verses = re.compile(r'([\w .]+)[ ]+([0-9]+)[ ]*[:|v|V][ ]*([0-9]+)'
    r'(?:[ ]*-[ ]*([0-9]+|end))?(?:[ ]*,[ ]*([0-9]+)(?:[ ]*-[ ]*([0-9]+|end))?)?',
    re.UNICODE)
chapter_range = re.compile(r'([\w .]+)[ ]+([0-9]+)[ ]*[:|v|V][ ]*'
    r'([0-9]+)[ ]*-[ ]*([0-9]+)[ ]*[:|v|V][ ]*([0-9]+)',
    re.UNICODE)

log = logging.getLogger(__name__)

def parse_reference(reference):
    """
    This is the über-awesome function that takes a person's typed in string
    and converts it to a reference list, a list of references to be queried
    from the Bible database files.

    The reference list is a list of tuples, with each tuple structured like
    this::

        (book, chapter, start_verse, end_verse)
    """
    reference = reference.strip()
    log.debug('parse_reference("%s")', reference)
    reference_list = []
    # We start with the most "complicated" match first, so that they are found
    # first, and we don't have any "false positives".
    match = chapter_range.match(reference)
    if match:
        log.debug('Found a chapter range.')
        book = match.group(1)
        from_verse = match.group(3)
        to_verse = match.group(5)
        if int(match.group(2)) == int(match.group(4)):
            reference_list.append(
                (match.group(1), int(match.group(2)), from_verse, to_verse)
            )
        else:
            if int(match.group(2)) > int(match.group(4)):
                from_chapter = int(match.group(4))
                to_chapter = int(match.group(2))
            else:
                from_chapter = int(match.group(2))
                to_chapter = int(match.group(4))
            for chapter in xrange(from_chapter, to_chapter + 1):
                if chapter == from_chapter:
                    reference_list.append(
                        (match.group(1), chapter, from_verse, -1)
                    )
                elif chapter == to_chapter:
                    reference_list.append(
                        (match.group(1), chapter, 1, to_verse)
                    )
                else:
                    reference_list.append(
                        (match.group(1), chapter, 1, -1)
                    )
    else:
        match = only_verses.match(reference)
        if match:
            log.debug('Found a verse range.')
            book = match.group(1)
            chapter = match.group(2)
            verse = match.group(3)
            if match.group(4) is None:
                reference_list.append((book, chapter, verse, verse))
            elif match.group(5) is None:
                end_verse = match.group(4)
                if end_verse == u'end':
                    end_verse = -1
                reference_list.append((book, chapter, verse, end_verse))
            elif match.group(6) is None:
                reference_list.extend([
                    (book, chapter, verse, match.group(4)),
                    (book, chapter, match.group(5), match.group(5))
                ])
            else:
                end_verse = match.group(6)
                if end_verse == u'end':
                    end_verse = -1
                reference_list.extend([
                    (book, chapter, verse, match.group(4)),
                    (book, chapter, match.group(5), end_verse)
                ])
        else:
            log.debug('Didn\'t find anything.')
    log.debug(reference_list)
    return reference_list


class SearchResults(object):
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

    def _get_web_text(self, urlstring, proxyurl):
        """
        Get the HTML from the web page.

        ``urlstring``
            The URL of the page to open.

        ``proxyurl``
            The URL of a proxy server used to access the Internet.
        """
        log.debug(u'get_web_text %s %s', proxyurl, urlstring)
        if proxyurl:
            proxy_support = urllib2.ProxyHandler({'http': self.proxyurl})
            http_support = urllib2.HTTPHandler()
            opener = urllib2.build_opener(proxy_support, http_support)
            urllib2.install_opener(opener)
        xml_string = u''
        req = urllib2.Request(urlstring)
        #Make us look like an IE Browser on XP to stop blocking by web site
        req.add_header(u'User-Agent',
            u'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
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
        return text.rstrip().lstrip()
