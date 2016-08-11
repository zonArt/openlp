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
from openlp.plugins.bibles.lib.http import get_soup_for_bible_ref, send_error_message

VERSE_NUMBER_REGEX = re.compile(r'v(\d{1,2})(\d{3})(\d{3}) verse.*')

BIBLESERVER_LANGUAGE_CODE = {
    'fl_1': 'de',
    'fl_2': 'en',
    'fl_3': 'fr',
    'fl_4': 'it',
    'fl_5': 'es',
    'fl_6': 'pt',
    'fl_7': 'ru',
    'fl_8': 'sv',
    'fl_9': 'no',
    'fl_10': 'nl',
    'fl_11': 'cs',
    'fl_12': 'sk',
    'fl_13': 'ro',
    'fl_14': 'hr',
    'fl_15': 'hu',
    'fl_16': 'bg',
    'fl_17': 'ar',
    'fl_18': 'tr',
    'fl_19': 'pl',
    'fl_20': 'da',
    'fl_21': 'zh'
}

log = logging.getLogger(__name__)


class BSExtract(RegistryProperties):
    """
    Extract verses from Bibleserver.com
    """
    def __init__(self, proxy_url=None):
        log.debug('BSExtract.init("{url}")'.format(url=proxy_url))
        self.proxy_url = proxy_url
        socket.setdefaulttimeout(30)

    def get_bible_chapter(self, version, book_name, chapter):
        """
        Access and decode bibles via Bibleserver mobile website

        :param version: The version of the bible like NIV for New International Version
        :param book_name: Text name of bible book e.g. Genesis, 1. John, 1John or Offenbarung
        :param chapter: Chapter number
        """
        log.debug('BSExtract.get_bible_chapter("{version}", "{book}", "{chapter}")'.format(version=version,
                                                                                           book=book_name,
                                                                                           chapter=chapter))
        url_version = urllib.parse.quote(version.encode("utf-8"))
        url_book_name = urllib.parse.quote(book_name.encode("utf-8"))
        chapter_url = 'http://m.bibleserver.com/text/{version}/{name}{chapter:d}'.format(version=url_version,
                                                                                         name=url_book_name,
                                                                                         chapter=chapter)
        header = ('Accept-Language', 'en')
        soup = get_soup_for_bible_ref(chapter_url, header)
        if not soup:
            return None
        self.application.process_events()
        content = soup.find('div', 'content')
        if not content:
            log.error('No verses found in the Bibleserver response.')
            send_error_message('parse')
            return None
        content = content.find('div').find_all('div')
        verses = {}
        for verse in content:
            self.application.process_events()
            versenumber = int(VERSE_NUMBER_REGEX.sub(r'\3', ' '.join(verse['class'])))
            verses[versenumber] = verse.contents[1].rstrip('\n')
        return SearchResults(book_name, chapter, verses)

    def get_books_from_http(self, version):
        """
        Load a list of all books a Bible contains from Bibleserver mobile website.

        :param version: The version of the Bible like NIV for New International Version
        """
        log.debug('BSExtract.get_books_from_http("{version}")'.format(version=version))
        url_version = urllib.parse.quote(version.encode("utf-8"))
        chapter_url = 'http://m.bibleserver.com/overlay/selectBook?translation={version}'.format(version=url_version)
        soup = get_soup_for_bible_ref(chapter_url)
        if not soup:
            return None
        content = soup.find('ul')
        if not content:
            log.error('No books found in the Bibleserver response.')
            send_error_message('parse')
            return None
        content = content.find_all('li')
        return [book.contents[0].contents[0] for book in content if len(book.contents[0].contents)]

    def get_bibles_from_http(self):
        """
        Load a list of bibles from Bibleserver website.

        returns a list in the form [(biblename, biblekey, language_code)]
        """
        log.debug('BSExtract.get_bibles_from_http')
        bible_url = 'http://www.bibleserver.com/index.php?language=2'
        soup = get_soup_for_bible_ref(bible_url)
        if not soup:
            return None
        bible_links = soup.find_all('a', {'class': 'trlCell'})
        if not bible_links:
            log.debug('No a tags found - did site change?')
            return None
        bibles = []
        for link in bible_links:
            bible_name = link.get_text()
            # Skip any audio
            if 'audio' in bible_name.lower():
                continue
            try:
                bible_link = link['href']
                bible_key = bible_link[bible_link.rfind('/') + 1:]
                css_classes = link['class']
            except KeyError:
                log.debug('No href/class attribute found - did site change?')
            language_code = ''
            for css_class in css_classes:
                if css_class.startswith('fl_'):
                    try:
                        language_code = BIBLESERVER_LANGUAGE_CODE[css_class]
                    except KeyError:
                        language_code = ''
            bibles.append((bible_name, bible_key, language_code))
        return bibles
