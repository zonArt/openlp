# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80
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

class Plugin(object):
    """
    Base class for openlp plugins to inherit from.

    Basic attributes are:
    name: the name that should appear in the plugins list
    version: The version number of this iteration of the plugin (just an incrementing integer!)
    paint_context: A list of paint contexts?
    """

    def __init__(self, name=None, version=None):
        """
        This is the constructor for the plugin object. This provides an easy
        way for descendent plugins to populate common data.
        """
        if name is not None:
            self.Name = name
        else:
            self.Name = 'Plugin'
        if version is not None:
            self.__version__ = version
        # this will be a MediaManagerItem if it needs one
        self.MediaManagerItem = None
        # this will be a PrefsPage object if it needs one
        self.SettingsTab = None
        #self.paint_context = None

    def save(self, data):
        """
        Service item data is passed to this function, which should return a
        string which can be written to the service file
        """
        pass
    def load(self, str):
        """
        A string from the service file is passed in. This function parses and
        sets up the internals of the plugin
        """
        pass

    def render(self, screen=None):
        """
        Render the screenth screenful of data to self.paint_conext
        """
        pass

    def __repr__(self):
        return '<Plugin %s>' % self.__class__.__name__


