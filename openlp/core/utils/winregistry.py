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
import _winreg
import types

from openlp.core.utils import Registry

class WinRegistry(Registry):
    """
    The WinRegistry class is a high-level wrapper class for the Windows registry
    functions in Python.
    """
    def __init__(self, base_key):
        """
        Connection to the Windows registry, and save the handle.
        """
        self.reg_handle = _winreg.CreateConnection(None, _winreg.HKEY_CURRENT_USER)
        self.base_key = base_key
        if not self.base_key.endswith('\\'):
            self.base_key = self.base_key + '\\'

    def has_value(self, section, key):
        """
        Check if a key/value exists.
        """
        key_handle = _winreg.OpenKey(self.reg_handle, self.base_key + section)
        value, reg_type = _winreg.QueryValueEx(key_handle, key)[0]
        _winreg.CloseKey(key_handle)
        if reg_type == _winreg.REG_NONE:
            return False
        elif reg_type == _winreg.REG_SZ and value == '':
            return False
        elif reg_type == _winreg.REG_DWORD and value == 0:
            return False
        else:
            return True

    def get_value(self, section, key):
        """
        Get a single value from the Windows registry.
        """
        key_handle = _winreg.OpenKey(self.reg_handle, self.base_key + section)
        value = _winreg.QueryValueEx(key_handle, key)[0]
        _winreg.CloseKey(key_handle)
        return value

    def set_value(self, section, key, value):
        """
        Set a single value in the Windows registry.
        """
        reg_type = _winreg.REG_BINARY
        if type(value) is types.String:
            reg_type = _winreg.REG_SZ
        elif type(value) is types.Integer:
            reg_type = _winreg.REG_DWORD
        key_handle = _winreg.OpenKey(self.reg_handle, self.base_key + section)
        _winreg.SetValueEx(key_handle, key, 0, reg_type, value)
        _winreg.CloseKey(key_handle)

    def delete_value(self, section, key):
        """
        Delete a value from the Windows registry.
        """
        key_handle = _winreg.OpenKey(self.reg_handle, self.base_key + section)
        _winreg.DeleteValue(key_handle, key)
        _winreg.CloseKey(key_handle)

    def has_section(self, section):
        """
        Check if a section exists.
        """
        try:
            key_handle = _winreg.OpenKey(self.reg_handle, self.base_key + section)
        except EnvironmentError:
            return False
        finally:
            _winreg.CloseKey(key_handle)
            return True

    def create_section(self, section):
        """
        Create a new section in the Windows registry.
        """
        try:
            _winreg.CreateKey(self.reg_handle, self.base_key + section)
            return True
        except EnvironmentError:
            return False

    def delete_section(self, section):
        try:
            key_handle = _winreg.OpenKey(self.reg_handle, self.base_key)
            _winreg.DeleteKey(key_handle, section)
        except EnvironmentError:
            return False
        finally:
            _winreg.CloseKey(key_handle)
            return True
