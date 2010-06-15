import openlp.plugins.songs.lib.opensongimport

def test():
    o=opensongimport.opensongimport(0)# xxx needs a song manager here
    o.osimport(u'test.opensong')
    pass

if __name__=="__main__":
    test()
