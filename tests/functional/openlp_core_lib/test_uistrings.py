"""
Package to test the openlp.core.lib.uistrings package.
"""

from unittest import TestCase

from openlp.core.lib import UiStrings


class TestUiStrings(TestCase):

    def check_same_instance_test(self):
        """
        Test the UiStrings class - we always should have only one instance of the UiStrings class.
        """
        # WHEN: Create two instances of the UiStrings class.
        first_instance = UiStrings()
        second_instance = UiStrings()

        # THEN: Check if the instances are the same.
        assert first_instance is second_instance, "They should be the same instance!"


