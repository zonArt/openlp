"""
Functional tests to test the AppLocation class and related methods.
"""
from unittest import TestCase

from mock import patch

from openlp.core.utils import get_filesystem_encoding

class TestUtils(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """
    def get_filesystem_encoding_test(self):
        """
        Test the get_filesystem_encoding() function
        """
        assert False, u'This test needs to be written'

