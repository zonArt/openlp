# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import cgi
import cPickle
import logging
import os
import shutil
import zipfile
from tempfile import mkstemp
from datetime import datetime, timedelta

log = logging.getLogger(__name__)

from PyQt4 import QtCore, QtGui

from openlp.core.lib import OpenLPToolbar, ServiceItem, Receiver, build_icon, \
    ItemCapabilities, SettingsManager, translate, str_to_bool, Settings
from openlp.core.lib.theme import ThemeLevel
from openlp.core.lib.ui import UiStrings, critical_error_message_box, \
    create_widget_action, find_and_set_in_combo_box
from openlp.core.ui import ServiceNoteForm, ServiceItemEditForm, StartTimeForm
from openlp.core.ui.printserviceform import PrintServiceForm
from openlp.core.utils import AppLocation, delete_file, split_filename
from openlp.core.utils.actions import ActionList, CategoryOrder

class ServiceManagerList(QtGui.QTreeWidget):
    """
    Set up key bindings and mouse behaviour for the service list
    """
    def __init__(self, serviceManager, parent=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.serviceManager = serviceManager

    def keyPressEvent(self, event):
        if isinstance(event, QtGui.QKeyEvent):
            # here accept the event and do something
            if event.key() == QtCore.Qt.Key_Up:
                self.serviceManager.onMoveSelectionUp()
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                self.serviceManager.onMoveSelectionDown()
                event.accept()
            elif event.key() == QtCore.Qt.Key_Delete:
                self.serviceManager.onDeleteFromService()
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
        if not self.itemAt(self.mapFromGlobal(QtGui.QCursor.pos())):
            event.ignore()
            return
        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        drag.setMimeData(mimeData)
        mimeData.setText(u'ServiceManager')
        drag.start(QtCore.Qt.CopyAction)


class ServiceManager(QtGui.QWidget):
    """
    Manages the services. This involves taking text strings from plugins and
    adding them to the service. This service can then be zipped up with all
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
        self.suffixes = []
        self.dropPosition = 0
        self.expandTabs = False
        self.serviceId = 0
        # is a new service and has not been saved
        self._modified = False
        self._fileName = u''
        self.serviceNoteForm = ServiceNoteForm(self.mainwindow)
        self.serviceItemEditForm = ServiceItemEditForm(self.mainwindow)
        self.startTimeForm = StartTimeForm(self.mainwindow)
        # start with the layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        # Create the top toolbar
        self.toolbar = OpenLPToolbar(self)
        self.toolbar.addToolbarAction(u'newService',
            text=UiStrings().NewService, icon=u':/general/general_new.png',
            tooltip=UiStrings().CreateService,
            triggers=self.onNewServiceClicked)
        self.toolbar.addToolbarAction(u'openService',
            text=UiStrings().OpenService, icon=u':/general/general_open.png',
            tooltip=translate('OpenLP.ServiceManager',
            'Load an existing service.'), triggers=self.onLoadServiceClicked)
        self.toolbar.addToolbarAction(u'saveService',
            text=UiStrings().SaveService, icon=u':/general/general_save.png',
            tooltip=translate('OpenLP.ServiceManager', 'Save this service.'),
            triggers=self.saveFile)
        self.toolbar.addSeparator()
        self.themeLabel = QtGui.QLabel(u'%s:' % UiStrings().Theme, self)
        self.themeLabel.setMargin(3)
        self.themeLabel.setObjectName(u'themeLabel')
        self.toolbar.addToolbarWidget(self.themeLabel)
        self.themeComboBox = QtGui.QComboBox(self.toolbar)
        self.themeComboBox.setToolTip(translate('OpenLP.ServiceManager',
            'Select a theme for the service.'))
        self.themeComboBox.setSizeAdjustPolicy(
            QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.themeComboBox.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.themeComboBox.setObjectName(u'themeComboBox')
        self.toolbar.addToolbarWidget(self.themeComboBox)
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
        action_list = ActionList.get_instance()
        action_list.add_category(
            unicode(UiStrings().Service), CategoryOrder.standardToolbar)
        self.serviceManagerList.moveTop = self.orderToolbar.addToolbarAction(
            u'moveTop', text=translate('OpenLP.ServiceManager', 'Move to &top'),
            icon=u':/services/service_top.png', tooltip=translate(
            'OpenLP.ServiceManager', 'Move item to the top of the service.'),
            shortcuts=[QtCore.Qt.Key_Home], category=UiStrings().Service,
            triggers=self.onServiceTop)
        self.serviceManagerList.moveUp = self.orderToolbar.addToolbarAction(
            u'moveUp', text=translate('OpenLP.ServiceManager', 'Move &up'),
            icon=u':/services/service_up.png',
            tooltip=translate('OpenLP.ServiceManager',
            'Move item up one position in the service.'),
            shortcuts=[QtCore.Qt.Key_PageUp], category=UiStrings().Service,
            triggers=self.onServiceUp)
        self.serviceManagerList.moveDown = self.orderToolbar.addToolbarAction(
            u'moveDown', text=translate('OpenLP.ServiceManager', 'Move &down'),
            icon=u':/services/service_down.png',
            tooltip=translate('OpenLP.ServiceManager',
            'Move item down one position in the service.'),
            shortcuts=[QtCore.Qt.Key_PageDown], category=UiStrings().Service,
            triggers=self.onServiceDown)
        self.serviceManagerList.moveBottom = self.orderToolbar.addToolbarAction(
            u'moveBottom',
            text=translate('OpenLP.ServiceManager', 'Move to &bottom'),
            icon=u':/services/service_bottom.png', tooltip=translate(
            'OpenLP.ServiceManager', 'Move item to the end of the service.'),
            shortcuts=[QtCore.Qt.Key_End], category=UiStrings().Service,
            triggers=self.onServiceEnd)
        self.serviceManagerList.down = self.orderToolbar.addToolbarAction(
            u'down', text=translate('OpenLP.ServiceManager', 'Move &down'),
            tooltip=translate('OpenLP.ServiceManager',
            'Moves the selection down the window.'), visible=False,
            shortcuts=[QtCore.Qt.Key_Down], triggers=self.onMoveSelectionDown)
        action_list.add_action(self.serviceManagerList.down)
        self.serviceManagerList.up = self.orderToolbar.addToolbarAction(
            u'up', text=translate('OpenLP.ServiceManager', 'Move up'),
            tooltip=translate('OpenLP.ServiceManager',
            'Moves the selection up the window.'), visible=False,
            shortcuts=[QtCore.Qt.Key_Up], triggers=self.onMoveSelectionUp)
        action_list.add_action(self.serviceManagerList.up)
        self.orderToolbar.addSeparator()
        self.serviceManagerList.delete = self.orderToolbar.addToolbarAction(
            u'delete',
            text=translate('OpenLP.ServiceManager', '&Delete From Service'),
            icon=u':/general/general_delete.png',
            tooltip=translate('OpenLP.ServiceManager',
            'Delete the selected item from the service.'),
            shortcuts=[QtCore.Qt.Key_Delete],
            triggers=self.onDeleteFromService)
        self.orderToolbar.addSeparator()
        self.serviceManagerList.expand = self.orderToolbar.addToolbarAction(
            u'expand', text=translate('OpenLP.ServiceManager', '&Expand all'),
            icon=u':/services/service_expand_all.png', tooltip=translate(
            'OpenLP.ServiceManager', 'Expand all the service items.'),
            shortcuts=[QtCore.Qt.Key_Plus], category=UiStrings().Service,
            triggers=self.onExpandAll)
        self.serviceManagerList.collapse = self.orderToolbar.addToolbarAction(
            u'collapse',
            text=translate('OpenLP.ServiceManager', '&Collapse all'),
            icon=u':/services/service_collapse_all.png', tooltip=translate(
            'OpenLP.ServiceManager', 'Collapse all the service items.'),
            shortcuts=[QtCore.Qt.Key_Minus], category=UiStrings().Service,
            triggers=self.onCollapseAll)
        self.orderToolbar.addSeparator()
        self.serviceManagerList.makeLive = self.orderToolbar.addToolbarAction(
            u'makeLive', text=translate('OpenLP.ServiceManager', 'Go Live'),
            icon=u':/general/general_live.png', tooltip=translate(
            'OpenLP.ServiceManager', 'Send the selected item to Live.'),
            shortcuts=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return],
            category=UiStrings().Service, triggers=self.makeLive)
        self.layout.addWidget(self.orderToolbar)
        # Connect up our signals and slots
        QtCore.QObject.connect(self.themeComboBox,
            QtCore.SIGNAL(u'activated(int)'), self.onThemeComboBoxSelected)
        QtCore.QObject.connect(self.serviceManagerList,
            QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.onMakeLive)
        QtCore.QObject.connect(self.serviceManagerList,
           QtCore.SIGNAL(u'itemCollapsed(QTreeWidgetItem*)'), self.collapsed)
        QtCore.QObject.connect(self.serviceManagerList,
           QtCore.SIGNAL(u'itemExpanded(QTreeWidgetItem*)'), self.expanded)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'theme_update_list'), self.updateThemeList)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_preview_live'), self.previewLive)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_next_item'), self.nextItem)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_previous_item'), self.previousItem)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'servicemanager_set_item'), self.onSetItem)
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
        self.service_theme = Settings().value(
            self.mainwindow.serviceManagerSettingsSection + u'/service theme',
            u'')
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
        self.editAction = create_widget_action(self.menu,
            text=translate('OpenLP.ServiceManager', '&Edit Item'),
            icon=u':/general/general_edit.png', triggers=self.remoteEdit)
        self.maintainAction = create_widget_action(self.menu,
            text=translate('OpenLP.ServiceManager', '&Reorder Item'),
            icon=u':/general/general_edit.png',
            triggers=self.onServiceItemEditForm)
        self.notesAction = create_widget_action(self.menu,
            text=translate('OpenLP.ServiceManager', '&Notes'),
            icon=u':/services/service_notes.png',
            triggers=self.onServiceItemNoteForm)
        self.timeAction = create_widget_action(self.menu,
            text=translate('OpenLP.ServiceManager', '&Start Time'),
            icon=u':/media/media_time.png', triggers=self.onStartTimeForm)
        # Add already existing delete action to the menu.
        self.menu.addAction(self.serviceManagerList.delete)
        self.menu.addSeparator()
        self.previewAction = create_widget_action(self.menu,
            text=translate('OpenLP.ServiceManager', 'Show &Preview'),
            icon=u':/general/general_preview.png', triggers=self.makePreview)
        # Add already existing make live action to the menu.
        self.menu.addAction(self.serviceManagerList.makeLive)
        self.menu.addSeparator()
        self.themeMenu = QtGui.QMenu(
            translate('OpenLP.ServiceManager', '&Change Item Theme'))
        self.menu.addMenu(self.themeMenu)
        self.serviceManagerList.addActions(
            [self.serviceManagerList.moveDown,
            self.serviceManagerList.moveUp,
            self.serviceManagerList.makeLive,
            self.serviceManagerList.moveTop,
            self.serviceManagerList.moveBottom,
            self.serviceManagerList.up,
            self.serviceManagerList.down,
            self.serviceManagerList.expand,
            self.serviceManagerList.collapse
            ])
        self.configUpdated()

    def setModified(self, modified=True):
        """
        Setter for property "modified". Sets whether or not the current service
        has been modified.
        """
        if modified:
            self.serviceId += 1
        self._modified = modified
        serviceFile = self.shortFileName() or translate(
            'OpenLP.ServiceManager', 'Untitled Service')
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
        self.mainwindow.setServiceModified(
            self.isModified(), self.shortFileName())
        Settings().setValue(u'servicemanager/last file', fileName)

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
        self.expandTabs = Settings().value(
            u'advanced/expand service item', False)

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

    def onLoadServiceClicked(self, loadFile=None):
        """
        Loads the service file and saves the existing one it there is one
        unchanged

        ``loadFile``
            The service file to the loaded.  Will be None is from menu so
            selection will be required.
        """
        if self.isModified():
            result = self.saveModifiedService()
            if result == QtGui.QMessageBox.Cancel:
                return False
            elif result == QtGui.QMessageBox.Save:
                self.saveFile()
        if not loadFile:
            fileName = unicode(QtGui.QFileDialog.getOpenFileName(
                self.mainwindow,
                translate('OpenLP.ServiceManager', 'Open File'),
                SettingsManager.get_last_dir(
                self.mainwindow.serviceManagerSettingsSection),
                translate('OpenLP.ServiceManager',
                'OpenLP Service Files (*.osz)')))
            if not fileName:
                return False
        else:
            fileName = loadFile
        SettingsManager.set_last_dir(
            self.mainwindow.serviceManagerSettingsSection,
            split_filename(fileName)[0])
        self.loadFile(fileName)

    def saveModifiedService(self):
        return QtGui.QMessageBox.question(self.mainwindow,
            translate('OpenLP.ServiceManager', 'Modified Service'),
            translate('OpenLP.ServiceManager', 'The current service has '
            'been modified. Would you like to save this service?'),
            QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Save)

    def onRecentServiceClicked(self):
        sender = self.sender()
        self.loadFile(sender.data())

    def newFile(self):
        """
        Create a blank new service file.
        """
        self.serviceManagerList.clear()
        self.serviceItems = []
        self.setFileName(u'')
        self.serviceId += 1
        self.setModified(False)
        Settings().setValue(u'servicemanager/last file', u'')
        Receiver.send_message(u'servicemanager_new_service')

    def saveFile(self):
        """
        Save the current service file.

        A temporary file is created so that we don't overwrite the existing one
        and leave a mangled service file should there be an error when saving.
        Audio files are also copied into the service manager directory, and
        then packaged into the zip file.
        """
        if not self.fileName():
            return self.saveFileAs()
        temp_file, temp_file_name = mkstemp(u'.osz', u'openlp_')
        # We don't need the file handle.
        os.close(temp_file)
        log.debug(temp_file_name)
        path_file_name = unicode(self.fileName())
        path, file_name = os.path.split(path_file_name)
        basename = os.path.splitext(file_name)[0]
        service_file_name = '%s.osd' % basename
        log.debug(u'ServiceManager.saveFile - %s', path_file_name)
        SettingsManager.set_last_dir(
            self.mainwindow.serviceManagerSettingsSection,
            path)
        service = []
        write_list = []
        audio_files = []
        total_size = 0
        Receiver.send_message(u'cursor_busy')
        # Number of items + 1 to zip it
        self.mainwindow.displayProgressBar(len(self.serviceItems) + 1)
        for item in self.serviceItems:
            self.mainwindow.incrementProgressBar()
            service_item = item[u'service_item'].get_service_repr()
            # Get all the audio files, and ready them for embedding in the
            # service file.
            if service_item[u'header'][u'background_audio']:
                for i, filename in \
                    enumerate(service_item[u'header'][u'background_audio']):
                    new_file = os.path.join(u'audio',
                        item[u'service_item']._uuid, filename)
                    audio_files.append((filename, new_file))
                    service_item[u'header'][u'background_audio'][i] = new_file
            # Add the service item to the service.
            service.append({u'serviceitem': service_item})
            if not item[u'service_item'].uses_file():
                continue
            skipMissing = False
            for frame in item[u'service_item'].get_frames():
                if item[u'service_item'].is_image():
                    path_from = frame[u'path']
                else:
                    path_from = os.path.join(frame[u'path'], frame[u'title'])
                # Only write a file once
                if path_from in write_list:
                    continue
                if not os.path.exists(path_from):
                    if not skipMissing:
                        Receiver.send_message(u'cursor_normal')
                        title = unicode(translate('OpenLP.ServiceManager',
                            'Service File Missing'))
                        message = unicode(translate('OpenLP.ServiceManager',
                            'File missing from service\n\n %s \n\n'
                            'Continue saving?' % path_from ))
                        answer = QtGui.QMessageBox.critical(self, title,
                            message,
                            QtGui.QMessageBox.StandardButtons(
                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No |
                            QtGui.QMessageBox.YesToAll))
                        if answer == QtGui.QMessageBox.No:
                            self.mainwindow.finishedProgressBar()
                            return False
                        if answer == QtGui.QMessageBox.YesToAll:
                            skipMissing = True
                        Receiver.send_message(u'cursor_busy')
                else:
                    file_size = os.path.getsize(path_from)
                    write_list.append(path_from)
                    total_size += file_size
        log.debug(u'ServiceManager.saveFile - ZIP contents size is %i bytes' %
            total_size)
        service_content = cPickle.dumps(service)
        # Usual Zip file cannot exceed 2GiB, file with Zip64 cannot be
        # extracted using unzip in UNIX.
        allow_zip_64 = (total_size > 2147483648 + len(service_content))
        log.debug(u'ServiceManager.saveFile - allowZip64 is %s' % allow_zip_64)
        zip = None
        success = True
        self.mainwindow.incrementProgressBar()
        try:
            zip = zipfile.ZipFile(temp_file_name, 'w', zipfile.ZIP_STORED,
                allow_zip_64)
            # First we add service contents.
            # We save ALL filenames into ZIP using UTF-8.
            zip.writestr(service_file_name.encode(u'utf-8'), service_content)
            # Finally add all the listed media files.
            for write_from in write_list:
                zip.write(write_from, write_from.encode(u'utf-8'))
            for audio_from, audio_to in audio_files:
                if audio_from.startswith(u'audio'):
                    # When items are saved, they get new UUID's. Let's copy the
                    # file to the new location. Unused files can be ignored,
                    # OpenLP automatically cleans up the service manager dir on
                    # exit.
                    audio_from = os.path.join(self.servicePath, audio_from)
                save_file = os.path.join(self.servicePath, audio_to)
                save_path = os.path.split(save_file)[0]
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                if not os.path.exists(save_file):
                    shutil.copy(audio_from, save_file)
                zip.write(audio_from, audio_to.encode(u'utf-8'))
        except IOError:
            log.exception(u'Failed to save service to disk: %s', temp_file_name)
            # Add this line in after the release to notify the user that saving
            # their file failed. Commented out due to string freeze.
            #Receiver.send_message(u'openlp_error_message', {
            #    u'title': translate(u'OpenLP.ServiceManager',
            #        u'Error Saving File'),
            #    u'message': translate(u'OpenLP.ServiceManager',
            #        u'There was an error saving your file.')
            #})
            success = False
        finally:
            if zip:
                zip.close()
        self.mainwindow.finishedProgressBar()
        Receiver.send_message(u'cursor_normal')
        if success:
            try:
                shutil.copy(temp_file_name, path_file_name)
            except:
                return self.saveFileAs()
            self.mainwindow.addRecentFile(path_file_name)
            self.setModified(False)
        try:
            delete_file(temp_file_name)
        except:
            pass
        return success

    def saveFileAs(self):
        """
        Get a file name and then call :func:`ServiceManager.saveFile` to
        save the file.
        """
        default_service_enabled = Settings().value(
            u'advanced/default service enabled', True)
        if default_service_enabled:
            service_day = Settings().value(
                u'advanced/default service day', 7).toInt()[0]
            if service_day == 7:
                time = datetime.now()
            else:
                service_hour = Settings().value(
                    u'advanced/default service hour', 11).toInt()[0]
                service_minute = Settings().value(
                    u'advanced/default service minute', 0).toInt()[0]
                now = datetime.now()
                day_delta = service_day - now.weekday()
                if day_delta < 0:
                    day_delta += 7
                time = now + timedelta(days=day_delta)
                time = time.replace(hour=service_hour, minute=service_minute)
            default_pattern = Settings().value(
                u'advanced/default service name',
                translate('OpenLP.AdvancedTab', 'Service %Y-%m-%d %H-%M',
                    'This may not contain any of the following characters: '
                    '/\\?*|<>\[\]":+\nSee http://docs.python.org/library/'
                    'datetime.html#strftime-strptime-behavior for more '
                    'information.'))
            default_filename = time.strftime(default_pattern)
        else:
            default_filename = u''
        directory = SettingsManager.get_last_dir(
            self.mainwindow.serviceManagerSettingsSection)
        path = os.path.join(directory, default_filename)
        fileName = unicode(QtGui.QFileDialog.getSaveFileName(self.mainwindow,
            UiStrings().SaveService, path,
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
        fileName = unicode(fileName)
        if not os.path.exists(fileName):
            return False
        zip = None
        fileTo = None
        try:
            zip = zipfile.ZipFile(fileName)
            for zipinfo in zip.infolist():
                try:
                    ucsfile = zipinfo.filename.decode(u'utf-8')
                except UnicodeDecodeError:
                    log.exception(u'Filename "%s" is not valid UTF-8' %
                        zipinfo.filename.decode(u'utf-8', u'replace'))
                    critical_error_message_box(
                        message=translate('OpenLP.ServiceManager',
                        'File is not a valid service.\n'
                        'The content encoding is not UTF-8.'))
                    continue
                osfile = ucsfile.replace(u'/', os.path.sep)
                if not osfile.startswith(u'audio'):
                    osfile = os.path.split(osfile)[1]
                log.debug(u'Extract file: %s', osfile)
                zipinfo.filename = osfile
                zip.extract(zipinfo, self.servicePath)
                if osfile.endswith(u'osd'):
                    p_file = os.path.join(self.servicePath, osfile)
            if 'p_file' in locals():
                Receiver.send_message(u'cursor_busy')
                fileTo = open(p_file, u'r')
                items = cPickle.load(fileTo)
                fileTo.close()
                self.newFile()
                self.mainwindow.displayProgressBar(len(items))
                for item in items:
                    self.mainwindow.incrementProgressBar()
                    serviceItem = ServiceItem()
                    serviceItem.renderer = self.mainwindow.renderer
                    serviceItem.set_from_service(item, self.servicePath)
                    self.validateItem(serviceItem)
                    self.load_item_uuid = 0
                    if serviceItem.is_capable(ItemCapabilities.OnLoadUpdate):
                        Receiver.send_message(u'%s_service_load' %
                            serviceItem.name.lower(), serviceItem)
                    # if the item has been processed
                    if serviceItem._uuid == self.load_item_uuid:
                        serviceItem.edit_id = int(self.load_item_edit_id)
                        serviceItem.temporary_edit = self.load_item_temporary
                    self.addServiceItem(serviceItem, repaint=False)
                delete_file(p_file)
                self.setFileName(fileName)
                self.mainwindow.addRecentFile(fileName)
                self.setModified(False)
                Settings().setValue(
                    'servicemanager/last file', fileName)
            else:
                critical_error_message_box(
                    message=translate('OpenLP.ServiceManager',
                    'File is not a valid service.'))
                log.exception(u'File contains no service data')
        except (IOError, NameError, zipfile.BadZipfile):
            log.exception(u'Problem loading service file %s' % fileName)
            critical_error_message_box(
                message=translate('OpenLP.ServiceManager',
                'File could not be opened because it is corrupt.'))
        except zipfile.BadZipfile:
            if os.path.getsize(fileName) == 0:
                log.exception(u'Service file is zero sized: %s' % fileName)
                QtGui.QMessageBox.information(self,
                    translate('OpenLP.ServiceManager', 'Empty File'),
                    translate('OpenLP.ServiceManager', 'This service file '
                    'does not contain any data.'))
            else:
                log.exception(u'Service file is cannot be extracted as zip: '
                    u'%s' % fileName)
                QtGui.QMessageBox.information(self,
                    translate('OpenLP.ServiceManager', 'Corrupt File'),
                    translate('OpenLP.ServiceManager', 'This file is either '
                    'corrupt or it is not an OpenLP 2.0 service file.'))
            return
        finally:
            if fileTo:
                fileTo.close()
            if zip:
                zip.close()
        self.mainwindow.finishedProgressBar()
        Receiver.send_message(u'cursor_normal')
        self.repaintServiceList(-1, -1)

    def loadLastFile(self):
        """
        Load the last service item from the service manager when the
        service was last closed. Can be blank if there was no service
        present.
        """
        fileName = Settings().value(u'servicemanager/last file', u'')
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
        self.timeAction.setVisible(False)
        if serviceItem[u'service_item'].is_capable(ItemCapabilities.CanEdit)\
            and serviceItem[u'service_item'].edit_id:
            self.editAction.setVisible(True)
        if serviceItem[u'service_item']\
            .is_capable(ItemCapabilities.CanMaintain):
            self.maintainAction.setVisible(True)
        if item.parent() is None:
            self.notesAction.setVisible(True)
        if serviceItem[u'service_item']\
            .is_capable(ItemCapabilities.HasVariableStartTime):
            self.timeAction.setVisible(True)
        self.themeMenu.menuAction().setVisible(False)
        # Set up the theme menu.
        if serviceItem[u'service_item'].is_text() and \
            self.mainwindow.renderer.theme_level == ThemeLevel.Song:
            self.themeMenu.menuAction().setVisible(True)
            # The service item does not have a theme, check the "Default".
            if serviceItem[u'service_item'].theme is None:
                themeAction = self.themeMenu.defaultAction()
            else:
                themeAction = self.themeMenu.findChild(
                    QtGui.QAction, serviceItem[u'service_item'].theme)
            if themeAction is not None:
                themeAction.setChecked(True)
        self.menu.exec_(self.serviceManagerList.mapToGlobal(point))

    def onServiceItemNoteForm(self):
        item = self.findServiceItem()[0]
        self.serviceNoteForm.textEdit.setPlainText(
            self.serviceItems[item][u'service_item'].notes)
        if self.serviceNoteForm.exec_():
            self.serviceItems[item][u'service_item'].notes = \
                self.serviceNoteForm.textEdit.toPlainText()
            self.repaintServiceList(item, -1)
            self.setModified()

    def onStartTimeForm(self):
        """
        Opens a dialog to type in service item notes.
        """
        item = self.findServiceItem()[0]
        self.startTimeForm.item = self.serviceItems[item]
        if self.startTimeForm.exec_():
            self.repaintServiceList(item, -1)

    def onServiceItemEditForm(self):
        item = self.findServiceItem()[0]
        self.serviceItemEditForm.setServiceItem(
            self.serviceItems[item][u'service_item'])
        if self.serviceItemEditForm.exec_():
            self.addServiceItem(self.serviceItemEditForm.getServiceItem(),
                replace=True, expand=self.serviceItems[item][u'expanded'])

    def previewLive(self, message):
        """
        Called by the SlideController to request a preview item be made live
        and allows the next preview to be updated if relevent.
        """
        uuid, row = message.split(u':')
        for sitem in self.serviceItems:
            if sitem[u'service_item']._uuid == uuid:
                item = self.serviceManagerList.topLevelItem(sitem[u'order'] - 1)
                self.serviceManagerList.setCurrentItem(item)
                self.makeLive(int(row))
                return

    def nextItem(self):
        """
        Called by the SlideController to select the next service item.
        """
        if not self.serviceManagerList.selectedItems():
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

    def previousItem(self, message):
        """
        Called by the SlideController to select the previous service item.
        """
        if not self.serviceManagerList.selectedItems():
            return
        selected = self.serviceManagerList.selectedItems()[0]
        prevItem = None
        prevItemLastSlide = None
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.serviceManagerList)
        while serviceIterator.value():
            if serviceIterator.value() == selected:
                if message == u'last slide' and prevItemLastSlide:
                    pos = prevItem.data(0, QtCore.Qt.UserRole).toInt()[0]
                    check_expanded = self.serviceItems[pos - 1][u'expanded']
                    self.serviceManagerList.setCurrentItem(prevItemLastSlide)
                    if not check_expanded:
                        self.serviceManagerList.collapseItem(prevItem)
                    self.makeLive()
                    self.serviceManagerList.setCurrentItem(prevItem)
                elif prevItem:
                    self.serviceManagerList.setCurrentItem(prevItem)
                    self.makeLive()
                return
            if serviceIterator.value().parent() is None:
                prevItem = serviceIterator.value()
            if serviceIterator.value().parent() is prevItem:
                prevItemLastSlide = serviceIterator.value()
            serviceIterator += 1

    def onSetItem(self, message):
        """
        Called by a signal to select a specific item.
        """
        self.setItem(int(message))

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
        Moves the cursor selection up the window.
        Called by the up arrow.
        """
        item = self.serviceManagerList.currentItem()
        itemBefore = self.serviceManagerList.itemAbove(item)
        if itemBefore is None:
            return
        self.serviceManagerList.setCurrentItem(itemBefore)

    def onMoveSelectionDown(self):
        """
        Moves the cursor selection down the window.
        Called by the down arrow.
        """
        item = self.serviceManagerList.currentItem()
        itemAfter = self.serviceManagerList.itemBelow(item)
        if itemAfter is None:
            return
        self.serviceManagerList.setCurrentItem(itemAfter)

    def onCollapseAll(self):
        """
        Collapse all the service items.
        """
        for item in self.serviceItems:
            item[u'expanded'] = False
        self.serviceManagerList.collapseAll()

    def collapsed(self, item):
        """
        Record if an item is collapsed. Used when repainting the list to get the
        correct state.
        """
        pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        self.serviceItems[pos - 1][u'expanded'] = False

    def onExpandAll(self):
        """
        Collapse all the service items.
        """
        for item in self.serviceItems:
            item[u'expanded'] = True
        self.serviceManagerList.expandAll()

    def expanded(self, item):
        """
        Record if an item is collapsed. Used when repainting the list to get the
        correct state.
        """
        pos = item.data(0, QtCore.Qt.UserRole).toInt()[0]
        self.serviceItems[pos - 1][u'expanded'] = True

    def onServiceTop(self):
        """
        Move the current ServiceItem to the top of the list.
        """
        item, child = self.findServiceItem()
        if item < len(self.serviceItems) and item != -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(0, temp)
            self.repaintServiceList(0, child)
            self.setModified()

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
            self.setModified()

    def onServiceDown(self):
        """
        Move the current ServiceItem one position down in the list.
        """
        item, child = self.findServiceItem()
        if item < len(self.serviceItems) and item != -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(item + 1, temp)
            self.repaintServiceList(item + 1, child)
            self.setModified()

    def onServiceEnd(self):
        """
        Move the current ServiceItem to the bottom of the list.
        """
        item, child = self.findServiceItem()
        if item < len(self.serviceItems) and item != -1:
            temp = self.serviceItems[item]
            self.serviceItems.remove(self.serviceItems[item])
            self.serviceItems.insert(len(self.serviceItems), temp)
            self.repaintServiceList(len(self.serviceItems) - 1, child)
            self.setModified()

    def onDeleteFromService(self):
        """
        Remove the current ServiceItem from the list.
        """
        item = self.findServiceItem()[0]
        if item != -1:
            self.serviceItems.remove(self.serviceItems[item])
            self.repaintServiceList(item - 1, -1)
            self.setModified()

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
                elif serviceitem.temporary_edit:
                    icon = QtGui.QImage(serviceitem.icon)
                    icon = icon.scaled(80, 80, QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation)
                    overlay = QtGui.QImage(':/general/general_export.png')
                    overlay = overlay.scaled(40, 40, QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation)
                    painter = QtGui.QPainter(icon)
                    painter.drawImage(40, 0, overlay)
                    painter.end()
                    treewidgetitem.setIcon(0, build_icon(icon))
                else:
                    treewidgetitem.setIcon(0, serviceitem.iconic_representation)
            else:
                treewidgetitem.setIcon(0,
                    build_icon(u':/general/general_delete.png'))
            treewidgetitem.setText(0, serviceitem.get_display_title())
            tips = []
            if serviceitem.temporary_edit:
                tips.append(u'<strong>%s:</strong> <em>%s</em>' %
                    (unicode(translate('OpenLP.ServiceManager', 'Edit')),
                    (unicode(translate('OpenLP.ServiceManager',
                    'Service copy only')))))
            if serviceitem.theme and serviceitem.theme != -1:
                tips.append(u'<strong>%s:</strong> <em>%s</em>' %
                    (unicode(translate('OpenLP.ServiceManager', 'Slide theme')),
                    serviceitem.theme))
            if serviceitem.notes:
                tips.append(u'<strong>%s: </strong> %s' %
                    (unicode(translate('OpenLP.ServiceManager', 'Notes')),
                    cgi.escape(unicode(serviceitem.notes))))
            if item[u'service_item'] \
                .is_capable(ItemCapabilities.HasVariableStartTime):
                tips.append(item[u'service_item'].get_media_time())
            treewidgetitem.setToolTip(0, u'<br>'.join(tips))
            treewidgetitem.setData(0, QtCore.Qt.UserRole, item[u'order'])
            treewidgetitem.setSelected(item[u'selected'])
            # Add the children to their parent treewidgetitem.
            for count, frame in enumerate(serviceitem.get_frames()):
                child = QtGui.QTreeWidgetItem(treewidgetitem)
                text = frame[u'title'].replace(u'\n', u' ')
                child.setText(0, text[:40])
                child.setData(0, QtCore.Qt.UserRole, count)
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
        log.debug(u'Cleaning up servicePath')
        for file in os.listdir(self.servicePath):
            file_path = os.path.join(self.servicePath, file)
            delete_file(file_path)
        if os.path.exists(os.path.join(self.servicePath, u'audio')):
            shutil.rmtree(os.path.join(self.servicePath, u'audio'), True)

    def onThemeComboBoxSelected(self, currentIndex):
        """
        Set the theme for the current service.
        """
        log.debug(u'onThemeComboBoxSelected')
        self.service_theme = unicode(self.themeComboBox.currentText())
        self.mainwindow.renderer.set_service_theme(self.service_theme)
        Settings().setValue(
            self.mainwindow.serviceManagerSettingsSection +
            u'/service theme', self.service_theme)
        self.regenerateServiceItems(True)

    def themeChange(self):
        """
        The theme may have changed in the settings dialog so make
        sure the theme combo box is in the correct state.
        """
        log.debug(u'themeChange')
        visible = self.mainwindow.renderer.theme_level == ThemeLevel.Global
        self.themeLabel.setVisible(visible)
        self.themeComboBox.setVisible(visible)

    def regenerateServiceItems(self, changed=False):
        """
        Rebuild the service list as things have changed and a
        repaint is the easiest way to do this.
        """
        Receiver.send_message(u'cursor_busy')
        log.debug(u'regenerateServiceItems')
        # force reset of renderer as theme data has changed
        self.mainwindow.renderer.themedata = None
        if self.serviceItems:
            for item in self.serviceItems:
                item[u'selected'] = False
            serviceIterator = QtGui.QTreeWidgetItemIterator(
                self.serviceManagerList)
            selectedItem = None
            while serviceIterator.value():
                if serviceIterator.value().isSelected():
                    selectedItem = serviceIterator.value()
                serviceIterator += 1
            if selectedItem is not None:
                if selectedItem.parent() is None:
                    pos = selectedItem.data(0, QtCore.Qt.UserRole).toInt()[0]
                else:
                    pos = selectedItem.parent().data(0, QtCore.Qt.UserRole). \
                        toInt()[0]
                self.serviceItems[pos - 1][u'selected'] = True
            tempServiceItems = self.serviceItems
            self.serviceManagerList.clear()
            self.serviceItems = []
            self.isNew = True
            for item in tempServiceItems:
                self.addServiceItem(
                    item[u'service_item'], False, expand=item[u'expanded'],
                    repaint=False, selected=item[u'selected'])
            # Set to False as items may have changed rendering
            # does not impact the saved song so True may also be valid
            if changed:
                self.setModified()
            # Repaint it once only at the end
            self.repaintServiceList(-1, -1)
        Receiver.send_message(u'cursor_normal')

    def serviceItemUpdate(self, message):
        """
        Triggered from plugins to update service items.
        Save the values as they will be used as part of the service load
        """
        edit_id, self.load_item_uuid, temporary = message.split(u':')
        self.load_item_edit_id = int(edit_id)
        self.load_item_temporary = str_to_bool(temporary)

    def replaceServiceItem(self, newItem):
        """
        Using the service item passed replace the one with the same edit id
        if found.
        """
        for itemcount, item in enumerate(self.serviceItems):
            if item[u'service_item'].edit_id == newItem.edit_id and \
                item[u'service_item'].name == newItem.name:
                newItem.render()
                newItem.merge(item[u'service_item'])
                item[u'service_item'] = newItem
                self.repaintServiceList(itemcount + 1, 0)
                self.mainwindow.liveController.replaceServiceManagerItem(
                    newItem)
                self.setModified()

    def addServiceItem(self, item, rebuild=False, expand=None, replace=False,
        repaint=True, selected=False):
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
        item.from_service = True
        if replace:
            sitem, child = self.findServiceItem()
            item.merge(self.serviceItems[sitem][u'service_item'])
            self.serviceItems[sitem][u'service_item'] = item
            self.repaintServiceList(sitem, child)
            self.mainwindow.liveController.replaceServiceManagerItem(item)
        else:
            item.render()
            # nothing selected for dnd
            if self.dropPosition == 0:
                if isinstance(item, list):
                    for inditem in item:
                        self.serviceItems.append({u'service_item': inditem,
                            u'order': len(self.serviceItems) + 1,
                            u'expanded': expand, u'selected': selected})
                else:
                    self.serviceItems.append({u'service_item': item,
                        u'order': len(self.serviceItems) + 1,
                        u'expanded': expand, u'selected': selected})
                if repaint:
                    self.repaintServiceList(len(self.serviceItems) - 1, -1)
            else:
                self.serviceItems.insert(self.dropPosition,
                    {u'service_item': item, u'order': self.dropPosition,
                    u'expanded': expand, u'selected': selected})
                self.repaintServiceList(self.dropPosition, -1)
            # if rebuilding list make sure live is fixed.
            if rebuild:
                self.mainwindow.liveController.replaceServiceManagerItem(item)
        self.dropPosition = 0
        self.setModified()

    def makePreview(self):
        """
        Send the current item to the Preview slide controller
        """
        Receiver.send_message(u'cursor_busy')
        item, child = self.findServiceItem()
        if self.serviceItems[item][u'service_item'].is_valid:
            self.mainwindow.previewController.addServiceManagerItem(
                self.serviceItems[item][u'service_item'], child)
        else:
            critical_error_message_box(
                translate('OpenLP.ServiceManager', 'Missing Display Handler'),
                translate('OpenLP.ServiceManager', 'Your item cannot be '
                'displayed as there is no handler to display it'))
        Receiver.send_message(u'cursor_normal')

    def getServiceItem(self):
        """
        Send the current item to the Preview slide controller
        """
        item = self.findServiceItem()[0]
        if item == -1:
            return False
        else:
            return self.serviceItems[item][u'service_item']

    def onMakeLive(self):
        """
        Send the current item to the Live slide controller but triggered
        by a tablewidget click event.
        """
        self.makeLive()

    def makeLive(self, row=-1):
        """
        Send the current item to the Live slide controller

        ``row``
            Row number to be displayed if from preview.
            -1 is passed if the value is not set
        """
        item, child = self.findServiceItem()
        # No items in service
        if item == -1:
            return
        if row != -1:
            child = row
        Receiver.send_message(u'cursor_busy')
        if self.serviceItems[item][u'service_item'].is_valid:
            self.mainwindow.liveController.addServiceManagerItem(
                self.serviceItems[item][u'service_item'], child)
            if Settings().value(
                self.mainwindow.generalSettingsSection + u'/auto preview',
                False):
                item += 1
                if self.serviceItems and item < len(self.serviceItems) and \
                    self.serviceItems[item][u'service_item'].is_capable(
                    ItemCapabilities.CanPreview):
                    self.mainwindow.previewController.addServiceManagerItem(
                        self.serviceItems[item][u'service_item'], 0)
                    self.mainwindow.liveController.previewListWidget.setFocus()
        else:
            critical_error_message_box(
                translate('OpenLP.ServiceManager', 'Missing Display Handler'),
                translate('OpenLP.ServiceManager', 'Your item cannot be '
                'displayed as the plugin required to display it is missing '
                'or inactive'))
        Receiver.send_message(u'cursor_normal')

    def remoteEdit(self):
        """
        Posts a remote edit message to a plugin to allow item to be edited.
        """
        item = self.findServiceItem()[0]
        if self.serviceItems[item][u'service_item']\
            .is_capable(ItemCapabilities.CanEdit):
            Receiver.send_message(u'%s_edit' %
                self.serviceItems[item][u'service_item'].name.lower(),
                u'L:%s' % self.serviceItems[item][u'service_item'].edit_id)

    def findServiceItem(self):
        """
        Finds the first selected ServiceItem in the list and returns the
        position of the serviceitem and its selected child item. For example,
        if the third child item (in the Slidecontroller known as slide) in the
        second service item is selected this will return::

            (1, 2)
        """
        items = self.serviceManagerList.selectedItems()
        serviceItem = -1
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
            # Only process the first item on the list for this method.
            break
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
        if link.hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in link.urls():
                filename = unicode(url.toLocalFile())
                if filename.endswith(u'.osz'):
                    self.onLoadServiceClicked(filename)
        elif link.hasText():
            plugin = unicode(link.text())
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
                self.setModified()
            else:
                # we are not over anything so drop
                replace = False
                if item is None:
                    self.dropPosition = len(self.serviceItems)
                else:
                    # we are over something so lets investigate
                    pos = self._getParentItemData(item) - 1
                    serviceItem = self.serviceItems[pos]
                    if (plugin == serviceItem[u'service_item'].name and
                        serviceItem[u'service_item'].is_capable(
                        ItemCapabilities.CanAppend)):
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
        themeGroup = QtGui.QActionGroup(self.themeMenu)
        themeGroup.setExclusive(True)
        themeGroup.setObjectName(u'themeGroup')
        # Create a "Default" theme, which allows the user to reset the item's
        # theme to the service theme or global theme.
        defaultTheme = create_widget_action(self.themeMenu,
            text=UiStrings().Default, checked=False,
            triggers=self.onThemeChangeAction)
        self.themeMenu.setDefaultAction(defaultTheme)
        themeGroup.addAction(defaultTheme)
        self.themeMenu.addSeparator()
        for theme in theme_list:
            self.themeComboBox.addItem(theme)
            themeGroup.addAction(create_widget_action(self.themeMenu, theme,
                text=theme, checked=False, triggers=self.onThemeChangeAction))
        find_and_set_in_combo_box(self.themeComboBox, self.service_theme)
        self.mainwindow.renderer.set_service_theme(self.service_theme)
        self.regenerateServiceItems()

    def onThemeChangeAction(self):
        theme = unicode(self.sender().objectName())
        # No object name means that the "Default" theme is supposed to be used.
        if not theme:
            theme = None
        item = self.findServiceItem()[0]
        self.serviceItems[item][u'service_item'].update_theme(theme)
        self.regenerateServiceItems(True)

    def _getParentItemData(self, item):
        parentitem = item.parent()
        if parentitem is None:
            return item.data(0, QtCore.Qt.UserRole).toInt()[0]
        else:
            return parentitem.data(0, QtCore.Qt.UserRole).toInt()[0]

    def printServiceOrder(self):
        """
        Print a Service Order Sheet.
        """
        settingDialog = PrintServiceForm(self.mainwindow, self)
        settingDialog.exec_()
