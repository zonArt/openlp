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

import types
from PyQt4 import QtCore, QtGui

class PluginUtils(object):
    def __init__(self):
        """
        IClass for plugin helpers so the Plugin class is just a simple interface
        """
        pass

    def add_separator(self, base):
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
