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
The actual plugin view form
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import PluginStatus, Registry, translate
from plugindialog import Ui_PluginViewDialog

log = logging.getLogger(__name__)


class PluginForm(QtGui.QDialog, Ui_PluginViewDialog):
    """
    The plugin form provides user control over the plugins OpenLP uses.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.activePlugin = None
        self.programaticChange = False
        self.setupUi(self)
        self.load()
        self._clearDetails()
        # Right, now let's put some signals and slots together!
        QtCore.QObject.connect(self.pluginListWidget, QtCore.SIGNAL(u'itemSelectionChanged()'),
            self.onPluginListWidgetSelectionChanged)
        QtCore.QObject.connect(self.statusComboBox, QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onStatusComboBoxChanged)

    def load(self):
        """
        Load the plugin details into the screen
        """
        self.pluginListWidget.clear()
        self.programaticChange = True
        self._clearDetails()
        self.programaticChange = True
        pluginListWidth = 0
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
            item.setText(status_text % plugin.nameStrings[u'singular'])
            # If the plugin has an icon, set it!
            if plugin.icon:
                item.setIcon(plugin.icon)
            self.pluginListWidget.addItem(item)
            pluginListWidth = max(pluginListWidth, self.fontMetrics().width(
                translate('OpenLP.PluginForm', '%s (Inactive)') % plugin.nameStrings[u'singular']))
        self.pluginListWidget.setFixedWidth(pluginListWidth + self.pluginListWidget.iconSize().width() + 48)

    def _clearDetails(self):
        """
        Clear the plugin details widgets
        """
        self.statusComboBox.setCurrentIndex(-1)
        self.versionNumberLabel.setText(u'')
        self.aboutTextBrowser.setHtml(u'')
        self.statusComboBox.setEnabled(False)

    def _setDetails(self):
        """
        Set the details of the currently selected plugin
        """
        log.debug(u'PluginStatus: %s', str(self.activePlugin.status))
        self.versionNumberLabel.setText(self.activePlugin.version)
        self.aboutTextBrowser.setHtml(self.activePlugin.about())
        self.programaticChange = True
        status = PluginStatus.Active
        if self.activePlugin.status == PluginStatus.Active:
            status = PluginStatus.Inactive
        self.statusComboBox.setCurrentIndex(status)
        self.statusComboBox.setEnabled(True)
        self.programaticChange = False

    def onPluginListWidgetSelectionChanged(self):
        """
        If the selected plugin changes, update the form
        """
        if self.pluginListWidget.currentItem() is None:
            self._clearDetails()
            return
        plugin_name_singular = self.pluginListWidget.currentItem().text().split(u'(')[0][:-1]
        self.activePlugin = None
        for plugin in self.plugin_manager.plugins:
            if plugin.status != PluginStatus.Disabled:
                if plugin.nameStrings[u'singular'] == plugin_name_singular:
                    self.activePlugin = plugin
                    break
        if self.activePlugin:
            self._setDetails()
        else:
            self._clearDetails()

    def onStatusComboBoxChanged(self, status):
        """
        If the status of a plugin is altered, apply the change
        """
        if self.programaticChange or status == PluginStatus.Disabled:
            return
        if status == PluginStatus.Inactive:
            self.application.set_busy_cursor()
            self.activePlugin.toggleStatus(PluginStatus.Active)
            self.application.set_normal_cursor()
            self.activePlugin.app_startup()
        else:
            self.activePlugin.toggleStatus(PluginStatus.Inactive)
        status_text = translate('OpenLP.PluginForm', '%s (Inactive)')
        if self.activePlugin.status == PluginStatus.Active:
            status_text = translate('OpenLP.PluginForm', '%s (Active)')
        elif self.activePlugin.status == PluginStatus.Inactive:
            status_text = translate('OpenLP.PluginForm', '%s (Inactive)')
        elif self.activePlugin.status == PluginStatus.Disabled:
            status_text = translate('OpenLP.PluginForm', '%s (Disabled)')
        self.pluginListWidget.currentItem().setText(
            status_text % self.activePlugin.nameStrings[u'singular'])

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, u'_plugin_manager'):
            self._plugin_manager = Registry().get(u'plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)

    def _get_application(self):
        """
        Adds the openlp to the class dynamically
        """
        if not hasattr(self, u'_application'):
            self._application = Registry().get(u'application')
        return self._application

    application = property(_get_application)
