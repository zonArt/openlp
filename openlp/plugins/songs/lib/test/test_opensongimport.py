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
from openlp.core.lib.db import Manager
from openlp.plugins.songs.lib.db import init_schema

import logging
LOG_FILENAME = 'test.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

# Stubs to replace the UI functions for raw testing
class wizard_stub:
    def __init__(self):
        self.progressBar=progbar_stub()
    def incrementProgressBar(self, str):
        pass
class progbar_stub:
    def __init__(self):
        pass
    def setMaximum(self, arg):
        pass

def test():
    manager = Manager(u'songs', init_schema)
    o = OpenSongImport(manager, filenames=[u'test.opensong'])
    o.import_wizard = wizard_stub()
    o.commit = False
    o.do_import()
    o.print_song()
    assert o.copyright == u'2010 Martin Thompson'
    assert o.authors == [u'MartiÑ Thómpson', u'Martin2 Thómpson']
    assert o.title == u'Martins Test'
    assert o.alternate_title == u''
    assert o.song_number == u'1'
    assert [u'C1', u'Chorus 1'] in o.verses
    assert [u'C2', u'Chorus 2'] in o.verses
    assert not [u'C3', u'Chorus 3'] in o.verses
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.verses
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.verses
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.verses
    assert [u'V3A', u'V3 Line 1\nV3 Line 2'] in o.verses
    assert [u'RAP1', u'Rap 1 Line 1\nRap 1 Line 2'] in o.verses
    assert [u'RAP2', u'Rap 2 Line 1\nRap 2 Line 2'] in o.verses
    assert [u'RAP3', u'Rap 3 Line 1\nRap 3 Line 2'] in o.verses
    assert [u'X1', u'Unreferenced verse line 1'] in o.verses
    assert o.verse_order_list == [u'V1', u'C1', u'V2', u'C2', u'V3A', u'B1', u'V1', u'T1', u'RAP1', u'RAP2', u'RAP3']
    assert o.ccli_number == u'Blah'
    assert o.topics == [u'TestTheme', u'TestAltTheme']

    o.filenames = [u'test.opensong.zip']
    o.set_defaults()
    o.do_import()
    o.print_song()
    assert o.copyright == u'2010 Martin Thompson'
    assert o.authors == [u'MartiÑ Thómpson']
    assert o.title == u'Martins Test'
    assert o.alternate_title == u''
    assert o.song_number == u'1'
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.verses
    assert [u'C1', u'Chorus 1'] in o.verses
    assert [u'C2', u'Chorus 2'] in o.verses
    assert not [u'C3', u'Chorus 3'] in o.verses
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.verses
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.verses
    print o.verse_order_list
    assert o.verse_order_list == [u'V1', u'C1', u'V2', u'C2', u'V3', u'B1', u'V1']

    o.filenames = [u'test2.opensong']
    o.set_defaults()
    o.do_import()
    o.print_song()
    assert o.copyright == u'2010 Martin Thompson'
    assert o.authors == [u'Martin Thompson']
    assert o.title == u'Martins 2nd Test'
    assert o.alternate_title == u''
    assert o.song_number == u'2'
    print o.verses
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.verses
    assert [u'C1', u'Chorus 1'] in o.verses
    assert [u'C2', u'Chorus 2'] in o.verses
    assert not [u'C3', u'Chorus 3'] in o.verses
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.verses
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.verses
    print o.verse_order_list
    assert o.verse_order_list == [u'V1', u'V2', u'B1', u'C1', u'C2']

    o.filenames = [u'test3.opensong']
    o.set_defaults()
    o.do_import()
    o.print_song()
    assert o.copyright == u'2010'
    assert o.authors == [u'Martin Thompson']
    assert o.title == u'Test single verse'
    assert o.alternate_title == u''
    assert o.ccli_number == u'123456'
    assert o.verse_order_list == [u'V1']
    assert o.topics == [u'Worship: Declaration']
    print o.verses[0]
    assert [u'V1', u'Line 1\nLine 2'] in o.verses

    print "Tests passed"

if __name__ == "__main__":
    test()
