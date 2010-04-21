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

from PyQt4 import QtGui

from openlp.core.ui import GeneralTab, ThemesTab
from settingsdialog import Ui_SettingsDialog

log = logging.getLogger(__name__)

class SettingsForm(QtGui.QDialog, Ui_SettingsDialog):

    def __init__(self, screens, mainWindow, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        # General tab
        self.GeneralTab = GeneralTab(screens)
        self.addTab(u'General', self.GeneralTab)
        # Themes tab
        self.ThemesTab = ThemesTab(mainWindow)
        self.addTab(u'Themes', self.ThemesTab)

    def addTab(self, name, tab):
        log.info(u'Adding %s tab' % tab.tabTitle)
        self.SettingsTabWidget.addTab(tab, tab.tabTitleVisible)

    def insertTab(self, tab, location):
        log.debug(u'Inserting %s tab' % tab.tabTitle)
        #13 : There are 3 tables currently and locations starts at -10
        self.SettingsTabWidget.insertTab(
            location + 13, tab, tab.tabTitleVisible)

    def removeTab(self, name):
        log.debug(u'remove %s tab' % name)
        for tab_index in range(0, self.SettingsTabWidget.count()):
            if self.SettingsTabWidget.widget(tab_index):
                if self.SettingsTabWidget.widget(tab_index).tabTitle == name:
                    self.SettingsTabWidget.removeTab(tab_index)

    def accept(self):
        for tab_index in range(0, self.SettingsTabWidget.count()):
            self.SettingsTabWidget.widget(tab_index).save()
        return QtGui.QDialog.accept(self)

    def postSetUp(self):
        for tab_index in range(0, self.SettingsTabWidget.count()):
            self.SettingsTabWidget.widget(tab_index).postSetUp()
