# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Ken Roberts, Simon Scudder,               #
# Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon Tibble,             #
# Dave Warnock, Frode Woldsund, Martin Zibricky, Patrick Zimmermann           #
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
The :mod: projectormanager` module provides the functions for
    the display/control of Projectors.
"""

import logging
log = logging.getLogger(__name__)
log.debug('projectormanager loaded')

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, QThread, pyqtSlot

from openlp.core.common import RegistryProperties, Settings, OpenLPMixin, \
    RegistryMixin, translate
from openlp.core.lib import OpenLPToolbar
from openlp.core.lib.ui import create_widget_action
from openlp.core.lib.projector.constants import *
from openlp.core.lib.projector.db import ProjectorDB
from openlp.core.lib.projector.pjlink1 import PJLink1
from openlp.core.ui.projector.editform import ProjectorEditForm

# Dict for matching projector status to display icon
STATUS_ICONS = {S_NOT_CONNECTED:  ':/projector/projector_item_disconnect.png',
                S_CONNECTING:  ':/projector/projector_item_connect.png',
                S_CONNECTED:  ':/projector/projector_off.png',
                S_OFF:  ':/projector/projector_off.png',
                S_INITIALIZE:  ':/projector/projector_off.png',
                S_STANDBY:  ':/projector/projector_off.png',
                S_WARMUP:  ':/projector/projector_warmup.png',
                S_ON:  ':/projector/projector_on.png',
                S_COOLDOWN:  ':/projector/projector_cooldown.png',
                E_ERROR:  ':/projector/projector_error.png',
                E_NETWORK:  ':/projector/projector_not_connected_error.png',
                E_AUTHENTICATION:  ':/projector/projector_not_connected_error.png',
                E_UNKNOWN_SOCKET_ERROR: ':/projector/projector_not_connected_error.png',
                E_NOT_CONNECTED: ':/projector/projector_not_connected_error.png'
                }


class Ui_ProjectorManager(object):
    """
    UI part of the Projector Manager
    """
    def setup_ui(self, widget):
        """
        Define the UI
        :param widget: The screen object the dialog is to be attached to.
        """
        log.debug('setup_ui()')
        # Create ProjectorManager box
        self.layout = QtGui.QVBoxLayout(widget)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.layout.setObjectName('layout')
        # Add one selection toolbar
        self.one_toolbar = OpenLPToolbar(widget)
        self.one_toolbar.add_toolbar_action('new_projector',
                                            text=translate('OpenLP.ProjectorManager', 'Add Projector'),
                                            icon=':/projector/projector_new.png',
                                            tooltip=translate('OpenLP.ProjectorManager', 'Add a new projector'),
                                            triggers=self.on_add_projector)
        # Show edit/delete when projector not connected
        self.one_toolbar.add_toolbar_action('edit_projector',
                                            text=translate('OpenLP.ProjectorManager', 'Edit Projector'),
                                            icon=':/general/general_edit.png',
                                            tooltip=translate('OpenLP.ProjectorManager', 'Edit selected projector'),
                                            triggers=self.on_edit_projector)
        self.one_toolbar.add_toolbar_action('delete_projector',
                                            text=translate('OpenLP.ProjectorManager', 'Delete Projector'),
                                            icon=':/general/general_delete.png',
                                            tooltip=translate('OpenLP.ProjectorManager', 'Delete selected projector'),
                                            triggers=self.on_delete_projector)
        # Show source/view when projector connected
        self.one_toolbar.add_toolbar_action('source_projector',
                                            text=translate('OpenLP.ProjectorManager', 'Select Input Source'),
                                            icon=':/projector/projector_hdmi.png',
                                            tooltip=translate('OpenLP.ProjectorManager',
                                                              'Choose input source on selected projector'),
                                            triggers=self.on_select_input)
        self.one_toolbar.add_toolbar_action('view_projector',
                                            text=translate('OpenLP.ProjectorManager', 'View Projector'),
                                            icon=':/system/system_about.png',
                                            tooltip=translate('OpenLP.ProjectorManager',
                                                              'View selected projector information'),
                                            triggers=self.on_status_projector)
        self.one_toolbar.addSeparator()
        self.one_toolbar.add_toolbar_action('connect_projector',
                                            text=translate('OpenLP.ProjectorManager',
                                                           'Connect to selected projector'),
                                            icon=':/projector/projector_connect.png',
                                            tootip=translate('OpenLP.ProjectorManager',
                                                             'Connect to selected projector'),
                                            triggers=self.on_connect_projector)
        self.one_toolbar.add_toolbar_action('disconnect_projector',
                                            text=translate('OpenLP.ProjectorManager',
                                                           'Disconnect from selected projector'),
                                            icon=':/projector/projector_disconnect.png',
                                            tooltip=translate('OpenLP.ProjectorManager',
                                                              'Disconnect from selected projector'),
                                            triggers=self.on_disconnect_projector)
        self.one_toolbar.addSeparator()
        self.one_toolbar.add_toolbar_action('poweron_projector',
                                            text=translate('OpenLP.ProjectorManager',
                                                           'Power on selected projector'),
                                            icon=':/projector/projector_power_on.png',
                                            tooltip=translate('OpenLP.ProjectorManager',
                                                              'Power on selected projector'),
                                            triggers=self.on_poweron_projector)
        self.one_toolbar.add_toolbar_action('poweroff_projector',
                                            text=translate('OpenLP.ProjectorManager', 'Standby selected projector'),
                                            icon=':/projector/projector_power_off.png',
                                            tooltip=translate('OpenLP.ProjectorManager',
                                                              'Put selected projector in standby'),
                                            triggers=self.on_poweroff_projector)
        self.one_toolbar.addSeparator()
        self.one_toolbar.add_toolbar_action('blank_projector',
                                            text=translate('OpenLP.ProjectorManager',
                                                           'Blank selected projector screen'),
                                            icon=':/projector/projector_blank.png',
                                            tooltip=translate('OpenLP.ProjectorManager',
                                                              'Blank selected projector screen'),
                                            triggers=self.on_blank_projector)
        self.one_toolbar.add_toolbar_action('show_projector',
                                            ext=translate('OpenLP.ProjectorManager',
                                                          'Show selected projector screen'),
                                            icon=':/projector/projector_show.png',
                                            tooltip=translate('OpenLP.ProjectorManager',
                                                              'Show selected projector screen'),
                                            triggers=self.on_show_projector)
        self.layout.addWidget(self.one_toolbar)
        self.projector_one_widget = QtGui.QWidgetAction(self.one_toolbar)
        self.projector_one_widget.setObjectName('projector_one_toolbar_widget')
        # Create projector manager list
        self.projector_list_widget = QtGui.QListWidget(widget)
        self.projector_list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.projector_list_widget.setAlternatingRowColors(True)
        self.projector_list_widget.setIconSize(QtCore.QSize(90, 50))
        self.projector_list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.projector_list_widget.setObjectName('projector_list_widget')
        self.layout.addWidget(self.projector_list_widget)
        self.projector_list_widget.customContextMenuRequested.connect(self.context_menu)
        self.projector_list_widget.itemDoubleClicked.connect(self.on_doubleclick_item)
        # Build the context menu
        self.menu = QtGui.QMenu()
        self.status_action = create_widget_action(self.menu,
                                                  text=translate('OpenLP.ProjectorManager',
                                                                 '&View Projector Information'),
                                                  icon=':/system/system_about.png',
                                                  triggers=self.on_status_projector)
        self.edit_action = create_widget_action(self.menu,
                                                text=translate('OpenLP.ProjectorManager',
                                                               '&Edit Projector'),
                                                icon=':/projector/projector_edit.png',
                                                triggers=self.on_edit_projector)
        self.menu.addSeparator()
        self.connect_action = create_widget_action(self.menu,
                                                   text=translate('OpenLP.ProjectorManager',
                                                                  '&Connect Projector'),
                                                   icon=':/projector/projector_connect.png',
                                                   triggers=self.on_connect_projector)
        self.disconnect_action = create_widget_action(self.menu,
                                                      text=translate('OpenLP.ProjectorManager',
                                                                     'D&isconnect Projector'),
                                                      icon=':/projector/projector_disconnect.png',
                                                      triggers=self.on_disconnect_projector)
        self.menu.addSeparator()
        self.poweron_action = create_widget_action(self.menu,
                                                   text=translate('OpenLP.ProjectorManager',
                                                                  'Power &On Projector'),
                                                   icon=':/projector/projector_power_on.png',
                                                   triggers=self.on_poweron_projector)
        self.poweroff_action = create_widget_action(self.menu,
                                                    text=translate('OpenLP.ProjectorManager',
                                                                   'Power O&ff Projector'),
                                                    icon=':/projector/projector_power_off.png',
                                                    triggers=self.on_poweroff_projector)
        self.menu.addSeparator()
        self.select_input_action = create_widget_action(self.menu,
                                                        text=translate('OpenLP.ProjectorManager',
                                                                       'Select &Input'),
                                                        icon=':/projector/projector_connectors.png',
                                                        triggers=self.on_select_input)
        self.blank_action = create_widget_action(self.menu,
                                                 text=translate('OpenLP.ProjectorManager',
                                                                '&Blank Projector Screen'),
                                                 icon=':/projector/projector_blank.png',
                                                 triggers=self.on_blank_projector)
        self.show_action = create_widget_action(self.menu,
                                                text=translate('OpenLP.ProjectorManager',
                                                               '&Show Projector Screen'),
                                                icon=':/projector/projector_show.png',
                                                triggers=self.on_show_projector)
        self.menu.addSeparator()
        self.delete_action = create_widget_action(self.menu,
                                                  text=translate('OpenLP.ProjectorManager',
                                                                 '&Delete Projector'),
                                                  icon=':/general/general_delete.png',
                                                  triggers=self.on_delete_projector)
        self.update_icons()


class ProjectorManager(OpenLPMixin, RegistryMixin, QtGui.QWidget, Ui_ProjectorManager, RegistryProperties):
    """
    Manage the projectors.
    """
    def __init__(self, parent=None, projectordb=None):
        log.debug('__init__()')
        super().__init__(parent)
        self.settings_section = 'projector'
        self.projectordb = projectordb
        self.projector_list = []

    def bootstrap_initialise(self):
        self.setup_ui(self)
        if self.projectordb is None:
            # Work around for testing creating a ~/.openlp.data.projector.projector.sql file
            log.debug('Creating new ProjectorDB() instance')
            self.projectordb = ProjectorDB()
        else:
            log.debug('Using existing ProjectorDB() instance')
        settings = Settings()
        settings.beginGroup(self.settings_section)
        self.autostart = settings.value('connect on start')
        self.poll_time = settings.value('poll time')
        self.socket_timeout = settings.value('socket timeout')
        settings.endGroup()
        del(settings)

    def bootstrap_post_set_up(self):
        self.load_projectors()
        '''
        self.projector_form = ProjectorWizard(self, projectordb=self.projectordb)
        self.projector_form.edit_page.newProjector.connect(self.add_projector_from_wizard)
        self.projector_form.edit_page.editProjector.connect(self.edit_projector_from_wizard)
        '''
        self.projector_form = ProjectorEditForm(self, projectordb=self.projectordb)
        self.projector_form.newProjector.connect(self.add_projector_from_wizard)
        self.projector_form.editProjector.connect(self.edit_projector_from_wizard)

        self.projector_list_widget.itemSelectionChanged.connect(self.update_icons)

    def context_menu(self, point):
        """
        Build the Right Click Context menu and set state.

        :param point: The position of the mouse so the correct item can be found.
        """
        # QListWidgetItem
        item = self.projector_list_widget.itemAt(point)
        if item is None:
            return
        real_projector = item.data(QtCore.Qt.UserRole)
        projector_name = str(item.text())
        visible = real_projector.link.status_connect >= S_CONNECTED
        log.debug('(%s) Building menu - visible = %s' % (projector_name, visible))
        self.delete_action.setVisible(True)
        self.edit_action.setVisible(True)
        self.connect_action.setVisible(not visible)
        self.disconnect_action.setVisible(visible)
        self.status_action.setVisible(visible)
        if visible:
            self.select_input_action.setVisible(real_projector.link.power == S_ON)
            self.poweron_action.setVisible(real_projector.link.power == S_STANDBY)
            self.poweroff_action.setVisible(real_projector.link.power == S_ON)
            self.blank_action.setVisible(real_projector.link.power == S_ON and
                                         not real_projector.link.shutter)
            self.show_action.setVisible(real_projector.link.power == S_ON and
                                        real_projector.link.shutter)
        else:
            self.select_input_action.setVisible(False)
            self.poweron_action.setVisible(False)
            self.poweroff_action.setVisible(False)
            self.blank_action.setVisible(False)
            self.show_action.setVisible(False)
        self.menu.projector = real_projector
        self.menu.exec_(self.projector_list_widget.mapToGlobal(point))

    def _select_input_widget(self, parent, selected, code, text):
        """
        Build the radio button widget for selecting source input menu

        :param parent: parent widget
        :param selected: Selected widget text
        :param code: PJLink code for this widget
        :param text: Text to display
        :returns: radio button widget
        """
        widget = QtGui.QRadioButton(text, parent=parent)
        widget.setChecked(True if code == selected else False)
        widget.button_role = code
        widget.clicked.connect(self._select_input_radio)
        self.radio_buttons.append(widget)
        return widget

    def _select_input_radio(self, opt1=None, opt2=None):
        """
        Returns the currently selected radio button

        :param opt1: Needed by PyQt4
        :param op2: future
        :returns: Selected button role
        """
        for button in self.radio_buttons:
            if button.isChecked():
                self.radio_button_selected = button.button_role
                break
        return

    def on_select_input(self, opt=None):
        """
        Builds menu for 'Select Input' option, then calls the selected projector
        item to change input source.

        :param opt: Needed by PyQt4
        :returns: None
        """
        list_item = self.projector_list_widget.item(self.projector_list_widget.currentRow())
        projector = list_item.data(QtCore.Qt.UserRole)
        layout = QtGui.QVBoxLayout()
        box = QtGui.QDialog(parent=self)
        box.setModal(True)
        title = QtGui.QLabel(translate('OpenLP.ProjectorManager', 'Select the input source below'))
        layout.addWidget(title)
        self.radio_button_selected = None
        self.radio_buttons = []
        source_list = self.projectordb.get_source_list(make=projector.link.manufacturer,
                                                       model=projector.link.model,
                                                       sources=projector.link.source_available
                                                       )
        if source_list is None:
            return
        sort = []
        for item in source_list.keys():
            sort.append(item)
        sort.sort()
        for item in sort:
            button = self._select_input_widget(parent=self,
                                               selected=projector.link.source,
                                               code=item,
                                               text=source_list[item])
            layout.addWidget(button)
        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok |
                                            QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(box.accept)
        button_box.rejected.connect(box.reject)
        layout.addWidget(button_box)
        box.setLayout(layout)
        check = box.exec_()
        if check == 0:
            # Cancel button clicked or window closed - don't set source
            return
        selected = self.radio_button_selected
        projector.link.set_input_source(self.radio_button_selected)
        self.radio_button_selected = None

    def on_add_projector(self, opt=None):
        """
        Calls wizard to add a new projector to the database

        :param opt: Needed by PyQt4
        :returns: None
        """
        self.projector_form.exec_()

    def on_blank_projector(self, opt=None):
        """
        Calls projector thread to send blank screen command

        :param opt: Needed by PyQt4
        :returns: None
        """
        try:
            ip = opt.link.ip
            projector = opt
            projector.link.set_shutter_closed()
        except AttributeError:
            for list_item in self.projector_list_widget.selectedItems():
                if list_item is None:
                    return
                projector = list_item.data(QtCore.Qt.UserRole)
                try:
                    projector.link.set_shutter_closed()
                except:
                    continue

    def on_doubleclick_item(self, item, opt=None):
        projector = item.data(QtCore.Qt.UserRole)
        if projector.link.state() != projector.link.ConnectedState:
            try:
                projector.link.connect_to_host()
            except:
                pass
        return

    def on_connect_projector(self, opt=None):
        """
        Calls projector thread to connect to projector

        :param opt: Needed by PyQt4
        :returns: None
        """
        try:
            ip = opt.link.ip
            projector = opt
            projector.link.connect_to_host()
        except AttributeError:
            for list_item in self.projector_list_widget.selectedItems():
                if list_item is None:
                    return
                projector = list_item.data(QtCore.Qt.UserRole)
                try:
                    projector.link.connect_to_host()
                except:
                    continue

    def on_delete_projector(self, opt=None):
        """
        Deletes a projector from the list and the database

        :param opt: Needed by PyQt4
        :returns: None
        """
        list_item = self.projector_list_widget.item(self.projector_list_widget.currentRow())
        if list_item is None:
            return
        projector = list_item.data(QtCore.Qt.UserRole)
        msg = QtGui.QMessageBox()
        msg.setText('Delete projector (%s) %s?' % (projector.link.ip, projector.link.name))
        msg.setInformativeText('Are you sure you want to delete this projector?')
        msg.setStandardButtons(msg.Cancel | msg.Ok)
        msg.setDefaultButton(msg.Cancel)
        ans = msg.exec_()
        if ans == msg.Cancel:
            return
        try:
            projector.link.projectorNetwork.disconnect(self.update_status)
        except (AttributeError, TypeError):
            pass
        try:
            projector.link.changeStatus.disconnect(self.update_status)
        except (AttributeError, TypeError):
            pass
        try:
            projector.link.authentication_error.disconnect(self.authentication_error)
        except (AttributeError, TypeError):
            pass
        try:
            projector.link.no_authentication_error.disconnect(self.no_authentication_error)
        except (AttributeError, TypeError):
            pass
        try:
            projector.link.projectorUpdateIcons.disconnect(self.update_icons)
        except (AttributeError, TypeError):
            pass
        try:
            projector.timer.stop()
            projector.timer.timeout.disconnect(projector.link.poll_loop)
        except (AttributeError, TypeError):
            pass
        projector.thread.quit()
        new_list = []
        for item in self.projector_list:
            if item.link.dbid == projector.link.dbid:
                continue
            new_list.append(item)
        self.projector_list = new_list
        list_item = self.projector_list_widget.takeItem(self.projector_list_widget.currentRow())
        list_item = None
        deleted = self.projectordb.delete_projector(projector.db_item)
        for item in self.projector_list:
            log.debug('New projector list - item: %s %s' % (item.link.ip, item.link.name))

    def on_disconnect_projector(self, opt=None):
        """
        Calls projector thread to disconnect from projector

        :param opt: Needed by PyQt4
        :returns: None
        """
        try:
            ip = opt.link.ip
            projector = opt
            projector.link.disconnect_from_host()
        except AttributeError:
            for list_item in self.projector_list_widget.selectedItems():
                if list_item is None:
                    return
                projector = list_item.data(QtCore.Qt.UserRole)
                try:
                    projector.link.disconnect_from_host()
                except:
                    continue

    def on_edit_projector(self, opt=None):
        """
        Calls wizard with selected projector to edit information

        :param opt: Needed by PyQt4
        :returns: None
        """
        list_item = self.projector_list_widget.item(self.projector_list_widget.currentRow())
        projector = list_item.data(QtCore.Qt.UserRole)
        if projector is None:
            return
        self.old_projector = projector
        projector.link.disconnect_from_host()
        record = self.projectordb.get_projector_by_ip(projector.link.ip)
        self.projector_form.exec_(record)
        new_record = self.projectordb.get_projector_by_id(record.id)

    def on_poweroff_projector(self, opt=None):
        """
        Calls projector link to send Power Off command

        :param opt: Needed by PyQt4
        :returns: None
        """
        try:
            ip = opt.link.ip
            projector = opt
            projector.link.set_power_off()
        except AttributeError:
            for list_item in self.projector_list_widget.selectedItems():
                if list_item is None:
                    return
                projector = list_item.data(QtCore.Qt.UserRole)
                try:
                    projector.link.set_power_off()
                except:
                    continue

    def on_poweron_projector(self, opt=None):
        """
        Calls projector link to send Power On command

        :param opt: Needed by PyQt4
        :returns: None
        """
        try:
            ip = opt.link.ip
            projector = opt
            projector.link.set_power_on()
        except AttributeError:
            for list_item in self.projector_list_widget.selectedItems():
                if list_item is None:
                    return
                projector = list_item.data(QtCore.Qt.UserRole)
                try:
                    projector.link.set_power_on()
                except:
                    continue

    def on_show_projector(self, opt=None):
        """
        Calls projector thread to send open shutter command

        :param opt: Needed by PyQt4
        :returns: None
        """
        try:
            ip = opt.link.ip
            projector = opt
            projector.link.set_shutter_open()
        except AttributeError:
            for list_item in self.projector_list_widget.selectedItems():
                if list_item is None:
                    return
                projector = list_item.data(QtCore.Qt.UserRole)
                try:
                    projector.link.set_shutter_open()
                except:
                    continue

    def on_status_projector(self, opt=None):
        """
        Builds message box with projector status information

        :param opt: Needed by PyQt4
        :returns: None
        """
        lwi = self.projector_list_widget.item(self.projector_list_widget.currentRow())
        projector = lwi.data(QtCore.Qt.UserRole)
        message = '<b>%s</b>: %s<BR />' % (translate('OpenLP.ProjectorManager', 'Name'),
                                           projector.link.name)
        message = '%s<b>%s</b>: %s<br />' % (message, translate('OpenLP.ProjectorManager', 'IP'),
                                             projector.link.ip)
        message = '%s<b>%s</b>: %s<br />' % (message, translate('OpenLP.ProjectorManager', 'Port'),
                                             projector.link.port)
        message = '%s<b>%s</b>: %s<br />' % (message, translate('OpenLP.ProjectorManager', 'Notes'),
                                             projector.link.notes)
        message = '%s<hr /><br >' % message
        if projector.link.manufacturer is None:
            message = '%s%s' % (message, translate('OpenLP.ProjectorManager',
                                                   'Projector information not available at this time.'))
        else:
            message = '%s<b>%s</b>: %s<BR />' % (message, translate('OpenLP.ProjectorManager', 'Projector Name'),
                                                 projector.link.pjlink_name)
            message = '%s<b>%s</b>: %s<br />' % (message, translate('OpenLP.ProjectorManager', 'Manufacturer'),
                                                 projector.link.manufacturer)
            message = '%s<b>%s</b>: %s<br />' % (message, translate('OpenLP.ProjectorManager', 'Model'),
                                                 projector.link.model)
            message = '%s<b>%s</b>: %s<br /><br />' % (message, translate('OpenLP.ProjectorManager', 'Other info'),
                                                       projector.link.other_info)
            message = '%s<b>%s</b>: %s<br />' % (message, translate('OpenLP.ProjectorManager', 'Power status'),
                                                 ERROR_MSG[projector.link.power])
            message = '%s<b>%s</b>: %s<br />' % (message, translate('OpenLP.ProjectorManager', 'Shutter is'),
                                                 translate('OpenLP.ProjectorManager', 'Closed')
                                                 if projector.link.shutter else translate('OpenLP', 'Open'))
            message = '%s<b>%s</b>: %s<br />' % (message,
                                                 translate('OpenLP.ProjectorManager', 'Current source input is'),
                                                 projector.link.source)
            count = 1
            for item in projector.link.lamp:
                message = '%s <b>%s %s</b> (%s) %s: %s<br />' % (message,
                                                                 translate('OpenLP.ProjectorManager', 'Lamp'),
                                                                 count,
                                                                 translate('OpenLP.ProjectorManager', 'On')
                                                                 if item['On']
                                                                 else translate('OpenLP.ProjectorManager', 'Off'),
                                                                 translate('OpenLP.ProjectorManager', 'Hours'),
                                                                 item['Hours'])
                count = count + 1
            message = '%s<hr /><br />' % message
            if projector.link.projector_errors is None:
                message = '%s%s' % (message, translate('OpenLP.ProjectorManager', 'No current errors or warnings'))
            else:
                message = '%s<b>%s</b>' % (message, translate('OpenLP.ProjectorManager', 'Current errors/warnings'))
                for (key, val) in projector.link.projector_errors.items():
                    message = '%s<b>%s</b>: %s<br />' % (message, key, ERROR_MSG[val])
        QtGui.QMessageBox.information(self, translate('OpenLP.ProjectorManager', 'Projector Information'), message)

    def _add_projector(self, projector):
        """
        Helper app to build a projector instance

        :param p: Dict of projector database information
        :returns: PJLink() instance
        """
        log.debug('_add_projector()')
        return PJLink1(dbid=projector.id,
                       ip=projector.ip,
                       port=int(projector.port),
                       name=projector.name,
                       location=projector.location,
                       notes=projector.notes,
                       pin=None if projector.pin == '' else projector.pin,
                       poll_time=self.poll_time,
                       socket_timeout=self.socket_timeout
                       )

    def add_projector(self, opt1, opt2=None):
        """
        Builds manager list item, projector thread, and timer for projector instance.

        If called by add projector wizard:
            opt1 = wizard instance
            opt2 = item
        Otherwise:
            opt1 = item
            opt2 = None

        We are not concerned with the wizard instance,
        just the projector item

        :param opt1: See docstring
        :param opt2: See docstring
        :returns: None
        """
        if opt1 is None:
            return
        if opt2 is None:
            projector = opt1
        else:
            projector = opt2
        item = ProjectorItem(link=self._add_projector(projector))
        item.db_item = projector
        icon = QtGui.QIcon(QtGui.QPixmap(STATUS_ICONS[S_NOT_CONNECTED]))
        item.icon = icon
        widget = QtGui.QListWidgetItem(icon,
                                       item.link.name,
                                       self.projector_list_widget
                                       )
        widget.setData(QtCore.Qt.UserRole, item)
        item.widget = widget
        thread = QThread(parent=self)
        thread.my_parent = self
        item.moveToThread(thread)
        thread.started.connect(item.link.thread_started)
        thread.finished.connect(item.link.thread_stopped)
        thread.finished.connect(thread.deleteLater)
        item.link.projectorNetwork.connect(self.update_status)
        item.link.changeStatus.connect(self.update_status)
        item.link.projectorAuthentication.connect(self.authentication_error)
        item.link.projectorNoAuthentication.connect(self.no_authentication_error)
        item.link.projectorUpdateIcons.connect(self.update_icons)
        timer = QtCore.QTimer(self)
        timer.setInterval(self.poll_time)
        timer.timeout.connect(item.link.poll_loop)
        item.timer = timer
        thread.start()
        item.thread = thread
        item.link.timer = timer
        item.link.widget = item.widget
        self.projector_list.append(item)
        if self.autostart:
            item.link.connect_to_host()
        for i in self.projector_list:
            log.debug('New projector list - item: (%s) %s' % (i.link.ip, i.link.name))

    @pyqtSlot(str)
    def add_projector_from_wizard(self, ip, opts=None):
        """
        Add a projector from the wizard

        :param ip: IP address of new record item
        :param opts: Needed by PyQt4
        :returns: None
        """
        log.debug('load_projector(ip=%s)' % ip)
        item = self.projectordb.get_projector_by_ip(ip)
        self.add_projector(item)

    @pyqtSlot(object)
    def edit_projector_from_wizard(self, projector, opts=None):
        """
        Update projector from the wizard edit page

        :param projector: Projector() instance of projector with updated information
        :param opts: Needed by PyQt4
        :returns: None
        """

        self.old_projector.link.name = projector.name
        self.old_projector.link.ip = projector.ip
        self.old_projector.link.pin = None if projector.pin == '' else projector.pin
        self.old_projector.link.port = projector.port
        self.old_projector.link.location = projector.location
        self.old_projector.link.notes = projector.notes
        self.old_projector.widget.setText(projector.name)

    def load_projectors(self):
        """'
        Load projectors - only call when initializing
        """
        log.debug('load_projectors()')
        self.projector_list_widget.clear()
        for item in self.projectordb.get_projector_all():
            self.add_projector(item)

    def get_projector_list(self):
        """
        Return the list of active projectors

        :returns: list
        """
        return self.projector_list

    @pyqtSlot(str, int, str)
    def update_status(self, ip, status=None, msg=None):
        """
        Update the status information/icon for selected list item

        :param ip: IP address of projector
        :param status: Optional status code
        :param msg: Optional status message
        :returns: None
        """
        if status is None:
            return
        item = None
        for list_item in self.projector_list:
            if ip == list_item.link.ip:
                item = list_item
                break
        message = translate('OpenLP.ProjectorManager', 'No message') if msg is None else msg
        if status in STATUS_STRING:
            status_code = STATUS_STRING[status]
            message = ERROR_MSG[status] if msg is None else msg
        elif status in ERROR_STRING:
            status_code = ERROR_STRING[status]
            message = ERROR_MSG[status] if msg is None else msg
        else:
            status_code = status
            message = ERROR_MSG[status] if msg is None else msg
        log.debug('(%s) updateStatus(status=%s) message: "%s"' % (item.link.name, status_code, message))
        if status in STATUS_ICONS:
            if item.status == status:
                return
            item.status = status
            item.icon = QtGui.QIcon(QtGui.QPixmap(STATUS_ICONS[status]))
            if status in ERROR_STRING:
                status_code = ERROR_STRING[status]
            elif status in STATUS_STRING:
                status_code = STATUS_STRING[status]
            log.debug('(%s) Updating icon with %s' % (item.link.name, status_code))
            item.widget.setIcon(item.icon)
            self.update_icons()

    def get_toolbar_item(self, name, enabled=False, hidden=False):
        item = self.one_toolbar.findChild(QtGui.QAction, name)
        if item == 0:
            log.debug('No item found with name "%s"' % name)
        else:
            log.debug('item "%s" updating enabled=%s hidden=%s' % (name, enabled, hidden))
        item.setVisible(False if hidden else True)
        item.setEnabled(True if enabled else False)

    @pyqtSlot()
    def update_icons(self):
        """
        Update the icons when the selected projectors change
        """
        count = len(self.projector_list_widget.selectedItems())
        projector = None
        if count == 0:
            self.get_toolbar_item('edit_projector')
            self.get_toolbar_item('delete_projector')
            self.get_toolbar_item('view_projector', hidden=True)
            self.get_toolbar_item('source_projector', hidden=True)
            self.get_toolbar_item('connect_projector')
            self.get_toolbar_item('disconnect_projector')
            self.get_toolbar_item('poweron_projector')
            self.get_toolbar_item('poweroff_projector')
            self.get_toolbar_item('blank_projector')
            self.get_toolbar_item('show_projector')
        elif count == 1:
            projector = self.projector_list_widget.selectedItems()[0].data(QtCore.Qt.UserRole)
            connected = projector.link.state() == projector.link.ConnectedState
            power = projector.link.power == S_ON
            if connected:
                self.get_toolbar_item('view_projector', enabled=True)
                self.get_toolbar_item('source_projector',
                                      enabled=connected and power and projector.link.source_available is not None)
                self.get_toolbar_item('edit_projector', hidden=True)
                self.get_toolbar_item('delete_projector', hidden=True)
            else:
                self.get_toolbar_item('view_projector', hidden=True)
                self.get_toolbar_item('source_projector', hidden=True)
                self.get_toolbar_item('edit_projector', enabled=True)
                self.get_toolbar_item('delete_projector', enabled=True)
            self.get_toolbar_item('connect_projector', enabled=not connected)
            self.get_toolbar_item('disconnect_projector', enabled=connected)
            self.get_toolbar_item('poweron_projector', enabled=connected and (projector.link.power == S_STANDBY))
            self.get_toolbar_item('poweroff_projector', enabled=connected and (projector.link.power == S_ON))
            if projector.link.shutter is not None:
                self.get_toolbar_item('blank_projector', enabled=(connected and power and not projector.link.shutter))
                self.get_toolbar_item('show_projector', enabled=(connected and power and projector.link.shutter))
            else:
                self.get_toolbar_item('blank_projector', enabled=False)
                self.get_toolbar_item('show_projector', enabled=False)
        else:
            self.get_toolbar_item('edit_projector', enabled=False)
            self.get_toolbar_item('delete_projector', enabled=False)
            self.get_toolbar_item('view_projector', hidden=True)
            self.get_toolbar_item('source_projector', hidden=True)
            self.get_toolbar_item('connect_projector', enabled=True)
            self.get_toolbar_item('disconnect_projector', enabled=True)
            self.get_toolbar_item('poweron_projector', enabled=True)
            self.get_toolbar_item('poweroff_projector', enabled=True)
            self.get_toolbar_item('blank_projector', enabled=True)
            self.get_toolbar_item('show_projector', enabled=True)

    @pyqtSlot(str)
    def authentication_error(self, name):
        QtGui.QMessageBox.warning(self, translate('OpenLP.ProjectorManager',
                                                  '"%s" Authentication Error' % name),
                                  '<br />There was an authentictaion error while trying to connect.'
                                  '<br /><br />Please verify your PIN setting '
                                  'for projector item "%s"' % name)

    @pyqtSlot(str)
    def no_authentication_error(self, name):
        QtGui.QMessageBox.warning(self, translate('OpenLP.ProjectorManager',
                                                  '"%s" No Authentication Error' % name),
                                  '<br />PIN is set and projector does not require authentication.'
                                  '<br /><br />Please verify your PIN setting '
                                  'for projector item "%s"' % name)


class ProjectorItem(QObject):
    """
    Class for the projector list widget item.
    NOTE: Actual PJLink class instance should be saved as self.link
    """
    def __init__(self, link=None):
        self.link = link
        self.thread = None
        self.icon = None
        self.widget = None
        self.my_parent = None
        self.timer = None
        self.projectordb_item = None
        self.poll_time = None
        self.socket_timeout = None
        self.status = S_NOT_CONNECTED
        super(ProjectorItem, self).__init__()


def not_implemented(function):
    """
    Temporary function to build an information message box indicating function not implemented yet

    :param func: Function name
    :returns: None
    """
    QtGui.QMessageBox.information(None,
                                  translate('OpenLP.ProjectorManager', 'Not Implemented Yet'),
                                  translate('OpenLP.ProjectorManager',
                                            'Function "%s"<br />has not been implemented yet.'
                                            '<br />Please check back again later.' % function))
