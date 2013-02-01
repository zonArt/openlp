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

from openlp.core.lib import OpenLPToolbar, translate, UiStrings, Receiver, build_icon, Settings
from openlp.core.lib.ui import create_widget_action
from openlp.core.utils.actions import ActionList, CategoryOrder
from openlp.core.utils import AppLocation

from PyQt4 import QtCore, QtGui

class ServiceManagerList(QtGui.QTreeWidget):
    """
    Set up key bindings and mouse behaviour for the service list
    """
    def __init__(self, serviceManager, parent=None):
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
    def setup_ui(self,widget):
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
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'servicemanager_preview_live'),
            self.preview_live)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'servicemanager_next_item'), self.next_item)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'servicemanager_previous_item'),
            self.previous_item)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'servicemanager_set_item'), self.on_set_item)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_updated'), self.config_updated)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'config_screen_changed'),
            self.regenerate_service_Items)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'theme_update_global'), self.theme_change)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'service_item_update'),
            self.service_item_update)
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