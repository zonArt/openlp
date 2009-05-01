# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

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

from PyQt4 import QtCore, QtGui

from openlp.core import translate

class MainDisplay(QtGui.QWidget):

    def __init__(self, parent, screens):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle(u'OpenLP Display')
        self.screens = screens
        self.display = QtGui.QLabel(self)

    def setup(self, screenNumber):
        """
        Sets up the screen on a particular screen.
        @param (integer) screen This is the screen number.
        """
        screen = self.screens[screenNumber]
        if screen['number'] != screenNumber:
            # We will most probably never actually hit this bit, but just in
            # case the index in the list doesn't match the screen number, we
            # search for it.
            for scrn in self.screens:
                if scrn['number'] == screenNumber:
                    screen = scrn
                    break
        self.setGeometry(screen['size'])
        if not screen['primary']:
            self.showFullScreen()
        else:
            self.hide()

    def frameView(self, frame):
        self.display.setGeometry(0, 0, imagesize.width(), imagesize.height())
        self.display.setPixmap(QtGui.QPixmap(frame))

    def kill(self):
        pass
