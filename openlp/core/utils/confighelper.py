# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008-2009 Raoul Snyman
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
from openlp.core.utils.registry import Registry

class ConfigHelper(object):
    """
    Utility Helper to allow classes to find directories in a standard manner.
    """
    __registry__ = None

    @staticmethod
    def get_data_path():
        if os.name == u'nt':
            # ask OS for path to application data, set on Windows XP and Vista
            path = os.path.join(os.getenv(u'APPDATA'), u'openlp', u'data')
        elif os.name == u'mac':
            path = os.path.join(os.getenv(u'HOME'), u'Library',
                u'Application Support', u'openlp', u'Data')
        else:
            try:
                from xdg import BaseDirectory
                path = os.path.join(BaseDirectory.xdg_data_home, u'openlp')
            except ImportError:
                path = os.path.join(os.getenv(u'HOME'), u'.openlp', u'data')
        reg = ConfigHelper.get_registry()
        #path = ConfigHelper.get_config('main', 'data path', path)
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
    def delete_config(section, key):
        reg = ConfigHelper.get_registry()
        reg.delete_value(section, key)

    @staticmethod
    def get_registry():
        """
        This static method loads the appropriate registry class based on the
        current operating system, and returns an instantiation of that class.
        """
        if ConfigHelper.__registry__ is None:
            config_path = u''
            if os.name == u'nt':
                config_path = os.path.join(os.getenv(u'APPDATA'), u'openlp')
            elif os.name == u'mac':
                config_path = os.path.join(os.getenv(u'HOME'), u'Library',
                    u'Application Support', u'openlp')
            else:
                try:
                    from xdg import BaseDirectory
                    config_path = os.path.join(BaseDirectory.xdg_config_home, u'openlp')
                except ImportError:
                    config_path = os.path.join(os.getenv(u'HOME'), u'.openlp')
            ConfigHelper.__registry__ = Registry(config_path)
        return ConfigHelper.__registry__
