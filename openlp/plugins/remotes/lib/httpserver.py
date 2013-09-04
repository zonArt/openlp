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

``/stage/api/poll``
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
import urllib.request, urllib.parse, urllib.error
import urllib.parse
import cherrypy

from mako.template import Template
from PyQt4 import QtCore

from openlp.core.lib import Registry, Settings, PluginStatus, StringContent, image_to_byte
from openlp.core.utils import AppLocation, translate

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


class HttpServer(object):
    """
    Ability to control OpenLP via a web browser.
    This class controls the Cherrypy server and configuration.
    """
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    def __init__(self):
        """
        Initialise the http server, and start the server.
        """
        log.debug('Initialise httpserver')
        self.settings_section = 'remotes'
        self.router = HttpRouter()

    def start_server(self):
        """
        Start the http server based on configuration.
        """
        log.debug('Start CherryPy server')
        # Define to security levels and inject the router code
        self.root = self.Public()
        self.root.files = self.Files()
        self.root.stage = self.Stage()
        self.root.main = self.Main()
        self.root.router = self.router
        self.root.files.router = self.router
        self.root.stage.router = self.router
        self.root.main.router = self.router
        cherrypy.tree.mount(self.root, '/', config=self.define_config())
        # Turn off the flood of access messages cause by poll
        cherrypy.log.access_log.propagate = False
        cherrypy.engine.start()

    def define_config(self):
        """
        Define the configuration of the server.
        """
        if Settings().value(self.settings_section + '/https enabled'):
            port = Settings().value(self.settings_section + '/https port')
            address = Settings().value(self.settings_section + '/ip address')
            local_data = AppLocation.get_directory(AppLocation.DataDir)
            cherrypy.config.update({'server.socket_host': str(address),
                                    'server.socket_port': port,
                                    'server.ssl_certificate': os.path.join(local_data, 'remotes', 'openlp.crt'),
                                    'server.ssl_private_key': os.path.join(local_data, 'remotes', 'openlp.key')})
        else:
            port = Settings().value(self.settings_section + '/port')
            address = Settings().value(self.settings_section + '/ip address')
            cherrypy.config.update({'server.socket_host': str(address)})
            cherrypy.config.update({'server.socket_port': port})
        cherrypy.config.update({'environment': 'embedded'})
        cherrypy.config.update({'engine.autoreload_on': False})
        directory_config = {'/': {'tools.staticdir.on': True,
                                'tools.staticdir.dir': self.router.html_dir,
                                'tools.basic_auth.on': Settings().value('remotes/authentication enabled'),
                                'tools.basic_auth.realm': 'OpenLP Remote Login',
                                'tools.basic_auth.users': fetch_password,
                                'tools.basic_auth.encrypt': make_sha_hash},
                         '/files': {'tools.staticdir.on': True,
                                     'tools.staticdir.dir': self.router.html_dir,
                                     'tools.basic_auth.on': False},
                         '/stage': {'tools.staticdir.on': True,
                                     'tools.staticdir.dir': self.router.html_dir,
                                     'tools.basic_auth.on': False},
                         '/main': {'tools.staticdir.on': True,
                                     'tools.staticdir.dir': self.router.html_dir,
                                     'tools.basic_auth.on': False}}
        return directory_config

    class Public(object):
        """
        Main access class with may have security enabled on it.
        """
        @cherrypy.expose
        def default(self, *args, **kwargs):
            self.router.request_data = None
            if isinstance(kwargs, dict):
                self.router.request_data = kwargs.get('data', None)
            url = urllib.parse.urlparse(cherrypy.url())
            return self.router.process_http_request(url.path, *args)

    class Files(object):
        """
        Provides access to files and has no security available.  These are read only accesses
        """
        @cherrypy.expose
        def default(self, *args, **kwargs):
            url = urllib.parse.urlparse(cherrypy.url())
            return self.router.process_http_request(url.path, *args)

    class Stage(object):
        """
        Stage view is read only so security is not relevant and would reduce it's usability
        """
        @cherrypy.expose
        def default(self, *args, **kwargs):
            url = urllib.parse.urlparse(cherrypy.url())
            return self.router.process_http_request(url.path, *args)

    class Main(object):
        """
        Main view is read only so security is not relevant and would reduce it's usability
        """
        @cherrypy.expose
        def default(self, *args, **kwargs):
            url = urllib.parse.urlparse(cherrypy.url())
            return self.router.process_http_request(url.path, *args)

    def close(self):
        """
        Close down the http server.
        """
        log.debug('close http server')
        cherrypy.engine.exit()


class HttpRouter(object):
    """
    This code is called by the HttpServer upon a request and it processes it based on the routing table.
    """
    def __init__(self):
        """
        Initialise the router
        """
        self.routes = [
            ('^/$', self.serve_file),
            ('^/(stage)$', self.serve_file),
            ('^/(main)$', self.serve_file),
            (r'^/files/(.*)$', self.serve_file),
            (r'^/api/poll$', self.poll),
            (r'^/stage/poll$', self.poll),
            (r'^/main/poll$', self.main_poll),
            (r'^/main/image$', self.main_image),
            (r'^/api/controller/(live|preview)/(.*)$', self.controller),
            (r'^/stage/controller/(live|preview)/(.*)$', self.controller),
            (r'^/api/service/(.*)$', self.service),
            (r'^/stage/service/(.*)$', self.service),
            (r'^/api/display/(hide|show|blank|theme|desktop)$', self.display),
            (r'^/api/alert$', self.alert),
            (r'^/api/plugin/(search)$', self.plugin_info),
            (r'^/api/(.*)/search$', self.search),
            (r'^/api/(.*)/live$', self.go_live),
            (r'^/api/(.*)/add$', self.add_to_service)
        ]
        self.translate()
        self.html_dir = os.path.join(AppLocation.get_directory(AppLocation.PluginsDir), 'remotes', 'html')

    def process_http_request(self, url_path, *args):
        """
        Common function to process HTTP requests

        ``url_path``
            The requested URL.

        ``*args``
            Any passed data.
        """
        response = None
        for route, func in self.routes:
            match = re.match(route, url_path)
            if match:
                log.debug('Route "%s" matched "%s"', route, url_path)
                args = []
                for param in match.groups():
                    args.append(param)
                response = func(*args)
                break
        if response:
            return response
        else:
            log.debug('Path not found %s', url_path)
            return self._http_not_found()

    def _get_service_items(self):
        """
        Read the service item in use and return the data as a json object
        """
        service_items = []
        if self.live_controller.service_item:
            current_unique_identifier = self.live_controller.service_item.unique_identifier
        else:
            current_unique_identifier = None
        for item in self.service_manager.service_items:
            service_item = item['service_item']
            service_items.append({
                'id': str(service_item.unique_identifier),
                'title': str(service_item.get_display_title()),
                'plugin': str(service_item.name),
                'notes': str(service_item.notes),
                'selected': (service_item.unique_identifier == current_unique_identifier)
            })
        return service_items

    def translate(self):
        """
        Translate various strings in the mobile app.
        """
        self.template_vars = {
            'app_title': translate('RemotePlugin.Mobile', 'OpenLP 2.1 Remote'),
            'stage_title': translate('RemotePlugin.Mobile', 'OpenLP 2.1 Stage View'),
            'live_title': translate('RemotePlugin.Mobile', 'OpenLP 2.1 Live View'),
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

    def serve_file(self, file_name=None):
        """
        Send a file to the socket. For now, just a subset of file types and must be top level inside the html folder.
        If subfolders requested return 404, easier for security for the present.

        Ultimately for i18n, this could first look for xx/file.html before falling back to file.html.
        where xx is the language, e.g. 'en'
        """
        log.debug('serve file request %s' % file_name)
        if not file_name:
            file_name = 'index.html'
        elif file_name == 'stage':
            file_name = 'stage.html'
        elif file_name == 'main':
            file_name = 'main.html'
        path = os.path.normpath(os.path.join(self.html_dir, file_name))
        if not path.startswith(self.html_dir):
            return self._http_not_found()
        ext = os.path.splitext(file_name)[1]
        html = None
        if ext == '.html':
            mimetype = 'text/html'
            variables = self.template_vars
            html = Template(filename=path, input_encoding='utf-8', output_encoding='utf-8').render(**variables)
        elif ext == '.css':
            mimetype = 'text/css'
        elif ext == '.js':
            mimetype = 'application/x-javascript'
        elif ext == '.jpg':
            mimetype = 'image/jpeg'
        elif ext == '.gif':
            mimetype = 'image/gif'
        elif ext == '.png':
            mimetype = 'image/png'
        else:
            mimetype = 'text/plain'
        file_handle = None
        try:
            if html:
                content = html
            else:
                file_handle = open(path, 'rb')
                log.debug('Opened %s' % path)
                content = file_handle.read()
        except IOError:
            log.exception('Failed to open %s' % path)
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
            'service': self.service_manager.service_id,
            'slide': self.live_controller.selected_row or 0,
            'item': self.live_controller.service_item.unique_identifier if self.live_controller.service_item else '',
            'twelve': Settings().value('remotes/twelve hour'),
            'blank': self.live_controller.blank_screen.isChecked(),
            'theme': self.live_controller.theme_screen.isChecked(),
            'display': self.live_controller.desktop_screen.isChecked()
        }
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'results': result}).encode()

    def main_poll(self):
        """
        Poll OpenLP to determine the current slide count.
        """
        result = {
            'slide_count': self.live_controller.slide_count
        }
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'results': result}).encode()

    def main_image(self):
        """
        Return the latest display image as a byte stream.
        """
        result = {
            'slide_image': 'data:image/png;base64,' + str(image_to_byte(self.live_controller.slide_image))
        }
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'results': result}).encode()

    def display(self, action):
        """
        Hide or show the display screen.
        This is a cross Thread call and UI is updated so Events need to be used.

        ``action``
            This is the action, either ``hide`` or ``show``.
        """
        self.live_controller.emit(QtCore.SIGNAL('slidecontroller_toggle_display'), action)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'results': {'success': True}}).encode()

    def alert(self):
        """
        Send an alert.
        """
        plugin = self.plugin_manager.get_plugin_by_name("alerts")
        if plugin.status == PluginStatus.Active:
            try:
                text = json.loads(self.request_data)['request']['text']
            except KeyError as ValueError:
                return self._http_bad_request()
            text = urllib.parse.unquote(text)
            self.alerts_manager.emit(QtCore.SIGNAL('alerts_text'), [text])
            success = True
        else:
            success = False
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'results': {'success': success}}).encode()

    def controller(self, display_type, action):
        """
        Perform an action on the slide controller.

        ``display_type``
            This is the type of slide controller, either ``preview`` or ``live``.

        ``action``
            The action to perform.
        """
        event = 'slidecontroller_%s_%s' % (display_type, action)
        if action == 'text':
            current_item = self.live_controller.service_item
            data = []
            if current_item:
                for index, frame in enumerate(current_item.get_frames()):
                    item = {}
                    if current_item.is_text():
                        if frame['verseTag']:
                            item['tag'] = str(frame['verseTag'])
                        else:
                            item['tag'] = str(index + 1)
                        item['text'] = str(frame['text'])
                        item['html'] = str(frame['html'])
                    else:
                        item['tag'] = str(index + 1)
                        item['text'] = str(frame['title'])
                        item['html'] = str(frame['title'])
                    item['selected'] = (self.live_controller.selected_row == index)
                    data.append(item)
            json_data = {'results': {'slides': data}}
            if current_item:
                json_data['results']['item'] = self.live_controller.service_item.unique_identifier
        else:
            if self.request_data:
                try:
                    data = json.loads(self.request_data)['request']['id']
                except KeyError as ValueError:
                    return self._http_bad_request()
                log.info(data)
                # This slot expects an int within a list.
                self.live_controller.emit(QtCore.SIGNAL(event), [data])
            else:
                self.live_controller.emit(QtCore.SIGNAL(event))
            json_data = {'results': {'success': True}}
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(json_data).encode()

    def service(self, action):
        """
        Handles requests for service items in the service manager

        ``action``
            The action to perform.
        """
        event = 'servicemanager_%s' % action
        if action == 'list':
            cherrypy.response.headers['Content-Type'] = 'application/json'
            return json.dumps({'results': {'items': self._get_service_items()}}).encode()
        event += '_item'
        if self.request_data:
            try:
                data = json.loads(self.request_data)['request']['id']
            except KeyError:
                return self._http_bad_request()
            self.service_manager.emit(QtCore.SIGNAL(event), data)
        else:
            Registry().execute(event)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'results': {'success': True}}).encode()

    def plugin_info(self, action):
        """
        Return plugin related information, based on the action.

        ``action``
            The action to perform. If *search* return a list of plugin names
            which support search.
        """
        if action == 'search':
            searches = []
            for plugin in self.plugin_manager.plugins:
                if plugin.status == PluginStatus.Active and plugin.media_item and plugin.media_item.has_search:
                    searches.append([plugin.name, str(plugin.text_strings[StringContent.Name]['plural'])])
            cherrypy.response.headers['Content-Type'] = 'application/json'
            return json.dumps({'results': {'items': searches}}).encode()

    def search(self, plugin_name):
        """
        Return a list of items that match the search text.

        ``plugin``
            The plugin name to search in.
        """
        try:
            text = json.loads(self.request_data)['request']['text']
        except KeyError as ValueError:
            return self._http_bad_request()
        text = urllib.parse.unquote(text)
        plugin = self.plugin_manager.get_plugin_by_name(plugin_name)
        if plugin.status == PluginStatus.Active and plugin.media_item and plugin.media_item.has_search:
            results = plugin.media_item.search(text, False)
        else:
            results = []
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'results': {'items': results}}).encode()

    def go_live(self, plugin_name):
        """
        Go live on an item of type ``plugin``.
        """
        try:
            id = json.loads(self.request_data)['request']['id']
        except KeyError as ValueError:
            return self._http_bad_request()
        plugin = self.plugin_manager.get_plugin_by_name(plugin_name)
        if plugin.status == PluginStatus.Active and plugin.media_item:
            plugin.media_item.emit(QtCore.SIGNAL('%s_go_live' % plugin_name), [id, True])
        return self._http_success()

    def add_to_service(self, plugin_name):
        """
        Add item of type ``plugin_name`` to the end of the service.
        """
        try:
            id = json.loads(self.request_data)['request']['id']
        except KeyError as ValueError:
            return self._http_bad_request()
        plugin = self.plugin_manager.get_plugin_by_name(plugin_name)
        if plugin.status == PluginStatus.Active and plugin.media_item:
            item_id = plugin.media_item.create_item_from_id(id)
            plugin.media_item.emit(QtCore.SIGNAL('%s_add_to_service' % plugin_name), [item_id, True])
        self._http_success()

    def _http_success(self):
        """
        Set the HTTP success return code.
        """
        cherrypy.response.status = 200

    def _http_bad_request(self):
        """
        Set the HTTP bad response return code.
        """
        cherrypy.response.status = 400

    def _http_not_found(self):
        """
        Set the HTTP not found return code.
        """
        cherrypy.response.status = 404
        cherrypy.response.body = [b'<html><body>Sorry, an error occurred </body></html>']

    def _get_service_manager(self):
        """
        Adds the service manager to the class dynamically
        """
        if not hasattr(self, '_service_manager'):
            self._service_manager = Registry().get('service_manager')
        return self._service_manager

    service_manager = property(_get_service_manager)

    def _get_live_controller(self):
        """
        Adds the live controller to the class dynamically
        """
        if not hasattr(self, '_live_controller'):
            self._live_controller = Registry().get('live_controller')
        return self._live_controller

    live_controller = property(_get_live_controller)

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, '_plugin_manager'):
            self._plugin_manager = Registry().get('plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)

    def _get_alerts_manager(self):
        """
        Adds the alerts manager to the class dynamically
        """
        if not hasattr(self, '_alerts_manager'):
            self._alerts_manager = Registry().get('alerts_manager')
        return self._alerts_manager

    alerts_manager = property(_get_alerts_manager)
