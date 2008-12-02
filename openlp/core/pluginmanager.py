# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
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

import os
import sys
import logging

from openlp.core.lib import Plugin

class PluginManager(object):
    """
    This is the Plugin manager, which loads all the plugins,
    and executes all the hooks, as and when necessary.
    """
    global log
    log=logging.getLogger("PluginMgr")
    log.info("Plugin manager loaded")

    def __init__(self, dir):
        """
        The constructor for the plugin manager. This does a, b and c.
        """
        log.info("Plugin manager initing")
        if not dir in sys.path:
            log.debug("Inserting %s into sys.path", dir)
            sys.path.insert(0, dir)
        self.basepath = os.path.abspath(dir)
        log.debug("Base path %s ", self.basepath)
        self.plugins = []
        self.find_plugins(dir)
        log.info("Plugin manager done init")

    def find_plugins(self, dir):
        """
        Scan the directory dir for objects inheriting from openlp.plugin
        """
        log.debug("find plugins " + str(dir))
        for root, dirs, files in os.walk(dir):
            for name in files:
                if name.endswith(".py") and not name.startswith("__"):
                    path = os.path.abspath(os.path.join(root, name))
                    modulename, pyext = os.path.splitext(path)
                    prefix = os.path.commonprefix([self.basepath, path])
                    # hack off the plugin base path
                    modulename = modulename[len(prefix) + 1:]
                    modulename = modulename.replace('/', '.')
                    # import the modules
                    log.debug("Importing %s from %s." % (modulename, path))
                    try:
                        __import__(modulename, globals(), locals(), [])
                    except ImportError, e:
                        print e.message
        self.plugin_classes = Plugin.__subclasses__()
        self.plugins = []
        plugin_objects = []
        for p in self.plugin_classes:
            plugin = p()
            plugin_objects.append(plugin)
        self.plugins = sorted(plugin_objects, self.orderByWeight)

    def orderByWeight(self, x, y):
        return cmp(x.Weight, y.Weight)

    def hookMediaManager(self, mediatoolbox):
        """
        Loop through all the plugins. If a plugin has a valid media manager item,
        add it to the media manager.
        """
        for plugin in self.plugins:
            media_manager_item = plugin.getMediaManagerItem()
            if media_manager_item is not None:
                log.debug('Inserting media manager item from %s' % plugin.Name)
                mediatoolbox.addItem(media_manager_item, plugin.Icon, media_manager_item.Title)

    def hookHandleEvent(self, event):
        pass
