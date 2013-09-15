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

from openlp.core.lib import PluginStatus, Registry, build_icon
from openlp.core.ui import AdvancedTab, GeneralTab, ThemesTab
from openlp.core.ui.media import PlayerTab
from .settingsdialog import Ui_SettingsDialog

log = logging.getLogger(__name__)


class SettingsForm(QtGui.QDialog, Ui_SettingsDialog):
    """
    Provide the form to manipulate the settings for OpenLP
    """
    def __init__(self, parent=None):
        """
        Initialise the settings form
        """
        Registry().register('settings_form', self)
        Registry().register_function('bootstrap_post_set_up', self.post_set_up)
        super(SettingsForm, self).__init__(parent)
        self.processes = []
        self.setupUi(self)

    def exec_(self):
        """
        Execute the form
        """
        # load all the settings
        self.setting_list_widget.clear()
        while self.stacked_layout.count():
            # take at 0 and the rest shuffle up.
            self.stacked_layout.takeAt(0)
        self.insert_tab(self.general_tab, 0, PluginStatus.Active)
        self.insert_tab(self.themes_tab, 1, PluginStatus.Active)
        self.insert_tab(self.advanced_tab, 2, PluginStatus.Active)
        self.insert_tab(self.player_tab, 3, PluginStatus.Active)
        count = 4
        for plugin in self.plugin_manager.plugins:
            if plugin.settings_tab:
                self.insert_tab(plugin.settings_tab, count, plugin.status)
                count += 1
        self.setting_list_widget.setCurrentRow(0)
        return QtGui.QDialog.exec_(self)

    def insert_tab(self, tab, location, is_active):
        """
        Add a tab to the form at a specific location
        """
        log.debug('Inserting %s tab' % tab.tab_title)
        # add the tab to get it to display in the correct part of the screen
        pos = self.stacked_layout.addWidget(tab)
        if is_active:
            item_name = QtGui.QListWidgetItem(tab.tab_title_visible)
            icon = build_icon(tab.icon_path)
            item_name.setIcon(icon)
            self.setting_list_widget.insertItem(location, item_name)
        else:
            # then remove tab to stop the UI displaying it even if it is not required.
            self.stacked_layout.takeAt(pos)

    def accept(self):
        """
        Process the form saving the settings
        """
        log.debug('Processing settings exit')
        for tabIndex in range(self.stacked_layout.count()):
            self.stacked_layout.widget(tabIndex).save()
        # if the display of image background are changing we need to regenerate the image cache
        if 'images_config_updated' in self.processes or 'config_screen_changed' in self.processes:
            self.register_post_process('images_regenerate')
        # Now lets process all the post save handlers
        while self.processes:
            Registry().execute(self.processes.pop(0))
        return QtGui.QDialog.accept(self)

    def reject(self):
        """
        Process the form saving the settings
        """
        self.processes = []
        for tabIndex in range(self.stacked_layout.count()):
            self.stacked_layout.widget(tabIndex).cancel()
        return QtGui.QDialog.reject(self)

    def post_set_up(self):
        """
        Run any post-setup code for the tabs on the form
        """
        # General tab
        self.general_tab = GeneralTab(self)
        # Themes tab
        self.themes_tab = ThemesTab(self)
        # Advanced tab
        self.advanced_tab = AdvancedTab(self)
        # Advanced tab
        self.player_tab = PlayerTab(self)
        self.general_tab.post_set_up()
        self.themes_tab.post_set_up()
        self.advanced_tab.post_set_up()
        self.player_tab.post_set_up()
        for plugin in self.plugin_manager.plugins:
            if plugin.settings_tab:
                plugin.settings_tab.post_set_up()

    def tab_changed(self, tabIndex):
        """
        A different settings tab is selected
        """
        self.stacked_layout.setCurrentIndex(tabIndex)
        self.stacked_layout.currentWidget().tab_visible()

    def register_post_process(self, function):
        """
        Register for updates to be done on save removing duplicate functions

        ``function``
            The function to be called
        """
        if not function in self.processes:
            self.processes.append(function)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, '_main_window'):
            self._main_window = Registry().get('main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _get_service_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, '_service_manager'):
            self._service_manager = Registry().get('service_manager')
        return self._service_manager

    service_manager = property(_get_service_manager)

    def _get_plugin_manager(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, '_plugin_manager'):
            self._plugin_manager = Registry().get('plugin_manager')
        return self._plugin_manager

    plugin_manager = property(_get_plugin_manager)
