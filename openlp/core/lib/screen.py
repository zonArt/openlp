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
The :mod:`screen` module provides management functionality for a machines'
displays.
"""
import logging
import copy

from PyQt4 import QtCore

from openlp.core.lib import Receiver, translate

log = logging.getLogger(__name__)


class ScreenList(object):
    """
    Wrapper to handle the parameters of the display screen.

    To get access to the screen list call ``ScreenList()``.
    """
    log.info(u'Screen loaded')
    __instance__ = None

    def __new__(cls):
        """
        Re-implement __new__ to create a true singleton.
        """
        if not cls.__instance__:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    @classmethod
    def create(cls, desktop):
        """
        Initialise the screen list.

        ``desktop``
            A ``QDesktopWidget`` object.
        """
        screen_list = cls()
        screen_list.desktop = desktop
        screen_list.preview = None
        screen_list.current = None
        screen_list.override = None
        screen_list.screen_list = []
        screen_list.display_count = 0
        screen_list.screen_count_changed()
        screen_list.load_screen_settings()
        QtCore.QObject.connect(desktop, QtCore.SIGNAL(u'resized(int)'), screen_list.screen_resolution_changed)
        QtCore.QObject.connect(desktop, QtCore.SIGNAL(u'screenCountChanged(int)'), screen_list.screen_count_changed)
        return screen_list

    def screen_resolution_changed(self, number):
        """
        Called when the resolution of a screen has changed.

        ``number``
            The number of the screen, which size has changed.
        """
        log.info(u'screen_resolution_changed %d' % number)
        for screen in self.screen_list:
            if number == screen[u'number']:
                newScreen = {
                    u'number': number,
                    u'size': self.desktop.screenGeometry(number),
                    u'primary': self.desktop.primaryScreen() == number
                }
                self.remove_screen(number)
                self.add_screen(newScreen)
                # The screen's default size is used, that is why we have to
                # update the override screen.
                if screen == self.override:
                    self.override = copy.deepcopy(newScreen)
                    self.set_override_display()
                Receiver.send_message(u'config_screen_changed')
                break

    def screen_count_changed(self, changed_screen=-1):
        """
        Called when a screen has been added or removed.

        ``changed_screen``
            The screen's number which has been (un)plugged.
        """
        # Do not log at start up.
        if changed_screen != -1:
            log.info(u'screen_count_changed %d' % self.desktop.screenCount())
        # Remove unplugged screens.
        for screen in copy.deepcopy(self.screen_list):
            if screen[u'number'] == self.desktop.screenCount():
                self.remove_screen(screen[u'number'])
        # Add new screens.
        for number in xrange(self.desktop.screenCount()):
            if not self.screen_exists(number):
                self.add_screen({
                    u'number': number,
                    u'size': self.desktop.screenGeometry(number),
                    u'primary': (self.desktop.primaryScreen() == number)
                })
        # We do not want to send this message at start up.
        if changed_screen != -1:
            # Reload setting tabs to apply possible changes.
            Receiver.send_message(u'config_screen_changed')

    def get_screen_list(self):
        """
        Returns a list with the screens. This should only be used to display
        available screens to the user::

            [u'Screen 1 (primary)', u'Screen 2']
        """
        screen_list = []
        for screen in self.screen_list:
            screen_name = u'%s %d' % (translate('OpenLP.ScreenList', 'Screen'), screen[u'number'] + 1)
            if screen[u'primary']:
                screen_name = u'%s (%s)' % (screen_name, translate('OpenLP.ScreenList', 'primary'))
            screen_list.append(screen_name)
        return screen_list

    def add_screen(self, screen):
        """
        Add a screen to the list of known screens.

        ``screen``
            A dict with the screen properties::

                {
                    u'primary': True,
                    u'number': 0,
                    u'size': PyQt4.QtCore.QRect(0, 0, 1024, 768)
                }
        """
        log.info(u'Screen %d found with resolution %s', screen[u'number'], screen[u'size'])
        if screen[u'primary']:
            self.current = screen
            self.override = copy.deepcopy(self.current)
        self.screen_list.append(screen)
        self.display_count += 1

    def remove_screen(self, number):
        """
        Remove a screen from the list of known screens.

        ``number``
            The screen number (int).
        """
        log.info(u'remove_screen %d' % number)
        for screen in self.screen_list:
            if screen[u'number'] == number:
                self.screen_list.remove(screen)
                self.display_count -= 1
                break

    def screen_exists(self, number):
        """
        Confirms a screen is known.

        ``number``
            The screen number (int).
        """
        for screen in self.screen_list:
            if screen[u'number'] == number:
                return True
        return False

    def set_current_display(self, number):
        """
        Set up the current screen dimensions.

        ``number``
            The screen number (int).
        """
        log.debug(u'set_current_display %s', number)
        if number + 1 > self.display_count:
            self.current = self.screen_list[0]
        else:
            self.current = self.screen_list[number]
            self.preview = copy.deepcopy(self.current)
        self.override = copy.deepcopy(self.current)
        if self.display_count == 1:
            self.preview = self.screen_list[0]

    def set_override_display(self):
        """
        Replace the current size with the override values, as the user wants to
        have their own screen attributes.
        """
        log.debug(u'set_override_display')
        self.current = copy.deepcopy(self.override)
        self.preview = copy.deepcopy(self.current)

    def reset_current_display(self):
        """
        Replace the current values with the correct values, as the user wants to
        use the correct screen attributes.
        """
        log.debug(u'reset_current_display')
        self.set_current_display(self.current[u'number'])

    def which_screen(self, window):
        """
        Return the screen number that the centre of the passed window is in.

        ``window``
            A QWidget we are finding the location of.
        """
        x = window.x() + (window.width() / 2)
        y = window.y() + (window.height() / 2)
        for screen in self.screen_list:
            size = screen[u'size']
            if x >= size.x() and x <= (size.x() + size.width()) and y >= size.y() and y <= (size.y() + size.height()):
                return screen[u'number']

    def load_screen_settings(self):
        """
        Loads the screen size and the monitor number from the settings.
        """
        from openlp.core.lib import Settings
        # Add the screen settings to the settings dict. This has to be done here due to crycle dependency.
        # Do not do this anywhere else.
        screen_settings = {
            u'general/x position': self.current[u'size'].x(),
            u'general/y position': self.current[u'size'].y(),
            u'general/monitor': self.display_count - 1,
            u'general/height': self.current[u'size'].height(),
            u'general/width': self.current[u'size'].width()
        }
        Settings.extend_default_settings(screen_settings)
        settings = Settings()
        settings.beginGroup(u'general')
        monitor = settings.value(u'monitor')
        self.set_current_display(monitor)
        self.display = settings.value(u'display on monitor')
        override_display = settings.value(u'override position')
        x = settings.value(u'x position')
        y = settings.value(u'y position')
        width = settings.value(u'width')
        height = settings.value(u'height')
        self.override[u'size'] = QtCore.QRect(x, y, width, height)
        self.override[u'primary'] = False
        settings.endGroup()
        if override_display:
            self.set_override_display()
        else:
            self.reset_current_display()
