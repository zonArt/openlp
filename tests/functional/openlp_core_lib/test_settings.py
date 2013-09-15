"""
    Package to test the openlp.core.lib.settings package.
"""
import os
from unittest import TestCase
from tempfile import mkstemp

from openlp.core.lib import Settings

from PyQt4 import QtGui


class TestSettings(TestCase):
    """
    Test the functions in the Settings module
    """
    def setUp(self):
        """
        Create the UI
        """
        fd, self.ini_file = mkstemp('.ini')
        Settings().set_filename(self.ini_file)
        self.application = QtGui.QApplication.instance()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        os.unlink(self.ini_file)
        os.unlink(Settings().fileName())

    def settings_basic_test(self):
        """
        Test the Settings creation and its default usage
        """
        # GIVEN: A new Settings setup

        # WHEN reading a setting for the first time
        default_value = Settings().value('core/has run wizard')

        # THEN the default value is returned
        assert default_value is False, 'The default value should be False'

        # WHEN a new value is saved into config
        Settings().setValue('core/has run wizard', True)

        # THEN the new value is returned when re-read
        assert Settings().value('core/has run wizard') is True, 'The saved value should have been returned'

    def settings_override_test(self):
        """
        Test the Settings creation and its override usage
        """
        # GIVEN: an override for the settings
        screen_settings = {
            'test/extend': 'very wide',
        }
        Settings().extend_default_settings(screen_settings)

        # WHEN reading a setting for the first time
        extend = Settings().value('test/extend')

        # THEN the default value is returned
        assert extend == 'very wide', 'The default value of "very wide" should be returned'

        # WHEN a new value is saved into config
        Settings().setValue('test/extend', 'very short')

        # THEN the new value is returned when re-read
        assert Settings().value('test/extend') == 'very short', 'The saved value should be returned'

    def settings_override_with_group_test(self):
        """
        Test the Settings creation and its override usage - with groups
        """
        # GIVEN: an override for the settings
        screen_settings = {
            'test/extend': 'very wide',
        }
        Settings.extend_default_settings(screen_settings)

        # WHEN reading a setting for the first time
        settings = Settings()
        settings.beginGroup('test')
        extend = settings.value('extend')

        # THEN the default value is returned
        assert extend == 'very wide', 'The default value defined should be returned'

        # WHEN a new value is saved into config
        Settings().setValue('test/extend', 'very short')

        # THEN the new value is returned when re-read
        assert Settings().value('test/extend') == 'very short', 'The saved value should be returned'
