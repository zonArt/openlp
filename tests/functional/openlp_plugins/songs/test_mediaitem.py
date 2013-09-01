"""
This module contains tests for the lib submodule of the Songs plugin.
"""
import os
from tempfile import mkstemp
from unittest import TestCase

from mock import patch, MagicMock

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Registry, ServiceItem, Settings

from openlp.plugins.songs.lib.mediaitem import SongMediaItem


class TestMediaItem(TestCase):
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
        with patch('openlp.core.lib.mediamanageritem.MediaManagerItem.__init__'), \
                patch('openlp.plugins.songs.forms.editsongform.EditSongForm.__init__'):
            self.media_item = SongMediaItem(MagicMock(), MagicMock())

        fd, self.ini_file = mkstemp('.ini')
        Settings().set_filename(self.ini_file)
        self.application = QtGui.QApplication.instance()
        QtCore.QLocale.setDefault(QtCore.QLocale('en_GB'))

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application
        # Not all tests use settings!
        try:
            os.unlink(self.ini_file)
            os.unlink(Settings().fileName())
        except Exception:
            pass

    def build_song_footer_one_author_test(self):
        """
        Test build songs footer with basic song and one author
        """
        # GIVEN: A Song and a Service Item
        mock_song = MagicMock()
        mock_song.title = 'My Song'
        mock_author = MagicMock()
        mock_author.display_name = 'my author'
        mock_song.authors = []
        mock_song.authors.append(mock_author)
        mock_song.copyright = 'My copyright'
        service_item = ServiceItem(None)

        # WHEN: I generate the Footer with default settings
        author_list = self.media_item.generate_footer(service_item, mock_song)

        # THEN: I get the following Array returned
        self.assertEqual(service_item.raw_footer, ['My Song', 'my author', 'My copyright'],
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
        mock_author = MagicMock()
        mock_author.display_name = 'my author'
        mock_song.authors = []
        mock_song.authors.append(mock_author)
        mock_author = MagicMock()
        mock_author.display_name = 'another author'
        mock_song.authors.append(mock_author)
        mock_song.copyright = 'My copyright'
        service_item = ServiceItem(None)

        # WHEN: I generate the Footer with default settings
        author_list = self.media_item.generate_footer(service_item, mock_song)

        # THEN: I get the following Array returned
        self.assertEqual(service_item.raw_footer, ['My Song', 'my author and another author', 'My copyright'],
                         'The array should be returned correctly with a song, two authors and copyright')
        self.assertEqual(author_list, ['my author', 'another author'],
                         'The author list should be returned correctly with two authors')

    def build_song_footer_base_ccli_test(self):
        """
        Test build songs footer with basic song and two authors
        """
        # GIVEN: A Song and a Service Item and a configured CCLI license
        mock_song = MagicMock()
        mock_song.title = 'My Song'
        mock_author = MagicMock()
        mock_author.display_name = 'my author'
        mock_song.authors = []
        mock_song.authors.append(mock_author)
        mock_song.copyright = 'My copyright'
        service_item = ServiceItem(None)
        Settings().setValue('core/ccli number', '1234')

        # WHEN: I generate the Footer with default settings
        self.media_item.generate_footer(service_item, mock_song)

        # THEN: I get the following Array returned
        self.assertEqual(service_item.raw_footer, ['My Song', 'my author', 'My copyright', 'CCLI License: 1234'],
                         'The array should be returned correctly with a song, an author, copyright and ccli')

        # WHEN: I amend the CCLI value
        Settings().setValue('core/ccli number', '4321')
        self.media_item.generate_footer(service_item, mock_song)

        # THEN: I would get an amended footer string
        self.assertEqual(service_item.raw_footer, ['My Song', 'my author', 'My copyright', 'CCLI License: 4321'],
                         'The array should be returned correctly with a song, an author, copyright and amended ccli')
