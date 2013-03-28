"""
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os
from unittest import TestCase
from tempfile import mkstemp
from mock import patch, MagicMock

from openlp.core.lib import Settings
from openlp.plugins.remotes.lib.httpauth import check_credentials, check_authentication
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

SESSION_KEY = '_cp_openlp'


class TestAuth(TestCase):
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
        Test the Authentication check routine with credentials.
        """
        # GIVEN: A user and password in settings
        Settings().setValue(u'remotes/user id', u'twinkle')
        Settings().setValue(u'remotes/password', u'mongoose')

        # WHEN: We run the function with no input
        authenticated = check_credentials(u'', u'')

        # THEN: The authentication will fail with an error message
        self.assertEqual(authenticated, u'Incorrect username or password.',
                         u'The return should be a error message string')

        # WHEN: We run the function with the correct input
        authenticated = check_credentials(u'twinkle', u'mongoose')

        # THEN: The authentication will pass.
        self.assertEqual(authenticated, None, u'The return should be a None string')

    def check_auth_inactive_test(self):
        """
        Test the Authentication check routine when inactive.
        """
        # GIVEN: A access which is secure
        Settings().setValue(u'remotes/authentication enabled', False)

        # WHEN: We run the function with no input
        with patch(u'cherrypy.request.config'):
            authenticated = check_authentication(None, None)

            # THEN: The authentication will fail with an error message
            self.assertEqual(authenticated, None, u'The authentication should return None as not required')
