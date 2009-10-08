# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from openlp.core.lib.plugin import PluginStatus
from plugindialog import Ui_PluginViewDialog

class PluginForm(QtGui.QDialog, Ui_PluginViewDialog):
    global log
    log = logging.getLogger(u'PluginForm')

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.activePlugin = None
        self.setupUi(self)
        log.debug(u'Defined')
        self.load()
        self._clearDetails()
        # Right, now let's put some signals and slots together!
        QtCore.QObject.connect(
            self.PluginListWidget,
            QtCore.SIGNAL(u'itemSelectionChanged()'),
            self.onPluginListWidgetSelectionChanged)
        QtCore.QObject.connect(
            self.StatusComboBox,
            QtCore.SIGNAL(u'currentIndexChanged(int)'),
            self.onStatusComboBoxChanged)

    def load(self):
        """
        Load the plugin details into the screen
        """
        self.PluginListWidget.clear()
        for plugin in self.parent.plugin_manager.plugins:
            item = QtGui.QListWidgetItem(self.PluginListWidget)
            item.setText(plugin.name)
            if plugin.icon is not None:
                item.setIcon(plugin.icon)
            self.PluginListWidget.addItem(item)

    def _clearDetails(self):
        self.StatusComboBox.setCurrentIndex(-1)
        self.VersionNumberLabel.setText(u'')
        self.AboutTextBrowser.setHtml(u'')

    def _setDetails(self):
        self.VersionNumberLabel.setText(self.activePlugin.version)
        self.AboutTextBrowser.setHtml(self.activePlugin.about())
        self.StatusComboBox.setCurrentIndex(int(self.activePlugin.status))

    def onPluginListWidgetSelectionChanged(self):
        if self.PluginListWidget.currentItem() is None:
            self._clearDetails()
            return
        plugin_name = self.PluginListWidget.currentItem().text()
        self.activePlugin = None
        for plugin in self.parent.plugin_manager.plugins:
            if plugin.name == plugin_name:
                self.activePlugin = plugin
                break
        if self.activePlugin is not None:
            self._setDetails()
        else:
            self._clearDetails()

    def onStatusComboBoxChanged(self, status):
        self.activePlugin.toggle_status(status)
        if status == PluginStatus.Active:
            self.activePlugin.initialise()
        else:
            self.activePlugin.finalise()

