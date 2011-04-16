# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
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
from datetime import datetime

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, StringContent, Receiver, build_icon, \
    translate
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import base_action, shortcut_action, UiStrings
from openlp.core.utils.actions import ActionList
from openlp.plugins.songusage.forms import SongUsageDetailForm, \
    SongUsageDeleteForm
from openlp.plugins.songusage.lib.db import init_schema, SongUsageItem

log = logging.getLogger(__name__)

class SongUsagePlugin(Plugin):
    log.info(u'SongUsage Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'SongUsage', plugin_helpers)
        self.weight = -4
        self.icon = build_icon(u':/plugins/plugin_songusage.png')
        self.manager = None
        self.songusageActive = False

    def addToolsMenuItem(self, tools_menu):
        """
        Give the SongUsage plugin the opportunity to add items to the
        **Tools** menu.

        ``tools_menu``
            The actual **Tools** menu item, so that your actions can
            use it as their parent.
        """
        log.info(u'add tools menu')
        self.toolsMenu = tools_menu
        self.SongUsageMenu = QtGui.QMenu(tools_menu)
        self.SongUsageMenu.setObjectName(u'SongUsageMenu')
        self.SongUsageMenu.setTitle(translate(
            'SongUsagePlugin', '&Song Usage Tracking'))
        # SongUsage Delete
        self.SongUsageDelete = base_action(tools_menu, u'SongUsageDelete')
        self.SongUsageDelete.setText(translate('SongUsagePlugin',
            '&Delete Tracking Data'))
        self.SongUsageDelete.setStatusTip(translate('SongUsagePlugin',
            'Delete song usage data up to a specified date.'))
        # SongUsage Report
        self.SongUsageReport = base_action(tools_menu, u'SongUsageReport')
        self.SongUsageReport.setText(
            translate('SongUsagePlugin', '&Extract Tracking Data'))
        self.SongUsageReport.setStatusTip(
            translate('SongUsagePlugin', 'Generate a report on song usage.'))
        # SongUsage activation
        self.SongUsageStatus = shortcut_action(tools_menu, u'SongUsageStatus',
            [QtCore.Qt.Key_F4], self.toggleSongUsageState, checked=False)
        self.SongUsageStatus.setText(translate(
            'SongUsagePlugin', 'Toggle Tracking'))
        self.SongUsageStatus.setStatusTip(translate('SongUsagePlugin',
                'Toggle the tracking of song usage.'))
        #Add Menus together
        self.toolsMenu.addAction(self.SongUsageMenu.menuAction())
        self.SongUsageMenu.addAction(self.SongUsageStatus)
        self.SongUsageMenu.addSeparator()
        self.SongUsageMenu.addAction(self.SongUsageDelete)
        self.SongUsageMenu.addAction(self.SongUsageReport)
        # Signals and slots
        QtCore.QObject.connect(self.SongUsageStatus,
            QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.SongUsageStatus.setChecked)
        QtCore.QObject.connect(self.SongUsageDelete,
            QtCore.SIGNAL(u'triggered()'), self.onSongUsageDelete)
        QtCore.QObject.connect(self.SongUsageReport,
            QtCore.SIGNAL(u'triggered()'), self.onSongUsageReport)
        self.SongUsageMenu.menuAction().setVisible(False)

    def initialise(self):
        log.info(u'SongUsage Initialising')
        Plugin.initialise(self)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_live_started'),
            self.onReceiveSongUsage)
        self.SongUsageActive = QtCore.QSettings().value(
            self.settingsSection + u'/active',
            QtCore.QVariant(False)).toBool()
        self.SongUsageStatus.setChecked(self.SongUsageActive)
        action_list = ActionList.get_instance()
        action_list.add_action(self.SongUsageDelete,
            translate('SongUsagePlugin', 'Song Usage'))
        action_list.add_action(self.SongUsageReport,
            translate('SongUsagePlugin', 'Song Usage'))
        action_list.add_action(self.SongUsageStatus,
            translate('SongUsagePlugin', 'Song Usage'))
        if self.manager is None:
            self.manager = Manager(u'songusage', init_schema)
        self.SongUsagedeleteform = SongUsageDeleteForm(self.manager,
            self.formparent)
        self.SongUsagedetailform = SongUsageDetailForm(self, self.formparent)
        self.SongUsageMenu.menuAction().setVisible(True)

    def finalise(self):
        """
        Tidy up on exit
        """
        log.info(u'Plugin Finalise')
        self.manager.finalise()
        Plugin.finalise(self)
        self.SongUsageMenu.menuAction().setVisible(False)
        action_list = ActionList.get_instance()
        action_list.remove_action(self.SongUsageDelete,
            translate('SongUsagePlugin', 'Song Usage'))
        action_list.remove_action(self.SongUsageReport,
            translate('SongUsagePlugin', 'Song Usage'))
        action_list.remove_action(self.SongUsageStatus,
            translate('SongUsagePlugin', 'Song Usage'))
        #stop any events being processed
        self.SongUsageActive = False

    def toggleSongUsageState(self):
        self.SongUsageActive = not self.SongUsageActive
        QtCore.QSettings().setValue(self.settingsSection + u'/active',
            QtCore.QVariant(self.SongUsageActive))

    def onReceiveSongUsage(self, item):
        """
        Song Usage for live song from SlideController
        """
        audit = item[0].audit
        if self.SongUsageActive and audit:
            song_usage_item = SongUsageItem()
            song_usage_item.usagedate = datetime.today()
            song_usage_item.usagetime = datetime.now().time()
            song_usage_item.title = audit[0]
            song_usage_item.copyright = audit[2]
            song_usage_item.ccl_number = audit[3]
            song_usage_item.authors = u''
            for author in audit[1]:
                song_usage_item.authors += author + u' '
            self.manager.save_object(song_usage_item)

    def onSongUsageDelete(self):
        self.SongUsagedeleteform.exec_()

    def onSongUsageReport(self):
        self.SongUsagedetailform.initialise()
        self.SongUsagedetailform.exec_()

    def about(self):
        about_text = translate('SongUsagePlugin', '<strong>SongUsage Plugin'
            '</strong><br />This plugin tracks the usage of songs in '
            'services.')
        return about_text

    def setPluginTextStrings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.textStrings[StringContent.Name] = {
            u'singular': translate('SongUsagePlugin', 'SongUsage',
                'name singular'),
            u'plural': translate('SongUsagePlugin', 'SongUsage',
                'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.textStrings[StringContent.VisibleName] = {
            u'title': translate('SongUsagePlugin', 'SongUsage',
                'container title')
        }
