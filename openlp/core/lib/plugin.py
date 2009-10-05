# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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
from PyQt4 import QtCore

from openlp.core.lib import PluginConfig, Receiver

class PluginStatus(object):
    """
    Defines the status of the plugin
    """
    Active = 0
    Inactive = 1
    Disabled = 2

class Plugin(object):
    """
    Base class for openlp plugins to inherit from.

    **Basic Attributes**

    ``name``
        The name that should appear in the plugins list.

    ``version``
        The version number of this iteration of the plugin.

    ``icon``
        An instance of QIcon, which holds an icon for this plugin.

    ``config``
        An instance of PluginConfig, which allows plugins to read and write to
        openlp.org's configuration. This is pre-instantiated.

    ``log``
        A log object used to log debugging messages. This is pre-instantiated.

    ``weight``
        A numerical value used to order the plugins.

    **Hook Functions**

    ``check_pre_conditions()``
        Provides the Plugin with a handle to check if it can be loaded.

    ``get_media_manager_item()``
        Returns an instance of MediaManagerItem to be used in the Media Manager.

    ``add_import_menu_item(import_menu)``
        Add an item to the Import menu.

    ``add_export_menu_item(export_menu)``
        Add an item to the Export menu.

    ``get_settings_tab()``
        Returns an instance of SettingsTabItem to be used in the Settings dialog.

    ``add_to_menu(menubar)``
        A method to add a menu item to anywhere in the menu, given the menu bar.

    ``handle_event(event)``
        A method use to handle events, given an Event object.

    ``about()``
        Used in the plugin manager, when a person clicks on the 'About' button.

    """
    global log
    log = logging.getLogger(u'Plugin')
    log.info(u'loaded')

    def __init__(self, name=None, version=None, plugin_helpers=None):
        """
        This is the constructor for the plugin object. This provides an easy
        way for descendent plugins to populate common data. This method *must*
        be overridden, like so::

            class MyPlugin(Plugin):
                def __init__(self):
                    Plugin.__init(self, u'MyPlugin', u'0.1')

        ``name``
            Defaults to *None*. The name of the plugin.

        ``version``
            Defaults to *None*. The version of the plugin.

        ``plugin_helpers``
            Defaults to *None*. A list of helper objects.
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
        self.media_id = -1
        self.settings_id = -1
        self.media_active = False
        self.status = PluginStatus.Inactive
        # Set up logging
        self.log = logging.getLogger(self.name)
        self.preview_controller = plugin_helpers[u'preview']
        self.live_controller = plugin_helpers[u'live']
        self.render_manager = plugin_helpers[u'render']
        self.service_manager = plugin_helpers[u'service']
        self.settings = plugin_helpers[u'settings']
        self.mediatoolbox = plugin_helpers[u'toolbox']
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_add_service_item'% self.name), self.process_add_service_event)

    def check_pre_conditions(self):
        """
        Provides the Plugin with a handle to check if it can be loaded.
        Failing Preconditions does not stop a settings Tab being created

        Returns True or False.
        """
        return True

    def can_be_disabled(self):
        """
        Indicates whether the plugin can be disabled by the plugin list.

        Returns True or False.
        """
        return False

    def set_status(self):
        """
        Sets the status of the plugin
        """
        self.status = self.config.get_config(\
            u'%s_status' % self.name, PluginStatus.Inactive)

    def toggle_status(self, new_status):
        """
        Changes the status of the plugin and remembers it
        """
        self.status = new_status
        self.config.set_config(u'%s_status' % self.name, self.status)

    def is_active(self):
        """
        Indicates if the plugin is active

        Returns True or False.
        """
        return int(self.status ) == int(PluginStatus.Active)

    def get_media_manager_item(self):
        """
        Construct a MediaManagerItem object with all the buttons and things
        you need, and return it for integration into openlp.org.
        """
        pass

    def add_import_menu_item(self, import_menu):
        """
        Create a menu item and add it to the "Import" menu.

        ``import_menu``
            The Import menu.
        """
        pass

    def add_export_menu_item(self, export_menu):
        """
        Create a menu item and add it to the "Export" menu.

        ``export_menu``
            The Export menu
        """
        pass

    def add_tools_menu_item(self, tools_menu):
        """
        Create a menu item and add it to the "Tools" menu.

        ``tools_menu``
            The Tools menu
        """
        pass

    def get_settings_tab(self):
        """
        Create a tab for the settings window.
        """
        pass

    def add_to_menu(self, menubar):
        """
        Add menu items to the menu, given the menubar.

        ``menubar``
            The application's menu bar.
        """
        pass

    def process_add_service_event(self):
        """
        Generic Drag and drop handler triggered from service_manager.
        """
        log.debug(u'process_add_service_event event called for plugin %s' % self.name)
        self.media_item.onAddClick()

    def about(self):
        """
        Show a dialog when the user clicks on the 'About' button in the plugin
        manager.
        """
        pass

    def initialise(self):
        """
        Called by the plugin Manager to initialise anything it needs.
        """
        if self.media_item is not None:
            self.media_item.initialise()

    def finalise(self):
        """
        Called by the plugin Manager to cleanup things.
        """
        pass

    def remove_toolbox_item(self):
        """
        Called by the plugin to remove toolbar
        """
        if self.media_id is not -1:
            self.mediatoolbox.removeItem(self.media_id)
        if self.settings_id is not -1:
            self.settings.removeTab(self.settings_id)
        self.media_active = False

    def insert_toolbox_item(self):
        """
        Called by plugin to replace toolbar
        """
        if not self.media_active:
            if self.media_id is not -1:
                self.mediatoolbox.insertItem(
                    self.media_id, self.media_item, self.icon, self.media_item.title)
            if self.settings_id is not -1:
                self.settings.insertTab(
                    self.settings_id, self.settings_tab)
            self.media_active = True
