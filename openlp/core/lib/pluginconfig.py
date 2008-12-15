# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

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
from openlp.core.utils import ConfigHelper

class PluginConfig(object):
    """
    This is a generic config helper for plugins.
    """
    def __init__(self, plugin_name):
        """
        Initialise the plugin config object, setting the section name to the
        plugin name.
        """
        self.section = plugin_name.lower()

    def get_config(self, key, default=None):
        """
        Get a configuration value from the configuration registry.
        """
        return ConfigHelper.get_config(self.section, key, default)

    def set_config(self, key, value):
        """
        Set a configuration value in the configuration registry.
        """
        return ConfigHelper.set_config(self.section, key, value)

    def get_data_path(self):
        app_data = ConfigHelper.get_data_path()
        safe_name = self.section.replace(' ', '-')
        plugin_data = self.get_config('data path', safe_name)
        path = os.path.join(app_data, plugin_data)

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def set_data_path(self, path):
        return self.set_config('data path', os.path.basename(path))
        
    def get_files(self, default_suffixes=None):
        returnfiles = []        
        suffix = self.get_config("suffix name", default_suffixes)
        try:
            files = os.listdir(self.get_data_path()) 
        except:
            return returnfiles
        if suffix != None:
            for f in files:
                if f.find('.') != -1:
                    nme = f.split('.')
                    bname = nme[0]
                    sfx = nme[1].lower()
                    sfx = sfx.lower()
                    if suffix.find(sfx) > -1 : # only load files with the correct suffix
                        returnfiles.append(f)
            return returnfiles
        else:
            return files  # no filtering required
