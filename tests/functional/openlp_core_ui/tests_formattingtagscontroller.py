"""
Package to test the openlp.core.ui.formattingtagscontroller package.
"""
from unittest import TestCase

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

    def test_end_tag_changed_processes_correctly(self):
        """
        Test that the end html tags are generated correctly
        """
        # GIVEN: A list of start , end tags and error messages
        tests = []
        test = {'start': '<b>', 'end': None, 'gen': '</b>', 'valid': None}
        tests.append(test)
        test = {'start': '<i>', 'end': '</i>', 'gen': None, 'valid': None}
        tests.append(test)
        test = {'start': '<b>', 'end': '</i>', 'gen': None,
                'valid': 'End tag </b> does not match end tag for start tag <b>'}
        tests.append(test)

        # WHEN: Testing each one of them in turn
        for test in tests:
            error, result = self.services.end_tag_changed(test['start'], test['end'])

            # THEN: The result should match the predetermined value.
            self.assertTrue(result == test['gen'],
                'Function should handle end tag correctly : %s and %s for %s ' % (test['gen'], result, test['start']))
            self.assertTrue(error == test['valid'],
                'Function should not generate unexpected error messages : %s ' % error)

    def test_start_tag_changed_processes_correctly(self):
        """
        Test that the end html tags are generated correctly
        """
        # GIVEN: A list of start , end tags and error messages
        tests = []
        test = {'start': '<b>', 'end': '', 'gen': '</b>', 'valid': None}
        tests.append(test)
        test = {'start': '<i>', 'end': '</i>', 'gen': None, 'valid': None}
        tests.append(test)
        test = {'start': 'superfly', 'end': '', 'gen': None, 'valid': 'Start tag superfly is not valid HTML'}
        tests.append(test)

        # WHEN: Testing each one of them in turn
        for test in tests:
            error, result = self.services.start_tag_changed(test['start'], test['end'])

            # THEN: The result should match the predetermined value.
            self.assertTrue(result == test['gen'],
                'Function should handle end tag correctly : %s and %s ' % (test['gen'], result))
            self.assertTrue(error == test['valid'],
                'Function should not generate unexpected error messages : %s ' % error)

    def test_start_html_to_end_html(self):
        """
        Test that the end html tags are generated correctly
        """
        # GIVEN: A list of valid and invalid tags
        tests = {'<b>': '</b>', '<i>': '</i>', 'superfly': '', '<HTML START>': None,
                 '<span style="-webkit-text-fill-color:red">': '</span>'}

        # WHEN: Testing each one of them
        for test1, test2 in tests.items():
            result = self.services.start_html_to_end_html(test1)

            # THEN: The result should match the predetermined value.
            self.assertTrue(result == test2, 'Calculated end tag should be valid: %s and %s = %s'
                % (test1, test2, result))