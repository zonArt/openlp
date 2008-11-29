#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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

import sys
from PyQt4 import QtCore, QtGui

from openlp.core.resources import *
from openlp.core.ui import MainWindow, SplashScreen

class OpenLP(QtGui.QApplication):

    def run(self):
        self.splash = SplashScreen()
        self.splash.show()
        # make sure Qt really display the splash screen
        self.processEvents()
        # start tha main app window
        self.main_window = MainWindow()
        self.main_window.show()
        # now kill the splashscreen
        self.splash.finish(self.main_window.main_window)
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = OpenLP(sys.argv)
    app.run()
