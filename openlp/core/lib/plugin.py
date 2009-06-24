# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

import logging

from openlp.core.lib import PluginConfig
# why does this not work???
# from openlp.core.lib import Event,  EventType
# so I have to do this???
from event import Event, EventType

class Plugin(object):
    """
    Base class for openlp plugins to inherit from.

    Basic attributes are:
    * name
        The name that should appear in the plugins list.
    * version
        The version number of this iteration of the plugin.
    * icon
        An instance of QIcon, which holds an icon for this plugin.
    * config
        An instance of PluginConfig, which allows plugins to read and write to
        openlp.org's configuration. This is pre-instantiated.
    * log
        A log object used to log debugging messages. This is pre-instantiated.

    Hook functions:
    * check_pre_conditions()
        Provides the Plugin with a handle to check if it can be loaded.
    * get_media_manager_item()
        Returns an instance of MediaManagerItem to be used in the Media Manager.
    * add_import_menu_item(import_menu)
        Add an item to the Import menu.
    * add_export_menu_item(export_menu)
        Add an item to the Export menu.
    * get_settings_tab()
        Returns an instance of SettingsTabItem to be used in the Settings dialog.
    * add_to_menu(menubar)
        A method to add a menu item to anywhere in the menu, given the menu bar.
    * handle_event(event)
        A method use to handle events, given an Event object.
    * about()
        Used in the plugin manager, when a person clicks on the 'About' button.
    * save(data)
        A method to convert the plugin's data to a string to be stored in the
        Service file.
    * load(string)
        A method to convert the string from a Service file into the plugin's
        own data format.
    * render(theme, screen_number)
        A method used to render something to the screen, given the current theme
        and screen number.
    """
    global log
    log = logging.getLogger(u'Plugin')
    log.info(u'loaded')

    def __init__(self, name=None, version=None, plugin_helpers=None):
        """
        This is the constructor for the plugin object. This provides an easy
        way for descendent plugins to populate common data. This method *must*
        be overridden, like so:
        class MyPlugin(Plugin):
            def __init__(self):
                Plugin.__init(self, 'MyPlugin', '0.1')
                ...
        """
        if name is not None:
            self.name = name
        else:
            self.name = u'Plugin'
        if version is not None:
            self.version = version
        self.icon = None
        self.config = PluginConfig(self.name)
        self.weight = 0
        # Set up logging
        self.log = logging.getLogger(self.name)
        self.preview_controller = plugin_helpers[u'preview']
        self.live_controller = plugin_helpers[u'live']
        self.theme_manager = plugin_helpers[u'theme']
        self.event_manager = plugin_helpers[u'event']
        self.render_manager = plugin_helpers[u'render']
        self.service_manager = plugin_helpers[u'service']
        self.settings= plugin_helpers[u'settings']
        self.dnd_id=None

    def check_pre_conditions(self):
        """
        Provides the Plugin with a handle to check if it can be loaded.
        Returns True or False.
        """
        return True

    def get_media_manager_item(self):
        """
        Construct a MediaManagerItem object with all the buttons and things you
        need, and return it for integration into openlp.org.
        """
        pass

    def add_import_menu_item(self, import_menu):
        """
        Create a menu item and add it to the "Import" menu.
        """
        pass

    def add_export_menu_item(self, export_menu):
        """
        Create a menu item and add it to the "Export" menu.
        """
        pass

    def get_settings_tab(self):
        """
        Create a menu item and add it to the "Import" menu.
        """
        pass

    def add_to_menu(self, menubar):
        """
        Add menu items to the menu, given the menubar.
        """
        pass

    def handle_event(self, event):
        """
        Handle the event contained in the event object.
        """
    def handle_event(self, event):
        """
        Handle the event contained in the event object.  If you want
        to use this default behaviour, you must set self.dnd_id equal
        to that sent by the dnd source - eg the MediaItem
        """
        # default behaviour - can be overridden if desired
        log.debug(u'Handle event called with event %s with payload %s'%(event.event_type, event.payload))
        if event.event_type == EventType.LoadServiceItem and event.payload == self.dnd_id:
            log.debug(u'Load Service Item received')
            self.media_item.onAddClick()
        if event.event_type == EventType.PreviewShow and event.payload == self.dnd_id:
            log.debug(u'Load Preview Item received')
            self.media_item.onPreviewClick()
        if event.event_type == EventType.LiveShow and event.payload == self.dnd_id:
            log.debug(u'Load Live Show Item received')
            self.media_item.onLiveClick()

    def about(self):
        """
        Show a dialog when the user clicks on the 'About' button in the plugin
        manager.
        """
        pass

    def save(self, data):
        """
        Service item data is passed to this function, which should return a
        string which can be written to the service file.
        """
        pass

    def load(self, string):
        """
        A string from the service file is passed in. This function parses and
        sets up the internals of the plugin.
        """
        pass

    def render(self, theme, screen=None):
        """
        Render the screenth screenful of data using theme settings in theme.
        """
        pass

    def initialise(self):
        """
        Called by the plugin Manager to initialise anything it needs.
        """
        pass

