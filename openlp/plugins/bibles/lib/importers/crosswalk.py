# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
"""
The :mod:`http` module enables OpenLP to retrieve scripture from bible websites.
"""
import logging
import re
import socket
import urllib.parse
import urllib.error

from openlp.core.common import RegistryProperties
from openlp.plugins.bibles.lib import SearchResults
from openlp.plugins.bibles.lib.importers.http import get_soup_for_bible_ref, send_error_message

FIX_PUNKCTUATION_REGEX = re.compile(r'[ ]+([.,;])')
REDUCE_SPACES_REGEX = re.compile(r'[ ]{2,}')


CROSSWALK_LANGUAGES = {
    'Portuguese': 'pt',
    'German': 'de',
    'Italian': 'it',
    'Español': 'es',
    'French': 'fr',
    'Dutch': 'nl'
}

log = logging.getLogger(__name__)


class CWExtract(RegistryProperties):
    """
    Extract verses from CrossWalk/BibleStudyTools
    """
    def __init__(self, proxy_url=None):
        log.debug('CWExtract.init("{url}")'.format(url=proxy_url))
        self.proxy_url = proxy_url
        socket.setdefaulttimeout(30)

    def get_bible_chapter(self, version, book_name, chapter):
        """
        Access and decode bibles via the Crosswalk website

        :param version: The version of the Bible like niv for New International Version
        :param book_name:  Text name of in english e.g. 'gen' for Genesis
        :param chapter: Chapter number
        """
        log.debug('CWExtract.get_bible_chapter("{version}", "{book}", "{chapter}")'.format(version=version,
                                                                                           book=book_name,
                                                                                           chapter=chapter))
        url_book_name = book_name.replace(' ', '-')
        url_book_name = url_book_name.lower()
        url_book_name = urllib.parse.quote(url_book_name.encode("utf-8"))
        chapter_url = 'http://www.biblestudytools.com/{version}/{book}/{chapter}.html'.format(version=version,
                                                                                              book=url_book_name,
                                                                                              chapter=chapter)
        soup = get_soup_for_bible_ref(chapter_url)
        if not soup:
            return None
        self.application.process_events()
        verses_div = soup.find_all('div', 'verse')
        if not verses_div:
            log.error('No verses found in the CrossWalk response.')
            send_error_message('parse')
            return None
        verses = {}
        for verse in verses_div:
            self.application.process_events()
            verse_number = int(verse.find('strong').contents[0])
            verse_span = verse.find('span')
            tags_to_remove = verse_span.find_all(['a', 'sup'])
            for tag in tags_to_remove:
                tag.decompose()
            verse_text = verse_span.get_text()
            self.application.process_events()
            # Fix up leading and trailing spaces, multiple spaces, and spaces between text and , and .
            verse_text = verse_text.strip('\n\r\t ')
            verse_text = REDUCE_SPACES_REGEX.sub(' ', verse_text)
            verse_text = FIX_PUNKCTUATION_REGEX.sub(r'\1', verse_text)
            verses[verse_number] = verse_text
        return SearchResults(book_name, chapter, verses)

    def get_books_from_http(self, version):
        """
        Load a list of all books a Bible contain from the Crosswalk website.

        :param version: The version of the bible like NIV for New International Version
        """
        log.debug('CWExtract.get_books_from_http("{version}")'.format(version=version))
        chapter_url = 'http://www.biblestudytools.com/{version}/'.format(version=version)
        soup = get_soup_for_bible_ref(chapter_url)
        if not soup:
            return None
        content = soup.find_all('h4', {'class': 'small-header'})
        if not content:
            log.error('No books found in the Crosswalk response.')
            send_error_message('parse')
            return None
        books = []
        for book in content:
            books.append(book.contents[0])
        return books

    def get_bibles_from_http(self):
        """
        Load a list of bibles from Crosswalk website.
        returns a list in the form [(biblename, biblekey, language_code)]
        """
        log.debug('CWExtract.get_bibles_from_http')
        bible_url = 'http://www.biblestudytools.com/bible-versions/'
        soup = get_soup_for_bible_ref(bible_url)
        if not soup:
            return None
        h4_tags = soup.find_all('h4', {'class': 'small-header'})
        if not h4_tags:
            log.debug('No h4 tags found - did site change?')
            return None
        bibles = []
        for h4t in h4_tags:
            short_name = None
            if h4t.span:
                short_name = h4t.span.get_text().strip().lower()
            else:
                log.error('No span tag found - did site change?')
                return None
            if not short_name:
                continue
            h4t.span.extract()
            tag_text = h4t.get_text().strip()
            # The names of non-english bibles has their language in parentheses at the end
            if tag_text.endswith(')'):
                language = tag_text[tag_text.rfind('(') + 1:-1]
                if language in CROSSWALK_LANGUAGES:
                    language_code = CROSSWALK_LANGUAGES[language]
                else:
                    language_code = ''
            # ... except for those that don't...
            elif 'latin' in tag_text.lower():
                language_code = 'la'
            elif 'la biblia' in tag_text.lower() or 'nueva' in tag_text.lower():
                language_code = 'es'
            elif 'chinese' in tag_text.lower():
                language_code = 'zh'
            elif 'greek' in tag_text.lower():
                language_code = 'el'
            elif 'nova' in tag_text.lower():
                language_code = 'pt'
            else:
                language_code = 'en'
            bibles.append((tag_text, short_name, language_code))
        return bibles
