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
import types
from PyQt4 import QtCore, QtGui

class PluginUtils(object):
    """
    Extension class for plugin helpers so the Plugin class is just a simple interface
    """
    def add_to_context_separator(self, base):
        action = QtGui.QAction("", base)
        action.setSeparator(True)
        return action
        
    def add_to_context_menu(self, base, icon, text, slot):
        """
        Utility method to help build context menus for plugins
        """        
        if type(icon) is QtGui.QIcon:
            ButtonIcon = icon
        elif type(icon) is types.StringType:
            ButtonIcon = QtGui.QIcon()
            if icon.startswith(':/'):
                ButtonIcon.addPixmap(QtGui.QPixmap(icon), QtGui.QIcon.Normal,
                    QtGui.QIcon.Off)
            else:
                ButtonIcon.addPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(icon)),
                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    
        action = QtGui.QAction(text, base)
        action .setIcon(ButtonIcon)
        QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"), slot)
        return action
        
    def _load_display_list(self):
        """
        Load a display list from the config files
        """
        listcount = self.config.get_config("List Count")
        list = []
        if listcount != None:
            for i in range(0 ,  int(listcount)):
                x = self.config.get_config("List Item "+str(i))
                list.append(x)
        return list
            
    def _save_display_list(self, displaylist):
        """
        Save display list from the config files
        """
        c = displaylist.rowCount()
        self.config.set_config("List Count", str(c))
        for i in range (0, int(c)):
            self.config.set_config("List Item "+str(i), str(displaylist.item(i, 0).text()))            

    def _get_last_dir(self):
        """
        Read the last directory used for plugin
        """
        lastdir = self.config.get_config("Last Dir")
        if lastdir==None:
            lastdir = ""
        return lastdir
        
    def _save_last_directory(self, list):
        """
        Save the last directory used for plugin
        """        
        path ,  nm = os.path.split(str(list)) 
        self.config.set_config("Last Dir", path)
