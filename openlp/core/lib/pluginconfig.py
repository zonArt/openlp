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

import os

from openlp.core.utils import ConfigHelper

class PluginConfig(object):
    """
    This is a generic config helper for plugins.
    """
    def __init__(self, plugin_name):
        """
        Initialise the plugin config object, setting the section name to the
        plugin name.

        ``plugin_name``
            The name of the plugin to use as a section name.
        """
        self.section = plugin_name.lower()

    def get_config(self, key, default=None):
        """
        Get a configuration value from the configuration registry.

        ``key``
            The name of configuration to load.

        ``default``
            Defaults to *None*. The default value to return if there is no
            other value.
        """
        return ConfigHelper.get_config(self.section, key, default)

    def delete_config(self, key):
        """
        Delete a configuration value from the configuration registry.

        ``key``
            The name of the configuration to remove.
        """
        return ConfigHelper.delete_config(self.section, key)

    def set_config(self, key, value):
        """
        Set a configuration value in the configuration registry.

        ``key``
            The name of the configuration to save.

        ``value``
            The value of the configuration to save.
        """
        return ConfigHelper.set_config(self.section, key, value)

    def get_data_path(self):
        """
        Dynamically build the data file path for a plugin.
        """
        #app_data = ConfigHelper.get_data_path()
        app_data = ConfigHelper.get_data_path()
        safe_name = self.section.replace(u' ',u'-')
        plugin_data = self.get_config(u'data path', safe_name)
        path = os.path.join(app_data, plugin_data)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def set_data_path(self, path):
        """
        Set the data file path.

        ``path``
            The path to save.
        """
        return self.set_config(u'data path', os.path.basename(path))

    def get_files(self, suffix=None):
        """
        Get a list of files from the data files path.

        ``suffix``
            Defaults to *None*. The extension to search for.
        """
        try:
            files = os.listdir(self.get_data_path())
        except:
            return []
        if suffix:
            return_files = []
            for file in files:
                if file.find(u'.') != -1:
                    filename = file.split(u'.')
                    #bname = nme[0]
                    filesuffix = filename[1].lower()
                    filesuffix = filesuffix.lower()
                    # only load files with the correct suffix
                    if suffix.find(filesuffix) > -1 :
                        return_files.append(file)
            return return_files
        else:
            # no filtering required
            return files

    def load_list(self, name):
        """
        Load a list from the config file.

        ``name``
            The name of the list.
        """
        list_count = self.get_config(u'%s count' % name)
        if list_count:
            list_count = int(list_count)
        else:
            list_count = 0
        list = []
        if list_count > 0:
            for counter in range(0, list_count):
                item = unicode(self.get_config(u'%s %d' % (name, counter)))
                list.append(item)
        return list

    def set_list(self, name, list):
        """
        Save a list to the config file.

        ``name``
            The name of the list to save.

        ``list``
            The list of values to save.
        """
        old_count = int(self.get_config(u'%s count' % name, int(0)))
        new_count = len(list)
        self.set_config(u'%s count' % name, new_count)
        for counter in range (0, new_count):
            self.set_config(u'%s %d' % (name, counter), list[counter-1])
        if old_count > new_count:
            # Tidy up any old list itrms if list is smaller now
            for counter in range(new_count, old_count):
                self.delete_config(u'%s %d' % (name, counter))

    def get_last_dir(self, num=None):
        """
        Read the last directory used for plugin.

        ``num``
            Defaults to *None*. A further qualifier.
        """
        if num:
            name = u'last directory %d' % num
        else:
            name = u'last directory'
        last_dir = self.get_config(name)
        if not last_dir:
            last_dir = u''
        return last_dir

    def set_last_dir(self, directory, num=None):
        """
        Save the last directory used for plugin.

        ``num``
            Defaults to *None*. A further qualifier.
        """
        if num:
            name = u'last directory %d' % num
        else:
            name = u'last directory'
        self.set_config(name, directory)
