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
from datetime import datetime

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, Receiver, Settings, StringContent, build_icon, translate
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import create_action
from openlp.core.utils.actions import ActionList
from openlp.plugins.songusage.forms import SongUsageDetailForm, SongUsageDeleteForm
from openlp.plugins.songusage.lib import upgrade
from openlp.plugins.songusage.lib.db import init_schema, SongUsageItem

log = logging.getLogger(__name__)


YEAR = QtCore.QDate().currentDate().year()
if QtCore.QDate().currentDate().month() < 9:
    YEAR -= 1


__default_settings__ = {
        u'songusage/db type': u'sqlite',
        u'songusage/active': False,
        u'songusage/to date': QtCore.QDate(YEAR, 8, 31),
        u'songusage/from date': QtCore.QDate(YEAR - 1, 9, 1),
        u'songusage/last directory export': u''
    }


class SongUsagePlugin(Plugin):
    log.info(u'SongUsage Plugin loaded')

    def __init__(self):
        Plugin.__init__(self, u'songusage', __default_settings__)
        self.manager = Manager(u'songusage', init_schema, upgrade_mod=upgrade)
        self.weight = -4
        self.icon = build_icon(u':/plugins/plugin_songusage.png')
        self.activeIcon = build_icon(u':/songusage/song_usage_active.png')
        self.inactiveIcon = build_icon(u':/songusage/song_usage_inactive.png')
        self.songUsageActive = False

    def checkPreConditions(self):
        return self.manager.session is not None

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
        self.songUsageMenu.setTitle(translate('SongUsagePlugin', '&Song Usage Tracking'))
        # SongUsage Delete
        self.songUsageDelete = create_action(tools_menu, u'songUsageDelete',
            text=translate('SongUsagePlugin', '&Delete Tracking Data'),
            statustip=translate('SongUsagePlugin', 'Delete song usage data up to a specified date.'),
            triggers=self.onSongUsageDelete)
        # SongUsage Report
        self.songUsageReport = create_action(tools_menu, u'songUsageReport',
            text=translate('SongUsagePlugin', '&Extract Tracking Data'),
            statustip=translate('SongUsagePlugin', 'Generate a report on song usage.'),
            triggers=self.onSongUsageReport)
        # SongUsage activation
        self.songUsageStatus = create_action(tools_menu, u'songUsageStatus',
            text=translate('SongUsagePlugin', 'Toggle Tracking'),
            statustip=translate('SongUsagePlugin', 'Toggle the tracking of song usage.'), checked=False,
            shortcuts=[QtCore.Qt.Key_F4], triggers=self.toggleSongUsageState)
        # Add Menus together
        self.toolsMenu.addAction(self.songUsageMenu.menuAction())
        self.songUsageMenu.addAction(self.songUsageStatus)
        self.songUsageMenu.addSeparator()
        self.songUsageMenu.addAction(self.songUsageReport)
        self.songUsageMenu.addAction(self.songUsageDelete)
        self.songUsageActiveButton = QtGui.QToolButton(self.main_window.statusBar)
        self.songUsageActiveButton.setCheckable(True)
        self.songUsageActiveButton.setAutoRaise(True)
        self.songUsageActiveButton.setStatusTip(translate('SongUsagePlugin', 'Toggle the tracking of song usage.'))
        self.songUsageActiveButton.setObjectName(u'songUsageActiveButton')
        self.main_window.statusBar.insertPermanentWidget(1, self.songUsageActiveButton)
        self.songUsageActiveButton.hide()
        # Signals and slots
        QtCore.QObject.connect(self.songUsageStatus, QtCore.SIGNAL(u'visibilityChanged(bool)'),
            self.songUsageStatus.setChecked)
        QtCore.QObject.connect(self.songUsageActiveButton, QtCore.SIGNAL(u'toggled(bool)'), self.toggleSongUsageState)
        self.songUsageMenu.menuAction().setVisible(False)

    def initialise(self):
        log.info(u'SongUsage Initialising')
        Plugin.initialise(self)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'slidecontroller_live_started'),
            self.displaySongUsage)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'print_service_started'),
            self.printSongUsage)
        self.songUsageActive = Settings().value(self.settingsSection + u'/active')
        # Set the button and checkbox state
        self.setButtonState()
        action_list = ActionList.get_instance()
        action_list.add_action(self.songUsageStatus, translate('SongUsagePlugin', 'Song Usage'))
        action_list.add_action(self.songUsageDelete, translate('SongUsagePlugin', 'Song Usage'))
        action_list.add_action(self.songUsageReport, translate('SongUsagePlugin', 'Song Usage'))
        self.songUsageDeleteForm = SongUsageDeleteForm(self.manager, self.main_window)
        self.songUsageDetailForm = SongUsageDetailForm(self, self.main_window)
        self.songUsageMenu.menuAction().setVisible(True)
        self.songUsageActiveButton.show()

    def finalise(self):
        """
        Tidy up on exit
        """
        log.info(u'Plugin Finalise')
        self.manager.finalise()
        Plugin.finalise(self)
        self.songUsageMenu.menuAction().setVisible(False)
        action_list = ActionList.get_instance()
        action_list.remove_action(self.songUsageStatus, translate('SongUsagePlugin', 'Song Usage'))
        action_list.remove_action(self.songUsageDelete, translate('SongUsagePlugin', 'Song Usage'))
        action_list.remove_action(self.songUsageReport, translate('SongUsagePlugin', 'Song Usage'))
        self.songUsageActiveButton.hide()
        # stop any events being processed
        self.songUsageActive = False

    def toggleSongUsageState(self):
        """
        Manage the state of the audit collection and amend
        the UI when necessary,
        """
        self.songUsageActive = not self.songUsageActive
        Settings().setValue(self.settingsSection + u'/active', self.songUsageActive)
        self.setButtonState()

    def setButtonState(self):
        """
        Keep buttons inline.  Turn of signals to stop dead loop but we need the
        button and check box set correctly.
        """
        self.songUsageActiveButton.blockSignals(True)
        self.songUsageStatus.blockSignals(True)
        if self.songUsageActive:
            self.songUsageActiveButton.setIcon(self.activeIcon)
            self.songUsageStatus.setChecked(True)
            self.songUsageActiveButton.setChecked(True)
            self.songUsageActiveButton.setToolTip(translate('SongUsagePlugin', 'Song usage tracking is active.'))
        else:
            self.songUsageActiveButton.setIcon(self.inactiveIcon)
            self.songUsageStatus.setChecked(False)
            self.songUsageActiveButton.setChecked(False)
            self.songUsageActiveButton.setToolTip(translate('SongUsagePlugin', 'Song usage tracking is inactive.'))
        self.songUsageActiveButton.blockSignals(False)
        self.songUsageStatus.blockSignals(False)


    def displaySongUsage(self, item):
        """
        Song Usage for which has been displayed
        """
        self._add_song_usage(translate('SongUsagePlugin', 'display'), item)

    def printSongUsage(self, item):
        """
        Song Usage for which has been printed
        """
        self._add_song_usage(translate('SongUsagePlugin', 'printed'), item)

    def _add_song_usage(self, source, item):
        audit = item[0].audit
        if self.songUsageActive and audit:
            song_usage_item = SongUsageItem()
            song_usage_item.usagedate = datetime.today()
            song_usage_item.usagetime = datetime.now().time()
            song_usage_item.title = audit[0]
            song_usage_item.copyright = audit[2]
            song_usage_item.ccl_number = audit[3]
            song_usage_item.authors = u' '.join(audit[1])
            song_usage_item.plugin_name = item[0].name
            song_usage_item.source = source
            self.manager.save_object(song_usage_item)

    def onSongUsageDelete(self):
        self.songUsageDeleteForm.exec_()

    def onSongUsageReport(self):
        self.songUsageDetailForm.initialise()
        self.songUsageDetailForm.exec_()

    def about(self):
        about_text = translate('SongUsagePlugin', '<strong>SongUsage Plugin'
            '</strong><br />This plugin tracks the usage of songs in services.')
        return about_text

    def setPluginTextStrings(self):
        """
        Called to define all translatable texts of the plugin
        """
        ## Name PluginList ##
        self.textStrings[StringContent.Name] = {
            u'singular': translate('SongUsagePlugin', 'SongUsage', 'name singular'),
            u'plural': translate('SongUsagePlugin', 'SongUsage', 'name plural')
        }
        ## Name for MediaDockManager, SettingsManager ##
        self.textStrings[StringContent.VisibleName] = {
            u'title': translate('SongUsagePlugin', 'SongUsage', 'container title')
        }
