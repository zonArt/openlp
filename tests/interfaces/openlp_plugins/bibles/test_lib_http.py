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
    Package to test the openlp.plugin.bible.lib.https package.
"""
from unittest import TestCase, skip

from openlp.core.common import Registry
from openlp.plugins.bibles.lib.importers.http import BGExtract, CWExtract, BSExtract
from tests.interfaces import MagicMock


class TestBibleHTTP(TestCase):

    def setUp(self):
        """
        Set up the Registry
        """
        Registry.create()
        Registry().register('service_list', MagicMock())
        Registry().register('application', MagicMock())

    def test_bible_gateway_extract_books(self):
        """
        Test the Bible Gateway retrieval of book list for NIV bible
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http('NIV')

        # THEN: We should get back a valid service item
        self.assertEqual(len(books), 66, 'The bible should not have had any books added or removed')
        self.assertEqual(books[0], 'Genesis', 'The first bible book should be Genesis')

    def test_bible_gateway_extract_books_support_redirect(self):
        """
        Test the Bible Gateway retrieval of book list for DN1933 bible with redirect (bug 1251437)
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http('DN1933')

        # THEN: We should get back a valid service item
        self.assertEqual(len(books), 66, 'This bible should have 66 books')

    def test_bible_gateway_extract_verse(self):
        """
        Test the Bible Gateway retrieval of verse list for NIV bible John 3
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        results = handler.get_bible_chapter('NIV', 'John', 3)

        # THEN: We should get back a valid service item
        self.assertEqual(len(results.verse_list), 36,
                         'The book of John should not have had any verses added or removed')

    def test_bible_gateway_extract_verse_nkjv(self):
        """
        Test the Bible Gateway retrieval of verse list for NKJV bible John 3
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        results = handler.get_bible_chapter('NKJV', 'John', 3)

        # THEN: We should get back a valid service item
        self.assertEqual(len(results.verse_list), 36,
                         'The book of John should not have had any verses added or removed')

    def test_crosswalk_extract_books(self):
        """
        Test Crosswalk retrieval of book list for NIV bible
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = CWExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http('niv')

        # THEN: We should get back a valid service item
        self.assertEqual(len(books), 66, 'The bible should not have had any books added or removed')

    def test_crosswalk_extract_verse(self):
        """
        Test Crosswalk retrieval of verse list for NIV bible John 3
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = CWExtract()

        # WHEN: The Books list is called
        results = handler.get_bible_chapter('niv', 'john', 3)

        # THEN: We should get back a valid service item
        self.assertEqual(len(results.verse_list), 36,
                         'The book of John should not have had any verses added or removed')

    def test_bibleserver_get_bibles(self):
        """
        Test getting list of bibles from BibleServer.com
        """
        # GIVEN: A new Bible Server extraction class
        handler = BSExtract()

        # WHEN: downloading bible list from bibleserver
        bibles = handler.get_bibles_from_http()

        # THEN: The list should not be None, and some known bibles should be there
        self.assertIsNotNone(bibles)
        self.assertIn(('New Int. Readers Version', 'NIRV', 'en'), bibles)
        self.assertIn(('Священное Писание, Восточный перевод', 'CARS', 'ru'), bibles)

    def test_biblegateway_get_bibles(self):
        """
        Test getting list of bibles from BibleGateway.com
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: downloading bible list from Crosswalk
        bibles = handler.get_bibles_from_http()

        # THEN: The list should not be None, and some known bibles should be there
        self.assertIsNotNone(bibles)
        self.assertIn(('Holman Christian Standard Bible (HCSB)', 'HCSB', 'en'), bibles)

    def test_crosswalk_get_bibles(self):
        """
        Test getting list of bibles from Crosswalk.com
        """
        # GIVEN: A new Crosswalk extraction class
        handler = CWExtract()

        # WHEN: downloading bible list from Crosswalk
        bibles = handler.get_bibles_from_http()

        # THEN: The list should not be None, and some known bibles should be there
        self.assertIsNotNone(bibles)
        self.assertIn(('Giovanni Diodati 1649 (Italian)', 'gdb', 'it'), bibles)
