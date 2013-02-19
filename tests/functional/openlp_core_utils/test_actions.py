"""
Package to test the openlp.core.utils.actions package.
"""
from unittest import TestCase

from mock import patch

from openlp.core.utils import ActionList


class TestActionList(TestCase):

    def setUp(self):
        """
        Prepare the tests
        """
        self.action_list = ActionList.get_instance()

    def test_(self):
        """
        """
        pass
