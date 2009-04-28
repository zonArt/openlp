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
import logging

from PyQt4 import QtCore, QtGui
from openlp.core.lib import Receiver

logging.basicConfig(level=logging.DEBUG,
                format=u'%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt=u'%m-%d %H:%M',
                filename=u'openlp.log',
                filemode=u'w')

from openlp.core.resources import *
from openlp.core.ui import MainWindow, SplashScreen

class OpenLP(QtGui.QApplication):
    global log
    log=logging.getLogger(u'OpenLP Application')
    log.info(u'Application Loaded')

    def bye(self):
        print "bye"

    def run(self):
        #provide a listener for widgets to reqest a screen update.
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlpprocessevents'), self.processEvents)

        self.setApplicationName(u'openlp.org')
        self.setApplicationVersion(u'1.9.0')
        self.splash = SplashScreen(self.applicationVersion())
        self.splash.show()
        # make sure Qt really display the splash screen
        self.processEvents()
        screens = []
        # Decide how many screens we have and their size
        for screen in xrange (0 ,  self.desktop().numScreens()):
            screens.insert(screen, (screen+1, self.desktop().availableGeometry(screen+1)))
            log.info(u'Screen %d found with resolution %s', screen+1, self.desktop().availableGeometry(screen+1))
        # start the main app window
        self.main_window = MainWindow(screens)
        self.main_window.show()
        # now kill the splashscreen
        self.splash.finish(self.main_window.main_window)
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = OpenLP(sys.argv)
    app.run()

