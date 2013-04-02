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

import logging
import os

from openlp.core.lib import Receiver, SettingsManager, Settings, translate
from openlp.core.utils import AppLocation, delete_file
from openlp.plugins.bibles.lib import parse_reference, get_reference_separator, LanguageSelection
from openlp.plugins.bibles.lib.db import BibleDB, BibleMeta
from csvbible import CSVBible
from http import HTTPBible
from opensong import OpenSongBible
from osis import OSISBible
# Imports that might fail.
try:
    from openlp1 import OpenLP1Bible
    HAS_OPENLP1 = True
except ImportError:
    HAS_OPENLP1 = False

log = logging.getLogger(__name__)

class BibleFormat(object):
    """
    This is a special enumeration class that holds the various types of Bibles,
    plus a few helper functions to facilitate generic handling of Bible types
    for importing.
    """
    _format_availability = {}
    Unknown = -1
    OSIS = 0
    CSV = 1
    OpenSong = 2
    WebDownload = 3
    OpenLP1 = 4

    @staticmethod
    def get_class(format):
        """
        Return the appropriate imeplementation class.

        ``format``
            The Bible format.
        """
        if format == BibleFormat.OSIS:
            return OSISBible
        elif format == BibleFormat.CSV:
            return CSVBible
        elif format == BibleFormat.OpenSong:
            return OpenSongBible
        elif format == BibleFormat.WebDownload:
            return HTTPBible
        elif format == BibleFormat.OpenLP1:
            return OpenLP1Bible
        else:
            return None

    @staticmethod
    def get_formats_list():
        """
        Return a list of the supported Bible formats.
        """
        return [
            BibleFormat.OSIS,
            BibleFormat.CSV,
            BibleFormat.OpenSong,
            BibleFormat.WebDownload,
            BibleFormat.OpenLP1
        ]

    @staticmethod
    def set_availability(format, available):
        BibleFormat._format_availability[format] = available

    @staticmethod
    def get_availability(format):
        return BibleFormat._format_availability.get(format, True)


class BibleManager(object):
    """
    The Bible manager which holds and manages all the Bibles.
    """
    log.info(u'Bible manager loaded')

    def __init__(self, parent):
        """
        Finds all the bibles defined for the system and creates an interface
        object for each bible containing connection information. Throws
        Exception if no Bibles are found.

        Init confirms the bible exists and stores the database path.
        """
        log.debug(u'Bible Initialising')
        self.parent = parent
        self.settingsSection = u'bibles'
        self.web = u'Web'
        self.db_cache = None
        self.path = AppLocation.get_section_data_path(self.settingsSection)
        self.proxy_name = Settings().value(self.settingsSection + u'/proxy name')
        self.suffix = u'.sqlite'
        self.import_wizard = None
        self.reload_bibles()
        self.media = None

    def reload_bibles(self):
        """
        Reloads the Bibles from the available Bible databases on disk. If a web
        Bible is encountered, an instance of HTTPBible is loaded instead of the
        BibleDB class.
        """
        log.debug(u'Reload bibles')
        files = SettingsManager.get_files(self.settingsSection, self.suffix)
        if u'alternative_book_names.sqlite' in files:
            files.remove(u'alternative_book_names.sqlite')
        log.debug(u'Bible Files %s', files)
        self.db_cache = {}
        self.old_bible_databases = []
        for filename in files:
            bible = BibleDB(self.parent, path=self.path, file=filename)
            name = bible.get_name()
            # Remove corrupted files.
            if name is None:
                bible.session.close()
                delete_file(os.path.join(self.path, filename))
                continue
            # Find old database versions.
            if bible.is_old_database():
                self.old_bible_databases.append([filename, name])
                bible.session.close()
                continue
            log.debug(u'Bible Name: "%s"', name)
            self.db_cache[name] = bible
            # Look to see if lazy load bible exists and get create getter.
            source = self.db_cache[name].get_object(BibleMeta, u'download_source')
            if source:
                download_name = self.db_cache[name].get_object(BibleMeta, u'download_name').value
                meta_proxy = self.db_cache[name].get_object(BibleMeta, u'proxy_server')
                web_bible = HTTPBible(self.parent, path=self.path, file=filename, download_source=source.value,
                    download_name=download_name)
                if meta_proxy:
                    web_bible.proxy_server = meta_proxy.value
                self.db_cache[name] = web_bible
        log.debug(u'Bibles reloaded')

    def set_process_dialog(self, wizard):
        """
        Sets the reference to the dialog with the progress bar on it.

        ``dialog``
            The reference to the import wizard.
        """
        self.import_wizard = wizard

    def import_bible(self, type, **kwargs):
        """
        Register a bible in the bible cache, and then import the verses.

        ``type``
            What type of Bible, one of the ``BibleFormat`` values.

        ``**kwargs``
            Keyword arguments to send to the actual importer class.
        """
        class_ = BibleFormat.get_class(type)
        kwargs['path'] = self.path
        importer = class_(self.parent, **kwargs)
        name = importer.register(self.import_wizard)
        self.db_cache[name] = importer
        return importer

    def delete_bible(self, name):
        """
        Delete a bible completely.

        ``name``
            The name of the bible.
        """
        log.debug(u'BibleManager.delete_bible("%s")', name)
        bible = self.db_cache[name]
        bible.session.close()
        bible.session = None
        return delete_file(os.path.join(bible.path, bible.file))

    def get_bibles(self):
        """
        Returns a dict with all available Bibles.
        """
        log.debug(u'get_bibles')
        return self.db_cache

    def get_books(self, bible):
        """
        Returns a list of Bible books, and the number of chapters in that book.

        ``bible``
            Unicode. The Bible to get the list of books from.
        """
        log.debug(u'BibleManager.get_books("%s")', bible)
        return [
            {
                u'name': book.name,
                u'book_reference_id': book.book_reference_id,
                u'chapters': self.db_cache[bible].get_chapter_count(book)
            }
            for book in self.db_cache[bible].get_books()
        ]

    def get_book_by_id(self, bible, id):
        """
        Returns a book object by given id.

        ``bible``
            Unicode. The Bible to get the list of books from.

        ``id``
            Unicode. The book_reference_id to get the book for.
        """
        log.debug(u'BibleManager.get_book_by_id("%s", "%s")', bible, id)
        return self.db_cache[bible].get_book_by_book_ref_id(id)

    def get_chapter_count(self, bible, book):
        """
        Returns the number of Chapters for a given book.

        ``bible``
            Unicode. The Bible to get the list of books from.

        ``book``
            The book object to get the chapter count for.
        """
        log.debug(u'BibleManager.get_book_chapter_count ("%s", "%s")', bible, book.name)
        return self.db_cache[bible].get_chapter_count(book)

    def get_verse_count(self, bible, book, chapter):
        """
        Returns all the number of verses for a given
        book and chapterMaxBibleBookVerses.
        """
        log.debug(u'BibleManager.get_verse_count("%s", "%s", %s)',
            bible, book, chapter)
        language_selection = self.get_language_selection(bible)
        book_ref_id = self.db_cache[bible].get_book_ref_id_by_localised_name(book, language_selection)
        return self.db_cache[bible].get_verse_count(book_ref_id, chapter)

    def get_verse_count_by_book_ref_id(self, bible, book_ref_id, chapter):
        """
        Returns all the number of verses for a given
        book_ref_id and chapterMaxBibleBookVerses.
        """
        log.debug(u'BibleManager.get_verse_count_by_book_ref_id("%s", "%s", "%s")', bible, book_ref_id, chapter)
        return self.db_cache[bible].get_verse_count(book_ref_id, chapter)

    def get_verses(self, bible, versetext, book_ref_id=False, show_error=True):
        """
        Parses a scripture reference, fetches the verses from the Bible
        specified, and returns a list of ``Verse`` objects.

        ``bible``
            Unicode. The Bible to use.

        ``versetext``
            Unicode. The scripture reference. Valid scripture references are:

                - Genesis 1
                - Genesis 1-2
                - Genesis 1:1
                - Genesis 1:1-10
                - Genesis 1:1-10,15-20
                - Genesis 1:1-2:10
                - Genesis 1:1-10,2:1-10

        ``book_ref_id``
            Unicode. The book referece id from the book in versetext.
            For second bible this is necessary.
        """
        log.debug(u'BibleManager.get_verses("%s", "%s")', bible, versetext)
        if not bible:
            if show_error:
                Receiver.send_message(u'openlp_information_message', {
                    u'title': translate('BiblesPlugin.BibleManager', 'No Bibles Available'),
                    u'message': translate('BiblesPlugin.BibleManager',
                        'There are no Bibles currently installed. Please use the '
                        'Import Wizard to install one or more Bibles.')
                    })
            return None
        language_selection = self.get_language_selection(bible)
        reflist = parse_reference(versetext, self.db_cache[bible],
            language_selection, book_ref_id)
        if reflist:
            return self.db_cache[bible].get_verses(reflist, show_error)
        else:
            if show_error:
                reference_seperators = {
                    u'verse': get_reference_separator(u'sep_v_display'),
                    u'range': get_reference_separator(u'sep_r_display'),
                    u'list': get_reference_separator(u'sep_l_display')}
                Receiver.send_message(u'openlp_information_message', {
                    u'title': translate('BiblesPlugin.BibleManager',
                    'Scripture Reference Error'),
                    u'message': translate('BiblesPlugin.BibleManager',
                    'Your scripture reference is either not supported by '
                    'OpenLP or is invalid. Please make sure your reference '
                    'conforms to one of the following patterns or consult the '
                    'manual:\n\n'
                    'Book Chapter\n'
                    'Book Chapter%(range)sChapter\n'
                    'Book Chapter%(verse)sVerse%(range)sVerse\n'
                    'Book Chapter%(verse)sVerse%(range)sVerse%(list)sVerse'
                    '%(range)sVerse\n'
                    'Book Chapter%(verse)sVerse%(range)sVerse%(list)sChapter'
                    '%(verse)sVerse%(range)sVerse\n'
                    'Book Chapter%(verse)sVerse%(range)sChapter%(verse)sVerse',
                    'Please pay attention to the appended "s" of the wildcards '
                    'and refrain from translating the words inside the '
                    'names in the brackets.') % reference_seperators
                    })
            return None

    def get_language_selection(self, bible):
        """
        Returns the language selection of a bible.

        ``bible``
            Unicode. The Bible to get the language selection from.
        """
        log.debug(u'BibleManager.get_language_selection("%s")', bible)
        language_selection = self.get_meta_data(bible, u'book_name_language')
        if not language_selection or language_selection.value == "None" or language_selection.value == "-1":
            # If None is returned, it's not the singleton object but a
            # BibleMeta object with the value "None"
            language_selection = Settings().value(self.settingsSection + u'/book name language')
        else:
            language_selection = language_selection.value
        try:
            language_selection = int(language_selection)
        except (ValueError, TypeError):
            language_selection = LanguageSelection.Application
        return language_selection

    def verse_search(self, bible, second_bible, text):
        """
        Does a verse search for the given bible and text.

        ``bible``
            The bible to search in (unicode).

        ``second_bible``
            The second bible (unicode). We do not search in this bible.

        ``text``
            The text to search for (unicode).
        """
        log.debug(u'BibleManager.verse_search("%s", "%s")', bible, text)
        if not bible:
            Receiver.send_message(u'openlp_information_message', {
                u'title': translate('BiblesPlugin.BibleManager', 'No Bibles Available'),
                u'message': translate('BiblesPlugin.BibleManager',
                    'There are no Bibles currently installed. Please use the '
                    'Import Wizard to install one or more Bibles.')
                })
            return None
        # Check if the bible or second_bible is a web bible.
        webbible = self.db_cache[bible].get_object(BibleMeta,
            u'download_source')
        second_webbible = u''
        if second_bible:
            second_webbible = self.db_cache[second_bible].get_object(BibleMeta,
                u'download_source')
        if webbible or second_webbible:
            Receiver.send_message(u'openlp_information_message', {
                u'title': translate('BiblesPlugin.BibleManager', 'Web Bible cannot be used'),
                u'message': translate('BiblesPlugin.BibleManager', 'Text Search is not available with Web Bibles.')
                })
            return None
        if text:
            return self.db_cache[bible].verse_search(text)
        else:
            Receiver.send_message(u'openlp_information_message', {
                u'title': translate('BiblesPlugin.BibleManager', 'Scripture Reference Error'),
                u'message': translate('BiblesPlugin.BibleManager', 'You did not enter a search keyword.\n'
                    'You can separate different keywords by a space to '
                    'search for all of your keywords and you can separate '
                    'them by a comma to search for one of them.')
                })
            return None

    def save_meta_data(self, bible, version, copyright, permissions,
        book_name_language=None):
        """
        Saves the bibles meta data.
        """
        log.debug(u'save_meta data %s, %s, %s, %s',
            bible, version, copyright, permissions)
        self.db_cache[bible].save_meta(u'name', version)
        self.db_cache[bible].save_meta(u'copyright', copyright)
        self.db_cache[bible].save_meta(u'permissions', permissions)
        self.db_cache[bible].save_meta(u'book_name_language',
            book_name_language)

    def get_meta_data(self, bible, key):
        """
        Returns the meta data for a given key.
        """
        log.debug(u'get_meta %s,%s', bible, key)
        return self.db_cache[bible].get_object(BibleMeta, key)

    def update_book(self, bible, book):
        """
        Update a book of the bible.
        """
        log.debug(u'BibleManager.update_book("%s", "%s")', bible, book.name)
        self.db_cache[bible].update_book(book)

    def exists(self, name):
        """
        Check cache to see if new bible.
        """
        if not isinstance(name, unicode):
            name = unicode(name)
        for bible in self.db_cache.keys():
            log.debug(u'Bible from cache in is_new_bible %s', bible)
            if not isinstance(bible, unicode):
                bible = unicode(bible)
            if bible == name:
                return True
        return False

    def finalise(self):
        """
        Loop through the databases to VACUUM them.
        """
        for bible in self.db_cache:
            self.db_cache[bible].finalise()

BibleFormat.set_availability(BibleFormat.OpenLP1, HAS_OPENLP1)

__all__ = [u'BibleFormat']
