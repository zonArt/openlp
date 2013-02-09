# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The service manager sets up, loads, saves and manages services.
"""
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

from openlp.core.lib import OpenLPToolbar, ServiceItem, Receiver, ItemCapabilities, Settings, PluginStatus, Registry, \
    UiStrings, build_icon, translate, str_to_bool, check_directory_exists
from openlp.core.lib.theme import ThemeLevel
from openlp.core.lib.ui import critical_error_message_box, create_widget_action, find_and_set_in_combo_box
from openlp.core.ui import ServiceNoteForm, ServiceItemEditForm, StartTimeForm
from openlp.core.ui.printserviceform import PrintServiceForm
from openlp.core.utils import AppLocation, delete_file, split_filename, format_time
from openlp.core.utils.actions import ActionList, CategoryOrder


class ServiceManagerList(QtGui.QTreeWidget):
    """
    Set up key bindings and mouse behaviour for the service list
    """
    def __init__(self, serviceManager, parent=None):
        """
        Constructor
        """
        QtGui.QTreeWidget.__init__(self, parent)
        self.serviceManager = serviceManager

    def keyPressEvent(self, event):
        """
        Capture Key press and respond accordingly.
        """
        if isinstance(event, QtGui.QKeyEvent):
            # here accept the event and do something
            if event.key() == QtCore.Qt.Key_Up:
                self.serviceManager.on_move_selection_up()
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                self.serviceManager.on_move_selection_down()
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
        mime_data = QtCore.QMimeData()
        drag.setMimeData(mime_data)
        mime_data.setText(u'ServiceManager')
        drag.start(QtCore.Qt.CopyAction)


class ServiceManagerDialog(object):
    """
    UI part of the Service Manager
    """
    def setup_ui(self, widget):
        """
        Define the UI
        """
        # Create the top toolbar
        self.toolbar = OpenLPToolbar(self)
        self.toolbar.addToolbarAction(u'newService', text=UiStrings().NewService, icon=u':/general/general_new.png',
            tooltip=UiStrings().CreateService, triggers=self.on_new_service_clicked)
        self.toolbar.addToolbarAction(u'openService', text=UiStrings().OpenService, icon=u':/general/general_open.png',
            tooltip=translate('OpenLP.ServiceManager', 'Load an existing service.'),
            triggers=self.on_load_service_clicked)
        self.toolbar.addToolbarAction(u'saveService', text=UiStrings().SaveService, icon=u':/general/general_save.png',
            tooltip=translate('OpenLP.ServiceManager', 'Save this service.'), triggers=self.decide_save_method)
        self.toolbar.addSeparator()
        self.theme_label = QtGui.QLabel(u'%s:' % UiStrings().Theme, self)
        self.theme_label.setMargin(3)
        self.theme_label.setObjectName(u'theme_label')
        self.toolbar.addToolbarWidget(self.theme_label)
        self.theme_combo_box = QtGui.QComboBox(self.toolbar)
        self.theme_combo_box.setToolTip(translate('OpenLP.ServiceManager', 'Select a theme for the service.'))
        self.theme_combo_box.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.theme_combo_box.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.theme_combo_box.setObjectName(u'theme_combo_box')
        self.toolbar.addToolbarWidget(self.theme_combo_box)
        self.toolbar.setObjectName(u'toolbar')
        self.layout.addWidget(self.toolbar)
        # Create the service manager list
        self.service_manager_list = ServiceManagerList(self)
        self.service_manager_list.setEditTriggers(
            QtGui.QAbstractItemView.CurrentChanged |
            QtGui.QAbstractItemView.DoubleClicked |
            QtGui.QAbstractItemView.EditKeyPressed)
        self.service_manager_list.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.service_manager_list.setAlternatingRowColors(True)
        self.service_manager_list.setHeaderHidden(True)
        self.service_manager_list.setExpandsOnDoubleClick(False)
        self.service_manager_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.service_manager_list, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
            self.context_menu)
        self.service_manager_list.setObjectName(u'service_manager_list')
        # enable drop
        self.service_manager_list.__class__.dragEnterEvent = self.drag_enter_event
        self.service_manager_list.__class__.dragMoveEvent = self.drag_enter_event
        self.service_manager_list.__class__.dropEvent = self.drop_event
        self.layout.addWidget(self.service_manager_list)
        # Add the bottom toolbar
        self.order_toolbar = OpenLPToolbar(self)
        action_list = ActionList.get_instance()
        action_list.add_category(UiStrings().Service, CategoryOrder.standardToolbar)
        self.service_manager_list.moveTop = self.order_toolbar.addToolbarAction(u'moveTop',
            text=translate('OpenLP.ServiceManager', 'Move to &top'), icon=u':/services/service_top.png',
            tooltip=translate('OpenLP.ServiceManager', 'Move item to the top of the service.'),
            shortcuts=[QtCore.Qt.Key_Home], category=UiStrings().Service, triggers=self.onServiceTop)
        self.service_manager_list.moveUp = self.order_toolbar.addToolbarAction(u'moveUp',
            text=translate('OpenLP.ServiceManager', 'Move &up'), icon=u':/services/service_up.png',
            tooltip=translate('OpenLP.ServiceManager', 'Move item up one position in the service.'),
            shortcuts=[QtCore.Qt.Key_PageUp], category=UiStrings().Service, triggers=self.onServiceUp)
        self.service_manager_list.moveDown = self.order_toolbar.addToolbarAction(u'moveDown',
            text=translate('OpenLP.ServiceManager', 'Move &down'), icon=u':/services/service_down.png',
            tooltip=translate('OpenLP.ServiceManager', 'Move item down one position in the service.'),
            shortcuts=[QtCore.Qt.Key_PageDown], category=UiStrings().Service, triggers=self.onServiceDown)
        self.service_manager_list.moveBottom = self.order_toolbar.addToolbarAction(u'moveBottom',
            text=translate('OpenLP.ServiceManager', 'Move to &bottom'), icon=u':/services/service_bottom.png',
            tooltip=translate('OpenLP.ServiceManager', 'Move item to the end of the service.'),
            shortcuts=[QtCore.Qt.Key_End], category=UiStrings().Service, triggers=self.onServiceEnd)
        self.service_manager_list.down = self.order_toolbar.addToolbarAction(u'down',
            text=translate('OpenLP.ServiceManager', 'Move &down'),
            tooltip=translate('OpenLP.ServiceManager', 'Moves the selection down the window.'), visible=False,
            shortcuts=[QtCore.Qt.Key_Down], triggers=self.on_move_selection_down)
        action_list.add_action(self.service_manager_list.down)
        self.service_manager_list.up = self.order_toolbar.addToolbarAction(u'up',
            text=translate('OpenLP.ServiceManager', 'Move up'), tooltip=translate('OpenLP.ServiceManager',
                'Moves the selection up the window.'), visible=False, shortcuts=[QtCore.Qt.Key_Up],
            triggers=self.on_move_selection_up)
        action_list.add_action(self.service_manager_list.up)
        self.order_toolbar.addSeparator()
        self.service_manager_list.delete = self.order_toolbar.addToolbarAction(u'delete',
            text=translate('OpenLP.ServiceManager', '&Delete From Service'), icon=u':/general/general_delete.png',
            tooltip=translate('OpenLP.ServiceManager', 'Delete the selected item from the service.'),
            shortcuts=[QtCore.Qt.Key_Delete], triggers=self.onDeleteFromService)
        self.order_toolbar.addSeparator()
        self.service_manager_list.expand = self.order_toolbar.addToolbarAction(u'expand',
            text=translate('OpenLP.ServiceManager', '&Expand all'), icon=u':/services/service_expand_all.png',
            tooltip=translate('OpenLP.ServiceManager', 'Expand all the service items.'),
            shortcuts=[QtCore.Qt.Key_Plus], category=UiStrings().Service, triggers=self.onExpandAll)
        self.service_manager_list.collapse = self.order_toolbar.addToolbarAction(u'collapse',
            text=translate('OpenLP.ServiceManager', '&Collapse all'), icon=u':/services/service_collapse_all.png',
            tooltip=translate('OpenLP.ServiceManager', 'Collapse all the service items.'),
            shortcuts=[QtCore.Qt.Key_Minus], category=UiStrings().Service, triggers=self.onCollapseAll)
        self.order_toolbar.addSeparator()
        self.service_manager_list.make_live = self.order_toolbar.addToolbarAction(u'make_live',
            text=translate('OpenLP.ServiceManager', 'Go Live'), icon=u':/general/general_live.png',
            tooltip=translate('OpenLP.ServiceManager', 'Send the selected item to Live.'),
            shortcuts=[QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return], category=UiStrings().Service,
            triggers=self.make_live)
        self.layout.addWidget(self.order_toolbar)
        # Connect up our signals and slots
        QtCore.QObject.connect(self.theme_combo_box, QtCore.SIGNAL(u'activated(int)'),
            self.on_theme_combo_box_selected)
        QtCore.QObject.connect(self.service_manager_list, QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
            self.on_make_live)
        QtCore.QObject.connect(self.service_manager_list, QtCore.SIGNAL(u'itemCollapsed(QTreeWidgetItem*)'),
            self.collapsed)
        QtCore.QObject.connect(self.service_manager_list, QtCore.SIGNAL(u'itemExpanded(QTreeWidgetItem*)'),
            self.expanded)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_update_list'), self.update_theme_list)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_updated'), self.config_updated)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_screen_changed'),
            self.regenerate_service_Items)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_update_global'), self.theme_change)
        # Last little bits of setting up
        self.service_theme = Settings().value(self.main_window.serviceManagerSettingsSection + u'/service theme')
        self.servicePath = AppLocation.get_section_data_path(u'servicemanager')
        # build the drag and drop context menu
        self.dndMenu = QtGui.QMenu()
        self.newAction = self.dndMenu.addAction(translate('OpenLP.ServiceManager', '&Add New Item'))
        self.newAction.setIcon(build_icon(u':/general/general_edit.png'))
        self.addToAction = self.dndMenu.addAction(translate('OpenLP.ServiceManager', '&Add to Selected Item'))
        self.addToAction.setIcon(build_icon(u':/general/general_edit.png'))
        # build the context menu
        self.menu = QtGui.QMenu()
        self.edit_action = create_widget_action(self.menu, text=translate('OpenLP.ServiceManager', '&Edit Item'),
            icon=u':/general/general_edit.png', triggers=self.remote_edit)
        self.maintain_action = create_widget_action(self.menu, text=translate('OpenLP.ServiceManager', '&Reorder Item'),
            icon=u':/general/general_edit.png', triggers=self.on_service_item_edit_form)
        self.notes_action = create_widget_action(self.menu, text=translate('OpenLP.ServiceManager', '&Notes'),
            icon=u':/services/service_notes.png', triggers=self.on_service_item_note_form)
        self.time_action = create_widget_action(self.menu, text=translate('OpenLP.ServiceManager', '&Start Time'),
            icon=u':/media/media_time.png', triggers=self.on_start_time_form)
        self.auto_start_action = create_widget_action(self.menu, text=u'',
            icon=u':/media/auto-start_active.png', triggers=self.on_auto_start)
        # Add already existing delete action to the menu.
        self.menu.addAction(self.service_manager_list.delete)
        self.create_custom_action = create_widget_action(self.menu,
            text=translate('OpenLP.ServiceManager', 'Create New &Custom Slide'),
            icon=u':/general/general_edit.png', triggers=self.create_custom)
        self.menu.addSeparator()
        # Add AutoPlay menu actions
        self.auto_play_slides_group = QtGui.QMenu(translate('OpenLP.ServiceManager', '&Auto play slides'))
        self.menu.addMenu(self.auto_play_slides_group)
        self.auto_play_slides_loop = create_widget_action(self.auto_play_slides_group,
            text=translate('OpenLP.ServiceManager', 'Auto play slides &Loop'),
            checked=False, triggers=self.toggle_auto_play_slides_loop)
        self.auto_play_slides_once = create_widget_action(self.auto_play_slides_group,
            text=translate('OpenLP.ServiceManager', 'Auto play slides &Once'),
            checked=False, triggers=self.toggle_auto_play_slides_once)
        self.auto_play_slides_group.addSeparator()
        self.timed_slide_interval = create_widget_action(self.auto_play_slides_group,
            text=translate('OpenLP.ServiceManager', '&Delay between slides'),
            checked=False, triggers=self.on_timed_slide_interval)
        self.menu.addSeparator()
        self.preview_action = create_widget_action(self.menu, text=translate('OpenLP.ServiceManager', 'Show &Preview'),
            icon=u':/general/general_preview.png', triggers=self.make_preview)
        # Add already existing make live action to the menu.
        self.menu.addAction(self.service_manager_list.make_live)
        self.menu.addSeparator()
        self.theme_menu = QtGui.QMenu(translate('OpenLP.ServiceManager', '&Change Item Theme'))
        self.menu.addMenu(self.theme_menu)
        self.service_manager_list.addActions(
            [self.service_manager_list.moveDown,
             self.service_manager_list.moveUp,
             self.service_manager_list.make_live,
             self.service_manager_list.moveTop,
             self.service_manager_list.moveBottom,
             self.service_manager_list.up,
             self.service_manager_list.down,
             self.service_manager_list.expand,
             self.service_manager_list.collapse
            ])

    def drag_enter_event(self, event):
        """
        Accept Drag events

        ``event``
            Handle of the event pint passed
        """
        event.accept()


class ServiceManager(QtGui.QWidget, ServiceManagerDialog):
    """
    Manages the services. This involves taking text strings from plugins and
    adding them to the service. This service can then be zipped up with all
    the resources used into one OSZ or oszl file for use on any OpenLP v2
    installation. Also handles the UI tasks of moving things up and down etc.
    """
    def __init__(self, parent=None):
        """
        Sets up the service manager, toolbars, list view, et al.
        """
        QtGui.QWidget.__init__(self, parent)
        self.active = build_icon(QtGui.QImage(u':/media/auto-start_active.png'))
        self.inactive = build_icon(QtGui.QImage(u':/media/auto-start_inactive.png'))
        Registry().register(u'service_manager', self)
        self.service_items = []
        self.suffixes = []
        self.drop_position = 0
        self.expand_tabs = False
        self.service_id = 0
        # is a new service and has not been saved
        self._modified = False
        self._file_name = u''
        self.service_has_all_original_files = True
        self.serviceNoteForm = ServiceNoteForm()
        self.serviceItemEditForm = ServiceItemEditForm()
        self.startTimeForm = StartTimeForm()
        # start with the layout
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.setup_ui(self)
        self.config_updated()

    def set_modified(self, modified=True):
        """
        Setter for property "modified". Sets whether or not the current service
        has been modified.
        """
        if modified:
            self.service_id += 1
        self._modified = modified
        service_file = self.short_file_name() or translate('OpenLP.ServiceManager', 'Untitled Service')
        self.main_window.setServiceModified(modified, service_file)

    def is_modified(self):
        """
        Getter for boolean property "modified".
        """
        return self._modified

    def set_file_name(self, file_name):
        """
        Setter for service file.
        """
        self._file_name = unicode(file_name)
        self.main_window.setServiceModified(self.is_modified(), self.short_file_name())
        Settings().setValue(u'servicemanager/last file', file_name)
        self._saveLite = self._file_name.endswith(u'.oszl')

    def file_name(self):
        """
        Return the current file name including path.
        """
        return self._file_name

    def short_file_name(self):
        """
        Return the current file name, excluding the path.
        """
        return split_filename(self._file_name)[1]

    def config_updated(self):
        """
        Triggered when Config dialog is updated.
        """
        self.expand_tabs = Settings().value(u'advanced/expand service item')

    def reset_supported_suffixes(self):
        """
        Resets the Suffixes list.

        """
        self.suffixes = []

    def supported_suffixes(self, suffix):
        """
        Adds Suffixes supported to the master list.  Called from Plugins.

        ``suffix``
            New Suffix to be supported
        """
        if not suffix in self.suffixes:
            self.suffixes.append(suffix)

    def on_new_service_clicked(self):
        """
        Create a new service.
        """
        if self.is_modified():
            result = self.save_modified_service()
            if result == QtGui.QMessageBox.Cancel:
                return False
            elif result == QtGui.QMessageBox.Save:
                if not self.decide_save_method():
                    return False
        self.new_file()

    def on_load_service_clicked(self, load_file=None):
        """
        Loads the service file and saves the existing one it there is one
        unchanged

        ``load_file``
            The service file to the loaded.  Will be None is from menu so
            selection will be required.
        """
        if self.is_modified():
            result = self.save_modified_service()
            if result == QtGui.QMessageBox.Cancel:
                return False
            elif result == QtGui.QMessageBox.Save:
                self.decide_save_method()
        if not load_file:
            file_name = QtGui.QFileDialog.getOpenFileName(
                self.main_window,
                translate('OpenLP.ServiceManager', 'Open File'),
                Settings().value(self.main_window.serviceManagerSettingsSection + u'/last directory'),
                translate('OpenLP.ServiceManager', 'OpenLP Service Files (*.osz *.oszl)')
            )
            if not file_name:
                return False
        else:
            file_name = load_file
        Settings().setValue(self.main_window.serviceManagerSettingsSection + u'/last directory',
            split_filename(file_name)[0])
        self.load_file(file_name)

    def save_modified_service(self):
        """
        Check to see if a service needs to be saved.
        """
        return QtGui.QMessageBox.question(self.main_window,
            translate('OpenLP.ServiceManager', 'Modified Service'),
            translate('OpenLP.ServiceManager',
                'The current service has been modified. Would you like to save this service?'),
            QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Save)

    def on_recent_service_clicked(self):
        """
        Load a recent file as the service triggered by mainwindow recent service list.
        """
        sender = self.sender()
        self.load_file(sender.data())

    def new_file(self):
        """
        Create a blank new service file.
        """
        self.service_manager_list.clear()
        self.service_items = []
        self.set_file_name(u'')
        self.service_id += 1
        self.set_modified(False)
        Settings().setValue(u'servicemanager/last file', u'')
        self.plugin_manager.new_service_created()

    def save_file(self):
        """
        Save the current service file.

        A temporary file is created so that we don't overwrite the existing one
        and leave a mangled service file should there be an error when saving.
        Audio files are also copied into the service manager directory, and
        then packaged into the zip file.
        """
        if not self.file_name():
            return self.save_file_as()
        temp_file, temp_file_name = mkstemp(u'.osz', u'openlp_')
        # We don't need the file handle.
        os.close(temp_file)
        log.debug(temp_file_name)
        path_file_name = unicode(self.file_name())
        path, file_name = os.path.split(path_file_name)
        base_name = os.path.splitext(file_name)[0]
        service_file_name = '%s.osd' % base_name
        log.debug(u'ServiceManager.save_file - %s', path_file_name)
        Settings().setValue(self.main_window.serviceManagerSettingsSection + u'/last directory', path)
        service = []
        write_list = []
        missing_list = []
        audio_files = []
        total_size = 0
        self.application.set_busy_cursor()
        # Number of items + 1 to zip it
        self.main_window.displayProgressBar(len(self.service_items) + 1)
        # Get list of missing files, and list of files to write
        for item in self.service_items:
            if not item[u'service_item'].uses_file():
                continue
            for frame in item[u'service_item'].get_frames():
                path_from = item[u'service_item'].get_frame_path(frame=frame)
                if path_from in write_list or path_from in missing_list:
                    continue
                if not os.path.exists(path_from):
                    missing_list.append(path_from)
                else:
                    write_list.append(path_from)
        if missing_list:
            self.application.set_normal_cursor()
            title = translate('OpenLP.ServiceManager', 'Service File(s) Missing')
            message = translate('OpenLP.ServiceManager',
                'The following file(s) in the service are missing:\n\t%s\n\n'
                'These files will be removed if you continue to save.') % "\n\t".join(missing_list)
            answer = QtGui.QMessageBox.critical(self, title, message,
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel))
            if answer == QtGui.QMessageBox.Cancel:
                self.main_window.finishedProgressBar()
                return False
        # Check if item contains a missing file.
        for item in list(self.service_items):
            self.main_window.incrementProgressBar()
            item[u'service_item'].remove_invalid_frames(missing_list)
            if item[u'service_item'].missing_frames():
                self.service_items.remove(item)
            else:
                service_item = item[u'service_item'].get_service_repr(self._saveLite)
                if service_item[u'header'][u'background_audio']:
                    for i, file_name in enumerate(service_item[u'header'][u'background_audio']):
                        new_file = os.path.join(u'audio', item[u'service_item'].unique_identifier, file_name)
                        audio_files.append((file_name, new_file))
                        service_item[u'header'][u'background_audio'][i] = new_file
                # Add the service item to the service.
                service.append({u'serviceitem': service_item})
        self.repaint_service_list(-1, -1)
        for file_item in write_list:
            file_size = os.path.getsize(file_item)
            total_size += file_size
        log.debug(u'ServiceManager.save_file - ZIP contents size is %i bytes' % total_size)
        service_content = cPickle.dumps(service)
        # Usual Zip file cannot exceed 2GiB, file with Zip64 cannot be
        # extracted using unzip in UNIX.
        allow_zip_64 = (total_size > 2147483648 + len(service_content))
        log.debug(u'ServiceManager.save_file - allowZip64 is %s' % allow_zip_64)
        zip_file = None
        success = True
        self.main_window.incrementProgressBar()
        try:
            zip_file = zipfile.ZipFile(temp_file_name, 'w', zipfile.ZIP_STORED, allow_zip_64)
            # First we add service contents.
            # We save ALL file_names into ZIP using UTF-8.
            zip_file.writestr(service_file_name.encode(u'utf-8'), service_content)
            # Finally add all the listed media files.
            for write_from in write_list:
                zip_file.write(write_from, write_from.encode(u'utf-8'))
            for audio_from, audio_to in audio_files:
                if audio_from.startswith(u'audio'):
                    # When items are saved, they get new unique_identifier. Let's copy the
                    # file to the new location. Unused files can be ignored,
                    # OpenLP automatically cleans up the service manager dir on
                    # exit.
                    audio_from = os.path.join(self.servicePath, audio_from)
                save_file = os.path.join(self.servicePath, audio_to)
                save_path = os.path.split(save_file)[0]
                check_directory_exists(save_path)
                if not os.path.exists(save_file):
                    shutil.copy(audio_from, save_file)
                zip_file.write(audio_from, audio_to.encode(u'utf-8'))
        except IOError:
            log.exception(u'Failed to save service to disk: %s', temp_file_name)
            Receiver.send_message(u'openlp_error_message', {
                u'title': translate(u'OpenLP.ServiceManager', u'Error Saving File'),
                u'message': translate(u'OpenLP.ServiceManager', u'There was an error saving your file.')
            })
            success = False
        finally:
            if zip_file:
                zip_file.close()
        self.main_window.finishedProgressBar()
        self.application.set_normal_cursor()
        if success:
            try:
                shutil.copy(temp_file_name, path_file_name)
            except shutil.Error:
                return self.save_file_as()
            self.main_window.addRecentFile(path_file_name)
            self.set_modified(False)
        delete_file(temp_file_name)
        return success

    def save_local_file(self):
        """
        Save the current service file but leave all the file references alone to point to the current machine.
        This format is not transportable as it will not contain any files.
        """
        if not self.file_name():
            return self.save_file_as()
        temp_file, temp_file_name = mkstemp(u'.oszl', u'openlp_')
        # We don't need the file handle.
        os.close(temp_file)
        log.debug(temp_file_name)
        path_file_name = unicode(self.file_name())
        path, file_name = os.path.split(path_file_name)
        base_name = os.path.splitext(file_name)[0]
        service_file_name = '%s.osd' % base_name
        log.debug(u'ServiceManager.save_file - %s', path_file_name)
        Settings().setValue(self.main_window.serviceManagerSettingsSection + u'/last directory', path)
        service = []
        self.application.set_busy_cursor()
        # Number of items + 1 to zip it
        self.main_window.displayProgressBar(len(self.service_items) + 1)
        for item in self.service_items:
            self.main_window.incrementProgressBar()
            service_item = item[u'service_item'].get_service_repr(self._saveLite)
            #@todo check for file item on save.
            service.append({u'serviceitem': service_item})
            self.main_window.incrementProgressBar()
        service_content = cPickle.dumps(service)
        zip_file = None
        success = True
        self.main_window.incrementProgressBar()
        try:
            zip_file = zipfile.ZipFile(temp_file_name, 'w', zipfile.ZIP_STORED,
                True)
            # First we add service contents.
            zip_file.writestr(service_file_name.encode(u'utf-8'), service_content)
        except IOError:
            log.exception(u'Failed to save service to disk: %s', temp_file_name)
            Receiver.send_message(u'openlp_error_message', {
                u'title': translate(u'OpenLP.ServiceManager', u'Error Saving File'),
                u'message': translate(u'OpenLP.ServiceManager', u'There was an error saving your file.')
            })
            success = False
        finally:
            if zip_file:
                zip_file.close()
        self.main_window.finishedProgressBar()
        self.application.set_normal_cursor()
        if success:
            try:
                shutil.copy(temp_file_name, path_file_name)
            except shutil.Error:
                return self.save_file_as()
            self.main_window.addRecentFile(path_file_name)
            self.set_modified(False)
        delete_file(temp_file_name)
        return success

    def save_file_as(self):
        """
        Get a file name and then call :func:`ServiceManager.save_file` to
        save the file.
        """
        default_service_enabled = Settings().value(u'advanced/default service enabled')
        if default_service_enabled:
            service_day = Settings().value(u'advanced/default service day')
            if service_day == 7:
                local_time = datetime.now()
            else:
                service_hour = Settings().value(u'advanced/default service hour')
                service_minute = Settings().value(u'advanced/default service minute')
                now = datetime.now()
                day_delta = service_day - now.weekday()
                if day_delta < 0:
                    day_delta += 7
                time = now + timedelta(days=day_delta)
                local_time = time.replace(hour=service_hour, minute=service_minute)
            default_pattern = Settings().value(u'advanced/default service name')
            default_file_name = format_time(default_pattern, local_time)
        else:
            default_file_name = u''
        directory = Settings().value(self.main_window.serviceManagerSettingsSection + u'/last directory')
        path = os.path.join(directory, default_file_name)
        # SaveAs from osz to oszl is not valid as the files will be deleted
        # on exit which is not sensible or usable in the long term.
        if self._file_name.endswith(u'oszl') or self.service_has_all_original_files:
            file_name = QtGui.QFileDialog.getSaveFileName(self.main_window, UiStrings().SaveService, path,
                translate('OpenLP.ServiceManager',
                    'OpenLP Service Files (*.osz);; OpenLP Service Files - lite (*.oszl)'))
        else:
            file_name = QtGui.QFileDialog.getSaveFileName(self.main_window, UiStrings().SaveService, path,
                translate('OpenLP.ServiceManager', 'OpenLP Service Files (*.osz);;'))
        if not file_name:
            return False
        if os.path.splitext(file_name)[1] == u'':
            file_name += u'.osz'
        else:
            ext = os.path.splitext(file_name)[1]
            file_name.replace(ext, u'.osz')
        self.set_file_name(file_name)
        self.decide_save_method()

    def decide_save_method(self):
        """
        Determine which type of save method to use.
        """
        if not self.file_name():
            return self.save_file_as()
        if self._saveLite:
            return self.save_local_file()
        else:
            return self.save_file()

    def load_file(self, file_name):
        """
        Load an existing service file
        """
        if not file_name:
            return False
        file_name = unicode(file_name)
        if not os.path.exists(file_name):
            return False
        zip_file = None
        file_to = None
        self.application.set_busy_cursor()
        try:
            zip_file = zipfile.ZipFile(file_name)
            for zip_info in zip_file.infolist():
                try:
                    ucsfile = zip_info.filename.decode(u'utf-8')
                except UnicodeDecodeError:
                    log.exception(u'file_name "%s" is not valid UTF-8' %
                        zip_info.file_name.decode(u'utf-8', u'replace'))
                    critical_error_message_box(message=translate('OpenLP.ServiceManager',
                        'File is not a valid service.\n The content encoding is not UTF-8.'))
                    continue
                osfile = ucsfile.replace(u'/', os.path.sep)
                if not osfile.startswith(u'audio'):
                    osfile = os.path.split(osfile)[1]
                log.debug(u'Extract file: %s', osfile)
                zip_info.filename = osfile
                zip_file.extract(zip_info, self.servicePath)
                if osfile.endswith(u'osd'):
                    p_file = os.path.join(self.servicePath, osfile)
            if 'p_file' in locals():
                file_to = open(p_file, u'r')
                items = cPickle.load(file_to)
                file_to.close()
                self.new_file()
                self.set_file_name(file_name)
                self.main_window.displayProgressBar(len(items))
                for item in items:
                    self.main_window.incrementProgressBar()
                    service_item = ServiceItem()
                    if self._saveLite:
                        service_item.set_from_service(item)
                    else:
                        service_item.set_from_service(item, self.servicePath)
                    service_item.validate_item(self.suffixes)
                    self.load_item_unique_identifier = 0
                    if service_item.is_capable(ItemCapabilities.OnLoadUpdate):
                        Receiver.send_message(u'%s_service_load' % service_item.name.lower(), service_item)
                    # if the item has been processed
                    if service_item.unique_identifier == self.load_item_unique_identifier:
                        service_item.edit_id = int(self.load_item_edit_id)
                        service_item.temporary_edit = self.load_item_temporary
                    self.add_service_item(service_item, repaint=False)
                delete_file(p_file)
                self.main_window.addRecentFile(file_name)
                self.set_modified(False)
                Settings().setValue('servicemanager/last file', file_name)
            else:
                critical_error_message_box(message=translate('OpenLP.ServiceManager', 'File is not a valid service.'))
                log.exception(u'File contains no service data')
        except (IOError, NameError, zipfile.BadZipfile):
            log.exception(u'Problem loading service file %s' % file_name)
            critical_error_message_box(message=translate('OpenLP.ServiceManager',
                'File could not be opened because it is corrupt.'))
        except zipfile.BadZipfile:
            if os.path.getsize(file_name) == 0:
                log.exception(u'Service file is zero sized: %s' % file_name)
                QtGui.QMessageBox.information(self, translate('OpenLP.ServiceManager', 'Empty File'),
                    translate('OpenLP.ServiceManager', 'This service file does not contain any data.'))
            else:
                log.exception(u'Service file is cannot be extracted as zip: '
                    u'%s' % file_name)
                QtGui.QMessageBox.information(self, translate('OpenLP.ServiceManager', 'Corrupt File'),
                    translate('OpenLP.ServiceManager',
                        'This file is either corrupt or it is not an OpenLP 2 service file.'))
            self.application.set_normal_cursor()
            return
        finally:
            if file_to:
                file_to.close()
            if zip_file:
                zip_file.close()
        self.main_window.finishedProgressBar()
        self.application.set_normal_cursor()
        self.repaint_service_list(-1, -1)

    def load_Last_file(self):
        """
        Load the last service item from the service manager when the
        service was last closed. Can be blank if there was no service
        present.
        """
        file_name = Settings().value(u'servicemanager/last file')
        if file_name:
            self.load_file(file_name)

    def context_menu(self, point):
        """
        The Right click context menu from the Serviceitem list
        """
        item = self.service_manager_list.itemAt(point)
        if item is None:
            return
        if item.parent():
            pos = item.parent().data(0, QtCore.Qt.UserRole)
        else:
            pos = item.data(0, QtCore.Qt.UserRole)
        service_item = self.service_items[pos - 1]
        self.edit_action.setVisible(False)
        self.create_custom_action.setVisible(False)
        self.maintain_action.setVisible(False)
        self.notes_action.setVisible(False)
        self.time_action.setVisible(False)
        self.auto_start_action.setVisible(False)
        if service_item[u'service_item'].is_capable(ItemCapabilities.CanEdit) and service_item[u'service_item'].edit_id:
            self.edit_action.setVisible(True)
        if service_item[u'service_item'].is_capable(ItemCapabilities.CanMaintain):
            self.maintain_action.setVisible(True)
        if item.parent() is None:
            self.notes_action.setVisible(True)
        if service_item[u'service_item'].is_capable(ItemCapabilities.CanLoop) and  \
                len(service_item[u'service_item'].get_frames()) > 1:
            self.auto_play_slides_group.menuAction().setVisible(True)
            self.auto_play_slides_once.setChecked(service_item[u'service_item'].auto_play_slides_once)
            self.auto_play_slides_loop.setChecked(service_item[u'service_item'].auto_play_slides_loop)
            self.timed_slide_interval.setChecked(service_item[u'service_item'].timed_slide_interval > 0)
            if service_item[u'service_item'].timed_slide_interval > 0:
                delay_suffix = u' %s s' % unicode(service_item[u'service_item'].timed_slide_interval)
            else:
                delay_suffix = u' ...'
            self.timed_slide_interval.setText(
                translate('OpenLP.ServiceManager', '&Delay between slides') + delay_suffix)
            # TODO for future: make group explains itself more visually
        else:
            self.auto_play_slides_group.menuAction().setVisible(False)
        if service_item[u'service_item'].is_capable(ItemCapabilities.HasVariableStartTime):
            self.time_action.setVisible(True)
        if service_item[u'service_item'].is_capable(ItemCapabilities.CanAutoStartForLive):
            self.auto_start_action.setVisible(True)
            self.auto_start_action.setIcon(self.inactive)
            self.auto_start_action.setText(translate('OpenLP.ServiceManager', '&Auto Start - inactive'))
            if service_item[u'service_item'].will_auto_start:
                self.auto_start_action.setText(translate('OpenLP.ServiceManager', '&Auto Start - active'))
                self.auto_start_action.setIcon(self.active)
        if service_item[u'service_item'].is_text():
            for plugin in self.plugin_manager.plugins:
                if plugin.name == u'custom' and plugin.status == PluginStatus.Active:
                    self.create_custom_action.setVisible(True)
                    break
        self.theme_menu.menuAction().setVisible(False)
        # Set up the theme menu.
        if service_item[u'service_item'].is_text() and self.renderer.theme_level == ThemeLevel.Song:
            self.theme_menu.menuAction().setVisible(True)
            # The service item does not have a theme, check the "Default".
            if service_item[u'service_item'].theme is None:
                theme_action = self.theme_menu.defaultAction()
            else:
                theme_action = self.theme_menu.findChild(QtGui.QAction, service_item[u'service_item'].theme)
            if theme_action is not None:
                theme_action.setChecked(True)
        self.menu.exec_(self.service_manager_list.mapToGlobal(point))

    def on_service_item_note_form(self):
        """
        Allow the service note to be edited
        """
        item = self.find_service_item()[0]
        self.serviceNoteForm.text_edit.setPlainText(self.service_items[item][u'service_item'].notes)
        if self.serviceNoteForm.exec_():
            self.service_items[item][u'service_item'].notes = self.serviceNoteForm.text_edit.toPlainText()
            self.repaint_service_list(item, -1)
            self.set_modified()

    def on_start_time_form(self):
        """
        Opens a dialog to type in service item notes.
        """
        item = self.find_service_item()[0]
        self.startTimeForm.item = self.service_items[item]
        if self.startTimeForm.exec_():
            self.repaint_service_list(item, -1)

    def toggle_auto_play_slides_once(self):
        """
        Toggle Auto play slide once.
        Inverts auto play once option for the item
        """
        item = self.find_service_item()[0]
        service_item = self.service_items[item][u'service_item']
        service_item.auto_play_slides_once = not service_item.auto_play_slides_once
        if service_item.auto_play_slides_once:
            service_item.auto_play_slides_loop = False
            self.auto_play_slides_loop.setChecked(False)
        if service_item.auto_play_slides_once and service_item.timed_slide_interval == 0:
            service_item.timed_slide_interval = Settings().value(
                self.main_window.generalSettingsSection + u'/loop delay')
        self.set_modified()

    def toggle_auto_play_slides_loop(self):
        """
        Toggle Auto play slide loop.
        """
        item = self.find_service_item()[0]
        service_item = self.service_items[item][u'service_item']
        service_item.auto_play_slides_loop = not service_item.auto_play_slides_loop
        if service_item.auto_play_slides_loop:
            service_item.auto_play_slides_once = False
            self.auto_play_slides_once.setChecked(False)
        if service_item.auto_play_slides_loop and service_item.timed_slide_interval == 0:
            service_item.timed_slide_interval = Settings().value(
                self.main_window.generalSettingsSection + u'/loop delay')
        self.set_modified()

    def on_timed_slide_interval(self):
        """
        Shows input dialog for enter interval in seconds for delay
        """
        item = self.find_service_item()[0]
        service_item = self.service_items[item][u'service_item']
        if service_item.timed_slide_interval == 0:
            timed_slide_interval = Settings().value(self.mainwindow.generalSettingsSection + u'/loop delay')
        else:
            timed_slide_interval = service_item.timed_slide_interval
        timed_slide_interval, ok = QtGui.QInputDialog.getInteger(self, translate('OpenLP.ServiceManager',
            'Input delay'), translate('OpenLP.ServiceManager', 'Delay between slides in seconds.'),
            timed_slide_interval, 0, 180, 1)
        if ok:
            service_item.timed_slide_interval = timed_slide_interval
        if service_item.timed_slide_interval != 0 and not service_item.auto_play_slides_loop \
                and not service_item.auto_play_slides_once:
            service_item.auto_play_slides_loop = True
        elif service_item.timed_slide_interval == 0:
            service_item.auto_play_slides_loop = False
            service_item.auto_play_slides_once = False
        self.set_modified()

    def on_auto_start(self):
        """
        Toggles to Auto Start Setting.
        """
        item = self.find_service_item()[0]
        self.service_items[item][u'service_item'].will_auto_start = \
            not self.service_items[item][u'service_item'].will_auto_start

    def on_service_item_edit_form(self):
        """
        Opens a dialog to edit the service item and update the service
        display if changes are saved.
        """
        item = self.find_service_item()[0]
        self.serviceItemEditForm.set_service_item(self.service_items[item][u'service_item'])
        if self.serviceItemEditForm.exec_():
            self.add_service_item(self.serviceItemEditForm.get_service_item(),
                replace=True, expand=self.service_items[item][u'expanded'])

    def preview_live(self, unique_identifier, row):
        """
        Called by the SlideController to request a preview item be made live
        and allows the next preview to be updated if relevant.


        ``unique_identifier``
            Reference to the service_item


        ``row``
            individual row number

        """
        for sitem in self.service_items:
            if sitem[u'service_item'].unique_identifier == unique_identifier:
                item = self.service_manager_list.topLevelItem(sitem[u'order'] - 1)
                self.service_manager_list.setCurrentItem(item)
                self.make_live(int(row))
                return

    def next_item(self):
        """
        Called by the SlideController to select the next service item.
        """
        if not self.service_manager_list.selectedItems():
            return
        selected = self.service_manager_list.selectedItems()[0]
        lookFor = 0
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.service_manager_list)
        while serviceIterator.value():
            if lookFor == 1 and serviceIterator.value().parent() is None:
                self.service_manager_list.setCurrentItem(serviceIterator.value())
                self.make_live()
                return
            if serviceIterator.value() == selected:
                lookFor = 1
            serviceIterator += 1

    def previous_item(self, last_slide=False):
        """
        Called by the SlideController to select the previous service item.

        ``last_slide``
            Is this the last slide in the service_item

        """
        if not self.service_manager_list.selectedItems():
            return
        selected = self.service_manager_list.selectedItems()[0]
        prevItem = None
        prevItemLastSlide = None
        serviceIterator = QtGui.QTreeWidgetItemIterator(self.service_manager_list)
        while serviceIterator.value():
            if serviceIterator.value() == selected:
                if last_slide and prevItemLastSlide:
                    pos = prevItem.data(0, QtCore.Qt.UserRole)
                    check_expanded = self.service_items[pos - 1][u'expanded']
                    self.service_manager_list.setCurrentItem(prevItemLastSlide)
                    if not check_expanded:
                        self.service_manager_list.collapseItem(prevItem)
                    self.make_live()
                    self.service_manager_list.setCurrentItem(prevItem)
                elif prevItem:
                    self.service_manager_list.setCurrentItem(prevItem)
                    self.make_live()
                return
            if serviceIterator.value().parent() is None:
                prevItem = serviceIterator.value()
            if serviceIterator.value().parent() is prevItem:
                prevItemLastSlide = serviceIterator.value()
            serviceIterator += 1

    def on_set_item(self, message):
        """
        Called by a signal to select a specific item.
        """
        self.set_item(int(message))

    def set_item(self, index):
        """
        Makes a specific item in the service live.
        """
        if index >= 0 and index < self.service_manager_list.topLevelItemCount:
            item = self.service_manager_list.topLevelItem(index)
            self.service_manager_list.setCurrentItem(item)
            self.make_live()

    def on_move_selection_up(self):
        """
        Moves the cursor selection up the window.
        Called by the up arrow.
        """
        item = self.service_manager_list.currentItem()
        itemBefore = self.service_manager_list.itemAbove(item)
        if itemBefore is None:
            return
        self.service_manager_list.setCurrentItem(itemBefore)

    def on_move_selection_down(self):
        """
        Moves the cursor selection down the window.
        Called by the down arrow.
        """
        item = self.service_manager_list.currentItem()
        itemAfter = self.service_manager_list.itemBelow(item)
        if itemAfter is None:
            return
        self.service_manager_list.setCurrentItem(itemAfter)

    def onCollapseAll(self):
        """
        Collapse all the service items.
        """
        for item in self.service_items:
            item[u'expanded'] = False
        self.service_manager_list.collapseAll()

    def collapsed(self, item):
        """
        Record if an item is collapsed. Used when repainting the list to get the
        correct state.
        """
        pos = item.data(0, QtCore.Qt.UserRole)
        self.service_items[pos - 1][u'expanded'] = False

    def onExpandAll(self):
        """
        Collapse all the service items.
        """
        for item in self.service_items:
            item[u'expanded'] = True
        self.service_manager_list.expandAll()

    def expanded(self, item):
        """
        Record if an item is collapsed. Used when repainting the list to get the
        correct state.
        """
        pos = item.data(0, QtCore.Qt.UserRole)
        self.service_items[pos - 1][u'expanded'] = True

    def onServiceTop(self):
        """
        Move the current ServiceItem to the top of the list.
        """
        item, child = self.find_service_item()
        if item < len(self.service_items) and item != -1:
            temp = self.service_items[item]
            self.service_items.remove(self.service_items[item])
            self.service_items.insert(0, temp)
            self.repaint_service_list(0, child)
            self.set_modified()

    def onServiceUp(self):
        """
        Move the current ServiceItem one position up in the list.
        """
        item, child = self.find_service_item()
        if item > 0:
            temp = self.service_items[item]
            self.service_items.remove(self.service_items[item])
            self.service_items.insert(item - 1, temp)
            self.repaint_service_list(item - 1, child)
            self.set_modified()

    def onServiceDown(self):
        """
        Move the current ServiceItem one position down in the list.
        """
        item, child = self.find_service_item()
        if item < len(self.service_items) and item != -1:
            temp = self.service_items[item]
            self.service_items.remove(self.service_items[item])
            self.service_items.insert(item + 1, temp)
            self.repaint_service_list(item + 1, child)
            self.set_modified()

    def onServiceEnd(self):
        """
        Move the current ServiceItem to the bottom of the list.
        """
        item, child = self.find_service_item()
        if item < len(self.service_items) and item != -1:
            temp = self.service_items[item]
            self.service_items.remove(self.service_items[item])
            self.service_items.insert(len(self.service_items), temp)
            self.repaint_service_list(len(self.service_items) - 1, child)
            self.set_modified()

    def onDeleteFromService(self):
        """
        Remove the current ServiceItem from the list.
        """
        item = self.find_service_item()[0]
        if item != -1:
            self.service_items.remove(self.service_items[item])
            self.repaint_service_list(item - 1, -1)
            self.set_modified()

    def repaint_service_list(self, serviceItem, serviceItemChild):
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
        self.service_has_all_original_files = True
        for item in self.service_items:
            item[u'order'] = count
            count += 1
            if not item[u'service_item'].has_original_files:
                self.service_has_all_original_files = False
        # Repaint the screen
        self.service_manager_list.clear()
        for item_count, item in enumerate(self.service_items):
            serviceitem = item[u'service_item']
            treewidgetitem = QtGui.QTreeWidgetItem(self.service_manager_list)
            if serviceitem.is_valid:
                if serviceitem.notes:
                    icon = QtGui.QImage(serviceitem.icon)
                    icon = icon.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    overlay = QtGui.QImage(':/services/service_item_notes.png')
                    overlay = overlay.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    painter = QtGui.QPainter(icon)
                    painter.drawImage(0, 0, overlay)
                    painter.end()
                    treewidgetitem.setIcon(0, build_icon(icon))
                elif serviceitem.temporary_edit:
                    icon = QtGui.QImage(serviceitem.icon)
                    icon = icon.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    overlay = QtGui.QImage(':/general/general_export.png')
                    overlay = overlay.scaled(40, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    painter = QtGui.QPainter(icon)
                    painter.drawImage(40, 0, overlay)
                    painter.end()
                    treewidgetitem.setIcon(0, build_icon(icon))
                else:
                    treewidgetitem.setIcon(0, serviceitem.iconic_representation)
            else:
                treewidgetitem.setIcon(0, build_icon(u':/general/general_delete.png'))
            treewidgetitem.setText(0, serviceitem.get_display_title())
            tips = []
            if serviceitem.temporary_edit:
                tips.append(u'<strong>%s:</strong> <em>%s</em>' %
                    (translate('OpenLP.ServiceManager', 'Edit'),
                    (translate('OpenLP.ServiceManager', 'Service copy only'))))
            if serviceitem.theme and serviceitem.theme != -1:
                tips.append(u'<strong>%s:</strong> <em>%s</em>' %
                    (translate('OpenLP.ServiceManager', 'Slide theme'), serviceitem.theme))
            if serviceitem.notes:
                tips.append(u'<strong>%s: </strong> %s' %
                    (translate('OpenLP.ServiceManager', 'Notes'), cgi.escape(serviceitem.notes)))
            if item[u'service_item'].is_capable(ItemCapabilities.HasVariableStartTime):
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
                if serviceItem == item_count:
                    if item[u'expanded'] and serviceItemChild == count:
                        self.service_manager_list.setCurrentItem(child)
                    elif serviceItemChild == -1:
                        self.service_manager_list.setCurrentItem(treewidgetitem)
            treewidgetitem.setExpanded(item[u'expanded'])

    def clean_up(self):
        """
        Empties the servicePath of temporary files on system exit.
        """
        log.debug(u'Cleaning up servicePath')
        for file_name in os.listdir(self.servicePath):
            file_path = os.path.join(self.servicePath, file_name)
            delete_file(file_path)
        if os.path.exists(os.path.join(self.servicePath, u'audio')):
            shutil.rmtree(os.path.join(self.servicePath, u'audio'), True)

    def on_theme_combo_box_selected(self, currentIndex):
        """
        Set the theme for the current service.
        """
        log.debug(u'ontheme_combo_box_selected')
        self.service_theme = self.theme_combo_box.currentText()
        self.renderer.set_service_theme(self.service_theme)
        Settings().setValue(self.main_window.serviceManagerSettingsSection + u'/service theme', self.service_theme)
        self.regenerate_service_Items(True)

    def theme_change(self):
        """
        The theme may have changed in the settings dialog so make
        sure the theme combo box is in the correct state.
        """
        log.debug(u'theme_change')
        visible = self.renderer.theme_level == ThemeLevel.Global
        self.theme_label.setVisible(visible)
        self.theme_combo_box.setVisible(visible)

    def regenerate_service_Items(self, changed=False):
        """
        Rebuild the service list as things have changed and a
        repaint is the easiest way to do this.
        """
        self.application.set_busy_cursor()
        log.debug(u'regenerate_service_Items')
        # force reset of renderer as theme data has changed
        self.service_has_all_original_files = True
        if self.service_items:
            for item in self.service_items:
                item[u'selected'] = False
            serviceIterator = QtGui.QTreeWidgetItemIterator(self.service_manager_list)
            selectedItem = None
            while serviceIterator.value():
                if serviceIterator.value().isSelected():
                    selectedItem = serviceIterator.value()
                serviceIterator += 1
            if selectedItem is not None:
                if selectedItem.parent() is None:
                    pos = selectedItem.data(0, QtCore.Qt.UserRole)
                else:
                    pos = selectedItem.parent().data(0, QtCore.Qt.UserRole)
                self.service_items[pos - 1][u'selected'] = True
            tempServiceItems = self.service_items
            self.service_manager_list.clear()
            self.service_items = []
            self.isNew = True
            for item in tempServiceItems:
                self.add_service_item(item[u'service_item'], False, expand=item[u'expanded'], repaint=False,
                    selected=item[u'selected'])
            # Set to False as items may have changed rendering
            # does not impact the saved song so True may also be valid
            if changed:
                self.set_modified()
            # Repaint it once only at the end
            self.repaint_service_list(-1, -1)
        self.application.set_normal_cursor()

    def service_item_update(self, edit_id, unique_identifier, temporary=False):
        """
        Triggered from plugins to update service items.
        Save the values as they will be used as part of the service load
        """
        self.load_item_unique_identifier = unique_identifier
        self.load_item_edit_id = int(edit_id)
        self.load_item_temporary = str_to_bool(temporary)

    def replace_service_item(self, newItem):
        """
        Using the service item passed replace the one with the same edit id
        if found.
        """
        for item_count, item in enumerate(self.service_items):
            if item[u'service_item'].edit_id == newItem.edit_id and item[u'service_item'].name == newItem.name:
                newItem.render()
                newItem.merge(item[u'service_item'])
                item[u'service_item'] = newItem
                self.repaint_service_list(item_count + 1, 0)
                self.live_controller.replaceServiceManagerItem(newItem)
                self.set_modified()

    def add_service_item(self, item, rebuild=False, expand=None, replace=False, repaint=True, selected=False):
        """
        Add a Service item to the list

        ``item``
            Service Item to be added

        ``expand``
            Override the default expand settings. (Tristate)
        """
        # if not passed set to config value
        if expand is None:
            expand = self.expand_tabs
        item.from_service = True
        if replace:
            sitem, child = self.find_service_item()
            item.merge(self.service_items[sitem][u'service_item'])
            self.service_items[sitem][u'service_item'] = item
            self.repaint_service_list(sitem, child)
            self.live_controller.replaceServiceManagerItem(item)
        else:
            item.render()
            # nothing selected for dnd
            if self.drop_position == 0:
                if isinstance(item, list):
                    for inditem in item:
                        self.service_items.append({u'service_item': inditem,
                            u'order': len(self.service_items) + 1,
                            u'expanded': expand, u'selected': selected})
                else:
                    self.service_items.append({u'service_item': item,
                        u'order': len(self.service_items) + 1,
                        u'expanded': expand, u'selected': selected})
                if repaint:
                    self.repaint_service_list(len(self.service_items) - 1, -1)
            else:
                self.service_items.insert(self.drop_position,
                    {u'service_item': item, u'order': self.drop_position,
                    u'expanded': expand, u'selected': selected})
                self.repaint_service_list(self.drop_position, -1)
            # if rebuilding list make sure live is fixed.
            if rebuild:
                self.live_controller.replaceServiceManagerItem(item)
        self.drop_position = 0
        self.set_modified()

    def make_preview(self):
        """
        Send the current item to the Preview slide controller
        """
        self.application.set_busy_cursor()
        item, child = self.find_service_item()
        if self.service_items[item][u'service_item'].is_valid:
            self.preview_controller.addServiceManagerItem(self.service_items[item][u'service_item'], child)
        else:
            critical_error_message_box(translate('OpenLP.ServiceManager', 'Missing Display Handler'),
                translate('OpenLP.ServiceManager',
                    'Your item cannot be displayed as there is no handler to display it'))
        self.application.set_normal_cursor()

    def get_service_item(self):
        """
        Send the current item to the Preview slide controller
        """
        item = self.find_service_item()[0]
        if item == -1:
            return False
        else:
            return self.service_items[item][u'service_item']

    def on_make_live(self):
        """
        Send the current item to the Live slide controller but triggered
        by a tablewidget click event.
        """
        self.make_live()

    def make_live(self, row=-1):
        """
        Send the current item to the Live slide controller

        ``row``
            Row number to be displayed if from preview.
            -1 is passed if the value is not set
        """
        item, child = self.find_service_item()
        # No items in service
        if item == -1:
            return
        if row != -1:
            child = row
        self.application.set_busy_cursor()
        if self.service_items[item][u'service_item'].is_valid:
            self.live_controller.addServiceManagerItem(self.service_items[item][u'service_item'], child)
            if Settings().value(self.main_window.generalSettingsSection + u'/auto preview'):
                item += 1
                if self.service_items and item < len(self.service_items) and \
                        self.service_items[item][u'service_item'].is_capable(ItemCapabilities.CanPreview):
                    self.preview_controller.addServiceManagerItem(self.service_items[item][u'service_item'], 0)
                    next_item = self.service_manager_list.topLevelItem(item)
                    self.service_manager_list.setCurrentItem(next_item)
                    self.live_controller.previewListWidget.setFocus()
        else:
            critical_error_message_box(translate('OpenLP.ServiceManager', 'Missing Display Handler'),
                translate('OpenLP.ServiceManager',
                    'Your item cannot be displayed as the plugin required to display it is missing or inactive'))
            self.application.set_normal_cursor()

    def remote_edit(self):
        """
        Triggers a remote edit to a plugin to allow item to be edited.
        """
        item = self.find_service_item()[0]
        if self.service_items[item][u'service_item'].is_capable(ItemCapabilities.CanEdit):
            new_item = Registry().get(self.service_items[item][u'service_item'].name). \
                onRemoteEdit(self.service_items[item][u'service_item'].edit_id)
            if new_item:
                self.add_service_item(new_item, replace=True)

    def create_custom(self):
        """
        Saves the current text item as a custom slide
        """
        item = self.find_service_item()[0]
        Receiver.send_message(u'custom_create_from_service', self.service_items[item][u'service_item'])

    def find_service_item(self):
        """
        Finds the first selected ServiceItem in the list and returns the
        position of the serviceitem and its selected child item. For example,
        if the third child item (in the Slidecontroller known as slide) in the
        second service item is selected this will return::

            (1, 2)
        """
        items = self.service_manager_list.selectedItems()
        serviceItem = -1
        serviceItemChild = -1
        for item in items:
            parent_item = item.parent()
            if parent_item is None:
                serviceItem = item.data(0, QtCore.Qt.UserRole)
            else:
                serviceItem = parent_item.data(0, QtCore.Qt.UserRole)
                serviceItemChild = item.data(0, QtCore.Qt.UserRole)
            # Adjust for zero based arrays.
            serviceItem -= 1
            # Only process the first item on the list for this method.
            break
        return serviceItem, serviceItemChild

    def drop_event(self, event):
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
                file_name = url.toLocalFile()
                if file_name.endswith(u'.osz'):
                    self.on_load_service_clicked(file_name)
                elif file_name.endswith(u'.oszl'):
                    # todo correct
                    self.on_load_service_clicked(file_name)
        elif link.hasText():
            plugin = link.text()
            item = self.service_manager_list.itemAt(event.pos())
            # ServiceManager started the drag and drop
            if plugin == u'ServiceManager':
                startpos, child = self.find_service_item()
                # If no items selected
                if startpos == -1:
                    return
                if item is None:
                    endpos = len(self.service_items)
                else:
                    endpos = self._get_parent_item_data(item) - 1
                serviceItem = self.service_items[startpos]
                self.service_items.remove(serviceItem)
                self.service_items.insert(endpos, serviceItem)
                self.repaint_service_list(endpos, child)
                self.set_modified()
            else:
                # we are not over anything so drop
                replace = False
                if item is None:
                    self.drop_position = len(self.service_items)
                else:
                    # we are over something so lets investigate
                    pos = self._get_parent_item_data(item) - 1
                    serviceItem = self.service_items[pos]
                    if (plugin == serviceItem[u'service_item'].name and
                            serviceItem[u'service_item'].is_capable(ItemCapabilities.CanAppend)):
                        action = self.dndMenu.exec_(QtGui.QCursor.pos())
                        # New action required
                        if action == self.newAction:
                            self.drop_position = self._get_parent_item_data(item)
                        # Append to existing action
                        if action == self.addToAction:
                            self.drop_position = self._get_parent_item_data(item)
                            item.setSelected(True)
                            replace = True
                    else:
                        self.drop_position = self._get_parent_item_data(item)
                Receiver.send_message(u'%s_add_service_item' % plugin, replace)

    def update_theme_list(self, theme_list):
        """
        Called from ThemeManager when the Themes have changed

        ``theme_list``
            A list of current themes to be displayed
        """
        self.theme_combo_box.clear()
        self.theme_menu.clear()
        self.theme_combo_box.addItem(u'')
        theme_group = QtGui.QActionGroup(self.theme_menu)
        theme_group.setExclusive(True)
        theme_group.setObjectName(u'theme_group')
        # Create a "Default" theme, which allows the user to reset the item's
        # theme to the service theme or global theme.
        defaultTheme = create_widget_action(self.theme_menu, text=UiStrings().Default, checked=False,
            triggers=self.on_theme_change_action)
        self.theme_menu.setDefaultAction(defaultTheme)
        theme_group.addAction(defaultTheme)
        self.theme_menu.addSeparator()
        for theme in theme_list:
            self.theme_combo_box.addItem(theme)
            theme_group.addAction(create_widget_action(self.theme_menu, theme, text=theme, checked=False,
                triggers=self.on_theme_change_action))
        find_and_set_in_combo_box(self.theme_combo_box, self.service_theme)
        self.renderer.set_service_theme(self.service_theme)
        self.regenerate_service_Items()

    def on_theme_change_action(self):
        """
        Handles theme change events
        """
        theme = self.sender().objectName()
        # No object name means that the "Default" theme is supposed to be used.
        if not theme:
            theme = None
        item = self.find_service_item()[0]
        self.service_items[item][u'service_item'].update_theme(theme)
        self.regenerate_service_Items(True)

    def _get_parent_item_data(self, item):
        """
        Finds and returns the parent item for any item
        """
        parent_item = item.parent()
        if parent_item is None:
            return item.data(0, QtCore.Qt.UserRole)
        else:
            return parent_item.data(0, QtCore.Qt.UserRole)

    def print_service_order(self):
        """
        Print a Service Order Sheet.
        """
        settingDialog = PrintServiceForm()
        settingDialog.exec_()

    def _get_renderer(self):
        """
        Adds the Renderer to the class dynamically
        """
        if not hasattr(self, u'_renderer'):
            self._renderer = Registry().get(u'renderer')
        return self._renderer

    renderer = property(_get_renderer)

    def _get_live_controller(self):
        """
        Adds the live controller to the class dynamically
        """
        if not hasattr(self, u'_live_controller'):
            self._live_controller = Registry().get(u'live_controller')
        return self._live_controller

    live_controller = property(_get_live_controller)

    def _get_preview_controller(self):
        """
        Adds the preview controller to the class dynamically
        """
        if not hasattr(self, u'_preview_controller'):
            self._preview_controller = Registry().get(u'preview_controller')
        return self._preview_controller

    preview_controller = property(_get_preview_controller)

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, u'_plugin_manager'):
            self._plugin_manager = Registry().get(u'plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
