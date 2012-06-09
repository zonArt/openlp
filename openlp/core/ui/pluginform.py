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

import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import PluginStatus, Receiver, translate
from plugindialog import Ui_PluginViewDialog

log = logging.getLogger(__name__)

class PluginForm(QtGui.QDialog, Ui_PluginViewDialog):
    """
    The plugin form provides user control over the plugins OpenLP uses.
    """
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.activePlugin = None
        self.programaticChange = False
        self.setupUi(self)
        self.load()
        self._clearDetails()
        # Right, now let's put some signals and slots together!
        QtCore.QObject.connect(
            self.pluginListWidget,
            QtCore.SIGNAL(u'itemSelectionChanged()'),
            self.onPluginListWidgetSelectionChanged)
        QtCore.QObject.connect(
            self.statusComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
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
        for plugin in self.parent().pluginManager.plugins:
            item = QtGui.QListWidgetItem(self.pluginListWidget)
            # We do this just to make 100% sure the status is an integer as
            # sometimes when it's loaded from the config, it isn't cast to int.
            plugin.status = int(plugin.status)
            # Set the little status text in brackets next to the plugin name.
            if plugin.status == PluginStatus.Disabled:
                status_text = unicode(
                    translate('OpenLP.PluginForm', '%s (Disabled)'))
            elif plugin.status == PluginStatus.Active:
                status_text = unicode(
                    translate('OpenLP.PluginForm', '%s (Active)'))
            else:
                # PluginStatus.Inactive
                status_text = unicode(
                    translate('OpenLP.PluginForm', '%s (Inactive)'))
            item.setText(status_text % plugin.nameStrings[u'singular'])
            # If the plugin has an icon, set it!
            if plugin.icon:
                item.setIcon(plugin.icon)
            self.pluginListWidget.addItem(item)
            pluginListWidth = max(pluginListWidth, self.fontMetrics().width(
                unicode(translate('OpenLP.PluginForm', '%s (Inactive)')) %
                plugin.nameStrings[u'singular']))
        self.pluginListWidget.setFixedWidth(pluginListWidth +
            self.pluginListWidget.iconSize().width() + 48)

    def _clearDetails(self):
        self.statusComboBox.setCurrentIndex(-1)
        self.versionNumberLabel.setText(u'')
        self.aboutTextBrowser.setHtml(u'')
        self.statusComboBox.setEnabled(False)

    def _setDetails(self):
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
        if self.pluginListWidget.currentItem() is None:
            self._clearDetails()
            return
        plugin_name_singular = \
            self.pluginListWidget.currentItem().text().split(u'(')[0][:-1]
        self.activePlugin = None
        for plugin in self.parent().pluginManager.plugins:
            if plugin.status != PluginStatus.Disabled:
                if plugin.nameStrings[u'singular'] == plugin_name_singular:
                    self.activePlugin = plugin
                    break
        if self.activePlugin:
            self._setDetails()
        else:
            self._clearDetails()

    def onStatusComboBoxChanged(self, status):
        if self.programaticChange or status == PluginStatus.Disabled:
            return
        if status == PluginStatus.Inactive:
            Receiver.send_message(u'cursor_busy')
            self.activePlugin.toggleStatus(PluginStatus.Active)
            Receiver.send_message(u'cursor_normal')
            self.activePlugin.appStartup()
        else:
            self.activePlugin.toggleStatus(PluginStatus.Inactive)
        status_text = unicode(
            translate('OpenLP.PluginForm', '%s (Inactive)'))
        if self.activePlugin.status == PluginStatus.Active:
            status_text = unicode(
                translate('OpenLP.PluginForm', '%s (Active)'))
        elif self.activePlugin.status == PluginStatus.Inactive:
            status_text = unicode(
                translate('OpenLP.PluginForm', '%s (Inactive)'))
        elif self.activePlugin.status == PluginStatus.Disabled:
            status_text = unicode(
                translate('OpenLP.PluginForm', '%s (Disabled)'))
        self.pluginListWidget.currentItem().setText(
            status_text % self.activePlugin.nameStrings[u'singular'])
