# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import logging

from PyQt4 import QtCore, QtGui

from openlp.core.lib import SettingsTab
from openlp.core.resources import *
from openlp.core.ui import GeneralTab, ThemesTab, AlertsTab

from settingsdialog import Ui_SettingsDialog

log = logging.getLogger('SettingsForm')

class SettingsForm(QtGui.QDialog, Ui_SettingsDialog):

    def __init__(self, screen_list, mainWindow, parent=None):
        QtGui.QDialog.__init__(self, None)
        self.setupUi(self)
        # General tab
        self.GeneralTab = GeneralTab(screen_list)
        self.addTab(self.GeneralTab)
        # Themes tab
        self.ThemesTab = ThemesTab(mainWindow)
        self.addTab(self.ThemesTab)
        # Alert tab
        self.AlertsTab = AlertsTab()
        self.addTab(self.AlertsTab)

    def addTab(self, tab):
        log.info(u'Inserting %s' % tab.title())
        self.SettingsTabWidget.addTab(tab, tab.title())

    def accept(self):
        for tab_index in range(0,  self.SettingsTabWidget.count()):
            self.SettingsTabWidget.widget(tab_index).save()
        return QtGui.QDialog.accept(self)
