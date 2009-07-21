/usr/bin/sqlite ~/.local/share/openlp/songs/songs.olp .dump > ~/.local/share/openlp/songs/songs.dmp
./cnvdb.py ~/.local/share/openlp/songs/songs.dmp ~/.local/share/openlp/songs/songs.dmp2
rm ~/.local/share/openlp/songs/songs.sqlite
sqlite3 ~/.local/share/openlp/songs/songs.sqlite < ~/.local/share/openlp/songs/songs.dmp2
./openlpcnv.pyw
