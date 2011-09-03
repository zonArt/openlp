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

import logging
import random
import string

from PyQt4 import QtCore
from sqlalchemy.orm import clear_mappers

from openlp.core import main as openlp_main
from openlp.core.lib.db import Manager
from openlp.plugins.songs.lib.db import init_schema

# set up logging to stderr (console)
_handler = logging.StreamHandler(stream=None)
_handler.setFormatter(logging.Formatter(
    u'%(asctime)s %(name)-55s %(levelname)-8s %(message)s'))
logging.addLevelName(15, u'Timer')
log = logging.getLogger()
log.addHandler(_handler)
log.setLevel(logging.DEBUG)


# Test function argument to make openlp gui instance persistent for all tests.
# Test cases in module have to access the same instance. To allow creating
# multiple
# instances it would be necessary use diffrent configuraion and data files.
# Created instance will use your OpenLP settings.
def pytest_funcarg__openlpapp(request):
    def setup():
        return openlp_main(['--testing'])
    def teardown(app):
        # sqlalchemy allows to map classess to only one database at a time
        clear_mappers()
    return request.cached_setup(setup=setup, teardown=teardown, scope='module')


# Test function argument to make openlp gui instance persistent for all tests.
def pytest_funcarg__empty_songs_db(request):
    def setup():
        tmpdir = request.getfuncargvalue('tmpdir')
        db_file_path = tmpdir.join('songs.sqlite')
        # unique QSettings group
        unique = ''.join(random.choice(string.letters + string.digits)
            for i in range(8))
        plugin_name = 'test_songs_%s' % unique
        settings = QtCore.QSettings()
        settings.beginGroup(plugin_name)
        settings.setValue(u'db type', QtCore.QVariant(u'sqlite'))
        settings.endGroup()
        manager = Manager(plugin_name, init_schema,
            db_file_path=db_file_path.strpath)
        return manager
    def teardown(manager):
        # sqlalchemy allows to map classess to only one database at a time
        clear_mappers()
    return request.cached_setup(setup=setup, teardown=teardown, scope='function')
