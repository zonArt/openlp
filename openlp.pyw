#!/usr/bin/env python
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

import os
import sys
import logging

from logging.handlers import RotatingFileHandler
from optparse import OptionParser
from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, str_to_bool
from openlp.core.resources import qInitResources
from openlp.core.ui import MainWindow, SplashScreen, ScreenList
from openlp.core.utils import ConfigHelper

log = logging.getLogger()

application_stylesheet = u"""
QMainWindow::separator
{
  border: none;
}

QDockWidget::title
{
  border: none;
  padding-left: 5px;
  padding-top: 3px;
}

QToolBar
{
  border: none;
  margin: 0;
  padding: 0;
}
"""

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
        #Load and store current Application Version
        filepath = os.path.split(os.path.abspath(__file__))[0]
        filepath = os.path.abspath(os.path.join(filepath, u'version.txt'))
        fversion = None
        try:
            fversion = open(filepath, u'r')
            for line in fversion:
                full_version = unicode(line).rstrip() #\
                    #.replace(u'\r', u'').replace(u'\n', u'')
                bits = full_version.split(u'-')
                app_version = {
                    u'full': full_version,
                    u'version': bits[0],
                    u'build': bits[1]
                }
            log.info(u'Openlp version %s build %s' % (
                app_version[u'version'], app_version[u'build']))
        except:
                app_version = {
                    u'full': u'1.9.0-000',
                    u'version': u'1.9.0',
                    u'build': u'000'
                }
        finally:
            if fversion:
                fversion.close()
        #set the default string encoding
        try:
            sys.setappdefaultencoding(u'utf-8')
        except:
            pass
        #provide a listener for widgets to reqest a screen update.
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'process_events'), self.processEvents)
        self.setApplicationName(u'OpenLP')
        self.setApplicationVersion(app_version[u'version'])
        if os.name == u'nt':
            self.setStyleSheet(application_stylesheet)
        show_splash = str_to_bool(ConfigHelper.get_registry().get_value(
            u'general', u'show splash', True))
        if show_splash:
            self.splash = SplashScreen(self.applicationVersion())
            self.splash.show()
        # make sure Qt really display the splash screen
        self.processEvents()
        screens = ScreenList()
        # Decide how many screens we have and their size
        for screen in xrange(0, self.desktop().numScreens()):
            screens.add_screen({u'number': screen,
                            u'size': self.desktop().availableGeometry(screen),
                            u'primary': (self.desktop().primaryScreen() == screen)})
            log.info(u'Screen %d found with resolution %s',
                screen, self.desktop().availableGeometry(screen))
        # start the main app window
        self.mainWindow = MainWindow(screens, app_version)
        self.mainWindow.show()
        if show_splash:
            # now kill the splashscreen
            self.splash.finish(self.mainWindow)
        self.mainWindow.versionCheck()
        return self.exec_()

def main():
    """
    The main function which parses command line options and then runs
    the PyQt4 Application.
    """
    # Set up command line options.
    usage = u'Usage: %prog [options] [qt-options]'
    parser = OptionParser(usage=usage)
    parser.add_option("-l", "--log-level", dest="loglevel",
                      default="info", metavar="LEVEL",
                      help="Set logging to LEVEL level. Valid values are "
                           "\"debug\", \"info\", \"warning\".")
    parser.add_option("-p", "--portable", dest="portable",
                      action="store_true",
                      help="Specify if this should be run as a portable app, "
                           "off a USB flash drive.")
    parser.add_option("-s", "--style", dest="style",
                      help="Set the Qt4 style (passed directly to Qt4).")
    # Set up logging
    filename = u'openlp.log'
    logfile = RotatingFileHandler(filename, maxBytes=200000, backupCount=5)
    logfile.setFormatter(logging.Formatter(
        u'%(asctime)s %(name)-15s %(levelname)-8s %(message)s'))
    log.addHandler(logfile)
    logging.addLevelName(15, u'Timer')
    # Parse command line options and deal with them.
    (options, args) = parser.parse_args()
    qt_args = []
    if options.loglevel.lower() in ['d', 'debug']:
        log.setLevel(logging.DEBUG)
    elif options.loglevel.lower() in ['w', 'warning']:
        log.setLevel(logging.WARNING)
    else:
        log.setLevel(logging.INFO)
    if options.style:
        qt_args.extend(['-style', options.style])
    # Throw the rest of the arguments at Qt, just in case.
    qt_args.extend(args)
    # Initialise the resources
    qInitResources()
    # Now create and actually run the application.
    app = OpenLP(qt_args)
    sys.exit(app.run())

if __name__ == u'__main__':
    """
    Instantiate and run the application.
    """
    main()
