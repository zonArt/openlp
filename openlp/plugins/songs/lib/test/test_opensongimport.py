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

from openlp.plugins.songs.lib.opensongimport import OpenSongImport
from openlp.core.lib.db import Manager
from openlp.plugins.songs.lib.db import init_schema

def test():
    manager = Manager(u'songs', init_schema)
    o = OpenSongImport(manager)
    o.do_import(u'test.opensong', commit=False)
    o.song_import.print_song()
    assert o.song_import.copyright == u'2010 Martin Thompson'
    assert o.song_import.authors == [u'MartiÑ Thómpson']
    assert o.song_import.title == u'Martins Test'
    assert o.song_import.alternate_title == u''
    assert o.song_import.song_number == u'1'
    assert [u'C1', u'Chorus 1'] in o.song_import.verses 
    assert [u'C2', u'Chorus 2'] in o.song_import.verses 
    assert not [u'C3', u'Chorus 3'] in o.song_import.verses 
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.song_import.verses 
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.song_import.verses 
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.song_import.verses
    assert o.song_import.verse_order_list == [u'V1', u'C1', u'V2', u'C2', u'V3', u'B1', u'V1']
    assert o.song_import.ccli_number == u'Blah'
    assert o.song_import.topics == [u'TestTheme', u'TestAltTheme']
    o.do_import(u'test.opensong.zip', commit=False)
    o.song_import.print_song()
    o.finish()
    assert o.song_import.copyright == u'2010 Martin Thompson'
    assert o.song_import.authors == [u'MartiÑ Thómpson']
    assert o.song_import.title == u'Martins Test'
    assert o.song_import.alternate_title == u''
    assert o.song_import.song_number == u'1'
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.song_import.verses 
    assert [u'C1', u'Chorus 1'] in o.song_import.verses 
    assert [u'C2', u'Chorus 2'] in o.song_import.verses 
    assert not [u'C3', u'Chorus 3'] in o.song_import.verses 
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.song_import.verses 
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.song_import.verses
    assert o.song_import.verse_order_list == [u'V1', u'C1', u'V2', u'C2', u'V3', u'B1', u'V1']

    o = OpenSongImport(manager)
    o.do_import(u'test2.opensong', commit=False)
    # o.finish()
    o.song_import.print_song()
    assert o.song_import.copyright == u'2010 Martin Thompson'
    assert o.song_import.authors == [u'Martin Thompson']
    assert o.song_import.title == u'Martins 2nd Test'
    assert o.song_import.alternate_title == u''
    assert o.song_import.song_number == u'2'
    print o.song_import.verses
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.song_import.verses 
    assert [u'C1', u'Chorus 1'] in o.song_import.verses 
    assert [u'C2', u'Chorus 2'] in o.song_import.verses 
    assert not [u'C3', u'Chorus 3'] in o.song_import.verses 
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.song_import.verses 
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.song_import.verses
    print o.song_import.verse_order_list
    assert o.song_import.verse_order_list == [u'V1', u'V2', u'B1', u'C1', u'C2']

    print "Tests passed"
    pass

if __name__ == "__main__":
    test()