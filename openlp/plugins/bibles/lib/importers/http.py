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

from bs4 import BeautifulSoup, NavigableString, Tag

from openlp.core.common import Registry, RegistryProperties, translate
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.lib.webpagereader import get_web_page
from openlp.plugins.bibles.lib import SearchResults
from openlp.plugins.bibles.lib.bibleimport import BibleImport
from openlp.plugins.bibles.lib.db import BibleDB, BiblesResourcesDB, Book

CLEANER_REGEX = re.compile(r'&nbsp;|<br />|\'\+\'')

log = logging.getLogger(__name__)


class HTTPBible(BibleImport, RegistryProperties):
    log.info('{name} HTTPBible loaded'.format(name=__name__))

    def __init__(self, *args, **kwargs):
        """
        Finds all the bibles defined for the system. Creates an Interface Object for each bible containing connection
        information.

        Throws Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        super().__init__(*args, **kwargs)
        self.download_source = kwargs['download_source']
        self.download_name = kwargs['download_name']
        # TODO: Clean up proxy stuff. We probably want one global proxy per connection type (HTTP and HTTPS) at most.
        self.proxy_server = None
        self.proxy_username = None
        self.proxy_password = None
        self.language_id = None
        if 'path' in kwargs:
            self.path = kwargs['path']
        if 'proxy_server' in kwargs:
            self.proxy_server = kwargs['proxy_server']
        if 'proxy_username' in kwargs:
            self.proxy_username = kwargs['proxy_username']
        if 'proxy_password' in kwargs:
            self.proxy_password = kwargs['proxy_password']
        if 'language_id' in kwargs:
            self.language_id = kwargs['language_id']

    def do_import(self, bible_name=None):
        """
        Run the import. This method overrides the parent class method. Returns ``True`` on success, ``False`` on
        failure.
        """
        self.wizard.progress_bar.setMaximum(68)
        self.wizard.increment_progress_bar(translate('BiblesPlugin.HTTPBible',
                                                     'Registering Bible and loading books...'))
        self.save_meta('download_source', self.download_source)
        self.save_meta('download_name', self.download_name)
        if self.proxy_server:
            self.save_meta('proxy_server', self.proxy_server)
        if self.proxy_username:
            # Store the proxy userid.
            self.save_meta('proxy_username', self.proxy_username)
        if self.proxy_password:
            # Store the proxy password.
            self.save_meta('proxy_password', self.proxy_password)
        if self.download_source.lower() == 'crosswalk':
            handler = CWExtract(self.proxy_server)
        elif self.download_source.lower() == 'biblegateway':
            handler = BGExtract(self.proxy_server)
        elif self.download_source.lower() == 'bibleserver':
            handler = BSExtract(self.proxy_server)
        books = handler.get_books_from_http(self.download_name)
        if not books:
            log.error('Importing books from {source} - download name: "{name}" '
                      'failed'.format(source=self.download_source, name=self.download_name))
            return False
        self.wizard.progress_bar.setMaximum(len(books) + 2)
        self.wizard.increment_progress_bar(translate('BiblesPlugin.HTTPBible', 'Registering Language...'))
        self.language_id = self.get_language_id(bible_name=bible_name)
        if not self.language_id:
            return False
        for book in books:
            if self.stop_import_flag:
                break
            self.wizard.increment_progress_bar(translate('BiblesPlugin.HTTPBible',
                                                         'Importing {book}...',
                                                         'Importing <book name>...').format(book=book))
            book_ref_id = self.get_book_ref_id_by_name(book, len(books), self.language_id)
            if not book_ref_id:
                log.error('Importing books from {source} - download name: "{name}" '
                          'failed'.format(source=self.download_source, name=self.download_name))
                return False
            book_details = BiblesResourcesDB.get_book_by_id(book_ref_id)
            log.debug('Book details: Name:{book}; id:{ref}; '
                      'testament_id:{detail}'.format(book=book,
                                                     ref=book_ref_id,
                                                     detail=book_details['testament_id']))
            self.create_book(book, book_ref_id, book_details['testament_id'])
        if self.stop_import_flag:
            return False
        else:
            return True

    def get_verses(self, reference_list, show_error=True):
        """
        A reimplementation of the ``BibleDB.get_verses`` method, this one is specifically for web Bibles. It first
        checks to see if the particular chapter exists in the DB, and if not it pulls it from the web. If the chapter
        DOES exist, it simply pulls the verses from the DB using the ancestor method.

        ``reference_list``
            This is the list of references the media manager item wants. It is a list of tuples, with the following
            format::

                (book_reference_id, chapter, start_verse, end_verse)

            Therefore, when you are looking for multiple items, simply break them up into references like this, bundle
            them into a list. This function then runs through the list, and returns an amalgamated list of ``Verse``
            objects. For example::

                [('35', 1, 1, 1), ('35', 2, 2, 3)]
        """
        log.debug('HTTPBible.get_verses("{ref}")'.format(ref=reference_list))
        for reference in reference_list:
            book_id = reference[0]
            db_book = self.get_book_by_book_ref_id(book_id)
            if not db_book:
                if show_error:
                    critical_error_message_box(
                        translate('BiblesPlugin', 'No Book Found'),
                        translate('BiblesPlugin', 'No matching book could be found in this Bible. Check that you have '
                                  'spelled the name of the book correctly.'))
                return []
            book = db_book.name
            if BibleDB.get_verse_count(self, book_id, reference[1]) == 0:
                self.application.set_busy_cursor()
                search_results = self.get_chapter(book, reference[1])
                if search_results and search_results.has_verse_list():
                    # We have found a book of the bible lets check to see
                    # if it was there. By reusing the returned book name
                    # we get a correct book. For example it is possible
                    # to request ac and get Acts back.
                    book_name = search_results.book
                    self.application.process_events()
                    # Check to see if book/chapter exists.
                    db_book = self.get_book(book_name)
                    self.create_chapter(db_book.id, search_results.chapter, search_results.verse_list)
                    self.application.process_events()
                self.application.set_normal_cursor()
            self.application.process_events()
        return BibleDB.get_verses(self, reference_list, show_error)

    def get_chapter(self, book, chapter):
        """
        Receive the request and call the relevant handler methods.
        """
        log.debug('HTTPBible.get_chapter("{book}", "{chapter}")'.format(book=book, chapter=chapter))
        log.debug('source = {source}'.format(source=self.download_source))
        if self.download_source.lower() == 'crosswalk':
            handler = CWExtract(self.proxy_server)
        elif self.download_source.lower() == 'biblegateway':
            handler = BGExtract(self.proxy_server)
        elif self.download_source.lower() == 'bibleserver':
            handler = BSExtract(self.proxy_server)
        return handler.get_bible_chapter(self.download_name, book, chapter)

    def get_books(self):
        """
        Return the list of books.
        """
        log.debug('HTTPBible.get_books("{name}")'.format(name=Book.name))
        return self.get_all_objects(Book, order_by_ref=Book.id)

    def get_chapter_count(self, book):
        """
        Return the number of chapters in a particular book.

        :param book: The book object to get the chapter count for.
        """
        log.debug('HTTPBible.get_chapter_count("{name}")'.format(name=book.name))
        return BiblesResourcesDB.get_chapter_count(book.book_reference_id)

    def get_verse_count(self, book_id, chapter):
        """
        Return the number of verses for the specified chapter and book.

        :param book_id: The name of the book.
        :param chapter: The chapter whose verses are being counted.
        """
        log.debug('HTTPBible.get_verse_count("{ref}", {chapter})'.format(ref=book_id, chapter=chapter))
        return BiblesResourcesDB.get_verse_count(book_id, chapter)


def get_soup_for_bible_ref(reference_url, header=None, pre_parse_regex=None, pre_parse_substitute=None):
    """
    Gets a webpage and returns a parsed and optionally cleaned soup or None.

    :param reference_url: The URL to obtain the soup from.
    :param header: An optional HTTP header to pass to the bible web server.
    :param pre_parse_regex: A regular expression to run on the webpage. Allows manipulation of the webpage before
        passing to BeautifulSoup for parsing.
    :param pre_parse_substitute: The text to replace any matches to the regular expression with.
    """
    if not reference_url:
        return None
    try:
        page = get_web_page(reference_url, header, True)
    except:
        page = None
    if not page:
        send_error_message('download')
        return None
    page_source = page.read()
    if pre_parse_regex and pre_parse_substitute is not None:
        page_source = re.sub(pre_parse_regex, pre_parse_substitute, page_source.decode())
    soup = None
    try:
        soup = BeautifulSoup(page_source, 'lxml')
        CLEANER_REGEX.sub('', str(soup))
    except Exception:
        log.exception('BeautifulSoup could not parse the bible page.')
    if not soup:
        send_error_message('parse')
        return None
    Registry().get('application').process_events()
    return soup


def send_error_message(error_type):
    """
    Send a standard error message informing the user of an issue.

    :param error_type: The type of error that occurred for the issue.
    """
    if error_type == 'download':
        critical_error_message_box(
            translate('BiblesPlugin.HTTPBible', 'Download Error'),
            translate('BiblesPlugin.HTTPBible', 'There was a problem downloading your verse selection. Please check '
                      'your Internet connection, and if this error continues to occur please consider reporting a bug'
                      '.'))
    elif error_type == 'parse':
        critical_error_message_box(
            translate('BiblesPlugin.HTTPBible', 'Parse Error'),
            translate('BiblesPlugin.HTTPBible', 'There was a problem extracting your verse selection. If this error '
                      'continues to occur please consider reporting a bug.'))
