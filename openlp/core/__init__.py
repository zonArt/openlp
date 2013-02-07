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
The :mod:`core` module provides all core application functions

All the core functions of the OpenLP application including the GUI, settings,
logging and a plugin framework are contained within the openlp.core module.
"""

import os
import sys
import platform
import logging
from optparse import OptionParser
from traceback import format_exception

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, Settings, ScreenList, UiStrings, Registry, check_directory_exists
from openlp.core.resources import qInitResources
from openlp.core.ui.mainwindow import MainWindow
from openlp.core.ui.firsttimelanguageform import FirstTimeLanguageForm
from openlp.core.ui.firsttimeform import FirstTimeForm
from openlp.core.ui.exceptionform import ExceptionForm
from openlp.core.ui import SplashScreen
from openlp.core.utils import AppLocation, LanguageManager, VersionThread, get_application_version


__all__ = [u'OpenLP', u'main']


log = logging.getLogger()
nt_repair_stylesheet = u"""
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

    args = []

    def exec_(self):
        """
        Override exec method to allow the shared memory to be released on exit
        """
        self.is_event_loop_active = True
        result = QtGui.QApplication.exec_()
        self.shared_memory.detach()
        return result

    def run(self, args):
        """
        Run the OpenLP application.
        """
        self.is_event_loop_active = False
        # On Windows, the args passed into the constructor are ignored. Not
        # very handy, so set the ones we want to use. On Linux and FreeBSD, in
        # order to set the WM_CLASS property for X11, we pass "OpenLP" in as a
        # command line argument. This interferes with files being passed in as
        # command line arguments, so we remove it from the list.
        if 'OpenLP' in args:
            args.remove('OpenLP')
        self.args.extend(args)
        # Decide how many screens we have and their size
        screens = ScreenList.create(self.desktop())
        # First time checks in settings
        has_run_wizard = Settings().value(u'general/has run wizard')
        if not has_run_wizard:
            if FirstTimeForm(screens).exec_() == QtGui.QDialog.Accepted:
                Settings().setValue(u'general/has run wizard', True)
        # Correct stylesheet bugs
        application_stylesheet = u''
        if not Settings().value(u'advanced/alternate rows'):
            base_color = self.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Base)
            alternate_rows_repair_stylesheet = \
                u'QTableWidget, QListWidget, QTreeWidget {alternate-background-color: ' + base_color.name() + ';}\n'
            application_stylesheet += alternate_rows_repair_stylesheet
        if os.name == u'nt':
            application_stylesheet += nt_repair_stylesheet
        if application_stylesheet:
            self.setStyleSheet(application_stylesheet)
        show_splash = Settings().value(u'general/show splash')
        if show_splash:
            self.splash = SplashScreen()
            self.splash.show()
        # make sure Qt really display the splash screen
        self.processEvents()
        # start the main app window
        self.main_window = MainWindow()
        self.main_window.show()
        if show_splash:
            # now kill the splashscreen
            self.splash.finish(self.main_window)
            log.debug(u'Splashscreen closed')
        # make sure Qt really display the splash screen
        self.processEvents()
        self.main_window.repaint()
        self.processEvents()
        if not has_run_wizard:
            self.main_window.first_time()
        update_check = Settings().value(u'general/update check')
        if update_check:
            VersionThread(self.main_window).start()
        Receiver.send_message(u'live_display_blank_check')
        self.main_window.app_startup()
        return self.exec_()

    def close_splash_screen(self):
        """
        Close the splash screen when requested.
        """
        self.splash.close()

    def is_already_running(self):
        """
        Look to see if OpenLP is already running and ask if a 2nd copy
        is to be started.
        """
        self.shared_memory = QtCore.QSharedMemory('OpenLP')
        if self.shared_memory.attach():
            status = QtGui.QMessageBox.critical(None, UiStrings().Error, UiStrings().OpenLPStart,
                QtGui.QMessageBox.StandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No))
            if status == QtGui.QMessageBox.No:
                return True
            return False
        else:
            self.shared_memory.create(1)
            return False

    def hook_exception(self, exctype, value, traceback):
        """
        Add an exception hook so that any uncaught exceptions are displayed in this window rather than somewhere where
        users cannot see it and cannot report when we encounter these problems.

        ``exctype``
            The class of exception.

        ``value``
            The actual exception object.

        ``traceback``
            A traceback object with the details of where the exception occurred.
        """
        if not hasattr(self, u'mainWindow'):
            log.exception(''.join(format_exception(exctype, value, traceback)))
            return
        if not hasattr(self, u'exceptionForm'):
            self.exception_form = ExceptionForm(self.main_window)
        self.exception_form.exceptionTextEdit.setPlainText(''.join(format_exception(exctype, value, traceback)))
        self.set_normal_cursor()
        self.exception_form.exec_()

    def process_events(self):
        """
        Wrapper to make ProcessEvents visible and named correctly
        """
        self.processEvents()

    def set_busy_cursor(self):
        """
        Sets the Busy Cursor for the Application
        """
        self.setOverrideCursor(QtCore.Qt.BusyCursor)
        self.processEvents()

    def set_normal_cursor(self):
        """
        Sets the Normal Cursor for the Application
        """
        self.restoreOverrideCursor()
        self.processEvents()

    def event(self, event):
        """
        Enables direct file opening on OS X
        """
        if event.type() == QtCore.QEvent.FileOpen:
            file_name = event.file()
            log.debug(u'Got open file event for %s!', file_name)
            self.args.insert(0, file_name)
            return True
        else:
            return QtGui.QApplication.event(self, event)


def set_up_logging(log_path):
    """
    Setup our logging using log_path
    """
    check_directory_exists(log_path, True)
    filename = os.path.join(log_path, u'openlp.log')
    logfile = logging.FileHandler(filename, u'w')
    logfile.setFormatter(logging.Formatter(u'%(asctime)s %(name)-55s %(levelname)-8s %(message)s'))
    log.addHandler(logfile)
    if log.isEnabledFor(logging.DEBUG):
        print('Logging to: %s' % filename)


def main(args=None):
    """
    The main function which parses command line options and then runs
    the PyQt4 Application.
    """
    # Set up command line options.
    usage = 'Usage: %prog [options] [qt-options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-e', '--no-error-form', dest='no_error_form', action='store_true',
        help='Disable the error notification form.')
    parser.add_option('-l', '--log-level', dest='loglevel', default='warning', metavar='LEVEL',
        help='Set logging to LEVEL level. Valid values are "debug", "info", "warning".')
    parser.add_option('-p', '--portable', dest='portable', action='store_true',
        help='Specify if this should be run as a portable app, off a USB flash drive (not implemented).')
    parser.add_option('-d', '--dev-version', dest='dev_version', action='store_true',
        help='Ignore the version file and pull the version directly from Bazaar')
    parser.add_option('-s', '--style', dest='style', help='Set the Qt4 style (passed directly to Qt4).')
    # Parse command line options and deal with them.
    # Use args supplied programatically if possible.
    (options, args) = parser.parse_args(args) if args else parser.parse_args()
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
    # Bug #1018855: Set the WM_CLASS property in X11
    if platform.system() not in ['Windows', 'Darwin']:
        qt_args.append('OpenLP')
    # Initialise the resources
    qInitResources()
    # Now create and actually run the application.
    application = OpenLP(qt_args)
    application.setOrganizationName(u'OpenLP')
    application.setOrganizationDomain(u'openlp.org')
    if options.portable:
        application.setApplicationName(u'OpenLPPortable')
        Settings.setDefaultFormat(Settings.IniFormat)
        # Get location OpenLPPortable.ini
        application_path = AppLocation.get_directory(AppLocation.AppDir)
        set_up_logging(os.path.abspath(os.path.join(application_path, u'..', u'..', u'Other')))
        log.info(u'Running portable')
        portable_settings_file = os.path.abspath(os.path.join(application_path, u'..', u'..', u'Data', u'OpenLP.ini'))
        # Make this our settings file
        log.info(u'INI file: %s', portable_settings_file)
        Settings.set_filename(portable_settings_file)
        portable_settings = Settings()
        # Set our data path
        data_path = os.path.abspath(os.path.join(application_path, u'..', u'..', u'Data',))
        log.info(u'Data path: %s', data_path)
        # Point to our data path
        portable_settings.setValue(u'advanced/data path', data_path)
        portable_settings.setValue(u'advanced/is portable', True)
        portable_settings.sync()
    else:
        application.setApplicationName(u'OpenLP')
        set_up_logging(AppLocation.get_directory(AppLocation.CacheDir))
    Registry.create()
    Registry().register(u'application', application)
    application.setApplicationVersion(get_application_version()[u'version'])
    # Instance check
    if application.is_already_running():
        sys.exit()
    # First time checks in settings
    if not Settings().value(u'general/has run wizard'):
        if not FirstTimeLanguageForm().exec_():
            # if cancel then stop processing
            sys.exit()
    # i18n Set Language
    language = LanguageManager.get_language()
    application_translator, default_translator = LanguageManager.get_translator(language)
    if not application_translator.isEmpty():
        application.installTranslator(application_translator)
    if not default_translator.isEmpty():
        application.installTranslator(default_translator)
    else:
        log.debug(u'Could not find default_translator.')
    if not options.no_error_form:
        sys.excepthook = application.hook_exception
    sys.exit(application.run(qt_args))

