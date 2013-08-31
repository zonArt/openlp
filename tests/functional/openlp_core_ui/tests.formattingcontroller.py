"""
Package to test the openlp.core.ui.formattingtagscontroller package.
"""
from unittest import TestCase

from mock import MagicMock, patch

from openlp.core.ui.formattingtagform import FormattingTagForm

class TestFormattingTagForm(TestCase):

    def strip_test(self):
        """
        Test that the _strip strips the correct chars
        """

        # GIVEN: An instance of the Formatting Tag Form and a string containing a tag
        form = FormattingTagForm()
        tag = u'{tag}'

        # WHEN: Calling _strip
        result = form._strip(tag)

        # THEN: The tag should be returned with the wrappers removed.
        self.assertEqual(result, u'tag', u'FormattingTagForm._strip should return u\'tag\' when called with u\'{tag}\'')