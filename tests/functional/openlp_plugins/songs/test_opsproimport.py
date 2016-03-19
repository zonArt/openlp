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
This module contains tests for the WorshipCenter Pro song importer.
"""
import os
import json
from unittest import TestCase, SkipTest

from tests.functional import patch, MagicMock

from openlp.core.common import Registry
from openlp.plugins.songs.lib.importers.opspro import OpsProImport

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'opsprosongs'))

class TestRecord(object):
    """
    Microsoft Access Driver is not available on non Microsoft Systems for this reason the :class:`TestRecord` is used
    to simulate a recordset that would be returned by pyobdc.
    """
    def __init__(self, id, field, value):
        # The case of the following instance variables is important as it needs to be the same as the ones in use in the
        # WorshipCenter Pro database.
        self.ID = id
        self.Field = field
        self.Value = value

class TestOpsProSongImport(TestCase):
    """
    Test the functions in the :mod:`opsproimport` module.
    """
    def setUp(self):
        """
        Create the registry
        """
        Registry.create()

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def create_importer_test(self, mocked_songimport):
        """
        Test creating an instance of the OPS Pro file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        mocked_manager = MagicMock()

        # WHEN: An importer object is created
        importer = OpsProImport(mocked_manager, filenames=[])

        # THEN: The importer object should not be None
        self.assertIsNotNone(importer, 'Import should not be none')

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def detect_chorus_test(self, mocked_songimport):
        """
        Test importing lyrics with a chorus in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a mocked song and lyrics entry
        mocked_manager = MagicMock()
        importer = OpsProImport(mocked_manager, filenames=[])
        importer.finish = MagicMock()
        song, lyrics = self._build_test_data('you are so faithfull.txt', False)

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The imported data should look like expected
        result_file = open(os.path.join(TEST_PATH, 'You are so faithful.json'), 'rb')
        result_data = json.loads(result_file.read().decode())
        self.assertListEqual(importer.verses, self._get_data(result_data, 'verses'))
        self.assertListEqual(importer.verse_order_list_generated, self._get_data(result_data, 'verse_order_list'))

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def join_and_split_test(self, mocked_songimport):
        """
        Test importing lyrics with a split and join tags works in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a mocked song and lyrics entry
        mocked_manager = MagicMock()
        importer = OpsProImport(mocked_manager, filenames=[])
        importer.finish = MagicMock()
        song, lyrics = self._build_test_data('amazing grace.txt', False)

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The imported data should look like expected
        result_file = open(os.path.join(TEST_PATH, 'Amazing Grace.json'), 'rb')
        result_data = json.loads(result_file.read().decode())
        self.assertListEqual(importer.verses, self._get_data(result_data, 'verses'))
        self.assertListEqual(importer.verse_order_list_generated, self._get_data(result_data, 'verse_order_list'))

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def trans_off_tag_test(self, mocked_songimport):
        """
        Test importing lyrics with a split and join and translations tags works in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a mocked song and lyrics entry
        mocked_manager = MagicMock()
        importer = OpsProImport(mocked_manager, filenames=[])
        importer.finish = MagicMock()
        song, lyrics = self._build_test_data('amazing grace2.txt', True)

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The imported data should look like expected
        result_file = open(os.path.join(TEST_PATH, 'Amazing Grace.json'), 'rb')
        result_data = json.loads(result_file.read().decode())
        self.assertListEqual(importer.verses, self._get_data(result_data, 'verses'))
        self.assertListEqual(importer.verse_order_list_generated, self._get_data(result_data, 'verse_order_list'))

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def trans_tag_test(self, mocked_songimport):
        """
        Test importing lyrics with various translations tags works in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a mocked song and lyrics entry
        mocked_manager = MagicMock()
        importer = OpsProImport(mocked_manager, filenames=[])
        importer.finish = MagicMock()
        song, lyrics = self._build_test_data('amazing grace3.txt', True)

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The imported data should look like expected
        result_file = open(os.path.join(TEST_PATH, 'Amazing Grace3.json'), 'rb')
        result_data = json.loads(result_file.read().decode())
        self.assertListEqual(importer.verses, self._get_data(result_data, 'verses'))
        self.assertListEqual(importer.verse_order_list_generated, self._get_data(result_data, 'verse_order_list'))

    def _get_data(self, data, key):
        if key in data:
            return data[key]
        return ''

    def _build_test_data(self, test_file, dual_language):
        song = MagicMock()
        song.ID = 100
        song.SongNumber = 123
        song.SongBookName = 'The Song Book'
        song.Title = 'Song Title'
        song.CopyrightText = 'Music and text by me'
        song.Version = '1'
        song.Origin = '...'
        lyrics = MagicMock()
        test_file = open(os.path.join(TEST_PATH, test_file), 'rb')
        lyrics.Lyrics = test_file.read().decode()
        lyrics.Type = 1
        lyrics.IsDualLanguage = dual_language
        return song, lyrics
