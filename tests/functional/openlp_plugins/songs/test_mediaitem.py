"""
This module contains tests for the lib submodule of the Songs plugin.
"""
from unittest import TestCase

from PyQt4 import QtCore, QtGui

from openlp.core.common import Registry, Settings
from openlp.core.lib import ServiceItem
from openlp.plugins.songs.lib.mediaitem import SongMediaItem
from openlp.plugins.songs.lib.db import AuthorType
from tests.functional import patch, MagicMock
from tests.helpers.testmixin import TestMixin


class TestMediaItem(TestCase, TestMixin):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Set up the components need for all tests.
        """
        Registry.create()
        Registry().register('service_list', MagicMock())
        Registry().register('main_window', MagicMock())
        with patch('openlp.core.lib.mediamanageritem.MediaManagerItem._setup'), \
                patch('openlp.plugins.songs.forms.editsongform.EditSongForm.__init__'):
            self.media_item = SongMediaItem(None, MagicMock())
            self.media_item.display_songbook = False
        self.get_application()
        self.build_settings()
        QtCore.QLocale.setDefault(QtCore.QLocale('en_GB'))

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.destroy_settings()

    def build_song_footer_one_author_test(self):
        """
        Test build songs footer with basic song and one author
        """
        # GIVEN: A Song and a Service Item
        mock_song = MagicMock()
        mock_song.title = 'My Song'
        mock_song.authors_songs = []
        mock_author = MagicMock()
        mock_author.display_name = 'my author'
        mock_author_song = MagicMock()
        mock_author_song.author = mock_author
        mock_song.authors_songs.append(mock_author_song)
        mock_song.copyright = 'My copyright'
        service_item = ServiceItem(None)

        # WHEN: I generate the Footer with default settings
        author_list = self.media_item.generate_footer(service_item, mock_song)

        # THEN: I get the following Array returned
        self.assertEqual(service_item.raw_footer, ['My Song', 'Written by: my author', 'My copyright'],
                         'The array should be returned correctly with a song, one author and copyright')
        self.assertEqual(author_list, ['my author'],
                         'The author list should be returned correctly with one author')

    def build_song_footer_two_authors_test(self):
        """
        Test build songs footer with basic song and two authors
        """
        # GIVEN: A Song and a Service Item
        mock_song = MagicMock()
        mock_song.title = 'My Song'
        mock_song.authors_songs = []
        mock_author = MagicMock()
        mock_author.display_name = 'my author'
        mock_author_song = MagicMock()
        mock_author_song.author = mock_author
        mock_author_song.author_type = AuthorType.Music
        mock_song.authors_songs.append(mock_author_song)
        mock_author = MagicMock()
        mock_author.display_name = 'another author'
        mock_author_song = MagicMock()
        mock_author_song.author = mock_author
        mock_author_song.author_type = AuthorType.Words
        mock_song.authors_songs.append(mock_author_song)
        mock_author = MagicMock()
        mock_author.display_name = 'translator'
        mock_author_song = MagicMock()
        mock_author_song.author = mock_author
        mock_author_song.author_type = AuthorType.Translation
        mock_song.authors_songs.append(mock_author_song)
        mock_song.copyright = 'My copyright'
        service_item = ServiceItem(None)

        # WHEN: I generate the Footer with default settings
        author_list = self.media_item.generate_footer(service_item, mock_song)

        # THEN: I get the following Array returned
        self.assertEqual(service_item.raw_footer, ['My Song', 'Words: another author', 'Music: my author',
                                                   'Translation: translator',  'My copyright'],
                         'The array should be returned correctly with a song, two authors and copyright')
        self.assertEqual(author_list, ['another author', 'my author', 'translator'],
                         'The author list should be returned correctly with two authors')

    def build_song_footer_base_ccli_test(self):
        """
        Test build songs footer with basic song and a CCLI number
        """
        # GIVEN: A Song and a Service Item and a configured CCLI license
        mock_song = MagicMock()
        mock_song.title = 'My Song'
        mock_song.copyright = 'My copyright'
        service_item = ServiceItem(None)
        Settings().setValue('core/ccli number', '1234')

        # WHEN: I generate the Footer with default settings
        self.media_item.generate_footer(service_item, mock_song)

        # THEN: I get the following Array returned
        self.assertEqual(service_item.raw_footer, ['My Song', 'My copyright', 'CCLI License: 1234'],
                         'The array should be returned correctly with a song, an author, copyright and ccli')

        # WHEN: I amend the CCLI value
        Settings().setValue('core/ccli number', '4321')
        self.media_item.generate_footer(service_item, mock_song)

        # THEN: I would get an amended footer string
        self.assertEqual(service_item.raw_footer, ['My Song', 'My copyright', 'CCLI License: 4321'],
                         'The array should be returned correctly with a song, an author, copyright and amended ccli')

    def build_song_footer_base_songbook_test(self):
        """
        Test build songs footer with basic song and a songbook
        """
        # GIVEN: A Song and a Service Item
        mock_song = MagicMock()
        mock_song.title = 'My Song'
        mock_song.copyright = 'My copyright'
        mock_song.book = MagicMock()
        mock_song.book.name = "My songbook"
        mock_song.song_number = 12
        service_item = ServiceItem(None)

        # WHEN: I generate the Footer with default settings
        self.media_item.generate_footer(service_item, mock_song)

        # THEN: The songbook should not be in the footer
        self.assertEqual(service_item.raw_footer, ['My Song', 'My copyright'])

        # WHEN: I activate the "display songbook" option
        self.media_item.display_songbook = True
        self.media_item.generate_footer(service_item, mock_song)

        # THEN: The songbook should be in the footer
        self.assertEqual(service_item.raw_footer, ['My Song', 'My copyright', 'My songbook #12'])
