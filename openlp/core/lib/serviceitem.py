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

class ServiceItem():
    """
    The service item is a base class for the plugins to use to interact with
    the service manager, the slide controller, and the projection screen
    compositor.
    """

    def __init__(self):
        """
        Init Method
        """
        pass
    
    def render(self):
        """
        The render method is what the plugin uses to render it's meda to the
        screen.
        """
        pass

    def get_parent_node(self):
        """
        This method returns a parent node to be inserted into the Service
        Manager. At the moment this has to be a QAbstractListModel based class
        """
        pass

    def get_oos_repr(self):
        """
        This method returns some text which can be saved into the OOS
        file to represent this item
        """
        pass

    def set_from_oos(self, oostext):
        """
        This method takes some oostext (passed from the ServiceManager)
        and parses it into the data actually required
        """
        pass

    def set_from_plugin(self, data):
        """
        Takes data from the plugin media chooser
        """
