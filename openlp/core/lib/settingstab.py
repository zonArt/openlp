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
The :mod:`~openlp.core.lib.settingstab` module contains the base SettingsTab class which plugins use for adding their
own tab to the settings dialog.
"""


from PyQt4 import QtGui


from openlp.core.lib import Registry


class SettingsTab(QtGui.QWidget):
    """
    SettingsTab is a helper widget for plugins to define Tabs for the settings dialog.
    """
    def __init__(self, parent, title, visible_title=None, icon_path=None):
        """
        Constructor to create the Settings tab item.

        ``title``
            The title of the tab, which is used internally for the tab handling.

        ``visible_title``
            The title of the tab, which is usually displayed on the tab.
        """
        super(SettingsTab, self).__init__(parent)
        self.tab_title = title
        self.tab_title_visible = visible_title
        self.settings_section = self.tab_title.lower()
        self.tab_visited = False
        if icon_path:
            self.icon_path = icon_path
        self.setupUi()
        self.retranslateUi()
        self.initialise()
        self.load()

    def setupUi(self):
        """
        Setup the tab's interface.
        """
        self.tab_layout = QtGui.QHBoxLayout(self)
        self.tab_layout.setObjectName('tab_layout')
        self.left_column = QtGui.QWidget(self)
        self.left_column.setObjectName('left_column')
        self.left_layout = QtGui.QVBoxLayout(self.left_column)
        self.left_layout.setMargin(0)
        self.left_layout.setObjectName('left_layout')
        self.tab_layout.addWidget(self.left_column)
        self.right_column = QtGui.QWidget(self)
        self.right_column.setObjectName('right_column')
        self.right_layout = QtGui.QVBoxLayout(self.right_column)
        self.right_layout.setMargin(0)
        self.right_layout.setObjectName('right_layout')
        self.tab_layout.addWidget(self.right_column)

    def resizeEvent(self, event=None):
        """
        Resize the sides in two equal halves if the layout allows this.
        """
        if event:
            QtGui.QWidget.resizeEvent(self, event)
        width = self.width() - self.tab_layout.spacing() - \
            self.tab_layout.contentsMargins().left() - self.tab_layout.contentsMargins().right()
        left_width = min(width - self.right_column.minimumSizeHint().width(), width // 2)
        left_width = max(left_width, self.left_column.minimumSizeHint().width())
        self.left_column.setFixedWidth(left_width)

    def retranslateUi(self):
        """
        Setup the interface translation strings.
        """
        pass

    def initialise(self):
        """
        Do any extra initialisation here.
        """
        pass

    def load(self):
        """
        Load settings from disk.
        """
        pass

    def save(self):
        """
        Save settings to disk.
        """
        pass

    def cancel(self):
        """
        Reset any settings if cancel triggered
        """
        self.load()

    def post_set_up(self, postUpdate=False):
        """
        Changes which need to be made after setup of application

        ``postUpdate``
            Indicates if called before or after updates.

        """
        pass

    def tab_visible(self):
        """
        Tab has just been made visible to the user
        """
        self.tab_visited = True

    def _get_service_manager(self):
        """
        Adds the service manager to the class dynamically
        """
        if not hasattr(self, '_service_manager'):
            self._service_manager = Registry().get('service_manager')
        return self._service_manager

    service_manager = property(_get_service_manager)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, '_main_window'):
            self._main_window = Registry().get('main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _get_renderer(self):
        """
        Adds the Renderer to the class dynamically
        """
        if not hasattr(self, '_renderer'):
            self._renderer = Registry().get('renderer')
        return self._renderer

    renderer = property(_get_renderer)

    def _get_theme_manager(self):
        """
        Adds the theme manager to the class dynamically
        """
        if not hasattr(self, '_theme_manager'):
            self._theme_manager = Registry().get('theme_manager')
        return self._theme_manager

    theme_manager = property(_get_theme_manager)

    def _get_media_controller(self):
        """
        Adds the media controller to the class dynamically
        """
        if not hasattr(self, '_media_controller'):
            self._media_controller = Registry().get('media_controller')
        return self._media_controller

    media_controller = property(_get_media_controller)

    def _get_settings_form(self):
        """
        Adds the plugin manager to the class dynamically
        """
        if not hasattr(self, '_settings_form'):
            self._settings_form = Registry().get('settings_form')
        return self._settings_form

    settings_form = property(_get_settings_form)
