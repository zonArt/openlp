# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import codecs
import datetime
import logging
import os
import re

from PyQt4 import QtCore

from openlp.core.lib import Receiver, translate
from openlp.core.ui.wizard import WizardStrings
from openlp.core.utils import AppLocation
from openlp.plugins.songs.lib import clean_song, VerseType
from openlp.plugins.songs.lib.db import Song, Author, Topic, Book, MediaFile
from openlp.plugins.songs.lib.ui import SongStrings
from openlp.plugins.songs.lib.xml import SongXML

log = logging.getLogger(__name__)

class SongImport(QtCore.QObject):
    """
    Helper class for import a song from a third party source into OpenLP

    This class just takes the raw strings, and will work out for itself
    whether the authors etc already exist and add them or refer to them
    as necessary
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise and create defaults for properties

        ``manager``
            An instance of a SongManager, through which all database access is
            performed.

        """
        self.manager = manager
        QtCore.QObject.__init__(self)
        if kwargs.has_key(u'filename'):
            self.import_source = kwargs[u'filename']
        elif kwargs.has_key(u'filenames'):
            self.import_source = kwargs[u'filenames']
        else:
            raise KeyError(u'Keyword arguments "filename[s]" not supplied.')
        log.debug(self.import_source)
        self.import_wizard = None
        self.song = None
        self.stop_import_flag = False
        self.set_defaults()
        self.error_log = []
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_stop_wizard'), self.stop_import)

    def set_defaults(self):
        """
        Create defaults for properties - call this before each song
        if importing many songs at once to ensure a clean beginning
        """
        self.title = u''
        self.song_number = u''
        self.alternate_title = u''
        self.copyright = u''
        self.comments = u''
        self.theme_name = u''
        self.ccli_number = u''
        self.authors = []
        self.topics = []
        self.media_files = []
        self.song_book_name = u''
        self.song_book_pub = u''
        self.verse_order_list_generated_useful = False
        self.verse_order_list_generated = []
        self.verse_order_list = []
        self.verses = []
        self.verse_counts = {}
        self.copyright_string = unicode(translate(
            'SongsPlugin.SongImport', 'copyright'))

    def log_error(self, filepath, reason=SongStrings.SongIncomplete):
        """
        This should be called, when a song could not be imported.

        ``filepath``
            This should be the file path if ``self.import_source`` is a list
            with different files. If it is not a list, but a  single file (for
            instance a database), then this should be the song's title.

        ``reason``
            The reason, why the import failed. The string should be as
            informative as possible.
        """
        self.error_log.append((filepath, unicode(reason)))

    def write_error_report(self):
        """
        Creates a error import containing all error messages.
        """
        report_path = os.path.join(AppLocation.get_data_path(), unicode(translate(
            'SongsPlugin.SongImport','song_import_report (%s).txt')) %
            datetime.datetime.now().strftime(u'%Y-%m-%dT%H:%M:%S'))
        report_file = codecs.open(report_path, u'w', u'utf-8')
        report_file.write(translate('SongsPlugin.SongImport',
            'The following songs could not be imported:\n'))
        for filepath, reason in self.error_log:
            report_file.write(u'- %s (%s)\n' % (filepath, reason))
        report_file.close()
        return report_path

    def stop_import(self):
        """
        Sets the flag for importers to stop their import
        """
        log.debug(u'Stopping songs import')
        self.stop_import_flag = True

    def register(self, import_wizard):
        self.import_wizard = import_wizard

    def tidy_text(self, text):
        """
        Get rid of some dodgy unicode and formatting characters we're not
        interested in. Some can be converted to ascii.
        """
        text = text.replace(u'\u2018', u'\'')
        text = text.replace(u'\u2019', u'\'')
        text = text.replace(u'\u201c', u'"')
        text = text.replace(u'\u201d', u'"')
        text = text.replace(u'\u2026', u'...')
        text = text.replace(u'\u2013', u'-')
        text = text.replace(u'\u2014', u'-')
        # Remove surplus blank lines, spaces, trailing/leading spaces
        text = re.sub(r'[ \t\v]+', u' ', text)
        text = re.sub(r' ?(\r\n?|\n) ?', u'\n', text)
        text = re.sub(r' ?(\n{5}|\f)+ ?', u'\f', text)
        return text

    def process_song_text(self, text):
        verse_texts = text.split(u'\n\n')
        for verse_text in verse_texts:
            if verse_text.strip() != u'':
                self.process_verse_text(verse_text.strip())

    def process_verse_text(self, text):
        lines = text.split(u'\n')
        if text.lower().find(self.copyright_string) >= 0 \
            or text.find(unicode(SongStrings.CopyrightSymbol)) >= 0:
            copyright_found = False
            for line in lines:
                if (copyright_found or
                    line.lower().find(self.copyright_string) >= 0 or
                    line.find(unicode(SongStrings.CopyrightSymbol)) >= 0):
                    copyright_found = True
                    self.add_copyright(line)
                else:
                    self.parse_author(line)
            return
        if len(lines) == 1:
            self.parse_author(lines[0])
            return
        if not self.title:
            self.title = lines[0]
        self.add_verse(text)

    def add_copyright(self, copyright):
        """
        Build the copyright field
        """
        if self.copyright.find(copyright) >= 0:
            return
        if self.copyright != u'':
            self.copyright += ' '
        self.copyright += copyright

    def parse_author(self, text):
        """
        Add the author. OpenLP stores them individually so split by 'and', '&'
        and comma. However need to check for 'Mr and Mrs Smith' and turn it to
        'Mr Smith' and 'Mrs Smith'.
        """
        for author in text.split(u','):
            authors = author.split(u'&')
            for i in range(len(authors)):
                author2 = authors[i].strip()
                if author2.find(u' ') == -1 and i < len(authors) - 1:
                    author2 = author2 + u' ' \
                        + authors[i + 1].strip().split(u' ')[-1]
                if author2.endswith(u'.'):
                    author2 = author2[:-1]
                if author2:
                    self.add_author(author2)

    def add_author(self, author):
        """
        Add an author to the list
        """
        if author in self.authors:
            return
        self.authors.append(author)

    def add_media_file(self, filename):
        """
        Add a media file to the list
        """
        if filename in self.media_files:
            return
        self.media_files.append(filename)

    def add_verse(self, verse_text, verse_def=u'v', lang=None):
        """
        Add a verse. This is the whole verse, lines split by \\n. It will also
        attempt to detect duplicates. In this case it will just add to the verse
        order.

        ``verse_text``
            The text of the verse.

        ``verse_def``
            The verse tag can be v1/c1/b etc, or 'v' and 'c' (will count the
            verses/choruses itself) or None, where it will assume verse.

        ``lang``
            The language code (ISO-639) of the verse, for example *en* or *de*.

        """
        for (old_verse_def, old_verse, old_lang) in self.verses:
            if old_verse.strip() == verse_text.strip():
                self.verse_order_list_generated.append(old_verse_def)
                self.verse_order_list_generated_useful = True
                return
        if verse_def[0] in self.verse_counts:
            self.verse_counts[verse_def[0]] += 1
        else:
            self.verse_counts[verse_def[0]] = 1
        if len(verse_def) == 1:
            verse_def += unicode(self.verse_counts[verse_def[0]])
        elif int(verse_def[1:]) > self.verse_counts[verse_def[0]]:
            self.verse_counts[verse_def[0]] = int(verse_def[1:])
        self.verses.append([verse_def, verse_text.rstrip(), lang])
        self.verse_order_list_generated.append(verse_def)

    def repeat_verse(self):
        """
        Repeat the previous verse in the verse order
        """
        self.verse_order_list_generated.append(
            self.verse_order_list_generated[-1])
        self.verse_order_list_generated_useful = True

    def check_complete(self):
        """
        Check the mandatory fields are entered (i.e. title and a verse)
        Author not checked here, if no author then "Author unknown" is
        automatically added
        """
        if not self.title or not len(self.verses):
            return False
        else:
            return True

    def finish(self):
        """
        All fields have been set to this song. Write the song to disk.
        """
        if not self.check_complete():
            self.set_defaults()
            return False
        log.info(u'committing song %s to database', self.title)
        song = Song()
        song.title = self.title
        self.import_wizard.incrementProgressBar(
            WizardStrings.ImportingType % song.title)
        song.alternate_title = self.alternate_title
        # Values will be set when cleaning the song.
        song.search_title = u''
        song.search_lyrics = u''
        song.verse_order = u''
        song.song_number = self.song_number
        verses_changed_to_other = {}
        sxml = SongXML()
        other_count = 1
        for (verse_def, verse_text, lang) in self.verses:
            if verse_def[0].lower() in VerseType.Tags:
                verse_tag = verse_def[0].lower()
            else:
                new_verse_def = u'%s%d' % (VerseType.Tags[VerseType.Other],
                    other_count)
                verses_changed_to_other[verse_def] = new_verse_def
                other_count += 1
                verse_tag = VerseType.Tags[VerseType.Other]
                log.info(u'Versetype %s changing to %s' , verse_def,
                    new_verse_def)
                verse_def = new_verse_def
            sxml.add_verse_to_lyrics(verse_tag, verse_def[1:], verse_text, lang)
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        if not len(self.verse_order_list) and \
            self.verse_order_list_generated_useful:
            self.verse_order_list = self.verse_order_list_generated
        for i, current_verse_def in enumerate(self.verse_order_list):
            if verses_changed_to_other.has_key(current_verse_def):
                self.verse_order_list[i] = \
                    verses_changed_to_other[current_verse_def]
        song.verse_order = u' '.join(self.verse_order_list)
        song.copyright = self.copyright
        song.comments = self.comments
        song.theme_name = self.theme_name
        song.ccli_number = self.ccli_number
        for authortext in self.authors:
            author = self.manager.get_object_filtered(Author,
                Author.display_name == authortext)
            if not author:
                author = Author.populate(display_name=authortext,
                    last_name=authortext.split(u' ')[-1],
                    first_name=u' '.join(authortext.split(u' ')[:-1]))
            song.authors.append(author)
        for filename in self.media_files:
            media_file = self.manager.get_object_filtered(MediaFile,
                MediaFile.file_name == filename)
            if not media_file:
                song.media_files.append(MediaFile.populate(file_name=filename))
        if self.song_book_name:
            song_book = self.manager.get_object_filtered(Book,
                Book.name == self.song_book_name)
            if song_book is None:
                song_book = Book.populate(name=self.song_book_name,
                    publisher=self.song_book_pub)
            song.book = song_book
        for topictext in self.topics:
            if not topictext:
                continue
            topic = self.manager.get_object_filtered(Topic,
                Topic.name == topictext)
            if topic is None:
                topic = Topic.populate(name=topictext)
            song.topics.append(topic)
        clean_song(self.manager, song)
        self.manager.save_object(song)
        self.set_defaults()
        return True

    def print_song(self):
        """
        For debugging
        """
        print u'========================================' \
            + u'========================================'
        print u'TITLE: ' + self.title
        print u'ALT TITLE: ' + self.alternate_title
        for (verse_def, verse_text, lang) in self.verses:
            print u'VERSE ' + verse_def + u': ' + verse_text
        print u'ORDER: ' + u' '.join(self.verse_order_list)
        print u'GENERATED ORDER: ' + u' '.join(self.verse_order_list_generated)
        for author in self.authors:
            print u'AUTHOR: ' + author
        if self.copyright:
            print u'COPYRIGHT: ' + self.copyright
        if self.song_book_name:
            print u'BOOK: ' + self.song_book_name
        if self.song_book_pub:
            print u'BOOK PUBLISHER: ' + self.song_book_pub
        if self.song_number:
            print u'NUMBER: ' + self.song_number
        for topictext in self.topics:
            print u'TOPIC: ' + topictext
        if self.comments:
            print u'COMMENTS: ' + self.comments
        if self.theme_name:
            print u'THEME: ' + self.theme_name
        if self.ccli_number:
            print u'CCLI: ' + self.ccli_number
