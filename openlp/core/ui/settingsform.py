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
"""
The :mod:`settingsform` provides a user interface for the OpenLP settings
"""
import logging

from PyQt4 import QtGui

from openlp.core.lib import Receiver, PluginStatus, Registry, build_icon
from openlp.core.ui import AdvancedTab, GeneralTab, ThemesTab
from openlp.core.ui.media import PlayerTab
from settingsdialog import Ui_SettingsDialog

log = logging.getLogger(__name__)


class SettingsForm(QtGui.QDialog, Ui_SettingsDialog):
    """
    Provide the form to manipulate the settings for OpenLP
    """
    def __init__(self, parent=None):
        """
        Initialise the settings form
        """
        Registry().register(u'settings_form', self)
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        # General tab
        self.generalTab = GeneralTab(self)
        # Themes tab
        self.themesTab = ThemesTab(self)
        # Advanced tab
        self.advancedTab = AdvancedTab(self)
        # Advanced tab
        self.playerTab = PlayerTab(self)

    def exec_(self):
        """
        Execute the form
        """
        # load all the settings
        self.settingListWidget.clear()
        while self.stackedLayout.count():
            # take at 0 and the rest shuffle up.
            self.stackedLayout.takeAt(0)
        self.insertTab(self.generalTab, 0, PluginStatus.Active)
        self.insertTab(self.themesTab, 1, PluginStatus.Active)
        self.insertTab(self.advancedTab, 2, PluginStatus.Active)
        self.insertTab(self.playerTab, 3, PluginStatus.Active)
        count = 4
        for plugin in self.plugins:
            if plugin.settingsTab:
                self.insertTab(plugin.settingsTab, count, plugin.status)
                count += 1
        self.settingListWidget.setCurrentRow(0)
        return QtGui.QDialog.exec_(self)

    def insertTab(self, tab, location, is_active):
        """
        Add a tab to the form at a specific location
        """
        log.debug(u'Inserting %s tab' % tab.tabTitle)
        # add the tab to get it to display in the correct part of the screen
        pos = self.stackedLayout.addWidget(tab)
        if is_active:
            item_name = QtGui.QListWidgetItem(tab.tabTitleVisible)
            icon = build_icon(tab.iconPath)
            item_name.setIcon(icon)
            self.settingListWidget.insertItem(location, item_name)
        else:
            # then remove tab to stop the UI displaying it even if
            # it is not required.
            self.stackedLayout.takeAt(pos)

    def accept(self):
        """
        Process the form saving the settings
        """
        self.resetSuffixes = True
        for tabIndex in range(self.stackedLayout.count()):
            self.stackedLayout.widget(tabIndex).save()
        # Must go after all settings are save
        Receiver.send_message(u'config_updated')
        return QtGui.QDialog.accept(self)

    def reject(self):
        """
        Process the form saving the settings
        """
        for tabIndex in range(self.stackedLayout.count()):
            self.stackedLayout.widget(tabIndex).cancel()
        return QtGui.QDialog.reject(self)

    def postSetUp(self):
        """
        Run any post-setup code for the tabs on the form
        """
        self.generalTab.postSetUp()
        self.themesTab.postSetUp()
        self.advancedTab.postSetUp()
        self.playerTab.postSetUp()
        for plugin in self.plugins:
            if plugin.settingsTab:
                plugin.settingsTab.postSetUp()

    def tabChanged(self, tabIndex):
        """
        A different settings tab is selected
        """
        self.stackedLayout.setCurrentIndex(tabIndex)
        self.stackedLayout.currentWidget().tabVisible()

    def resetSupportedSuffixes(self):
        """
        Control the resetting of the serviceManager suffix list as can be
        called by a number of settings tab and only needs to be called once
        per save.
        """
        if self.resetSuffixes:
            self.service_manager.reset_supported_suffixes()
            self.resetSuffixes = False

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _get_service_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, u'_service_manager'):
            self._service_manager = Registry().get(u'service_manager')
        return self._service_manager

    service_manager = property(_get_service_manager)
