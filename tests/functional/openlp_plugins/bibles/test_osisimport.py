# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
from openlp.plugins.bibles.lib.osis import OSISBible
from openlp.plugins.bibles.lib.db import BibleDB

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'resources', 'bibles'))


class TestOsisImport(TestCase):
    """
    Test the functions in the :mod:`osisimport` module.
    """

    def setUp(self):
        self.registry_patcher = patch('openlp.plugins.bibles.lib.db.Registry')
        self.registry_patcher.start()
        self.manager_patcher = patch('openlp.plugins.bibles.lib.db.Manager')
        self.manager_patcher.start()

    def tearDown(self):
        self.registry_patcher.stop()
        self.manager_patcher.stop()

    def create_importer_test(self):
        """
        Test creating an instance of the OSIS file importer
        """
        # GIVEN: A mocked out "manager"
        mocked_manager = MagicMock()

        # WHEN: An importer object is created
        importer = OSISBible(mocked_manager, path='.', name='.', filename='')

        # THEN: The importer should be an instance of BibleDB
        self.assertIsInstance(importer, BibleDB)

    def file_import_nested_tags_test(self):
        """
        Test the actual import of OSIS Bible file, with nested chapter and verse tags
        """
        # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
        #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
        result_file = open(os.path.join(TEST_PATH, 'dk1933.json'), 'rb')
        test_data = json.loads(result_file.read().decode())
        bible_file = 'osis-dk1933.xml'
        with patch('openlp.plugins.bibles.lib.osis.OSISBible.application'):
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

    def file_import_mixed_tags_test(self):
        """
        Test the actual import of OSIS Bible file, with chapter tags containing milestone verse tags.
        """
        # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
        #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
        result_file = open(os.path.join(TEST_PATH, 'kjv.json'), 'rb')
        test_data = json.loads(result_file.read().decode())
        bible_file = 'osis-kjv.xml'
        with patch('openlp.plugins.bibles.lib.osis.OSISBible.application'):
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

    def file_import_milestone_tags_test(self):
        """
        Test the actual import of OSIS Bible file, with milestone chapter and verse tags.
        """
        # GIVEN: Test files with a mocked out "manager", "import_wizard", and mocked functions
        #        get_book_ref_id_by_name, create_verse, create_book, session and get_language.
        result_file = open(os.path.join(TEST_PATH, 'web.json'), 'rb')
        test_data = json.loads(result_file.read().decode())
        bible_file = 'osis-web.xml'
        with patch('openlp.plugins.bibles.lib.osis.OSISBible.application'):
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
            print(importer.create_verse.call_list())
            for verse_tag, verse_text in test_data['verses']:
                importer.create_verse.assert_any_call(importer.create_book().id, '1', verse_tag, verse_text)
