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
import socket
import urllib.parse
import urllib.error

from bs4 import BeautifulSoup, NavigableString, Tag

from openlp.core.common import RegistryProperties
from openlp.core.lib.webpagereader import get_web_page
from openlp.plugins.bibles.lib import SearchResults
from openlp.plugins.bibles.lib.importers.http import get_soup_for_bible_ref, send_error_message

UGLY_CHARS = {
    '\u2014': ' - ',
    '\u2018': '\'',
    '\u2019': '\'',
    '\u201c': '"',
    '\u201d': '"',
    '&nbsp;': ' '
}

log = logging.getLogger(__name__)


class BGExtract(RegistryProperties):
    """
    Extract verses from BibleGateway
    """
    def __init__(self, proxy_url=None):
        log.debug('BGExtract.init("{url}")'.format(url=proxy_url))
        self.proxy_url = proxy_url
        socket.setdefaulttimeout(30)

    def _remove_elements(self, parent, tag, class_=None):
        """
        Remove a particular element from the BeautifulSoup tree.

        :param parent: The element from which items need to be removed.
        :param tag: A string of the tab type, e.g. "div"
        :param class_: An HTML class attribute for further qualification.
        """
        if class_:
            all_tags = parent.find_all(tag, class_)
        else:
            all_tags = parent.find_all(tag)
        for element in all_tags:
            element.extract()

    def _extract_verse(self, tag):
        """
        Extract a verse (or part of a verse) from a tag.

        :param tag: The BeautifulSoup Tag element with the stuff we want.
        """
        if isinstance(tag, NavigableString):
            return None, str(tag)
        elif tag.get('class') and (tag.get('class')[0] == 'versenum' or tag.get('class')[0] == 'versenum mid-line'):
            verse = str(tag.string).replace('[', '').replace(']', '').strip()
            return verse, None
        elif tag.get('class') and tag.get('class')[0] == 'chapternum':
            verse = '1'
            return verse, None
        else:
            verse = None
            text = ''
            for child in tag.contents:
                c_verse, c_text = self._extract_verse(child)
                if c_verse:
                    verse = c_verse
                if text and c_text:
                    text += c_text
                elif c_text is not None:
                    text = c_text
            return verse, text

    def _clean_soup(self, tag):
        """
        Remove all the rubbish from the HTML page.

        :param tag: The base tag within which we want to remove stuff.
        """
        self._remove_elements(tag, 'sup', 'crossreference')
        self._remove_elements(tag, 'sup', 'footnote')
        self._remove_elements(tag, 'div', 'footnotes')
        self._remove_elements(tag, 'div', 'crossrefs')
        self._remove_elements(tag, 'h3')
        self._remove_elements(tag, 'h4')
        self._remove_elements(tag, 'h5')

    def _extract_verses(self, tags):
        """
        Extract all the verses from a pre-prepared list of HTML tags.

        :param tags: A list of BeautifulSoup Tag elements.
        """
        verses = []
        tags = tags[::-1]
        current_text = ''
        for tag in tags:
            verse = None
            text = ''
            for child in tag.contents:
                c_verse, c_text = self._extract_verse(child)
                if c_verse:
                    verse = c_verse
                if text and c_text:
                    text += c_text
                elif c_text is not None:
                    text = c_text
            if not verse:
                current_text = text + ' ' + current_text
            else:
                text += ' ' + current_text
                current_text = ''
            if text:
                for old, new in UGLY_CHARS.items():
                    text = text.replace(old, new)
                text = ' '.join(text.split())
            if verse and text:
                verse = verse.strip()
                try:
                    verse = int(verse)
                except ValueError:
                    verse_parts = verse.split('-')
                    if len(verse_parts) > 1:
                        verse = int(verse_parts[0])
                except TypeError:
                    log.warning('Illegal verse number: {verse:d}'.format(verse=verse))
                verses.append((verse, text))
        verse_list = {}
        for verse, text in verses[::-1]:
            verse_list[verse] = text
        return verse_list

    def _extract_verses_old(self, div):
        """
        Use the old style of parsing for those Bibles on BG who mysteriously have not been migrated to the new (still
        broken) HTML.

        :param div:  The parent div.
        """
        verse_list = {}
        # Cater for inconsistent mark up in the first verse of a chapter.
        first_verse = div.find('versenum')
        if first_verse and first_verse.contents:
            verse_list[1] = str(first_verse.contents[0])
        for verse in div('sup', 'versenum'):
            raw_verse_num = verse.next_element
            clean_verse_num = 0
            # Not all verses exist in all translations and may or may not be represented by a verse number. If they are
            # not fine, if they are it will probably be in a format that breaks int(). We will then have no idea what
            # garbage may be sucked in to the verse text so if we do not get a clean int() then ignore the verse
            # completely.
            try:
                clean_verse_num = int(str(raw_verse_num))
            except ValueError:
                verse_parts = str(raw_verse_num).split('-')
                if len(verse_parts) > 1:
                    clean_verse_num = int(verse_parts[0])
            except TypeError:
                log.warning('Illegal verse number: {verse:d}'.format(verse=raw_verse_num))
            if clean_verse_num:
                verse_text = raw_verse_num.next_element
                part = raw_verse_num.next_element.next_element
                while not (isinstance(part, Tag) and part.get('class')[0] == 'versenum'):
                    # While we are still in the same verse grab all the text.
                    if isinstance(part, NavigableString):
                        verse_text += part
                    if isinstance(part.next_element, Tag) and part.next_element.name == 'div':
                        # Run out of verses so stop.
                        break
                    part = part.next_element
                verse_list[clean_verse_num] = str(verse_text)
        return verse_list

    def get_bible_chapter(self, version, book_name, chapter):
        """
        Access and decode Bibles via the BibleGateway website.

        :param version: The version of the Bible like 31 for New International version.
        :param book_name: Name of the Book.
        :param chapter: Chapter number.
        """
        log.debug('BGExtract.get_bible_chapter("{version}", "{name}", "{chapter}")'.format(version=version,
                                                                                           name=book_name,
                                                                                           chapter=chapter))
        url_book_name = urllib.parse.quote(book_name.encode("utf-8"))
        url_params = 'search={name}+{chapter}&version={version}'.format(name=url_book_name,
                                                                        chapter=chapter,
                                                                        version=version)
        soup = get_soup_for_bible_ref(
            'http://biblegateway.com/passage/?{url}'.format(url=url_params),
            pre_parse_regex=r'<meta name.*?/>', pre_parse_substitute='')
        if not soup:
            return None
        div = soup.find('div', 'result-text-style-normal')
        if not div:
            return None
        self._clean_soup(div)
        span_list = div.find_all('span', 'text')
        log.debug('Span list: {span}'.format(span=span_list))
        if not span_list:
            # If we don't get any spans then we must have the old HTML format
            verse_list = self._extract_verses_old(div)
        else:
            verse_list = self._extract_verses(span_list)
        if not verse_list:
            log.debug('No content found in the BibleGateway response.')
            send_error_message('parse')
            return None
        return SearchResults(book_name, chapter, verse_list)

    def get_books_from_http(self, version):
        """
        Load a list of all books a Bible contains from BibleGateway website.

        :param version: The version of the Bible like NIV for New International Version
        """
        log.debug('BGExtract.get_books_from_http("{version}")'.format(version=version))
        url_params = urllib.parse.urlencode({'action': 'getVersionInfo', 'vid': '{version}'.format(version=version)})
        reference_url = 'http://biblegateway.com/versions/?{url}#books'.format(url=url_params)
        page = get_web_page(reference_url)
        if not page:
            send_error_message('download')
            return None
        page_source = page.read()
        try:
            page_source = str(page_source, 'utf8')
        except UnicodeDecodeError:
            page_source = str(page_source, 'cp1251')
        try:
            soup = BeautifulSoup(page_source, 'lxml')
        except Exception:
            log.error('BeautifulSoup could not parse the Bible page.')
            send_error_message('parse')
            return None
        if not soup:
            send_error_message('parse')
            return None
        self.application.process_events()
        content = soup.find('table', 'infotable')
        if content:
            content = content.find_all('tr')
        if not content:
            log.error('No books found in the Biblegateway response.')
            send_error_message('parse')
            return None
        books = []
        for book in content:
            book = book.find('td')
            if book:
                books.append(book.contents[1])
        return books

    def get_bibles_from_http(self):
        """
        Load a list of bibles from BibleGateway website.

        returns a list in the form [(biblename, biblekey, language_code)]
        """
        log.debug('BGExtract.get_bibles_from_http')
        bible_url = 'https://biblegateway.com/versions/'
        soup = get_soup_for_bible_ref(bible_url)
        if not soup:
            return None
        bible_select = soup.find('select', {'class': 'search-translation-select'})
        if not bible_select:
            log.debug('No select tags found - did site change?')
            return None
        option_tags = bible_select.find_all('option')
        if not option_tags:
            log.debug('No option tags found - did site change?')
            return None
        current_lang = ''
        bibles = []
        for ot in option_tags:
            tag_class = ''
            try:
                tag_class = ot['class'][0]
            except KeyError:
                tag_class = ''
            tag_text = ot.get_text()
            if tag_class == 'lang':
                current_lang = tag_text[tag_text.find('(') + 1:tag_text.find(')')].lower()
            elif tag_class == 'spacer':
                continue
            else:
                bibles.append((tag_text, ot['value'], current_lang))
        return bibles
