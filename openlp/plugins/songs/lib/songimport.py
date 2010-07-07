# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

import re

from openlp.core.lib import translate
from openlp.plugins.songs.lib import SongXMLBuilder, VerseType
from openlp.plugins.songs.lib.db import Song, Author, Topic, Book

class SongImport(object):
    """
    Helper class for import a song from a third party source into OpenLP

    This class just takes the raw strings, and will work out for itself
    whether the authors etc already exist and add them or refer to them
    as necessary
    """

    def __init__(self, song_manager):
        """
        Initialise and create defaults for properties

        song_manager is an instance of a SongManager, through which all
        database access is performed
        """
        self.manager = song_manager
        self.title = u''
        self.song_number = u''
        self.alternate_title = u''
        self.copyright = u''
        self.comment = u''
        self.theme = u''
        self.song_cclino = u''
        self.authors = []
        self.topics = []
        self.song_book_name = u''
        self.song_book_pub = u''
        self.verse_order_list = []
        self.verses = []
        self.versecount = 0
        self.choruscount = 0
        self.copyright_string = unicode(translate(
            'SongsPlugin.SongImport', 'copyright'))
        self.copyright_symbol = unicode(translate(
            'SongsPlugin.SongImport', '\xa9'))

    @staticmethod
    def process_songs_text(manager, text):
        songs = []
        songtexts = SongImport.tidy_text(text).split(u'\f')
        song = SongImport(manager)
        for songtext in songtexts:
            if songtext.strip():
                song.process_song_text(songtext.strip())
                if song.check_complete():
                    songs.append(song)
                    song = SongImport(manager)
        if song.check_complete():
            songs.append(song)
        return songs

    @staticmethod
    def tidy_text(text):
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
        versetexts = text.split(u'\n\n')
        for versetext in versetexts:
            if versetext.strip() != u'':
                self.process_verse_text(versetext.strip())

    def process_verse_text(self, text):
        lines = text.split(u'\n')
        if text.lower().find(self.copyright_string) >= 0 \
            or text.lower().find(self.copyright_symbol) >= 0:
            copyright_found = False
            for line in lines:
                if (copyright_found or
                    line.lower().find(self.copyright_string) >= 0 or
                    line.lower().find(self.copyright_symbol) >= 0):
                    copyright_found = True
                    self.add_copyright(line)
                else:
                    self.parse_author(line)
            return
        if len(lines) == 1:
            self.parse_author(lines[0])
            return
        if not self.get_title():
            self.set_title(lines[0])
        self.add_verse(text)

    def get_title(self):
        """
        Return the title
        """
        return self.title

    def get_copyright(self):
        """
        Return the copyright
        """
        return self.copyright

    def get_song_number(self):
        """
        Return the song number
        """
        return self.song_number

    def set_title(self, title):
        """
        Set the title
        """
        self.title = title

    def set_alternate_title(self, title):
        """
        Set the alternate title
        """
        self.alternate_title = title

    def set_song_number(self, song_number):
        """
        Set the song number
        """
        self.song_number = song_number

    def set_ccli_number(self, ccli_number):
        """
        Set the ccli number
        """
        self.ccli_number = ccli_number

    def set_song_book(self, song_book, publisher):
        """
        Set the song book name and publisher
        """
        self.song_book_name = song_book
        self.song_book_pub = publisher

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
        and comma.
        However need to check for "Mr and Mrs Smith" and turn it to
        "Mr Smith" and "Mrs Smith".
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

    def add_verse(self, verse, versetag=None):
        """
        Add a verse. This is the whole verse, lines split by \n
        Verse tag can be V1/C1/B etc, or 'V' and 'C' (will count the verses/
        choruses itself) or None, where it will assume verse
        It will also attempt to detect duplicates. In this case it will just
        add to the verse order
        """
        for (oldversetag, oldverse) in self.verses:
            if oldverse.strip() == verse.strip():
                self.verse_order_list.append(oldversetag)
                return
        if versetag == u'V' or not versetag:
            self.versecount += 1
            versetag = u'V' + unicode(self.versecount)
        if versetag.startswith(u'C'):
            self.choruscount += 1
        if versetag == u'C':
            versetag += unicode(self.choruscount)
        self.verses.append([versetag, verse.rstrip()])
        self.verse_order_list.append(versetag)
        if versetag.startswith(u'V') and self.contains_verse(u'C1'):
            self.verse_order_list.append(u'C1')

    def repeat_verse(self):
        """
        Repeat the previous verse in the verse order
        """
        self.verse_order_list.append(self.verse_order_list[-1])

    def contains_verse(self, versetag):
        return versetag in self.verse_order_list

    def check_complete(self):
        """
        Check the mandatory fields are entered (i.e. title and a verse)
        Author not checked here, if no author then "Author unknown" is
        automatically added
        """
        if self.title == u'' or len(self.verses) == 0:
            return False
        else:
            return True

    def remove_punctuation(self, text):
        """
        Extracts alphanumeric words for searchable fields
        """
        return re.sub(r'\W+', u' ', text)

    def finish(self):
        """
        All fields have been set to this song. Write it away
        """
        if len(self.authors) == 0:
            self.authors.append(u'Author unknown')
        self.commit_song()

    def commit_song(self):
        """
        Write the song and it's fields to disk
        """
        song = Song()
        song.title = self.title
        song.search_title = self.remove_punctuation(self.title) \
            + '@' + self.alternate_title
        song.song_number = self.song_number
        song.search_lyrics = u''
        sxml = SongXMLBuilder()
        for (versetag, versetext) in self.verses:
            if versetag[0] == u'C':
                versetype = VerseType.to_string(VerseType.Chorus)
            elif versetag[0] == u'V':
                versetype = VerseType.to_string(VerseType.Verse)
            elif versetag[0] == u'B':
                versetype = VerseType.to_string(VerseType.Bridge)
            elif versetag[0] == u'I':
                versetype = VerseType.to_string(VerseType.Intro)
            elif versetag[0] == u'P':
                versetype = VerseType.to_string(VerseType.PreChorus)
            elif versetag[0] == u'E':
                versetype = VerseType.to_string(VerseType.Ending)
            else:
                versetype = VerseType.to_string(VerseType.Other)
            sxml.add_verse_to_lyrics(versetype, versetag[1:], versetext)
            song.search_lyrics += u' ' + self.remove_punctuation(versetext)
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        song.verse_order = u' '.join(self.verse_order_list)
        song.copyright = self.copyright
        song.comment = self.comment
        song.theme = self.theme
        song.song_cclino = self.song_cclino
        for authortext in self.authors:
            author = self.manager.get_object_filtered(Author,
                Author.display_name == authortext)
            if author is None:
                author = Author()
                author.display_name = authortext
                author.last_name = authortext.split(u' ')[-1]
                author.first_name = u' '.join(authortext.split(u' ')[:-1])
                self.manager.save_object(author)
            song.authors.append(author)
        if self.song_book_name:
            song_book = self.manager.get_object_filtered(Book,
                Book.name == self.song_book_name)
            if song_book is None:
                song_book = Book()
                song_book.name = self.song_book_name
                song_book.publisher = self.song_book_pub
                self.manager.save_object(song_book)
            song.song_book_id = song_book.id
        for topictext in self.topics:
            topic = self.manager.get_object_filtered(Topic.name == topictext)
            if topic is None:
                topic = Topic()
                topic.name = topictext
                self.manager.save_object(topic)
            song.topics.append(topictext)
        self.manager.save_object(song)

    def print_song(self):
        """
        For debugging
        """
        print u'========================================'   \
            + u'========================================'
        print u'TITLE: ' + self.title
        print u'ALT TITLE: ' + self.alternate_title
        for (versetag, versetext) in self.verses:
            print u'VERSE ' + versetag + u': ' + versetext
        print u'ORDER: ' + u' '.join(self.verse_order_list)
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
        if self.comment:
            print u'COMMENT: ' + self.comment
        if self.theme:
            print u'THEME: ' + self.theme
        if self.song_cclino:
            print u'CCLI: ' + self.song_cclino
