from openlp.plugins.songs.lib.opensongimport import OpenSongImport
from openlp.plugins.songs.lib.db import init_schema
from openlp.core.lib.db import Manager
from glob import glob
from zipfile import ZipFile
import os
from traceback import print_exc
import sys
import codecs

import logging
LOG_FILENAME = 'import.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

from test_opensongimport import wizard_stub, progbar_stub
def opensong_import_lots():
    ziploc = u'/home/mjt/openlp/OpenSong_Data/'
    files = []
    #files = [u'test.opensong.zip', ziploc+u'ADond.zip']
    # files.extend(glob(ziploc+u'Songs.zip'))
    files.extend(glob(ziploc+u'RaoulSongs.zip'))
    #files.extend(glob(ziploc+u'SOF.zip'))
    #files.extend(glob(ziploc+u'spanish_songs_for_opensong.zip'))
#    files.extend(glob(ziploc+u'opensong_*.zip'))
    errfile = codecs.open(u'import_lots_errors.txt', u'w', u'utf8')
    manager = Manager(u'songs', init_schema)
    o = OpenSongImport(manager, filenames=files)
    o.import_wizard=wizard_stub()
    o.do_import()

if __name__ == "__main__":
    opensong_import_lots()
