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
import chardet
import sqlite

from openlp.core.lib import translate
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

    def decode_string(self, raw):
        """
        Use chardet to detect the encoding of the raw string, and convert it
        to unicode.

        ``raw``
            The raw bytestring to decode.
        """
        detection = chardet.detect(raw)
        if detection[u'confidence'] < 0.8:
            codec = u'windows-1252'
        else:
            codec = detection[u'encoding']
        return unicode(raw, codec)

    def do_import(self):
        """
        Run the import for an openlp.org 1.x song database.
        """
        # Connect to the database
        connection = sqlite.connect(self.import_source)
        cursor = connection.cursor()
        # Determine if we're using a new or an old DB
        cursor.execute(u'SELECT name FROM sqlite_master '
            u'WHERE type = \'table\' AND name = \'tracks\'')
        table_list = cursor.fetchall()
        new_db = len(table_list) > 0
        # Count the number of records we need to import, for the progress bar
        cursor.execute(u'SELECT COUNT(songid) FROM songs')
        count = int(cursor.fetchone()[0])
        success = True
        self.import_wizard.importProgressBar.setMaximum(count)
        # "cache" our list of authors
        cursor.execute(u'SELECT authorid, authorname FROM authors')
        authors = cursor.fetchall()
        if new_db:
          # "cache" our list of tracks
          cursor.execute(u'SELECT trackid, fulltrackname FROM tracks')
          tracks = cursor.fetchall()
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
            title = self.decode_string(song[1])
            lyrics = self.decode_string(song[2]).replace(u'\r', u'')
            copyright = self.decode_string(song[3])
            self.import_wizard.incrementProgressBar(
                unicode(translate('SongsPlugin.ImportWizardForm',
                    'Importing "%s"...')) % title)
            self.title = title
            self.process_song_text(lyrics)
            self.add_copyright(copyright)
            cursor.execute(u'SELECT authorid FROM songauthors '
                u'WHERE songid = %s' % song_id)
            author_ids = cursor.fetchall()
            for author_id in author_ids:
                if self.stop_import_flag:
                    success = False
                    break
                for author in authors:
                    if author[0] == author_id[0]:
                        self.parse_author(self.decode_string(author[1]))
                        break
            if self.stop_import_flag:
                success = False
                break
            if new_db:
                cursor.execute(u'SELECT trackid FROM songtracks '
                    u'WHERE songid = %s ORDER BY listindex' % song_id)
                track_ids = cursor.fetchall()
                for track_id in track_ids:
                    if self.stop_import_flag:
                        success = False
                        break
                    for track in tracks:
                        if track[0] == track_id[0]:
                            self.add_media_file(self.decode_string(track[1]))
                            break
            if self.stop_import_flag:
                success = False
                break
            self.finish()
        return success

