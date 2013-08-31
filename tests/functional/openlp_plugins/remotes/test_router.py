"""
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os

from unittest import TestCase
from tempfile import mkstemp
from mock import MagicMock

from openlp.core.lib import Settings
from openlp.plugins.remotes.lib.httpserver import HttpRouter, fetch_password, make_sha_hash
from PyQt4 import QtGui

__default_settings__ = {
    'remotes/twelve hour': True,
    'remotes/port': 4316,
    'remotes/https port': 4317,
    'remotes/https enabled': False,
    'remotes/user id': 'openlp',
    'remotes/password': 'password',
    'remotes/authentication enabled': False,
    'remotes/ip address': '0.0.0.0'
}


class TestRouter(TestCase):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Create the UI
        """
        fd, self.ini_file = mkstemp('.ini')
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

    def fetch_password_unknown_test(self):
        """
        Test the fetch password code with an unknown userid
        """
        # GIVEN: A default configuration
        # WHEN: called with the defined userid
        password = fetch_password('itwinkle')

        # THEN: the function should return None
        self.assertEqual(password, None, 'The result for fetch_password should be None')

    def fetch_password_known_test(self):
        """
        Test the fetch password code with the defined userid
        """
        # GIVEN: A default configuration
        # WHEN: called with the defined userid
        password = fetch_password('openlp')
        required_password = make_sha_hash('password')

        # THEN: the function should return the correct password
        self.assertEqual(password, required_password, 'The result for fetch_password should be the defined password')

    def sha_password_encrypter_test(self):
        """
        Test hash password function
        """
        # GIVEN: A default configuration
        # WHEN: called with the defined userid
        required_password = make_sha_hash('password')
        test_value = '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'

        # THEN: the function should return the correct password
        self.assertEqual(required_password, test_value,
            'The result for make_sha_hash should return the correct encrypted password')

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
        self.router.process_http_request('/stage/api/poll', None)

        # THEN: the function should have been called only once
        assert mocked_function.call_count == 1, \
            'The mocked function should have been matched and called once.'
