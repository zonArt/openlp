#!/usr/bin/env python

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

class Migration():
    def __init__(self):
        """
        """
        self.display = Display()
        self.stime =  time.strftime(u'%Y-%m-%d-%H%M%S', time.localtime())
        self.display.output(u'OpenLp v1.9.0 Migration Utility Started')

    def process(self):
        #MigrateFiles(self.display).process()
        MigrateSongs(self.display).process()
        #MigrateBibles(self.display).process()

    def move_log_file(self):
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
