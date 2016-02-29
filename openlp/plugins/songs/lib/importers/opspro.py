# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
The :mod:`opspro` module provides the functionality for importing
a OPS Pro database into the OpenLP database.
"""
import logging
import re
import pyodbc

from openlp.core.common import translate
from openlp.plugins.songs.lib.importers.songimport import SongImport

log = logging.getLogger(__name__)


class OpsProImport(SongImport):
    """
    The :class:`OpsProImport` class provides the ability to import the
    WorshipCenter Pro Access Database
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the WorshipCenter Pro importer.
        """
        super(OpsProImport, self).__init__(manager, **kwargs)

    def do_import(self):
        """
        Receive a single file to import.
        """
        try:
            conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s' % self.import_source)
        except (pyodbc.DatabaseError, pyodbc.IntegrityError, pyodbc.InternalError, pyodbc.OperationalError) as e:
            log.warning('Unable to connect the OPS Pro database %s. %s', self.import_source, str(e))
            # Unfortunately no specific exception type
            self.log_error(self.import_source, translate('SongsPlugin.OpsProImport',
                                                         'Unable to connect the OPS Pro database.'))
            return
        cursor = conn.cursor()
        cursor.execute('SELECT Song.ID, Song.SongNumber, Song.SongBookID, Song.Title, Song.CopyrightText, Version, Origin FROM Song ORDER BY Song.Title')
        songs = cursor.fetchall()
        self.import_wizard.progress_bar.setMaximum(len(songs))
        for song in songs:
            if self.stop_import_flag:
                break
            cursor.execute('SELECT Lyrics FROM Lyrics WHERE SongID = %s ORDER BY Type, Number'
                           % song.ID)
            verses = cursor.fetchall()
            cursor.execute('SELECT CategoryName FROM Category INNER JOIN SongCategory ON SongCategory.CategoryID = Category.CategoryID '
                           'WHERE SongCategory.SongID = %s' % song.ID)
            topics = cursor.fetchall()


            self.process_song(song, verses, topics)

    def process_song(self, song, verses, verse_order, topics):
        """
        Create the song, i.e. title, verse etc.
        """
        self.set_defaults()
        self.title = song.Title
        self.parse_author(song.CopyrightText)
        self.add_copyright(song.Origin)
        for topic in topics:
            self.topics.append(topic.Name)
        self.add_verse(verses.Lyrics)
        self.finish()
