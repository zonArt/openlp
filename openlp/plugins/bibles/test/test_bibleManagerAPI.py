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

from openlp.plugins.biblemanager.bibleManager import BibleManager

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

    def testGetBibles(self):
        log.debug(u'\n.......testGetBibles')
        # make sure the shuffled sequence does not lose any elements
        b = self.bm.getBibles()
        for b1 in b:
            log.debug( b1)
            assert(b1 in b)

    def testGetBibleBooks(self):
        log.debug(u'\n.......testGetBibleBooks')
        c = self.bm.getBibleBooks(u'asv')
        for c1 in c:
            log.debug( c1)
            assert(c1 in c)

    def testGetBookChapterCount(self):
        log.debug(u'\n.......testGetBookChapterCount')
        assert(self.bm.getBookChapterCount(u'asv', u'Matthew')[0] == 28)

    def testGetBookVerseCount(self):
        log.debug(u'\n.......testGetBookVerseCount')
        assert(self.bm.getBookVerseCount(u'asv', u'Genesis', 1)[0] == 31)
        assert(self.bm.getBookVerseCount(u'TheMessage', u'Genesis', 2)[0] == 25)
        assert(self.bm.getBookVerseCount(u'asv', u'Matthew', 1)[0] == 25)
        assert(self.bm.getBookVerseCount(u'TheMessage', u'Revelation',
        1)[0] == 20)

    def testGetVerseText(self):
        log.debug(u'\n.......testGetVerseText')
        #c = self.bm.getVerseText(u'TheMessage",'Genesis',1,2,1)
        #log.debug( c )
        #c = self.bm.getVerseText(u'NIV','Genesis',1,1,2)
        #log.debug( c )
        c = self.bm.getVerseText(u'asv', u'Genesis', 10, 1, 20)
        log.debug( c )
        c = self.bm.getVerseText(u'TheMessage', u'Genesis', 10, 1, 20)
        log.debug( c )
        c = self.bm.getVerseText(u'asv', u'Revelation', 10, 1, 20)
        log.debug( c )
        c = self.bm.getVersesFromText(u'asv', u'Jesus wept')
        log.debug( c )
        c = self.bm.getVersesFromText(u'TheMessage', u'Jesus wept')
        log.debug( c )
