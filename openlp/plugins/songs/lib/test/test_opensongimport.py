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
from openlp.plugins.songs.lib.opensongimport import OpenSongImport
from openlp.plugins.songs.lib.manager import SongManager
import sys

def test():
    manager = SongManager()
    o = OpenSongImport(manager)
    o.do_import(u'test.opensong', commit=False)
    o.finish()
    o.song.print_song()
    assert o.song.copyright == u'2010 Martin Thompson'
    assert o.song.authors == [u'MartiÑ Thómpson']
    assert o.song.title == u'Martins Test'
    assert o.song.alternate_title == u''
    assert o.song.song_number == u'1'
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.song.verses 
    assert [u'C1', u'Chorus 1'] in o.song.verses 
    assert [u'C2', u'Chorus 2'] in o.song.verses 
    assert not [u'C3', u'Chorus 3'] in o.song.verses 
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.song.verses 
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.song.verses
    assert o.song.verse_order_list == [u'V1', u'C1', u'V2', u'C2', u'V3', u'B1', u'V1']
    assert o.song.song_cclino == u'Blah'
    print u':%s:'%o.song.theme
    assert o.song.theme == u'TestTheme, TestAltTheme'
    o.do_import(u'test.opensong.zip', commit=False)
    o.finish()
    o.song.print_song()
    assert o.song.copyright == u'2010 Martin Thompson'
    assert o.song.authors == [u'MartiÑ Thómpson']
    assert o.song.title == u'Martins Test'
    assert o.song.alternate_title == u''
    assert o.song.song_number == u'1'
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.song.verses 
    assert [u'C1', u'Chorus 1'] in o.song.verses 
    assert [u'C2', u'Chorus 2'] in o.song.verses 
    assert not [u'C3', u'Chorus 3'] in o.song.verses 
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.song.verses 
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.song.verses
    assert o.song.verse_order_list == [u'V1', u'C1', u'V2', u'C2', u'V3', u'B1', u'V1']

    o = OpenSongImport(manager)
    o.do_import(u'test2.opensong', commit=False)
    # o.finish()
    o.song.print_song()
    assert o.song.copyright == u'2010 Martin Thompson'
    assert o.song.authors == [u'Martin Thompson']
    assert o.song.title == u'Martins 2nd Test'
    assert o.song.alternate_title == u''
    assert o.song.song_number == u'2'
    print o.song.verses
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.song.verses 
    assert [u'C1', u'Chorus 1'] in o.song.verses 
    assert [u'C2', u'Chorus 2'] in o.song.verses 
    assert not [u'C3', u'Chorus 3'] in o.song.verses 
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.song.verses 
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.song.verses
    print o.song.verse_order_list
    assert o.song.verse_order_list == [u'V1', u'V2', u'B1', u'C1', u'C2']

    print "Tests passed"
    pass

if __name__ == "__main__":
    test()
