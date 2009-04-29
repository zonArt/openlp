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

    def __init__(self, screens, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.setWindowTitle(u'OpenLP Display')
            self.screens = screens
            self.imagesize = screens[0][1]
            self.display = QtGui.QLabel(self)
            #self.showMinimized()

    def initialView(self):
            self.display.setGeometry((self.imagesize.width()-429)/2, (self.imagesize.height()-429)/2, 429, 429)
            self.display.setPixmap(QtGui.QPixmap("openlp2.png"))
            self.showMaximized()
            print len(self.screens)
            print self.isEnabled()
            print self.isVisible()
            print self.geometry()
            #if len(self.screens) > 0:
            self.showFullScreen()
            self.show()

    def frameView(self, frame):
            self.display.setGeometry(0, 0, imagesize.width(), imagesize.height())
            self.display.setPixmap(QtGui.QPixmap(frame))

    def kill(self):
        pass



