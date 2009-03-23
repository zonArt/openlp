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
from copy import deepcopy
from PyQt4 import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from openlp.core.resources import *
# from openlp.core.ui import AboutForm, AlertForm, SettingsForm, SlideController
from openlp.core.lib import OpenLPToolbar
#from openlp.core.lib import ThemeItem

# from openlp.core import PluginManager
import logging

class ThemeData(QAbstractItemModel):
    """
    Tree of items for an order of Theme.
    Includes methods for reading and writing the contents to an OOS file
    Root contains a list of ThemeItems
    """
    global log
    log=logging.getLogger(u'ThemeData')
    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.items=[]
        log.info("Starting")
    def columnCount(self, parent):
        return 1; # always only a single column (for now)
    def rowCount(self, parent):
        return len(self.items)
    def insertRow(self, row, Theme_item):
#         self.beginInsertRows(QModelIndex(),row,row)
        log.info("insert row %d:%s"%(row,Theme_item))
        self.items.insert(row, Theme_item)
        log.info("Items: %s" % self.items)
#         self.endInsertRows()
    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()
    def addRow(self, item):
        self.insertRow(len(self.items), item)
        
    def index(self, row, col, parent = QModelIndex()):
        return self.createIndex(row,col)

    def parent(self, index=QModelIndex()):
        return QModelIndex() # no children as yet
    def data(self, index, role):
        """
        Called by the Theme manager to draw us in the Theme window
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
        
    def __iter__(self):
        for i in self.items:
            yield i

    def item(self, row):
        log.info("Get Item:%d -> %s" %(row, str(self.items)))
        return self.items[row]

    
class ThemeManager(QWidget):

    """Manages the orders of Theme.  Currently this involves taking
    text strings from plugins and adding them to an OOS file. In
    future, it will also handle zipping up all the resources used into
    one lump.
    Also handles the UI tasks of moving things up and down etc.
    """
    global log
    log=logging.getLogger(u'ThemeManager')

    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent=parent
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton("New Theme", ":/themes/theme_new.png")
        self.Toolbar.addToolbarButton("Edit Theme", ":/themes/theme_edit.png")
        self.Toolbar.addToolbarButton("Delete Theme", ":/themes/theme_delete.png")
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton("Import Theme", ":/themes/theme_import.png")
        self.Toolbar.addToolbarButton("Export Theme", ":/themes/theme_export.png")        
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.Toolbar.addAction(self.ThemeWidget)

        self.Layout.addWidget(self.Toolbar)

        self.TreeView = QtGui.QTreeView(self)
        self.Theme_data=ThemeData()
        self.TreeView.setModel(self.Theme_data)
        self.Layout.addWidget(self.TreeView)
        
#    def addThemeItem(self, item):
#        """Adds Theme item"""
#        log.info("addThemeItem")
#        indexes=self.TreeView.selectedIndexes()
#        assert len(indexes) <= 1 # can only have one selected index in this view
#        if indexes == []:
#            log.info("No row")
#            row = None
#            selected_item = None
#        else:
#            row=indexes[0].row()
#            # if currently selected is of correct type, add it to it
#            log.info("row:%d"%row)
#            selected_item=self.Theme_data.item(row)
#        if type(selected_item) == type(item):
#            log.info("Add to existing item")
#            selected_item.add(item)
#        else:
#            log.info("Create new item")
#            if row is None:
#                self.Theme_data.addRow(item)
#            else:
#                self.Theme_data.insertRow(row+1, item)
#                
#    def removeThemeItem(self):
#        """Remove currently selected item"""
#        pass
#
#    def oos_as_text(self):
#        text=[]
#        log.info( "oos as text")
#        log.info("Data:"+str(self.Theme_data))
#        for i in self.Theme_data:
#            text.append("# " + str(i))
#            text.append(i.get_oos_text())
#        return '\n'.join(text)
#
#    def write_oos(self, filename):
#        """
#        Write a full OOS file out - iterate over plugins and call their respective methods
#        This format is totally arbitrary testing purposes - something sensible needs to go in here!
#        """
#        oosfile=open(filename, "w")
#        oosfile.write("# BEGIN OOS\n")
#        oosfile.write(self.oos_as_text)
#        oosfile.write("# END OOS\n")
#        oosfile.close()
        
    def get_themes(self):
        return [u'Theme A', u'Theme B']

