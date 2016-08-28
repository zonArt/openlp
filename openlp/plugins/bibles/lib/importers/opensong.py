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

import logging
from lxml import etree

from openlp.core.common import trace_error_handler, translate
from openlp.core.lib.exceptions import ValidationError
from openlp.core.lib.ui import critical_error_message_box
from openlp.plugins.bibles.lib.bibleimport import BibleImport


log = logging.getLogger(__name__)


def get_text(element):
    """
    Recursively get all text in an objectify element and its child elements.

    :param element: An objectify element to get the text from
    :return: The text content of the element (str)
    """
    verse_text = ''
    if element.text:
        verse_text = element.text
    for sub_element in element.iterchildren():
        verse_text += get_text(sub_element)
    if element.tail:
        verse_text += element.tail
    return verse_text


def parse_chapter_number(number, previous_number):
    """
    Parse the chapter number

    :param number: The raw data from the xml
    :param previous_number: The previous chapter number
    :return: Number of current chapter. (Int)
    """
    if number:
        return int(number.split()[-1])
    return previous_number + 1


def parse_verse_number(number, previous_number):
    """
    Parse the verse number retrieved from the xml

    :param number: The raw data from the xml
    :param previous_number: The previous verse number
    :return: Number of current verse. (Int)
    """
    if not number:
        return previous_number + 1
    try:
        return int(number)
    except ValueError:
        verse_parts = number.split('-')
        if len(verse_parts) > 1:
            number = int(verse_parts[0])
            return number
    except TypeError:
        log.warning('Illegal verse number: {verse_no}'.format(verse_no=str(number)))
    return previous_number + 1


class OpenSongBible(BibleImport):
    """
    OpenSong Bible format importer class. This class is used to import Bibles from OpenSong's XML format.
    """
    def process_books(self, books):
        """
        Extract and create the books from the objectified xml

        :param books: Objectified xml
        :return: None
        """
        for book in books:
            if self.stop_import_flag:
                break
            db_book = self.find_and_create_book(str(book.attrib['n']), len(books), self.language_id)
            self.process_chapters(db_book, book.c)
            self.session.commit()

    def process_chapters(self, book, chapters):
        """
        Extract and create the chapters from the objectified xml for the book `book`

        :param book: A database Book object to add the chapters to
        :param chapters: Objectified xml containing chapters
        :return: None
        """
        chapter_number = 0
        for chapter in chapters:
            if self.stop_import_flag:
                break
            chapter_number = parse_chapter_number(chapter.attrib['n'], chapter_number)
            self.process_verses(book, chapter_number, chapter.v)
            self.wizard.increment_progress_bar(translate('BiblesPlugin.Opensong',
                                                         'Importing {name} {chapter}...'
                                                         ).format(name=book.name, chapter=chapter_number))

    def process_verses(self, book, chapter_number, verses):
        """
        Extract and create the verses from the objectified xml

        :param book: A database Book object
        :param chapter_number: The chapter number to add the verses to (int)
        :param verses: Objectified xml containing verses
        :return: None
        """
        verse_number = 0
        for verse in verses:
            if self.stop_import_flag:
                break
            verse_number = parse_verse_number(verse.attrib['n'], verse_number)
            self.create_verse(book.id, chapter_number, verse_number, get_text(verse))

    def validate_file(self, filename):
        """
        Validate the supplied file

        :param filename: The supplied file
        :return: True if valid. ValidationError is raised otherwise.
        """
        if BibleImport.is_compressed(filename):
            raise ValidationError(msg='Compressed file')
        bible = self.parse_xml(filename, use_objectify=True)
        if bible is None:
            raise ValidationError(msg='Error when opening file')
        root_tag = bible.tag.lower()
        if root_tag != 'bible':
            if root_tag == 'xmlbible':
                # Zefania bibles have a root tag of XMLBIBLE". Sometimes these bibles are referred to as 'OpenSong'
                critical_error_message_box(
                    message=translate('BiblesPlugin.OpenSongImport',
                                      'Incorrect Bible file type supplied. This looks like a Zefania XML bible, '
                                      'please use the Zefania import option.'))
            raise ValidationError(msg='Invalid xml.')
        return True

    def do_import(self, bible_name=None):
        """
        Loads an Open Song Bible from a file.

        :param bible_name: The name of the bible being imported
        :return: True if import completed, False if import was unsuccessful
        """
        log.debug('Starting OpenSong import from "{name}"'.format(name=self.filename))
        self.validate_file(self.filename)
        bible = self.parse_xml(self.filename, use_objectify=True)
        if bible is None:
            return False
        # No language info in the opensong format, so ask the user
        self.language_id = self.get_language_id(bible_name=self.filename)
        if not self.language_id:
            return False
        self.process_books(bible.b)
        return not self.stop_import_flag
