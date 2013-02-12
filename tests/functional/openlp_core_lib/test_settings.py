"""
    Package to test the openlp.core.lib package.
"""
import os

from unittest import TestCase
from openlp.core.lib import Settings

from PyQt4 import QtGui, QtTest

TESTPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))


class TestSettings(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        self.application = QtGui.QApplication([])
        self.application.setOrganizationName(u'OpenLP-tests')
        self.application.setOrganizationDomain(u'openlp.org')
        Settings()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        try:
            os.remove(Settings().fileName())
        except OSError:
            pass

    def settings_basic_test(self):
        """
        Test the Settings creation and its default usage
        """
        # GIVEN: A new Settings setup

        # WHEN reading a setting for the first time
        default_value = Settings().value(u'general/has run wizard')

        # THEN the default value is returned
        assert default_value is False, u'The default value defined has not been returned'

        # WHEN a new value is saved into config
        Settings().setValue(u'general/has run wizard', True)

        # THEN the new value is returned when re-read
        assert Settings().value(u'general/has run wizard') is True, u'The saved value has not been returned'

    def settings_override_test(self):
        """
        Test the Settings creation and its override usage
        """
        # GIVEN: an override for the settings
        screen_settings = {
            u'test/extend': u'very wide',
        }
        Settings().extend_default_settings(screen_settings)

        # WHEN reading a setting for the first time
        extend = Settings().value(u'test/extend')

        # THEN the default value is returned
        assert extend == u'very wide', u'The default value defined is returned'

        # WHEN a new value is saved into config
        Settings().setValue(u'test/extend', u'very short')

        # THEN the new value is returned when re-read
        assert Settings().value(u'test/extend') == u'very short', u'The saved value is returned'

    def settings_override_with_group_test(self):
        """
        Test the Settings creation and its override usage - with groups
        """
        # GIVEN: an override for the settings
        screen_settings = {
            u'test/extend': u'very wide',
        }
        Settings.extend_default_settings(screen_settings)

        # WHEN reading a setting for the first time
        settings = Settings()
        settings.beginGroup(u'test')
        extend = settings.value(u'extend')

        # THEN the default value is returned
        assert extend == u'very wide', u'The default value defined has not been returned'

        # WHEN a new value is saved into config
        Settings().setValue(u'test/extend', u'very short')

        # THEN the new value is returned when re-read
        assert Settings().value(u'test/extend') == u'very short', u'The saved value has not been returned'
