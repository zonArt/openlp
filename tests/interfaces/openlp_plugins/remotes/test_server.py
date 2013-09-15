"""
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os

from unittest import TestCase
from tempfile import mkstemp
from mock import MagicMock
import urllib.request, urllib.error, urllib.parse
import cherrypy

from bs4 import BeautifulSoup

from openlp.core.lib import Settings
from openlp.plugins.remotes.lib.httpserver import HttpServer
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
        self.server = HttpServer()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        os.unlink(self.ini_file)
        self.server.close()

    def start_server(self):
        """
        Common function to start server then mock out the router.  CherryPy crashes if you mock before you start
        """
        self.server.start_server()
        self.server.router = MagicMock()
        self.server.router.process_http_request = process_http_request

    def start_default_server_test(self):
        """
        Test the default server serves the correct initial page
        """
        # GIVEN: A default configuration
        Settings().setValue('remotes/authentication enabled', False)
        self.start_server()

        # WHEN: called the route location
        code, page = call_remote_server('http://localhost:4316')

        # THEN: default title will be returned
        self.assertEqual(BeautifulSoup(page).title.text, 'OpenLP 2.1 Remote',
            'The default menu should be returned')

    def start_authenticating_server_test(self):
        """
        Test the default server serves the correctly with authentication
        """
        # GIVEN: A default authorised configuration
        Settings().setValue('remotes/authentication enabled', True)
        self.start_server()

        # WHEN: called the route location with no user details
        code, page = call_remote_server('http://localhost:4316')

        # THEN: then server will ask for details
        self.assertEqual(code, 401, 'The basic authorisation request should be returned')

        # WHEN: called the route location with user details
        code, page = call_remote_server('http://localhost:4316', 'openlp', 'password')

        # THEN: default title will be returned
        self.assertEqual(BeautifulSoup(page).title.text, 'OpenLP 2.1 Remote',
                         'The default menu should be returned')

        # WHEN: called the route location with incorrect user details
        code, page = call_remote_server('http://localhost:4316', 'itwinkle', 'password')

        # THEN: then server will ask for details
        self.assertEqual(code, 401, 'The basic authorisation request should be returned')


def call_remote_server(url, username=None, password=None):
    """
    Helper function

    ``username``
        The username.

    ``password``
        The password.
    """
    if username:
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, username, password)
        authhandler = urllib.request.HTTPBasicAuthHandler(passman)
        opener = urllib.request.build_opener(authhandler)
        urllib.request.install_opener(opener)
    try:
        page = urllib.request.urlopen(url)
        return 0, page.read()
    except urllib.error.HTTPError as e:
        return e.code, ''


def process_http_request(url_path, *args):
    """
    Override function to make the Mock work but does nothing.

    ``Url_path``
        The url_path.

    ``*args``
        Some args.
    """
    cherrypy.response.status = 200
    return None

