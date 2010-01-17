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

from datetime import datetime
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Plugin, Receiver, str_to_bool, buildIcon
from openlp.plugins.songusage.lib import SongUsageManager
from openlp.plugins.songusage.forms import SongUsageDetailForm, SongUsageDeleteForm
from openlp.plugins.songusage.lib.models import SongUsageItem

class SongUsagePlugin(Plugin):
    global log
    log = logging.getLogger(u'SongUsagePlugin')
    log.info(u'SongUsage Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'SongUsage', u'1.9.0', plugin_helpers)
        self.weight = -4
        self.icon = buildIcon(u':/media/media_image.png')
        self.songusagemanager = None
        self.songusageActive = False

    def add_tools_menu_item(self, tools_menu):
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
        self.SongUsageMenu.setTitle(tools_menu.trUtf8(u'&Song Usage'))
        #SongUsage Delete
        self.SongUsageDelete = QtGui.QAction(tools_menu)
        self.SongUsageDelete.setText(
            tools_menu.trUtf8(u'&Delete recorded data'))
        self.SongUsageDelete.setStatusTip(
            tools_menu.trUtf8(u'Delete song usage to specified date'))
        self.SongUsageDelete.setObjectName(u'SongUsageDelete')
        #SongUsage Report
        self.SongUsageReport = QtGui.QAction(tools_menu)
        self.SongUsageReport.setText(
            tools_menu.trUtf8(u'&Extract recorded data'))
        self.SongUsageReport.setStatusTip(
            tools_menu.trUtf8(u'Generate report on Song Usage'))
        self.SongUsageReport.setObjectName(u'SongUsageReport')
        #SongUsage activation
        SongUsageIcon = buildIcon(u':/tools/tools_alert.png')
        self.SongUsageStatus = QtGui.QAction(tools_menu)
        self.SongUsageStatus.setIcon(SongUsageIcon)
        self.SongUsageStatus.setCheckable(True)
        self.SongUsageStatus.setChecked(False)
        self.SongUsageStatus.setText(tools_menu.trUtf8(u'Song Usage Status'))
        self.SongUsageStatus.setStatusTip(
            tools_menu.trUtf8(u'Start/Stop live song usage recording'))
        self.SongUsageStatus.setShortcut(u'F4')
        self.SongUsageStatus.setObjectName(u'SongUsageStatus')
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
        QtCore.QObject.connect(self.SongUsageStatus,
            QtCore.SIGNAL(u'triggered(bool)'),
            self.toggleSongUsageState)
        QtCore.QObject.connect(self.SongUsageDelete,
            QtCore.SIGNAL(u'triggered()'), self.onSongUsageDelete)
        QtCore.QObject.connect(self.SongUsageReport,
            QtCore.SIGNAL(u'triggered()'), self.onSongUsageReport)
        self.SongUsageMenu.menuAction().setVisible(False)

    def initialise(self):
        log.info(u'SongUsage Initialising')
        Plugin.initialise(self)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'songusage_live'), self.onReceiveSongUsage)
        self.SongUsageActive = str_to_bool(
            self.config.get_config(u'audit active', False))
        self.SongUsageStatus.setChecked(self.SongUsageActive)
        if self.songusagemanager is None:
            self.songusagemanager = SongUsageManager(self.config)
        self.SongUsagedeleteform = SongUsageDeleteForm(self.songusagemanager)
        self.SongUsagedetailform = SongUsageDetailForm(self)
        self.SongUsageMenu.menuAction().setVisible(True)

    def finalise(self):
        log.info(u'Plugin Finalise')
        self.SongUsageMenu.menuAction().setVisible(False)
        #stop any events being processed
        self.SongUsageActive = False

    def toggleSongUsageState(self):
        self.SongUsageActive = not self.SongUsageActive
        self.config.set_config(u'SongUsage active', self.SongUsageActive)

    def onReceiveSongUsage(self, SongUsageData):
        """
        SongUsage a live song from SlideController
        """
        if self.SongUsageActive:
            SongUsageitem = SongUsageItem()
            SongUsageitem.usagedate = datetime.today()
            SongUsageitem.usagetime = datetime.now().time()
            SongUsageitem.title = SongUsageData[0]
            SongUsageitem.copyright = SongUsageData[2]
            SongUsageitem.ccl_number = SongUsageData[3]
            SongUsageitem.authors = u''
            for author in SongUsageData[1]:
                SongUsageitem.authors += author + u' '
            self.songusagemanager.insert_SongUsage(SongUsageitem)

    def onSongUsageDelete(self):
        self.SongUsagedeleteform.exec_()

    def onSongUsageReport(self):
        self.SongUsagedetailform.initialise()
        self.SongUsagedetailform.exec_()

    def about(self):
        about_text = self.trUtf8(u'<b>SongUsage Plugin</b><br>This plugin '
            u'records the use of songs and when they have been used during '
            u'a live service')
        return about_text
