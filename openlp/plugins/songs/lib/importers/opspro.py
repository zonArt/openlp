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
import os
if os.name == 'nt':
    import pyodbc
import struct

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
        password = self.extract_mdb_password()
        try:
            conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s;PWD=%s' % (self.import_source, password))
        except (pyodbc.DatabaseError, pyodbc.IntegrityError, pyodbc.InternalError, pyodbc.OperationalError) as e:
            log.warning('Unable to connect the OPS Pro database %s. %s', self.import_source, str(e))
            # Unfortunately no specific exception type
            self.log_error(self.import_source, translate('SongsPlugin.OpsProImport',
                                                         'Unable to connect the OPS Pro database.'))
            return
        cursor = conn.cursor()
        cursor.execute('SELECT Song.ID, SongNumber, SongBookName, Title, CopyrightText, Version, Origin FROM Song '
                       'LEFT JOIN SongBook ON Song.SongBookID = SongBook.ID ORDER BY Title')
        songs = cursor.fetchall()
        self.import_wizard.progress_bar.setMaximum(len(songs))
        for song in songs:
            if self.stop_import_flag:
                break
            cursor.execute('SELECT Lyrics, Type, IsDualLanguage FROM Lyrics WHERE SongID = %d AND Type < 2 ORDER BY Type DESC' % song.ID)
            lyrics = cursor.fetchone()
            cursor.execute('SELECT CategoryName FROM Category INNER JOIN SongCategory '
                           'ON Category.ID = SongCategory.CategoryID WHERE SongCategory.SongID = %d '
                           'ORDER BY CategoryName' % song.ID)
            topics = cursor.fetchall()
            self.process_song(song, lyrics, topics)
            break

    def process_song(self, song, lyrics, topics):
        """
        Create the song, i.e. title, verse etc.
        """
        self.set_defaults()
        self.title = song.Title
        if song.CopyrightText:
            self.parse_author(song.CopyrightText)
        if song.Origin:
            self.comments = song.Origin
        if song.SongBookName:
            self.song_book_name = song.SongBookName
        if song.SongNumber:
            self.song_number = song.SongNumber
        for topic in topics:
            self.topics.append(topic.CategoryName)
        # Try to split lyrics based on various rules
        print(song.ID)
        if lyrics:
            lyrics_text = lyrics.Lyrics
            # Remove whitespaces around the join-tag to keep verses joint
            lyrics_text = re.sub('\s*\[join\]\s*', '[join]', lyrics_text, flags=re.IGNORECASE)
            lyrics_text = re.sub('\s*\[splits?\]\s*', '[split]', lyrics_text, flags=re.IGNORECASE)
            verses = re.split('\r\n\s*?\r\n', lyrics_text)
            verse_tag_defs = {}
            verse_tag_texts = {}
            chorus = ''
            for verse_text in verses:
                if verse_text.strip() == '':
                    continue
                verse_def = 'v'
                # Try to detect verse number
                verse_number = re.match('^(\d+)\r\n', verse_text)
                if verse_number:
                    verse_text = re.sub('^\d+\r\n', '', verse_text)
                    verse_def = 'v' + verse_number.group(1)
                # Detect verse tags
                elif re.match('^.+?\:\r\n', verse_text):
                    tag_match = re.match('^(.+?)\:\r\n(.*)', verse_text, flags=re.DOTALL)
                    tag = tag_match.group(1).lower()
                    tag = tag.split(' ')[0]
                    verse_text = tag_match.group(2)
                    if 'refrein' in tag:
                        verse_def = 'c'
                    elif 'bridge' in tag:
                        verse_def = 'b'
                    verse_tag_defs[tag] = verse_def
                    verse_tag_texts[tag] = verse_text
                # Detect tag reference
                elif re.match('^\(.*?\)$', verse_text):
                    tag_match = re.match('^\((.*?)\)$', verse_text)
                    tag = tag_match.group(1).lower()
                    if tag in verse_tag_defs:
                        verse_text = verse_tag_texts[tag]
                        verse_def = verse_tag_defs[tag]
                # Try to detect end tag
                elif re.match('^\[slot\]\r\n', verse_text, re.IGNORECASE):
                    verse_def = 'e'
                    verse_text = re.sub('^\[slot\]\r\n', '', verse_text, flags=re.IGNORECASE)
                # Handle tags
                # Replace the join tag with line breaks
                verse_text = re.sub('\[join\]', '\r\n\r\n', verse_text)
                # Replace the split tag with line breaks and an optional split
                verse_text = re.sub('\[split\]', '\r\n\r\n[---]\r\n', verse_text)
                # Handle translations
                #if lyrics.IsDualLanguage:
                #    ...

                # Remove comments
                verse_text = re.sub('\(.*?\)\r\n', '', verse_text, flags=re.IGNORECASE)
                self.add_verse(verse_text, verse_def)
                print(verse_def)
                print(verse_text)
        self.finish()

    def extract_mdb_password(self):
        """
        Extract password from mdb. Based on code from
        http://tutorialsto.com/database/access/crack-access-*.-mdb-all-current-versions-of-the-password.html
        """
        # The definition of 13 bytes as the source XOR Access2000. Encrypted with the corresponding signs are 0x13
        xor_pattern_2k  = (0xa1, 0xec, 0x7a, 0x9c, 0xe1, 0x28, 0x34, 0x8a, 0x73, 0x7b, 0xd2, 0xdf, 0x50)
        # Access97 XOR of the source
        xor_pattern_97 = (0x86, 0xfb, 0xec, 0x37, 0x5d, 0x44, 0x9c, 0xfa, 0xc6, 0x5e, 0x28, 0xe6, 0x13)
        mdb = open(self.import_source, 'rb')
        mdb.seek(0x14)
        version = struct.unpack('B', mdb.read(1))[0]
        # Get encrypted logo
        mdb.seek(0x62)
        EncrypFlag = struct.unpack('B', mdb.read(1))[0]
        # Get encrypted password
        mdb.seek(0x42);
        encrypted_password = mdb.read(26)
        mdb.close()
        # "Decrypt" the password based on the version
        decrypted_password = ''
        if version < 0x01:
            # Access 97
            if int (encrypted_password[0] ^ xor_pattern_97[0]) == 0:
                # No password
                decrypted_password = ''
            else:
                for j in range(0, 12):
                    decrypted_password = decrypted_password + chr(encrypted_password[j] ^ xor_pattern_97[j])
        else:
            # Access 2000 or 2002
            for j in range(0, 12):
                if j% 2 == 0:
                    # Every byte with a different sign or encrypt. Encryption signs here for the 0x13
                    t1 = chr (0x13 ^ EncrypFlag ^ encrypted_password[j * 2] ^ xor_pattern_2k[j])
                else:
                    t1 = chr(encrypted_password[j * 2] ^ xor_pattern_2k[j]);
                decrypted_password = decrypted_password + t1;
        if ord(decrypted_password[1]) < 0x20 or ord(decrypted_password[1]) > 0x7e:
            decrypted_password = ''
        return decrypted_password
