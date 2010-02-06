# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

import os
import sys
import logging

from openlp.core.lib import Plugin, PluginStatus

class PluginManager(object):
    """
    This is the Plugin manager, which loads all the plugins,
    and executes all the hooks, as and when necessary.
    """
    global log
    log = logging.getLogger(u'PluginMgr')
    log.info(u'Plugin manager loaded')

    def __init__(self, dir):
        """
        The constructor for the plugin manager. Passes the controllers on to
        the plugins for them to interact with via their ServiceItems.

        ``dir``
            The directory to search for plugins.
        """
        log.info(u'Plugin manager initing')
        if not dir in sys.path:
            log.debug(u'Inserting %s into sys.path', dir)
            sys.path.insert(0, dir)
        self.basepath = os.path.abspath(dir)
        log.debug(u'Base path %s ', self.basepath)
        self.plugins = []
        # this has to happen after the UI is sorted self.find_plugins(dir)
        log.info(u'Plugin manager Initialised')

    def find_plugins(self, dir, plugin_helpers):
        """
        Scan the directory ``dir`` for objects inheriting from the ``Plugin``
        class.

        ``dir``
            The directory to scan.

        ``plugin_helpers``
            A list of helper objects to pass to the plugins.

        """
        self.plugin_helpers = plugin_helpers
        startdepth = len(os.path.abspath(dir).split(os.sep))
        log.debug(u'find plugins %s at depth %d', unicode(dir), startdepth)

        for root, dirs, files in os.walk(dir):
            for name in files:
                if name.endswith(u'.py') and not name.startswith(u'__'):
                    path = os.path.abspath(os.path.join(root, name))
                    thisdepth = len(path.split(os.sep))
                    if thisdepth-startdepth > 2:
                        # skip anything lower down
                        continue
                    modulename, pyext = os.path.splitext(path)
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
                        log.exception(u'Failed to import module %s on path %s for reason %s',
                                   modulename, path, e.args[0])
        plugin_classes = Plugin.__subclasses__()
        plugin_objects = []
        for p in plugin_classes:
            try:
                plugin = p(self.plugin_helpers)
                log.debug(u'Loaded plugin %s with helpers', unicode(p))
                plugin_objects.append(plugin)
            except TypeError:
                log.error(u'loaded plugin %s has no helpers', unicode(p))
        plugins_list = sorted(plugin_objects, self.order_by_weight)
        for plugin in plugins_list:
            if plugin.check_pre_conditions():
                log.debug(u'Plugin %s active', unicode(plugin.name))
                plugin.set_status()
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
                plugin.media_item = plugin.get_media_manager_item()

    def hook_settings_tabs(self, settingsform=None):
        """
        Loop through all the plugins. If a plugin has a valid settings tab
        item, add it to the settings tab.
        Tabs are set for all plugins not just Active ones

        ``settingsform``
            Defaults to *None*. The settings form to add tabs to.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.settings_tab = plugin.get_settings_tab()
                if plugin.settings_tab:
                    log.debug(u'Inserting settings tab item from %s' %
                        plugin.name)
                    settingsform.addTab(plugin.name, plugin.settings_tab)
                else:
                    log.debug(u'No tab settings in %s' % plugin.name)

    def hook_import_menu(self, import_menu):
        """
        Loop through all the plugins and give them an opportunity to add an
        item to the import menu.

        ``import_menu``
            The Import menu.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.add_import_menu_item(import_menu)

    def hook_export_menu(self, export_menu):
        """
        Loop through all the plugins and give them an opportunity to add an
        item to the export menu.

        ``export_menu``
            The Export menu.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.add_export_menu_item(export_menu)

    def hook_tools_menu(self, tools_menu):
        """
        Loop through all the plugins and give them an opportunity to add an
        item to the tools menu.

        ``tools_menu``
            The Tools menu.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.add_tools_menu_item(tools_menu)

    def initialise_plugins(self):
        """
        Loop through all the plugins and give them an opportunity to
        initialise themselves.
        """
        for plugin in self.plugins:
            log.info(u'initialising plugins %s in a %s state'
                % (plugin.name, plugin.is_active()))
            if plugin.is_active():
                plugin.initialise()
                log.info(u'Initialisation Complete for %s ' % plugin.name)
            if not plugin.is_active():
                plugin.remove_toolbox_item()

    def finalise_plugins(self):
        """
        Loop through all the plugins and give them an opportunity to
        clean themselves up
        """
        log.info(u'finalising plugins')
        for plugin in self.plugins:
            if plugin.is_active():
                plugin.finalise()
                log.info(u'Finalisation Complete for %s ' % plugin.name)
