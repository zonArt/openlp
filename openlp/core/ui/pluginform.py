# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from openlp.core.lib import translate
from openlp.core.lib.plugin import PluginStatus
from plugindialog import Ui_PluginViewDialog

log = logging.getLogger(__name__)

class PluginForm(QtGui.QDialog, Ui_PluginViewDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.activePlugin = None
        self.programaticChange = False
        self.setupUi(self)
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
            # We do this just to make 100% sure the status is an integer as
            # sometimes when it's loaded from the config, it isn't cast to int.
            plugin.status = int(plugin.status)
            # Set the little status text in brackets next to the plugin name.
            status_text = unicode(translate(u'PluginForm', u'%s (Inactive)'))
            if plugin.status == PluginStatus.Active:
                status_text = unicode(translate(u'PluginForm', u'%s (Active)'))
            elif plugin.status == PluginStatus.Inactive:
                status_text = unicode(translate(u'PluginForm', u'%s (Inactive)'))
            elif plugin.status == PluginStatus.Disabled:
                status_text = unicode(translate(u'PluginForm', u'%s (Disabled)'))
            item.setText(status_text % plugin.name)
            # If the plugin has an icon, set it!
            if plugin.icon:
                item.setIcon(plugin.icon)
            self.PluginListWidget.addItem(item)

    def _clearDetails(self):
        self.StatusComboBox.setCurrentIndex(-1)
        self.VersionNumberLabel.setText(u'')
        self.AboutTextBrowser.setHtml(u'')
        self.StatusComboBox.setEnabled(False)

    def _setDetails(self):
        log.debug('PluginStatus: %s', str(self.activePlugin.status))
        self.VersionNumberLabel.setText(self.activePlugin.version)
        self.AboutTextBrowser.setHtml(self.activePlugin.about())
        self.programaticChange = True
        status = 1
        if self.activePlugin.status == PluginStatus.Active:
            status = 0
        self.StatusComboBox.setCurrentIndex(status)
        self.StatusComboBox.setEnabled(True)
        self.programaticChange = False

    def onPluginListWidgetSelectionChanged(self):
        if self.PluginListWidget.currentItem() is None:
            self._clearDetails()
            return
        plugin_name = self.PluginListWidget.currentItem().text().split(u' ')[0]
        self.activePlugin = None
        for plugin in self.parent.plugin_manager.plugins:
            if plugin.name == plugin_name:
                self.activePlugin = plugin
                break
        if self.activePlugin:
            self._setDetails()
        else:
            self._clearDetails()

    def onStatusComboBoxChanged(self, status):
        if self.programaticChange:
            return
        if status == 0:
            self.activePlugin.toggle_status(PluginStatus.Active)
            self.activePlugin.initialise()
        else:
            self.activePlugin.toggle_status(PluginStatus.Inactive)
            self.activePlugin.finalise()
        status_text = 'Inactive'
        if self.activePlugin.status == PluginStatus.Active:
            status_text = 'Active'
        elif self.activePlugin.status == PluginStatus.Inactive:
            status_text = 'Inactive'
        elif self.activePlugin.status == PluginStatus.Disabled:
            status_text = 'Disabled'
        self.PluginListWidget.currentItem().setText(
            u'%s (%s)' % (self.activePlugin.name, status_text))
