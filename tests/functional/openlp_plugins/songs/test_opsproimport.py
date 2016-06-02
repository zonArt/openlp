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
from unittest import TestCase, skipUnless

try:
    from openlp.core.common import Registry
    from openlp.plugins.songs.lib.importers.opspro import OPSProImport
    CAN_RUN_TESTS = True
except ImportError:
    CAN_RUN_TESTS = False

from tests.functional import patch, MagicMock

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'opsprosongs'))


def _get_item(data, key):
    """
    Get an item or return a blank string
    """
    if key in data:
        return data[key]
    return ''


def _build_data(test_file, dual_language):
    """
    Build the test data
    """
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


@skipUnless(CAN_RUN_TESTS, 'Not Windows, skipping test')
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
    def test_create_importer(self, mocked_songimport):
        """
        Test creating an instance of the OPS Pro file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        mocked_manager = MagicMock()

        # WHEN: An importer object is created
        importer = OPSProImport(mocked_manager, filenames=[])

        # THEN: The importer object should not be None
        self.assertIsNotNone(importer, 'Import should not be none')

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def test_detect_chorus(self, mocked_songimport):
        """
        Test importing lyrics with a chorus in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a mocked song and lyrics entry
        mocked_manager = MagicMock()
        importer = OPSProImport(mocked_manager, filenames=[])
        importer.finish = MagicMock()
        song, lyrics = _build_data('you are so faithfull.txt', False)

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The imported data should look like expected
        result_file = open(os.path.join(TEST_PATH, 'You are so faithful.json'), 'rb')
        result_data = json.loads(result_file.read().decode())
        self.assertListEqual(importer.verses, _get_item(result_data, 'verses'))
        self.assertListEqual(importer.verse_order_list_generated, _get_item(result_data, 'verse_order_list'))

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def test_join_and_split(self, mocked_songimport):
        """
        Test importing lyrics with a split and join tags works in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a mocked song and lyrics entry
        mocked_manager = MagicMock()
        importer = OPSProImport(mocked_manager, filenames=[])
        importer.finish = MagicMock()
        song, lyrics = _build_data('amazing grace.txt', False)

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The imported data should look like expected
        result_file = open(os.path.join(TEST_PATH, 'Amazing Grace.json'), 'rb')
        result_data = json.loads(result_file.read().decode())
        self.assertListEqual(importer.verses, _get_item(result_data, 'verses'))
        self.assertListEqual(importer.verse_order_list_generated, _get_item(result_data, 'verse_order_list'))

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def test_trans_off_tag(self, mocked_songimport):
        """
        Test importing lyrics with a split and join and translations tags works in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a mocked song and lyrics entry
        mocked_manager = MagicMock()
        importer = OPSProImport(mocked_manager, filenames=[])
        importer.finish = MagicMock()
        song, lyrics = _build_data('amazing grace2.txt', True)

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The imported data should look like expected
        result_file = open(os.path.join(TEST_PATH, 'Amazing Grace.json'), 'rb')
        result_data = json.loads(result_file.read().decode())
        self.assertListEqual(importer.verses, _get_item(result_data, 'verses'))
        self.assertListEqual(importer.verse_order_list_generated, _get_item(result_data, 'verse_order_list'))

    @patch('openlp.plugins.songs.lib.importers.opspro.SongImport')
    def test_trans_tag(self, mocked_songimport):
        """
        Test importing lyrics with various translations tags works in OPS Pro
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a mocked song and lyrics entry
        mocked_manager = MagicMock()
        importer = OPSProImport(mocked_manager, filenames=[])
        importer.finish = MagicMock()
        song, lyrics = _build_data('amazing grace3.txt', True)

        # WHEN: An importer object is created
        importer.process_song(song, lyrics, [])

        # THEN: The imported data should look like expected
        result_file = open(os.path.join(TEST_PATH, 'Amazing Grace3.json'), 'rb')
        result_data = json.loads(result_file.read().decode())
        self.assertListEqual(importer.verses, _get_item(result_data, 'verses'))
        self.assertListEqual(importer.verse_order_list_generated, _get_item(result_data, 'verse_order_list'))

