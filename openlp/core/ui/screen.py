# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

log = logging.getLogger(__name__)

class ScreenList(object):
    """
    Wrapper to handle the parameters of the display screen
    """
    log.info(u'Screen loaded')

    def __init__(self):
        # The screen used for the rendermanager.
        # (Why does the rendermanager needs his own?)
        self.preview = None
        self.current = None
        self.override = None
        self.screen_list = []
        self.display_count = 0
        # actual display number
        self.current_display = 0
        # save config display number
        self.monitor_number = 0

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
        log.info(u'Screen %d found with resolution %s',
            screen[u'number'], screen[u'size'])
        if screen[u'primary']:
            self.current = screen
        self.screen_list.append(screen)
        self.display_count += 1

    def update_screen(self, newScreen):
        """
        Adjusts the screen's properties in the ``screen_list`` to the properties
        of the given screen.

        ``newScreen``
            A dict with the new properties of the screen::

                {
                    u'primary': True,
                    u'number': 0,
                    u'size': PyQt4.QtCore.QRect(0, 0, 1024, 768)
                }
        """
        log.info(u'update_screen %d' % newScreen[u'number'])
        for oldScreen in self.screen_list:
            if newScreen[u'number'] == oldScreen[u'number']:
                self.remove_screen(oldScreen[u'number'])
                self.add_screen(newScreen)
                # The screen's default size is used, that is why we have to
                # update the override screen.
                if oldScreen == self.override:
                    self.override = copy.deepcopy(newScreen)
                    self.set_override_display()
                break

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
            self.override = copy.deepcopy(self.current)
            self.current_display = 0
        else:
            self.current = self.screen_list[number]
            self.override = copy.deepcopy(self.current)
            self.preview = copy.deepcopy(self.current)
            self.current_display = number
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
        self.set_current_display(self.current_display)
