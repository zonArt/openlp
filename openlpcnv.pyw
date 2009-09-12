#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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
import time
import datetime

from openlp.migration.display import *
from openlp.migration.migratefiles import *
from openlp.migration.migratebibles import *
from openlp.migration.migratesongs import *

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='openlp-migration.log',
                filemode='w')

class Migration(object):
    """
    A class to take care of the migration process.
    """
    def __init__(self):
        """
        Initialise the process.
        """
        self.display = Display()
        self.stime =  time.strftime(u'%Y-%m-%d-%H%M%S', time.localtime())
        self.display.output(u'OpenLp v1.9.0 Migration Utility Started')

    def process(self):
        """
        Perform the conversion.
        """
        #MigrateFiles(self.display).process()
        MigrateSongs(self.display).process()
        #MigrateBibles(self.display).process()

    def move_log_file(self):
        """
        Move the log file to a new location.
        """
        fname = 'openlp-migration.log'
        c = os.path.splitext(fname)
        b = (c[0]+'-'+ unicode(self.stime) + c[1])
        self.display.output(u'Logfile " +b + " generated')
        self.display.output(u'Migration Utility Finished ')
        os.rename(fname, b)


if __name__ == '__main__':
    mig = Migration()
    mig.process()
    #mig.move_log_file()
