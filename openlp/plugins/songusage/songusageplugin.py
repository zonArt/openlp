# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
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
        self.activeIcon = QtGui.QIcon(u':/songusage/song_usage_active.png')
        self.inactiveIcon = QtGui.QIcon(u':/songusage/song_usage_inactive.png')
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
        self.songUsageMenu = QtGui.QMenu(tools_menu)
        self.songUsageMenu.setObjectName(u'songUsageMenu')
        self.songUsageMenu.setTitle(translate(
            'SongUsagePlugin', '&Song Usage Tracking'))
        # SongUsage Delete
        self.songUsageDelete = base_action(tools_menu, u'songUsageDelete')
        self.songUsageDelete.setText(translate('SongUsagePlugin',
            '&Delete Tracking Data'))
        self.songUsageDelete.setStatusTip(translate('SongUsagePlugin',
            'Delete song usage data up to a specified date.'))
        # SongUsage Report
        self.songUsageReport = base_action(tools_menu, u'songUsageReport')
        self.songUsageReport.setText(
            translate('SongUsagePlugin', '&Extract Tracking Data'))
        self.songUsageReport.setStatusTip(
            translate('SongUsagePlugin', 'Generate a report on song usage.'))
        # SongUsage activation
        # Add Menus together
        self.toolsMenu.addAction(self.songUsageMenu.menuAction())
        self.songUsageMenu.addAction(self.songUsageDelete)
        self.songUsageMenu.addAction(self.songUsageReport)
        self.songUsageStatus = QtGui.QToolButton(self.formparent.statusBar)
        self.songUsageStatus.setCheckable(True)
        self.songUsageStatus.setStatusTip(translate('SongUsagePlugin',
                'Toggle the tracking of song usage.'))
        self.songUsageStatus.setObjectName(u'songUsageStatus')
        self.formparent.statusBar.insertPermanentWidget(1, self.songUsageStatus)
        self.songUsageStatus.hide()
        # Signals and slots
        QtCore.QObject.connect(self.songUsageStatus,
            QtCore.SIGNAL(u'toggled(bool)'),
            self.toggleSongUsageState)
        QtCore.QObject.connect(self.songUsageDelete,
            QtCore.SIGNAL(u'triggered()'), self.onSongUsageDelete)
        QtCore.QObject.connect(self.songUsageReport,
            QtCore.SIGNAL(u'triggered()'), self.onSongUsageReport)
        self.songUsageMenu.menuAction().setVisible(False)

    def initialise(self):
        log.info(u'SongUsage Initialising')
        Plugin.initialise(self)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_live_started'),
            self.onReceiveSongUsage)
        self.SongUsageActive = QtCore.QSettings().value(
            self.settingsSection + u'/active',
            QtCore.QVariant(False)).toBool()
        self.songUsageStatus.setChecked(self.SongUsageActive)
        action_list = ActionList.get_instance()
        action_list.add_action(self.songUsageDelete,
            translate('SongUsagePlugin', 'Song Usage'))
        action_list.add_action(self.songUsageReport,
            translate('SongUsagePlugin', 'Song Usage'))
        if self.manager is None:
            self.manager = Manager(u'songusage', init_schema)
        self.songUsageDeleteForm = SongUsageDeleteForm(self.manager,
            self.formparent)
        self.songUsageDetailForm = SongUsageDetailForm(self, self.formparent)
        self.songUsageMenu.menuAction().setVisible(True)
        self.songUsageStatus.show()
        self.songUsageStatus.setIcon(self.activeIcon)

    def finalise(self):
        """
        Tidy up on exit
        """
        log.info(u'Plugin Finalise')
        self.manager.finalise()
        Plugin.finalise(self)
        self.songUsageMenu.menuAction().setVisible(False)
        action_list = ActionList.get_instance()
        action_list.remove_action(self.songUsageDelete,
            translate('SongUsagePlugin', 'Song Usage'))
        action_list.remove_action(self.songUsageReport,
            translate('SongUsagePlugin', 'Song Usage'))
        self.songUsageStatus.hide()
        # stop any events being processed
        self.SongUsageActive = False

    def toggleSongUsageState(self):
        """
        Manage the state of the audit collection and amend
        the UI when necessary,
        """
        print "toggle state"
        self.SongUsageActive = not self.SongUsageActive
        QtCore.QSettings().setValue(self.settingsSection + u'/active',
            QtCore.QVariant(self.SongUsageActive))
        if self.SongUsageActive:
            self.songUsageStatus.setIcon(self.activeIcon)
        else:
            self.songUsageStatus.setIcon(self.inactiveIcon)

    def onReceiveSongUsage(self, item):
        """
        Song Usage for live song from SlideController
        """
        audit = item[0].audit
        print audit
        if self.SongUsageActive and audit:
            print "here"
            song_usage_item = SongUsageItem()
            song_usage_item.usagedate = datetime.today()
            song_usage_item.usagetime = datetime.now().time()
            song_usage_item.title = audit[0]
            song_usage_item.copyright = audit[2]
            song_usage_item.ccl_number = audit[3]
            song_usage_item.authors = u' '.join(audit[1])
            self.manager.save_object(song_usage_item)

    def onSongUsageDelete(self):
        self.songUsageDeleteForm.exec_()

    def onSongUsageReport(self):
        self.songUsageDetailForm.initialise()
        self.songUsageDetailForm.exec_()

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
