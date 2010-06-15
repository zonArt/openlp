from openlp.plugins.songs.lib.opensongimport import OpenSongImport
from openlp.plugins.songs.lib.manager import SongManager

def test():
    manager=SongManager()
    o=OpenSongImport(manager)
    o.do_import(u'test.opensong')
    # xxx need some more asserts in here to test it...
    assert (1)
    # now to XML
    # asserts
    pass

if __name__=="__main__":
    test()
