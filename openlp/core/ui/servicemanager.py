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
import zipfile
import shutil

from PyQt4 import QtCore, QtGui
from openlp.core.lib import PluginConfig, OpenLPToolbar, ServiceItem, Event, \
    RenderManager, EventType, EventManager, translate, buildIcon, \
    contextMenuAction, contextMenuSeparator
from openlp.core.utils import ConfigHelper

class ServiceManagerList(QtGui.QTreeWidget):

    def __init__(self,parent=None,name=None):
        QtGui.QListView.__init__(self,parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            #here accept the event and do something
            if event.key() == QtCore.Qt.Key_Enter:
                self.parent.makeLive()
                event.accept()
            elif event.key() == QtCore.Qt.Key_Home:
                self.parent.onServiceTop()
                event.accept()
            elif event.key() == QtCore.Qt.Key_End:
                self.parent.onServiceEnd()
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageUp:
                self.parent.onServiceUp()
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageDown:
                self.parent.onServiceDown()
                event.accept()
            elif event.key() == QtCore.Qt.Key_Up:
                self.parent.onMoveSelectionUp()
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                self.parent.onMoveSelectionDown()
                event.accept()
            event.ignore()
        else:
            event.ignore()

class Iter(QtGui.QTreeWidgetItemIterator):
  def __init__(self, *args):
        QtGui.QTreeWidgetItemIterator.__init__(self, *args)
  def next(self):
        self.__iadd__(1)
        value = self.value()
        if value:
            return self.value()
        else:
            return None

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
        self.serviceName = u''
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
        self.ServiceManagerList = ServiceManagerList(self)
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
        QtCore.QObject.connect(self.ServiceManagerList,
           QtCore.SIGNAL(u'itemCollapsed(QTreeWidgetItem*)'), self.collapsed)
        QtCore.QObject.connect(self.ServiceManagerList,
           QtCore.SIGNAL(u'itemExpanded(QTreeWidgetItem*)'), self.expanded)
        # Last little bits of setting up
        self.config = PluginConfig(u'ServiceManager')
        self.servicePath = self.config.get_data_path()
        self.service_theme = self.config.get_config(u'theme service theme', u'')

    def onMoveSelectionUp(self):
        """
        Moves the selection up the window
        Called by the up arrow
        """
        it = Iter(self.ServiceManagerList)
        item = it.value()
        tempItem = None
        setLastItem = False
        while item is not None:
            if item.isSelected() and tempItem is None:
                setLastItem = True
                item.setSelected(False)
            if item.isSelected():
                #We are on the first record
                if tempItem is not None:
                    tempItem.setSelected(True)
                    item.setSelected(False)
            else:
                tempItem = item
            lastItem = item
            item = it.next()
        #Top Item was selected so set the last one
        if setLastItem:
            lastItem.setSelected(True)

    def onMoveSelectionDown(self):
        """
        Moves the selection down the window
        Called by the down arrow
        """
        it = Iter(self.ServiceManagerList)
        item = it.value()
        firstItem = item
        setSelected = False
        while item is not None:
            if setSelected:
                setSelected = False
                item.setSelected(True)
            elif item.isSelected():
                item.setSelected(False)
                setSelected = True
            item = it.next()
        if setSelected:
            firstItem.setSelected(True)

    def collapsed(self, item):
        """
        Record if an item is collapsed
        Used when repainting the list to get the correct state
        """
        pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        self.serviceItems[pos -1 ][u'expanded'] = False

    def expanded(self, item):
        """
        Record if an item is collapsed
        Used when repainting the list to get the correct state
        """
        pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        self.serviceItems[pos -1 ][u'expanded'] = True

    def onServiceTop(self):
        """
        Move the current ServiceItem to the top of the list
        """
        item, count = self.findServiceItem()
        if item < len(self.serviceItems) and item is not -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(0, temp)
            self.repaintServiceList(0, count)
        self.parent.OosChanged(False, self.serviceName)

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
            self.repaintServiceList(item - 1 ,  count)
        self.parent.OosChanged(False, self.serviceName)

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
            self.repaintServiceList(item + 1 ,  count)
        self.parent.OosChanged(False, self.serviceName)

    def onServiceEnd(self):
        """
        Move the current ServiceItem to the bottom of the list
        """
        item, count = self.findServiceItem()
        if item < len(self.serviceItems) and item is not -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(len(self.serviceItems), temp)
            self.repaintServiceList(len(self.serviceItems) - 1, count)
        self.parent.OosChanged(False, self.serviceName)

    def onNewService(self):
        """
        Clear the list to create a new service
        """
        self.ServiceManagerList.clear()
        self.serviceItems = []
        self.serviceName = u''
        self.parent.OosChanged(True, self.serviceName)

    def onDeleteFromService(self):
        """
        Remove the current ServiceItem from the list
        """
        item, count = self.findServiceItem()
        if item is not -1:
            self.serviceItems.remove(self.serviceItems[item])
            self.repaintServiceList(0, 0)
        self.parent.OosChanged(False, self.serviceName)

    def repaintServiceList(self, serviceItem,  serviceItemCount):
        """
        Clear the existing service list and prepaint all the items
        Used when moving items as the move takes place in supporting array,
        and when regenerating all the items due to theme changes
        """
        #Correct order of items in array
        count = 1
        for item in self.serviceItems:
            item[u'order'] = count
            count += 1
        #Repaint the screen
        self.ServiceManagerList.clear()
        for itemcount, item in enumerate(self.serviceItems):
            serviceitem = item[u'data']
            treewidgetitem = QtGui.QTreeWidgetItem(self.ServiceManagerList)
            treewidgetitem.setText(0,serviceitem.title)
            treewidgetitem.setIcon(0,serviceitem.iconic_representation)
            treewidgetitem.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(item[u'order']))
            treewidgetitem.setExpanded(item[u'expanded'])
            for count , frame in enumerate(serviceitem.frames):
                treewidgetitem1 = QtGui.QTreeWidgetItem(treewidgetitem)
                text = frame[u'title']
                treewidgetitem1.setText(0,text[:40])
                treewidgetitem1.setData(0, QtCore.Qt.UserRole,QtCore.QVariant(count))
                if serviceItem == itemcount and serviceItemCount == count:
                   self.ServiceManagerList.setCurrentItem(treewidgetitem1)

    def onSaveService(self):
        """
        Save the current service in a zip file
        This file contains
        * An ood which is a pickle of the service items
        * All image , presentation and video files needed to run the service.
        """
        filename = QtGui.QFileDialog.getSaveFileName(self, u'Save Order of Service',self.config.get_last_dir() )
        filename = unicode(filename)
        if filename != u'':
            self.config.set_last_dir(filename)
            service = []
            servicefile= filename + u'.ood'
            zip = zipfile.ZipFile(unicode(filename) + u'.oos', 'w')
            for item in self.serviceItems:
                service.append({u'serviceitem':item[u'data'].get_oos_repr()})
                if item[u'data'].service_item_type == u'image':
                    for frame in item[u'data'].frames:
                        path_from = unicode(item[u'data'].service_item_path + u'/' + frame[u'title'])
                        zip.write(path_from)
            file = open(servicefile, u'wb')
            cPickle.dump(service, file)
            file.close()
            zip.write(servicefile)
            zip.close()
            try:
                os.remove(servicefile)
            except:
                pass #if not present do not worry
        self.parent.OosChanged(True, self.serviceName)

    def onLoadService(self):
        """
        Load an existing service from disk and rebuilds the serviceitems
        All files retrieved from the zip file are placed in a temporary directory and
        will only be used for this service.
        """
        filename = QtGui.QFileDialog.getOpenFileName(self, u'Open Order of Service',self.config.get_last_dir(),
            u'Services (*.oos)')
        filename = unicode(filename)
        name = filename.split(os.path.sep)
        if filename != u'':
            self.config.set_last_dir(filename)
            zip = zipfile.ZipFile(unicode(filename))
            filexml = None
            themename = None
            for file in zip.namelist():
                names = file.split(os.path.sep)
                file_to = os.path.join(self.servicePath, names[len(names) - 1])
                file_data = zip.read(file)
                f = open(file_to, u'w')
                f.write(file_data)
                f.close()
                if file_to.endswith(u'ood'):
                    p_file = file_to
            f = open(p_file, u'r')
            items = cPickle.load(f)
            f.close()
            self.onNewService()
            for item in items:
                serviceitem = ServiceItem()
                serviceitem.RenderManager = self.parent.RenderManager
                serviceitem.set_from_oos(item, self.servicePath )
                self.addServiceItem(serviceitem)
            try:
                os.remove(p_file)
            except:
                #if not present do not worry
                pass
        self.serviceName = name[len(name) - 1]
        self.parent.OosChanged(True, self.serviceName)

    def onThemeComboBoxSelected(self, currentIndex):
        """
        Set the theme for the current service
        """
        self.service_theme = unicode(self.ThemeComboBox.currentText())
        self.parent.RenderManager.set_service_theme(self.service_theme)
        self.config.set_config(u'theme service theme', self.service_theme)
        self.regenerateServiceItems()

    def regenerateServiceItems(self):
        if len(self.serviceItems) > 0:
            tempServiceItems = self.serviceItems
            self.onNewService()
            for item in tempServiceItems:
                self.addServiceItem(item[u'data'])

    def addServiceItem(self, item):
        """
        Add an item to the list
        """
        self.serviceItems.append({u'data': item, u'order': len(self.serviceItems)+1, u'expanded':True})
        treewidgetitem = QtGui.QTreeWidgetItem(self.ServiceManagerList)
        treewidgetitem.setText(0,item.title)
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
        self.parent.OosChanged(False, self.serviceName)

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
        self.regenerateServiceItems()
