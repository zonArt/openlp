"""
    Package to test the openlp.core.lib package.
"""
import os

from unittest import TestCase
from mock import MagicMock
from openlp.core.lib import Settings

TESTPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))

class TestSettings(TestCase):

    def settings_basic_test(self):
        """
        Test the Settings creation and its usage
        """
        # GIVEN: A new Settings
        settings = Settings()
