# -*- coding: utf-8 -*-
from openlp.plugins.songs.lib.opensongimport import OpenSongImport
from openlp.plugins.songs.lib.manager import SongManager

def test():
    manager=SongManager()
    o=OpenSongImport(manager)
    o.do_import(u'test.opensong')
    # o.finish()
    o.song.print_song()
    assert o.song.copyright == u'2010 Martin Thompson'
    assert o.song.authors == [u'MartiÑ Thómpson']
    assert o.song.title == u'Martins Test'
    assert o.song.alternate_title == u''
    assert o.song.song_number == u'1'
    assert [u'B1', u'Bridge 1\nBridge 1 line 2'] in o.song.verses 
    assert [u'C', u'Chorus 1'] in o.song.verses 
    assert [u'C2', u'Chorus 2'] in o.song.verses 
    assert not [u'C3', u'Chorus 3'] in o.song.verses 
    assert [u'V1', u'v1 Line 1\nV1 Line 2'] in o.song.verses 
    assert [u'V2', u'v2 Line 1\nV2 Line 2'] in o.song.verses
    assert o.song.verse_order_list == [u'V1', u'C', u'V2', u'C2', u'V3', u'B1', u'V1']

    o=OpenSongImport(manager)
    o.do_import(u'test2.opensong')
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

if __name__=="__main__":
    test()
