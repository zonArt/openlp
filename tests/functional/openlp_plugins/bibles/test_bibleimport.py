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

from openlp.core.common.languages import Language
from openlp.core.lib.exceptions import ValidationError
from openlp.plugins.bibles.lib.bibleimport import BibleImport
from openlp.plugins.bibles.lib.db import BibleDB
from tests.functional import ANY, MagicMock, patch


class TestBibleImport(TestCase):
    """
    Test the functions in the :mod:`bibleimport` module.
    """

    def setUp(self):
        test_file = BytesIO(
            b'<?xml version="1.0" encoding="UTF-8" ?>\n'
            b'<root>\n'
            b'    <data><div>Test<p>data</p><a>to</a>keep</div></data>\n'
            b'    <data><unsupported>Test<x>data</x><y>to</y>discard</unsupported></data>\n'
            b'</root>'
        )
        self.file_patcher = patch('builtins.open', return_value=test_file)
        self.addCleanup(self.file_patcher.stop)
        self.file_patcher.start()
        self.log_patcher = patch('openlp.plugins.bibles.lib.bibleimport.log')
        self.addCleanup(self.log_patcher.stop)
        self.mock_log = self.log_patcher.start()
        self.setup_patcher = patch('openlp.plugins.bibles.lib.db.BibleDB._setup')
        self.addCleanup(self.setup_patcher.stop)
        self.setup_patcher.start()

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

    def get_language_id_language_found_test(self):
        """
        Test get_language_id() when called with a name found in the languages list
        """
        # GIVEN: A mocked languages.get_language which returns language and an instance of BibleImport
        with patch('openlp.core.common.languages.get_language', return_value=Language(30, 'English', 'en')) \
                as mocked_languages_get_language, \
                patch('openlp.plugins.bibles.lib.db.BibleDB.get_language') as mocked_db_get_language:
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
                patch('openlp.plugins.bibles.lib.db.BibleDB.get_language', return_value=20) as mocked_db_get_language:
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
                patch('openlp.plugins.bibles.lib.db.BibleDB.get_language', return_value=40) as mocked_db_get_language:
            self.mock_log.error.reset_mock()
            instance = BibleImport(MagicMock())
            instance.save_meta = MagicMock()

            # WHEN: Calling get_language_id() with a language name and bible name
            result = instance.get_language_id('English', 'KJV')

            # THEN: The id of the language returned from BibleDB.get_language should be returned
            mocked_languages_get_language.assert_called_once_with('English')
            mocked_db_get_language.assert_called_once_with('KJV')
            self.assertFalse(self.mock_log.error.called)
            instance.save_meta.assert_called_once_with('language_id', 40)
            self.assertEqual(result, 40)

    def get_language_id_user_choice_rejected_test(self):
        """
        Test get_language_id() when the language is not found and the user rejects the dilaog box
        """
        # GIVEN: A mocked languages.get_language which returns None a mocked BibleDB.get_language which returns a
        #       language id.
        with patch('openlp.core.common.languages.get_language', return_value=None) as mocked_languages_get_language, \
                patch('openlp.plugins.bibles.lib.db.BibleDB.get_language', return_value=None) as mocked_db_get_language:
            self.mock_log.error.reset_mock()
            instance = BibleImport(MagicMock())
            instance.save_meta = MagicMock()

            # WHEN: Calling get_language_id() with a language name and bible name
            result = instance.get_language_id('Qwerty', 'KJV')

            # THEN: None should be returned and an error should be logged
            mocked_languages_get_language.assert_called_once_with('Qwerty')
            mocked_db_get_language.assert_called_once_with('KJV')
            self.mock_log.error.assert_called_once_with('Language detection failed when importing from "KJV". '
                                                        'User aborted language selection.')
            self.assertFalse(instance.save_meta.called)
            self.assertIsNone(result)

    def parse_xml_etree_test(self):
        """
        Test BibleImport.parse_xml() when called with the use_objectify default value
        """
        # GIVEN: A sample "file" to parse
        # WHEN: Calling parse_xml
        result = BibleImport.parse_xml('file.tst')

        # THEN: The result returned should contain the correct data, and should be an instance of eetree_Element
        self.assertEqual(etree.tostring(result),
                         b'<root>\n    <data><div>Test<p>data</p><a>to</a>keep</div></data>\n'
                         b'    <data><unsupported>Test<x>data</x><y>to</y>discard</unsupported></data>\n</root>')
        self.assertIsInstance(result, etree._Element)

    def parse_xml_etree_use_objectify_test(self):
        """
        Test BibleImport.parse_xml() when called with use_objectify set to True
        """
        # GIVEN: A sample "file" to parse
        # WHEN: Calling parse_xml
        result = BibleImport.parse_xml('file.tst', use_objectify=True)

        # THEN: The result returned should contain the correct data, and should be an instance of ObjectifiedElement
        self.assertEqual(etree.tostring(result),
                         b'<root><data><div>Test<p>data</p><a>to</a>keep</div></data>'
                         b'<data><unsupported>Test<x>data</x><y>to</y>discard</unsupported></data></root>')
        self.assertIsInstance(result, objectify.ObjectifiedElement)

    def parse_xml_elements_test(self):
        """
        Test BibleImport.parse_xml() when given a tuple of elements to remove
        """
        # GIVEN: A tuple of elements to remove
        elements = ('unsupported', 'x', 'y')

        # WHEN: Calling parse_xml, with a test file
        result = BibleImport.parse_xml('file.tst', elements=elements)

        # THEN: The result returned should contain the correct data
        self.assertEqual(etree.tostring(result),
                         b'<root>\n    <data><div>Test<p>data</p><a>to</a>keep</div></data>\n    <data/>\n</root>')

    def parse_xml_tags_test(self):
        """
        Test BibleImport.parse_xml() when given a tuple of tags to remove
        """
        # GIVEN: A tuple of tags to remove
        tags = ('div', 'p', 'a')

        # WHEN: Calling parse_xml, with a test file
        result = BibleImport.parse_xml('file.tst', tags=tags)

        # THEN: The result returned should contain the correct data
        self.assertEqual(etree.tostring(result), b'<root>\n    <data>Testdatatokeep</data>\n    <data><unsupported>Test'
                                                 b'<x>data</x><y>to</y>discard</unsupported></data>\n</root>')

    def parse_xml_elements_tags_test(self):
        """
        Test BibleImport.parse_xml() when given a tuple of elements and of tags to remove
        """
        # GIVEN: A tuple of elements and of tags to remove
        elements = ('unsupported', 'x', 'y')
        tags = ('div', 'p', 'a')

        # WHEN: Calling parse_xml, with a test file
        result = BibleImport.parse_xml('file.tst', elements=elements, tags=tags)

        # THEN: The result returned should contain the correct data
        self.assertEqual(etree.tostring(result), b'<root>\n    <data>Testdatatokeep</data>\n    <data/>\n</root>')
