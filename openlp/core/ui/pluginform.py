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
The actual plugin view form
"""
import logging
import os

from PyQt4 import QtGui

from openlp.core.common import translate
from openlp.core.lib import PluginStatus, Registry
from .plugindialog import Ui_PluginViewDialog

log = logging.getLogger(__name__)


class PluginForm(QtGui.QDialog, Ui_PluginViewDialog):
    """
    The plugin form provides user control over the plugins OpenLP uses.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        super(PluginForm, self).__init__(parent)
        self.active_plugin = None
        self.programatic_change = False
        self.setupUi(self)
        self.load()
        self._clear_details()
        # Right, now let's put some signals and slots together!
        self.pluginListWidget.itemSelectionChanged.connect(self.on_plugin_list_widget_selection_changed)
        self.statusComboBox.currentIndexChanged.connect(self.on_status_combo_box_changed)

    def load(self):
        """
        Load the plugin details into the screen
        """
        self.pluginListWidget.clear()
        self.programatic_change = True
        self._clear_details()
        self.programatic_change = True
        plugin_list_width = 0
        for plugin in self.plugin_manager.plugins:
            item = QtGui.QListWidgetItem(self.pluginListWidget)
            # We do this just to make 100% sure the status is an integer as
            # sometimes when it's loaded from the config, it isn't cast to int.
            plugin.status = int(plugin.status)
            # Set the little status text in brackets next to the plugin name.
            if plugin.status == PluginStatus.Disabled:
                status_text = translate('OpenLP.PluginForm', '%s (Disabled)')
            elif plugin.status == PluginStatus.Active:
                status_text = translate('OpenLP.PluginForm', '%s (Active)')
            else:
                # PluginStatus.Inactive
                status_text = translate('OpenLP.PluginForm', '%s (Inactive)')
            item.setText(status_text % plugin.name_strings['singular'])
            # If the plugin has an icon, set it!
            if plugin.icon:
                item.setIcon(plugin.icon)
            self.pluginListWidget.addItem(item)
            plugin_list_width = max(plugin_list_width, self.fontMetrics().width(
                translate('OpenLP.PluginForm', '%s (Inactive)') % plugin.name_strings['singular']))
        self.pluginListWidget.setFixedWidth(plugin_list_width + self.pluginListWidget.iconSize().width() + 48)

    def _clear_details(self):
        """
        Clear the plugin details widgets
        """
        self.statusComboBox.setCurrentIndex(-1)
        self.versionNumberLabel.setText('')
        self.aboutTextBrowser.setHtml('')
        self.statusComboBox.setEnabled(False)

    def _set_details(self):
        """
        Set the details of the currently selected plugin
        """
        log.debug('PluginStatus: %s', str(self.active_plugin.status))
        self.versionNumberLabel.setText(self.active_plugin.version)
        self.aboutTextBrowser.setHtml(self.active_plugin.about())
        self.programatic_change = True
        status = PluginStatus.Active
        if self.active_plugin.status == PluginStatus.Active:
            status = PluginStatus.Inactive
        self.statusComboBox.setCurrentIndex(status)
        self.statusComboBox.setEnabled(True)
        self.programatic_change = False

    def on_plugin_list_widget_selection_changed(self):
        """
        If the selected plugin changes, update the form
        """
        if self.pluginListWidget.currentItem() is None:
            self._clear_details()
            return
        plugin_name_singular = self.pluginListWidget.currentItem().text().split('(')[0][:-1]
        self.active_plugin = None
        for plugin in self.plugin_manager.plugins:
            if plugin.status != PluginStatus.Disabled:
                if plugin.name_strings['singular'] == plugin_name_singular:
                    self.active_plugin = plugin
                    break
        if self.active_plugin:
            self._set_details()
        else:
            self._clear_details()

    def on_status_combo_box_changed(self, status):
        """
        If the status of a plugin is altered, apply the change
        """
        if self.programatic_change or status == PluginStatus.Disabled:
            return
        if status == PluginStatus.Inactive:
            self.application.set_busy_cursor()
            self.active_plugin.toggle_status(PluginStatus.Active)
            self.application.set_normal_cursor()
            self.active_plugin.app_startup()
        else:
            self.active_plugin.toggle_status(PluginStatus.Inactive)
        status_text = translate('OpenLP.PluginForm', '%s (Inactive)')
        if self.active_plugin.status == PluginStatus.Active:
            status_text = translate('OpenLP.PluginForm', '%s (Active)')
        elif self.active_plugin.status == PluginStatus.Inactive:
            status_text = translate('OpenLP.PluginForm', '%s (Inactive)')
        elif self.active_plugin.status == PluginStatus.Disabled:
            status_text = translate('OpenLP.PluginForm', '%s (Disabled)')
        self.pluginListWidget.currentItem().setText(
            status_text % self.active_plugin.name_strings['singular'])

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, '_plugin_manager'):
            self._plugin_manager = Registry().get('plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically.
        Windows needs to access the application in a dynamic manner.
        """
        if os.name == 'nt':
            return Registry().get('application')
        else:
            if not hasattr(self, '_application'):
                self._application = Registry().get('application')
            return self._application

    application = property(_get_application)
