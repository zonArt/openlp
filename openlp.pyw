#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin Köhler,        #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
# Import uuid now, to avoid the rare bug described in the support system:
# http://support.openlp.org/issues/102
# If https://bugs.gentoo.org/show_bug.cgi?id=317557 is fixed, the import can be
# removed.
import uuid
from optparse import OptionParser
from traceback import format_exception

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, check_directory_exists
from openlp.core.lib.ui import UiStrings
from openlp.core.resources import qInitResources
from openlp.core.ui.mainwindow import MainWindow
from openlp.core.ui.firsttimelanguageform import FirstTimeLanguageForm
from openlp.core.ui.firsttimeform import FirstTimeForm
from openlp.core.ui.exceptionform import ExceptionForm
from openlp.core.ui import SplashScreen, ScreenList
from openlp.core.utils import AppLocation, LanguageManager, VersionThread, \
    get_application_version, DelayStartThread

log = logging.getLogger()

application_stylesheet = u"""
QMainWindow::separator
{
  border: none;
}

QDockWidget::title
{
  border: 1px solid palette(dark);
  padding-left: 5px;
  padding-top: 2px;
  margin: 1px 0;
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

    def exec_(self):
        """
        Override exec method to allow the shared memory to be released on exit
        """
        QtGui.QApplication.exec_()
        self.sharedMemory.detach()

    def run(self):
        """
        Run the OpenLP application.
        """
        # provide a listener for widgets to reqest a screen update.
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_process_events'), self.processEvents)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'cursor_busy'), self.setBusyCursor)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'cursor_normal'), self.setNormalCursor)
        # Decide how many screens we have and their size
        screens = ScreenList(self.desktop())
        # First time checks in settings
        has_run_wizard = QtCore.QSettings().value(
            u'general/has run wizard', QtCore.QVariant(False)).toBool()
        if not has_run_wizard:
            if FirstTimeForm(screens).exec_() == QtGui.QDialog.Accepted:
                QtCore.QSettings().setValue(u'general/has run wizard',
                    QtCore.QVariant(True))
        if os.name == u'nt':
            self.setStyleSheet(application_stylesheet)
        show_splash = QtCore.QSettings().value(
            u'general/show splash', QtCore.QVariant(True)).toBool()
        if show_splash:
            self.splash = SplashScreen()
            self.splash.show()
        # make sure Qt really display the splash screen
        self.processEvents()
        # start the main app window
        self.mainWindow = MainWindow(self.clipboard(), self.arguments())
        self.mainWindow.show()
        if show_splash:
            # now kill the splashscreen
            self.splash.finish(self.mainWindow)
            log.debug(u'Splashscreen closed')
        self.mainWindow.repaint()
        self.processEvents()
        if not has_run_wizard:
            self.mainWindow.firstTime()
        update_check = QtCore.QSettings().value(
            u'general/update check', QtCore.QVariant(True)).toBool()
        if update_check:
            VersionThread(self.mainWindow).start()
        DelayStartThread(self.mainWindow).start()
        return self.exec_()

    def isAlreadyRunning(self):
        """
        Look to see if OpenLP is already running and ask if a 2nd copy
        is to be started.
        """
        self.sharedMemory = QtCore.QSharedMemory('OpenLP')
        if self.sharedMemory.attach():
            status = QtGui.QMessageBox.critical(None,
                UiStrings().Error, UiStrings().OpenLPStart,
                QtGui.QMessageBox.StandardButtons(
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No))
            if status == QtGui.QMessageBox.No:
                return True
            return False
        else:
            self.sharedMemory.create(1)
            return False

    def hookException(self, exctype, value, traceback):
        if not hasattr(self, u'mainWindow'):
            log.exception(''.join(format_exception(exctype, value, traceback)))
            return
        if not hasattr(self, u'exceptionForm'):
            self.exceptionForm = ExceptionForm(self.mainWindow)
        self.exceptionForm.exceptionTextEdit.setPlainText(
            ''.join(format_exception(exctype, value, traceback)))
        self.setNormalCursor()
        self.exceptionForm.exec_()

    def setBusyCursor(self):
        """
        Sets the Busy Cursor for the Application
        """
        self.setOverrideCursor(QtCore.Qt.BusyCursor)
        self.processEvents()

    def setNormalCursor(self):
        """
        Sets the Normal Cursor for the Application
        """
        self.restoreOverrideCursor()

def main():
    """
    The main function which parses command line options and then runs
    the PyQt4 Application.
    """
    # Set up command line options.
    usage = 'Usage: %prog [options] [qt-options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-e', '--no-error-form', dest='no_error_form',
        action='store_true', help='Disable the error notification form.')
    parser.add_option('-l', '--log-level', dest='loglevel',
        default='warning', metavar='LEVEL', help='Set logging to LEVEL '
        'level. Valid values are "debug", "info", "warning".')
    parser.add_option('-p', '--portable', dest='portable',
        action='store_true', help='Specify if this should be run as a '
        'portable app, off a USB flash drive (not implemented).')
    parser.add_option('-d', '--dev-version', dest='dev_version',
        action='store_true', help='Ignore the version file and pull the '
        'version directly from Bazaar')
    parser.add_option('-s', '--style', dest='style',
        help='Set the Qt4 style (passed directly to Qt4).')
    # Set up logging
    log_path = AppLocation.get_directory(AppLocation.CacheDir)
    check_directory_exists(log_path)
    filename = os.path.join(log_path, u'openlp.log')
    logfile = logging.FileHandler(filename, u'w')
    logfile.setFormatter(logging.Formatter(
        u'%(asctime)s %(name)-55s %(levelname)-8s %(message)s'))
    log.addHandler(logfile)
    logging.addLevelName(15, u'Timer')
    # Parse command line options and deal with them.
    (options, args) = parser.parse_args()
    qt_args = []
    if options.loglevel.lower() in ['d', 'debug']:
        log.setLevel(logging.DEBUG)
        print 'Logging to:', filename
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
    # Instance check
    if app.isAlreadyRunning():
        sys.exit()
    app.setOrganizationName(u'OpenLP')
    app.setOrganizationDomain(u'openlp.org')
    app.setApplicationName(u'OpenLP')
    app.setApplicationVersion(get_application_version()[u'version'])
    # First time checks in settings
    if not QtCore.QSettings().value(u'general/has run wizard',
        QtCore.QVariant(False)).toBool():
        if not FirstTimeLanguageForm().exec_():
            # if cancel then stop processing
            sys.exit()
    if sys.platform == u'darwin':
        OpenLP.addLibraryPath(QtGui.QApplication.applicationDirPath()
            + "/qt4_plugins")
    # i18n Set Language
    language = LanguageManager.get_language()
    app_translator, default_translator = \
        LanguageManager.get_translator(language)
    if not app_translator.isEmpty():
        app.installTranslator(app_translator)
    if not default_translator.isEmpty():
        app.installTranslator(default_translator)
    else:
        log.debug(u'Could not find default_translator.')
    if not options.no_error_form:
        sys.excepthook = app.hookException
    sys.exit(app.run())

if __name__ == u'__main__':
    """
    Instantiate and run the application.
    """
    main()
