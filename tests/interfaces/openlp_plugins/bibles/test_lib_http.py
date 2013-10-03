"""
    Package to test the openlp.plugin.bible.lib.https package.
"""

from unittest import TestCase
from mock import MagicMock

from openlp.core.lib import Registry
from openlp.plugins.bibles.lib.http import BGExtract, CWExtract


class TestBibleHTTP(TestCase):

    def setUp(self):
        """
        Set up the Registry
        """
        Registry.create()
        Registry().register('service_list', MagicMock())
        Registry().register('application', MagicMock())

    def bible_gateway_extract_books_test(self):
        """
        Test the Bible Gateway retrieval of book list for NIV bible
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http('NIV')

        # THEN: We should get back a valid service item
        assert len(books) == 66, 'The bible should not have had any books added or removed'

    def bible_gateway_extract_verse_test(self):
        """
        Test the Bible Gateway retrieval of verse list for NIV bible John 3
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        results = handler.get_bible_chapter('NIV', 'John', 3)

        # THEN: We should get back a valid service item
        assert len(results.verse_list) == 36, 'The book of John should not have had any verses added or removed'

    def crosswalk_extract_books_test(self):
        """
        Test Crosswalk retrieval of book list for NIV bible
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = CWExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http('niv')

        # THEN: We should get back a valid service item
        assert len(books) == 66, 'The bible should not have had any books added or removed'

    def crosswalk_extract_verse_test(self):
        """
        Test Crosswalk retrieval of verse list for NIV bible John 3
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = CWExtract()

        # WHEN: The Books list is called
        results = handler.get_bible_chapter('niv', 'john', 3)

        # THEN: We should get back a valid service item
        assert len(results.verse_list) == 36, 'The book of John should not have had any verses added or removed'

