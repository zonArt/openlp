"""
This module contains tests for the lib submodule of the Songs plugin.
"""

from unittest import TestCase

from mock import patch

from openlp.plugins.songs.lib import VerseType


class TestVerseType(TestCase):
    """
    This is a test case to test various methods in the VerseType enumeration class.
    """

    def translated_tag_test(self):
        """
        Test that the translated_tag() method returns the correct tags
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the translated_tag() method with a "verse"
            result = VerseType.translated_tag(u'v')

            # THEN: The result should be "V"
            self.assertEqual(result, u'V', u'The result should be "V"')

            # WHEN: We run the translated_tag() method with a "chorus"
            result = VerseType.translated_tag(u'c')

            # THEN: The result should be "C"
            self.assertEqual(result, u'C', u'The result should be "C"')

    def translated_invalid_tag_test(self):
        """
        Test that the translated_tag() method returns the default tag when passed an invalid tag
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the translated_tag() method with an invalid verse type
            result = VerseType.translated_tag(u'z')

            # THEN: The result should be "O"
            self.assertEqual(result, u'O', u'The result should be "O", but was "%s"' % result)

    def translated_invalid_tag_with_specified_default_test(self):
        """
        Test that the translated_tag() method returns the specified default tag when passed an invalid tag
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the translated_tag() method with an invalid verse type and specify a default
            result = VerseType.translated_tag(u'q', VerseType.Bridge)

            # THEN: The result should be "B"
            self.assertEqual(result, u'B', u'The result should be "B", but was "%s"' % result)

