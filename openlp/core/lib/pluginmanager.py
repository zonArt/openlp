# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from openlp.core.lib import Plugin, PluginStatus

log = logging.getLogger(__name__)

class PluginManager(object):
    """
    This is the Plugin manager, which loads all the plugins,
    and executes all the hooks, as and when necessary.
    """
    log.info(u'Plugin manager loaded')

    @staticmethod
    def get_instance():
        """
        Obtain a single instance of class.
        """
        return PluginManager.instance

    def __init__(self, plugin_dir):
        """
        The constructor for the plugin manager. Passes the controllers on to
        the plugins for them to interact with via their ServiceItems.

        ``plugin_dir``
            The directory to search for plugins.
        """
        log.info(u'Plugin manager Initialising')
        PluginManager.instance = self
        if not plugin_dir in sys.path:
            log.debug(u'Inserting %s into sys.path', plugin_dir)
            sys.path.insert(0, plugin_dir)
        self.basepath = os.path.abspath(plugin_dir)
        log.debug(u'Base path %s ', self.basepath)
        self.plugins = []
        log.info(u'Plugin manager Initialised')

    def find_plugins(self, plugin_dir, plugin_helpers):
        """
        Scan the directory ``plugin_dir`` for objects inheriting from the
        ``Plugin`` class.

        ``plugin_dir``
            The directory to scan.

        ``plugin_helpers``
            A list of helper objects to pass to the plugins.

        """
        log.info(u'Finding plugins')
        startdepth = len(os.path.abspath(plugin_dir).split(os.sep))
        log.debug(u'finding plugins in %s at depth %d',
            unicode(plugin_dir), startdepth)
        for root, dirs, files in os.walk(plugin_dir):
            for name in files:
                if name.endswith(u'.py') and not name.startswith(u'__'):
                    path = os.path.abspath(os.path.join(root, name))
                    thisdepth = len(path.split(os.sep))
                    if thisdepth - startdepth > 2:
                        # skip anything lower down
                        continue
                    modulename = os.path.splitext(path)[0]
                    prefix = os.path.commonprefix([self.basepath, path])
                    # hack off the plugin base path
                    modulename = modulename[len(prefix) + 1:]
                    modulename = modulename.replace(os.path.sep, '.')
                    # import the modules
                    log.debug(u'Importing %s from %s. Depth %d',
                        modulename, path, thisdepth)
                    try:
                        __import__(modulename, globals(), locals(), [])
                    except ImportError, e:
                        log.exception(u'Failed to import module %s on path %s '
                            'for reason %s', modulename, path, e.args[0])
        plugin_classes = Plugin.__subclasses__()
        plugin_objects = []
        for p in plugin_classes:
            try:
                plugin = p(plugin_helpers)
                log.debug(u'Loaded plugin %s', unicode(p))
                plugin_objects.append(plugin)
            except TypeError:
                log.exception(u'Failed to load plugin %s', unicode(p))
        plugins_list = sorted(plugin_objects, self.order_by_weight)
        for plugin in plugins_list:
            if plugin.checkPreConditions():
                log.debug(u'Plugin %s active', unicode(plugin.name))
                plugin.setStatus()
            else:
                plugin.status = PluginStatus.Disabled
            self.plugins.append(plugin)

    def order_by_weight(self, x, y):
        """
        Sort two plugins and order them by their weight.

        ``x``
            The first plugin.

        ``y``
            The second plugin.
        """
        return cmp(x.weight, y.weight)

    def hook_media_manager(self, mediadock):
        """
        Loop through all the plugins. If a plugin has a valid media manager
        item, add it to the media manager.

        ``mediatoolbox``
            The Media Manager itself.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.mediaItem = plugin.getMediaManagerItem()

    def hook_settings_tabs(self, settings_form=None):
        """
        Loop through all the plugins. If a plugin has a valid settings tab
        item, add it to the settings tab.
        Tabs are set for all plugins not just Active ones

        ``settingsform``
            Defaults to *None*. The settings form to add tabs to.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.settings_tab = plugin.getSettingsTab(settings_form)
            else:
                plugin.settings_tab = None
        settings_form.plugins = self.plugins

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
            log.info(u'initialising plugins %s in a %s state'
                % (plugin.name, plugin.isActive()))
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
        Return the plugin which has a name with value ``name``
        """
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        return None
