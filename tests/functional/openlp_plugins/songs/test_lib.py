"""
This module contains tests for the lib submodule of the Songs plugin.
"""

from unittest import TestCase

from mock import patch

from openlp.plugins.songs.lib import VerseType, clean_string, clean_title


class TestLib(TestCase):
    """
    Test the functions in the :mod:`lib` module.
    """
    def clean_string_test(self):
        """
        Test the clean_string() function
        """
        # GIVEN: A "dirty" string
        dirty_string = u'Ain\'t gonna   find\t you there.'

        # WHEN: We run the string through the function
        result = clean_string(dirty_string)

        # THEN: The string should be cleaned up and lower-cased
        self.assertEqual(result, u'aint gonna find you there ', u'The string should be cleaned up properly')

    def clean_title_test(self):
        """
        Test the clean_title() function
        """
        # GIVEN: A "dirty" string
        dirty_string = u'This\u0000 is a\u0014 dirty \u007Fstring\u009F'

        # WHEN: We run the string through the function
        result = clean_title(dirty_string)

        # THEN: The string should be cleaned up
        self.assertEqual(result, u'This is a dirty string', u'The title should be cleaned up properly: "%s"' % result)


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

    def translated_invalid_tag_with_invalid_default_test(self):
        """
        Test that the translated_tag() method returns a sane default tag when passed an invalid default
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the translated_tag() method with an invalid verse type and an invalid default
            result = VerseType.translated_tag(u'q', 29)

            # THEN: The result should be "O"
            self.assertEqual(result, u'O', u'The result should be "O", but was "%s"' % result)

    def translated_name_test(self):
        """
        Test that the translated_name() method returns the correct name
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the translated_name() method with a "verse"
            result = VerseType.translated_name(u'v')

            # THEN: The result should be "Verse"
            self.assertEqual(result, u'Verse', u'The result should be "Verse"')

            # WHEN: We run the translated_name() method with a "chorus"
            result = VerseType.translated_name(u'c')

            # THEN: The result should be "Chorus"
            self.assertEqual(result, u'Chorus', u'The result should be "Chorus"')

    def translated_invalid_name_test(self):
        """
        Test that the translated_name() method returns the default name when passed an invalid tag
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the translated_name() method with an invalid verse type
            result = VerseType.translated_name(u'z')

            # THEN: The result should be "Other"
            self.assertEqual(result, u'Other', u'The result should be "Other", but was "%s"' % result)

    def translated_invalid_name_with_specified_default_test(self):
        """
        Test that the translated_name() method returns the specified default name when passed an invalid tag
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the translated_name() method with an invalid verse type and specify a default
            result = VerseType.translated_name(u'q', VerseType.Bridge)

            # THEN: The result should be "Bridge"
            self.assertEqual(result, u'Bridge', u'The result should be "Bridge", but was "%s"' % result)

    def translated_invalid_name_with_invalid_default_test(self):
        """
        Test that the translated_name() method returns the specified default tag when passed an invalid tag
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the translated_name() method with an invalid verse type and specify an invalid default
            result = VerseType.translated_name(u'q', 29)

            # THEN: The result should be "Other"
            self.assertEqual(result, u'Other', u'The result should be "Other", but was "%s"' % result)

    def from_tag_test(self):
        """
        Test that the from_tag() method returns the correct VerseType.
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the from_tag() method with a valid verse type, we get the name back
            result = VerseType.from_tag(u'v')

            # THEN: The result should be VerseType.Verse
            self.assertEqual(result, VerseType.Verse, u'The result should be VerseType.Verse, but was "%s"' % result)

    def from_tag_with_invalid_tag_test(self):
        """
        Test that the from_tag() method returns the default VerseType when it is passed an invalid tag.
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the from_tag() method with a valid verse type, we get the name back
            result = VerseType.from_tag(u'w')

            # THEN: The result should be VerseType.Other
            self.assertEqual(result, VerseType.Other, u'The result should be VerseType.Other, but was "%s"' % result)

    def from_tag_with_specified_default_test(self):
        """
        Test that the from_tag() method returns the specified default when passed an invalid tag.
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the from_tag() method with an invalid verse type, we get the specified default back
            result = VerseType.from_tag(u'x', VerseType.Chorus)

            # THEN: The result should be VerseType.Chorus
            self.assertEqual(result, VerseType.Chorus, u'The result should be VerseType.Chorus, but was "%s"' % result)

    def from_tag_with_invalid_default_test(self):
        """
        Test that the from_tag() method returns a sane default when passed an invalid tag and an invalid default.
        """
        # GIVEN: A mocked out translate() function that just returns what it was given
        with patch(u'openlp.plugins.songs.lib.translate') as mocked_translate:
            mocked_translate.side_effect = lambda x, y: y

            # WHEN: We run the from_tag() method with an invalid verse type, we get the specified default back
            result = VerseType.from_tag(u'm', 29)

            # THEN: The result should be VerseType.Other
            self.assertEqual(result, VerseType.Other, u'The result should be VerseType.Other, but was "%s"' % result)
