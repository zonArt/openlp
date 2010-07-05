from openlp.plugins.songs.lib.opensongimport import OpenSongImport
from openlp.plugins.songs.lib.manager import SongManager
from glob import glob
from zipfile import ZipFile
import os
from traceback import print_exc
import sys
import codecs
def opensong_import_lots():
    ziploc=u'/home/mjt/openlp/OpenSong_Data/'
    files=[]
    files=[u'test.opensong.zip', ziploc+u'ADond.zip']
    #files.extend(glob(ziploc+u'Songs.zip'))
    #files.extend(glob(ziploc+u'SOF.zip'))
    files.extend(glob(ziploc+u'spanish_songs_for_opensong.zip'))
#    files.extend(glob(ziploc+u'opensong_*.zip'))
    errfile=codecs.open(u'import_lots_errors.txt', u'w', u'utf8')
    manager=SongManager()
    for file in files:
        print u'Importing', file
        z=ZipFile(file, u'r')
        for song in z.infolist():
            # need to handle unicode filenames (CP437 -  Winzip does this)
            filename=song.filename#.decode('cp852')
            parts=os.path.split(filename)
            if parts[-1] == u'':
                #No final part => directory
                continue
            print "  ", file, ":",filename,
            songfile=z.open(song)
            #z.extract(song)
            #songfile=open(filename, u'r')
            o=OpenSongImport(manager)
            try:
                o.do_import_file(songfile)
                o.song.print_song()
            except:
                print "Failure",
                
                errfile.write(u'Failure: %s:%s\n' %(file, filename.decode('cp437')))
                songfile=z.open(song)
                for l in songfile.readlines():
                    l=l.decode('utf8')
                    print(u'  |%s\n'%l.strip())
                    errfile.write(u'  |%s\n'%l.strip())   
                print_exc(3, file=errfile)
                print_exc(3)
                sys.exit(1)
                # continue
            #o.finish()
            print "OK"
            #os.unlink(filename)
            # o.song.print_song()
if __name__=="__main__":
    opensong_import_lots()
