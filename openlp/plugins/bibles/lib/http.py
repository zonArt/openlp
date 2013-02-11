# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
The :mod:`http` module enables OpenLP to retrieve scripture from bible
websites.
"""
import logging
import re
import socket
import urllib
from HTMLParser import HTMLParseError

from BeautifulSoup import BeautifulSoup, NavigableString, Tag

from openlp.core.lib import Registry, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.utils import get_web_page
from openlp.plugins.bibles.lib import SearchResults
from openlp.plugins.bibles.lib.db import BibleDB, BiblesResourcesDB, Book

UGLY_CHARS = {
    u'\u2014': u' - ',
    u'\u2018': u'\'',
    u'\u2019': u'\'',
    u'\u201c': u'"',
    u'\u201d': u'"',
    u'&nbsp;': u' '
}

log = logging.getLogger(__name__)

class BGExtract(object):
    """
    Extract verses from BibleGateway
    """
    def __init__(self, proxy_url=None):
        log.debug(u'BGExtract.init("%s")', proxy_url)
        self.proxy_url = proxy_url
        socket.setdefaulttimeout(30)

    def _remove_elements(self, parent, tag, class_=None):
        """
        Remove a particular element from the BeautifulSoup tree.

        ``parent``
            The element from which items need to be removed.

        ``tag``
            A string of the tab type, e.g. "div"

        ``class_``
            An HTML class attribute for further qualification.
        """
        if class_:
            all_tags = parent.findAll(tag, class_)
        else:
            all_tags = parent.findAll(tag)
        for element in all_tags:
            element.extract()

    def _extract_verse(self, tag):
        """
        Extract a verse (or part of a verse) from a tag.

        ``tag``
            The BeautifulSoup Tag element with the stuff we want.
        """
        if isinstance(tag, NavigableString):
            return None, unicode(tag)
        elif tag.get('class') == 'versenum' or tag.get('class') == 'versenum mid-line':
            verse = unicode(tag.string).replace('[', '').replace(']', '').strip()
            return verse, None
        elif tag.get('class') == 'chapternum':
            verse = '1'
            return verse, None
        else:
            verse, text = None, ''
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

        ``tag``
            The base tag within which we want to remove stuff.
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

        ``tags``
            A list of BeautifulSoup Tag elements.
        """
        verses = []
        tags = tags[::-1]
        current_text = ''
        for tag in tags:
            verse, text = None, ''
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
                for old, new in UGLY_CHARS.iteritems():
                    text = text.replace(old, new)
                text = u' '.join(text.split())
            if verse and text:
                verse = verse.strip()
                try:
                    verse = int(verse)
                except ValueError:
                    verse_parts = verse.split(u'-')
                    if len(verse_parts) > 1:
                        verse = int(verse_parts[0])
                except TypeError:
                    log.warn(u'Illegal verse number: %s', unicode(verse))
                verses.append((verse, text))
        verse_list = {}
        for verse, text in verses[::-1]:
            verse_list[verse] = text
        return verse_list

    def _extract_verses_old(self, div):
        """
        Use the old style of parsing for those Bibles on BG who mysteriously
        have not been migrated to the new (still broken) HTML.

        ``div``
            The parent div.
        """
        verse_list = {}
        # Cater for inconsistent mark up in the first verse of a chapter.
        first_verse = div.find(u'versenum')
        if first_verse and first_verse.contents:
            verse_list[1] = unicode(first_verse.contents[0])
        for verse in div(u'sup', u'versenum'):
            raw_verse_num = verse.next
            clean_verse_num = 0
            # Not all verses exist in all translations and may or may not be
            # represented by a verse number. If they are not fine, if they are
            # it will probably be in a format that breaks int(). We will then
            # have no idea what garbage may be sucked in to the verse text so
            # if we do not get a clean int() then ignore the verse completely.
            try:
                clean_verse_num = int(str(raw_verse_num))
            except ValueError:
                verse_parts = str(raw_verse_num).split(u'-')
                if len(verse_parts) > 1:
                    clean_verse_num = int(verse_parts[0])
            except TypeError:
                log.warn(u'Illegal verse number: %s', unicode(raw_verse_num))
            if clean_verse_num:
                verse_text = raw_verse_num.next
                part = raw_verse_num.next.next
                while not (isinstance(part, Tag) and part.get(u'class') == u'versenum'):
                    # While we are still in the same verse grab all the text.
                    if isinstance(part, NavigableString):
                        verse_text += part
                    if isinstance(part.next, Tag) and part.next.name == u'div':
                        # Run out of verses so stop.
                        break
                    part = part.next
                verse_list[clean_verse_num] = unicode(verse_text)
        return verse_list

    def get_bible_chapter(self, version, book_name, chapter):
        """
        Access and decode Bibles via the BibleGateway website.

        ``version``
            The version of the Bible like 31 for New International version.

        ``book_name``
            Name of the Book.

        ``chapter``
            Chapter number.
        """
        log.debug(u'BGExtract.get_bible_chapter("%s", "%s", "%s")', version, book_name, chapter)
        url_book_name = urllib.quote(book_name.encode("utf-8"))
        url_params = u'search=%s+%s&version=%s' % (url_book_name, chapter, version)
        cleaner = [(re.compile('&nbsp;|<br />|\'\+\''), lambda match: '')]
        soup = get_soup_for_bible_ref(
            u'http://www.biblegateway.com/passage/?%s' % url_params,
            pre_parse_regex=r'<meta name.*?/>', pre_parse_substitute='', cleaner=cleaner)
        self.application.process_events()
        if not soup:
            return None
        self.application.process_events()
        div = soup.find('div', 'result-text-style-normal')
        self._clean_soup(div)
        span_list = div.findAll('span', 'text')
        log.debug('Span list: %s', span_list)
        if not span_list:
            # If we don't get any spans then we must have the old HTML format
            verse_list = self._extract_verses_old(div)
        else:
            verse_list = self._extract_verses(span_list)
        if not verse_list:
            log.debug(u'No content found in the BibleGateway response.')
            send_error_message(u'parse')
            return None
        return SearchResults(book_name, chapter, verse_list)

    def get_books_from_http(self, version):
        """
        Load a list of all books a Bible contaions from BibleGateway website.

        ``version``
            The version of the Bible like NIV for New International Version
        """
        log.debug(u'BGExtract.get_books_from_http("%s")', version)
        url_params = urllib.urlencode({u'action': 'getVersionInfo', u'vid': u'%s' % version})
        reference_url = u'http://www.biblegateway.com/versions/?%s#books' % url_params
        page = get_web_page(reference_url)
        if not page:
            send_error_message(u'download')
            return None
        page_source = page.read()
        try:
            page_source = unicode(page_source, u'utf8')
        except UnicodeDecodeError:
            page_source = unicode(page_source, u'cp1251')
        try:
            soup = BeautifulSoup(page_source)
        except HTMLParseError:
            log.error(u'BeautifulSoup could not parse the Bible page.')
            send_error_message(u'parse')
            return None
        if not soup:
            send_error_message(u'parse')
            return None
        self.application.process_events()
        content = soup.find(u'table', u'infotable')
        if content:
            content = content.findAll(u'tr')
        if not content:
            log.error(u'No books found in the Biblegateway response.')
            send_error_message(u'parse')
            return None
        books = []
        for book in content:
            book = book.find(u'td')
            if book:
                books.append(book.contents[0])
        return books


class BSExtract(object):
    """
    Extract verses from Bibleserver.com
    """
    def __init__(self, proxy_url=None):
        log.debug(u'BSExtract.init("%s")', proxy_url)
        self.proxy_url = proxy_url
        socket.setdefaulttimeout(30)

    def get_bible_chapter(self, version, book_name, chapter):
        """
        Access and decode bibles via Bibleserver mobile website

        ``version``
            The version of the bible like NIV for New International Version

        ``book_name``
            Text name of bible book e.g. Genesis, 1. John, 1John or Offenbarung

        ``chapter``
            Chapter number
        """
        log.debug(u'BSExtract.get_bible_chapter("%s", "%s", "%s")', version, book_name, chapter)
        url_version = urllib.quote(version.encode("utf-8"))
        url_book_name = urllib.quote(book_name.encode("utf-8"))
        chapter_url = u'http://m.bibleserver.com/text/%s/%s%d' % (url_version, url_book_name, chapter)
        header = (u'Accept-Language', u'en')
        soup = get_soup_for_bible_ref(chapter_url, header)
        if not soup:
            return None
        self.application.process_events()
        content = soup.find(u'div', u'content')
        if not content:
            log.error(u'No verses found in the Bibleserver response.')
            send_error_message(u'parse')
            return None
        content = content.find(u'div').findAll(u'div')
        verse_number = re.compile(r'v(\d{1,2})(\d{3})(\d{3}) verse.*')
        verses = {}
        for verse in content:
            self.application.process_events()
            versenumber = int(verse_number.sub(r'\3', verse[u'class']))
            verses[versenumber] = verse.contents[1].rstrip(u'\n')
        return SearchResults(book_name, chapter, verses)

    def get_books_from_http(self, version):
        """
        Load a list of all books a Bible contains from Bibleserver mobile
        website.

        ``version``
            The version of the Bible like NIV for New International Version
        """
        log.debug(u'BSExtract.get_books_from_http("%s")', version)
        urlversion = urllib.quote(version.encode("utf-8"))
        chapter_url = u'http://m.bibleserver.com/overlay/selectBook?translation=%s' % (urlversion)
        soup = get_soup_for_bible_ref(chapter_url)
        if not soup:
            return None
        content = soup.find(u'ul')
        if not content:
            log.error(u'No books found in the Bibleserver response.')
            send_error_message(u'parse')
            return None
        content = content.findAll(u'li')
        return [book.contents[0].contents[0] for book in content]


class CWExtract(object):
    """
    Extract verses from CrossWalk/BibleStudyTools
    """
    def __init__(self, proxy_url=None):
        log.debug(u'CWExtract.init("%s")', proxy_url)
        self.proxy_url = proxy_url
        socket.setdefaulttimeout(30)

    def get_bible_chapter(self, version, book_name, chapter):
        """
        Access and decode bibles via the Crosswalk website

        ``version``
            The version of the Bible like niv for New International Version

        ``book_name``
            Text name of in english e.g. 'gen' for Genesis

        ``chapter``
            Chapter number
        """
        log.debug(u'CWExtract.get_bible_chapter("%s", "%s", "%s")', version, book_name, chapter)
        url_book_name = book_name.replace(u' ', u'-')
        url_book_name = url_book_name.lower()
        url_book_name = urllib.quote(url_book_name.encode("utf-8"))
        chapter_url = u'http://www.biblestudytools.com/%s/%s/%s.html' % (version, url_book_name, chapter)
        soup = get_soup_for_bible_ref(chapter_url)
        if not soup:
            return None
        self.application.process_events()
        html_verses = soup.findAll(u'span', u'versetext')
        if not html_verses:
            log.error(u'No verses found in the CrossWalk response.')
            send_error_message(u'parse')
            return None
        verses = {}
        reduce_spaces = re.compile(r'[ ]{2,}')
        fix_punctuation = re.compile(r'[ ]+([.,;])')
        for verse in html_verses:
            self.application.process_events()
            verse_number = int(verse.contents[0].contents[0])
            verse_text = u''
            for part in verse.contents:
                self.application.process_events()
                if isinstance(part, NavigableString):
                    verse_text += part
                elif part and part.attrMap and \
                        (part.attrMap[u'class'] == u'WordsOfChrist' or part.attrMap[u'class'] == u'strongs'):
                    for subpart in part.contents:
                        self.application.process_events()
                        if isinstance(subpart, NavigableString):
                            verse_text += subpart
                        elif subpart and subpart.attrMap and subpart.attrMap[u'class'] == u'strongs':
                            for subsub in subpart.contents:
                                self.application.process_events()
                                if isinstance(subsub, NavigableString):
                                    verse_text += subsub
            self.application.process_events()
            # Fix up leading and trailing spaces, multiple spaces, and spaces
            # between text and , and .
            verse_text = verse_text.strip(u'\n\r\t ')
            verse_text = reduce_spaces.sub(u' ', verse_text)
            verse_text = fix_punctuation.sub(r'\1', verse_text)
            verses[verse_number] = verse_text
        return SearchResults(book_name, chapter, verses)

    def get_books_from_http(self, version):
        """
        Load a list of all books a Bible contain from the Crosswalk website.

        ``version``
            The version of the bible like NIV for New International Version
        """
        log.debug(u'CWExtract.get_books_from_http("%s")', version)
        chapter_url = u'http://www.biblestudytools.com/%s/' % (version)
        soup = get_soup_for_bible_ref(chapter_url)
        if not soup:
            return None
        content = soup.find(u'div', {u'class': u'Body'})
        content = content.find(u'ul', {u'class': u'parent'})
        if not content:
            log.error(u'No books found in the Crosswalk response.')
            send_error_message(u'parse')
            return None
        content = content.findAll(u'li')
        books = []
        for book in content:
            book = book.find(u'a')
            books.append(book.contents[0])
        return books


class HTTPBible(BibleDB):
    log.info(u'%s HTTPBible loaded', __name__)

    def __init__(self, parent, **kwargs):
        """
        Finds all the bibles defined for the system
        Creates an Interface Object for each bible containing connection
        information

        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        BibleDB.__init__(self, parent, **kwargs)
        self.download_source = kwargs[u'download_source']
        self.download_name = kwargs[u'download_name']
        # TODO: Clean up proxy stuff. We probably want one global proxy per
        # connection type (HTTP and HTTPS) at most.
        self.proxy_server = None
        self.proxy_username = None
        self.proxy_password = None
        if u'path' in kwargs:
            self.path = kwargs[u'path']
        if u'proxy_server' in kwargs:
            self.proxy_server = kwargs[u'proxy_server']
        if u'proxy_username' in kwargs:
            self.proxy_username = kwargs[u'proxy_username']
        if u'proxy_password' in kwargs:
            self.proxy_password = kwargs[u'proxy_password']

    def do_import(self, bible_name=None):
        """
        Run the import. This method overrides the parent class method. Returns
        ``True`` on success, ``False`` on failure.
        """
        self.wizard.progressBar.setMaximum(68)
        self.wizard.incrementProgressBar(translate('BiblesPlugin.HTTPBible', 'Registering Bible and loading books...'))
        self.save_meta(u'download_source', self.download_source)
        self.save_meta(u'download_name', self.download_name)
        if self.proxy_server:
            self.save_meta(u'proxy_server', self.proxy_server)
        if self.proxy_username:
            # Store the proxy userid.
            self.save_meta(u'proxy_username', self.proxy_username)
        if self.proxy_password:
            # Store the proxy password.
            self.save_meta(u'proxy_password', self.proxy_password)
        if self.download_source.lower() == u'crosswalk':
            handler = CWExtract(self.proxy_server)
        elif self.download_source.lower() == u'biblegateway':
            handler = BGExtract(self.proxy_server)
        elif self.download_source.lower() == u'bibleserver':
            handler = BSExtract(self.proxy_server)
        books = handler.get_books_from_http(self.download_name)
        if not books:
            log.exception(u'Importing books from %s - download name: "%s" '\
                'failed' % (self.download_source, self.download_name))
            return False
        self.wizard.progressBar.setMaximum(len(books) + 2)
        self.wizard.incrementProgressBar(translate( 'BiblesPlugin.HTTPBible', 'Registering Language...'))
        bible = BiblesResourcesDB.get_webbible(self.download_name, self.download_source.lower())
        if bible[u'language_id']:
            language_id = bible[u'language_id']
            self.save_meta(u'language_id', language_id)
        else:
            language_id = self.get_language(bible_name)
        if not language_id:
            log.exception(u'Importing books from %s failed' % self.filename)
            return False
        for book in books:
            if self.stop_import_flag:
                break
            self.wizard.incrementProgressBar(translate(
                'BiblesPlugin.HTTPBible', 'Importing %s...',
                'Importing <book name>...') % book)
            book_ref_id = self.get_book_ref_id_by_name(book, len(books), language_id)
            if not book_ref_id:
                log.exception(u'Importing books from %s - download name: "%s" '\
                    'failed' % (self.download_source, self.download_name))
                return False
            book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
            log.debug(u'Book details: Name:%s; id:%s; testament_id:%s',
                book, book_ref_id, book_details[u'testament_id'])
            self.create_book(book, book_ref_id, book_details[u'testament_id'])
        if self.stop_import_flag:
            return False
        else:
            return True

    def get_verses(self, reference_list, show_error=True):
        """
        A reimplementation of the ``BibleDB.get_verses`` method, this one is
        specifically for web Bibles. It first checks to see if the particular
        chapter exists in the DB, and if not it pulls it from the web. If the
        chapter DOES exist, it simply pulls the verses from the DB using the
        ancestor method.

        ``reference_list``
            This is the list of references the media manager item wants. It is
            a list of tuples, with the following format::

                (book_reference_id, chapter, start_verse, end_verse)

            Therefore, when you are looking for multiple items, simply break
            them up into references like this, bundle them into a list. This
            function then runs through the list, and returns an amalgamated
            list of ``Verse`` objects. For example::

                [(u'35', 1, 1, 1), (u'35', 2, 2, 3)]
        """
        log.debug(u'HTTPBible.get_verses("%s")', reference_list)
        for reference in reference_list:
            book_id = reference[0]
            db_book = self.get_book_by_book_ref_id(book_id)
            if not db_book:
                if show_error:
                    critical_error_message_box(
                        translate('BiblesPlugin', 'No Book Found'),
                        translate('BiblesPlugin', 'No matching '
                        'book could be found in this Bible. Check that you '
                        'have spelled the name of the book correctly.'))
                return []
            book = db_book.name
            if BibleDB.get_verse_count(self, book_id, reference[1]) == 0:
                self.application.set_busy_cursor()
                search_results = self.get_chapter(book, reference[1])
                if search_results and search_results.has_verselist():
                    ## We have found a book of the bible lets check to see
                    ## if it was there. By reusing the returned book name
                    ## we get a correct book. For example it is possible
                    ## to request ac and get Acts back.
                    book_name = search_results.book
                    self.application.process_events()
                    # Check to see if book/chapter exists.
                    db_book = self.get_book(book_name)
                    self.create_chapter(db_book.id, search_results.chapter, search_results.verselist)
                    self.application.process_events()
                self.application.set_normal_cursor()
            self.application.process_events()
        return BibleDB.get_verses(self, reference_list, show_error)

    def get_chapter(self, book, chapter):
        """
        Receive the request and call the relevant handler methods.
        """
        log.debug(u'HTTPBible.get_chapter("%s", "%s")', book, chapter)
        log.debug(u'source = %s', self.download_source)
        if self.download_source.lower() == u'crosswalk':
            handler = CWExtract(self.proxy_server)
        elif self.download_source.lower() == u'biblegateway':
            handler = BGExtract(self.proxy_server)
        elif self.download_source.lower() == u'bibleserver':
            handler = BSExtract(self.proxy_server)
        return handler.get_bible_chapter(self.download_name, book, chapter)

    def get_books(self):
        """
        Return the list of books.
        """
        log.debug(u'HTTPBible.get_books("%s")', Book.name)
        return self.get_all_objects(Book, order_by_ref=Book.id)

    def get_chapter_count(self, book):
        """
        Return the number of chapters in a particular book.

        ``book``
        The book object to get the chapter count for.
        """
        log.debug(u'HTTPBible.get_chapter_count("%s")', book.name)
        return BiblesResourcesDB.get_chapter_count(book.book_reference_id)

    def get_verse_count(self, book_id, chapter):
        """
        Return the number of verses for the specified chapter and book.

        ``book``
            The name of the book.

        ``chapter``
            The chapter whose verses are being counted.
        """
        log.debug(u'HTTPBible.get_verse_count("%s", %s)', book_id, chapter)
        return BiblesResourcesDB.get_verse_count(book_id, chapter)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)

def get_soup_for_bible_ref(reference_url, header=None, pre_parse_regex=None,
    pre_parse_substitute=None, cleaner=None):
    """
    Gets a webpage and returns a parsed and optionally cleaned soup or None.

    ``reference_url``
        The URL to obtain the soup from.

    ``header``
        An optional HTTP header to pass to the bible web server.

    ``pre_parse_regex``
        A regular expression to run on the webpage. Allows manipulation of the
        webpage before passing to BeautifulSoup for parsing.

    ``pre_parse_substitute``
        The text to replace any matches to the regular expression with.

    ``cleaner``
        An optional regex to use during webpage parsing.
    """
    if not reference_url:
        return None
    page = get_web_page(reference_url, header, True)
    if not page:
        send_error_message(u'download')
        return None
    page_source = page.read()
    if pre_parse_regex and pre_parse_substitute is not None:
        page_source = re.sub(pre_parse_regex, pre_parse_substitute, page_source)
    soup = None
    try:
        if cleaner:
            soup = BeautifulSoup(page_source, markupMassage=cleaner)
        else:
            soup = BeautifulSoup(page_source)
    except HTMLParseError:
        log.exception(u'BeautifulSoup could not parse the bible page.')
    if not soup:
        send_error_message(u'parse')
        return None
    Registry().get(u'application').process_events()
    return soup

def send_error_message(error_type):
    """
    Send a standard error message informing the user of an issue.

    ``error_type``
        The type of error that occured for the issue.
    """
    if error_type == u'download':
        critical_error_message_box(
            translate('BiblesPlugin.HTTPBible', 'Download Error'),
            translate('BiblesPlugin.HTTPBible', 'There was a '
            'problem downloading your verse selection. Please check your '
            'Internet connection, and if this error continues to occur '
            'please consider reporting a bug.'))
    elif error_type == u'parse':
        critical_error_message_box(
            translate('BiblesPlugin.HTTPBible', 'Parse Error'),
            translate('BiblesPlugin.HTTPBible', 'There was a '
            'problem extracting your verse selection. If this error continues '
            'to occur please consider reporting a bug.'))
