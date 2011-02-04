# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
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

import cPickle
import datetime
import logging
import mutagen
import os
import zipfile

log = logging.getLogger(__name__)

from PyQt4 import QtCore, QtGui

from openlp.core.lib import OpenLPToolbar, ServiceItem, context_menu_action, \
    Receiver, build_icon, ItemCapabilities, SettingsManager, translate, \
    ThemeLevel
from openlp.core.lib.ui import critical_error_message_box
from openlp.core.ui import ServiceNoteForm, ServiceItemEditForm
from openlp.core.utils import AppLocation, delete_file, file_is_unicode, \
    split_filename

class ServiceManagerList(QtGui.QTreeWidget):
    """
    Set up key bindings and mouse behaviour for the service list
    """
    def __init__(self, mainwindow, parent=None, name=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.mainwindow = mainwindow

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
    def __init__(self, mainwindow, parent=None):
        """
        Sets up the service manager, toolbars, list view, et al.
        """
        QtGui.QWidget.__init__(self, parent)
        self.mainwindow = mainwindow
        self.serviceItems = []
        self.serviceName = u''
        self.suffixes = []
        self.dropPosition = 0
        self.expandTabs = False
        # is a new service and has not been saved
        self._modified = False
        self._fileName = u''
        self.serviceNoteForm = ServiceNoteForm(self.mainwindow)
        self.serviceItemEditForm = ServiceItemEditForm(self.mainwindow)
        # start with the layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        # Create the top toolbar
        self.toolbar = OpenLPToolbar(self)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'New Service'),
            u':/general/general_new.png',
            translate('OpenLP.ServiceManager', 'Create a new service'),
            self.onNewServiceClicked)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Open Service'),
            u':/general/general_open.png',
            translate('OpenLP.ServiceManager', 'Load an existing service'),
            self.onLoadServiceClicked)
        self.toolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Save Service'),
            u':/general/general_save.png',
            translate('OpenLP.ServiceManager', 'Save this service'),
            self.saveFile)
        self.toolbar.addSeparator()
        self.themeLabel = QtGui.QLabel(translate('OpenLP.ServiceManager',
            'Theme:'), self)
        self.themeLabel.setMargin(3)
        self.themeLabel.setObjectName(u'themeLabel')
        self.toolbar.addToolbarWidget(u'ThemeLabel', self.themeLabel)
        self.themeComboBox = QtGui.QComboBox(self.toolbar)
        self.themeComboBox.setToolTip(translate('OpenLP.ServiceManager',
            'Select a theme for the service'))
        self.themeComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.themeComboBox.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.themeComboBox.setObjectName(u'themeComboBox')
        self.toolbar.addToolbarWidget(u'ThemeWidget', self.themeComboBox)
        self.toolbar.setObjectName(u'toolbar')
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
        self.serviceManagerList.moveTop = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move to &top'),
            u':/services/service_top.png',
            translate('OpenLP.ServiceManager',
            'Move item to the top of the service.'),
            self.onServiceTop, shortcut=QtCore.Qt.Key_Home)
        self.serviceManagerList.moveUp = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move &up'),
            u':/services/service_up.png',
            translate('OpenLP.ServiceManager',
            'Move item up one position in the service.'),
            self.onServiceUp, shortcut=QtCore.Qt.Key_PageUp)
        self.serviceManagerList.moveDown = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move &down'),
            u':/services/service_down.png',
            translate('OpenLP.ServiceManager',
            'Move item down one position in the service.'),
            self.onServiceDown, shortcut=QtCore.Qt.Key_PageDown)
        self.serviceManagerList.moveBottom = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move to &bottom'),
            u':/services/service_bottom.png',
            translate('OpenLP.ServiceManager',
            'Move item to the end of the service.'),
            self.onServiceEnd, shortcut=QtCore.Qt.Key_End)
        self.serviceManagerList.down = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move &down'),
            None,
            translate('OpenLP.ServiceManager',
            'Moves the selection down the window.'),
            self.onMoveSelectionDown, shortcut=QtCore.Qt.Key_Down)
        self.serviceManagerList.down.setVisible(False)
        self.serviceManagerList.up = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Move up'),
            None,
            translate('OpenLP.ServiceManager',
            'Moves the selection up the window.'),
            self.onMoveSelectionUp, shortcut=QtCore.Qt.Key_Up)
        self.serviceManagerList.up.setVisible(False)
        self.orderToolbar.addSeparator()
        self.serviceManagerList.delete = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', '&Delete From Service'),
            u':/general/general_delete.png',
            translate('OpenLP.ServiceManager',
            'Delete the selected item from the service.'),
            self.onDeleteFromService)
        self.orderToolbar.addSeparator()
        self.serviceManagerList.expand = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', '&Expand all'),
            u':/services/service_expand_all.png',
            translate('OpenLP.ServiceManager',
            'Expand all the service items.'),
            self.onExpandAll)
        self.serviceManagerList.collapse = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', '&Collapse all'),
            u':/services/service_collapse_all.png',
            translate('OpenLP.ServiceManager',
            'Collapse all the service items.'),
            self.onCollapseAll)
        self.orderToolbar.addSeparator()
        self.serviceManagerList.makeLive = self.orderToolbar.addToolbarButton(
            translate('OpenLP.ServiceManager', 'Go Live'),
            u':/general/general_live.png',
            translate('OpenLP.ServiceManager',
            'Send the selected item to Live.'),
            self.makeLive, shortcut=QtCore.Qt.Key_Enter,
            alternate=QtCore.Qt.Key_Return)
        self.orderToolbar.setObjectName(u'orderToolbar')
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
            QtCore.SIGNAL(u'config_updated'), self.configUpdated)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_screen_changed'),
            self.regenerateServiceItems)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_global'), self.themeChange)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'service_item_update'), self.serviceItemUpdate)
        # Last little bits of setting up
        self.service_theme = unicode(QtCore.QSettings().value(
            self.mainwindow.serviceSettingsSection + u'/service theme',
            QtCore.QVariant(u'')).toString())
        self.servicePath = AppLocation.get_section_data_path(u'servicemanager')
        # build the drag and drop context menu
        self.dndMenu = QtGui.QMenu()
        self.newAction = self.dndMenu.addAction(
            translate('OpenLP.ServiceManager', '&Add New Item'))
        self.newAction.setIcon(build_icon(u':/general/general_edit.png'))
        self.addToAction = self.dndMenu.addAction(
            translate('OpenLP.ServiceManager', '&Add to Selected Item'))
        self.addToAction.setIcon(build_icon(u':/general/general_edit.png'))
        # build the context menu
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
        self.setServiceHotkeys()
        self.serviceManagerList.addActions(
            [self.serviceManagerList.moveDown,
            self.serviceManagerList.moveUp,
            self.serviceManagerList.makeLive,
            self.serviceManagerList.moveTop,
            self.serviceManagerList.moveBottom,
            self.serviceManagerList.up,
            self.serviceManagerList.down
            ])
        self.configUpdated()

    def setServiceHotkeys(self):
        actionList = self.mainwindow.actionList
        actionList.add_action(self.serviceManagerList.moveDown, u'Service')
        actionList.add_action(self.serviceManagerList.moveUp, u'Service')
        actionList.add_action(self.serviceManagerList.moveTop, u'Service')
        actionList.add_action(self.serviceManagerList.moveBottom, u'Service')
        actionList.add_action(self.serviceManagerList.makeLive, u'Service')
        actionList.add_action(self.serviceManagerList.up, u'Service')
        actionList.add_action(self.serviceManagerList.down, u'Service')

    def setModified(self, modified=True):
        """
        Setter for property "modified". Sets whether or not the current service
        has been modified.
        """
        self._modified = modified
        serviceFile = self.shortFileName() or u'Untitled Service'
        self.mainwindow.setServiceModified(modified, serviceFile)

    def isModified(self):
        """
        Getter for boolean property "modified".
        """
        return self._modified

    def setFileName(self, fileName):
        """
        Setter for service file.
        """
        self._fileName = unicode(fileName)
        self.mainwindow.setServiceModified(self.isModified(),
            self.shortFileName())
        QtCore.QSettings(). \
            setValue(u'service/last file',QtCore.QVariant(fileName))

    def fileName(self):
        """
        Return the current file name including path.
        """
        return self._fileName

    def shortFileName(self):
        """
        Return the current file name, excluding the path.
        """
        return split_filename(self._fileName)[1]

    def configUpdated(self):
        """
        Triggered when Config dialog is updated.
        """
        self.expandTabs = QtCore.QSettings().value(
            u'advanced/expand service item',
            QtCore.QVariant(u'False')).toBool()

    def supportedSuffixes(self, suffix):
        self.suffixes.append(suffix)

    def onNewServiceClicked(self):
        """
        Create a new service.
        """
        if self.isModified():
            result = self.saveModifiedService()
            if result == QtGui.QMessageBox.Cancel:
                return False
            elif result == QtGui.QMessageBox.Save:
                if not self.saveFile():
                    return False
        self.newFile()

    def onLoadServiceClicked(self):
        if self.isModified():
            result = self.saveModifiedService()
            if result == QtGui.QMessageBox.Cancel:
                return False
            elif result == QtGui.QMessageBox.Save:
                self.saveFile()
        fileName = unicode(QtGui.QFileDialog.getOpenFileName(self.mainwindow,
            translate('OpenLP.ServiceManager', 'Open File'),
            SettingsManager.get_last_dir(
            self.mainwindow.serviceSettingsSection),
            translate('OpenLP.ServiceManager', 'OpenLP Service Files (*.osz)')))
        if not fileName:
            return False
        SettingsManager.set_last_dir(self.mainwindow.serviceSettingsSection,
            split_filename(fileName)[0])
        self.loadFile(fileName)

    def saveModifiedService(self):
        return QtGui.QMessageBox.question(self.mainwindow,
            translate('OpenLP.ServiceManager', 'Modified Service'),
            translate('OpenLP.ServiceManager', 'The current service has '
            'been modified.  Would you like to save this service?'),
            QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Save)

    def onRecentServiceClicked(self):
        sender = self.sender()
        self.loadFile(sender.data().toString())

    def newFile(self):
        """
        Create a blank new service file.
        """
        self.serviceManagerList.clear()
        self.serviceItems = []
        self.setFileName(u'')
        self.setModified(False)
        QtCore.QSettings(). \
            setValue(u'service/last file',QtCore.QVariant(u''))

    def saveFile(self):
        """
        Save the current Service file.
        """
        if not self.fileName():
            return self.saveFileAs()
        else:
            fileName = self.fileName()
            log.debug(u'ServiceManager.saveFile - %s' % fileName)
            SettingsManager.set_last_dir(self.mainwindow.serviceSettingsSection,
                split_filename(fileName)[0])
            service = []
            serviceFileName = fileName.replace(u'.osz', u'.osd')
            zip = None
            file = None
            try:
                write_list = []
                zip = zipfile.ZipFile(unicode(fileName), 'w')
                for item in self.serviceItems:
                    service.append({u'serviceitem': \
                        item[u'service_item'].get_service_repr()})
                    if item[u'service_item'].uses_file():
                        for frame in item[u'service_item'].get_frames():
                            if item[u'service_item'].is_image():
                                path_from = frame[u'path']
                            else:
                                path_from = unicode(os.path.join(
                                    frame[u'path'],
                                    frame[u'title']))
                            # On write a file once
                            if not path_from in write_list:
                                write_list.append(path_from)
                                zip.write(path_from.encode(u'utf-8'))
                file = open(serviceFileName, u'wb')
                cPickle.dump(service, file)
                file.close()
                zip.write(serviceFileName.encode(u'utf-8'))
            except IOError:
                log.exception(u'Failed to save service to disk')
            finally:
                if file:
                    file.close()
                if zip:
                    zip.close()
            delete_file(serviceFileName)
            self.mainwindow.addRecentFile(fileName)
            self.setModified(False)
        return True

    def saveFileAs(self):
        """
        Get a file name and then call :function:`ServiceManager.saveFile` to
        save the file.
        """
        fileName = unicode(QtGui.QFileDialog.getSaveFileName(self.mainwindow,
            translate('OpenLP.ServiceManager', 'Save Service'),
            SettingsManager.get_last_dir(
            self.mainwindow.serviceSettingsSection),
            translate('OpenLP.ServiceManager', 'OpenLP Service Files (*.osz)')))
        if not fileName:
            return False
        if os.path.splitext(fileName)[1] == u'':
            fileName += u'.osz'
        else:
            ext = os.path.splitext(fileName)[1]
            fileName.replace(ext, u'.osz')
        self.setFileName(fileName)
        return self.saveFile()

    def loadFile(self, fileName):
        if not fileName:
            return False
        else:
            fileName = unicode(fileName)
        zip = None
        fileTo = None
        try:
            zip = zipfile.ZipFile(fileName)
            for file in zip.namelist():
                ucsfile = file_is_unicode(file)
                if not ucsfile:
                    critical_error_message_box(
                        message=translate('OpenLP.ServiceManager',
                        'File is not a valid service.\n'
                        'The content encoding is not UTF-8.'))
                    continue
                osfile = unicode(QtCore.QDir.toNativeSeparators(ucsfile))
                filePath = os.path.join(self.servicePath,
                    os.path.split(osfile)[1])
                fileTo = open(filePath, u'wb')
                fileTo.write(zip.read(file))
                fileTo.flush()
                fileTo.close()
                if filePath.endswith(u'osd'):
                    p_file = filePath
            if 'p_file' in locals():
                Receiver.send_message(u'cursor_busy')
                Receiver.send_message(u'openlp_process_events')
                fileTo = open(p_file, u'r')
                items = cPickle.load(fileTo)
                fileTo.close()
                self.newFile()
                for item in items:
                    serviceItem = ServiceItem()
                    serviceItem.render_manager = self.mainwindow.renderManager
                    serviceItem.set_from_service(item, self.servicePath)
                    self.validateItem(serviceItem)
                    self.addServiceItem(serviceItem)
                    if serviceItem.is_capable(ItemCapabilities.OnLoadUpdate):
                        Receiver.send_message(u'%s_service_load' %
                            serviceItem.name.lower(), serviceItem)
                delete_file(p_file)
                Receiver.send_message(u'cursor_normal')
            else:
                critical_error_message_box(
                    message=translate('OpenLP.ServiceManager',
                    'File is not a valid service.'))
                log.exception(u'File contains no service data')
        except (IOError, NameError):
            log.exception(u'Problem loading service file %s' % fileName)
        finally:
            if fileTo:
                fileTo.close()
            if zip:
                zip.close()
        self.setFileName(fileName)
        self.mainwindow.addRecentFile(fileName)
        self.setModified(False)
        QtCore.QSettings(). \
            setValue(u'service/last file', QtCore.QVariant(fileName))

    def loadLastFile(self):
        """
        Load the last service item from the service manager when the
        service was last closed. Can be blank if there was no service
        present.
        """
        fileName = QtCore.QSettings(). \
            value(u'service/last file',QtCore.QVariant(u'')).toString()
        if fileName:
            self.loadFile(fileName)

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
        if serviceItem[u'service_item'].is_capable(ItemCapabilities.AllowsEdit)\
            and serviceItem[u'service_item'].edit_id:
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
            self.repaintServiceList(item, -1)

    def onServiceItemEditForm(self):
        item = self.findServiceItem()[0]
        self.serviceItemEditForm.setServiceItem(
            self.serviceItems[item][u'service_item'])
        if self.serviceItemEditForm.exec_():
            self.addServiceItem(self.serviceItemEditForm.getServiceItem(),
                replace=True, expand=self.serviceItems[item][u'expanded'])

    def nextItem(self):
        """
        Called by the SlideController to select the next service item.
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
        Called by the SlideController to select the previous service item.
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
        Called by a signal to select a specific item.
        """
        self.setItem(int(message[0]))

    def setItem(self, index):
        """
        Makes a specific item in the service live.
        """
        if index >= 0 and index < self.serviceManagerList.topLevelItemCount:
            item = self.serviceManagerList.topLevelItem(index)
            self.serviceManagerList.setCurrentItem(item)
            self.makeLive()

    def onMoveSelectionUp(self):
        """
        Moves the selection up the window. Called by the up arrow.
        """
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.serviceManagerList)
        tempItem = None
        setLastItem = False
        while serviceIterator.value():
            if serviceIterator.value().isSelected() and tempItem is None:
                setLastItem = True
                serviceIterator.value().setSelected(False)
            if serviceIterator.value().isSelected():
                # We are on the first record
                if tempItem:
                    tempItem.setSelected(True)
                    serviceIterator.value().setSelected(False)
            else:
                tempItem = serviceIterator.value()
            lastItem = serviceIterator.value()
            serviceIterator += 1
        # Top Item was selected so set the last one
        if setLastItem:
            lastItem.setSelected(True)
        self.setModified(True)

    def onMoveSelectionDown(self):
        """
        Moves the selection down the window. Called by the down arrow.
        """
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.serviceManagerList)
        firstItem = None
        setSelected = False
        while serviceIterator.value():
            if not firstItem:
                firstItem = serviceIterator.value()
            if setSelected:
                setSelected = False
                serviceIterator.value().setSelected(True)
            elif serviceIterator.value() and \
                serviceIterator.value().isSelected():
                serviceIterator.value().setSelected(False)
                setSelected = True
            serviceIterator += 1
        if setSelected:
            firstItem.setSelected(True)
        self.setModified(True)

    def onCollapseAll(self):
        """
        Collapse all the service items.
        """
        for item in self.serviceItems:
            item[u'expanded'] = False
        self.regenerateServiceItems()

    def collapsed(self, item):
        """
        Record if an item is collapsed. Used when repainting the list to get the
        correct state.
        """
        pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        self.serviceItems[pos -1 ][u'expanded'] = False

    def onExpandAll(self):
        """
        Collapse all the service items.
        """
        for item in self.serviceItems:
            item[u'expanded'] = True
        self.regenerateServiceItems()

    def expanded(self, item):
        """
        Record if an item is collapsed. Used when repainting the list to get the
        correct state.
        """
        pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        self.serviceItems[pos -1 ][u'expanded'] = True

    def onServiceTop(self):
        """
        Move the current ServiceItem to the top of the list.
        """
        item, child = self.findServiceItem()
        if item < len(self.serviceItems) and item is not -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(0, temp)
            self.repaintServiceList(0, child)
        self.setModified(True)

    def onServiceUp(self):
        """
        Move the current ServiceItem one position up in the list.
        """
        item, child = self.findServiceItem()
        if item > 0:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(item - 1, temp)
            self.repaintServiceList(item - 1, child)
        self.setModified(True)

    def onServiceDown(self):
        """
        Move the current ServiceItem one position down in the list.
        """
        item, child = self.findServiceItem()
        if item < len(self.serviceItems) and item is not -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(item + 1, temp)
            self.repaintServiceList(item + 1, child)
        self.setModified(True)

    def onServiceEnd(self):
        """
        Move the current ServiceItem to the bottom of the list.
        """
        item, child = self.findServiceItem()
        if item < len(self.serviceItems) and item is not -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(len(self.serviceItems), temp)
            self.repaintServiceList(len(self.serviceItems) - 1, child)
        self.setModified(True)

    def onDeleteFromService(self):
        """
        Remove the current ServiceItem from the list.
        """
        item = self.findServiceItem()[0]
        if item != -1:
            self.serviceItems.remove(self.serviceItems[item])
            self.repaintServiceList(item - 1, -1)
        self.setModified(True)

    def repaintServiceList(self, serviceItem, serviceItemChild):
        """
        Clear the existing service list and prepaint all the items. This is
        used when moving items as the move takes place in a supporting list,
        and when regenerating all the items due to theme changes.

        ``serviceItem``
            The item which changed. (int)

        ``serviceItemChild``
            The child of the ``serviceItem``, which will be selected. (int)
        """
        # Correct order of items in array
        count = 1
        for item in self.serviceItems:
            item[u'order'] = count
            count += 1
        # Repaint the screen
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
            treewidgetitem.setText(0, serviceitem.get_display_title())
            treewidgetitem.setToolTip(0, serviceitem.notes)
            treewidgetitem.setData(0, QtCore.Qt.UserRole,
                QtCore.QVariant(item[u'order']))
            # Add the children to their parent treewidgetitem.
            for count, frame in enumerate(serviceitem.get_frames()):
                child = QtGui.QTreeWidgetItem(treewidgetitem)
                text = frame[u'title'].replace(u'\n', u' ')
                child.setText(0, text[:40])
                child.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(count))
                if serviceItem == itemcount:
                    if item[u'expanded'] and serviceItemChild == count:
                        self.serviceManagerList.setCurrentItem(child)
                    elif serviceItemChild == -1:
                        self.serviceManagerList.setCurrentItem(treewidgetitem)
            treewidgetitem.setExpanded(item[u'expanded'])

    def validateItem(self, serviceItem):
        """
        Validates the service item and if the suffix matches an accepted
        one it allows the item to be displayed.
        """
        if serviceItem.is_command():
            type = serviceItem._raw_frames[0][u'title'].split(u'.')[-1]
            if type not in self.suffixes:
                serviceItem.is_valid = False

    def cleanUp(self):
        """
        Empties the servicePath of temporary files.
        """
        for file in os.listdir(self.servicePath):
            file_path = os.path.join(self.servicePath, file)
            delete_file(file_path)

    def onThemeComboBoxSelected(self, currentIndex):
        """
        Set the theme for the current service.
        """
        log.debug(u'onThemeComboBoxSelected')
        self.service_theme = unicode(self.themeComboBox.currentText())
        self.mainwindow.renderManager.set_service_theme(self.service_theme)
        QtCore.QSettings().setValue(
            self.mainwindow.serviceSettingsSection + u'/service theme',
            QtCore.QVariant(self.service_theme))
        self.regenerateServiceItems()

    def themeChange(self):
        """
        The theme may have changed in the settings dialog so make
        sure the theme combo box is in the correct state.
        """
        log.debug(u'themeChange')
        if self.mainwindow.renderManager.theme_level == ThemeLevel.Global:
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
        Receiver.send_message(u'cursor_busy')
        log.debug(u'regenerateServiceItems')
        # force reset of renderer as theme data has changed
        self.mainwindow.renderManager.themedata = None
        if self.serviceItems:
            tempServiceItems = self.serviceItems
            self.serviceManagerList.clear()
            self.serviceItems = []
            self.isNew = True
            for item in tempServiceItems:
                self.addServiceItem(
                    item[u'service_item'], False, expand=item[u'expanded'])
            # Set to False as items may have changed rendering
            # does not impact the saved song so True may also be valid
            self.setModified(True)
        Receiver.send_message(u'cursor_normal')

    def serviceItemUpdate(self, message):
        """
        Triggered from plugins to update service items.
        """
        editId, uuid = message.split(u':')
        for item in self.serviceItems:
            if item[u'service_item']._uuid == uuid:
                item[u'service_item'].edit_id = editId

    def replaceServiceItem(self, newItem):
        """
        Using the service item passed replace the one with the same edit id
        if found.
        """
        newItem.render()
        for itemcount, item in enumerate(self.serviceItems):
            if item[u'service_item'].edit_id == newItem.edit_id and \
                item[u'service_item'].name == newItem.name:
                newItem.merge(item[u'service_item'])
                item[u'service_item'] = newItem
                self.repaintServiceList(itemcount + 1, 0)
                self.mainwindow.liveController.replaceServiceManagerItem(
                    newItem)
        self.setModified(True)

    def addServiceItem(self, item, rebuild=False, expand=None, replace=False):
        """
        Add a Service item to the list

        ``item``
            Service Item to be added

        ``expand``
            Override the default expand settings. (Tristate)
        """
        # if not passed set to config value
        if expand is None:
            expand = self.expandTabs
        item.render()
        if replace:
            sitem, child = self.findServiceItem()
            item.merge(self.serviceItems[sitem][u'service_item'])
            self.serviceItems[sitem][u'service_item'] = item
            self.repaintServiceList(sitem, child)
            self.mainwindow.liveController.replaceServiceManagerItem(item)
        else:
            # nothing selected for dnd
            if self.dropPosition == 0:
                if isinstance(item, list):
                    for inditem in item:
                        self.serviceItems.append({u'service_item': inditem,
                            u'order': len(self.serviceItems) + 1,
                            u'expanded': expand})
                else:
                    self.serviceItems.append({u'service_item': item,
                        u'order': len(self.serviceItems) + 1,
                        u'expanded': expand})
                self.repaintServiceList(len(self.serviceItems) - 1, -1)
            else:
                self.serviceItems.insert(self.dropPosition,
                    {u'service_item': item, u'order': self.dropPosition,
                    u'expanded': expand})
                self.repaintServiceList(self.dropPosition, -1)
            # if rebuilding list make sure live is fixed.
            if rebuild:
                self.mainwindow.liveController.replaceServiceManagerItem(item)
        self.dropPosition = 0
        self.setModified(True)

    def makePreview(self):
        """
        Send the current item to the Preview slide controller
        """
        item, child = self.findServiceItem()
        if self.serviceItems[item][u'service_item'].is_valid:
            self.mainwindow.previewController.addServiceManagerItem(
                self.serviceItems[item][u'service_item'], child)
        else:
            critical_error_message_box(
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
        item, child = self.findServiceItem()
        if self.serviceItems[item][u'service_item'].is_valid:
            self.mainwindow.liveController.addServiceManagerItem(
                self.serviceItems[item][u'service_item'], child)
            if QtCore.QSettings().value(
                self.mainwindow.generalSettingsSection + u'/auto preview',
                QtCore.QVariant(False)).toBool():
                item += 1
                if self.serviceItems and item < len(self.serviceItems) and \
                    self.serviceItems[item][u'service_item'].is_capable(
                    ItemCapabilities.AllowsPreview):
                    self.mainwindow.previewController.addServiceManagerItem(
                        self.serviceItems[item][u'service_item'], 0)
                    self.mainwindow.liveController.previewListWidget.setFocus()
        else:
            critical_error_message_box(
                translate('OpenLP.ServiceManager', 'Missing Display Handler'),
                translate('OpenLP.ServiceManager', 'Your item cannot be '
                'displayed as the plugin required to display it is missing '
                'or inactive'))

    def remoteEdit(self):
        """
        Posts a remote edit message to a plugin to allow item to be edited.
        """
        item = self.findServiceItem()[0]
        if self.serviceItems[item][u'service_item']\
            .is_capable(ItemCapabilities.AllowsEdit):
            Receiver.send_message(u'%s_edit' %
                self.serviceItems[item][u'service_item'].name.lower(), u'L:%s' %
                self.serviceItems[item][u'service_item'].edit_id )

    def findServiceItem(self):
        """
        Finds the selected ServiceItem in the list and returns the position of
        the serviceitem and its selected child item. For example, if the third
        child item (in the Slidecontroller known as slide) in the second service
        item is selected this will return::

            (1, 2)
        """
        items = self.serviceManagerList.selectedItems()
        serviceItem = 0
        serviceItemChild = -1
        for item in items:
            parentitem = item.parent()
            if parentitem is None:
                serviceItem = item.data(0, QtCore.Qt.UserRole).toInt()[0]
            else:
                serviceItem = parentitem.data(0, QtCore.Qt.UserRole).toInt()[0]
                serviceItemChild = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        # Adjust for zero based arrays.
        serviceItem -= 1
        return serviceItem, serviceItemChild

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
            plugin = unicode(event.mimeData().text())
            item = self.serviceManagerList.itemAt(event.pos())
            # ServiceManager started the drag and drop
            if plugin == u'ServiceManager':
                startpos, child = self.findServiceItem()
                # If no items selected
                if startpos == -1:
                    return
                if item is None:
                    endpos = len(self.serviceItems)
                else:
                    endpos = self._getParentItemData(item) - 1
                serviceItem = self.serviceItems[startpos]
                self.serviceItems.remove(serviceItem)
                self.serviceItems.insert(endpos, serviceItem)
                self.repaintServiceList(endpos, child)
            else:
                # we are not over anything so drop
                replace = False
                if item is None:
                    self.dropPosition = len(self.serviceItems)
                else:
                    # we are over somthing so lets investigate
                    pos = self._getParentItemData(item) - 1
                    serviceItem = self.serviceItems[pos]
                    if (plugin == serviceItem[u'service_item'].name and
                        serviceItem[u'service_item'].is_capable(
                        ItemCapabilities.AllowsAdditions)):
                        action = self.dndMenu.exec_(QtGui.QCursor.pos())
                        # New action required
                        if action == self.newAction:
                            self.dropPosition = self._getParentItemData(item)
                        # Append to existing action
                        if action == self.addToAction:
                            self.dropPosition = self._getParentItemData(item)
                            item.setSelected(True)
                            replace = True
                    else:
                        self.dropPosition = self._getParentItemData(item)
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
        self.mainwindow.renderManager.set_service_theme(self.service_theme)
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
        item = self.findServiceItem()[0]
        if item >= 0 and item < len(self.serviceItems):
            curitem = self.serviceItems[item]
        else:
            curitem = None
        for item in self.serviceItems:
            service_item = item[u'service_item']
            data_item = {}
            data_item[u'title'] = unicode(service_item.get_display_title())
            data_item[u'plugin'] = unicode(service_item.name)
            data_item[u'notes'] = unicode(service_item.notes)
            data_item[u'selected'] = (item == curitem)
            data.append(data_item)
        Receiver.send_message(u'servicemanager_list_response', data)

    def printServiceOrder(self):
        """
        Print a Service Order Sheet.
        """
        printDialog = QtGui.QPrintDialog()
        if not printDialog.exec_():
            return
        text = u'<h2>%s</h2>' % translate('OpenLP.ServiceManager',
            'Service Order Sheet')
        for item in self.serviceItems:
            item = item[u'service_item']
            # Add the title of the service item.
            text += u'<h4><img src="%s" /> %s</h4>' % (item.icon,
                item.get_display_title())
            # Add slide text of the service item.
            if QtCore.QSettings().value(u'advanced' +
                u'/print slide text', QtCore.QVariant(False)).toBool():
                if item.is_text():
                    # Add the text of the service item.
                    for slide in item.get_frames():
                        text += u'<p>' + slide[u'text'] + u'</p>'
                elif item.is_image():
                    # Add the image names of the service item.
                    text += u'<ol>'
                    for slide in range(len(item.get_frames())):
                        text += u'<li><p>%s</p></li>' % \
                            item.get_frame_title(slide)
                    text += u'</ol>'
                if item.foot_text:
                    # add footer
                    text += u'<p>%s</p>' % item.foot_text
            # Add service items' notes.
            if QtCore.QSettings().value(u'advanced' +
                u'/print notes', QtCore.QVariant(False)).toBool():
                if item.notes:
                    text += u'<p><b>%s</b> %s</p>' % (translate(
                        'OpenLP.ServiceManager', 'Notes:'), item.notes)
            # Add play length of media files.
            if item.is_media() and QtCore.QSettings().value(u'advanced' +
                u'/print file meta data', QtCore.QVariant(False)).toBool():
                path = os.path.join(item.get_frames()[0][u'path'],
                    item.get_frames()[0][u'title'])
                if not os.path.isfile(path):
                    continue
                file = mutagen.File(path)
                if file is not None:
                    length = int(file.info.length)
                    text += u'<p><b>%s</b> %s</p>' % (translate(
                        'OpenLP.ServiceManager', u'Playing time:'),
                        unicode(datetime.timedelta(seconds=length)))
        serviceDocument = QtGui.QTextDocument()
        serviceDocument.setHtml(text)
        serviceDocument.print_(printDialog.printer())
