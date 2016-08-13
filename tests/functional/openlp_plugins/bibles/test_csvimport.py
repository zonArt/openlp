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
This module contains tests for the CSV Bible importer.
"""

import csv
import json
import os
from collections import namedtuple
from unittest import TestCase

from tests.functional import ANY, MagicMock, PropertyMock, call, patch
from openlp.core.lib.exceptions import ValidationError
from openlp.plugins.bibles.lib.bibleimport import BibleImport
from openlp.plugins.bibles.lib.importers.csvbible import Book, CSVBible, Verse


TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'resources', 'bibles'))


class TestCSVImport(TestCase):
    """
    Test the functions in the :mod:`csvimport` module.
    """

    def setUp(self):
        self.manager_patcher = patch('openlp.plugins.bibles.lib.db.Manager')
        self.registry_patcher = patch('openlp.plugins.bibles.lib.db.Registry')
        self.addCleanup(self.manager_patcher.stop)
        self.addCleanup(self.registry_patcher.stop)
        self.manager_patcher.start()
        self.registry_patcher.start()

    def test_create_importer(self):
        """
        Test creating an instance of the CSV file importer
        """
        # GIVEN: A mocked out "manager"
        mocked_manager = MagicMock()

        # WHEN: An importer object is created
        importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verse.csv')

        # THEN: The importer should be an instance of BibleImport
        self.assertIsInstance(importer, BibleImport)
        self.assertEqual(importer.books_file, 'books.csv')
        self.assertEqual(importer.verses_file, 'verse.csv')

    def book_namedtuple_test(self):
        """
        Test that the Book namedtuple is created as expected
        """
        # GIVEN: The Book namedtuple
        # WHEN: Creating an instance of Book
        result = Book('id', 'testament_id', 'name', 'abbreviation')

        # THEN: The attributes should match up with the data we used
        self.assertEqual(result.id, 'id')
        self.assertEqual(result.testament_id, 'testament_id')
        self.assertEqual(result.name, 'name')
        self.assertEqual(result.abbreviation, 'abbreviation')

    def verse_namedtuple_test(self):
        """
        Test that the Verse namedtuple is created as expected
        """
        # GIVEN: The Verse namedtuple
        # WHEN: Creating an instance of Verse
        result = Verse('book_id_name', 'chapter_number', 'number', 'text')

        # THEN: The attributes should match up with the data we used
        self.assertEqual(result.book_id_name, 'book_id_name')
        self.assertEqual(result.chapter_number, 'chapter_number')
        self.assertEqual(result.number, 'number')
        self.assertEqual(result.text, 'text')

    def get_book_name_id_test(self):
        """
        Test that get_book_name() returns the correct book when called with an id
        """
        # GIVEN: A dictionary of books with their id as the keys
        books = {1: 'Book 1', 2: 'Book 2', 3: 'Book 3'}

        # WHEN: Calling get_book_name() and the name is an integer represented as a string
        test_data = [['1', 'Book 1'], ['2', 'Book 2'], ['3', 'Book 3']]
        for name, expected_result in test_data:
            actual_result = CSVBible.get_book_name(name, books)

            # THEN: get_book_name() should return the book name associated with that id from the books dictionary
            self.assertEqual(actual_result, expected_result)

    def get_book_name_test(self):
        """
        Test that get_book_name() returns the name when called with a non integer value
        """
        # GIVEN: A dictionary of books with their id as the keys
        books = {1: 'Book 1', 2: 'Book 2', 3: 'Book 3'}

        # WHEN: Calling get_book_name() and the name is not an integer represented as a string
        test_data = [['Book 4', 'Book 4'], ['Book 5', 'Book 5'], ['Book 6', 'Book 6']]
        for name, expected_result in test_data:
            actual_result = CSVBible.get_book_name(name, books)

            # THEN: get_book_name() should return the input
            self.assertEqual(actual_result, expected_result)

    def parse_csv_file_test(self):
        """
        Test the parse_csv_file() with sample data
        """
        # GIVEN: A mocked csv.reader which returns an iterator with test data
        test_data = [['1', 'Line 1', 'Data 1'], ['2', 'Line 2', 'Data 2'], ['3', 'Line 3', 'Data 3']]
        TestTuple = namedtuple('TestTuple', 'line_no line_description line_data')

        with patch('openlp.plugins.bibles.lib.importers.csvbible.get_file_encoding',
                   return_value={'encoding': 'utf-8', 'confidence': 0.99}),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.open', create=True) as mocked_open,\
                patch('openlp.plugins.bibles.lib.importers.csvbible.csv.reader',
                      return_value=iter(test_data)) as mocked_reader:

            # WHEN: Calling the CSVBible parse_csv_file method with a file name and TestTuple
            result = CSVBible.parse_csv_file('file.csv', TestTuple)

            # THEN: A list of TestTuple instances with the parsed data should be returned
            self.assertEqual(result, [TestTuple('1', 'Line 1', 'Data 1'), TestTuple('2', 'Line 2', 'Data 2'),
                                      TestTuple('3', 'Line 3', 'Data 3')])
            mocked_open.assert_called_once_with('file.csv', 'r', encoding='utf-8', newline='')
            mocked_reader.assert_called_once_with(ANY, delimiter=',', quotechar='"')

    def parse_csv_file_oserror_test(self):
        """
        Test the parse_csv_file() handles an OSError correctly
        """
        # GIVEN: Mocked a mocked open object which raises an OSError
        with patch('openlp.plugins.bibles.lib.importers.csvbible.get_file_encoding',
                   return_value={'encoding': 'utf-8', 'confidence': 0.99}),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.open', side_effect=OSError, create=True):

            # WHEN: Calling CSVBible.parse_csv_file
            # THEN: A ValidationError should be raised
            with self.assertRaises(ValidationError) as context:
                CSVBible.parse_csv_file('file.csv', None)
            self.assertEqual(context.exception.msg, 'Parsing "file.csv" failed')

    def parse_csv_file_csverror_test(self):
        """
        Test the parse_csv_file() handles an csv.Error correctly
        """
        # GIVEN: Mocked a csv.reader which raises an csv.Error
        with patch('openlp.plugins.bibles.lib.importers.csvbible.get_file_encoding',
                   return_value={'encoding': 'utf-8', 'confidence': 0.99}),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.open', create=True),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.csv.reader', side_effect=csv.Error):

            # WHEN: Calling CSVBible.parse_csv_file
            # THEN: A ValidationError should be raised
            with self.assertRaises(ValidationError) as context:
                CSVBible.parse_csv_file('file.csv', None)
            self.assertEqual(context.exception.msg, 'Parsing "file.csv" failed')

    def process_books_stopped_import_test(self):
        """
        Test process books when the import is stopped
        """
        # GIVEN: An instance of CSVBible with the stop_import_flag set to True
        mocked_manager = MagicMock()
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'):
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verse.csv')
            type(importer).application = PropertyMock()
            importer.stop_import_flag = True
            importer.wizard = MagicMock()

            # WHEN: Calling process_books
            result = importer.process_books(['Book 1'])

            # THEN: increment_progress_bar should not be called and the return value should be None
            self.assertFalse(importer.wizard.increment_progress_bar.called)
            self.assertIsNone(result)

    def process_books_test(self):
        """
        Test process books when it completes successfully
        """
        # GIVEN: An instance of CSVBible with the stop_import_flag set to False, and some sample data
        mocked_manager = MagicMock()
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.translate'):
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verse.csv')
            type(importer).application = PropertyMock()
            importer.find_and_create_book = MagicMock()
            importer.language_id = 10
            importer.stop_import_flag = False
            importer.wizard = MagicMock()

            books = [Book('1', '1', '1. Mosebog', '1Mos'), Book('2', '1', '2. Mosebog', '2Mos')]

            # WHEN: Calling process_books
            result = importer.process_books(books)

            # THEN: translate and find_and_create_book should have been called with both book names.
            # 		The returned data should be a dictionary with both song's id and names.
            self.assertEqual(importer.find_and_create_book.mock_calls,
                             [call('1. Mosebog', 2, 10), call('2. Mosebog', 2, 10)])
            importer.application.process_events.assert_called_once_with()
            self.assertDictEqual(result, {1: '1. Mosebog', 2: '2. Mosebog'})

    def process_verses_stopped_import_test(self):
        """
        Test process_verses when the import is stopped
        """
        # GIVEN: An instance of CSVBible with the stop_import_flag set to True
        mocked_manager = MagicMock()
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'):
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verse.csv')
            type(importer).application = PropertyMock()
            importer.get_book_name = MagicMock()
            importer.session = MagicMock()
            importer.stop_import_flag = True
            importer.wizard = MagicMock()

            # WHEN: Calling process_verses
            result = importer.process_verses([], [])

            # THEN: get_book_name should not be called and the return value should be None
            self.assertFalse(importer.get_book_name.called)
            importer.wizard.increment_progress_bar.assert_called_once_with('Importing verses... done.')
            importer.application.process_events.assert_called_once_with()
            self.assertIsNone(result)

    def process_verses_successful_test(self):
        """
        Test process_verses when the import is successful
        """
        # GIVEN: An instance of CSVBible with the application and wizard attributes mocked out, and some test data.
        mocked_manager = MagicMock()
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.translate'):
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verse.csv')
            type(importer).application = PropertyMock()
            importer.create_verse = MagicMock()
            importer.get_book = MagicMock(return_value=Book('1', '1', '1. Mosebog', '1Mos'))
            importer.get_book_name = MagicMock(return_value='1. Mosebog')
            importer.session = MagicMock()
            importer.stop_import_flag = False
            importer.wizard = MagicMock()
            verses = [Verse(1, 1, 1, 'I Begyndelsen skabte Gud Himmelen og Jorden.'),
                      Verse(1, 1, 2, 'Og Jorden var øde og tom, og der var Mørke over Verdensdybet. '
                                     'Men Guds Ånd svævede over Vandene.')]
            books = {1: '1. Mosebog'}

            # WHEN: Calling process_verses
            importer.process_verses(verses, books)

            # THEN: create_verse is called with the test data
            self.assertEqual(importer.get_book_name.mock_calls, [call(1, books), call(1, books)])
            importer.get_book.assert_called_once_with('1. Mosebog')
            self.assertEqual(importer.session.commit.call_count, 2)
            self.assertEqual(importer.create_verse.mock_calls,
                             [call('1', 1, 1, 'I Begyndelsen skabte Gud Himmelen og Jorden.'),
                              call('1', 1, 2, 'Og Jorden var øde og tom, og der var Mørke over Verdensdybet. '
                                              'Men Guds Ånd svævede over Vandene.')])
            importer.application.process_events.assert_called_once_with()

    def do_import_invalid_language_id_test(self):
        """
        Test do_import when the user cancels the language selection dialog box
        """
        # GIVEN: An instance of CSVBible and a mocked get_language which simulates the user cancelling the language box
        mocked_manager = MagicMock()
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.log') as mocked_log:
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verse.csv')
            importer.get_language = MagicMock(return_value=None)

            # WHEN: Calling do_import
            result = importer.do_import('Bible Name')

            # THEN: The log.exception method should have been called to show that it reached the except clause.
            # False should be returned.
            importer.get_language.assert_called_once_with('Bible Name')
            mocked_log.exception.assert_called_once_with('Could not import CSV bible')
            self.assertFalse(result)

    def do_import_stop_import_test(self):
        """
        Test do_import when the import is stopped
        """
        # GIVEN: An instance of CSVBible with stop_import set to True
        mocked_manager = MagicMock()
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.log') as mocked_log:
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verse.csv')
            importer.get_language = MagicMock(return_value=10)
            importer.parse_csv_file = MagicMock(return_value=['Book 1', 'Book 2', 'Book 3'])
            importer.process_books = MagicMock()
            importer.stop_import_flag = True
            importer.wizard = MagicMock()

            # WHEN: Calling do_import
            result = importer.do_import('Bible Name')

            # THEN: log.exception should not be called, parse_csv_file should only be called once,
            # and False should be returned.
            self.assertFalse(mocked_log.exception.called)
            importer.parse_csv_file.assert_called_once_with('books.csv', Book)
            importer.process_books.assert_called_once_with(['Book 1', 'Book 2', 'Book 3'])
            self.assertFalse(result)

    def do_import_stop_import_2_test(self):
        """
        Test do_import when the import is stopped
        """
        # GIVEN: An instance of CSVBible with stop_import which is True the second time of calling
        mocked_manager = MagicMock()
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.log') as mocked_log:
            CSVBible.stop_import_flag = PropertyMock(side_effect=[False, True])
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verses.csv')
            importer.get_language = MagicMock(return_value=10)
            importer.parse_csv_file = MagicMock(side_effect=[['Book 1'], ['Verse 1']])
            importer.process_books = MagicMock(return_value=['Book 1'])
            importer.process_verses = MagicMock(return_value=['Verse 1'])
            importer.wizard = MagicMock()

            # WHEN: Calling do_import
            result = importer.do_import('Bible Name')

            # THEN: log.exception should not be called, parse_csv_file should be called twice,
            # and False should be returned.
            self.assertFalse(mocked_log.exception.called)
            self.assertEqual(importer.parse_csv_file.mock_calls, [call('books.csv', Book), call('verses.csv', Verse)])
            importer.process_verses.assert_called_once_with(['Verse 1'], ['Book 1'])
            self.assertFalse(result)

            # Cleanup
            del CSVBible.stop_import_flag

    def do_import_success_test(self):
        """
        Test do_import when the import succeeds
        """
        # GIVEN: An instance of CSVBible
        mocked_manager = MagicMock()
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'),\
                patch('openlp.plugins.bibles.lib.importers.csvbible.log') as mocked_log:
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile='books.csv', versefile='verses.csv')
            importer.get_language = MagicMock(return_value=10)
            importer.parse_csv_file = MagicMock(side_effect=[['Book 1'], ['Verse 1']])
            importer.process_books = MagicMock(return_value=['Book 1'])
            importer.process_verses = MagicMock(return_value=['Verse 1'])
            importer.session = MagicMock()
            importer.stop_import_flag = False
            importer.wizard = MagicMock()

            # WHEN: Calling do_import
            result = importer.do_import('Bible Name')

            # THEN: log.exception should not be called, parse_csv_file should be called twice,
            # and True should be returned.
            self.assertFalse(mocked_log.exception.called)
            self.assertEqual(importer.parse_csv_file.mock_calls, [call('books.csv', Book), call('verses.csv', Verse)])
            importer.process_books.assert_called_once_with(['Book 1'])
            importer.process_verses.assert_called_once_with(['Verse 1'], ['Book 1'])
            self.assertTrue(result)

    def file_import_test(self):
        """
        Test the actual import of CSV Bible file
        """
        # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
        #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
        result_file = open(os.path.join(TEST_PATH, 'dk1933.json'), 'rb')
        test_data = json.loads(result_file.read().decode())
        books_file = os.path.join(TEST_PATH, 'dk1933-books.csv')
        verses_file = os.path.join(TEST_PATH, 'dk1933-verses.csv')
        with patch('openlp.plugins.bibles.lib.importers.csvbible.CSVBible.application'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = CSVBible(mocked_manager, path='.', name='.', booksfile=books_file, versefile=verses_file)
            importer.wizard = mocked_import_wizard
            importer.get_book_ref_id_by_name = MagicMock()
            importer.create_verse = MagicMock()
            importer.create_book = MagicMock()
            importer.session = MagicMock()
            importer.get_language = MagicMock()
            importer.get_language.return_value = 'Danish'
            importer.get_book = MagicMock()

            # WHEN: Importing bible file
            importer.do_import()

            # THEN: The create_verse() method should have been called with each verse in the file.
            self.assertTrue(importer.create_verse.called)
            for verse_tag, verse_text in test_data['verses']:
                importer.create_verse.assert_any_call(importer.get_book().id, '1', verse_tag, verse_text)
            importer.create_book.assert_any_call('1. Mosebog', importer.get_book_ref_id_by_name(), 1)
            importer.create_book.assert_any_call('1. Krønikebog', importer.get_book_ref_id_by_name(), 1)
