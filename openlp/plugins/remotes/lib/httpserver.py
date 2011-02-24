# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

import logging
import os
import urlparse
import re

try:
    import json
except ImportError:
    import simplejson as json

from PyQt4 import QtCore, QtNetwork

from openlp.core.lib import Receiver
from openlp.core.utils import AppLocation

log = logging.getLogger(__name__)

class HttpResponse(object):
    """
    A simple object to encapsulate a pseudo-http response.
    """
    content = u''
    mimetype = None

    def __init__(self, content=u'', mimetype=None):
        self.content = content
        self.mimetype = mimetype


class HttpServer(object):
    """
    Ability to control OpenLP via a webbrowser
    e.g.  http://localhost:4316/send/slidecontroller_live_next
          http://localhost:4316/send/alerts_text?q=your%20alert%20text
    """
    def __init__(self, parent):
        """
        Initialise the httpserver, and start the server
        """
        log.debug(u'Initialise httpserver')
        self.parent = parent
        self.html_dir = os.path.join(
            AppLocation.get_directory(AppLocation.PluginsDir),
            u'remotes', u'html')
        self.connections = []
        self.current_item = None
        self.current_slide = None
        self.start_tcp()

    def start_tcp(self):
        """
        Start the http server, use the port in the settings default to 4316
        Listen out for slide and song changes so they can be broadcast to
        clients. Listen out for socket connections
        """
        log.debug(u'Start TCP server')
        port = QtCore.QSettings().value(
            self.parent.settingsSection + u'/port',
            QtCore.QVariant(4316)).toInt()[0]
        address = QtCore.QSettings().value(
            self.parent.settingsSection + u'/ip address',
            QtCore.QVariant(u'0.0.0.0')).toString()
        self.server = QtNetwork.QTcpServer()
        self.server.listen(QtNetwork.QHostAddress(address), port)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_live_changed'),
            self.slide_change)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_live_started'),
            self.item_change)
        QtCore.QObject.connect(self.server,
            QtCore.SIGNAL(u'newConnection()'), self.new_connection)
        log.debug(u'TCP listening on port %d' % port)

    def slide_change(self, row):
        """
        Slide change listener. Store the item and tell the clients
        """
        self.current_slide = row
        self.send_poll()

    def item_change(self, items):
        """
        Item (song) change listener. Store the slide and tell the clients
        """
        self.current_item = items[0].title
        self.send_poll()

    def send_poll(self):
        """
        Tell the clients something has changed
        """
        Receiver.send_message(u'remotes_poll_response',
            {'slide': self.current_slide,
             'item': self.current_item})

    def new_connection(self):
        """
        A new http connection has been made. Create a client object to handle
        communication
        """
        log.debug(u'new http connection')
        socket = self.server.nextPendingConnection()
        if socket:
            self.connections.append(HttpConnection(self, socket))

    def close_connection(self, connection):
        """
        The connection has been closed. Clean up
        """
        log.debug(u'close http connection')
        self.connections.remove(connection)

    def close(self):
        """
        Close down the http server
        """
        log.debug(u'close http server')
        self.server.close()

class HttpConnection(object):
    """
    A single connection, this handles communication between the server
    and the client
    """
    def __init__(self, parent, socket):
        """
        Initialise the http connection. Listen out for socket signals
        """
        log.debug(u'Initialise HttpConnection: %s' %
            socket.peerAddress().toString())
        self.socket = socket
        self.parent = parent
        self.routes = [
            (u'^/$', self.serve_file, [u'filename'], {u'filename': u''}),
            (r'^/files/(?P<filename>.*)$', self.serve_file, [u'filename'], None),
            (r'^/send/(?P<name>.*)$', self.process_event, [u'name', u'parameters'], None),
            (r'^/request/(?P<name>.*)$', self.process_request, [u'name', u'parameters'], None)
        ]
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'readyRead()'),
            self.ready_read)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'disconnected()'),
            self.disconnected)

    def ready_read(self):
        """
        Data has been sent from the client. Respond to it
        """
        log.debug(u'ready to read socket')
        if self.socket.canReadLine():
            data = unicode(self.socket.readLine())
            log.debug(u'received: ' + data)
            words = data.split(u' ')
            response = None
            if words[0] == u'GET':
                url = urlparse.urlparse(words[1])
                params = self.load_params(url.query)
                # Loop through the routes we set up earlier and execute them
                for route, func, kws, defaults in self.routes:
                    match = re.match(route, url.path)
                    if match:
                        log.debug(u'Matched on "%s" from "%s"', route, url.path)
                        log.debug(u'Groups: %s', match.groups())
                        kwargs = {}
                        # Loop through all the keywords supplied
                        for keyword in kws:
                            groups = match.groupdict()
                            if keyword in groups:
                                # If we find a valid keyword in our URL, use it
                                kwargs[keyword] = groups[keyword]
                            elif defaults and keyword in defaults:
                                # Otherwise, if we have defaults, use them
                                kwargs[keyword] = defaults[keyword]
                            else:
                                # Lastly, set our parameter to None.
                                kwargs[keyword] = None
                        if u'parameters' in kwargs:
                            kwargs[u'parameters'] = params
                        log.debug(u'Keyword arguments: %s', kwargs)
                        response = func(**kwargs)
                        break
                """
                folders = url.path.split(u'/')
                if folders[1] == u'':
                    mimetype, html = self.serve_file(u'')
                elif folders[1] == u'files':
                    mimetype, html = self.serve_file(os.sep.join(folders[2:]))
                elif folders[1] == u'send':
                    html = self.process_event(folders[2], params)
                elif folders[1] == u'request':
                    if self.process_request(folders[2], params):
                        return
                """
            if response:
                if hasattr(response, u'mimetype'):
                    self.send_200_ok(response.mimetype)
                else:
                    self.send_200_ok()
                if hasattr(response, u'content'):
                    self.socket.write(response.content)
                else:
                    self.socket.write(response)
            else:
                self.send_404_not_found()
            self.close()

    def serve_file(self, **kwargs):
        """
        Send a file to the socket. For now, just a subset of file types
        and must be top level inside the html folder.
        If subfolders requested return 404, easier for security for the present.

        Ultimately for i18n, this could first look for xx/file.html before
        falling back to file.html... where xx is the language, e.g. 'en'
        """
        filename = kwargs.get(u'filename', u'')
        log.debug(u'serve file request %s' % filename)
        if not filename:
            filename = u'index.html'
        path = os.path.normpath(os.path.join(self.parent.html_dir, filename))
        if not path.startswith(self.parent.html_dir):
            return None
        ext = os.path.splitext(filename)[1]
        if ext == u'.html':
            mimetype = u'text/html'
        elif ext == u'.css':
            mimetype = u'text/css'
        elif ext == u'.js':
            mimetype = u'application/x-javascript'
        elif ext == u'.jpg':
            mimetype = u'image/jpeg'
        elif ext == u'.gif':
            mimetype = u'image/gif'
        elif ext == u'.png':
            mimetype = u'image/png'
        else:
            return (None, None)
        file_handle = None
        try:
            file_handle = open(path, u'rb')
            log.debug(u'Opened %s' % path)
            html = file_handle.read()
        except IOError:
            log.exception(u'Failed to open %s' % path)
            return None
        finally:
            if file_handle:
                file_handle.close()
        return HttpResponse(content=html, mimetype=mimetype)

    def load_params(self, query):
        """
        Decode the query string parameters sent from the browser
        """
        log.debug(u'loading params %s' % query)
        params = urlparse.parse_qs(query)
        if not params:
            return None
        else:
            return params['q']

    def process_event(self, **kwargs):
        """
        Send a signal to openlp to perform an action.
        Currently lets anything through. Later we should restrict and perform
        basic parameter checking, otherwise rogue clients could crash openlp
        """
        event = kwargs.get(u'name')
        params = kwargs.get(u'parameters')
        log.debug(u'Processing event %s' % event)
        if params:
            Receiver.send_message(event, params)
        else:
            Receiver.send_message(event)
        return json.dumps([u'OK'])

    def process_request(self, **kwargs):
        """
        Client has requested data. Send the signal and parameters for openlp
        to handle, then listen out for a corresponding ``_request`` signal
        which will have the data to return.

        For most events, timeout after 10 seconds (i.e. in case the signal
        recipient isn't listening). ``remotes_poll_request`` is a special case
        however, this is a ajax long poll which is just waiting for slide
        change/song change activity. This can wait longer (one minute).

        ``event``
            The event from the web page.

        ``params``
            Parameters sent with the event.
        """
        event = kwargs.get(u'name')
        params = kwargs.get(u'parameters')
        log.debug(u'Processing request %s' % event)
        if not event.endswith(u'_request'):
            return False
        self.event = event
        response = event.replace(u'_request', u'_response')
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(response), self.process_response)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        QtCore.QObject.connect(self.timer,
            QtCore.SIGNAL(u'timeout()'), self.timeout)
        if event == 'remotes_poll_request':
            self.timer.start(60000)
        else:
            self.timer.start(10000)
        if params:
            Receiver.send_message(event, params)
        else:
            Receiver.send_message(event)
        return True

    def process_response(self, data):
        """
        The recipient of a _request signal has sent data. Convert this to
        json and return it to client
        """
        log.debug(u'Processing response for %s' % self.event)
        if not self.socket:
            return
        self.timer.stop()
        html = json.dumps(data)
        self.send_200_ok()
        self.socket.write(html)
        self.close()

    def send_200_ok(self, mimetype='text/html; charset="utf-8"'):
        """
        Successful request. Send OK headers. Assume html for now.
        """
        self.socket.write(u'HTTP/1.1 200 OK\r\n' + \
            u'Content-Type: %s\r\n\r\n' % mimetype)

    def send_404_not_found(self):
        """
        Invalid url. Say so
        """
        self.socket.write(u'HTTP/1.1 404 Not Found\r\n'+ \
            u'Content-Type: text/html; charset="utf-8"\r\n' + \
            u'\r\n')

    def send_408_timeout(self):
        """
        A _request hasn't returned anything in the timeout period.
        Return timeout
        """
        self.socket.write(u'HTTP/1.1 408 Request Timeout\r\n')

    def timeout(self):
        """
        Listener for timeout signal
        """
        if not self.socket:
            return
        self.send_408_timeout()
        self.close()

    def disconnected(self):
        """
        The client has disconnected. Tidy up
        """
        log.debug(u'socket disconnected')
        self.close()

    def close(self):
        """
        The server has closed the connection. Tidy up
        """
        if not self.socket:
            return
        log.debug(u'close socket')
        self.socket.close()
        self.socket = None
        self.parent.close_connection(self)
