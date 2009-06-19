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
import cPickle

from PyQt4 import QtCore, QtGui
from openlp.core.lib import PluginConfig, OpenLPToolbar, ServiceItem, Event, \
    RenderManager, EventType, EventManager, translate, buildIcon, \
    contextMenuAction, contextMenuSeparator

class ServiceManager(QtGui.QWidget):
    """
    Manages the orders of service.  Currently this involves taking
    text strings from plugins and adding them to an OOS file. In
    future, it will also handle zipping up all the resources used into
    one lump.
    Also handles the UI tasks of moving things up and down etc.
    """
    global log
    log = logging.getLogger(u'ServiceManager')

    def __init__(self, parent):
        """
        Sets up the service manager, toolbars, list view, et al.
        """
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.serviceItems = []
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        # Create the top toolbar
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton(u'New Service', u':/services/service_new.png',
            translate(u'ServiceManager', u'Create a new Service'), self.onNewService)
        self.Toolbar.addToolbarButton(u'Open Service', u':/services/service_open.png',
            translate(u'ServiceManager', u'Load Existing'), self.onLoadService)
        self.Toolbar.addToolbarButton(u'Save Service', u':/services/service_save.png',
            translate(u'ServiceManager', u'Save Service'), self.onSaveService)
        self.Toolbar.addSeparator()
        self.ThemeComboBox = QtGui.QComboBox(self.Toolbar)
        self.ThemeComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.ThemeWidget.setDefaultWidget(self.ThemeComboBox)
        self.Toolbar.addAction(self.ThemeWidget)
        self.Layout.addWidget(self.Toolbar)
        # Create the service manager list
        self.ServiceManagerList = QtGui.QTreeWidget(self)
        self.ServiceManagerList.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.ServiceManagerList.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.ServiceManagerList.setAlternatingRowColors(True)
        self.ServiceManagerList.setHeaderHidden(True)
        self.ServiceManagerList.setObjectName(u'ServiceManagerList')
        # enable drop
        self.ServiceManagerList.__class__.dragEnterEvent = self.dragEnterEvent
        self.ServiceManagerList.__class__.dragMoveEvent = self.dragEnterEvent
        self.ServiceManagerList.__class__.dropEvent = self.dropEvent
        # Add a context menu to the service manager list
        self.ServiceManagerList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ServiceManagerList.addAction(contextMenuAction(
            self.ServiceManagerList, ':/system/system_preview.png',
            translate(u'ServiceManager',u'&Preview Verse'), self.makePreview))
        self.ServiceManagerList.addAction(contextMenuAction(
            self.ServiceManagerList, ':/system/system_live.png',
            translate(u'ServiceManager',u'&Show Live'), self.makeLive))
        self.ServiceManagerList.addAction(contextMenuSeparator(self.ServiceManagerList))
        self.ServiceManagerList.addAction(contextMenuAction(
            self.ServiceManagerList, ':/services/service_delete',
            translate(u'ServiceManager',u'&Remove from Service'), self.onDeleteFromService))
        self.Layout.addWidget(self.ServiceManagerList)
        # Add the bottom toolbar
        self.OrderToolbar = OpenLPToolbar(self)
        self.OrderToolbar.addToolbarButton(u'Move to top', u':/services/service_top.png',
            translate(u'ServiceManager', u'Move to top'), self.onServiceTop)
        self.OrderToolbar.addToolbarButton(u'Move up', u':/services/service_up.png',
            translate(u'ServiceManager', u'Move up order'), self.onServiceUp)
        self.OrderToolbar.addToolbarButton(u'Move down', u':/services/service_down.png',
            translate(u'ServiceManager', u'Move down order'), self.onServiceDown)
        self.OrderToolbar.addToolbarButton(u'Move to bottom', u':/services/service_bottom.png',
            translate(u'ServiceManager', u'Move to end'), self.onServiceEnd)
        self.OrderToolbar.addSeparator()
        self.OrderToolbar.addToolbarButton(u'Delete From Service', u':/services/service_delete.png',
            translate(u'ServiceManager', u'Delete From Service'), self.onDeleteFromService)
        self.Layout.addWidget(self.OrderToolbar)
        # Connect up our signals and slots
        QtCore.QObject.connect(self.ThemeComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onThemeComboBoxSelected)
        QtCore.QObject.connect(self.ServiceManagerList,
           QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.makeLive)
        # Last little bits of setting up
        self.config = PluginConfig(u'Main')
        self.service_theme = self.config.get_config(u'theme service theme', u'')

    def onServiceTop(self):
        """
        Move the current ServiceItem to the top of the list
        """
        item, count = self.findServiceItem()
        if item < len(self.serviceItems) and item is not -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(0, temp)
            self.repaintServiceList()

    def onServiceUp(self):
        """
        Move the current ServiceItem up in the list
        Note move up means move to top of area  ie 0.
        """
        item, count = self.findServiceItem()
        if item > 0:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(item - 1, temp)
            self.repaintServiceList()

    def onServiceDown(self):
        """
        Move the current ServiceItem down in the list
        Note move down means move to bottom of area i.e len().
        """
        item, count = self.findServiceItem()
        if item < len(self.serviceItems) and item is not -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(item + 1, temp)
            self.repaintServiceList()

    def onServiceEnd(self):
        """
        Move the current ServiceItem to the bottom of the list
        """
        item, count = self.findServiceItem()
        if item < len(self.serviceItems) and item is not -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(len(self.serviceItems), temp)
            self.repaintServiceList()

    def onNewService(self):
        """
        Clear the list to create a new service
        """
        self.ServiceManagerList.clear()
        self.serviceItems = []

    def onDeleteFromService(self):
        """
        Remove the current ServiceItem from the list
        """
        item, count = self.findServiceItem()
        if item is not -1:
            self.serviceItems.remove(self.serviceItems[item])
            self.repaintServiceList()

    def repaintServiceList(self):
        #Correct order of idems in array
        count = 1
        for item in self.serviceItems:
            item[u'order'] = count
            count += 1
        #Repaint the screen
        self.ServiceManagerList.clear()
        for item in self.serviceItems:
            serviceitem = item[u'data']
            treewidgetitem = QtGui.QTreeWidgetItem(self.ServiceManagerList)
            treewidgetitem.setText(0,serviceitem.title)
            treewidgetitem.setIcon(0,serviceitem.iconic_representation)
            treewidgetitem.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(item[u'order']))
            count = 0
            for frame in serviceitem.frames:
                treewidgetitem1 = QtGui.QTreeWidgetItem(treewidgetitem)
                text = frame[u'title']
                treewidgetitem1.setText(0,text[:40])
                treewidgetitem1.setData(0, QtCore.Qt.UserRole,QtCore.QVariant(count))
                count = count + 1

    def onSaveService(self):
        """
        Save the current service
        """
        filename = QtGui.QFileDialog.getSaveFileName(self, u'Save Order of Service',self.config.get_last_dir() )
        if filename != u'':
            self.config.set_last_dir(filename)
            print filename
            service = []
            for item in self.serviceItems:
                service.append({u'serviceitem':item[u'data'].get_oos_repr()})
            file = open(filename+u'.oos', u'wb')
            cPickle.dump(service, file)
            file.close()

    def onLoadService(self):
        """
        Load an existing service from disk
        """
        filename = QtGui.QFileDialog.getOpenFileName(self, u'Open Order of Service',self.config.get_last_dir(),
            u'Services (*.oos)')
        if filename != u'':
            self.config.set_last_dir(filename)
            file = open(filename, u'r')
            items = cPickle.load(file)
            file.close()
            self.onNewService()
            for item in items:
                serviceitem = ServiceItem()
                serviceitem.RenderManager = self.parent.RenderManager
                serviceitem.set_from_oos(item)
                self.addServiceItem(serviceitem)

    def onThemeComboBoxSelected(self, currentIndex):
        """
        Set the theme for the current service
        """
        self.service_theme = self.ThemeComboBox.currentText()
        self.parent.RenderManager.set_service_theme(self.service_theme)
        self.config.set_config(u'theme service theme', self.service_theme)
        if len(self.serviceItems) > 0:
            tempServiceItems = self.serviceItems
            self.onNewService()
            for item in tempServiceItems:
                self.addServiceItem(item[u'data'])

    def addServiceItem(self, item, expand=True):
        """
        Add an item to the list
        """
        self.serviceItems.append({u'data': item, u'order': len(self.serviceItems)+1})
        treewidgetitem = QtGui.QTreeWidgetItem(self.ServiceManagerList)
        treewidgetitem.setText(0,item.title)
        treewidgetitem.setIcon(0,item.iconic_representation)
        treewidgetitem.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(len(self.serviceItems)))
        treewidgetitem.setExpanded(expand)
        item.render()
        count = 0
        for frame in item.frames:
            treewidgetitem1 = QtGui.QTreeWidgetItem(treewidgetitem)
            text = frame[u'title']
            treewidgetitem1.setText(0,text[:40])
            treewidgetitem1.setData(0, QtCore.Qt.UserRole,QtCore.QVariant(count))
            count = count + 1

    def makePreview(self):
        """
        Send the current item to the Preview slide controller
        """
        item, count = self.findServiceItem()
        self.parent.PreviewController.addServiceManagerItem(self.serviceItems[item][u'data'], count)

    def makeLive(self):
        """
        Send the current item to the Live slide controller
        """
        item, count = self.findServiceItem()
        self.parent.LiveController.addServiceManagerItem(self.serviceItems[item][u'data'], count)

    def findServiceItem(self):
        """
        Finds a ServiceItem in the list
        """
        items = self.ServiceManagerList.selectedItems()
        pos = 0
        count = 0
        for item in items:
            parentitem =  item.parent()
            if parentitem is None:
                pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
            else:
                pos = parentitem.data(0, QtCore.Qt.UserRole).toInt()[0]
                count = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        #adjuest for zero based arrays
        pos = pos - 1
        return pos, count

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
        link = event.mimeData()
        if link.hasText():
            plugin = event.mimeData().text()
            self.parent.EventManager.post_event(Event(EventType.LoadServiceItem, plugin))

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed
        """
        self.ThemeComboBox.clear()
        self.ThemeComboBox.addItem(u'')
        for theme in theme_list:
            self.ThemeComboBox.addItem(theme)
        id = self.ThemeComboBox.findText(unicode(self.service_theme), QtCore.Qt.MatchExactly)
        # Not Found
        if id == -1:
            id = 0
            self.service_theme = u''
        self.ThemeComboBox.setCurrentIndex(id)
        self.parent.RenderManager.set_service_theme(self.service_theme)
