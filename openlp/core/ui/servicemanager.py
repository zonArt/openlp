# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import OpenLPToolbar, ServiceItem, context_menu_action, \
    Receiver, build_icon, ItemCapabilities, SettingsManager, translate, \
    ThemeLevel
from openlp.core.ui import ServiceNoteForm, ServiceItemEditForm
from openlp.core.utils import AppLocation

class ServiceManagerList(QtGui.QTreeWidget):
    """
    Set up key bindings and mouse behaviour for the service list
    """
    def __init__(self, parent=None, name=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if isinstance(event, QtGui.QKeyEvent):
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
        drag.start(QtCore.Qt.CopyAction)

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
        self.suffixes = []
        self.droppos = 0
        #is a new service and has not been saved
        self.isNew = True
        self.serviceNoteForm = ServiceNoteForm(self.parent)
        self.serviceItemEditForm = ServiceItemEditForm(self.parent)
        #start with the layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        # Create the top toolbar
        self.toolbar = OpenLPToolbar(self)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'New Service'),
            u':/general/general_new.png',
            translate('OpenLP.ServiceManager', 'Create a new service'),
            self.onNewService)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Open Service'),
            u':/general/general_open.png',
            translate('OpenLP.ServiceManager', 'Load an existing service'),
            self.onLoadService)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Save Service'),
            u':/general/general_save.png',
            translate('OpenLP.ServiceManager', 'Save this service'),
            self.onQuickSaveService)
        self.toolbar.addSeparator()
        self.themeLabel = QtGui.QLabel(translate('OpenLP.ServiceManager',
            'Theme:'), self)
        self.themeLabel.setMargin(3)
        self.toolbar.addToolbarWidget(u'ThemeLabel', self.themeLabel)
        self.themeComboBox = QtGui.QComboBox(self.toolbar)
        self.themeComboBox.setToolTip(translate('OpenLP.ServiceManager',
            'Select a theme for the service'))
        self.themeComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToContents)
        self.toolbar.addToolbarWidget(u'ThemeWidget', self.themeComboBox)
        self.layout.addWidget(self.toolbar)
        # Create the service manager list
        self.serviceManagerList = ServiceManagerList(self)
        self.serviceManagerList.setEditTriggers(
            QtGui.QAbstractItemView.CurrentChanged |
            QtGui.QAbstractItemView.DoubleClicked |
            QtGui.QAbstractItemView.EditKeyPressed)
        self.serviceManagerList.setDragDropMode(
            QtGui.QAbstractItemView.DragDrop)
        self.serviceManagerList.setAlternatingRowColors(True)
        self.serviceManagerList.setHeaderHidden(True)
        self.serviceManagerList.setExpandsOnDoubleClick(False)
        self.serviceManagerList.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.serviceManagerList,
            QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
            self.contextMenu)
        self.serviceManagerList.setObjectName(u'serviceManagerList')
        # enable drop
        self.serviceManagerList.__class__.dragEnterEvent = self.dragEnterEvent
        self.serviceManagerList.__class__.dragMoveEvent = self.dragEnterEvent
        self.serviceManagerList.__class__.dropEvent = self.dropEvent
        self.layout.addWidget(self.serviceManagerList)
        # Add the bottom toolbar
        self.orderToolbar = OpenLPToolbar(self)
        self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move to &top'),
            u':/services/service_top.png',
            translate('OpenLP.ServiceManager',
            'Move item to the top of the service.'),
            self.onServiceTop)
        self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move &up'),
            u':/services/service_up.png',
            translate('OpenLP.ServiceManager',
            'Move item up one position in the service.'),
            self.onServiceUp)
        self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move &down'),
            u':/services/service_down.png',
            translate('OpenLP.ServiceManager',
            'Move item down one position in the service.'),
            self.onServiceDown)
        self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move to &bottom'),
            u':/services/service_bottom.png',
            translate('OpenLP.ServiceManager',
            'Move item to the end of the service.'),
            self.onServiceEnd)
        self.orderToolbar.addSeparator()
        self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', '&Delete From Service'),
            u':/general/general_delete.png',
            translate('OpenLP.ServiceManager',
            'Delete the selected item from the service.'),
            self.onDeleteFromService)
        self.layout.addWidget(self.orderToolbar)
        # Connect up our signals and slots
        QtCore.QObject.connect(self.themeComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onThemeComboBoxSelected)
        QtCore.QObject.connect(self.serviceManagerList,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.makeLive)
        QtCore.QObject.connect(self.serviceManagerList,
           QtCore.SIGNAL(u'itemCollapsed(QTreeWidgetItem*)'), self.collapsed)
        QtCore.QObject.connect(self.serviceManagerList,
           QtCore.SIGNAL(u'itemExpanded(QTreeWidgetItem*)'), self.expanded)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.updateThemeList)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_next_item'), self.nextItem)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_previous_item'), self.previousItem)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_set_item'), self.onSetItem)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_list_request'), self.listRequest)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.regenerateServiceItems)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_global'), self.themeChange)
        # Last little bits of setting up
        self.service_theme = unicode(QtCore.QSettings().value(
            self.parent.serviceSettingsSection + u'/service theme',
            QtCore.QVariant(u'')).toString())
        self.servicePath = AppLocation.get_section_data_path(u'servicemanager')
        #build the drag and drop context menu
        self.dndMenu = QtGui.QMenu()
        self.newAction = self.dndMenu.addAction(
            translate('OpenLP.ServiceManager', '&Add New Item'))
        self.newAction.setIcon(build_icon(u':/general/general_edit.png'))
        self.addToAction = self.dndMenu.addAction(
            translate('OpenLP.ServiceManager', '&Add to Selected Item'))
        self.addToAction.setIcon(build_icon(u':/general/general_edit.png'))
        #build the context menu
        self.menu = QtGui.QMenu()
        self.editAction = self.menu.addAction(
            translate('OpenLP.ServiceManager', '&Edit Item'))
        self.editAction.setIcon(build_icon(u':/general/general_edit.png'))
        self.maintainAction = self.menu.addAction(
            translate('OpenLP.ServiceManager', '&Reorder Item'))
        self.maintainAction.setIcon(build_icon(u':/general/general_edit.png'))
        self.notesAction = self.menu.addAction(
            translate('OpenLP.ServiceManager', '&Notes'))
        self.notesAction.setIcon(build_icon(u':/services/service_notes.png'))
        self.deleteAction = self.menu.addAction(
            translate('OpenLP.ServiceManager', '&Delete From Service'))
        self.deleteAction.setIcon(build_icon(u':/general/general_delete.png'))
        self.sep1 = self.menu.addAction(u'')
        self.sep1.setSeparator(True)
        self.previewAction = self.menu.addAction(
            translate('OpenLP.ServiceManager', '&Preview Verse'))
        self.previewAction.setIcon(build_icon(u':/general/general_preview.png'))
        self.liveAction = self.menu.addAction(
            translate('OpenLP.ServiceManager', '&Live Verse'))
        self.liveAction.setIcon(build_icon(u':/general/general_live.png'))
        self.sep2 = self.menu.addAction(u'')
        self.sep2.setSeparator(True)
        self.themeMenu = QtGui.QMenu(
            translate('OpenLP.ServiceManager', '&Change Item Theme'))
        self.menu.addMenu(self.themeMenu)

    def supportedSuffixes(self, suffix):
        self.suffixes.append(suffix)

    def contextMenu(self, point):
        item = self.serviceManagerList.itemAt(point)
        if item is None:
            return
        if item.parent() is None:
            pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        else:
            pos = item.parent().data(0, QtCore.Qt.UserRole).toInt()[0]
        serviceItem = self.serviceItems[pos - 1]
        self.editAction.setVisible(False)
        self.maintainAction.setVisible(False)
        self.notesAction.setVisible(False)
        if serviceItem[u'service_item'].is_capable(ItemCapabilities.AllowsEdit):
            self.editAction.setVisible(True)
        if serviceItem[u'service_item']\
            .is_capable(ItemCapabilities.AllowsMaintain):
            self.maintainAction.setVisible(True)
        if item.parent() is None:
            self.notesAction.setVisible(True)
        self.themeMenu.menuAction().setVisible(False)
        if serviceItem[u'service_item'].is_text():
            self.themeMenu.menuAction().setVisible(True)
        action = self.menu.exec_(self.serviceManagerList.mapToGlobal(point))
        if action == self.editAction:
            self.remoteEdit()
        if action == self.maintainAction:
            self.onServiceItemEditForm()
        if action == self.deleteAction:
            self.onDeleteFromService()
        if action == self.notesAction:
            self.onServiceItemNoteForm()
        if action == self.previewAction:
            self.makePreview()
        if action == self.liveAction:
            self.makeLive()

    def onServiceItemNoteForm(self):
        item = self.findServiceItem()[0]
        self.serviceNoteForm.textEdit.setPlainText(
            self.serviceItems[item][u'service_item'].notes)
        if self.serviceNoteForm.exec_():
            self.serviceItems[item][u'service_item'].notes = \
                self.serviceNoteForm.textEdit.toPlainText()
            self.repaintServiceList(item, 0)

    def onServiceItemEditForm(self):
        item = self.findServiceItem()[0]
        self.serviceItemEditForm.setServiceItem(
            self.serviceItems[item][u'service_item'])
        if self.serviceItemEditForm.exec_():
            self.serviceItems[item][u'service_item'] = \
                self.serviceItemEditForm.getServiceItem()
            self.repaintServiceList(item, 0)

    def nextItem(self):
        """
        Called by the SlideController to select the
        next service item
        """
        if len(self.serviceManagerList.selectedItems()) == 0:
            return
        selected = self.serviceManagerList.selectedItems()[0]
        lookFor = 0
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.serviceManagerList)
        while serviceIterator.value():
            if lookFor == 1 and serviceIterator.value().parent() is None:
                self.serviceManagerList.setCurrentItem(serviceIterator.value())
                self.makeLive()
                return
            if serviceIterator.value() == selected:
                lookFor = 1
            serviceIterator += 1

    def previousItem(self):
        """
        Called by the SlideController to select the
        previous service item
        """
        if len(self.serviceManagerList.selectedItems()) == 0:
            return
        selected = self.serviceManagerList.selectedItems()[0]
        prevItem = None
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.serviceManagerList)
        while serviceIterator.value():
            if serviceIterator.value() == selected:
                if prevItem:
                    self.serviceManagerList.setCurrentItem(prevItem)
                    self.makeLive()
                return
            if serviceIterator.value().parent() is None:
                prevItem = serviceIterator.value()
            serviceIterator += 1

    def onSetItem(self, message):
        """
        Called by a signal to select a specific item
        """
        self.setItem(int(message[0]))

    def setItem(self, index):
        """
        Makes a specific item in the service live
        """
        if index >= 0 and index < self.serviceManagerList.topLevelItemCount:
            item = self.serviceManagerList.topLevelItem(index)
            self.serviceManagerList.setCurrentItem(item)
            self.makeLive()

    def onMoveSelectionUp(self):
        """
        Moves the selection up the window
        Called by the up arrow
        """
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.serviceManagerList)
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
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.serviceManagerList)
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
        Note move up means move to top of area ie 0.
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
        if self.parent.serviceNotSaved and QtCore.QSettings().value(
            self.parent.generalSettingsSection + u'/save prompt',
            QtCore.QVariant(False)).toBool():
            ret = QtGui.QMessageBox.question(self,
                translate('OpenLP.ServiceManager', 'Save Changes to Service?'),
                translate('OpenLP.ServiceManager',
                    'Your service is unsaved, do you want to save '
                    'those changes before creating a new one?'),
                QtGui.QMessageBox.StandardButtons(
                    QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Save),
                QtGui.QMessageBox.Save)
            if ret == QtGui.QMessageBox.Save:
                self.onSaveService()
        self.serviceManagerList.clear()
        self.serviceItems = []
        self.serviceName = u''
        self.isNew = True
        self.parent.serviceChanged(True, self.serviceName)

    def onDeleteFromService(self):
        """
        Remove the current ServiceItem from the list
        """
        item = self.findServiceItem()[0]
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
        self.serviceManagerList.clear()
        for itemcount, item in enumerate(self.serviceItems):
            serviceitem = item[u'service_item']
            treewidgetitem = QtGui.QTreeWidgetItem(self.serviceManagerList)
            if serviceitem.is_valid:
                if serviceitem.notes:
                    icon = QtGui.QImage(serviceitem.icon)
                    icon = icon.scaled(80, 80, QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation)
                    overlay = QtGui.QImage(':/services/service_item_notes.png')
                    overlay = overlay.scaled(80, 80, QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation)
                    painter = QtGui.QPainter(icon)
                    painter.drawImage(0, 0, overlay)
                    painter.end()
                    treewidgetitem.setIcon(0, build_icon(icon))
                else:
                    treewidgetitem.setIcon(0, serviceitem.iconic_representation)
            else:
                treewidgetitem.setIcon(0,
                    build_icon(u':/general/general_delete.png'))
            treewidgetitem.setText(0, serviceitem.title)
            treewidgetitem.setToolTip(0, serviceitem.notes)
            treewidgetitem.setData(0, QtCore.Qt.UserRole,
                QtCore.QVariant(item[u'order']))
            for count, frame in enumerate(serviceitem.get_frames()):
                treewidgetitem1 = QtGui.QTreeWidgetItem(treewidgetitem)
                text = frame[u'title']
                treewidgetitem1.setText(0, text[:40])
                treewidgetitem1.setData(0, QtCore.Qt.UserRole,
                    QtCore.QVariant(count))
                if serviceItem == itemcount and serviceItemCount == count:
                    #preserve expanding status as setCurrentItem sets it to True
                    temp = item[u'expanded']
                    self.serviceManagerList.setCurrentItem(treewidgetitem1)
                    item[u'expanded'] = temp
            treewidgetitem.setExpanded(item[u'expanded'])

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
            translate('OpenLP.ServiceManager', 'Save Service'),
            SettingsManager.get_last_dir(self.parent.serviceSettingsSection),
            translate('OpenLP.ServiceManager', 'OpenLP Service Files (*.osz)'))
        else:
            filename = os.path.join(SettingsManager.get_last_dir(
                self.parent.serviceSettingsSection), self.serviceName)
        if filename:
            filename = QtCore.QDir.toNativeSeparators(filename)
            splittedFile = filename.split(u'.')
            if splittedFile[-1] != u'osz':
                filename = filename + u'.osz'
            filename = unicode(filename)
            self.isNew = False
            SettingsManager.set_last_dir(self.parent.serviceSettingsSection,
                os.path.split(filename)[0])
            service = []
            servicefile = filename + u'.osd'
            zip = None
            file = None
            try:
                zip = zipfile.ZipFile(unicode(filename), 'w')
                for item in self.serviceItems:
                    service.append({u'serviceitem':item[u'service_item']
                        .get_service_repr()})
                    if item[u'service_item'].uses_file():
                        for frame in item[u'service_item'].get_frames():
                            path_from = unicode(os.path.join(
                                frame[u'path'],
                                frame[u'title']))
                            zip.write(path_from.encode(u'utf-8'))
                file = open(servicefile, u'wb')
                cPickle.dump(service, file)
                file.close()
                zip.write(servicefile.encode(u'utf-8'))
            except IOError:
                log.exception(u'Failed to save service to disk')
            finally:
                if file:
                    file.close()
                if zip:
                    zip.close()
            try:
                os.remove(servicefile)
            except (IOError, OSError):
                pass #if not present do not worry
            name = filename.split(os.path.sep)
            self.serviceName = name[-1]
            self.parent.addRecentFile(filename)
            self.parent.serviceChanged(True, self.serviceName)

    def onQuickSaveService(self):
        self.onSaveService(True)

    def onLoadService(self, lastService=False):
        if lastService:
            filename = self.parent.recentFiles[0]
        else:
            filename = QtGui.QFileDialog.getOpenFileName(
                self, translate('OpenLP.ServiceManager', 'Open Service'),
                SettingsManager.get_last_dir(
                self.parent.serviceSettingsSection), u'Services (*.osz)')
        filename = QtCore.QDir.toNativeSeparators(filename)
        self.loadService(filename)

    def loadService(self, filename=None):
        """
        Load an existing service from disk and rebuild the serviceitems.  All
        files retrieved from the zip file are placed in a temporary directory
        and will only be used for this service.
        """
        if self.parent.serviceNotSaved:
            ret = QtGui.QMessageBox.question(self,
                translate('OpenLP.ServiceManager', 'Save Changes to Service?'),
                translate('OpenLP.ServiceManager',
                    'Your current service is unsaved, do you want to '
                    'save the changes before opening a new one?'),
                QtGui.QMessageBox.StandardButtons(
                    QtGui.QMessageBox.Discard | QtGui.QMessageBox.Save),
                QtGui.QMessageBox.Save)
            if ret == QtGui.QMessageBox.Save:
                self.onSaveService()
        if filename is None:
            action = self.sender()
            if isinstance(action, QtGui.QAction):
                filename = action.data().toString()
            else:
                return
        filename = unicode(filename)
        name = filename.split(os.path.sep)
        if filename:
            SettingsManager.set_last_dir(self.parent.serviceSettingsSection,
                os.path.split(filename)[0])
            zip = None
            file_to = None
            try:
                zip = zipfile.ZipFile(unicode(filename))
                for file in zip.namelist():
                    try:
                        ucsfile = file.decode(u'utf-8')
                    except UnicodeDecodeError:
                        QtGui.QMessageBox.critical(
                            self, translate('OpenLP.ServiceManager', 'Error'),
                            translate('OpenLP.ServiceManager',
                                'File is not a valid service.\n'
                                'The content encoding is not UTF-8.'))
                        log.exception(u'Filename "%s" is not valid UTF-8' %
                            file.decode(u'utf-8', u'replace'))
                        continue
                    osfile = unicode(QtCore.QDir.toNativeSeparators(ucsfile))
                    names = osfile.split(os.path.sep)
                    file_path = os.path.join(self.servicePath,
                        names[len(names) - 1])
                    file_to = open(file_path, u'wb')
                    file_to.write(zip.read(file))
                    file_to.flush()
                    file_to.close()
                    if file_path.endswith(u'osd'):
                        p_file = file_path
                if 'p_file' in locals():
                    file_to = open(p_file, u'r')
                    items = cPickle.load(file_to)
                    file_to.close()
                    self.onNewService()
                    for item in items:
                        serviceitem = ServiceItem()
                        serviceitem.render_manager = self.parent.RenderManager
                        serviceitem.set_from_service(item, self.servicePath)
                        self.validateItem(serviceitem)
                        self.addServiceItem(serviceitem)
                    try:
                        if os.path.isfile(p_file):
                            os.remove(p_file)
                    except (IOError, OSError):
                        log.exception(u'Failed to remove osd file')
                else:
                    QtGui.QMessageBox.critical(
                        self, translate('OpenLP.ServiceManager', 'Error'),
                        translate('OpenLP.ServiceManager',
                            'File is not a valid service.'))
                    log.exception(u'File contains no service data')
            except (IOError, NameError):
                log.exception(u'Problem loading a service file')
            finally:
                if file_to:
                    file_to.close()
                if zip:
                    zip.close()
        self.isNew = False
        self.serviceName = name[len(name) - 1]
        self.parent.addRecentFile(filename)
        self.parent.serviceChanged(True, self.serviceName)

    def validateItem(self, serviceItem):
        """
        Validates the service item and if the suffix matches an accepted
        one it allows the item to be displayed
        """
        if serviceItem.is_command():
            type = serviceItem._raw_frames[0][u'title'].split(u'.')[1]
            if type not in self.suffixes:
                serviceItem.is_valid = False

    def cleanUp(self):
        """
        Empties the servicePath of temporary files
        """
        for file in os.listdir(self.servicePath):
            file_path = os.path.join(self.servicePath, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except OSError:
                log.exception(u'Failed to clean up servicePath')

    def onThemeComboBoxSelected(self, currentIndex):
        """
        Set the theme for the current service
        """
        self.service_theme = unicode(self.themeComboBox.currentText())
        self.parent.RenderManager.set_service_theme(self.service_theme)
        QtCore.QSettings().setValue(
            self.parent.serviceSettingsSection + u'/service theme',
            QtCore.QVariant(self.service_theme))
        self.regenerateServiceItems()

    def themeChange(self):
        """
        The theme may have changed in the settings dialog so make
        sure the theme combo box is in the correct state.
        """
        if self.parent.RenderManager.theme_level == ThemeLevel.Global:
            self.toolbar.actions[u'ThemeLabel'].setVisible(False)
            self.toolbar.actions[u'ThemeWidget'].setVisible(False)
        else:
            self.toolbar.actions[u'ThemeLabel'].setVisible(True)
            self.toolbar.actions[u'ThemeWidget'].setVisible(True)

    def regenerateServiceItems(self):
        """
        Rebuild the service list as things have changed and a
        repaint is the easiest way to do this.
        """
        #force reset of renderer as theme data has changed
        self.parent.RenderManager.themedata = None
        if self.serviceItems:
            tempServiceItems = self.serviceItems
            self.serviceManagerList.clear()
            self.serviceItems = []
            self.isNew = True
            for item in tempServiceItems:
                self.addServiceItem(
                    item[u'service_item'], False, item[u'expanded'])
            #Set to False as items may have changed rendering
            #does not impact the saved song so True may also be valid
            self.parent.serviceChanged(False, self.serviceName)

    def addServiceItem(self, item, rebuild=False, expand=True, replace=False):
        """
        Add a Service item to the list

        ``item``
            Service Item to be added
        """
        sitem = self.findServiceItem()[0]
        item.render()
        if replace:
            item.merge(self.serviceItems[sitem][u'service_item'])
            self.serviceItems[sitem][u'service_item'] = item
            self.repaintServiceList(sitem + 1, 0)
            self.parent.LiveController.replaceServiceManagerItem(item)
        else:
            #nothing selected for dnd
            if self.droppos == 0:
                if isinstance(item, list):
                    for inditem in item:
                        self.serviceItems.append({u'service_item': inditem,
                            u'order': len(self.serviceItems) + 1,
                            u'expanded':expand})
                else:
                    self.serviceItems.append({u'service_item': item,
                        u'order': len(self.serviceItems) + 1,
                        u'expanded':expand})
                self.repaintServiceList(len(self.serviceItems) + 1, 0)
            else:
                self.serviceItems.insert(self.droppos, {u'service_item': item,
                    u'order': self.droppos,
                    u'expanded':expand})
                self.repaintServiceList(self.droppos, 0)
            #if rebuilding list make sure live is fixed.
            if rebuild:
                self.parent.LiveController.replaceServiceManagerItem(item)
        self.droppos = 0
        self.parent.serviceChanged(False, self.serviceName)

    def makePreview(self):
        """
        Send the current item to the Preview slide controller
        """
        item, count = self.findServiceItem()
        if self.serviceItems[item][u'service_item'].is_valid:
            self.parent.PreviewController.addServiceManagerItem(
                self.serviceItems[item][u'service_item'], count)
        else:
            QtGui.QMessageBox.critical(self,
                translate('OpenLP.ServiceManager', 'Missing Display Handler'),
                translate('OpenLP.ServiceManager', 'Your item cannot be '
                    'displayed as there is no handler to display it'))

    def getServiceItem(self):
        """
        Send the current item to the Preview slide controller
        """
        item = self.findServiceItem()[0]
        if item == -1:
            return False
        else:
            return self.serviceItems[item][u'service_item']

    def makeLive(self):
        """
        Send the current item to the Live slide controller
        """
        item, count = self.findServiceItem()
        if self.serviceItems[item][u'service_item'].is_valid:
            self.parent.LiveController.addServiceManagerItem(
                self.serviceItems[item][u'service_item'], count)
            if QtCore.QSettings().value(
                self.parent.generalSettingsSection + u'/auto preview',
                QtCore.QVariant(False)).toBool():
                item += 1
                if self.serviceItems and item < len(self.serviceItems) and \
                    self.serviceItems[item][u'service_item'].is_capable(
                    ItemCapabilities.AllowsPreview):
                    self.parent.PreviewController.addServiceManagerItem(
                        self.serviceItems[item][u'service_item'], 0)
                    self.parent.LiveController.PreviewListWidget.setFocus()
        else:
            QtGui.QMessageBox.critical(self,
                translate('OpenLP.ServiceManager', 'Missing Display Handler'),
                translate('OpenLP.ServiceManager', 'Your item cannot be '
                    'displayed as there is no handler to display it'))

    def remoteEdit(self):
        """
        Posts a remote edit message to a plugin to allow item to be edited.
        """
        item = self.findServiceItem()[0]
        if self.serviceItems[item][u'service_item']\
            .is_capable(ItemCapabilities.AllowsEdit):
            Receiver.send_message(u'%s_edit' %
                self.serviceItems[item][u'service_item'].name.lower(), u'L:%s' %
                self.serviceItems[item][u'service_item'].editId )

    def findServiceItem(self):
        """
        Finds a ServiceItem in the list
        """
        items = self.serviceManagerList.selectedItems()
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
            item = self.serviceManagerList.itemAt(event.pos())
            #ServiceManager started the drag and drop
            if plugin == u'ServiceManager':
                startpos, startCount = self.findServiceItem()
                if item is None:
                    endpos = len(self.serviceItems)
                else:
                    endpos = self._getParentItemData(item) - 1
                serviceItem = self.serviceItems[startpos]
                self.serviceItems.remove(serviceItem)
                self.serviceItems.insert(endpos, serviceItem)
                self.repaintServiceList(endpos, startCount)
            else:
                #we are not over anything so drop
                replace = False
                if item is None:
                    self.droppos = len(self.serviceItems)
                else:
                    #we are over somthing so lets investigate
                    pos = self._getParentItemData(item) - 1
                    serviceItem = self.serviceItems[pos]
                    if (plugin == serviceItem[u'service_item'].name and
                        serviceItem[u'service_item'].is_capable(
                        ItemCapabilities.AllowsAdditions)):
                        action = self.dndMenu.exec_(QtGui.QCursor.pos())
                        #New action required
                        if action == self.newAction:
                            self.droppos = self._getParentItemData(item)
                        #Append to existing action
                        if action == self.addToAction:
                            self.droppos = self._getParentItemData(item)
                            item.setSelected(True)
                            replace = True
                    else:
                        self.droppos = self._getParentItemData(item)
                Receiver.send_message(u'%s_add_service_item' % plugin, replace)

    def updateThemeList(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed

        ``theme_list``
            A list of current themes to be displayed
        """
        self.themeComboBox.clear()
        self.themeMenu.clear()
        self.themeComboBox.addItem(u'')
        for theme in theme_list:
            self.themeComboBox.addItem(theme)
            action = context_menu_action(self.serviceManagerList, None, theme,
                self.onThemeChangeAction)
            self.themeMenu.addAction(action)
        index = self.themeComboBox.findText(self.service_theme,
            QtCore.Qt.MatchExactly)
        # Not Found
        if index == -1:
            index = 0
            self.service_theme = u''
        self.themeComboBox.setCurrentIndex(index)
        self.parent.RenderManager.set_service_theme(self.service_theme)
        self.regenerateServiceItems()

    def onThemeChangeAction(self):
        theme = unicode(self.sender().text())
        item = self.findServiceItem()[0]
        self.serviceItems[item][u'service_item'].theme = theme
        self.regenerateServiceItems()

    def _getParentItemData(self, item):
        parentitem = item.parent()
        if parentitem is None:
            return item.data(0, QtCore.Qt.UserRole).toInt()[0]
        else:
            return parentitem.data(0, QtCore.Qt.UserRole).toInt()[0]

    def listRequest(self, message=None):
        data = []
        curindex = self.findServiceItem()[0]
        if curindex >= 0 and curindex < len(self.serviceItems):
            curitem = self.serviceItems[curindex]
        else:
            curitem = None
        for item in self.serviceItems:
            service_item = item[u'service_item']
            data_item = {}
            data_item[u'title'] = unicode(service_item.title)
            data_item[u'plugin'] = unicode(service_item.name)
            data_item[u'notes'] = unicode(service_item.notes)
            data_item[u'selected'] = (item == curitem)
            data.append(data_item)
        Receiver.send_message(u'servicemanager_list_response', data)
