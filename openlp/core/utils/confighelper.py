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

class ConfigHelper(object):
    """
    Utility Helper to allow classes to find directories in a standard manner.
    """
    @staticmethod
    def get_data_path():
        if os.name == 'nt':
            default = os.path.join(os.path.expanduser(u'~'),
                u'Application Data', u'.openlp', u'data')
        else:
            default = os.path.expanduser(u'~/.openlp/data')

        reg = ConfigHelper.get_registry()
        path = ConfigHelper.get_config('main', 'data path', default)

        if not os.path.exists(path):
            os.makedirs(path)
 
        return path

    @staticmethod
    def get_config(section, key, default=None):
        reg = ConfigHelper.get_registry()
        if reg.has_value(section, key):
            return reg.get_value(section, key, default)
        else:
            if default is not None:
                ConfigHelper.set_config(section, key, default)
            return default

    @staticmethod
    def set_config(section, key, value):
        reg = ConfigHelper.get_registry()
        if not reg.has_section(section):
            reg.create_section(section)
        return reg.set_value(section, key, value)

    @staticmethod
    def get_registry():
        """
        This static method loads the appropriate registry class based on the
        current operating system, and returns an instantiation of that class.
        """
        reg = None
        if os.name == 'nt':
            from winregistry import WinRegistry
            reg = WinRegistry(r'\Software\openlp')
        else:
            from linregistry import LinRegistry
            reg = LinRegistry(os.path.join(os.getenv('HOME'), '.openlp'))
        return reg
