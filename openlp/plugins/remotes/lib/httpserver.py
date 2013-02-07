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

*Routes:*

``/``
    Go to the web interface.

``/stage``
    Show the stage view.

``/files/{filename}``
    Serve a static file.

``/api/poll``
    Poll to see if there are any changes. Returns a JSON-encoded dict of
    any changes that occurred::

        {"results": {"type": "controller"}}

    Or, if there were no results, False::

        {"results": False}

``/api/display/{hide|show}``
    Blank or unblank the screen.

``/api/alert``
    Sends an alert message to the alerts plugin. This method expects a
    JSON-encoded dict like this::

        {"request": {"text": "<your alert text>"}}

``/api/controller/{live|preview}/{action}``
    Perform ``{action}`` on the live or preview controller. Valid actions
    are:

    ``next``
        Load the next slide.

    ``previous``
        Load the previous slide.

    ``set``
        Set a specific slide. Requires an id return in a JSON-encoded dict like
        this::

            {"request": {"id": 1}}

    ``first``
        Load the first slide.

    ``last``
        Load the last slide.

    ``text``
        Fetches the text of the current song. The output is a JSON-encoded
        dict which looks like this::

            {"result": {"slides": ["...", "..."]}}

``/api/service/{action}``
    Perform ``{action}`` on the service manager (e.g. go live). Data is
    passed as a json-encoded ``data`` parameter. Valid actions are:

    ``next``
        Load the next item in the service.

    ``previous``
        Load the previews item in the service.

    ``set``
        Set a specific item in the service. Requires an id returned in a
        JSON-encoded dict like this::

            {"request": {"id": 1}}

    ``list``
        Request a list of items in the service. Returns a list of items in the
        current service in a JSON-encoded dict like this::

            {"results": {"items": [{...}, {...}]}}
"""

import json
import logging
import os
import re
import urllib
import urlparse

from PyQt4 import QtCore, QtNetwork
from mako.template import Template

from openlp.core.lib import Receiver, Settings, PluginStatus, StringContent
from openlp.core.utils import AppLocation, translate

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

    def __init__(self, content='', headers=None, code=None):
        if headers is None:
            headers = {}
        self.content = content
        for key, value in headers.iteritems():
            self.headers[key] = value
        if code:
            self.code = code


class HttpServer(object):
    """
    Ability to control OpenLP via a web browser.
    """
    def __init__(self, plugin):
        """
        Initialise the httpserver, and start the server.
        """
        log.debug(u'Initialise httpserver')
        self.plugin = plugin
        self.html_dir = os.path.join(AppLocation.get_directory(AppLocation.PluginsDir), u'remotes', u'html')
        self.connections = []
        self.current_item = None
        self.current_slide = None
        self.start_tcp()

    def start_tcp(self):
        """
        Start the http server, use the port in the settings default to 4316.
        Listen out for slide and song changes so they can be broadcast to
        clients. Listen out for socket connections.
        """
        log.debug(u'Start TCP server')
        port = Settings().value(self.plugin.settingsSection + u'/port')
        address = Settings().value(self.plugin.settingsSection + u'/ip address')
        self.server = QtNetwork.QTcpServer()
        self.server.listen(QtNetwork.QHostAddress(address), port)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'slidecontroller_live_changed'),
            self.slide_change)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'slidecontroller_live_started'),
            self.item_change)
        QtCore.QObject.connect(self.server, QtCore.SIGNAL(u'newConnection()'), self.new_connection)
        log.debug(u'TCP listening on port %d' % port)

    def slide_change(self, row):
        """
        Slide change listener. Store the item and tell the clients.
        """
        self.current_slide = row

    def item_change(self, items):
        """
        Item (song) change listener. Store the slide and tell the clients.
        """
        self.current_item = items[0]

    def new_connection(self):
        """
        A new http connection has been made. Create a client object to handle
        communication.
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
        Close down the http server.
        """
        log.debug(u'close http server')
        self.server.close()


class HttpConnection(object):
    """
    A single connection, this handles communication between the server
    and the client.
    """
    def __init__(self, parent, socket):
        """
        Initialise the http connection. Listen out for socket signals.
        """
        log.debug(u'Initialise HttpConnection: %s' % socket.peerAddress())
        self.socket = socket
        self.parent = parent
        self.routes = [
            (u'^/$', self.serve_file),
            (u'^/(stage)$', self.serve_file),
            (r'^/files/(.*)$', self.serve_file),
            (r'^/api/poll$', self.poll),
            (r'^/api/controller/(live|preview)/(.*)$', self.controller),
            (r'^/api/service/(.*)$', self.service),
            (r'^/api/display/(hide|show|blank|theme|desktop)$', self.display),
            (r'^/api/alert$', self.alert),
            (r'^/api/plugin/(search)$', self.pluginInfo),
            (r'^/api/(.*)/search$', self.search),
            (r'^/api/(.*)/live$', self.go_live),
            (r'^/api/(.*)/add$', self.add_to_service)
        ]
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'readyRead()'), self.ready_read)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'disconnected()'), self.disconnected)
        self.translate()

    def _get_service_items(self):
        service_items = []
        service_manager = self.parent.plugin.serviceManager
        if self.parent.current_item:
            current_unique_identifier = self.parent.current_item.unique_identifier
        else:
            current_unique_identifier = None
        for item in service_manager.serviceItems:
            service_item = item[u'service_item']
            service_items.append({
                u'id': unicode(service_item.unique_identifier),
                u'title': unicode(service_item.get_display_title()),
                u'plugin': unicode(service_item.name),
                u'notes': unicode(service_item.notes),
                u'selected': (service_item.unique_identifier == current_unique_identifier)
            })
        return service_items

    def translate(self):
        """
        Translate various strings in the mobile app.
        """
        self.template_vars = {
            'app_title': translate('RemotePlugin.Mobile', 'OpenLP 2.1 Remote'),
            'stage_title': translate('RemotePlugin.Mobile', 'OpenLP 2.1 Stage View'),
            'service_manager': translate('RemotePlugin.Mobile', 'Service Manager'),
            'slide_controller': translate('RemotePlugin.Mobile', 'Slide Controller'),
            'alerts': translate('RemotePlugin.Mobile', 'Alerts'),
            'search': translate('RemotePlugin.Mobile', 'Search'),
            'home': translate('RemotePlugin.Mobile', 'Home'),
            'refresh': translate('RemotePlugin.Mobile', 'Refresh'),
            'blank': translate('RemotePlugin.Mobile', 'Blank'),
            'theme': translate('RemotePlugin.Mobile', 'Theme'),
            'desktop': translate('RemotePlugin.Mobile', 'Desktop'),
            'show': translate('RemotePlugin.Mobile', 'Show'),
            'prev': translate('RemotePlugin.Mobile', 'Prev'),
            'next': translate('RemotePlugin.Mobile', 'Next'),
            'text': translate('RemotePlugin.Mobile', 'Text'),
            'show_alert': translate('RemotePlugin.Mobile', 'Show Alert'),
            'go_live': translate('RemotePlugin.Mobile', 'Go Live'),
            'add_to_service': translate('RemotePlugin.Mobile', 'Add to Service'),
            'add_and_go_to_service': translate('RemotePlugin.Mobile', 'Add &amp; Go to Service'),
            'no_results': translate('RemotePlugin.Mobile', 'No Results'),
            'options': translate('RemotePlugin.Mobile', 'Options'),
            'service': translate('RemotePlugin.Mobile', 'Service'),
            'slides': translate('RemotePlugin.Mobile', 'Slides')
        }

    def ready_read(self):
        """
        Data has been sent from the client. Respond to it
        """
        log.debug(u'ready to read socket')
        if self.socket.canReadLine():
            data = str(self.socket.readLine())
            try:
                log.debug(u'received: ' + data)
            except UnicodeDecodeError:
                # Malicious request containing non-ASCII characters.
                self.close()
                return
            words = data.split(' ')
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
        elif filename == u'stage':
            filename = u'stage.html'
        path = os.path.normpath(os.path.join(self.parent.html_dir, filename))
        if not path.startswith(self.parent.html_dir):
            return HttpResponse(code=u'404 Not Found')
        ext = os.path.splitext(filename)[1]
        html = None
        if ext == u'.html':
            mimetype = u'text/html'
            variables = self.template_vars
            html = Template(filename=path, input_encoding=u'utf-8', output_encoding=u'utf-8').render(**variables)
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
            if html:
                content = html
            else:
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
            u'service': self.parent.plugin.serviceManager.service_id,
            u'slide': self.parent.current_slide or 0,
            u'item': self.parent.current_item.unique_identifier if self.parent.current_item else u'',
            u'twelve':Settings().value(u'remotes/twelve hour'),
            u'blank': self.parent.plugin.liveController.blankScreen.isChecked(),
            u'theme': self.parent.plugin.liveController.themeScreen.isChecked(),
            u'display': self.parent.plugin.liveController.desktopScreen.isChecked()
        }
        return HttpResponse(json.dumps({u'results': result}),
            {u'Content-Type': u'application/json'})

    def display(self, action):
        """
        Hide or show the display screen.

        ``action``
            This is the action, either ``hide`` or ``show``.
        """
        Receiver.send_message(u'slidecontroller_toggle_display', action)
        return HttpResponse(json.dumps({u'results': {u'success': True}}),
            {u'Content-Type': u'application/json'})

    def alert(self):
        """
        Send an alert.
        """
        plugin = self.parent.plugin.pluginManager.get_plugin_by_name("alerts")
        if plugin.status == PluginStatus.Active:
            try:
                text = json.loads(self.url_params[u'data'][0])[u'request'][u'text']
            except KeyError, ValueError:
                return HttpResponse(code=u'400 Bad Request')
            text = urllib.unquote(text)
            Receiver.send_message(u'alerts_text', [text])
            success = True
        else:
            success = False
        return HttpResponse(json.dumps({u'results': {u'success': success}}),
            {u'Content-Type': u'application/json'})

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
                        if frame[u'verseTag']:
                            item[u'tag'] = unicode(frame[u'verseTag'])
                        else:
                            item[u'tag'] = unicode(index + 1)
                        item[u'text'] = unicode(frame[u'text'])
                        item[u'html'] = unicode(frame[u'html'])
                    else:
                        item[u'tag'] = unicode(index + 1)
                        item[u'text'] = unicode(frame[u'title'])
                        item[u'html'] = unicode(frame[u'title'])
                    item[u'selected'] = (self.parent.current_slide == index)
                    data.append(item)
            json_data = {u'results': {u'slides': data}}
            if current_item:
                json_data[u'results'][u'item'] = self.parent.current_item.unique_identifier
        else:
            if self.url_params and self.url_params.get(u'data'):
                try:
                    data = json.loads(self.url_params[u'data'][0])
                except KeyError, ValueError:
                    return HttpResponse(code=u'400 Bad Request')
                log.info(data)
                # This slot expects an int within a list.
                id = data[u'request'][u'id']
                Receiver.send_message(event, [id])
            else:
                Receiver.send_message(event)
            json_data = {u'results': {u'success': True}}
        return HttpResponse(json.dumps(json_data),
            {u'Content-Type': u'application/json'})

    def service(self, action):
        event = u'servicemanager_%s' % action
        if action == u'list':
            return HttpResponse(json.dumps({u'results': {u'items': self._get_service_items()}}),
                {u'Content-Type': u'application/json'})
        else:
            event += u'_item'
        if self.url_params and self.url_params.get(u'data'):
            try:
                data = json.loads(self.url_params[u'data'][0])
            except KeyError, ValueError:
                return HttpResponse(code=u'400 Bad Request')
            Receiver.send_message(event, data[u'request'][u'id'])
        else:
            Receiver.send_message(event)
        return HttpResponse(json.dumps({u'results': {u'success': True}}),
            {u'Content-Type': u'application/json'})

    def pluginInfo(self, action):
        """
        Return plugin related information, based on the action.

        ``action``
            The action to perform. If *search* return a list of plugin names
            which support search.
        """
        if action == u'search':
            searches = []
            for plugin in self.parent.plugin.pluginManager.plugins:
                if plugin.status == PluginStatus.Active and plugin.mediaItem and plugin.mediaItem.hasSearch:
                    searches.append([plugin.name, unicode(plugin.textStrings[StringContent.Name][u'plural'])])
            return HttpResponse(
                json.dumps({u'results': {u'items': searches}}),
                {u'Content-Type': u'application/json'})

    def search(self, type):
        """
        Return a list of items that match the search text.

        ``type``
            The plugin name to search in.
        """
        try:
            text = json.loads(self.url_params[u'data'][0])[u'request'][u'text']
        except KeyError, ValueError:
            return HttpResponse(code=u'400 Bad Request')
        text = urllib.unquote(text)
        plugin = self.parent.plugin.pluginManager.get_plugin_by_name(type)
        if plugin.status == PluginStatus.Active and plugin.mediaItem and plugin.mediaItem.hasSearch:
            results = plugin.mediaItem.search(text, False)
        else:
            results = []
        return HttpResponse(json.dumps({u'results': {u'items': results}}),
            {u'Content-Type': u'application/json'})

    def go_live(self, type):
        """
        Go live on an item of type ``type``.
        """
        try:
            id = json.loads(self.url_params[u'data'][0])[u'request'][u'id']
        except KeyError, ValueError:
            return HttpResponse(code=u'400 Bad Request')
        plugin = self.parent.plugin.pluginManager.get_plugin_by_name(type)
        if plugin.status == PluginStatus.Active and plugin.mediaItem:
            plugin.mediaItem.goLive(id, remote=True)
        return HttpResponse(code=u'200 OK')

    def add_to_service(self, type):
        """
        Add item of type ``type`` to the end of the service.
        """
        try:
            id = json.loads(self.url_params[u'data'][0])[u'request'][u'id']
        except KeyError, ValueError:
            return HttpResponse(code=u'400 Bad Request')
        plugin = self.parent.plugin.pluginManager.get_plugin_by_name(type)
        if plugin.status == PluginStatus.Active and plugin.mediaItem:
            item_id = plugin.mediaItem.createItemFromId(id)
            plugin.mediaItem.addToService(item_id, remote=True)
        return HttpResponse(code=u'200 OK')

    def send_response(self, response):
        http = u'HTTP/1.1 %s\r\n' % response.code
        for header, value in response.headers.iteritems():
            http += '%s: %s\r\n' % (header, value)
        http += '\r\n'
        self.socket.write(http)
        self.socket.write(response.content)

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
