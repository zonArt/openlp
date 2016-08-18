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
This module contains tests for the OpenSong Bible importer.
"""

import os
import json
from unittest import TestCase


from lxml import objectify

from tests.functional import MagicMock, patch
from openlp.core.lib.exceptions import ValidationError
from openlp.plugins.bibles.lib.importers.opensong import OpenSongBible
from openlp.plugins.bibles.lib.bibleimport import BibleImport

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'resources', 'bibles'))


class TestOpenSongImport(TestCase):
    """
    Test the functions in the :mod:`opensongimport` module.
    """

    def setUp(self):
        self.manager_patcher = patch('openlp.plugins.bibles.lib.db.Manager')
        self.addCleanup(self.manager_patcher.stop)
        self.manager_patcher.start()
        self.registry_patcher = patch('openlp.plugins.bibles.lib.db.Registry')
        self.addCleanup(self.registry_patcher.stop)
        self.registry_patcher.start()

    def test_create_importer(self):
        """
        Test creating an instance of the OpenSong file importer
        """
        # GIVEN: A mocked out "manager"
        mocked_manager = MagicMock()

        # WHEN: An importer object is created
        importer = OpenSongBible(mocked_manager, path='.', name='.', filename='')

        # THEN: The importer should be an instance of BibleDB
        self.assertIsInstance(importer, BibleImport)

    def process_chapter_no_test(self):
        """
        Test process_chapter_no when supplied with chapter number and an instance of OpenSongBible
        """
        # GIVEN: The number 10 represented as a string
        # WHEN: Calling process_chapter_no
        result = OpenSongBible.process_chapter_no('10', 0)

        # THEN: The 10 should be returned as an Int
        self.assertEqual(result, 10)

    def process_chapter_no_empty_attribute_test(self):
        """
        Test process_chapter_no when the chapter number is an empty string. (Bug #1074727)
        """
        # GIVEN: An empty string, and the previous chapter number set as 12  and an instance of OpenSongBible
        # WHEN: Calling process_chapter_no
        result = OpenSongBible.process_chapter_no('', 12)

        # THEN: process_chapter_no should increment the previous verse number
        self.assertEqual(result, 13)

    def process_verse_no_valid_verse_no_test(self):
        """
        Test process_verse_no when supplied with a valid verse number
        """
        # GIVEN: The number 15 represented as a string and an instance of OpenSongBible
        # WHEN: Calling process_verse_no
        result = OpenSongBible.process_verse_no('15', 0)

        # THEN: process_verse_no should return the verse number
        self.assertEqual(result, 15)

    def process_verse_no_verse_range_test(self):
        """
        Test process_verse_no when supplied with a verse range
        """
        # GIVEN: The range 24-26 represented as a string
        # WHEN: Calling process_verse_no
        result = OpenSongBible.process_verse_no('24-26', 0)

        # THEN: process_verse_no should return the first verse number in the range
        self.assertEqual(result, 24)

    def process_verse_no_invalid_verse_no_test(self):
        """
        Test process_verse_no when supplied with a invalid verse number
        """
        # GIVEN: An non numeric string represented as a string
        # WHEN: Calling process_verse_no
        result = OpenSongBible.process_verse_no('invalid', 41)

        # THEN: process_verse_no should increment the previous verse number
        self.assertEqual(result, 42)

    def process_verse_no_empty_attribute_test(self):
        """
        Test process_verse_no when the verse number is an empty string. (Bug #1074727)
        """
        # GIVEN: An empty string, and the previous verse number set as 14
        # WHEN: Calling process_verse_no
        result = OpenSongBible.process_verse_no('', 14)

        # THEN: process_verse_no should increment the previous verse number
        self.assertEqual(result, 15)

    @patch('openlp.plugins.bibles.lib.importers.opensong.log')
    def process_verse_no_invalid_type_test(self, mocked_log):
        """
        Test process_verse_no when the verse number is an invalid type)
        """
        # GIVEN: A mocked out log, a Tuple, and the previous verse number set as 12
        # WHEN: Calling process_verse_no
        result = OpenSongBible.process_verse_no((1,2,3), 12)

        # THEN: process_verse_no should log the verse number it was called with increment the previous verse number
        mocked_log.warning.assert_called_once_with('Illegal verse number: (1, 2, 3)')
        self.assertEqual(result, 13)

    @patch('openlp.plugins.bibles.lib.importers.opensong.BibleImport')
    def validate_xml_bible_test(self, mocked_bible_import):
        """
        Test that validate_xml returns True with valid XML
        """
        # GIVEN: Some test data with an OpenSong Bible "bible" root tag
        mocked_bible_import.parse_xml.return_value = objectify.fromstring('<bible></bible>')

        # WHEN: Calling validate_xml
        result = OpenSongBible.validate_file('file.name')

        # THEN: A True should be returned
        self.assertTrue(result)

    @patch('openlp.plugins.bibles.lib.importers.opensong.critical_error_message_box')
    @patch('openlp.plugins.bibles.lib.importers.opensong.BibleImport')
    def validate_xml_zefania_root_test(self, mocked_bible_import, mocked_message_box):
        """
        Test that validate_xml raises a ValidationError with a Zefinia root tag
        """
        # GIVEN: Some test data with a Zefinia "XMLBIBLE" root tag
        mocked_bible_import.parse_xml.return_value = objectify.fromstring('<XMLBIBLE></XMLBIBLE>')

        # WHEN: Calling validate_xml
        # THEN: critical_error_message_box should be called and an ValidationError should be raised
        with self.assertRaises(ValidationError) as context:
            OpenSongBible.validate_file('file.name')
            self.assertEqual(context.exception.msg, 'Invalid xml.')
        mocked_message_box.assert_called_once_with(
            message='Incorrect Bible file type supplied. This looks like a Zefania XML bible, please use the '
                    'Zefania import option.')

    @patch('openlp.plugins.bibles.lib.importers.opensong.critical_error_message_box')
    @patch('openlp.plugins.bibles.lib.importers.opensong.BibleImport')
    def validate_xml_invalid_root_test(self, mocked_bible_import, mocked_message_box):
        """
        Test that validate_xml raises a ValidationError with an invalid root tag
        """
        # GIVEN: Some test data with an invalid root tag and an instance of OpenSongBible
        mocked_bible_import.parse_xml.return_value = objectify.fromstring('<song></song>')

        # WHEN: Calling validate_xml
        # THEN: ValidationError should be raised, and the critical error message box should not have been called
        with self.assertRaises(ValidationError) as context:
            OpenSongBible.validate_file('file.name')
            self.assertEqual(context.exception.msg, 'Invalid xml.')
        self.assertFalse(mocked_message_box.called)

    def test_file_import(self):
        """
        Test the actual import of OpenSong Bible file
        """
        # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
        #       get_book_ref_id_by_name, create_verse, create_book, session and get_language.
        result_file = open(os.path.join(TEST_PATH, 'dk1933.json'), 'rb')
        test_data = json.loads(result_file.read().decode())
        bible_file = 'opensong-dk1933.xml'
        with patch('openlp.plugins.bibles.lib.importers.opensong.OpenSongBible.application'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = OpenSongBible(mocked_manager, path='.', name='.', filename='')
            importer.wizard = mocked_import_wizard
            importer.get_book_ref_id_by_name = MagicMock()
            importer.create_verse = MagicMock()
            importer.create_book = MagicMock()
            importer.session = MagicMock()
            importer.get_language = MagicMock()
            importer.get_language.return_value = 'Danish'

            # WHEN: Importing bible file
            importer.filename = os.path.join(TEST_PATH, bible_file)
            importer.do_import()

            # THEN: The create_verse() method should have been called with each verse in the file.
            self.assertTrue(importer.create_verse.called)
            for verse_tag, verse_text in test_data['verses']:
                importer.create_verse.assert_any_call(importer.create_book().id, 1, int(verse_tag), verse_text)
