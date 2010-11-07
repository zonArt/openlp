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

from PyQt4 import QtGui, QtCore

import logging
from chardet.universaldetector import UniversalDetector
import sqlite

from openlp.core.lib import translate
from songimport import SongImport

log = logging.getLogger(__name__)

class OpenLP1SongImport(SongImport):
    """
    The :class:`OpenLP1SongImport` class provides OpenLP with the ability to
    import song databases from installations of openlp.org 1.x.
    """
    last_encoding = u'windows-1252'

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

    def decode_string(self, raw, encoding):
        """
        Use chardet to detect the encoding of the raw string, and convert it
        to unicode.

        ``raw``
            The raw bytestring to decode.
        ``encoding``
            The bytestring character encoding.
        """
        try:
            decoded = unicode(raw, encoding)
        except UnicodeDecodeError:
            log.exception(u'The openlp.org 1.x database is not %s encoded.' % \
                encoding)
            decoded = raw
        return decoded

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
        encoding = self.get_encoding()
        if not encoding:
            self.stop_import_flag = True
            return False
        for song in songs:
            self.set_defaults()
            if self.stop_import_flag:
                success = False
                break
            song_id = song[0]
            title = self.decode_string(song[1], encoding)
            lyrics = self.decode_string(song[2], encoding).replace(u'\r', u'')
            copyright = self.decode_string(song[3], encoding)
            self.import_wizard.incrementProgressBar(
                unicode(translate('SongsPlugin.ImportWizardForm',
                    'Importing "%s"...')) % title)
            self.title = title
            verses = lyrics.split(u'\n\n')
            for verse in verses:
                if verse.strip() != u'':
                    self.add_verse(verse.strip())
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
                        self.parse_author(self.decode_string(author[1], encoding))
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
                            self.add_media_file(self.decode_string(track[1], encoding))
                            break
            if self.stop_import_flag:
                success = False
                break
            self.finish()
        return success

    def get_encoding(self):
        """
        Detect character encoding of an openlp.org 1.x song database.
        """
        # Connect to the database
        connection = sqlite.connect(self.import_source)
        cursor = connection.cursor()

        detector = UniversalDetector()
        # detect charset by authors
        cursor.execute(u'SELECT authorname FROM authors')
        authors = cursor.fetchall()
        for author in authors:
            detector.feed(author[0])
            if detector.done:
                detector.close()
                return detector.result[u'encoding']
        # detect charset by songs
        cursor.execute(u'SELECT songtitle, copyrightinfo, '
            u'lyrics || \'\' AS lyrics FROM songs')
        songs = cursor.fetchall()
        for index in [0, 1, 2]:
            for song in songs:
                detector.feed(song[index])
                if detector.done:
                    detector.close()
                    return detector.result[u'encoding']
        # detect charset by songs
        cursor.execute(u'SELECT name FROM sqlite_master '
            u'WHERE type = \'table\' AND name = \'tracks\'')
        if len(cursor.fetchall()) > 0:
            cursor.execute(u'SELECT fulltrackname FROM tracks')
            tracks = cursor.fetchall()
            for track in tracks:
                detector.feed(track[0])
                if detector.done:
                    detector.close()
                    return detector.result[u'encoding']
        detector.close()
        guess = detector.result[u'encoding']

        # map chardet result to compatible windows standard code page
        codepage_mapping = {'IBM866': u'cp866', 'TIS-620': u'cp874',
            'SHIFT_JIS': u'cp932', 'GB2312': u'cp936', 'HZ-GB-2312': u'cp936',
            'EUC-KR': u'cp949', 'Big5': u'cp950', 'ISO-8859-2': u'cp1250',
            'windows-1250': u'cp1250', 'windows-1251': u'cp1251',
            'windows-1252': u'cp1252', 'ISO-8859-7': u'cp1253',
            'windows-1253': u'cp1253', 'ISO-8859-8': u'cp1255',
            'windows-1255': u'cp1255'}
        if guess in codepage_mapping:
            guess = codepage_mapping[guess]
        else:
            guess = u'cp1252'

        encodings = {u'cp874': translate('SongsPlugin.OpenLP1SongImport',
                'CP-874 (Thai)'),
            u'cp932': translate('SongsPlugin.OpenLP1SongImport',
                'CP-932 (Japanese)'),
            u'cp936': translate('SongsPlugin.OpenLP1SongImport',
                'CP-936 (Simplified Chinese)'),
            u'cp949': translate('SongsPlugin.OpenLP1SongImport',
                'CP-949 (Korean)'),
            u'cp950': translate('SongsPlugin.OpenLP1SongImport',
                'CP-950 (Traditional Chinese)'),
            u'cp1250': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1250 (Central European)'),
            u'cp1251': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1251 (Cyrillic)'),
            u'cp1252': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1252 (Western European)'),
            u'cp1253': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1253 (Greek)'),
            u'cp1254': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1254 (Turkish)'),
            u'cp1255': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1255 (Hebrew)'),
            u'cp1256': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1256 (Arabic)'),
            u'cp1257': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1257 (Baltic)'),
            u'cp1258': translate('SongsPlugin.OpenLP1SongImport',
                'CP-1258 (Vietnam)')}
        encoding_list = encodings.keys()
        encoding_index = 0
        for encoding in encoding_list:
            if encoding == guess:
                break
            else:
                encoding_index = encoding_index + 1
        ok_applied = False
        chosen_encoding = QtGui.QInputDialog.getItem(None,
            translate('SongsPlugin.OpenLP1SongImport',
                'Database Character Encoding'),
            translate('SongsPlugin.OpenLP1SongImport',
                'The codepage setting is responsible\n'
                'for the correct character representation.\n'
                'Usually you are fine with the preselected choise.'),
            encodings.values(), encoding_index, False)
        if not chosen_encoding[1]:
            return None
        for encoding in encodings.items():
             if encoding[1] == unicode(chosen_encoding[0]):
                 return encoding[0]
