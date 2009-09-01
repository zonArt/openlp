#!/usr/bin/env python
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

import sys
import logging, logging.handlers
from optparse import OptionParser

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver
from openlp.core.resources import *
from openlp.core.ui import MainWindow, SplashScreen

filename=u'openlp.log'
log = logging.getLogger()
log.setLevel(logging.INFO)

logfile = logging.handlers.RotatingFileHandler(filename ,maxBytes=200000, backupCount=5)
logfile.setLevel(logging.DEBUG)
logfile.setFormatter(logging.Formatter(u'%(asctime)s %(name)-15s %(levelname)-8s %(message)s'))

log.addHandler(logfile)

class OpenLP(QtGui.QApplication):
    """
    The core application class. This class inherits from Qt's QApplication
    class in order to provide the core of the application.
    """
    global log
    log.info(u'OpenLP Application Loaded')

    def run(self):
        """
        Run the OpenLP application.
        """
        #set the default string encoding
        try:
            sys.setappdefaultencoding(u'utf-8')
        except:
            pass
        #provide a listener for widgets to reqest a screen update.
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'process_events'), self.processEvents)
        self.setApplicationName(u'openlp.org')
        self.setApplicationVersion(u'1.9.0')
        self.splash = SplashScreen(self.applicationVersion())
        self.splash.show()
        # make sure Qt really display the splash screen
        self.processEvents()
        screens = []
        # Decide how many screens we have and their size
        for screen in xrange(0, self.desktop().numScreens()):
            screens.append({u'number': screen,
                            u'size': self.desktop().availableGeometry(screen),
                            u'primary': (self.desktop().primaryScreen() == screen)})
            log.info(u'Screen %d found with resolution %s',
                screen, self.desktop().availableGeometry(screen))
        # start the main app window
        self.mainWindow = MainWindow(screens)
        self.mainWindow.show()
        # now kill the splashscreen
        self.splash.finish(self.mainWindow)
        sys.exit(app.exec_())

def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--debug",dest="debug",action="store_true",
                      help="Switch on Debugging ")
    (options, args) = parser.parse_args()
    if options.debug is not None:
        log.setLevel(logging.DEBUG)
if __name__ == u'__main__':
    """
    Instantiate and run the application.
    """
    main()
    app = OpenLP(sys.argv)
    #import cProfile
    #cProfile.run("app.run()", "profile.out")
    app.run()
