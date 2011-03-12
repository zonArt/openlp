#!/usr/bin/env python
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
import os
import sys
import logging
from optparse import OptionParser
from traceback import format_exception
from subprocess import Popen, PIPE

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver, check_directory_exists
from openlp.core.resources import qInitResources
from openlp.core.ui.mainwindow import MainWindow
from openlp.core.ui.firsttimelanguageform import FirstTimeLanguageForm
from openlp.core.ui.firsttimeform import FirstTimeForm
from openlp.core.ui.exceptionform import ExceptionForm
from openlp.core.ui import SplashScreen, ScreenList
from openlp.core.utils import AppLocation, LanguageManager, VersionThread

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
    log.info(u'OpenLP Application Loaded')

    def _get_version(self):
        """
        Load and store current Application Version
        """
        if u'--dev-version' in sys.argv or u'-d' in sys.argv:
            # If we're running the dev version, let's use bzr to get the version
            try:
                # If bzrlib is availble, use it
                from bzrlib.branch import Branch
                b = Branch.open_containing('.')[0]
                b.lock_read()
                try:
                    # Get the branch's latest revision number.
                    revno = b.revno()
                    # Convert said revision number into a bzr revision id.
                    revision_id = b.dotted_revno_to_revision_id((revno,))
                    # Get a dict of tags, with the revision id as the key.
                    tags = b.tags.get_reverse_tag_dict()
                    # Check if the latest
                    if revision_id in tags:
                        full_version = u'%s' % tags[revision_id][0]
                    else:
                        full_version = '%s-bzr%s' % \
                            (sorted(b.tags.get_tag_dict().keys())[-1], revno)
                finally:
                    b.unlock()
            except:
                # Otherwise run the command line bzr client
                bzr = Popen((u'bzr', u'tags', u'--sort', u'time'), stdout=PIPE)
                output, error = bzr.communicate()
                code = bzr.wait()
                if code != 0:
                    raise Exception(u'Error running bzr tags')
                lines = output.splitlines()
                if len(lines) == 0:
                    tag = u'0.0.0'
                    revision = u'0'
                else:
                    tag, revision = lines[-1].split()
                bzr = Popen((u'bzr', u'log', u'--line', u'-r', u'-1'),
                    stdout=PIPE)
                output, error = bzr.communicate()
                code = bzr.wait()
                if code != 0:
                    raise Exception(u'Error running bzr log')
                latest = output.split(u':')[0]
                full_version = latest == revision and tag or \
                    u'%s-bzr%s' % (tag, latest)
        else:
            # We're not running the development version, let's use the file
            filepath = AppLocation.get_directory(AppLocation.VersionDir)
            filepath = os.path.join(filepath, u'.version')
            fversion = None
            try:
                fversion = open(filepath, u'r')
                full_version = unicode(fversion.read()).rstrip()
            except IOError:
                log.exception('Error in version file.')
                full_version = u'0.0.0-bzr000'
            finally:
                if fversion:
                    fversion.close()
        bits = full_version.split(u'-')
        app_version = {
            u'full': full_version,
            u'version': bits[0],
            u'build': bits[1] if len(bits) > 1 else None
        }
        if app_version[u'build']:
            log.info(
                u'Openlp version %s build %s',
                app_version[u'version'],
                app_version[u'build']
            )
        else:
            log.info(u'Openlp version %s' % app_version[u'version'])
        return app_version

    def run(self):
        """
        Run the OpenLP application.
        """
        app_version = self._get_version()
        # provide a listener for widgets to reqest a screen update.
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'openlp_process_events'), self.processEvents)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'cursor_busy'), self.setBusyCursor)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'cursor_normal'), self.setNormalCursor)
        self.setOrganizationName(u'OpenLP')
        self.setOrganizationDomain(u'openlp.org')
        self.setApplicationName(u'OpenLP')
        self.setApplicationVersion(app_version[u'version'])
        # Decide how many screens we have and their size
        screens = ScreenList(self.desktop())
        # First time checks in settings
        has_run_wizard = QtCore.QSettings().value(
            u'general/has run wizard', QtCore.QVariant(False)).toBool()
        if not has_run_wizard:
            FirstTimeForm(screens).exec_()
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
        self.mainWindow = MainWindow(screens, app_version, self.clipboard(),
            has_run_wizard)
        self.mainWindow.show()
        if show_splash:
            # now kill the splashscreen
            self.splash.finish(self.mainWindow)
        self.mainWindow.repaint()
        update_check = QtCore.QSettings().value(
            u'general/update check', QtCore.QVariant(True)).toBool()
        if update_check:
            VersionThread(self.mainWindow, app_version).start()
        return self.exec_()

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
    # Define the settings environment
    settings = QtCore.QSettings(u'OpenLP', u'OpenLP')
    # First time checks in settings
    # Use explicit reference as not inside a QT environment yet
    if not settings.value(u'general/has run wizard',
        QtCore.QVariant(False)).toBool():
        if not FirstTimeLanguageForm().exec_():
            # if cancel then stop processing
            sys.exit()
    if sys.platform == u'darwin':
        OpenLP.addLibraryPath(QtGui.QApplication.applicationDirPath()
            + "/qt4_plugins")
    # i18n Set Language
    language = LanguageManager.get_language()
    appTranslator = LanguageManager.get_translator(language)
    app.installTranslator(appTranslator)
    if not options.no_error_form:
        sys.excepthook = app.hookException
    sys.exit(app.run())

if __name__ == u'__main__':
    """
    Instantiate and run the application.
    """
    main()
