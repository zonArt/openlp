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
This module contains tests for the OSIS Bible importer.
"""

import os
import json
from unittest import TestCase

from tests.functional import MagicMock, patch
from openlp.plugins.bibles.lib.importers.osis import OSISBible
from openlp.plugins.bibles.lib.db import BibleDB

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'resources', 'bibles'))


class TestOsisImport(TestCase):
    """
    Test the functions in the :mod:`osisimport` module.
    """

    def setUp(self):
        self.registry_patcher = patch('openlp.plugins.bibles.lib.db.Registry')
        self.addCleanup(self.registry_patcher.stop)
        self.registry_patcher.start()
        self.manager_patcher = patch('openlp.plugins.bibles.lib.db.Manager')
        self.addCleanup(self.manager_patcher.stop)
        self.manager_patcher.start()

        def test_create_importer(self):
            """
            Test creating an instance of the OSIS file importer
            """
            # GIVEN: A mocked out "manager"
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = OSISBible(mocked_manager, path='.', name='.', filename='')

            # THEN: The importer should be an instance of BibleDB
            self.assertIsInstance(importer, BibleDB)

    def do_import_parse_xml_fails_test(self):
        """
        Test do_import when parse_xml fails (returns None)
        """
        # GIVEN: An instance of OpenSongBible and a mocked parse_xml which returns False
        with patch('openlp.plugins.bibles.lib.importers.opensong.log'), \
                patch.object(OSISBible, 'validate_file'), \
                patch.object(OSISBible, 'parse_xml', return_value=None), \
                patch.object(OSISBible, 'get_language_id') as mocked_language_id:
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling do_import
            result = importer.do_import()

            # THEN: do_import should return False and get_language_id should have not been called
            self.assertFalse(result)
            self.assertFalse(mocked_language_id.called)

    def do_import_no_language_test(self):
        """
        Test do_import when the user cancels the language selection dialog
        """
        # GIVEN: An instance of OpenSongBible and a mocked get_language which returns False
        with patch('openlp.plugins.bibles.lib.importers.opensong.log'), \
                patch.object(OSISBible, 'validate_file'), \
                patch.object(OSISBible, 'parse_xml'), \
                patch.object(OSISBible, 'get_language_id', **{'return_value': False}), \
                patch.object(OSISBible, 'process_books') as mocked_process_books:
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling do_import
            result = importer.do_import()

            # THEN: do_import should return False and process_books should have not been called
            self.assertFalse(result)
            self.assertFalse(mocked_process_books.called)

    def do_import_stop_import_test(self):
        """
        Test do_import when the stop_import_flag is set to True
        """
        # GIVEN: An instance of OpenSongBible and stop_import_flag set to True
        with patch('openlp.plugins.bibles.lib.importers.opensong.log'), \
                patch.object(OSISBible, 'validate_file'), \
                patch.object(OSISBible, 'parse_xml'), \
                patch.object(OSISBible, 'get_language_id', **{'return_value': 10}), \
                patch.object(OSISBible, 'process_books'):
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')
            importer.stop_import_flag = True

            # WHEN: Calling do_import
            result = importer.do_import()

            # THEN: do_import should return False and process_books should have not been called
            self.assertFalse(result)
            self.assertTrue(importer.process_books.called)

    @patch('openlp.plugins.bibles.lib.importers.opensong.log')
    def do_import_completes_test(self, mocked_log):
        """
        Test do_import when it completes successfully
        """
        # GIVEN: An instance of OpenSongBible and stop_import_flag set to True
        with patch('openlp.plugins.bibles.lib.importers.opensong.log'), \
                patch.object(OSISBible, 'validate_file'), \
                patch.object(OSISBible, 'parse_xml'), \
                patch.object(OSISBible, 'get_language_id', **{'return_value': 10}), \
                patch.object(OSISBible, 'process_books'):
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')
            importer.stop_import_flag = False

            # WHEN: Calling do_import
            result = importer.do_import()

            # THEN: do_import should return True
            self.assertTrue(result)

        def test_file_import_nested_tags(self):
            """
            Test the actual import of OSIS Bible file, with nested chapter and verse tags
            """
            # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
            #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
            result_file = open(os.path.join(TEST_PATH, 'dk1933.json'), 'rb')
            test_data = json.loads(result_file.read().decode())
            bible_file = 'osis-dk1933.xml'
            with patch('openlp.plugins.bibles.lib.importers.osis.OSISBible.application'):
                mocked_manager = MagicMock()
                mocked_import_wizard = MagicMock()
                importer = OSISBible(mocked_manager, path='.', name='.', filename='')
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
                    importer.create_verse.assert_any_call(importer.create_book().id, '1', verse_tag, verse_text)

        def test_file_import_mixed_tags(self):
            """
            Test the actual import of OSIS Bible file, with chapter tags containing milestone verse tags.
            """
            # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
            #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
            result_file = open(os.path.join(TEST_PATH, 'kjv.json'), 'rb')
            test_data = json.loads(result_file.read().decode())
            bible_file = 'osis-kjv.xml'
            with patch('openlp.plugins.bibles.lib.importers.osis.OSISBible.application'):
                mocked_manager = MagicMock()
                mocked_import_wizard = MagicMock()
                importer = OSISBible(mocked_manager, path='.', name='.', filename='')
                importer.wizard = mocked_import_wizard
                importer.get_book_ref_id_by_name = MagicMock()
                importer.create_verse = MagicMock()
                importer.create_book = MagicMock()
                importer.session = MagicMock()
                importer.get_language = MagicMock()
                importer.get_language.return_value = 'English'

                # WHEN: Importing bible file
                importer.filename = os.path.join(TEST_PATH, bible_file)
                importer.do_import()

                # THEN: The create_verse() method should have been called with each verse in the file.
                self.assertTrue(importer.create_verse.called)
                for verse_tag, verse_text in test_data['verses']:
                    importer.create_verse.assert_any_call(importer.create_book().id, '1', verse_tag, verse_text)

        def test_file_import_milestone_tags(self):
            """
            Test the actual import of OSIS Bible file, with milestone chapter and verse tags.
            """
            # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
            #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
            result_file = open(os.path.join(TEST_PATH, 'web.json'), 'rb')
            test_data = json.loads(result_file.read().decode())
            bible_file = 'osis-web.xml'
            with patch('openlp.plugins.bibles.lib.importers.osis.OSISBible.application'):
                mocked_manager = MagicMock()
                mocked_import_wizard = MagicMock()
                importer = OSISBible(mocked_manager, path='.', name='.', filename='')
                importer.wizard = mocked_import_wizard
                importer.get_book_ref_id_by_name = MagicMock()
                importer.create_verse = MagicMock()
                importer.create_book = MagicMock()
                importer.session = MagicMock()
                importer.get_language = MagicMock()
                importer.get_language.return_value = 'English'

                # WHEN: Importing bible file
                importer.filename = os.path.join(TEST_PATH, bible_file)
                importer.do_import()

                # THEN: The create_verse() method should have been called with each verse in the file.
                self.assertTrue(importer.create_verse.called)
                for verse_tag, verse_text in test_data['verses']:
                    importer.create_verse.assert_any_call(importer.create_book().id, '1', verse_tag, verse_text)

        def test_file_import_empty_verse_tags(self):
            """
            Test the actual import of OSIS Bible file, with an empty verse tags.
            """
            # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
            #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
            result_file = open(os.path.join(TEST_PATH, 'dk1933.json'), 'rb')
            test_data = json.loads(result_file.read().decode())
            bible_file = 'osis-dk1933-empty-verse.xml'
            with patch('openlp.plugins.bibles.lib.importers.osis.OSISBible.application'):
                mocked_manager = MagicMock()
                mocked_import_wizard = MagicMock()
                importer = OSISBible(mocked_manager, path='.', name='.', filename='')
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
                    importer.create_verse.assert_any_call(importer.create_book().id, '1', verse_tag, verse_text)
