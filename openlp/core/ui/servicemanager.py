# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

import os
import logging
import cPickle
import zipfile

log = logging.getLogger(__name__)

from PyQt4 import QtCore, QtGui

from openlp.core.lib import PluginConfig, OpenLPToolbar, ServiceItem, \
    contextMenuAction, contextMenuSeparator, contextMenu, Receiver, \
    contextMenu, str_to_bool, build_icon
from openlp.core.ui import ServiceItemNoteForm

class ServiceManagerList(QtGui.QTreeWidget):

    def __init__(self, parent=None, name=None):
        QtGui.QTreeWidget.__init__(self,parent)
        self.parent = parent
        self.setExpandsOnDoubleClick(False)

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

    def mouseMoveEvent(self, event):
        """
        Drag and drop event does not care what data is selected
        as the recipient will use events to request the data move
        just tell it what plugin to call
        """
        if event.buttons() != QtCore.Qt.LeftButton:
            event.ignore()
            return
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        drag.setMimeData(mimeData)
        mimeData.setText(u'ServiceManager')
        dropAction = drag.start(QtCore.Qt.CopyAction)

class ServiceManager(QtGui.QWidget):
    """
    Manages the services.  This involves taking text strings from plugins and
    adding them to the service.  This service can then be zipped up with all
    the resources used into one OSZ file for use on any OpenLP v2 installation.
    Also handles the UI tasks of moving things up and down etc.
    """
    def __init__(self, parent):
        """
        Sets up the service manager, toolbars, list view, et al.
        """
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.serviceItems = []
        self.serviceName = u''
        #is a new service and has not been saved
        self.isNew = True
        #Indicates if remoteTriggering is active.  If it is the next addServiceItem call
        #will replace the currently selected one.
        self.remoteEditTriggered = False
        self.serviceItemNoteForm = ServiceItemNoteForm()
        #start with the layout
        self.Layout = QtGui.QVBoxLayout(self)
        self.Layout.setSpacing(0)
        self.Layout.setMargin(0)
        # Create the top toolbar
        self.Toolbar = OpenLPToolbar(self)
        self.Toolbar.addToolbarButton(
            self.trUtf8('New Service'), u':/services/service_new.png',
            self.trUtf8('Create a new service'), self.onNewService)
        self.Toolbar.addToolbarButton(
            self.trUtf8('Open Service'), u':/services/service_open.png',
            self.trUtf8('Load an existing service'), self.onLoadService)
        self.Toolbar.addToolbarButton(
            self.trUtf8('Save Service'), u':/services/service_save.png',
            self.trUtf8('Save this service'), self.onSaveService)
        self.Toolbar.addSeparator()
        self.ThemeLabel = QtGui.QLabel(self.trUtf8('Theme:'),
            self)
        self.ThemeLabel.setMargin(3)
        self.Toolbar.addWidget(self.ThemeLabel)
        self.ThemeComboBox = QtGui.QComboBox(self.Toolbar)
        self.ThemeComboBox.setToolTip(self.trUtf8(
            u'Select a theme for the service'))
        self.ThemeComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToContents)
        self.ThemeWidget = QtGui.QWidgetAction(self.Toolbar)
        self.ThemeWidget.setDefaultWidget(self.ThemeComboBox)
        self.Toolbar.addAction(self.ThemeWidget)
        self.Layout.addWidget(self.Toolbar)
        # Create the service manager list
        self.ServiceManagerList = ServiceManagerList(self)
        self.ServiceManagerList.setEditTriggers(
            QtGui.QAbstractItemView.CurrentChanged |
            QtGui.QAbstractItemView.DoubleClicked |
            QtGui.QAbstractItemView.EditKeyPressed)
        self.ServiceManagerList.setDragDropMode(
            QtGui.QAbstractItemView.DragDrop)
        self.ServiceManagerList.setAlternatingRowColors(True)
        self.ServiceManagerList.setHeaderHidden(True)
        self.ServiceManagerList.setExpandsOnDoubleClick(False)
        self.ServiceManagerList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ServiceManagerList.customContextMenuRequested.connect(self.contextMenu)
        self.ServiceManagerList.setObjectName(u'ServiceManagerList')
        # enable drop
        self.ServiceManagerList.__class__.dragEnterEvent = self.dragEnterEvent
        self.ServiceManagerList.__class__.dragMoveEvent = self.dragEnterEvent
        self.ServiceManagerList.__class__.dropEvent = self.dropEvent
        self.Layout.addWidget(self.ServiceManagerList)
        # Add the bottom toolbar
        self.OrderToolbar = OpenLPToolbar(self)
        self.OrderToolbar.addToolbarButton(
            self.trUtf8('Move to top'), u':/services/service_top.png',
            self.trUtf8('Move to top'), self.onServiceTop)
        self.OrderToolbar.addToolbarButton(
            self.trUtf8('Move up'), u':/services/service_up.png',
            self.trUtf8('Move up order'), self.onServiceUp)
        self.OrderToolbar.addToolbarButton(
            self.trUtf8('Move down'), u':/services/service_down.png',
            self.trUtf8('Move down order'), self.onServiceDown)
        self.OrderToolbar.addToolbarButton(
            self.trUtf8('Move to bottom'), u':/services/service_bottom.png',
            self.trUtf8('Move to end'), self.onServiceEnd)
        self.OrderToolbar.addSeparator()
        self.OrderToolbar.addToolbarButton(
            self.trUtf8('Delete From Service'), u':/services/service_delete.png',
            self.trUtf8('Delete From Service'), self.onDeleteFromService)
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
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'update_themes'), self.updateThemeList)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'remote_edit_clear'), self.onRemoteEditClear)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation types'), self.onPresentationTypes)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_next_item'), self.nextItem)
        # Last little bits of setting up
        self.config = PluginConfig(u'ServiceManager')
        self.servicePath = self.config.get_data_path()
        self.service_theme = unicode(
            self.config.get_config(u'service theme', u''))
        #build the context menu
        self.menu = QtGui.QMenu()
        self.editAction = self.menu.addAction(self.trUtf8('&Edit Item'))
        self.editAction.setIcon(build_icon(':/services/service_edit.png'))
        self.notesAction = self.menu.addAction(self.trUtf8('&Notes'))
        self.notesAction.setIcon(build_icon(':/services/service_notes.png'))
        self.sep1 = self.menu.addAction(u'')
        self.sep1.setSeparator(True)
        self.previewAction = self.menu.addAction(self.trUtf8('&Preview Verse'))
        self.previewAction.setIcon(build_icon(':/system/system_preview.png'))
        self.liveAction = self.menu.addAction(self.trUtf8('&Live Verse'))
        self.liveAction.setIcon(build_icon(':/system/system_live.png'))
        self.sep2 = self.menu.addAction(u'')
        self.sep2.setSeparator(True)
        self.themeMenu = QtGui.QMenu(self.trUtf8('&Change Item Theme'))
        self.menu.addMenu(self.themeMenu)

    def contextMenu(self, point):
        item = self.ServiceManagerList.itemAt(point)
        if item.parent() is None:
            pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        else:
            pos = item.parent().data(0, QtCore.Qt.UserRole).toInt()[0]
        serviceItem = self.serviceItems[pos - 1]
        self.editAction.setVisible(False)
        self.notesAction.setVisible(False)
        if serviceItem[u'service_item'].edit_enabled:
            self.editAction.setVisible(True)
        if item.parent() is None:
            self.notesAction.setVisible(True)
        self.themeMenu.menuAction().setVisible(False)
        if serviceItem[u'service_item'].is_text():
            self.themeMenu.menuAction().setVisible(True)
        action = self.menu.exec_(self.ServiceManagerList.mapToGlobal(point))
        if action == self.editAction:
            self.remoteEdit()
        if action == self.notesAction:
            self.onServiceItemNoteForm()
        if action == self.previewAction:
            self.makePreview()
        if action == self.liveAction:
            self.makeLive()

    def onPresentationTypes(self, presentation_types):
        self.presentation_types = presentation_types

    def onServiceItemNoteForm(self):
        item, count = self.findServiceItem()
        self.serviceItemNoteForm.textEdit.setPlainText(
            self.serviceItems[item][u'service_item'].notes)
        if self.serviceItemNoteForm.exec_():
            self.serviceItems[item][u'service_item'].notes = \
                self.serviceItemNoteForm.textEdit.toPlainText()

    def nextItem(self):
        """
        Called by the SlideController to select the
        next service item
        """
        if len(self.ServiceManagerList.selectedItems()) == 0:
            return
        selected = self.ServiceManagerList.selectedItems()[0]
        lookFor = 0
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.ServiceManagerList)
        while serviceIterator.value():
            if lookFor == 1 and serviceIterator.value().parent() is None:
                self.ServiceManagerList.setCurrentItem(serviceIterator.value())
                self.makeLive()
                return
            if serviceIterator.value() == selected:
                lookFor = 1
            serviceIterator += 1

    def onMoveSelectionUp(self):
        """
        Moves the selection up the window
        Called by the up arrow
        """
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.ServiceManagerList)
        tempItem = None
        setLastItem = False
        while serviceIterator:
            if serviceIterator.isSelected() and tempItem is None:
                setLastItem = True
                serviceIterator.setSelected(False)
            if serviceIterator.isSelected():
                #We are on the first record
                if tempItem:
                    tempItem.setSelected(True)
                    serviceIterator.setSelected(False)
            else:
                tempItem = serviceIterator
            lastItem = serviceIterator
            ++serviceIterator
        #Top Item was selected so set the last one
        if setLastItem:
            lastItem.setSelected(True)

    def onMoveSelectionDown(self):
        """
        Moves the selection down the window
        Called by the down arrow
        """
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.ServiceManagerList)
        firstItem = serviceIterator
        setSelected = False
        while serviceIterator:
            if setSelected:
                setSelected = False
                serviceIterator.setSelected(True)
            elif serviceIterator.isSelected():
                serviceIterator.setSelected(False)
                setSelected = True
            ++serviceIterator
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
        self.parent.serviceChanged(False, self.serviceName)

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
            self.repaintServiceList(item - 1, count)
        self.parent.serviceChanged(False, self.serviceName)

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
            self.repaintServiceList(item + 1, count)
        self.parent.serviceChanged(False, self.serviceName)

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
        self.parent.serviceChanged(False, self.serviceName)

    def onNewService(self):
        """
        Clear the list to create a new service
        """
        if self.parent.serviceNotSaved and \
            str_to_bool(PluginConfig(u'General').
                        get_config(u'save prompt', u'False')):
            ret = QtGui.QMessageBox.question(self,
                self.trUtf8('Save Changes to Service?'),
                self.trUtf8('Your service is unsaved, do you want to save those '
                            'changes before creating a new one ?'),
                QtGui.QMessageBox.StandardButtons(
                    QtGui.QMessageBox.Cancel |
                    QtGui.QMessageBox.Save),
                QtGui.QMessageBox.Save)
            if ret == QtGui.QMessageBox.Save:
                self.onSaveService()
        self.ServiceManagerList.clear()
        self.serviceItems = []
        self.serviceName = u''
        self.isNew = True
        self.parent.serviceChanged(True, self.serviceName)

    def onDeleteFromService(self):
        """
        Remove the current ServiceItem from the list
        """
        item, count = self.findServiceItem()
        if item is not -1:
            self.serviceItems.remove(self.serviceItems[item])
            self.repaintServiceList(0, 0)
        self.parent.serviceChanged(False, self.serviceName)

    def repaintServiceList(self, serviceItem, serviceItemCount):
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
            serviceitem = item[u'service_item']
            treewidgetitem = QtGui.QTreeWidgetItem(self.ServiceManagerList)
            treewidgetitem.setText(0,serviceitem.title)
            treewidgetitem.setIcon(0,serviceitem.iconic_representation)
            treewidgetitem.setData(0, QtCore.Qt.UserRole,
                QtCore.QVariant(item[u'order']))
            treewidgetitem.setExpanded(item[u'expanded'])
            for count, frame in enumerate(serviceitem.get_frames()):
                treewidgetitem1 = QtGui.QTreeWidgetItem(treewidgetitem)
                text = frame[u'title']
                treewidgetitem1.setText(0,text[:40])
                treewidgetitem1.setData(0, QtCore.Qt.UserRole,
                    QtCore.QVariant(count))
                if serviceItem == itemcount and serviceItemCount == count:
                   self.ServiceManagerList.setCurrentItem(treewidgetitem1)

    def onSaveService(self, quick=False):
        """
        Save the current service in a zip (OSZ) file
        This file contains
        * An osd which is a pickle of the service items
        * All image, presentation and video files needed to run the service.
        """
        log.debug(u'onSaveService')
        if not quick or self.isNew:
            filename = QtGui.QFileDialog.getSaveFileName(self,
            u'Save Service', self.config.get_last_dir())
        else:
            filename = self.config.get_last_dir()
        if filename:
            splittedFile = filename.split(u'.')
            if splittedFile[-1] != u'osz':
                filename = filename + u'.osz'
            filename = unicode(filename)
            self.isNew = False
            self.config.set_last_dir(filename)
            service = []
            servicefile = filename + u'.osd'
            zip = None
            file = None
            try:
                zip = zipfile.ZipFile(unicode(filename), 'w')
                for item in self.serviceItems:
                    service.append({u'serviceitem':item[u'service_item'].get_service_repr()})
                    if item[u'service_item'].uses_file():
                        for frame in item[u'service_item'].get_frames():
                            path_from = unicode(os.path.join(
                                item[u'service_item'].service_item_path,
                                frame[u'title']))
                            zip.write(path_from)
                file = open(servicefile, u'wb')
                cPickle.dump(service, file)
                file.close()
                zip.write(servicefile)
            except:
                log.exception(u'Failed to save service to disk')
            finally:
                if file:
                    file.close()
                if zip:
                    zip.close()
            try:
                os.remove(servicefile)
            except:
                pass #if not present do not worry
        name = filename.split(os.path.sep)
        self.serviceName = name[-1]
        self.parent.serviceChanged(True, self.serviceName)

    def onQuickSaveService(self):
        self.onSaveService(True)

    def onLoadService(self, lastService=False):
        """
        Load an existing service from disk and rebuild the serviceitems.  All
        files retrieved from the zip file are placed in a temporary directory
        and will only be used for this service.
        """
        if lastService:
            filename = self.config.get_last_dir()
        else:
            filename = QtGui.QFileDialog.getOpenFileName(
                self, self.trUtf8('Open Service'),
                self.config.get_last_dir(), u'Services (*.osz)')
        filename = unicode(filename)
        name = filename.split(os.path.sep)
        if filename:
            self.config.set_last_dir(filename)
            zip = None
            f = None
            try:
                zip = zipfile.ZipFile(unicode(filename))
                for file in zip.namelist():
                    osfile = unicode(QtCore.QDir.toNativeSeparators(file))
                    names = osfile.split(os.path.sep)
                    file_to = os.path.join(self.servicePath,
                        names[len(names) - 1])
                    f = open(file_to, u'wb')
                    f.write(zip.read(file))
                    f.flush()
                    f.close()
                    if file_to.endswith(u'osd'):
                        p_file = file_to
                f = open(p_file, u'r')
                items = cPickle.load(f)
                f.close()
                self.onNewService()
                for item in items:
                    serviceitem = ServiceItem()
                    serviceitem.RenderManager = self.parent.RenderManager
                    serviceitem.set_from_service(item, self.servicePath)
                    if self.validateItem(serviceitem):
                        self.addServiceItem(serviceitem)
                try:
                    if os.path.isfile(p_file):
                        os.remove(p_file)
                except:
                    log.exception(u'Failed to remove osd file')
            except:
                log.exception(u'Problem loading a service file')
            finally:
                if f:
                    f.close()
                if zip:
                    zip.close()
        self.isNew = False
        self.serviceName = name[len(name) - 1]
        self.parent.serviceChanged(True, self.serviceName)

    def validateItem(self, serviceItem):
#        print "---"
#        print serviceItem.name
#        print serviceItem.title
#        print serviceItem.service_item_path
#        print serviceItem.service_item_type
        return True

    def cleanUp(self):
        """
        Empties the servicePath of temporary files
        """
        for file in os.listdir(self.servicePath):
            file_path = os.path.join(self.servicePath, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except:
                log.exception(u'Failed to clean up servicePath')

    def onThemeComboBoxSelected(self, currentIndex):
        """
        Set the theme for the current service
        """
        self.service_theme = unicode(self.ThemeComboBox.currentText())
        self.parent.RenderManager.set_service_theme(self.service_theme)
        self.config.set_config(u'service theme', self.service_theme)
        self.regenerateServiceItems()

    def regenerateServiceItems(self):
        #force reset of renderer as theme data has changed
        self.parent.RenderManager.themedata = None
        if len(self.serviceItems) > 0:
            tempServiceItems = self.serviceItems
            self.onNewService()
            for item in tempServiceItems:
                self.addServiceItem(item[u'service_item'], True)

    def addServiceItem(self, item, rebuild=False):
        """
        Add a Service item to the list

        ``item``
            Service Item to be added

        """
        sitem, count = self.findServiceItem()
        item.render()
        if self.remoteEditTriggered:
            item.merge(self.serviceItems[sitem][u'service_item'])
            self.serviceItems[sitem][u'service_item'] = item
            self.remoteEditTriggered = False
            self.repaintServiceList(sitem + 1, 0)
            self.parent.LiveController.replaceServiceManagerItem(item)
        else:
            if sitem == -1:
                self.serviceItems.append({u'service_item': item,
                    u'order': len(self.serviceItems) + 1,
                    u'expanded':True})
                self.repaintServiceList(len(self.serviceItems) + 1, 0)
            else:
                self.serviceItems.insert(sitem + 1, {u'service_item': item,
                    u'order': len(self.serviceItems)+1,
                    u'expanded':True})
                self.repaintServiceList(sitem + 1, 0)
            #if rebuilding list make sure live is fixed.
            if rebuild:
                self.parent.LiveController.replaceServiceManagerItem(item)
        self.parent.serviceChanged(False, self.serviceName)

    def makePreview(self):
        """
        Send the current item to the Preview slide controller
        """
        item, count = self.findServiceItem()
        self.parent.PreviewController.addServiceManagerItem(
            self.serviceItems[item][u'service_item'], count)


    def makeLive(self):
        """
        Send the current item to the Live slide controller
        """
        item, count = self.findServiceItem()
        self.parent.LiveController.addServiceManagerItem(
            self.serviceItems[item][u'service_item'], count)
        if str_to_bool(PluginConfig(u'General').
                        get_config(u'auto preview', u'False')):
            item += 1
            if len(self.serviceItems) > 0 and item < len(self.serviceItems) and \
                self.serviceItems[item][u'service_item'].autoPreviewAllowed:
                    self.parent.PreviewController.addServiceManagerItem(
                        self.serviceItems[item][u'service_item'], 0)

    def remoteEdit(self):
        """
        Posts a remote edit message to a plugin to allow item to be edited.
        """
        item, count = self.findServiceItem()
        if self.serviceItems[item][u'service_item'].edit_enabled:
            self.remoteEditTriggered = True
            Receiver.send_message(u'%s_edit' %
                self.serviceItems[item][u'service_item'].name, u'L:%s' %
                self.serviceItems[item][u'service_item'].editId )

    def onRemoteEditClear(self):
        self.remoteEditTriggered = False

    def findServiceItem(self):
        """
        Finds a ServiceItem in the list
        """
        items = self.ServiceManagerList.selectedItems()
        pos = 0
        count = 0
        for item in items:
            parentitem = item.parent()
            if parentitem is None:
                pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
            else:
                pos = parentitem.data(0, QtCore.Qt.UserRole).toInt()[0]
                count = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        #adjust for zero based arrays
        pos = pos - 1
        return pos, count

    def dragEnterEvent(self, event):
        """
        Accept Drag events

        ``event``
            Handle of the event pint passed

        """
        event.accept()

    def dropEvent(self, event):
        """
        Receive drop event and trigger an internal event to get the
        plugins to build and push the correct service item
        The drag event payload carries the plugin name

        ``event``
            Handle of the event pint passed
        """
        link = event.mimeData()
        if link.hasText():
            plugin = event.mimeData().text()
            if plugin == u'ServiceManager':
                startpos,  startCount = self.findServiceItem()
                item = self.ServiceManagerList.itemAt(event.pos())
                if item == None:
                    endpos = len(self.serviceItems)
                else:
                    parentitem = item.parent()
                    if parentitem is None:
                        endpos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
                    else:
                        endpos = parentitem.data(0, QtCore.Qt.UserRole).toInt()[0]
                    endpos -= 1
                if endpos < startpos:
                    newpos = endpos
                else:
                    newpos = endpos + 1
                serviceItem = self.serviceItems[startpos]
                self.serviceItems.remove(serviceItem)
                self.serviceItems.insert(newpos, serviceItem)
                self.repaintServiceList(endpos, startCount)
            else:
                Receiver.send_message(u'%s_add_service_item' % plugin)

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed

        ``theme_list``
            A list of current themes to be displayed
        """
        self.ThemeComboBox.clear()
        self.themeMenu.clear()
        self.ThemeComboBox.addItem(u'')
        for theme in theme_list:
            self.ThemeComboBox.addItem(theme)
            action = contextMenuAction(
                self.ServiceManagerList,
                None,
                theme , self.onThemeChangeAction)
            self.themeMenu.addAction(action)
        id = self.ThemeComboBox.findText(self.service_theme,
            QtCore.Qt.MatchExactly)
        # Not Found
        if id == -1:
            id = 0
            self.service_theme = u''
        self.ThemeComboBox.setCurrentIndex(id)
        self.parent.RenderManager.set_service_theme(self.service_theme)
        self.regenerateServiceItems()

    def onThemeChangeAction(self):
        theme = unicode(self.sender().text())
        item, count = self.findServiceItem()
        self.serviceItems[item][u'service_item'].theme = theme
        self.regenerateServiceItems()
