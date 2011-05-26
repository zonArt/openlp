# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Millar, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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

from openlp.core.lib import Plugin, StringContent, build_icon, translate
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import icon_action, UiStrings
from openlp.core.utils.actions import ActionList
from openlp.plugins.alerts.lib import AlertsManager, AlertsTab
from openlp.plugins.alerts.lib.db import init_schema
from openlp.plugins.alerts.forms import AlertForm

log = logging.getLogger(__name__)

class AlertsPlugin(Plugin):
    log.info(u'Alerts Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Alerts', plugin_helpers,
            settings_tab_class=AlertsTab)
        self.weight = -3
        self.icon_path = u':/plugins/plugin_alerts.png'
        self.icon = build_icon(self.icon_path)
        self.alertsmanager = AlertsManager(self)
        self.manager = Manager(u'alerts', init_schema)
        self.alertForm = AlertForm(self)

    def addToolsMenuItem(self, tools_menu):
        """
        Give the alerts plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.info(u'add tools menu')
        self.toolsAlertItem = icon_action(tools_menu, u'toolsAlertItem',
            u':/plugins/plugin_alerts.png')
        self.toolsAlertItem.setText(translate('AlertsPlugin', '&Alert'))
        self.toolsAlertItem.setStatusTip(
            translate('AlertsPlugin', 'Show an alert message.'))
        self.toolsAlertItem.setShortcut(u'F7')
        self.serviceManager.mainwindow.toolsMenu.addAction(self.toolsAlertItem)
        QtCore.QObject.connect(self.toolsAlertItem,
            QtCore.SIGNAL(u'triggered()'), self.onAlertsTrigger)
        self.toolsAlertItem.setVisible(False)

    def initialise(self):
        log.info(u'Alerts Initialising')
        Plugin.initialise(self)
        self.toolsAlertItem.setVisible(True)
        action_list = ActionList.get_instance()
        action_list.add_action(self.toolsAlertItem, UiStrings().Tools)
        self.liveController.alertTab = self.settings_tab

    def finalise(self):
        """
        Tidy up on exit
        """
        log.info(u'Alerts Finalising')
        self.manager.finalise()
        Plugin.finalise(self)
        self.toolsAlertItem.setVisible(False)
        action_list = ActionList.get_instance()
        action_list.remove_action(self.toolsAlertItem, u'Tools')

    def toggleAlertsState(self):
        self.alertsActive = not self.alertsActive
        QtCore.QSettings().setValue(self.settingsSection + u'/active',
            QtCore.QVariant(self.alertsActive))

    def onAlertsTrigger(self):
        self.alertForm.loadList()
        self.alertForm.exec_()

    def about(self):
        about_text = translate('AlertsPlugin', '<strong>Alerts Plugin</strong>'
            '<br />The alert plugin controls the displaying of nursery alerts '
            'on the display screen')
        return about_text

    def setPluginTextStrings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.textStrings[StringContent.Name] = {
            u'singular': translate('AlertsPlugin', 'Alert', 'name singular'),
            u'plural': translate('AlertsPlugin', 'Alerts', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.textStrings[StringContent.VisibleName] = {
            u'title': translate('AlertsPlugin', 'Alerts', 'container title')
        }

