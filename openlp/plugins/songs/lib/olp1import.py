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
"""
The :mod:`olp1import` module provides the functionality for importing
openlp.org 1.x song databases into the current installation database.
"""
import logging
import sqlite

#from openlp.core.lib.db import BaseModel
from openlp.plugins.songs.lib.db import Author, Book, Song, Topic #, MediaFile
from songimport import SongImport

log = logging.getLogger(__name__)

class OpenLP1SongImport(SongImport):
    """
    The :class:`OpenLP1SongImport` class provides OpenLP with the ability to
    import song databases from installations of openlp.org 1.x.
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the import.

        ``manager``
            The song manager for the running OpenLP installation.

        ``filename``
            The database providing the data to import.
        """
        SongImport.__init__(self, manager)
        self.import_source = kwargs[u'filename']

    def do_import(self):
        """
        Run the import for an openlp.org 1.x song database.
        """
        # Connect to the database
        connection = sqlite.connect(self.import_source)
        cursor = connection.cursor()
        # Count the number of records we need to import, for the progress bar
        cursor.execute(u'SELECT COUNT(songid) FROM songs')
        count = int(cursor.fetchone()[0])
        success = True
        self.import_wizard.importProgressBar.setMaximum(count)
        # Import the songs
        cursor.execute(u'SELECT songid, songtitle, lyrics || \'\' AS lyrics, '
            u'copyrightinfo FROM songs')
        songs = cursor.fetchall()
        for song in songs:
            self.set_defaults()
            if self.stop_import_flag:
                success = False
                break
            song_id = song[0]
            title = unicode(song[1], u'cp1252')
            lyrics = unicode(song[2], u'cp1252')
            copyright = unicode(song[3], u'cp1252')
            self.import_wizard.incrementProgressBar(
                unicode(translate('SongsPlugin.ImportWizardForm',
                    'Importing %s...')) % title)
            self.title = title
            self.process_song_text(lyrics)
            self.add_copyright(copyright)
            cursor.execute(u'SELECT displayname FROM authors a '
                u'JOIN songauthors sa ON a.authorid = sa.authorid '
                u'WHERE sa.songid = %s' % song_id)
            authors = cursor.fetchall()
            for author in authors:
                if self.stop_import_flag:
                    success = False
                    break
                self.parse_author(unicode(author[0], u'cp1252'))
            if self.stop_import_flag:
                success = False
                break
            cursor.execute(u'SELECT name FROM sqlite_master '
                u'WHERE type = \'table\' NAME name = \'tracks\'')
            table_list = cursor.fetchall()
            if len(table_list) > 0:
                cursor.execute(u'SELECT fulltrackname FROM tracks t '
                    u'JOIN songtracks st ON t.trackid = st.trackid '
                    u'WHERE st.songid = %s ORDER BY st.listindex' % song_id)
                tracks = cursor.fetchall()
                for track in tracks:
                    if self.stop_import_flag:
                        success = False
                        break
                    self.add_media_file(unicode(track[0], u'cp1252'))
            if self.stop_import_flag:
                success = False
                break
            self.finish()
        return success
