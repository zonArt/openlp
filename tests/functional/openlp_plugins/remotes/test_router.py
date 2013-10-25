# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os
from unittest import TestCase
from tempfile import mkstemp

from PyQt4 import QtGui

from openlp.core.lib import Settings
from openlp.plugins.remotes.lib.httpserver import HttpRouter
from tests.functional import MagicMock

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
        self.fd, self.ini_file = mkstemp('.ini')
        Settings().set_filename(self.ini_file)
        self.application = QtGui.QApplication.instance()
        Settings().extend_default_settings(__default_settings__)
        self.router = HttpRouter()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        os.close(self.fd)
        os.unlink(self.ini_file)

    def password_encrypter_test(self):
        """
        Test hash userid and password function
        """
        # GIVEN: A default configuration
        Settings().setValue('remotes/user id', 'openlp')
        Settings().setValue('remotes/password', 'password')

        # WHEN: called with the defined userid
        router = HttpRouter()
        router.initialise()
        test_value = 'b3BlbmxwOnBhc3N3b3Jk'
        print(router.auth)

        # THEN: the function should return the correct password
        self.assertEqual(router.auth, test_value,
            'The result for make_sha_hash should return the correct encrypted password')

    def process_http_request_test(self):
        """
        Test the router control functionality
        """
        # GIVEN: A testing set of Routes
        router = HttpRouter()
        mocked_function = MagicMock()
        test_route = [
            (r'^/stage/api/poll$', {'function': mocked_function, 'secure': False}),
        ]
        router.routes = test_route

        # WHEN: called with a poll route
        function, args = router.process_http_request('/stage/api/poll', None)

        # THEN: the function should have been called only once
        assert function['function'] == mocked_function, \
            'The mocked function should match defined value.'
        assert function['secure'] == False, \
            'The mocked function should not require any security.'

    def send_appropriate_header_test(self):
        """
        Test the header sending logic
        """
        headers = [ ['test.html','text/html'], ['test.css','text/css'],
            ['test.js','application/javascript'], ['test.jpg','image/jpeg'],
            ['test.gif','image/gif'],['test.ico','image/x-icon'],
            ['test.png','image/png'],['test.whatever','text/plain'],
            ['test','text/plain'],['','text/plain']]
        send_header = MagicMock()
        self.router.send_header = send_header
        for header in headers:
            self.router.send_appropriate_header(header[0])
            send_header.assert_called_with('Content-type',header[1])
            send_header.reset()
    