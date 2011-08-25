#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
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

from openlp.core import OpenLP
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
    sys.exit(app.run(qt_args))

if __name__ == u'__main__':
    """
    Instantiate and run the application.
    """
    main()
