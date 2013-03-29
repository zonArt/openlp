"""
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os

from unittest import TestCase
from tempfile import mkstemp
from mock import patch, MagicMock

from openlp.core.lib import Settings
from openlp.plugins.remotes.lib.httpserver import HttpRouter
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


class TestRouter(TestCase):
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
        self.router = HttpRouter()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        os.unlink(self.ini_file)

    def process_http_request_test(self):
        """
        Test the router control functionality
        """
        # GIVEN: A testing set of Routes
        mocked_function = MagicMock()
        test_route = [
            (r'^/stage/api/poll$', mocked_function),
        ]
        self.router.routes = test_route

        # WHEN: called with a poll route
        self.router.process_http_request(u'/stage/api/poll', None)

        # THEN: the function should have been called only once
        assert mocked_function.call_count == 1, \
            u'The mocked function should have been matched and called once.'


        #self.assertFalse()

        # WHEN: We run the function with no input
        #authenticated = check_credentials(u'', u'')

        # THEN: The authentication will fail with an error message
        #self.assertEqual(authenticated, u'Incorrect username or password.',
        #                 u'The return should be a error message string')

        # WHEN: We run the function with the correct input
        #authenticated = check_credentials(u'twinkle', u'mongoose')

        # THEN: The authentication will pass.
        #self.assertEqual(authenticated, None, u'The return should be a None string')



