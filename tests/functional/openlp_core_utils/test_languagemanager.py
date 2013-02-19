"""
Functional tests for the Language Manager.
"""

from unittest import TestCase

from mock import patch

from openlp.core.utils import LanguageManager

class TestLanguageManager(TestCase):
    """
    A test suite to test out various methods around the LanguageManager class.
    """
    def get_translator_linux_test(self):
        """
        """
        with patch(u'openlp.core.utils.sys.platform') as mocked_platform:
            # GIVEN: We are on linux.
            mocked_platform.return_value = u'linux2'

            app_translator, default_translator = LanguageManager.get_translator('en')

            assert not app_translator.isEmpty(), u'The application translator should not be empty'
            assert not default_translator.isEmpty(), u'The default translator should not be empty'

