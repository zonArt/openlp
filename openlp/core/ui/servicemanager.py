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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# from openlp.core.resources import *
# from openlp.core.ui import AboutForm, AlertForm, SettingsForm, SlideController
from openlp.core.lib import OpenLPToolbar
from openlp.core.lib import ServiceItem
from openlp.core.lib import RenderManager
from openlp.core import translate

# from openlp.core import PluginManager
import logging

class ServiceData(QAbstractItemModel):
    """
    Tree of items for an order of service.
    Includes methods for reading and writing the contents to an OOS file
    Root contains a list of ServiceItems
    """
    global log
    log=logging.getLogger(u'ServiceData')
    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.items=[]
        log.info("Starting")

    def clearItems(self):
        self.items = []

    def columnCount(self, parent):
        return 1; # always only a single column (for now)

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, service_item):
        self.beginInsertRows(QModelIndex(),row,row)
        log.info("insert row %s:%s" % (row,service_item))
        self.items.insert(row, service_item)
        log.info("Items: %s" % self.items)
        self.endInsertRows()

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
        Called by the service manager to draw us in the service window
        """
        log.debug(u'data %s %d', index, role)
        row=index.row()
        if row > len(self.items): # if the last row is selected and deleted, we then get called with an empty row!
            return QVariant()
        item=self.items[row]
        if role==Qt.DisplayRole:
            retval= item.title + u':' + item.shortname
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


class ServiceManager(QWidget):

    """Manages the orders of service.  Currently this involves taking
    text strings from plugins and adding them to an OOS file. In
    future, it will also handle zipping up all the resources used into
    one lump.
    Also handles the UI tasks of moving things up and down etc.
    """
    global log
    log=logging.getLogger(u'ServiceManager')

    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent=parent
        self.Layout = QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton("Move to top", ":/services/service_top.png",
            translate(u'ServiceManager', u'Move to start'), self.onServiceTop)
        self.Toolbar.addToolbarButton("Move up", ":/services/service_up.png",
            translate(u'ServiceManager', u'Move up order'), self.onServiceUp)
        self.Toolbar.addToolbarButton("Move down", ":/services/service_down.png",
            translate(u'ServiceManager', u'Move down order'), self.onServiceDown)
        self.Toolbar.addToolbarButton("Move to bottom", ":/services/service_bottom.png",
            translate(u'ServiceManager', u'Move to end'), self.onServiceEnd)
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton("New Service", ":/services/service_new.png",
            translate(u'ServiceManager', u'Create a new Service'), self.onNewService)
        self.Toolbar.addToolbarButton("Delete From Service", ":/services/service_delete.png",
            translate(u'ServiceManager', u'Delete From Service'), self.onDeleteFromService)
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton("Save Service", ":/services/service_save.png",
            translate(u'ServiceManager', u'Save Service'), self.onSaveService)
        self.Toolbar.addToolbarButton("Load Service", ":/services/service_open.png",
            translate(u'ServiceManager', u'Load Existing'), self.onLoadService)

        self.Toolbar.addSeparator()
        self.ThemeComboBox = QComboBox(self.Toolbar)
        self.ThemeComboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.ThemeWidget = QWidgetAction(self.Toolbar)
        self.ThemeWidget.setDefaultWidget(self.ThemeComboBox)
        self.Toolbar.addAction(self.ThemeWidget)

        self.Layout.addWidget(self.Toolbar)

        self.TreeView = QTreeView(self)
        self.service_data=ServiceData()
        self.TreeView.setModel(self.service_data)
        self.TreeView.setAlternatingRowColors(True)
        self.Layout.addWidget(self.TreeView)

        QObject.connect(self.ThemeComboBox,
            SIGNAL("activated(int)"), self.onThemeComboBoxSelected)

    def onServiceTop(self):
        pass

    def onServiceUp(self):
        pass

    def onServiceDown(self):
        pass

    def onServiceEnd(self):
        pass

    def onNewService(self):
        self.service_data.clearItems()

    def onDeleteFromService(self):
        pass

    def onSaveService(self):
        Pass

    def onLoadService(self):
        Pass




    def onThemeComboBoxSelected(self, currentIndex):
        self.renderManager.default_theme = self.ThemeComboBox.currentText()

    def addServiceItem(self, item):
        """Adds service item"""
        log.info("addServiceItem")
        indexes=self.TreeView.selectedIndexes()
        assert len(indexes) <= 1 # can only have one selected index in this view
        if indexes == []:
            log.info("No row")
            row = None
            selected_item = None
        else:
            row=indexes[0].row()
            # if currently selected is of correct type, add it to it
            log.info("row:%d"%row)
            selected_item=self.service_data.item(row)

        if type(selected_item) == type(item):
            log.info("Add to existing item")
            selected_item.add(item)
        else:
            log.info("Create new item")
            if row is None:
                self.service_data.addRow(item)
            else:
                self.service_data.insertRow(row+1, item)

    def removeServiceItem(self):
        """Remove currently selected item"""
        pass

    def oos_as_text(self):
        text=[]
        log.info( "oos as text")
        log.info("Data:"+str(self.service_data))
        for i in self.service_data:
            text.append("# " + str(i))
            text.append(i.get_oos_text())
        return '\n'.join(text)

    def write_oos(self, filename):
        """
        Write a full OOS file out - iterate over plugins and call their respective methods
        This format is totally arbitrary testing purposes - something sensible needs to go in here!
        """
        oosfile=open(filename, "w")
        oosfile.write("# BEGIN OOS\n")
        oosfile.write(self.oos_as_text)
        oosfile.write("# END OOS\n")
        oosfile.close()

    def updateThemeList(self, theme_list):
        self.ThemeComboBox.clear()
        for theme in theme_list:
            self.ThemeComboBox.addItem(theme)
            self.renderManager.default_theme = self.ThemeComboBox.currentText()

