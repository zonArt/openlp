# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
import sys

from openlp.plugins.songs.lib.opensongimport import OpenSongImport
from openlp.core.lib.db import Manager
from openlp.plugins.songs.lib.db import init_schema

import logging
LOG_FILENAME = 'test_import_file.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

from test_opensongimport import wizard_stub, progbar_stub

def test(filenames):
    manager = Manager(u'songs', init_schema)
    o = OpenSongImport(manager, filenames=filenames)
    o.import_wizard = wizard_stub()
    o.commit = False
    o.do_import()
    o.print_song()

if __name__ == "__main__":
    test(sys.argv[1:])