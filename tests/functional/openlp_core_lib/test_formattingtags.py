"""
Package to test the openlp.core.lib.formattingtags package.
"""
import copy
from unittest import TestCase

from mock import patch

from openlp.core.lib import FormattingTags


TAG = {
    'end tag': '{/aa}',
    'start html': '<span>',
    'start tag': '{aa}',
    'protected': False,
    'end html': '</span>',
    'desc': 'name'
}


class TestFormattingTags(TestCase):

    def tearDown(self):
        """
        Clean up the FormattingTags class.
        """
        FormattingTags.html_expands = []

    def get_html_tags_no_user_tags_test(self):
        """
        Test the FormattingTags class' get_html_tags static method.
        """
        with patch('openlp.core.lib.translate') as mocked_translate, \
                patch('openlp.core.lib.settings') as mocked_settings, \
                patch('openlp.core.lib.formattingtags.json') as mocked_json:
            # GIVEN: Our mocked modules and functions.
            mocked_translate.side_effect = lambda module, string_to_translate, comment: string_to_translate
            mocked_settings.value.return_value = ''
            mocked_json.load.return_value = []

            # WHEN: Get the display tags.
            FormattingTags.load_tags()
            old_tags_list = copy.deepcopy(FormattingTags.get_html_tags())
            FormattingTags.load_tags()
            new_tags_list = FormattingTags.get_html_tags()

            # THEN: Lists should be identical.
            assert old_tags_list == new_tags_list, 'The formatting tag lists should be identical.'

    def get_html_tags_with_user_tags_test(self):
        """
        FormattingTags class - test the get_html_tags(), add_html_tags() and remove_html_tag() methods.
        """
        with patch('openlp.core.lib.translate') as mocked_translate, \
                patch('openlp.core.lib.settings') as mocked_settings, \
                patch('openlp.core.lib.formattingtags.json') as mocked_json:
            # GIVEN: Our mocked modules and functions.
            mocked_translate.side_effect = lambda module, string_to_translate: string_to_translate
            mocked_settings.value.return_value = ''
            mocked_json.loads.side_effect = [[], [TAG]]

            # WHEN: Get the display tags.
            FormattingTags.load_tags()
            old_tags_list = copy.deepcopy(FormattingTags.get_html_tags())

            # WHEN: Add our tag and get the tags again.
            FormattingTags.load_tags()
            FormattingTags.add_html_tags([TAG])
            new_tags_list = copy.deepcopy(FormattingTags.get_html_tags())

            # THEN: Lists should not be identical.
            assert old_tags_list != new_tags_list, 'The lists should be different.'

            # THEN: Added tag and last tag should be the same.
            new_tag = new_tags_list.pop()
            assert TAG == new_tag, 'Tags should be identical.'

            # WHEN: Remove the new tag.
            FormattingTags.remove_html_tag(len(new_tags_list))

            # THEN: The lists should now be identical.
            assert old_tags_list == FormattingTags.get_html_tags(), 'The lists should be identical.'

