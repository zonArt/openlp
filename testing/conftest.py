#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Millar, Stevan Pettit, Andreas Preikschat, Mattias     #
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

"""
Configuration file for pytest framework.
"""

import os
import sys
import subprocess
import logging

import py.path
from PyQt4 import QtCore
from sqlalchemy.orm import clear_mappers

from openlp.core import main as openlp_main
from openlp.core.utils import AppLocation
from openlp.core.lib.db import Manager
from openlp.plugins.songs.lib.db import init_schema

TESTS_PATH = os.path.dirname(os.path.abspath(__file__))

RESOURCES_PATH = os.path.join(TESTS_PATH, 'resources')
SONGS_PATH = os.path.join(RESOURCES_PATH, 'songs')


# class to setup and teardown settings for running openlp tests
class OpenLPRunner(object):
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
        self._setup_qapp()
        self._setup_logging()
        self._cleanup_qsettings()
        # override data dir of OpenLP - it points to tmpdir of a test case
        AppLocation.BaseDir = tmpdir.strpath

    def _setup_qapp(self):
        QtCore.QCoreApplication.setOrganizationName(u'OpenLP')
        QtCore.QCoreApplication.setOrganizationDomain(u'openlp.org')
        QtCore.QCoreApplication.setApplicationName(u'TestOpenLP')

    def _setup_logging(self):
        # set up logging to stderr/stdout (console)
        _handler = logging.StreamHandler(stream=None)
        _handler.setFormatter(logging.Formatter(
            u'%(asctime)s %(name)-55s %(levelname)-8s %(message)s'))
        logging.addLevelName(15, u'Timer')
        log = logging.getLogger()
        log.addHandler(_handler)
        log.setLevel(logging.DEBUG)

    def _cleanup_qsettings(self):
        # Clean up QSettings for all plugins
        # The issue with QSettings is that is global for a running process
        # and thus it is necessary to clean it before another test case.
        # If it would not be cleaned up it could be saved in the system.
        s = QtCore.QSettings()
        keys = s.allKeys()
        for k in keys:
            s.setValue(k, None)

    ## Public interface

    def get_songs_db(self, empty=False):
        # return initialized db Manager with empty db or db containing
        # some example songs

        if not empty:
            # copy test data to tmpdir
            datadir = self.tmpdir.mkdir(u'data').mkdir(u'songs')
            orig_db = py.path.local(SONGS_PATH).join('songs.sqlite')
            orig_db.copy(datadir)

        manager = Manager('songs', init_schema)
        return manager

    def get_app(self):
        # return QGui.QApplication of OpenLP - this object allows
        # running different gui tests and allows access to gui objects
        # (e.g MainWindow etc.)
        # To allow creating multiple instances of OpenLP in one process
        # it would be necessary use diffrent configuration and data files.
        # Created instance will use your OpenLP settings.
        return openlp_main(['--testing'])

    def teardown(self):
        # clean up code to run after running the test case
        self._cleanup_qsettings()
        # sqlalchemy allows to map classess to only one database at a time
        clear_mappers()
        # set data dir to original value
        AppLocation.BaseDir = None


# Paths with resources for tests
def pytest_funcarg__pth(request):
    def setup():
        class Pth(object):
            def __init__(self):
                self.tests = py.path.local(TESTS_PATH)
                self.resources = py.path.local(RESOURCES_PATH)
                self.songs = py.path.local(SONGS_PATH)
        return Pth()
    return request.cached_setup(setup=setup, scope='session')


# Test function argument giving access to OpenLP runner
def pytest_funcarg__openlp_runner(request):
    def setup():
        return OpenLPRunner(request.getfuncargvalue('tmpdir'))
    def teardown(openlp_runner):
        openlp_runner.teardown()
    return request.cached_setup(setup=setup, teardown=teardown, scope='function')


class OpenLyricsValidator(object):
    """Validate xml if it conformns to OpenLyrics xml schema."""
    def __init__(self, script, schema):
            self.cmd = [sys.executable, script, schema]

    def validate(self, file_path):
        self.cmd.append(file_path)
        print self.cmd
        retcode = subprocess.call(self.cmd)
        if retcode == 0:
            # xml conforms to schema
            return True
        else:
            # xml has invalid syntax
            return False


# Test function argument giving access to song database.
def pytest_funcarg__openlyrics_validator(request):
    def setup():
        script = os.path.join(RESOURCES_PATH, 'openlyrics', 'validate.py')
        schema = os.path.join(RESOURCES_PATH, 'openlyrics',
            'openlyrics_schema.rng')
        return OpenLyricsValidator(script, schema)
    return request.cached_setup(setup=setup, scope='session')
