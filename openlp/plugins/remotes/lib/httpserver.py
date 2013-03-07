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
import cherrypy

from mako.template import Template
from PyQt4 import QtCore

from openlp.core.lib import Registry, Settings, PluginStatus, StringContent
from openlp.core.utils import AppLocation, translate
from openlp.plugins.remotes.lib.httpauth import AuthController, require_auth

log = logging.getLogger(__name__)

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
        self.conf = {'/files': {u'tools.staticdir.on': True,
                                u'tools.staticdir.dir': self.html_dir}}
        self.start_server()

    def start_server(self):
        """
        Start the http server, use the port in the settings default to 4316.
        Listen out for slide and song changes so they can be broadcast to
        clients. Listen out for socket connections.
        """
        log.debug(u'Start CherryPy server')
        port = Settings().value(self.plugin.settingsSection + u'/port')
        address = Settings().value(self.plugin.settingsSection + u'/ip address')
        server_config = {u'server.socket_host': str(address),
                         u'server.socket_port': port}
        cherrypy.config.update(server_config)
        cherrypy.config.update({'environment': 'embedded'})
        cherrypy.config.update({'engine.autoreload_on': False})
        cherrypy.tree.mount(HttpConnection(self), '/', config=self.conf)
        cherrypy.engine.start()
        Registry().register_function(u'slidecontroller_live_changed', self.slide_change)
        Registry().register_function(u'slidecontroller_live_started', self.item_change)
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

    def close(self):
        """
        Close down the http server.
        """
        log.debug(u'close http server')
        cherrypy.engine.exit()
        cherrypy.engine.stop()


class HttpConnection(object):
    """
    A single connection, this handles communication between the server and the client.
    """
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()

    def __init__(self, parent):
        """
        Initialise the http connection. Listen out for socket signals.
        """
        #log.debug(u'Initialise HttpConnection: %s' % socket.peerAddress())
        #self.socket = socket
        self.parent = parent
        self.routes = [
            (u'^/$', self.serve_file),
            (u'^/(stage)$', self.serve_file),
            (r'^/files/(.*)$', self.serve_file),
            (r'^/api/poll$', self.poll),
            (r'^/stage/api/poll$', self.poll),
            (r'^/api/controller/(live|preview)/(.*)$', self.controller),
            (r'^/stage/api/controller/live/(.*)$', self.controller),
            (r'^/api/service/(.*)$', self.service),
            (r'^/api/display/(hide|show|blank|theme|desktop)$', self.display),
            (r'^/api/alert$', self.alert),
            (r'^/api/plugin/(search)$', self.pluginInfo),
            (r'^/api/(.*)/search$', self.search),
            (r'^/api/(.*)/live$', self.go_live),
            (r'^/api/(.*)/add$', self.add_to_service)
        ]
        self.translate()

    @cherrypy.expose
    #@require_auth(auth)
    def default(self, *args, **kwargs):
        """
        Handles the requests for the main url.  This is secure depending on settings.
        """
        # Loop through the routes we set up earlier and execute them
        return self._process_http_request(args, kwargs)

    @cherrypy.expose
    def stage(self, *args, **kwargs):
        """
        Handles the requests for the stage url.  This is not secure.
        """
        print "Stage"
        url = urlparse.urlparse(cherrypy.url())
        self.url_params = urlparse.parse_qs(url.query)
        print url
        print [self.url_params]
        #return self.serve_file(u'stage')
        return self._process_http_request(args, kwargs)

    @cherrypy.expose
    def files(self, *args, **kwargs):
        """
        Handles the requests for the stage url.  This is not secure.
        """
        print "files"
        url = urlparse.urlparse(cherrypy.url())
        self.url_params = urlparse.parse_qs(url.query)
        print url
        print [self.url_params]
        print args
        #return self.serve_file(args)
        return self._process_http_request(args, kwargs)

    def _process_http_request(self, args, kwargs):
        """
        Common function to process HTTP requests where secure or insecure
        """
        print "common handler"
        url = urlparse.urlparse(cherrypy.url())
        self.url_params = urlparse.parse_qs(url.query)
        print url
        print [self.url_params]
        response = None
        for route, func in self.routes:
            match = re.match(route, url.path)
            if match:
                print 'Route "%s" matched "%s"', route, url.path
                log.debug('Route "%s" matched "%s"', route, url.path)
                args = []
                for param in match.groups():
                    args.append(param)
                response = func(*args)
                break
        if response:
            return response
        else:
            return self._http_not_found()

    def _get_service_items(self):
        """
        Read the service item in use and return the data as a json object
        """
        service_items = []
        if self.parent.current_item:
            current_unique_identifier = self.parent.current_item.unique_identifier
        else:
            current_unique_identifier = None
        for item in self.service_manager.service_items:
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

    def serve_file(self, filename=None):
        """
        Send a file to the socket. For now, just a subset of file types
        and must be top level inside the html folder.
        If subfolders requested return 404, easier for security for the present.

        Ultimately for i18n, this could first look for xx/file.html before
        falling back to file.html... where xx is the language, e.g. 'en'
        """
        print "serve_file", filename
        log.debug(u'serve file request %s' % filename)
        if not filename:
            filename = u'index.html'
        elif filename == u'stage':
            filename = u'stage.html'
        path = os.path.normpath(os.path.join(self.parent.html_dir, filename))
        if not path.startswith(self.parent.html_dir):
            return self._http_not_found()
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
            return self._http_not_found()
        finally:
            if file_handle:
                file_handle.close()
        cherrypy.response.headers['Content-Type'] = mimetype
        return content

    def poll(self):
        """
        Poll OpenLP to determine the current slide number and item name.
        """
        result = {
            u'service': self.service_manager.service_id,
            u'slide': self.parent.current_slide or 0,
            u'item': self.parent.current_item.unique_identifier if self.parent.current_item else u'',
            u'twelve': Settings().value(u'remotes/twelve hour'),
            u'blank': self.live_controller.blank_screen.isChecked(),
            u'theme': self.live_controller.theme_screen.isChecked(),
            u'display': self.live_controller.desktop_screen.isChecked()
        }
        cherrypy.response.headers['Content-Type'] = u'application/json'
        return json.dumps({u'results': result})

    def display(self, action):
        """
        Hide or show the display screen.
        This is a cross Thread call and UI is updated so Events need to be used.

        ``action``
            This is the action, either ``hide`` or ``show``.
        """
        self.live_controller.emit(QtCore.SIGNAL(u'slidecontroller_toggle_display'), action)
        cherrypy.response.headers['Content-Type'] = u'application/json'
        return json.dumps({u'results': {u'success': True}})

    def alert(self):
        """
        Send an alert.
        """
        plugin = self.plugin_manager.get_plugin_by_name("alerts")
        if plugin.status == PluginStatus.Active:
            try:
                text = json.loads(self.url_params[u'data'][0])[u'request'][u'text']
            except KeyError, ValueError:
                return self._http_bad_request()
            text = urllib.unquote(text)
            Registry().execute(u'alerts_text', [text])
            success = True
        else:
            success = False
        cherrypy.response.headers['Content-Type'] = u'application/json'
        return json.dumps({u'results': {u'success': success}})

    def controller(self, display_type, action):
        """
        Perform an action on the slide controller.

        ``display_type``
            This is the type of slide controller, either ``preview`` or ``live``.

        ``action``
            The action to perform.
        """
        event = u'slidecontroller_%s_%s' % (display_type, action)
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
                    return self._http_bad_request()
                log.info(data)
                # This slot expects an int within a list.
                id = data[u'request'][u'id']
                Registry().execute(event, [id])
            else:
                Registry().execute(event, [0])
            json_data = {u'results': {u'success': True}}
        cherrypy.response.headers['Content-Type'] = u'application/json'
        return json.dumps(json_data)

    def service(self, action):
        """
        Handles requests for service items

        ``action``
            The action to perform.
        """
        event = u'servicemanager_%s' % action
        if action == u'list':
            cherrypy.response.headers['Content-Type'] = u'application/json'
            return json.dumps({u'results': {u'items': self._get_service_items()}})
        else:
            event += u'_item'
        if self.url_params and self.url_params.get(u'data'):
            try:
                data = json.loads(self.url_params[u'data'][0])
            except KeyError, ValueError:
                return self._http_bad_request()
            Registry().execute(event, data[u'request'][u'id'])
        else:
            Registry().execute(event)
        cherrypy.response.headers['Content-Type'] = u'application/json'
        return json.dumps({u'results': {u'success': True}})

    def pluginInfo(self, action):
        """
        Return plugin related information, based on the action.

        ``action``
            The action to perform. If *search* return a list of plugin names
            which support search.
        """
        if action == u'search':
            searches = []
            for plugin in self.plugin_manager.plugins:
                if plugin.status == PluginStatus.Active and plugin.mediaItem and plugin.mediaItem.hasSearch:
                    searches.append([plugin.name, unicode(plugin.textStrings[StringContent.Name][u'plural'])])
            cherrypy.response.headers['Content-Type'] = u'application/json'
            return json.dumps({u'results': {u'items': searches}})

    def search(self, plugin_name):
        """
        Return a list of items that match the search text.

        ``plugin``
            The plugin name to search in.
        """
        try:
            text = json.loads(self.url_params[u'data'][0])[u'request'][u'text']
        except KeyError, ValueError:
            return self._http_bad_request()
        text = urllib.unquote(text)
        plugin = self.plugin_manager.get_plugin_by_name(plugin_name)
        if plugin.status == PluginStatus.Active and plugin.mediaItem and plugin.mediaItem.hasSearch:
            results = plugin.mediaItem.search(text, False)
        else:
            results = []
        cherrypy.response.headers['Content-Type'] = u'application/json'
        return json.dumps({u'results': {u'items': results}})

    def go_live(self, plugin_name):
        """
        Go live on an item of type ``plugin``.
        """
        try:
            id = json.loads(self.url_params[u'data'][0])[u'request'][u'id']
        except KeyError, ValueError:
            return self._http_bad_request()
        plugin = self.plugin_manager.get_plugin_by_name(type)
        if plugin.status == PluginStatus.Active and plugin.mediaItem:
            plugin.mediaItem.goLive(id, remote=True)
        return self._http_success()

    def add_to_service(self, plugin_name):
        """
        Add item of type ``plugin_name`` to the end of the service.
        """
        try:
            id = json.loads(self.url_params[u'data'][0])[u'request'][u'id']
        except KeyError, ValueError:
            return self._http_bad_request()
        plugin = self.plugin_manager.get_plugin_by_name(type)
        if plugin.status == PluginStatus.Active and plugin.mediaItem:
            item_id = plugin.mediaItem.createItemFromId(id)
            plugin.mediaItem.addToService(item_id, remote=True)
        self._http_success()

    def _http_success(self):
        cherrypy.response.status = 200

    def _http_bad_request(self):
        cherrypy.response.status = 400

    def _http_not_found(self):
        cherrypy.response.status = 404
        cherrypy.response.body = ["<html><body>Sorry, an error occured</body></html>"]

    def _get_service_manager(self):
        """
        Adds the service manager to the class dynamically
        """
        if not hasattr(self, u'_service_manager'):
            self._service_manager = Registry().get(u'service_manager')
        return self._service_manager

    service_manager = property(_get_service_manager)

    def _get_live_controller(self):
        """
        Adds the live controller to the class dynamically
        """
        if not hasattr(self, u'_live_controller'):
            self._live_controller = Registry().get(u'live_controller')
        return self._live_controller

    live_controller = property(_get_live_controller)

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, u'_plugin_manager'):
            self._plugin_manager = Registry().get(u'plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)
