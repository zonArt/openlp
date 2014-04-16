# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
This module contains tests for the OpenLyrics song importer.
"""

import os
from unittest import TestCase

from tests.functional import MagicMock, patch
from openlp.plugins.songs.lib.openlyricsimport import OpenLyricsImport
from openlp.plugins.songs.lib.songimport import SongImport

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'resources', 'openlyricssongs'))
SONG_TEST_DATA = {
    'Mám zde přítele, Pána Ježíše.xml': {
        'title': 'Mám zde přítele',
        'verses': [
            ('Mám zde přítele,\nPána Ježíše,\na na rámě jeho spoléhám;\nv něm své stěstí mám,\n\
             pokoj nalézám,\nkdyž na rámě jeho spoléhám!', 'v1'),
            ('Boží rámě\nje v soužení náš pevný hrad;\nBoží rámě,\nuč se na ně vždycky spoléhat!', 'c'),
            ('Jak je sladké být,\nv jeho družině,\nkdyž na rámě jeho spoléhám,\njak se života\ncesta zjasňuje\n\
             když na rámě Boží spoléhám!', 'v2'),
            ('Čeho bych se bál,\nčeho strachoval,\nkdyž na rámě Boží spoléhám?\nMír je v duši mé,\n\
             když On blízko je,\nkdyž na rámě jeho spoléhám.', 'v')
        ]
    }
}


class TestOpenLyricsImport(TestCase):
    """
    Test the functions in the :mod:`openlyricsimport` module.
    """
    def create_importer_test(self):
        """
        Test creating an instance of the OpenLyrics file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songbeamerimport.SongImport'):
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = OpenLyricsImport(mocked_manager, filenames=[])

            # THEN: The importer should be an instance of SongImport
            self.assertIsInstance(importer, SongImport)

    def file_import_test(self):
        """
        Test the actual import of real song files and check that the importer is called.
        """
        # GIVEN: Test files with a mocked out "manager" and a mocked out "import_wizard"
        for song_file in SONG_TEST_DATA:
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = OpenLyricsImport(mocked_manager, filenames=[])
            importer.import_wizard = mocked_import_wizard
            importer.open_lyrics = MagicMock()
            importer.open_lyrics.xml_to_song = MagicMock()

            # WHEN: Importing each file
            importer.import_source = [os.path.join(TEST_PATH, song_file)]
            importer.do_import()

            # THEN: The xml_to_song() method should have been called
            self.assertTrue(importer.open_lyrics.xml_to_song.called)
