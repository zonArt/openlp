from openlp.plugins.alerts.forms import AlertsTab, AlertForm# -*- coding: utf-8 -*-
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

from datetime import datetime
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, Receiver, str_to_bool, build_icon
from openlp.plugins.display.forms import DisplayForm

log = logging.getLogger(__name__)

class DisplayPlugin(Plugin):
    log.info(u'Display Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Display', u'1.9.1', plugin_helpers)
        self.weight = -2
        self.icon = build_icon(u':/media/media_image.png')

    def add_tools_menu_item(self, tools_menu):
        """
        Give the Display plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.info(u'add tools menu')
        self.toolsMenu = tools_menu
        self.DisplayMenu = QtGui.QMenu(tools_menu)
        self.DisplayMenu.setObjectName(u'DisplayMenu')
        self.DisplayMenu.setTitle(tools_menu.trUtf8('&Override Display'))
        #Display Delete
        self.DisplayOverride = QtGui.QAction(tools_menu)
        self.DisplayOverride.setText(
            tools_menu.trUtf8('&Change Display Attributes'))
        self.DisplayOverride.setStatusTip(
            tools_menu.trUtf8('Amend the display attributes'))
        self.DisplayOverride.setObjectName(u'DisplayOverride')
        #Display activation
        DisplayIcon = build_icon(u':/tools/tools_alert.png')
        self.DisplayStatus = QtGui.QAction(tools_menu)
        self.DisplayStatus.setIcon(DisplayIcon)
        self.DisplayStatus.setCheckable(True)
        self.DisplayStatus.setChecked(False)
        self.DisplayStatus.setText(tools_menu.trUtf8('Use Display Override'))
        self.DisplayStatus.setStatusTip(
            tools_menu.trUtf8('Change start/stop using Display Override'))
        self.DisplayStatus.setShortcut(u'FX')
        self.DisplayStatus.setObjectName(u'DisplayStatus')
        #Add Menus together
        self.toolsMenu.addAction(self.DisplayMenu.menuAction())
        self.DisplayMenu.addAction(self.DisplayStatus)
        self.DisplayMenu.addSeparator()
        self.DisplayMenu.addAction(self.DisplayOverride)
        # Signals and slots
        QtCore.QObject.connect(self.DisplayStatus,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.DisplayStatus.setChecked)
        QtCore.QObject.connect(self.DisplayStatus,
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleDisplayState)
        QtCore.QObject.connect(self.DisplayOverride,
            QtCore.SIGNAL(u'triggered()'), self.onDisplayOverride)
        self.DisplayMenu.menuAction().setVisible(False)

    def initialise(self):
        log.info(u'Display Initialising')
        Plugin.initialise(self)
        self.DisplayStatus.setChecked(False)
        self.screens = self.maindisplay.screens
        self.displayform = DisplayForm(self, self.screens)
        self.DisplayMenu.menuAction().setVisible(True)

    def finalise(self):
        log.info(u'Plugin Finalise')
        self.DisplayMenu.menuAction().setVisible(False)

    def toggleDisplayState(self):
        Receiver.send_message(u'config_screen_changed')

    def onDisplayOverride(self):
        self.displayform.initialise()
        self.displayform.exec_()
        if self.DisplayStatus.isChecked():
            Receiver.send_message(u'config_screen_changed')

    def about(self):
        about_text = self.trUtf8('<b>Display Plugin</b><br>This plugin '
            'allows the dimensions of the live display to be changed.\n'
            'These changes are not stored.')
        return about_text
