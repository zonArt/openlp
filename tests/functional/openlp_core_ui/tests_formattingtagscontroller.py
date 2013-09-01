"""
Package to test the openlp.core.ui.formattingtagscontroller package.
"""
from unittest import TestCase

from mock import MagicMock, patch

from openlp.core.ui import FormattingTagController


class TestFormattingTagController(TestCase):

    def setUp(self):
        self.services = FormattingTagController()

    def test_strip(self):
        """
        Test that the _strip strips the correct chars
        """

        # GIVEN: An instance of the Formatting Tag Form and a string containing a tag
        tag = u'{tag}'

        # WHEN: Calling _strip
        result = self.services._strip(tag)

        # THEN: The tag should be returned with the wrappers removed.
        self.assertEqual(result, u'tag', u'FormattingTagForm._strip should return u\'tag\' when called with u\'{tag}\'')