"""
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os
from unittest import TestCase
from tempfile import mkstemp
from mock import patch

from openlp.core.lib import Settings
from openlp.plugins.remotes.lib.httpauth import check_credentials
from PyQt4 import QtGui

__default_settings__ = {
    u'remotes/twelve hour': True,
    u'remotes/port': 4316,
    u'remotes/https port': 4317,
    u'remotes/https enabled': False,
    u'remotes/user id': u'openlp',
    u'remotes/password': u'password',
    u'remotes/authentication enabled': False,
    u'remotes/ip address': u'0.0.0.0'
}


class TestLib(TestCase):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Create the UI
        """
        fd, self.ini_file = mkstemp(u'.ini')
        Settings().set_filename(self.ini_file)
        self.application = QtGui.QApplication.instance()
        Settings().extend_default_settings(__default_settings__)

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        os.unlink(self.ini_file)
        os.unlink(Settings().fileName())

    def check_credentials_test(self):
        """
        Test the clean_string() function
        """
        # GIVEN: A user and password
        Settings().setValue(u'remotes/user id', u'twinkle')
        Settings().setValue(u'remotes/password', u'mongoose')

        # WHEN: We run the string through the function
        authenticated = check_credentials(u'', u'')

        # THEN: The string should be cleaned up and lower-cased
        self.assertEqual(authenticated, u'Incorrect username or password.',
                         u'The return should be a error message string')

        # WHEN: We run the string through the function
        authenticated = check_credentials(u'twinkle', u'mongoose')

        # THEN: The string should be cleaned up and lower-cased
        self.assertEqual(authenticated, None, u'The return should be a None string')
