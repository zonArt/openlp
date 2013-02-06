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

import logging

from PyQt4 import QtGui

from openlp.core.lib import Plugin, Settings, StringContent, build_icon, translate
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import create_action, UiStrings
from openlp.core.lib.theme import VerticalType
from openlp.core.ui import AlertLocation
from openlp.core.utils.actions import ActionList
from openlp.plugins.alerts.lib import AlertsManager, AlertsTab
from openlp.plugins.alerts.lib.db import init_schema
from openlp.plugins.alerts.forms import AlertForm

log = logging.getLogger(__name__)

JAVASCRIPT = """
    function show_alert(alerttext, position){
        var text = document.getElementById('alert');
        text.innerHTML = alerttext;
        if(alerttext == '') {
            text.style.visibility = 'hidden';
            return 0;
        }
        if(position == ''){
            position = getComputedStyle(text, '').verticalAlign;
        }
        switch(position)
        {
            case 'top':
                text.style.top = '0px';
                break;
            case 'middle':
                text.style.top = ((window.innerHeight - text.clientHeight) / 2)
                    + 'px';
                break;
            case 'bottom':
                text.style.top = (window.innerHeight - text.clientHeight)
                    + 'px';
                break;
        }
        text.style.visibility = 'visible';
        return text.clientHeight;
    }

    function update_css(align, font, size, color, bgcolor){
        var text = document.getElementById('alert');
        text.style.fontSize = size + "pt";
        text.style.fontFamily = font;
        text.style.color = color;
        text.style.backgroundColor = bgcolor;
        switch(align)
        {
            case 'top':
                text.style.top = '0px';
                break;
            case 'middle':
                text.style.top = ((window.innerHeight - text.clientHeight) / 2)
                    + 'px';
                break;
            case 'bottom':
                text.style.top = (window.innerHeight - text.clientHeight)
                    + 'px';
                break;
        }
    }
"""
CSS = """
    #alert {
        position: absolute;
        left: 0px;
        top: 0px;
        z-index: 10;
        width: 100%%;
        vertical-align: %s;
        font-family: %s;
        font-size: %spt;
        color: %s;
        background-color: %s;
        word-wrap: break-word;
    }
"""

HTML = """
    <div id="alert" style="visibility:hidden"></div>
"""

__default_settings__ = {
        u'alerts/font face': QtGui.QFont().family(),
        u'alerts/font size': 40,
        u'alerts/db type': u'sqlite',
        u'alerts/location': AlertLocation.Bottom,
        u'alerts/background color': u'#660000',
        u'alerts/font color': u'#ffffff',
        u'alerts/timeout': 5
    }


class AlertsPlugin(Plugin):
    log.info(u'Alerts Plugin loaded')

    def __init__(self):
        Plugin.__init__(self, u'alerts', __default_settings__, settings_tab_class=AlertsTab)
        self.weight = -3
        self.iconPath = u':/plugins/plugin_alerts.png'
        self.icon = build_icon(self.iconPath)
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
        self.toolsAlertItem = create_action(tools_menu, u'toolsAlertItem',
            text=translate('AlertsPlugin', '&Alert'), icon=u':/plugins/plugin_alerts.png',
            statustip=translate('AlertsPlugin', 'Show an alert message.'),
            visible=False, shortcuts=[u'F7'], triggers=self.onAlertsTrigger)
        self.main_window.toolsMenu.addAction(self.toolsAlertItem)

    def initialise(self):
        log.info(u'Alerts Initialising')
        Plugin.initialise(self)
        self.toolsAlertItem.setVisible(True)
        action_list = ActionList.get_instance()
        action_list.add_action(self.toolsAlertItem, UiStrings().Tools)

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
        Settings().setValue(self.settingsSection + u'/active', self.alertsActive)

    def onAlertsTrigger(self):
        self.alertForm.loadList()
        self.alertForm.exec_()

    def about(self):
        about_text = translate('AlertsPlugin', '<strong>Alerts Plugin</strong>'
            '<br />The alert plugin controls the displaying of nursery alerts on the display screen.')
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
        self.textStrings[StringContent.VisibleName] = {u'title': translate('AlertsPlugin', 'Alerts', 'container title')
        }

    def getDisplayJavaScript(self):
        """
        Add Javascript to the main display.
        """
        return JAVASCRIPT

    def getDisplayCss(self):
        """
        Add CSS to the main display.
        """
        align = VerticalType.Names[self.settingsTab.location]
        return CSS % (align, self.settingsTab.font_face, self.settingsTab.font_size, self.settingsTab.font_color,
            self.settingsTab.bg_color)

    def getDisplayHtml(self):
        """
        Add HTML to the main display.
        """
        return HTML

    def refreshCss(self, frame):
        """
        Trigger an update of the CSS in the maindisplay.

        ``frame``
            The Web frame holding the page.
        """
        align = VerticalType.Names[self.settingsTab.location]
        frame.evaluateJavaScript(u'update_css("%s", "%s", "%s", "%s", "%s")' %
            (align, self.settingsTab.font_face, self.settingsTab.font_size,
            self.settingsTab.font_color, self.settingsTab.bg_color))
