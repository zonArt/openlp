# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

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

from openlp.plugins.songs.lib.opensongimport import OpenSongImport
from openlp.plugins.songs.lib.db import init_schema
from openlp.core.lib.db import Manager
import os
import codecs

import logging
LOG_FILENAME = 'import.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

from test_opensongimport import wizard_stub

# Useful test function for importing a variety of different files
# Uncomment below depending on what problem trying to make occur!

def opensong_import_lots():
    ziploc = u'/home/mjt/openlp/OpenSong_Data/'
    files = []
    files = [os.path.join(ziploc, u'RaoulSongs', u'Songs', u'Jesus Freak')]
    # files.extend(glob(ziploc+u'Songs.zip'))
    # files.extend(glob(ziploc+u'RaoulSongs.zip'))
    # files.extend(glob(ziploc+u'SOF.zip'))
    # files.extend(glob(ziploc+u'spanish_songs_for_opensong.zip'))
    # files.extend(glob(ziploc+u'opensong_*.zip'))
    errfile = codecs.open(u'import_lots_errors.txt', u'w', u'utf8')
    manager = Manager(u'songs', init_schema)
    o = OpenSongImport(manager, filenames=files)
    o.import_wizard=wizard_stub()
    o.do_import()

if __name__ == "__main__":
    opensong_import_lots()
