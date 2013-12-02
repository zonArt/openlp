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
This module contains tests for the Songbeamer song importer.
"""

import os
from unittest import TestCase

from tests.functional import MagicMock, patch
from openlp.plugins.songs.lib.songbeamerimport import SongBeamerImport

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'resources', 'songbeamersongs'))
SONG_TEST_DATA = {'Lobsinget dem Herrn.sng':
        {'title': 'GL 1 - Lobsinget dem Herrn',
         'verses':
             [('1. Lobsinget dem Herrn,\no preiset Ihn gern!\n'
               'Anbetung und Lob Ihm gebühret.\n', 'v'),
              ('2. Lobsingt Seiner Lieb´,\ndie einzig ihn trieb,\n'
               'zu sterben für unsere Sünden!\n', 'v'),
              ('3. Lobsingt Seiner Macht!\nSein Werk ist vollbracht:\n'
               'Er sitzet zur Rechten des Vaters.\n', 'v'),
              ('4. Lobsingt seiner Treu´,\ndie immerdar neu,\n'
               'bis Er uns zur Herrlichket führet!\n\n', 'v')],
         'song_book_name': 'Glaubenslieder I',
         'song_number': "1"}
        }

class TestSongBeamerImport(TestCase):
    """
    Test the functions in the :mod:`songbeamerimport` module.
    """
    def create_importer_test(self):
        """
        Test creating an instance of the SongBeamer file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songbeamerimport.SongImport'):
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = SongBeamerImport(mocked_manager)

            # THEN: The importer object should not be None
            self.assertIsNotNone(importer, 'Import should not be none')

    def invalid_import_source_test(self):
        """
        Test SongBeamerImport.doImport handles different invalid import_source values
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songbeamerimport.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = SongBeamerImport(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = True

            # WHEN: Import source is not a list
            for source in ['not a list', 0]:
                importer.import_source = source

                # THEN: doImport should return none and the progress bar maximum should not be set.
                self.assertIsNone(importer.doImport(), 'doImport should return None when import_source is not a list')
                self.assertEquals(mocked_import_wizard.progress_bar.setMaximum.called, False,
                                  'setMaxium on import_wizard.progress_bar should not have been called')

    def valid_import_source_test(self):
        """
        Test SongBeamerImport.doImport handles different invalid import_source values
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch('openlp.plugins.songs.lib.songbeamerimport.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = SongBeamerImport(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = True

            # WHEN: Import source is a list
            importer.import_source = ['List', 'of', 'files']

            # THEN: doImport should return none and the progress bar setMaximum should be called with the length of
            #       import_source.
            self.assertIsNone(importer.doImport(),
                'doImport should return None when import_source is a list and stop_import_flag is True')
            mocked_import_wizard.progress_bar.setMaximum.assert_called_with(len(importer.import_source))

    def file_import_test(self):
        """
        Test the actual import of real song files and check that the imported data is correct.
        """

        # GIVEN: Test files with a mocked out SongImport class, a mocked out "manager", a mocked out "import_wizard",
        #       and mocked out "author", "add_copyright", "add_verse", "finish" methods.
        with patch('openlp.plugins.songs.lib.songbeamerimport.SongImport'):
            for song_file in SONG_TEST_DATA:
                mocked_manager = MagicMock()
                mocked_import_wizard = MagicMock()
                mocked_add_verse = MagicMock()
                mocked_finish = MagicMock()
                mocked_finish.return_value = True
                importer = SongBeamerImport(mocked_manager)
                importer.import_wizard = mocked_import_wizard
                importer.stop_import_flag = False
                importer.addVerse = mocked_add_verse
                importer.finish = mocked_finish

                # WHEN: Importing each file
                importer.import_source = [os.path.join(TEST_PATH, song_file)]
                title = SONG_TEST_DATA[song_file]['title']
                add_verse_calls = SONG_TEST_DATA[song_file]['verses']
                song_book_name = SONG_TEST_DATA[song_file]['song_book_name']
                song_number = SONG_TEST_DATA[song_file]['song_number']

                # THEN: doImport should return none, the song data should be as expected, and finish should have been
                #       called.
                self.assertIsNone(importer.doImport(), 'doImport should return None when it has completed')
                self.assertEquals(importer.title, title, 'title for %s should be "%s"' % (song_file, title))
                for verse_text, verse_tag in add_verse_calls:
                    mocked_add_verse.assert_any_call(verse_text, verse_tag)
                if song_book_name:
                    self.assertEquals(importer.songBookName, song_book_name, 'songBookName for %s should be "%s"'
                        % (song_file, song_book_name))
                if song_number:
                    self.assertEquals(importer.songNumber, song_number, 'songNumber for %s should be %s'
                        % (song_file, song_number))
                mocked_finish.assert_called_with()
