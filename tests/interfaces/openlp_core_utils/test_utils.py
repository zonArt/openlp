"""
Functional tests to test the AppLocation class and related methods.
"""
import os
from unittest import TestCase

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
        assert result is True, 'The missing file test should return True'

    def is_not_image_with_image_file_test(self):
        """
        Test the method handles an image file
        """
        # Given and empty string
        file_name = os.path.join(TEST_RESOURCES_PATH, 'church.jpg')

        # WHEN testing for it
        result = is_not_image_file(file_name)

        # THEN the result is false
        assert result is False, 'The file is present so the test should return False'

    def is_not_image_with_none_image_file_test(self):
        """
        Test the method handles a non image file
        """
        # Given and empty string
        file_name = os.path.join(TEST_RESOURCES_PATH, 'serviceitem_custom_1.osj')

        # WHEN testing for it
        result = is_not_image_file(file_name)

        # THEN the result is false
        assert result is True, 'The file is not an image file so the test should return True'