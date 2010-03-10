# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

log = logging.getLogger(__name__)

class ScreenList(object):
    """
    Wrapper to handle the parameters of the display screen
    """
    log.info(u'Screen loaded')

    def __init__(self):
        self.preview = None
        self.current = None
        self.screen_list = []
        self.count = 0
        self.current_display = 0

    def add_screen(self, screen):
        if screen[u'primary']:
            self.current = screen
        self.screen_list.append(screen)
        self.count += 1

    def screen_exists(self, number):
        for screen in self.screen_list:
            if screen[u'number'] == number:
                return True
        return False

    def set_current_display(self, number):
        if number + 1 > self.count:
            self.current = self.screen_list[0]
            self.current_display = 0
        else:
            self.current = self.screen_list[number]
            self.preview = self.current
            self.current_display = number
        if self.count == 1:
            self.preview = self.screen_list[0]

#        if self.screen[u'number'] != screenNumber:
#            # We will most probably never actually hit this bit, but just in
#            # case the index in the list doesn't match the screen number, we
#            # search for it.
#            for scrn in self.screens:
#                if scrn[u'number'] == screenNumber:
#                    self.screen = scrn
#                    break
