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

from tests.functional import MagicMock, call, patch
from openlp.plugins.bibles.lib.bibleimport import BibleImport
from openlp.plugins.bibles.lib.db import BibleDB
from openlp.plugins.bibles.lib.importers.osis import OSISBible

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),  '..', '..', '..', 'resources', 'bibles'))


class TestOsisImport(TestCase):
    """
    Test the functions in the :mod:`osisimport` module.
    """
    def setUp(self):
        self.etree_patcher = patch('openlp.plugins.bibles.lib.importers.osis.etree')
        self.addCleanup(self.etree_patcher.stop)
        self.mocked_etree = self.etree_patcher.start()
        self.create_verse_patcher = patch('openlp.plugins.bibles.lib.db.BibleDB.create_verse')
        self.addCleanup(self.create_verse_patcher.stop)
        self.mocked_create_verse = self.create_verse_patcher.start()
        self.find_and_create_book_patch = patch.object(BibleImport, 'find_and_create_book')
        self.addCleanup(self.find_and_create_book_patch.stop)
        self.mocked_find_and_create_book = self.find_and_create_book_patch.start()
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

    def process_books_stop_import_test(self):
        """
        Test process_books when stop_import is set to True
        """
        # GIVEN: An instance of OSISBible adn some mocked data
        importer = OSISBible(MagicMock(), path='.', name='.', filename='')
        mocked_data = MagicMock(**{'xpath.return_value': ['Book']})

        # WHEN: stop_import_flag is set to True and process_books is called
        importer.stop_import_flag = True
        importer.process_books(mocked_data)

        # THEN: find_and_create_book should not have been called
        self.assertFalse(self.mocked_find_and_create_book.called)

    def process_books_completes_test(self):
        """
        Test process_books when it processes all books
        """
        # GIVEN: An instance of OSISBible Importer and two mocked books
        self.mocked_find_and_create_book.side_effect = ['db_book1', 'db_book2']
        with patch.object(OSISBible, 'process_chapters') as mocked_process_chapters:
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')

            book1 = MagicMock()
            book1.get.return_value = 'Name1'
            book2 = MagicMock()
            book2.get.return_value = 'Name2'
            mocked_data = MagicMock(**{'xpath.return_value': [book1, book2]})
            importer.language_id = 10
            importer.session = MagicMock()
            importer.stop_import_flag = False

            # WHEN: Calling process_books with the two books
            importer.process_books(mocked_data)

            # THEN: find_and_create_book and process_books should be called with the details from the mocked books
            self.assertEqual(self.mocked_find_and_create_book.call_args_list,
                             [call('Name1', 2, 10), call('Name2', 2, 10)])
            self.assertEqual(mocked_process_chapters.call_args_list,
                             [call('db_book1', book1), call('db_book2', book2)])
            self.assertEqual(importer.session.commit.call_count, 2)

    def process_chapters_verse_in_chapter_verse_text_test(self):
        """
        Test process_chapters when supplied with an etree element with a verse element nested in it
        """
        with patch('openlp.plugins.bibles.lib.importers.osis.verse_in_chapter', return_value=True), \
                patch('openlp.plugins.bibles.lib.importers.osis.text_in_verse', return_value=True), \
                patch.object(OSISBible, 'set_current_chapter') as mocked_set_current_chapter, \
                patch.object(OSISBible, 'process_verse') as mocked_process_verse:

            # GIVEN: Some test data and an instance of OSISBible
            test_book = MagicMock()
            test_verse = MagicMock()
            test_verse.tail = '\n    '  # Whitespace
            test_verse.text = 'Verse Text'
            test_chapter = MagicMock()
            test_chapter.__iter__.return_value = [test_verse]
            test_chapter.get.side_effect = lambda x: {'osisID': '1.2.4', 'sID': '999'}.get(x)
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling process_chapters
            importer.process_chapters(test_book, [test_chapter])

            # THEN: set_current_chapter and process_verse should have been called with the test data
            mocked_set_current_chapter.assert_called_once_with(test_book.name, 2)
            mocked_process_verse.assert_called_once_with(test_book, 2, test_verse)

    def process_chapters_verse_in_chapter_verse_milestone_test(self):
        """
        Test process_chapters when supplied with an etree element with a verse element nested, when the verse system is
        based on milestones
        """
        with patch('openlp.plugins.bibles.lib.importers.osis.verse_in_chapter', return_value=True), \
                patch('openlp.plugins.bibles.lib.importers.osis.text_in_verse', return_value=False), \
                patch.object(OSISBible, 'set_current_chapter') as mocked_set_current_chapter, \
                patch.object(OSISBible, 'process_verse') as mocked_process_verse:

            # GIVEN: Some test data and an instance of OSISBible
            test_book = MagicMock()
            test_verse = MagicMock()
            test_verse.tail = '\n    '  # Whitespace
            test_verse.text = 'Verse Text'
            test_chapter = MagicMock()
            test_chapter.__iter__.return_value = [test_verse]
            test_chapter.get.side_effect = lambda x: {'osisID': '1.2.4', 'sID': '999'}.get(x)
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling process_chapters
            importer.process_chapters(test_book, [test_chapter])

            # THEN: set_current_chapter and process_verse should have been called with the test data
            mocked_set_current_chapter.assert_called_once_with(test_book.name, 2)
            mocked_process_verse.assert_called_once_with(test_book, 2, test_verse, use_milestones=True)

    def process_chapters_milestones_chapter_no_sid_test(self):
        """
        Test process_chapters when supplied with an etree element with a chapter and verse element in the milestone
        configuration, where the chapter is the "closing" milestone. (Missing the sID attribute)
        """
        with patch('openlp.plugins.bibles.lib.importers.osis.verse_in_chapter', return_value=False), \
                patch.object(OSISBible, 'set_current_chapter') as mocked_set_current_chapter, \
                patch.object(OSISBible, 'process_verse') as mocked_process_verse:

            # GIVEN: Some test data and an instance of OSISBible
            test_book = MagicMock()
            test_chapter = MagicMock()
            test_chapter.tag = '{http://www.bibletechnologies.net/2003/OSIS/namespace}chapter'
            test_chapter.get.side_effect = lambda x: {'osisID': '1.2.4'}.get(x)

            # WHEN: Calling process_chapters
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')
            importer.process_chapters(test_book, [test_chapter])

            # THEN: neither set_current_chapter or process_verse should have been called
            self.assertFalse(mocked_set_current_chapter.called)
            self.assertFalse(mocked_process_verse.called)

    def process_chapters_milestones_chapter_sid_test(self):
        """
        Test process_chapters when supplied with an etree element with a chapter and verse element in the milestone
        configuration, where the chapter is the "opening" milestone. (Has the sID attribute)
        """
        with patch('openlp.plugins.bibles.lib.importers.osis.verse_in_chapter', return_value=False), \
                patch.object(OSISBible, 'set_current_chapter') as mocked_set_current_chapter, \
                patch.object(OSISBible, 'process_verse') as mocked_process_verse:

            # GIVEN: Some test data and an instance of OSISBible
            test_book = MagicMock()
            test_chapter = MagicMock()
            test_chapter.tag = '{http://www.bibletechnologies.net/2003/OSIS/namespace}chapter'
            test_chapter.get.side_effect = lambda x: {'osisID': '1.2.4', 'sID': '999'}.get(x)
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling process_chapters
            importer.process_chapters(test_book, [test_chapter])

            # THEN: set_current_chapter should have been called with the test data
            mocked_set_current_chapter.assert_called_once_with(test_book.name, 2)
            self.assertFalse(mocked_process_verse.called)

    def process_chapters_milestones_verse_tag_test(self):
        """
        Test process_chapters when supplied with an etree element with a chapter and verse element in the milestone
        configuration, where the verse is the "opening" milestone. (Has the sID attribute)
        """
        with patch('openlp.plugins.bibles.lib.importers.osis.verse_in_chapter', return_value=False), \
                patch.object(OSISBible, 'set_current_chapter') as mocked_set_current_chapter, \
                patch.object(OSISBible, 'process_verse') as mocked_process_verse:

            # GIVEN: Some test data and an instance of OSISBible
            test_book = MagicMock()
            test_verse = MagicMock()
            test_verse.get.side_effect = lambda x: {'osisID': '1.2.4', 'sID': '999'}.get(x)
            test_verse.tag = '{http://www.bibletechnologies.net/2003/OSIS/namespace}verse'
            test_verse.tail = '\n    '  # Whitespace
            test_verse.text = 'Verse Text'

            # WHEN: Calling process_chapters
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')
            importer.process_chapters(test_book, [test_verse])

            # THEN: process_verse should have been called with the test data
            self.assertFalse(mocked_set_current_chapter.called)
            mocked_process_verse.assert_called_once_with(test_book, 0, test_verse, use_milestones=True)

    def process_verse_no_osis_id_test(self):
        """
        Test process_verse when the element supplied does not have and osisID attribute
        """
        # GIVEN: An instance of OSISBible, and some mocked test data
        test_book = MagicMock()
        test_verse = MagicMock()
        test_verse.get.side_effect = lambda x: {}.get(x)
        test_verse.tail = 'Verse Text'
        test_verse.text = None
        importer = OSISBible(MagicMock(), path='.', name='.', filename='')

        # WHEN: Calling process_verse with the test data
        importer.process_verse(test_book, 2, test_verse)

        # THEN: create_verse should not have been called
        self.assertFalse(self.mocked_create_verse.called)

    def process_verse_use_milestones_no_s_id_test(self):
        """
        Test process_verse when called with use_milestones set to True, but the element supplied does not have and sID
        attribute
        """
        # GIVEN: An instance of OSISBible, and some mocked test data
        test_book = MagicMock()
        test_verse = MagicMock()
        test_verse.get.side_effect = lambda x: {}.get(x)
        test_verse.tail = 'Verse Text'
        test_verse.text = None
        importer = OSISBible(MagicMock(), path='.', name='.', filename='')

        # WHEN: Calling process_verse with the test data
        importer.process_verse(test_book, 2, test_verse)

        # THEN: create_verse should not have been called
        self.assertFalse(self.mocked_create_verse.called)

    def process_verse_use_milestones_no_tail_test(self):
        """
        Test process_verse when called with use_milestones set to True, but the element supplied does not have a 'tail'
        """
        # GIVEN: An instance of OSISBible, and some mocked test data
        test_book = MagicMock()
        test_verse = MagicMock()
        test_verse.tail = None
        test_verse.text = None
        test_verse.get.side_effect = lambda x: {'osisID': '1.2.4', 'sID': '999'}.get(x)
        importer = OSISBible(MagicMock(), path='.', name='.', filename='')

        # WHEN: Calling process_verse with the test data
        importer.process_verse(test_book, 2, test_verse, use_milestones=True)

        # THEN: create_verse should not have been called
        self.assertFalse(self.mocked_create_verse.called)

    def process_verse_use_milestones_success_test(self):
        """
        Test process_verse when called with use_milestones set to True, and the verse element successfully imports
        """
        # GIVEN: An instance of OSISBible, and some mocked test data
        test_book = MagicMock()
        test_book.id = 1
        test_verse = MagicMock()
        test_verse.tail = 'Verse Text'
        test_verse.text = None
        test_verse.get.side_effect = lambda x: {'osisID': '1.2.4', 'sID': '999'}.get(x)
        importer = OSISBible(MagicMock(), path='.', name='.', filename='')

        # WHEN: Calling process_verse with the test data
        importer.process_verse(test_book, 2, test_verse, use_milestones=True)

        # THEN: create_verse should have been called with the test data
        self.mocked_create_verse.assert_called_once_with(1, 2, 4, 'Verse Text')

    def process_verse_no_text_test(self):
        """
        Test process_verse when called with an empty verse element
        """
        # GIVEN: An instance of OSISBible, and some mocked test data
        test_book = MagicMock()
        test_book.id = 1
        test_verse = MagicMock()
        test_verse.tail = '\n    '  # Whitespace
        test_verse.text = None
        test_verse.get.side_effect = lambda x: {'osisID': '1.2.4', 'sID': '999'}.get(x)
        importer = OSISBible(MagicMock(), path='.', name='.', filename='')

        # WHEN: Calling process_verse with the test data
        importer.process_verse(test_book, 2, test_verse)

        # THEN: create_verse should not have been called
        self.assertFalse(self.mocked_create_verse.called)

    def process_verse_success_test(self):
        """
        Test process_verse when called with an element with text set
        """
        # GIVEN: An instance of OSISBible, and some mocked test data
        test_book = MagicMock()
        test_book.id = 1
        test_verse = MagicMock()
        test_verse.tail = '\n    '  # Whitespace
        test_verse.text = 'Verse Text'
        test_verse.get.side_effect = lambda x: {'osisID': '1.2.4', 'sID': '999'}.get(x)
        importer = OSISBible(MagicMock(), path='.', name='.', filename='')

        # WHEN: Calling process_verse with the test data
        importer.process_verse(test_book, 2, test_verse)

        # THEN: create_verse should have been called with the test data
        self.mocked_create_verse.assert_called_once_with(1, 2, 4, 'Verse Text')

    def do_import_parse_xml_fails_test(self):
        """
        Test do_import when parse_xml fails (returns None)
        """
        # GIVEN: An instance of OpenSongBible and a mocked parse_xml which returns False
        with patch.object(OSISBible, 'log_debug'), \
                patch.object(OSISBible, 'validate_xml_file'), \
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
        with patch.object(OSISBible, 'log_debug'), \
                patch.object(OSISBible, 'validate_xml_file'), \
                patch.object(OSISBible, 'parse_xml'), \
                patch.object(OSISBible, 'get_language_id', **{'return_value': False}), \
                patch.object(OSISBible, 'process_books') as mocked_process_books:
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling do_import
            result = importer.do_import()

            # THEN: do_import should return False and process_books should have not been called
            self.assertFalse(result)
            self.assertFalse(mocked_process_books.called)

    def do_import_completes_test(self):
        """
        Test do_import when it completes successfully
        """
        # GIVEN: An instance of OpenSongBible
        with patch.object(OSISBible, 'log_debug'), \
                patch.object(OSISBible, 'validate_xml_file'), \
                patch.object(OSISBible, 'parse_xml'), \
                patch.object(OSISBible, 'get_language_id', **{'return_value': 10}), \
                patch.object(OSISBible, 'process_books'):
            importer = OSISBible(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling do_import
            result = importer.do_import()

            # THEN: do_import should return True
            self.assertTrue(result)


class TestOsisImportFileImports(TestCase):
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
                importer.create_verse.assert_any_call(importer.create_book().id, 1, verse_tag, verse_text)

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
                    importer.create_verse.assert_any_call(importer.create_book().id, 1, verse_tag, verse_text)

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
                importer.create_verse.assert_any_call(importer.create_book().id, 1, verse_tag, verse_text)

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
                importer.create_verse.assert_any_call(importer.create_book().id, 1, verse_tag, verse_text)
