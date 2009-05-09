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
import logging

from time import sleep
from copy import deepcopy

from PyQt4 import QtCore, QtGui

from openlp.core.lib import OpenLPToolbar
from openlp.core.lib import ServiceItem
from openlp.core.lib import RenderManager
from openlp.core import translate
from openlp.core.lib import Event, EventType, EventManager

class ServiceData(QtCore.QAbstractItemModel):
    """
    Tree of items for an order of service.
    Includes methods for reading and writing the contents to an OOS file
    Root contains a list of ServiceItems
    """
    global log
    log=logging.getLogger(u'ServiceData')
    def __init__(self):
        QtCore.QAbstractItemModel.__init__(self)
        self.items=[]
        log.info("Starting")

    def clearItems(self):
        self.items = []

    def columnCount(self, parent=None):
        return 1; # always only a single column (for now)

    def rowCount(self, parent=None):
        return len(self.items)

    def insertRow(self, row, service_item):
        self.beginInsertRows(QtCore.QModelIndex(),row,row)
        log.info("insert row %s:%s" % (row,service_item))
        self.items.insert(row, service_item)
        log.info("Items: %s" % self.items)
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, service_item):
        self.insertRow(len(self.items), service_item)

    def index(self, row, col, parent = QtCore.QModelIndex()):
        return self.createIndex(row,col)

    def parent(self, index=QtCore.QModelIndex()):
        return QtCore.QModelIndex() # no children as yet

    def data(self, index, role):
        """
        Called by the service manager to draw us in the service window
        """
        log.debug(u'data %s %d', index, role)
        row = index.row()
        if row > len(self.items): # if the last row is selected and deleted, we then get called with an empty row!
            return QtCore.QVariant()
        item = self.items[row]
        if role == QtCore.Qt.DisplayRole:
            retval= item.title + u':' + item.shortname
        elif role == QtCore.Qt.DecorationRole:
            retval = item.iconic_representation
        elif role == QtCore.Qt.ToolTipRole:
            retval = None
        else:
            retval = None
        if retval == None:
            retval = QtCore.QVariant()
#         log.info("Returning"+ str(retval))
        if type(retval) is not type(QtCore.QVariant):
            return QtCore.QVariant(retval)
        else:
            return retval

    def __iter__(self):
        for i in self.items:
            yield i

    def item(self, row):
        log.info("Get Item:%d -> %s" %(row, str(self.items)))
        return self.items[row]


class ServiceManager(QtGui.QWidget):

    """Manages the orders of service.  Currently this involves taking
    text strings from plugins and adding them to an OOS file. In
    future, it will also handle zipping up all the resources used into
    one lump.
    Also handles the UI tasks of moving things up and down etc.
    """
    global log
    log=logging.getLogger(u'ServiceManager')

    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent=parent
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton(u'Move to top', u':/services/service_top.png',
            translate(u'ServiceManager', u'Move to top'), self.onServiceTop)
        self.Toolbar.addToolbarButton(u'Move up', u':/services/service_up.png',
            translate(u'ServiceManager', u'Move up order'), self.onServiceUp)
        self.Toolbar.addToolbarButton(u'Move down', u':/services/service_down.png',
            translate(u'ServiceManager', u'Move down order'), self.onServiceDown)
        self.Toolbar.addToolbarButton(u'Move to bottom', u':/services/service_bottom.png',
            translate(u'ServiceManager', u'Move to end'), self.onServiceEnd)
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton(u'New Service', u':/services/service_new.png',
            translate(u'ServiceManager', u'Create a new Service'), self.onNewService)
        self.Toolbar.addToolbarButton(u'Delete From Service', u':/services/service_delete.png',
            translate(u'ServiceManager', u'Delete From Service'), self.onDeleteFromService)
        self.Toolbar.addSeparator()
        self.Toolbar.addToolbarButton(u'Save Service', u':/services/service_save.png',
            translate(u'ServiceManager', u'Save Service'), self.onSaveService)
        self.Toolbar.addToolbarButton(u'Load Service', u':/services/service_open.png',
            translate(u'ServiceManager', u'Load Existing'), self.onLoadService)

        self.Toolbar.addSeparator()
        self.ThemeComboBox = QtGui.QComboBox(self.Toolbar)
        self.ThemeComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.ThemeWidget.setDefaultWidget(self.ThemeComboBox)
        self.Toolbar.addAction(self.ThemeWidget)
        self.Layout.addWidget(self.Toolbar)

        self.serviceManagerList = QtGui.QTreeWidget(self)
        self.serviceManagerList.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.serviceManagerList.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.serviceManagerList.setAlternatingRowColors(True)
        self.serviceManagerList.setObjectName("serviceManagerList")
        self.serviceManagerList .__class__.dragEnterEvent=self.dragEnterEvent
        self.serviceManagerList .__class__.dragMoveEvent=self.dragEnterEvent
        self.serviceManagerList .__class__.dropEvent =self.dropEvent

        self.Layout.addWidget(self.serviceManagerList)

        QtCore.QObject.connect(self.ThemeComboBox,
            QtCore.SIGNAL("activated(int)"), self.onThemeComboBoxSelected)

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
        treewidgetitem = QtGui.QTreeWidgetItem(self.serviceManagerList)
        treewidgetitem.setText(0,item.title + u':' + item.shortname)
        treewidgetitem.setIcon(0,item.iconic_representation)
        treewidgetitem.setExpanded(True)
        item.render()
        for frame in item.frames:
            treewidgetitem1 = QtGui.QTreeWidgetItem(treewidgetitem)
            text = frame[u'formatted'][0]
            treewidgetitem1.setText(0,text[:10])
            #treewidgetitem1.setIcon(0,frame[u'image'])

    def dragEnterEvent(self, event):
        """
        Accept Drag events
        """
        event.accept()

    def dropEvent(self, event):
        """
        Handle the release of the event and trigger the plugin
        to add the data
        """
        link=event.mimeData()
        if link.hasText():
            plugin = event.mimeData().text()
            self.eventManager.post_event(Event(EventType.LoadServiceItem, plugin))

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
        """
        Called from ThemeManager when the Themes have changed
        """
        self.ThemeComboBox.clear()
        for theme in theme_list:
            self.ThemeComboBox.addItem(theme)
            self.renderManager.default_theme = self.ThemeComboBox.currentText()

