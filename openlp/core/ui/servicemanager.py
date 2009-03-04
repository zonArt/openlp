# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2009 Raoul Snyman
Portions copyright (c) 2009 Martin Thompson, Tim Bentley,

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

from time import sleep
from PyQt4 import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from openlp.core.resources import *
# from openlp.core.ui import AboutForm, AlertForm, SettingsForm, SlideController
from openlp.core.lib import OpenLPToolbar
from openlp.core.lib import ServiceItem

# from openlp.core import PluginManager
import logging

class ServiceData(QAbstractItemModel):
    """
    Tree of items for an order of service.
    Includes methods for reading and writing the contents to an OOS file
    Root contains a list of ServiceItems
    """
    global log
    log=logging.getLogger("ServiceData")
    def __init__(self):
        self.items=[]
        log.info("Starting")
    def rowCount(self, parent):
        return len(self.items)
    def insertRow(self, row, service_item):
        self.beginInsertRows(QModelIndex(),row,row)
        log.info("insert row %d:%s"%(row,filename))
        self.items.insert(row, service_item)
        self.endInsertRows()
    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()
    def addRow(self, filename):
        self.insertRow(len(self.items), filename)
        
    
    def data(self, index, role):
        """
        Called by the service manager to draw us in the service window
        """
        row=index.row()
        if row > len(self.items): # if the last row is selected and deleted, we then get called with an empty row!
            return QVariant()
        item=self.items[row]
        if role==Qt.DisplayRole:
            retval= item.pluginname + ":" + item.shortname
        elif role == Qt.DecorationRole:
            retval = item.iconic_representation
        elif role == Qt.ToolTipRole:
            retval= None
        else:
            retval= None
        if retval == None:
            retval=QVariant()
#         log.info("Returning"+ str(retval))
        if type(retval) is not type(QVariant):
            return QVariant(retval)
        else:
            return retval
        
        

class ServiceManager(QWidget):

    """Manages the orders of service.  Currently this involves taking
    text strings from plugins and adding them to an OOS file. In
    future, it will also handle zipping up all the resources used into
    one lump"""

    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent=parent
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton("Move to top", ":/services/service_top.png")
        self.Toolbar.addToolbarButton("Move up", ":/services/service_up.png")
        self.Toolbar.addToolbarButton("Move down", ":/services/service_down.png")
        self.Toolbar.addToolbarButton("Move to bottom", ":/services/service_bottom.png")
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton("New Service", ":/services/service_new.png")
        self.Toolbar.addToolbarButton("Save Service", ":/services/service_save.png")
        self.Toolbar.addSeparator()
        self.ThemeComboBox = QtGui.QComboBox(self.Toolbar)
        self.ThemeComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.ThemeComboBox.addItem(QtCore.QString())
        self.ThemeComboBox.addItem(QtCore.QString())
        self.ThemeComboBox.addItem(QtCore.QString())
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.ThemeWidget.setDefaultWidget(self.ThemeComboBox)
        self.Toolbar.addAction(self.ThemeWidget)

        self.Layout.addWidget(self.Toolbar)

        self.TreeView = QtGui.QTreeView(self)
        self.service_data=ServiceData()
#         self.TreeView.setModel(self.service_data)
        self.Layout.addWidget(self.TreeView)
        
    def addServiceItem(self, item):
        """Adds service item"""
        pass

    def removeServiceItem(self):
        """Remove currently selected item"""
        pass
