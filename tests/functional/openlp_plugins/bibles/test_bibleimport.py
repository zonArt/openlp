# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 OpenLP Developers                                   #
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
This module contains tests for the bibleimport module.
"""

from io import BytesIO
from lxml import etree, objectify

from unittest import TestCase
from PyQt5.QtWidgets import QDialog

from openlp.core.common.languages import Language
from openlp.core.lib.exceptions import ValidationError
from openlp.plugins.bibles.lib.bibleimport import BibleImport
from openlp.plugins.bibles.lib.db import BibleDB
from tests.functional import MagicMock, patch


class TestBibleImport(TestCase):
    """
    Test the functions in the :mod:`bibleimport` module.
    """

    def setUp(self):
        self.test_file = BytesIO(
            b'<?xml version="1.0" encoding="UTF-8" ?>\n'
            b'<root>\n'
            b'    <data><div>Test<p>data</p><a>to</a>keep</div></data>\n'
            b'    <data><unsupported>Test<x>data</x><y>to</y>discard</unsupported></data>\n'
            b'</root>'
        )
        self.open_patcher = patch('builtins.open')
        self.addCleanup(self.open_patcher.stop)
        self.mocked_open = self.open_patcher.start()
        self.critical_error_message_box_patcher = \
            patch('openlp.plugins.bibles.lib.bibleimport.critical_error_message_box')
        self.addCleanup(self.critical_error_message_box_patcher.stop)
        self.mocked_critical_error_message_box = self.critical_error_message_box_patcher.start()
        self.setup_patcher = patch('openlp.plugins.bibles.lib.db.BibleDB._setup')
        self.addCleanup(self.setup_patcher.stop)
        self.setup_patcher.start()
        self.translate_patcher = patch('openlp.plugins.bibles.lib.bibleimport.translate',
                                       side_effect=lambda module, string_to_translate, *args: string_to_translate)
        self.addCleanup(self.translate_patcher.stop)
        self.mocked_translate = self.translate_patcher.start()
        self.registry_patcher = patch('openlp.plugins.bibles.lib.bibleimport.Registry')
        self.addCleanup(self.registry_patcher.stop)
        self.registry_patcher.start()

    def init_kwargs_none_test(self):
        """
        Test the initialisation of the BibleImport Class when no key word arguments are supplied
        """
        # GIVEN: A patched BibleDB._setup, BibleImport class and mocked parent
        # WHEN: Creating an instance of BibleImport with no key word arguments
        instance = BibleImport(MagicMock())

        # THEN: The filename attribute should be None
        self.assertIsNone(instance.filename)
        self.assertIsInstance(instance, BibleDB)

    def init_kwargs_set_test(self):
        """
        Test the initialisation of the BibleImport Class when supplied with select keyword arguments
        """
        # GIVEN: A patched BibleDB._setup, BibleImport class and mocked parent
        # WHEN: Creating an instance of BibleImport with selected key word arguments
        kwargs = {'filename': 'bible.xml'}
        instance = BibleImport(MagicMock(), **kwargs)

        # THEN: The filename keyword should be set to bible.xml
        self.assertEqual(instance.filename, 'bible.xml')
        self.assertIsInstance(instance, BibleDB)

    def get_language_canceled_test(self):
        """
        Test the BibleImport.get_language method when the user rejects the dialog box
        """
        # GIVEN: A mocked LanguageForm with an exec method which returns QtDialog.Rejected and an instance of BibleDB
        with patch.object(BibleDB, '_setup'), patch('openlp.plugins.bibles.forms.LanguageForm') as mocked_language_form:

            # The integer value of QtDialog.Rejected is 0. Using the enumeration causes a seg fault for some reason
            mocked_language_form_instance = MagicMock(**{'exec.return_value': 0})
            mocked_language_form.return_value = mocked_language_form_instance
            instance = BibleImport(MagicMock())
            mocked_wizard = MagicMock()
            instance.wizard = mocked_wizard

            # WHEN: Calling get_language()
            result = instance.get_language()

            # THEN: get_language() should return False
            mocked_language_form.assert_called_once_with(mocked_wizard)
            mocked_language_form_instance.exec.assert_called_once_with(None)
            self.assertFalse(result, 'get_language() should return False if the user rejects the dialog box')

    def get_language_accepted_test(self):
        """
        Test the BibleImport.get_language method when the user accepts the dialog box
        """
        # GIVEN: A mocked LanguageForm with an exec method which returns QtDialog.Accepted an instance of BibleDB and
        #       a combobox with the selected item data as 10
        with patch.object(BibleDB, 'save_meta'), patch.object(BibleDB, '_setup'), \
                patch('openlp.plugins.bibles.forms.LanguageForm') as mocked_language_form:

            # The integer value of QtDialog.Accepted is 1. Using the enumeration causes a seg fault for some reason
            mocked_language_form_instance = MagicMock(**{'exec.return_value': 1,
                                                         'language_combo_box.itemData.return_value': 10})
            mocked_language_form.return_value = mocked_language_form_instance
            instance = BibleImport(MagicMock())
            mocked_wizard = MagicMock()
            instance.wizard = mocked_wizard

            # WHEN: Calling get_language()
            result = instance.get_language('Bible Name')

            # THEN: get_language() should return the id of the selected language in the combo box
            mocked_language_form.assert_called_once_with(mocked_wizard)
            mocked_language_form_instance.exec.assert_called_once_with('Bible Name')
            self.assertEqual(result, 10, 'get_language() should return the id of the language the user has chosen when '
                                         'they accept the dialog box')

    def get_language_id_language_found_test(self):
        """
        Test get_language_id() when called with a name found in the languages list
        """
        # GIVEN: A mocked languages.get_language which returns language and an instance of BibleImport
        with patch('openlp.core.common.languages.get_language', return_value=Language(30, 'English', 'en')) \
                as mocked_languages_get_language, \
                patch.object(BibleImport, 'get_language') as mocked_db_get_language:
            instance = BibleImport(MagicMock())
            instance.save_meta = MagicMock()

            # WHEN: Calling get_language_id() with a language name and bible name
            result = instance.get_language_id('English', 'KJV')

            # THEN: The id of the language returned from languages.get_language should be returned
            mocked_languages_get_language.assert_called_once_with('English')
            self.assertFalse(mocked_db_get_language.called)
            instance.save_meta.assert_called_once_with('language_id', 30)
            self.assertEqual(result, 30)

    def get_language_id_language_not_found_test(self):
        """
        Test get_language_id() when called with a name not found in the languages list
        """
        # GIVEN: A mocked languages.get_language which returns language and an instance of BibleImport
        with patch('openlp.core.common.languages.get_language', return_value=None) as mocked_languages_get_language, \
                patch.object(BibleImport, 'get_language', return_value=20) as mocked_db_get_language:
            instance = BibleImport(MagicMock())
            instance.save_meta = MagicMock()

            # WHEN: Calling get_language_id() with a language name and bible name
            result = instance.get_language_id('RUS', 'KJV')

            # THEN: The id of the language returned from languages.get_language should be returned
            mocked_languages_get_language.assert_called_once_with('RUS')
            mocked_db_get_language.assert_called_once_with('KJV')
            instance.save_meta.assert_called_once_with('language_id', 20)
            self.assertEqual(result, 20)

    def get_language_id_user_choice_test(self):
        """
        Test get_language_id() when the language is not found and the user is asked for the language
        """
        # GIVEN: A mocked languages.get_language which returns None a mocked BibleDB.get_language which returns a
        #       language id.
        with patch('openlp.core.common.languages.get_language', return_value=None) as mocked_languages_get_language, \
                patch.object(BibleImport, 'get_language', return_value=40) as mocked_db_get_language, \
                patch.object(BibleImport, 'log_error') as mocked_log_error:
            instance = BibleImport(MagicMock())
            instance.save_meta = MagicMock()

            # WHEN: Calling get_language_id() with a language name and bible name
            result = instance.get_language_id('English', 'KJV')

            # THEN: The id of the language returned from BibleDB.get_language should be returned
            mocked_languages_get_language.assert_called_once_with('English')
            mocked_db_get_language.assert_called_once_with('KJV')
            self.assertFalse(mocked_log_error.error.called)
            instance.save_meta.assert_called_once_with('language_id', 40)
            self.assertEqual(result, 40)

    def get_language_id_user_choice_rejected_test(self):
        """
        Test get_language_id() when the language is not found and the user rejects the dilaog box
        """
        # GIVEN: A mocked languages.get_language which returns None a mocked BibleDB.get_language which returns a
        #       language id.
        with patch('openlp.core.common.languages.get_language', return_value=None) as mocked_languages_get_language, \
                patch.object(BibleImport, 'get_language', return_value=None) as mocked_db_get_language, \
                patch.object(BibleImport, 'log_error') as mocked_log_error:
            instance = BibleImport(MagicMock())
            instance.save_meta = MagicMock()

            # WHEN: Calling get_language_id() with a language name and bible name
            result = instance.get_language_id('Qwerty', 'KJV')

            # THEN: None should be returned and an error should be logged
            mocked_languages_get_language.assert_called_once_with('Qwerty')
            mocked_db_get_language.assert_called_once_with('KJV')
            mocked_log_error.assert_called_once_with(
                'Language detection failed when importing from "KJV". User aborted language selection.')
            self.assertFalse(instance.save_meta.called)
            self.assertIsNone(result)

    def get_book_ref_id_by_name_get_book_test(self):
        """
        Test get_book_ref_id_by_name when the book is found as a book in BiblesResourcesDB
        """
        # GIVEN: An instance of BibleImport and a mocked BiblesResourcesDB which returns a book id when get_book is
        #        called
        with patch.object(BibleImport, 'log_debug'), \
                patch('openlp.plugins.bibles.lib.bibleimport.BiblesResourcesDB',
                      **{'get_book.return_value':{'id': 20}}):
            instance = BibleImport(MagicMock())

            # WHEN: Calling get_book_ref_id_by_name
            result = instance.get_book_ref_id_by_name('Gen', 66, 4)

            # THEN: The bible id should be returned
            self.assertEqual(result,20)

    def get_book_ref_id_by_name_get_alternative_book_name_test(self):
        """
        Test get_book_ref_id_by_name when the book is found as an alternative book in BiblesResourcesDB
        """
        # GIVEN: An instance of BibleImport and a mocked BiblesResourcesDB which returns a book id when
        #        get_alternative_book_name is called
        with patch.object(BibleImport, 'log_debug'), \
                patch('openlp.plugins.bibles.lib.bibleimport.BiblesResourcesDB',
                      **{'get_book.return_value': None, 'get_alternative_book_name.return_value': 30}):
            instance = BibleImport(MagicMock())

            # WHEN: Calling get_book_ref_id_by_name
            result = instance.get_book_ref_id_by_name('Gen', 66, 4)

            # THEN: The bible id should be returned
            self.assertEqual(result, 30)

    def get_book_ref_id_by_name_get_book_reference_id_test(self):
        """
        Test get_book_ref_id_by_name when the book is found as a book in AlternativeBookNamesDB
        """
        # GIVEN: An instance of BibleImport and a mocked AlternativeBookNamesDB which returns a book id when
        #        get_book_reference_id is called
        with patch.object(BibleImport, 'log_debug'), \
                patch('openlp.plugins.bibles.lib.bibleimport.BiblesResourcesDB',
                   **{'get_book.return_value': None, 'get_alternative_book_name.return_value': None}), \
                patch('openlp.plugins.bibles.lib.bibleimport.AlternativeBookNamesDB',
                      **{'get_book_reference_id.return_value': 40}):
            instance = BibleImport(MagicMock())

            # WHEN: Calling get_book_ref_id_by_name
            result = instance.get_book_ref_id_by_name('Gen', 66, 4)

            # THEN: The bible id should be returned
            self.assertEqual(result, 40)

    def get_book_ref_id_by_name_book_name_form_rejected_test(self):
        """
        Test get_book_ref_id_by_name when the user rejects the BookNameForm
        """
        # GIVEN: An instance of BibleImport and a mocked BookNameForm which simulates a user rejecting the dialog
        with patch.object(BibleImport, 'log_debug'), patch.object(BibleImport, 'get_books'), \
                patch('openlp.plugins.bibles.lib.bibleimport.BiblesResourcesDB',
                      **{'get_book.return_value': None, 'get_alternative_book_name.return_value': None}), \
                patch('openlp.plugins.bibles.lib.bibleimport.AlternativeBookNamesDB',
                      **{'get_book_reference_id.return_value': None}), \
                patch('openlp.plugins.bibles.forms.BookNameForm',
                      return_value=MagicMock(**{'exec.return_value': QDialog.Rejected})):
            instance = BibleImport(MagicMock())

            # WHEN: Calling get_book_ref_id_by_name
            result = instance.get_book_ref_id_by_name('Gen', 66, 4)

            # THEN: None should be returned
            self.assertIsNone(result)

    def get_book_ref_id_by_name_book_name_form_accepted_test(self):
        """
        Test get_book_ref_id_by_name when the user accepts the BookNameForm
        """
        # GIVEN: An instance of BibleImport and a mocked BookNameForm which simulates a user accepting the dialog
        with patch.object(BibleImport, 'log_debug'), patch.object(BibleImport, 'get_books'), \
                 patch('openlp.plugins.bibles.lib.bibleimport.BiblesResourcesDB',
                       **{'get_book.return_value': None, 'get_alternative_book_name.return_value': None}), \
                 patch('openlp.plugins.bibles.lib.bibleimport.AlternativeBookNamesDB',
                       **{'get_book_reference_id.return_value': None}) as mocked_alternative_book_names_db, \
                 patch('openlp.plugins.bibles.forms.BookNameForm',
                       return_value=MagicMock(**{'exec.return_value': QDialog.Accepted, 'book_id':50})):
            instance = BibleImport(MagicMock())

            # WHEN: Calling get_book_ref_id_by_name
            result = instance.get_book_ref_id_by_name('Gen', 66, 4)

            # THEN: An alternative book name should be created and a bible id should be returned
            mocked_alternative_book_names_db.create_alternative_book_name.assert_called_once_with('Gen', 50, 4)
            self.assertEqual(result, 50)

    def is_compressed_compressed_test(self):
        """
        Test is_compressed when the 'file' being tested is compressed
        """
        # GIVEN: An instance of BibleImport and a mocked is_zipfile which returns True
        with patch('openlp.plugins.bibles.lib.bibleimport.is_zipfile', return_value=True):
            instance = BibleImport(MagicMock())

            # WHEN: Calling is_compressed
            result = instance.is_compressed('file.ext')

            # THEN: Then critical_error_message_box should be called informing the user that the file is compressed and
            #       True should be returned
            self.mocked_critical_error_message_box.assert_called_once_with(
                message='The file "file.ext" you supplied is compressed. You must decompress it before import.')
            self.assertTrue(result)

    def is_compressed_not_compressed_test(self):
        """
        Test is_compressed when the 'file' being tested is not compressed
        """
        # GIVEN: An instance of BibleImport and a mocked is_zipfile which returns False
        with patch('openlp.plugins.bibles.lib.bibleimport.is_zipfile', return_value=False):
            instance = BibleImport(MagicMock())

            # WHEN: Calling is_compressed
            result = instance.is_compressed('file.ext')

            # THEN: False should be returned and critical_error_message_box should not have been called
            self.assertFalse(result)
            self.assertFalse(self.mocked_critical_error_message_box.called)

    def parse_xml_etree_test(self):
        """
        Test BibleImport.parse_xml() when called with the use_objectify default value
        """
        # GIVEN: A sample "file" to parse and an instance of BibleImport
        self.mocked_open.return_value = self.test_file
        instance = BibleImport(MagicMock())
        instance.wizard = MagicMock()

        # WHEN: Calling parse_xml
        result = instance.parse_xml('file.tst')

        # THEN: The result returned should contain the correct data, and should be an instance of eetree_Element
        self.assertEqual(etree.tostring(result),
                         b'<root>\n    <data><div>Test<p>data</p><a>to</a>keep</div></data>\n'
                         b'    <data><unsupported>Test<x>data</x><y>to</y>discard</unsupported></data>\n</root>')
        self.assertIsInstance(result, etree._Element)

    def parse_xml_etree_use_objectify_test(self):
        """
        Test BibleImport.parse_xml() when called with use_objectify set to True
        """
        # GIVEN: A sample "file" to parse and an instance of BibleImport
        self.mocked_open.return_value = self.test_file
        instance = BibleImport(MagicMock())
        instance.wizard = MagicMock()

        # WHEN: Calling parse_xml
        result = instance.parse_xml('file.tst', use_objectify=True)

        # THEN: The result returned should contain the correct data, and should be an instance of ObjectifiedElement
        self.assertEqual(etree.tostring(result),
                         b'<root><data><div>Test<p>data</p><a>to</a>keep</div></data>'
                         b'<data><unsupported>Test<x>data</x><y>to</y>discard</unsupported></data></root>')
        self.assertIsInstance(result, objectify.ObjectifiedElement)

    def parse_xml_elements_test(self):
        """
        Test BibleImport.parse_xml() when given a tuple of elements to remove
        """
        # GIVEN: A tuple of elements to remove and an instance of BibleImport
        self.mocked_open.return_value = self.test_file
        elements = ('unsupported', 'x', 'y')
        instance = BibleImport(MagicMock())
        instance.wizard = MagicMock()

        # WHEN: Calling parse_xml, with a test file
        result = instance.parse_xml('file.tst', elements=elements)

        # THEN: The result returned should contain the correct data
        self.assertEqual(etree.tostring(result),
                         b'<root>\n    <data><div>Test<p>data</p><a>to</a>keep</div></data>\n    <data/>\n</root>')

    def parse_xml_tags_test(self):
        """
        Test BibleImport.parse_xml() when given a tuple of tags to remove
        """
        # GIVEN: A tuple of tags to remove and an instance of BibleImport
        self.mocked_open.return_value = self.test_file
        tags = ('div', 'p', 'a')
        instance = BibleImport(MagicMock())
        instance.wizard = MagicMock()

        # WHEN: Calling parse_xml, with a test file
        result = instance.parse_xml('file.tst', tags=tags)

        # THEN: The result returned should contain the correct data
        self.assertEqual(etree.tostring(result), b'<root>\n    <data>Testdatatokeep</data>\n    <data><unsupported>Test'
                                                 b'<x>data</x><y>to</y>discard</unsupported></data>\n</root>')

    def parse_xml_elements_tags_test(self):
        """
        Test BibleImport.parse_xml() when given a tuple of elements and of tags to remove
        """
        # GIVEN: A tuple of elements and of tags to remove and an instacne of BibleImport
        self.mocked_open.return_value = self.test_file
        elements = ('unsupported', 'x', 'y')
        tags = ('div', 'p', 'a')
        instance = BibleImport(MagicMock())
        instance.wizard = MagicMock()

        # WHEN: Calling parse_xml, with a test file
        result = instance.parse_xml('file.tst', elements=elements, tags=tags)

        # THEN: The result returned should contain the correct data
        self.assertEqual(etree.tostring(result), b'<root>\n    <data>Testdatatokeep</data>\n    <data/>\n</root>')

    def parse_xml_file_file_not_found_exception_test(self):
        """
        Test that parse_xml handles a FileNotFoundError exception correctly
        """
        with patch.object(BibleImport, 'log_exception') as mocked_log_exception:
            # GIVEN: A mocked open which raises a FileNotFoundError and an instance of BibleImporter
            exception = FileNotFoundError()
            exception.filename = 'file.tst'
            exception.strerror = 'No such file or directory'
            self.mocked_open.side_effect = exception
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling parse_xml
            result = importer.parse_xml('file.tst')

            # THEN: parse_xml should have caught the error, informed the user and returned None
            mocked_log_exception.assert_called_once_with('Opening file.tst failed.')
            self.mocked_critical_error_message_box.assert_called_once_with(
                title='An Error Occured When Opening A File',
                message='The following error occurred when trying to open\nfile.tst:\n\nNo such file or directory')
            self.assertIsNone(result)

    def parse_xml_file_permission_error_exception_test(self):
        """
        Test that parse_xml handles a PermissionError exception correctly
        """
        with patch.object(BibleImport, 'log_exception') as mocked_log_exception:
            # GIVEN: A mocked open which raises a PermissionError and an instance of BibleImporter
            exception = PermissionError()
            exception.filename = 'file.tst'
            exception.strerror = 'Permission denied'
            self.mocked_open.side_effect = exception
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling parse_xml
            result = importer.parse_xml('file.tst')

            # THEN: parse_xml should have caught the error, informed the user and returned None
            mocked_log_exception.assert_called_once_with('Opening file.tst failed.')
            self.mocked_critical_error_message_box.assert_called_once_with(
                title='An Error Occured When Opening A File',
                message='The following error occurred when trying to open\nfile.tst:\n\nPermission denied')
            self.assertIsNone(result)

    def set_current_chapter_test(self):
        """
        Test set_current_chapter
        """
        # GIVEN: An instance of BibleImport and a mocked wizard
        importer = BibleImport(MagicMock(), path='.', name='.', filename='')
        importer.wizard = MagicMock()

        # WHEN: Calling set_current_chapter
        importer.set_current_chapter('Book_Name', 'Chapter')

        # THEN: Increment_progress_bar should have been called with a text string
        importer.wizard.increment_progress_bar.assert_called_once_with('Importing Book_Name Chapter...')

    def validate_xml_file_compressed_file_test(self):
        """
        Test that validate_xml_file raises a ValidationError when is_compressed returns True
        """
        # GIVEN: A mocked parse_xml which returns None
        with patch.object(BibleImport, 'is_compressed', return_value=True):
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling is_compressed
            # THEN: ValidationError should be raised, with the message 'Compressed file'
            with self.assertRaises(ValidationError) as context:
                importer.validate_xml_file('file.name', 'xbible')
            self.assertEqual(context.exception.msg, 'Compressed file')

    def validate_xml_file_parse_xml_fails_test(self):
        """
        Test that validate_xml_file raises a ValidationError when parse_xml returns None
        """
        # GIVEN: A mocked parse_xml which returns None
        with patch.object(BibleImport, 'parse_xml', return_value=None), \
                patch.object(BibleImport, 'is_compressed', return_value=False):
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling validate_xml_file
            # THEN: ValidationError should be raised, with the message 'Error when opening file'
            #       the user that an OpenSong bible was found
            with self.assertRaises(ValidationError) as context:
                importer.validate_xml_file('file.name', 'xbible')
            self.assertEqual(context.exception.msg, 'Error when opening file')

    def validate_xml_file_success_test(self):
        """
        Test that validate_xml_file returns True with valid XML
        """
        # GIVEN: Some test data with an OpenSong Bible "bible" root tag
        with patch.object(BibleImport, 'parse_xml', return_value=objectify.fromstring('<bible></bible>')), \
                patch.object(BibleImport, 'is_compressed', return_value=False):
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling validate_xml_file
            result = importer.validate_xml_file('file.name', 'bible')

            # THEN: True should be returned
            self.assertTrue(result)

    def validate_xml_file_opensong_root_test(self):
        """
        Test that validate_xml_file raises a ValidationError with an OpenSong root tag
        """
        # GIVEN: Some test data with an Zefania root tag and an instance of BibleImport
        with patch.object(BibleImport, 'parse_xml', return_value=objectify.fromstring('<bible></bible>')), \
                patch.object(BibleImport, 'is_compressed', return_value=False):
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling validate_xml_file
            # THEN: ValidationError should be raised, and the critical error message box should was called informing
            #       the user that an OpenSong bible was found
            with self.assertRaises(ValidationError) as context:
                importer.validate_xml_file('file.name', 'xbible')
            self.assertEqual(context.exception.msg, 'Invalid xml.')
            self.mocked_critical_error_message_box.assert_called_once_with(
                message='Incorrect Bible file type supplied. This looks like an OpenSong XML bible.')

    def validate_xml_file_osis_root_test(self):
        """
        Test that validate_xml_file raises a ValidationError with an OSIS root tag
        """
        # GIVEN: Some test data with an Zefania root tag and an instance of BibleImport
        with patch.object(BibleImport, 'parse_xml', return_value=objectify.fromstring(
                '<osis xmlns=\'http://www.bibletechnologies.net/2003/OSIS/namespace\'></osis>')), \
                patch.object(BibleImport, 'is_compressed', return_value=False):
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling validate_xml_file
            # THEN: ValidationError should be raised, and the critical error message box should was called informing
            #       the user that an OSIS bible was found
            with self.assertRaises(ValidationError) as context:
                importer.validate_xml_file('file.name', 'xbible')
            self.assertEqual(context.exception.msg, 'Invalid xml.')
            self.mocked_critical_error_message_box.assert_called_once_with(
                message='Incorrect Bible file type supplied. This looks like an OSIS XML bible.')

    def validate_xml_file_zefania_root_test(self):
        """
        Test that validate_xml_file raises a ValidationError with an Zefania root tag
        """
        # GIVEN: Some test data with an Zefania root tag and an instance of BibleImport
        with patch.object(BibleImport, 'parse_xml', return_value=objectify.fromstring('<xmlbible></xmlbible>')), \
                patch.object(BibleImport, 'is_compressed', return_value=False):
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling validate_xml_file
            # THEN: ValidationError should be raised, and the critical error message box should was called informing
            #       the user that an Zefania bible was found
            with self.assertRaises(ValidationError) as context:
                importer.validate_xml_file('file.name', 'xbible')
            self.assertEqual(context.exception.msg, 'Invalid xml.')
            self.mocked_critical_error_message_box.assert_called_once_with(
                message='Incorrect Bible file type supplied. This looks like an Zefania XML bible.')

    def validate_xml_file_unknown_root_test(self):
        """
        Test that validate_xml_file raises a ValidationError with an unknown root tag
        """
        # GIVEN: Some test data with an unknown root tag and an instance of BibleImport
        with patch.object(
                BibleImport, 'parse_xml', return_value=objectify.fromstring('<unknownbible></unknownbible>')), \
                patch.object(BibleImport, 'is_compressed', return_value=False):
            importer = BibleImport(MagicMock(), path='.', name='.', filename='')

            # WHEN: Calling validate_xml_file
            # THEN: ValidationError should be raised, and the critical error message box should was called informing
            #       the user that a unknown xml bible was found
            with self.assertRaises(ValidationError) as context:
                importer.validate_xml_file('file.name', 'xbible')
            self.assertEqual(context.exception.msg, 'Invalid xml.')
            self.mocked_critical_error_message_box.assert_called_once_with(
                message='Incorrect Bible file type supplied. This looks like an unknown type of XML bible.')
