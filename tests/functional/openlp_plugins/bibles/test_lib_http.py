"""
    Package to test the openlp.plugin.bible.lib.https package.
"""

from unittest import TestCase
from mock import MagicMock, patch

from openlp.core.lib import Registry
from openlp.plugins.bibles.lib.http import BGExtract


class TestBibleHTTP(TestCase):

    def setUp(self):
        """
        Set up the Registry
        """
        Registry.create()
        Registry().register(u'service_list', MagicMock())
        Registry().register(u'application', MagicMock())

    def bible_gateway_extract_test(self):
        """
        Test the Bible Gateway retrieval of book list for NIV
        """
        # GIVEN: A new Bible Gateway extraction class
        handler = BGExtract()

        # WHEN: The Books list is called
        books = handler.get_books_from_http(u'NIV')

        # THEN: We should get back a valid service item
        assert len(books) == 66, u'The bible should not have had its lenght changed'
