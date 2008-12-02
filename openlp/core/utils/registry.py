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

class Registry(object):
    """
    The Registry class is a generic class for the accessing configurations.
    """
    def __init__(self):
        """
        Initialise the Registry object. Override this to add custom initialisation.
        """
        pass

    def has_value(self, section, key):
        """
        Check if a value exists.
        """
        pass

    def create_value(self, section, key):
        """
        Create a new value in the registry.
        """
        pass

    def get_value(self, section, key):
        """
        Get a single value from the registry.
        """
        pass

    def set_value(self, section, key, value):
        """
        Set a single value in the registry.
        """
        pass

    def delete_value(self, section, key):
        """
        Delete a single value from the registry.
        """
        pass

    def has_section(self, section):
        """
        Check if a section exists.
        """
        return False

    def create_section(self, section):
        """
        Create a new section in the registry.
        """
        pass

    def delete_section(self, section):
        """
        Delete a section (including all values).
        """
        pass
