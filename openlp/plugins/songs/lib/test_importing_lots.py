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
    files.extend(glob(ziploc+u'Songs.zip'))
    files.extend(glob(ziploc+u'SOF.zip'))
#    files.extend(glob(ziploc+u'spanish_songs_for_opensong.zip'))
#    files.extend(glob(ziploc+u'opensong_*.zip'))
    errfile=codecs.open(u'import_lots_errors.txt', u'w', u'utf8')
    manager=SongManager()
    for file in files:
        print u'Importing', file
        z=ZipFile(file, u'r')
        for song in z.infolist():
            filename=song.filename.decode('cp852')
            parts=os.path.split(filename)
            if parts[-1] == u'':
                #No final part => directory
                continue
            # xxx need to handle unicode filenames (CP437?? Winzip does this)
            print "  ", file, ":",filename,
            songfile=z.open(song)

            o=OpenSongImport(manager)
            try:
                o.do_import_file(songfile)
            except:
                print "Failure",
                
                errfile.write(u'Failure: %s:%s\n' %(file, filename))
                songfile=z.open(song)
                for l in songfile.readlines():
                    l=l.decode('utf8')
                    print(u'  |%s\n'%l.strip())
                    errfile.write(u'  |%s\n'%l.strip())   
                print_exc(3, file=errfile)
                continue
            # o.finish()
            print "OK"
            # o.song.print_song()
if __name__=="__main__":
    opensong_import_lots()
