# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

import logging
import os
import os.path
import sys

from openlp.plugins.bibles.lib.biblemanager import BibleManager

mypath = os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..','..','..')))

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console = logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter(u'%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger(u'').addHandler(console)
log = logging.getLogger(u'')

logging.info(u'\nLogging started')

class TestBibleManager:
    log = logging.getLogger(u'testBibleMgr')
    def setup_class(self):
        log.debug(u'\n.......Register BM')
        self.bm = BibleManager()

    def testRegisterOSISBibleFiles(self):
        # Register a bible from files
        log.debug(u'\n.......testRegisterOSISBibleFiles')
        self.bm.register_osis_file_bible(u'asv', u'asv.osis')
        b = self.bm.get_bibles()
        for b1 in b:
            log.debug( b1)
            assert(b1 in b)
