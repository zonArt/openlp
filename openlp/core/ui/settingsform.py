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
"""
The :mod:`settingsform` provides a user interface for the OpenLP settings
"""
import logging

from PyQt4 import QtGui, QtCore

from openlp.core.lib import Receiver, build_icon
from openlp.core.ui import AdvancedTab, GeneralTab, ThemesTab
from settingsdialog import Ui_SettingsDialog

log = logging.getLogger(__name__)

class SettingsForm(QtGui.QDialog, Ui_SettingsDialog):
    """
    Provide the form to manipulate the settings for OpenLP
    """
    def __init__(self, screens, mainWindow, parent=None):
        """
        Initialise the settings form
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        # General tab
        generalTab = GeneralTab(screens)
        self.insertTab(generalTab, 1)
        # Themes tab
        themesTab = ThemesTab(mainWindow)
        self.insertTab(themesTab, 2)
        # Advanced tab
        advancedTab = AdvancedTab()
        self.insertTab(advancedTab, 3)

    def exec_(self):
        # load all the settings
        for tabIndex in range(0, self.stackedLayout.count()):
            self.stackedLayout.widget(tabIndex).load()
        self.settingListWidget.setCurrentRow(0)
        return QtGui.QDialog.exec_(self)

    def insertTab(self, tab, location):
        """
        Add a tab to the form at a specific location
        """
        log.debug(u'Inserting %s tab' % tab.tabTitle)
        # 14 : There are 3 tables currently and locations starts at -10
        match = False
        for tabIndex in range(0, self.stackedLayout.count()):
            if self.stackedLayout.widget(tabIndex):
                if self.stackedLayout.widget(tabIndex).tabTitleVisible == \
                    tab.tabTitleVisible:
                    self.stackedLayout.widget(tabIndex).setHidden(False)
                    match = True
                    break
        if not match:
            pos = self.stackedLayout.addWidget(tab)
            item_name = QtGui.QListWidgetItem(tab.tabTitleVisible)
            icon = build_icon(tab.icon_path)
            item_name.setIcon(icon)
            self.settingListWidget.insertItem(14 + location, item_name)

    def removeTab(self, tab):
        """
        Remove a tab from the form
        """
        log.debug(u'remove %s tab' % tab.tabTitleVisible)
        for tabIndex in range(0, self.stackedLayout.count()):
            if self.stackedLayout.widget(tabIndex):
                if self.stackedLayout.widget(tabIndex).tabTitleVisible == \
                    tab.tabTitleVisible:
                    self.settingListWidget.item(tabIndex).setHidden(True)

    def accept(self):
        """
        Process the form saving the settings
        """
        for tabIndex in range(0, self.stackedLayout.count()):
            self.stackedLayout.widget(tabIndex).save()
        # Must go after all settings are save
        Receiver.send_message(u'config_updated')
        return QtGui.QDialog.accept(self)

    def reject(self):
        """
        Process the form saving the settings
        """
        for tabIndex in range(0, self.stackedLayout.count()):
            self.stackedLayout.widget(tabIndex).cancel()
        return QtGui.QDialog.reject(self)

    def postSetUp(self):
        """
        Run any post-setup code for the tabs on the form
        """
        for tabIndex in range(0, self.stackedLayout.count()):
            self.stackedLayout.widget(tabIndex).postSetUp()
