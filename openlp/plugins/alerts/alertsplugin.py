# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.lib import Plugin, build_icon, translate
from openlp.core.lib.db import Manager
from openlp.plugins.alerts.lib import AlertsManager, AlertsTab
from openlp.plugins.alerts.lib.db import init_schema
from openlp.plugins.alerts.forms import AlertForm

log = logging.getLogger(__name__)

class AlertsPlugin(Plugin):
    log.info(u'Alerts Plugin loaded')

    def __init__(self, plugin_helpers):
        self.set_plugin_translations()
        Plugin.__init__(self, u'Alerts', u'1.9.2', plugin_helpers)
        self.weight = -3
        self.icon = build_icon(u':/plugins/plugin_alerts.png')
        self.alertsmanager = AlertsManager(self)
        self.manager = Manager(u'alerts', init_schema)
        self.alertForm = AlertForm(self)

    def getSettingsTab(self):
        """
        Return the settings tab for the Alerts plugin
        """
        self.alertsTab = AlertsTab(self)
        return self.alertsTab

    def addToolsMenuItem(self, tools_menu):
        """
        Give the alerts plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.info(u'add tools menu')
        self.toolsAlertItem = QtGui.QAction(tools_menu)
        self.toolsAlertItem.setIcon(build_icon(u':/plugins/plugin_alerts.png'))
        self.toolsAlertItem.setObjectName(u'toolsAlertItem')
        self.toolsAlertItem.setText(translate('AlertsPlugin', '&Alert'))
        self.toolsAlertItem.setStatusTip(
            translate('AlertsPlugin', 'Show an alert message.'))
        self.toolsAlertItem.setShortcut(u'F7')
        self.serviceManager.parent.ToolsMenu.addAction(self.toolsAlertItem)
        QtCore.QObject.connect(self.toolsAlertItem,
            QtCore.SIGNAL(u'triggered()'), self.onAlertsTrigger)
        self.toolsAlertItem.setVisible(False)

    def initialise(self):
        log.info(u'Alerts Initialising')
        Plugin.initialise(self)
        self.toolsAlertItem.setVisible(True)
        self.liveController.alertTab = self.alertsTab

    def finalise(self):
        log.info(u'Alerts Finalising')
        Plugin.finalise(self)
        self.toolsAlertItem.setVisible(False)

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
    def set_plugin_translations(self):
        """
        Called to define all translatable texts of the plugin
        """
        self.name = u'Alerts'
        self.name_lower = u'alerts'
        self.text = {}
        # for context menu
#        elf.text['context_edit'] = translate('AlertsPlugin', '&Edit Song')
#        elf.text['context_delete'] = translate('AlertsPlugin', '&Delete Song')
#        elf.text['context_preview'] = translate('AlertsPlugin', '&Preview Song')
#        elf.text['context_live'] = translate('AlertsPlugin', '&Show Live')
#        # forHeaders in mediamanagerdock
#        elf.text['import'] = translate('AlertsPlugin', 'Import a Song')
#        elf.text['file'] = translate('AlertsPlugin', 'Load a new Song')
#        elf.text['new'] = translate('AlertsPlugin', 'Add a new Song')
#        elf.text['edit'] = translate('AlertsPlugin', 'Edit the selected Song')
#        elf.text['delete'] = translate('AlertsPlugin', 'Delete the selected Song')
#        elf.text['delete_more'] = translate('AlertsPlugin', 'Delete the selected Songs')
#        elf.text['preview'] = translate('AlertsPlugin', 'Preview the selected Song')
#        elf.text['preview_more'] = translate('AlertsPlugin', 'Preview the selected Songs')
#        elf.text['live'] = translate('AlertsPlugin', 'Send the selected Song live')
#        elf.text['live_more'] = translate('AlertsPlugin', 'Send the selected Songs live')
#        elf.text['service'] = translate('AlertsPlugin', 'Add the selected Song to the service')
#        elf.text['service_more'] = translate('AlertsPlugin', 'Add the selected Songs to the service')
#        # for names in mediamanagerdock and pluginlist
        self.text['name'] = translate('AlertsPlugin', 'Alert')
        self.text['name_more'] = translate('AlertsPlugin', 'Alerts')
