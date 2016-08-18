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

from openlp.core.common import translate, trace_error_handler
from openlp.core.lib.exceptions import ValidationError
from openlp.core.lib.ui import critical_error_message_box
from openlp.plugins.bibles.lib.bibleimport import BibleImport


log = logging.getLogger(__name__)


class OpenSongBible(BibleImport):
    """
    OpenSong Bible format importer class. This class is used to import Bibles from OpenSong's XML format.
    """
    def get_text(self, element):
        """
        Recursively get all text in an objectify element and its child elements.

        :param element: An objectify element to get the text from
        """
        verse_text = ''
        if element.text:
            verse_text = element.text
        for sub_element in element.iterchildren():
            verse_text += self.get_text(sub_element)
        if element.tail:
            verse_text += element.tail
        return verse_text

    @staticmethod
    def process_chapter_no(number, previous_number):
        """
        Process the chapter number

        :param number: The raw data from the xml
        :param previous_number: The previous chapter number
        :return: Number of current chapter. (Int)
        """
        if number:
            return int(number.split()[-1])
        return previous_number + 1

    @staticmethod
    def process_verse_no(number, previous_number):
        """
        Process the verse number retrieved from the xml

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

    @staticmethod
    def validate_file(filename):
        """
        Validate the supplied file

        :param filename: The supplied file
        :return: True if valid. ValidationError is raised otherwise.
        """
        if BibleImport.is_compressed():
            raise ValidationError(msg='Compressed file')
        bible = BibleImport.parse_xml(filename, use_objectify=True)
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
        Loads a Bible from file.
        """
        self.validate_file(self.filename)
        log.debug('Starting OpenSong import from "{name}"'.format(name=self.filename))
        try:
            bible = self.parse_xml(self.filename, use_objectify=True)
            # Check that we're not trying to import a Zefania XML bible, it is sometimes refered to as 'OpenSong'
            if bible.tag.upper() == 'XMLBIBLE':
                critical_error_message_box(
                    message=translate('BiblesPlugin.OpenSongImport',
                                      'Incorrect Bible file type supplied. This looks like a Zefania XML bible, '
                                      'please use the Zefania import option.'))
                return False
            # No language info in the opensong format, so ask the user
            language_id = self.get_language_id(bible_name=self.filename)
            if not language_id:
                return False
            for book in bible.b:
                if self.stop_import_flag:
                    break
                db_book = self.find_and_create_book(str(book.attrib['n']), len(bible.b), language_id)
                chapter_number = 0
                for chapter in book.c:
                    if self.stop_import_flag:
                        break
                    chapter_number = self.process_chapter_no(chapter.attrib['n'], chapter_number)
                    verse_number = 0
                    for verse in chapter.v:
                        if self.stop_import_flag:
                            break
                        verse_number = self.process_verse_no(verse.attrib['n'], verse_number)
                        self.create_verse(db_book.id, chapter_number, verse_number, self.get_text(verse))
                    self.wizard.increment_progress_bar(translate('BiblesPlugin.Opensong',
                                                                 'Importing {name} {chapter}...'
                                                                 ).format(name=db_book.name, chapter=chapter_number))
                self.session.commit()
            self.application.process_events()
        except (AttributeError, ValidationError, etree.XMLSyntaxError):
            log.exception('Loading Bible from OpenSong file failed')
            trace_error_handler(log)
            return False
        if self.stop_import_flag:
            return False
