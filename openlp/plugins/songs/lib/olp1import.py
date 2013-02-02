# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
from chardet.universaldetector import UniversalDetector
import sqlite
import sys
import os

from openlp.core.lib import translate
from openlp.plugins.songs.lib import retrieve_windows_encoding
from songimport import SongImport

log = logging.getLogger(__name__)

class OpenLP1SongImport(SongImport):
    """
    The :class:`OpenLP1SongImport` class provides OpenLP with the ability to
    import song databases from installations of openlp.org 1.x.
    """
    lastEncoding = u'windows-1252'

    def __init__(self, manager, **kwargs):
        """
        Initialise the import.

        ``manager``
            The song manager for the running OpenLP installation.

        ``filename``
            The database providing the data to import.
        """
        SongImport.__init__(self, manager, **kwargs)
        self.availableThemes = kwargs[u'plugin'].theme_manager.get_themes()

    def doImport(self):
        """
        Run the import for an openlp.org 1.x song database.
        """
        if not self.importSource.endswith(u'.olp'):
            self.logError(self.importSource,
                translate('SongsPlugin.OpenLP1SongImport', 'Not a valid openlp.org 1.x song database.'))
            return
        encoding = self.getEncoding()
        if not encoding:
            return
        # Connect to the database.
        connection = sqlite.connect(self.importSource, mode=0444, encoding=(encoding, 'replace'))
        cursor = connection.cursor()
        # Determine if the db supports linking audio to songs.
        cursor.execute(u'SELECT name FROM sqlite_master '
            u'WHERE type = \'table\' AND name = \'tracks\'')
        db_has_tracks = len(cursor.fetchall()) > 0
        # Determine if the db contains theme information.
        cursor.execute(u'SELECT name FROM sqlite_master '
            u'WHERE type = \'table\' AND name = \'settings\'')
        db_has_themes = len(cursor.fetchall()) > 0
        # "cache" our list of authors.
        cursor.execute(u'-- types int, unicode')
        cursor.execute(u'SELECT authorid, authorname FROM authors')
        authors = cursor.fetchall()
        if db_has_tracks:
            # "cache" our list of tracks.
            cursor.execute(u'-- types int, unicode')
            cursor.execute(u'SELECT trackid, fulltrackname FROM tracks')
            tracks = cursor.fetchall()
        if db_has_themes:
            # "cache" our list of themes.
            themes = {}
            cursor.execute(u'-- types int, unicode')
            cursor.execute(u'SELECT settingsid, settingsname FROM settings')
            for theme_id, theme_name in cursor.fetchall():
                if theme_name in self.availableThemes:
                    themes[theme_id] = theme_name
        # Import the songs.
        cursor.execute(u'-- types int, unicode, unicode, unicode')
        cursor.execute(u'SELECT songid, songtitle, lyrics || \'\' AS ' \
                u'lyrics, copyrightinfo FROM songs')
        songs = cursor.fetchall()
        self.importWizard.progressBar.setMaximum(len(songs))
        for song in songs:
            self.setDefaults()
            if self.stopImportFlag:
                break
            song_id = song[0]
            self.title = song[1]
            lyrics = song[2].replace(u'\r\n', u'\n')
            self.addCopyright(song[3])
            if db_has_themes:
                cursor.execute(u'-- types int')
                cursor.execute(
                    u'SELECT settingsid FROM songs WHERE songid = %s' % song_id)
                theme_id = cursor.fetchone()[0]
                self.themeName = themes.get(theme_id, u'')
            verses = lyrics.split(u'\n\n')
            for verse in verses:
                if verse.strip():
                    self.addVerse(verse.strip())
            cursor.execute(u'-- types int')
            cursor.execute(u'SELECT authorid FROM songauthors '
                u'WHERE songid = %s' % song_id)
            author_ids = cursor.fetchall()
            for author_id in author_ids:
                if self.stopImportFlag:
                    break
                for author in authors:
                    if author[0] == author_id[0]:
                        self.parseAuthor(author[1])
                        break
            if self.stopImportFlag:
                break
            if db_has_tracks:
                cursor.execute(u'-- types int, int')
                cursor.execute(u'SELECT trackid, listindex '
                    u'FROM songtracks '
                    u'WHERE songid = %s ORDER BY listindex' % song_id)
                track_ids = cursor.fetchall()
                for track_id, listindex in track_ids:
                    if self.stopImportFlag:
                        break
                    for track in tracks:
                        if track[0] == track_id:
                            media_file = self.expandMediaFile(track[1])
                            self.addMediaFile(media_file, listindex)
                            break
            if self.stopImportFlag:
                break
            if not self.finish():
                self.logError(self.importSource)

    def getEncoding(self):
        """
        Detect character encoding of an openlp.org 1.x song database.
        """
        # Connect to the database.
        connection = sqlite.connect(self.importSource.encode(
            sys.getfilesystemencoding()), mode=0444)
        cursor = connection.cursor()

        detector = UniversalDetector()
        # Detect charset by authors.
        cursor.execute(u'SELECT authorname FROM authors')
        authors = cursor.fetchall()
        for author in authors:
            detector.feed(author[0])
            if detector.done:
                detector.close()
                return detector.result[u'encoding']
        # Detect charset by songs.
        cursor.execute(u'SELECT songtitle, copyrightinfo, '
            u'lyrics || \'\' AS lyrics FROM songs')
        songs = cursor.fetchall()
        for index in [0, 1, 2]:
            for song in songs:
                detector.feed(song[index])
                if detector.done:
                    detector.close()
                    return detector.result[u'encoding']
        # Detect charset by songs.
        cursor.execute(u'SELECT name FROM sqlite_master '
            u'WHERE type = \'table\' AND name = \'tracks\'')
        if cursor.fetchall():
            cursor.execute(u'SELECT fulltrackname FROM tracks')
            tracks = cursor.fetchall()
            for track in tracks:
                detector.feed(track[0])
                if detector.done:
                    detector.close()
                    return detector.result[u'encoding']
        detector.close()
        return retrieve_windows_encoding(detector.result[u'encoding'])

    def expandMediaFile(self, filename):
        """
        When you're on Windows, this function expands the file name to include
        the path to OpenLP's application data directory. If you are not on
        Windows, it returns the original file name.

        ``filename``
            The filename to expand.
        """
        if sys.platform != u'win32' and not os.environ.get(u'ALLUSERSPROFILE') and not os.environ.get(u'APPDATA'):
            return filename
        common_app_data = os.path.join(os.environ[u'ALLUSERSPROFILE'],
            os.path.split(os.environ[u'APPDATA'])[1])
        if not common_app_data:
            return filename
        return os.path.join(common_app_data, u'openlp.org', 'Audio', filename)
