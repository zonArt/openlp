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
The :mod:`http` module contains the API web server. This is a lightweight web
server used by remotes to interact with OpenLP. It uses JSON to communicate with
the remotes.
"""

import ssl
import socket
import os
import logging
from urllib.parse import urlparse, parse_qs

from PyQt4 import QtCore

from openlp.core.lib import Settings
from openlp.core.utils import AppLocation

from openlp.plugins.remotes.lib import HttpRouter

from socketserver import BaseServer, ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer

from hashlib import sha1

log = logging.getLogger(__name__)


def make_sha_hash(password):
    """
    Create an encrypted password for the given password.
    """
    log.debug("make_sha_hash")
    return sha1(password.encode()).hexdigest()


def fetch_password(username):
    """
    Fetch the password for a provided user.
    """
    log.debug("Fetch Password")
    if username != Settings().value('remotes/user id'):
        return None
    return make_sha_hash(Settings().value('remotes/password'))


class CustomHandler(BaseHTTPRequestHandler, HttpRouter):
    """
    Main class to present webpages and authentication.
    """

    def do_POST(self):
        self.do_GET()

    def do_GET(self):
        """
        Present frontpage with user authentication.
        """
        if self.path == '/favicon.ico':
            return
        print(self.headers['content-type'])
        if self.headers['content-type'] == 'application/json':
            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
            for var in postvars:
                print(var.decode("utf-8"))
        if not hasattr(self, 'auth'):
            self.initialise()
        function, args = self.process_http_request(self.path)
        if not function:
            self.do_http_error()
            return
        if function['secure']:
            if self.headers['Authorization'] is None:
                self.do_authorisation()
                self.wfile.write(bytes('no auth header received', 'UTF-8'))
            elif self.headers['Authorization'] == 'Basic %s' % self.auth:
                self.do_http_success()
                self.call_function(function, *args)
            else:
                self.do_authorisation()
                self.wfile.write(bytes(self.headers['Authorization'], 'UTF-8'))
                self.wfile.write(bytes(' not authenticated', 'UTF-8'))
        else:
            self.call_function(function, *args)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class HttpThread(QtCore.QThread):
    """
    A special Qt thread class to allow the HTTP server to run at the same time as the UI.
    """
    def __init__(self, server):
        """
        Constructor for the thread class.

        ``server``
            The http server class.
        """
        super(HttpThread, self).__init__(None)
        self.http_server = server

    def run(self):
        """
        Run the thread.
        """
        self.http_server.start_server()


class OpenLPServer():
    def __init__(self):
        """
        Initialise the http server, and start the server.
        """
        log.debug('Initialise httpserver')
        self.settings_section = 'remotes'
        self.http_thread = HttpThread(self)
        self.http_thread.start()

    def start_server(self):
        address = Settings().value(self.settings_section + '/ip address')
        if Settings().value(self.settings_section + '/https enabled'):
            port = Settings().value(self.settings_section + '/https port')
            self.httpd = HTTPSServer((address, port), CustomHandler)
            print('started ssl httpd...')
        else:
            port = Settings().value(self.settings_section + '/port')
            self.httpd = ThreadingHTTPServer((address, port), CustomHandler)
            print('started non ssl httpd...')
        self.httpd.serve_forever()

    def stop_server(self):
        self.httpd.socket.close()
        self.httpd = None


class HTTPSServer(HTTPServer):
    def __init__(self, address, handler):
        BaseServer.__init__(self, address, handler)
        local_data = AppLocation.get_directory(AppLocation.DataDir)
        self.socket = ssl.SSLSocket(
            sock=socket.socket(self.address_family, self.socket_type),
            ssl_version=ssl.PROTOCOL_TLSv1,
            certfile=os.path.join(local_data, 'remotes', 'openlp.crt'),
            keyfile=os.path.join(local_data, 'remotes', 'openlp.key'),
            server_side=True)
        self.server_bind()
        self.server_activate()



