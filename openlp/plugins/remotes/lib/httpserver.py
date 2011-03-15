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

"""
The :mod:`http` module contains the API web server. This is a lightweight web
server used by remotes to interact with OpenLP. It uses JSON to communicate with
the remotes.

*Routes:*

``/``
    Go to the web interface.

``/files/{filename}``
    Serve a static file.

``/api/poll``
    Poll to see if there are any changes. Returns a JSON-encoded dict of
    any changes that occurred::

        {"results": {"type": "controller"}}

    Or, if there were no results, False::

        {"results": False}

``/api/controller/{live|preview}/{action}``
    Perform ``{action}`` on the live or preview controller. Valid actions
    are:

    ``next``
        Load the next slide.

    ``previous``
        Load the previous slide.

    ``jump``
        Jump to a specific slide. Requires an id return in a JSON-encoded
        dict like so::

            {"request": {"id": 1}}

    ``first``
        Load the first slide.

    ``last``
        Load the last slide.

    ``text``
        Request the text of the current slide.

``/api/service/{action}``
    Perform ``{action}`` on the service manager (e.g. go live). Data is
    passed as a json-encoded ``data`` parameter. Valid actions are:

    ``next``
        Load the next item in the service.

    ``previous``
        Load the previews item in the service.

    ``jump``
        Jump to a specific item in the service. Requires an id returned in
        a JSON-encoded dict like so::

            {"request": {"id": 1}}

    ``list``
        Request a list of items in the service.
"""

import logging
import os
import urlparse
import re
from pprint import pformat

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
    code = '200 OK'
    content = ''
    headers = {
        'Content-Type': 'text/html; charset="utf-8"\r\n'
    }

    def __init__(self, content='', headers={}, code=None):
        self.content = content
        for key, value in headers.iteritems():
            self.headers[key] = value
        if code:
            self.code = code


class HttpServer(object):
    """
    Ability to control OpenLP via a webbrowser
    e.g. http://localhost:4316/send/slidecontroller_live_next
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
        #self.send_poll()

    def item_change(self, items):
        """
        Item (song) change listener. Store the slide and tell the clients
        """
        self.current_item = items[0]
        #log.debug(pformat(items[0].__dict__, 2))
        #self.send_poll()

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
        if connection in self.connections:
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
        Initialise the http connection. Listen out for socket signals.
                """
        log.debug(u'Initialise HttpConnection: %s' %
            socket.peerAddress().toString())
        self.socket = socket
        self.parent = parent
        self.routes = [
            (u'^/$', self.serve_file),
            (r'^/files/(.*)$', self.serve_file),
            (r'^/api/poll$', self.poll),
            (r'^/api/controller/(live|preview)/(.*)$', self.controller),
            (r'^/api/service/(.*)$', self.service)
        ]
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'readyRead()'),
            self.ready_read)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'disconnected()'),
            self.disconnected)

    def _get_service_items(self):
        service_items = []
        service_manager = self.parent.parent.serviceManager
        item = service_manager.findServiceItem()[0]
        if item >= 0 and item < len(service_manager.serviceItems):
            curitem = service_manager.serviceItems[item]
        else:
            curitem = None
        for item in service_manager.serviceItems:
            service_item = item[u'service_item']
            service_items.append({
                u'title': unicode(service_item.get_display_title()),
                u'plugin': unicode(service_item.name),
                u'notes': unicode(service_item.notes),
                u'selected': (item == curitem)
            })
        return service_items

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
                self.url_params = urlparse.parse_qs(url.query)
                # Loop through the routes we set up earlier and execute them
                for route, func in self.routes:
                    match = re.match(route, url.path)
                    if match:
                        log.debug('Route "%s" matched "%s"', route, url.path)
                        args = []
                        for param in match.groups():
                            args.append(param)
                        response = func(*args)
                        break
            if response:
                self.send_response(response)
                """
                if hasattr(response, u'mimetype'):
                    self.send_200_ok(response.mimetype)
                else:
                    self.send_200_ok()
                if hasattr(response, u'content'):
                    self.socket.write(response.content)
                elif isinstance(response, basestring):
                    self.socket.write(response)
                """
            else:
                self.send_response(HttpResponse(code='404 Not Found'))
            self.close()

    def serve_file(self, filename=None):
        """
        Send a file to the socket. For now, just a subset of file types
        and must be top level inside the html folder.
        If subfolders requested return 404, easier for security for the present.

        Ultimately for i18n, this could first look for xx/file.html before
        falling back to file.html... where xx is the language, e.g. 'en'
        """
        log.debug(u'serve file request %s' % filename)
        if not filename:
            filename = u'index.html'
        path = os.path.normpath(os.path.join(self.parent.html_dir, filename))
        if not path.startswith(self.parent.html_dir):
            return HttpResponse(code=u'404 Not Found')
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
            mimetype = u'text/plain'
        file_handle = None
        try:
            file_handle = open(path, u'rb')
            log.debug(u'Opened %s' % path)
            content = file_handle.read()
        except IOError:
            log.exception(u'Failed to open %s' % path)
            return HttpResponse(code=u'404 Not Found')
        finally:
            if file_handle:
                file_handle.close()
        return HttpResponse(content, {u'Content-Type': mimetype})

    def poll(self):
        """
        Poll OpenLP to determine the current slide number and item name.
        """
        result = {
            u'slide': self.parent.current_slide or 0,
            u'item': self.parent.current_item.title \
                if self.parent.current_item else u''
        }
        return HttpResponse(json.dumps({u'results': result}),
             {'Content-Type': 'application/json'})

    def controller(self, type, action):
        """
        Perform an action on the slide controller.

        ``type``
            This is the type of slide controller, either ``preview`` or
            ``live``.

        ``action``
            The action to perform.
        """
        event = u'slidecontroller_%s_%s' % (type, action)
        if action == u'text':
            current_item = self.parent.current_item
            data = []
            if current_item:
                for index, frame in enumerate(current_item.get_frames()):
                    item = {}
                    if current_item.is_text():
                        item[u'tag'] = unicode(frame[u'verseTag'])
                        item[u'text'] = unicode(frame[u'html'])
                    else:
                        item[u'tag'] = unicode(index)
                        item[u'text'] = u''
                    item[u'selected'] = (self.parent.current_slide == index)
                    data.append(item)
            json_data = {u'results': {u'slides': data}}
        else:
            if self.url_params and self.url_params.get(u'data'):
                data = json.loads(self.url_params[u'data'][0])
                log.info(data)
                # This slot expects an int within a list.
                id = data[u'request'][u'id']
                Receiver.send_message(event, [id])
            else:
                Receiver.send_message(event)
            json_data = {u'results': {u'success': True}}
        #if action == u'text':
        #    json_data = {u'results': }
        return HttpResponse(json.dumps(json_data),
            {'Content-Type': 'application/json'})

    def service(self, action):
        event = u'servicemanager_%s' % action
        if action == u'list':
            return HttpResponse(
                json.dumps({'results': self._get_service_items()}),
                {'Content-Type': 'application/json'})
        else:
            event += u'_item'
        if self.url_params and self.url_params.get(u'data'):
            data = json.loads(self.url_params[u'data'][0])
            Receiver.send_message(event, data[u'request'][u'id'])
        else:
            Receiver.send_message(event)
        return HttpResponse(json.dumps({'results': {u'success': True}}),
            {'Content-Type': 'application/json'})

    def process_event(self, **kwargs):
        """
        Send a signal to openlp to perform an action.
        Currently lets anything through. Later we should restrict and perform
        basic parameter checking, otherwise rogue clients could crash openlp
        """
        event = kwargs.get(u'event')
        log.debug(u'Processing event %s' % event)
        if self.url_params:
            Receiver.send_message(event, self.url_params)
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
        event = kwargs.get(u'event')
        log.debug(u'Processing request %s' % event)
        if not event.endswith(u'_request'):
            return None
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
        if self.url_params:
            Receiver.send_message(event, self.url_params)
        else:
            Receiver.send_message(event)
        return None

    def process_response(self, data):
        """
        The recipient of a _request signal has sent data. Convert this to
        json and return it to client
        """
        log.debug(u'Processing response for %s' % self.event)
        if not self.socket:
            return
        self.timer.stop()
        json_data = json.dumps(data)
        self.send_200_ok()
        self.socket.write(json_data)
        self.close()

    def send_response(self, response):
        http = u'HTTP/1.1 %s\r\n' % response.code
        for header in response.headers.iteritems():
            http += '%s: %s\r\n' % header
        http += '\r\n'
        self.socket.write(response.content)

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
