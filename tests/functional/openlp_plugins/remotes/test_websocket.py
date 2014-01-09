# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
This module contains tests for WebSockets
"""
import base64
import uuid
import socket
import time
from unittest import TestCase

from openlp.plugins.remotes.lib.websocket import WebSocketManager, ThreadedWebSocketHandler, \
    WEB_SOCKET_CLIENT_HEADERS
from tests.functional import MagicMock, patch, mock_open


class TestWebSockets(TestCase):
    """
    Test the functions in the :mod:`lib` module.
    """

    def setUp(self):
        """
        Setup the WebSocketsManager
        """
        self.manager = WebSocketManager()
        self.manager.start()

    def tearDown(self):
        self.manager.stop()

    def attempt_to_talk_with_no_handshake_test(self):
        """
        Test the websocket without handshaking first
        """
        # GIVEN: A default configuration

        # WHEN: attempts to talk without upgrading to websocket
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = bytes('No upgrade', 'utf-8')
        received = None
        try:
            # Connect to server and send data
            sock.connect(('localhost', 8888))
            sock.send(data)
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()

        # THEN:
        self.assertIs(isinstance(self.manager, WebSocketManager), True,
                      'It should be an object of WebSocketsManager type')
        self.assertRegexpMatches(received.decode('utf-8'), '.*Error:.*', 'Mismatch')

    def handshake_and_talk_test(self):
        """
        Test the websocket handshake
        """
        # GIVEN: A default configuration

        # WHEN: upgrade to websocket and then talk
        print("starting the websocket server")
        print("started")
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Fake a handshake
        uid = uuid.uuid4()
        key = base64.encodebytes(uid.bytes).strip()
        data = bytes('\r\n'.join(WEB_SOCKET_CLIENT_HEADERS).format(host='localhost', port='8888', key=key), 'utf-8')
        received = None
        try:
            # Connect to server and send data
            sock.connect(('localhost', 8888))
            print("connected")
            sock.send(data)
            #print("data sent: ", data.decode('utf-8'))
            # Receive data from the server and shut down
            time.sleep(1)
            received = sock.recv(1024)
            print("data received: ", received.decode('utf-8'))
            time.sleep(1)
            self.manager.send('broadcast')
            time.sleep(1)
            received_broadcast = sock.recv(1024)
            print(received_broadcast)
            decoded_broadcast = ThreadedWebSocketHandler.decode_client_websocket_message(received_broadcast)
        finally:
            time.sleep(1)
            sock.close()

        # THEN:
        self.assertIs(isinstance(self.manager, WebSocketManager), True,
                      'It should be an object of WebSocketsManager type')
        self.assertRegexpMatches(received.decode('utf-8'), '.*Upgrade: websocket.*', 'Handshake failed')
        self.assertRegexpMatches(decoded_broadcast, '.*broadcast', 'WebSocket did not receive correct string')
