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
        self.ServiceManagerList.setObjectName("ServiceManagerList")
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
        # Last little bits of setting up
        self.config = PluginConfig(u'Main')
        self.service_theme = self.config.get_config(u'theme service theme', u'')

    def onServiceTop(self):
        """
        Move the current ServiceItem to the top of the list
        """
        pass

    def onServiceUp(self):
        """
        Move the current ServiceItem up in the list
        """
        pass

    def onServiceDown(self):
        """
        Move the current ServiceItem down in the list
        """
        pass

    def onServiceEnd(self):
        """
        Move the current ServiceItem to the bottom of the list
        """
        pass

    def onNewService(self):
        """
        Clear the list to create a new service
        """
        self.service_data.clearItems()

    def onDeleteFromService(self):
        """
        Remove the current ServiceItem from the list
        """
        pass

    def onSaveService(self):
        """
        Save the current service
        """
        pass

    def onLoadService(self):
        """
        Load an existing service from disk
        """
        pass

    def onThemeComboBoxSelected(self, currentIndex):
        """
        Set the theme for the current service
        """
        self.service_theme = self.ThemeComboBox.currentText()
        self.parent.RenderManager.set_service_theme(self.service_theme)
        self.config.set_config(u'theme service theme', self.service_theme)

    def addServiceItem(self, item):
        """
        Add an item to the list
        """
        self.serviceItems.append({u'data': item, u'order': len(self.serviceItems)+1})
        treewidgetitem = QtGui.QTreeWidgetItem(self.ServiceManagerList)
        treewidgetitem.setText(0,item.title) # + u':' + item.shortname)
        treewidgetitem.setIcon(0,item.iconic_representation)
        treewidgetitem.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(len(self.serviceItems)))
        treewidgetitem.setExpanded(True)
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
            childCount = item.childCount()
            if childCount >= 1: # is the parent
                pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
            else:
                parentitem = item.parent()
                pos = parentitem.data(0, QtCore.Qt.UserRole).toInt()[0]
                count = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        pos = pos - 1 #adjust for zeor indexing
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
        self.ThemeComboBox.addItem(u'')
        for theme in theme_list:
            self.ThemeComboBox.addItem(theme)
        id = self.ThemeComboBox.findText(str(self.service_theme), QtCore.Qt.MatchExactly)
        # Not Found
        if id == -1:
            id = 0
            self.service_theme = u''
        self.ThemeComboBox.setCurrentIndex(id)
        self.parent.RenderManager.set_service_theme(self.service_theme)

