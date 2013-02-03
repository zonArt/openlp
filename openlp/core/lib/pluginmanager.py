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
        if not plugin_dir in sys.path:
            log.debug(u'Inserting %s into sys.path', plugin_dir)
            sys.path.insert(0, plugin_dir)
        self.basepath = os.path.abspath(plugin_dir)
        log.debug(u'Base path %s ', self.basepath)
        self.plugins = []
        log.info(u'Plugin manager Initialised')

    def find_plugins(self, plugin_dir):
        """
        Scan the directory ``plugin_dir`` for objects inheriting from the
        ``Plugin`` class.

        ``plugin_dir``
            The directory to scan.

        """
        log.info(u'Finding plugins')
        startdepth = len(os.path.abspath(plugin_dir).split(os.sep))
        log.debug(u'finding plugins in %s at depth %d',
            unicode(plugin_dir), startdepth)
        for root, dirs, files in os.walk(plugin_dir):
            # TODO Presentation plugin is not yet working on Mac OS X.
            # For now just ignore it. The following code will hide it
            # in settings dialog.
            if sys.platform == 'darwin':
                present_plugin_dir = os.path.join(plugin_dir, 'presentations')
                # Ignore files from the presentation plugin directory.
                if root.startswith(present_plugin_dir):
                    continue
            for name in files:
                if name.endswith(u'.py') and not name.startswith(u'__'):
                    path = os.path.abspath(os.path.join(root, name))
                    thisdepth = len(path.split(os.sep))
                    if thisdepth - startdepth > 2:
                        # skip anything lower down
                        break
                    modulename = os.path.splitext(path)[0]
                    prefix = os.path.commonprefix([self.basepath, path])
                    # hack off the plugin base path
                    modulename = modulename[len(prefix) + 1:]
                    modulename = modulename.replace(os.path.sep, '.')
                    # import the modules
                    log.debug(u'Importing %s from %s. Depth %d', modulename, path, thisdepth)
                    try:
                        __import__(modulename, globals(), locals(), [])
                    except ImportError, e:
                        log.exception(u'Failed to import module %s on path %s for reason %s',
                            modulename, path, e.args[0])
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

    def hook_settings_tabs(self, settings_form=None):
        """
        Loop through all the plugins. If a plugin has a valid settings tab
        item, add it to the settings tab.
        Tabs are set for all plugins not just Active ones

        ``settings_form``
            Defaults to *None*. The settings form to add tabs to.
        """
        for plugin in self.plugins:
            if plugin.status is not PluginStatus.Disabled:
                plugin.createSettingsTab(settings_form)
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

