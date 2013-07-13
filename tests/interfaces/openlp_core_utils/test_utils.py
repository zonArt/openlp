"""
Functional tests to test the AppLocation class and related methods.
"""
from unittest import TestCase

from mock import patch
from PyQt4 import QtCore


from openlp.core.utils import is_not_image_file
from tests.utils.constants import TEST_RESOURCES_PATH


class TestUtils(TestCase):
    """
    A test suite to test out various methods around the Utils functions.
    """
    def is_not_image_empty_test(self):
        """
        Test the method handles an empty string
        """
        # Given and empty string
        file_name = ""

        # WHEN testing for it
        result = is_not_image_file(file_name)

        # THEN the result is false
        assert result is True, u'The missing file test should return True'
