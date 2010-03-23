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

from openlp.core.lib import Plugin, build_icon, PluginStatus
from openlp.plugins.alerts.lib import AlertsManager, DBManager
from openlp.plugins.alerts.forms import AlertsTab, AlertForm, AlertEditForm

log = logging.getLogger(__name__)

class alertsPlugin(Plugin):
    log.info(u'Alerts Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Alerts', u'1.9.1', plugin_helpers)
        self.weight = -3
        self.icon = build_icon(u':/media/media_image.png')
        self.alertsmanager = AlertsManager(self)
        self.manager = DBManager(self.config)
        self.alertForm = AlertForm(self.manager, self)
        self.alertEditForm = AlertEditForm(self.manager, self)
        self.status = PluginStatus.Active

    def get_settings_tab(self):
        self.alertsTab = AlertsTab(self)
        return self.alertsTab

    def add_tools_menu_item(self, tools_menu):
        """
        Give the alerts plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.info(u'add tools menu')
        self.toolsAlertItem = QtGui.QAction(tools_menu)
        AlertIcon = build_icon(u':/tools/tools_alert.png')
        self.toolsAlertItem.setIcon(AlertIcon)
        self.toolsAlertItem.setObjectName(u'toolsAlertItem')
        self.toolsAlertItem.setText(self.trUtf8('&Alert'))
        self.toolsAlertItem.setStatusTip(self.trUtf8('Show an alert message'))
        self.toolsAlertItem.setShortcut(u'F7')
        self.service_manager.parent.ToolsMenu.addAction(self.toolsAlertItem)
        QtCore.QObject.connect(self.toolsAlertItem,
            QtCore.SIGNAL(u'triggered()'), self.onAlertsTrigger)
        self.toolsAlertItem.setVisible(False)

    def initialise(self):
        log.info(u'Alerts Initialising')
        Plugin.initialise(self)
        self.toolsAlertItem.setVisible(True)

    def finalise(self):
        log.info(u'Plugin Finalise')
        self.toolsAlertItem.setVisible(False)
        #stop any events being processed

    def togglealertsState(self):
        self.alertsActive = not self.alertsActive
        self.config.set_config(u'active', self.alertsActive)

    def onAlertsTrigger(self):
        self.alertForm.loadList()
        self.alertForm.exec_()

    def onAlertsEdit(self):
        self.alertEditForm.loadList()
        self.alertEditForm.exec_()

    def about(self):
        about_text = self.trUtf8('<b>Alerts Plugin</b><br>This plugin '
            'controls the displaying of alerts on the presentations screen')
        return about_text
