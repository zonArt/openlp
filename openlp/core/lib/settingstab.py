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
    SettingsTab is a helper widget for plugins to define Tabs for the settings
    dialog.
    """
    def __init__(self, parent, title, visible_title=None, icon_path=None):
        """
        Constructor to create the Settings tab item.

        ``title``
            The title of the tab, which is used internally for the tab handling.

        ``visible_title``
            The title of the tab, which is usually displayed on the tab.
        """
        QtGui.QWidget.__init__(self, parent)
        self.tabTitle = title
        self.tabTitleVisible = visible_title
        self.settingsSection = self.tabTitle.lower()
        if icon_path:
            self.iconPath = icon_path
        self.setupUi()
        self.retranslateUi()
        self.initialise()
        self.load()

    def setupUi(self):
        """
        Setup the tab's interface.
        """
        self.tabLayout = QtGui.QHBoxLayout(self)
        self.tabLayout.setObjectName(u'tabLayout')
        self.leftColumn = QtGui.QWidget(self)
        self.leftColumn.setObjectName(u'leftColumn')
        self.leftLayout = QtGui.QVBoxLayout(self.leftColumn)
        self.leftLayout.setMargin(0)
        self.leftLayout.setObjectName(u'leftLayout')
        self.tabLayout.addWidget(self.leftColumn)
        self.rightColumn = QtGui.QWidget(self)
        self.rightColumn.setObjectName(u'rightColumn')
        self.rightLayout = QtGui.QVBoxLayout(self.rightColumn)
        self.rightLayout.setMargin(0)
        self.rightLayout.setObjectName(u'rightLayout')
        self.tabLayout.addWidget(self.rightColumn)

    def resizeEvent(self, event=None):
        """
        Resize the sides in two equal halves if the layout allows this.
        """
        if event:
            QtGui.QWidget.resizeEvent(self, event)
        width = self.width() - self.tabLayout.spacing() - \
            self.tabLayout.contentsMargins().left() - self.tabLayout.contentsMargins().right()
        left_width = min(width - self.rightColumn.minimumSizeHint().width(), width / 2)
        left_width = max(left_width, self.leftColumn.minimumSizeHint().width())
        self.leftColumn.setFixedWidth(left_width)

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

    def postSetUp(self, postUpdate=False):
        """
        Changes which need to be made after setup of application

        ``postUpdate``
            Indicates if called before or after updates.

        """
        pass

    def tabVisible(self):
        """
        Tab has just been made visible to the user
        """
        pass

    def _get_service_manager(self):
        """
        Adds the service manager to the class dynamically
        """
        if not hasattr(self, u'_service_manager'):
            self._service_manager = Registry().get(u'service_manager')
        return self._service_manager

    service_manager = property(_get_service_manager)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)

    def _get_renderer(self):
        """
        Adds the Renderer to the class dynamically
        """
        if not hasattr(self, u'_renderer'):
            self._renderer = Registry().get(u'renderer')
        return self._renderer

    renderer = property(_get_renderer)

    def _get_theme_manager(self):
        """
        Adds the theme manager to the class dynamically
        """
        if not hasattr(self, u'_theme_manager'):
            self._theme_manager = Registry().get(u'theme_manager')
        return self._theme_manager

    theme_manager = property(_get_theme_manager)

    def _get_media_controller(self):
        """
        Adds the media controller to the class dynamically
        """
        if not hasattr(self, u'_media_controller'):
            self._media_controller = Registry().get(u'media_controller')
        return self._media_controller

    media_controller = property(_get_media_controller)

