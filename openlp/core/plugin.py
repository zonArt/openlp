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
    * Name
        The name that should appear in the plugins list.
    * Version
        The version number of this iteration of the plugin.
    * MediaManagerItem
        An instance of the MediaManagerItem class, used in the Media Manager.
    * SettingsTab
        An instance of the SettingsTab class, used in the Settings dialog.
    * ImportMenuItem
        A menu item to be placed in the Import menu.
    * ExportMenuItem
        A menu item to be placed in the Export menu.

    Hook functions:
    * about()
        Used in the plugin manager, when a person clicks on the 'About' button.
    * save(data)
        A method to convert the plugin's data to a string to be stored in the
        Service file.
    * load(string)
        A method to convert the string from a Service file into the plugin's
        own data format.
    * render(theme, screen_number)
        A method used to render something to the screen, given the current theme
        and screen number.
    * addToMenu(menubar)
        A method to add a menu item to anywhere in the menu, given the menu bar.
    * handleEvent(event)
        A method use to handle events, given an Event object.
    """

    def __init__(self, name=None, version=None):
        """
        This is the constructor for the plugin object. This provides an easy
        way for descendent plugins to populate common data. This method *must*
        be overridden, like so:
        class MyPlugin(Plugin):
            def __init__(self):
                Plugin.__init(self, 'MyPlugin', '0.1')
                ...
        """
        if name is not None:
            self.Name = name
        else:
            self.Name = 'Plugin'
        if version is not None:
            self.__version__ = version
        self.MediaManagerItem = None
        self.SettingsTab = None
        self.ImportMenuItem = None
        self.ExportMenuItem = None

    def about(self):
        """
        Show a dialog when the user clicks on the 'About' button in the plugin
        manager.
        """
        pass

    def save(self, data):
        """
        Service item data is passed to this function, which should return a
        string which can be written to the service file.
        """
        pass

    def load(self, string):
        """
        A string from the service file is passed in. This function parses and
        sets up the internals of the plugin.
        """
        pass

    def render(self, theme, screen=None):
        """
        Render the screenth screenful of data using theme settings in theme.
        """
        pass

    def addToMenu(self, menubar):
        """
        Add menu items to the menu, given the menubar.
        """
        pass

    def handleEvent(self, event):
        """
        Handle the event contained in the event object.
        """
        pass
