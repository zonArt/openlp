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
Provide plugin management
"""
import os
import sys
import logging
import imp

from openlp.core.lib import Plugin, PluginStatus, Registry

log = logging.getLogger(__name__)


class PluginManager(object):
    """
    This is the Plugin manager, which loads all the plugins,
    and executes all the hooks, as and when necessary.
    """
    log.info(u'Plugin manager loaded')

    def __init__(self, plugin_dir):
        """
        The constructor for the plugin manager. Passes the controllers on to
        the plugins for them to interact with via their ServiceItems.

        ``plugin_dir``
            The directory to search for plugins.
        """
        log.info(u'Plugin manager Initialising')
        Registry().register(u'plugin_manager', self)
        self.base_path = os.path.abspath(plugin_dir)
        log.debug(u'Base path %s ', self.base_path)
        self.plugins = []
        log.info(u'Plugin manager Initialised')

    def find_plugins(self):
        """
        Scan a directory for objects inheriting from the ``Plugin`` class.
        """
        log.info(u'Finding plugins')
        start_depth = len(os.path.abspath(self.base_path).split(os.sep))
        present_plugin_dir = os.path.join(self.base_path, 'presentations')
        log.debug(u'finding plugins in %s at depth %d', unicode(self.base_path), start_depth)
        for root, dirs, files in os.walk(self.base_path):
            if sys.platform == 'darwin' and root.startswith(present_plugin_dir):
                # TODO Presentation plugin is not yet working on Mac OS X.
                # For now just ignore it. The following code will ignore files from the presentation plugin directory
                # and thereby never import the plugin.
                continue
            for name in files:
                if name.endswith(u'.py') and not name.startswith(u'__'):
                    path = os.path.abspath(os.path.join(root, name))
                    this_depth = len(path.split(os.sep))
                    if this_depth - start_depth > 2:
                        # skip anything lower down
                        break
                    module_name = name[:-3]
                    # import the modules
                    log.debug(u'Importing %s from %s. Depth %d', module_name, root, this_depth)
                    try:
                        # Use the "imp" library to try to get around a problem with the PyUNO library which
                        # monkey-patches the __import__ function to do some magic. This causes issues with our tests.
                        # First, try to find the module we want to import, searching the directory in root
                        fp, path_name, description = imp.find_module(module_name, [root])
                        # Then load the module (do the actual import) using the details from find_module()
                        imp.load_module(module_name, fp, path_name, description)
                    except ImportError, e:
                        log.exception(u'Failed to import module %s on path %s: %s', module_name, path, e.args[0])
        plugin_classes = Plugin.__subclasses__()
        plugin_objects = []
        for p in plugin_classes:
            try:
                plugin = p()
                log.debug(u'Loaded plugin %s', unicode(p))
                plugin_objects.append(plugin)
            except TypeError:
                log.exception(u'Failed to load plugin %s', unicode(p))
        plugins_list = sorted(plugin_objects, key=lambda plugin: plugin.weight)
        for plugin in plugins_list:
            if plugin.checkPreConditions():
                log.debug(u'Plugin %s active', unicode(plugin.name))
                plugin.setStatus()
            else:
                plugin.status = PluginStatus.Disabled
            self.plugins.append(plugin)

    def hook_media_manager(self):
        """
        Create the plugins' media manager items.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.createMediaManagerItem()

    def hook_settings_tabs(self):
        """
        Loop through all the plugins. If a plugin has a valid settings tab
        item, add it to the settings tab.
        Tabs are set for all plugins not just Active ones

        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.createSettingsTab(self.settings_form)

    def hook_import_menu(self, import_menu):
        """
        Loop through all the plugins and give them an opportunity to add an
        item to the import menu.

        ``import_menu``
            The Import menu.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.addImportMenuItem(import_menu)

    def hook_export_menu(self, export_menu):
        """
        Loop through all the plugins and give them an opportunity to add an
        item to the export menu.

        ``export_menu``
            The Export menu.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.addExportMenuItem(export_menu)

    def hook_tools_menu(self, tools_menu):
        """
        Loop through all the plugins and give them an opportunity to add an
        item to the tools menu.

        ``tools_menu``
            The Tools menu.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.addToolsMenuItem(tools_menu)

    def initialise_plugins(self):
        """
        Loop through all the plugins and give them an opportunity to
        initialise themselves.
        """
        log.info(u'Initialise Plugins - Started')
        for plugin in self.plugins:
            log.info(u'initialising plugins %s in a %s state' % (plugin.name, plugin.isActive()))
            if plugin.isActive():
                plugin.initialise()
                log.info(u'Initialisation Complete for %s ' % plugin.name)
        log.info(u'Initialise Plugins - Finished')

    def finalise_plugins(self):
        """
        Loop through all the plugins and give them an opportunity to
        clean themselves up
        """
        log.info(u'finalising plugins')
        for plugin in self.plugins:
            if plugin.isActive():
                plugin.finalise()
                log.info(u'Finalisation Complete for %s ' % plugin.name)

    def get_plugin_by_name(self, name):
        """
        Return the plugin which has a name with value ``name``.
        """
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        return None

    def new_service_created(self):
        """
        Loop through all the plugins and give them an opportunity to handle a new service
        """
        log.info(u'plugins - new service created')
        for plugin in self.plugins:
            if plugin.isActive():
                plugin.new_service_created()

    #def _get_settings_form(self):
    #    """
    #    Adds the plugin manager to the class dynamically
    #    """
    #    if not hasattr(self, u'_settings_form'):
    #        self._settings_form = Registry().get(u'settings_form')
    #    return self._settings_form

    #settings_form = property(_get_settings_form)

