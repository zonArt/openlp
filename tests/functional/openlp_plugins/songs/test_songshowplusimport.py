"""
This module contains tests for the SongShow Plus song importer.
"""

import os
from unittest import TestCase
from mock import patch, MagicMock

from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.songshowplusimport import SongShowPlusImport

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'../../../resources/songshowplussongs'))
SONG_TEST_DATA = {u'Amazing Grace.sbsong':
        {u'title': u'Amazing Grace (Demonstration)',
         u'authors': [u'John Newton', u'Edwin Excell', u'John P. Rees'],
         u'copyright': u'Public Domain ',
         u'ccli_number': 22025,
         u'verses':
             [(u'Amazing grace! How sweet the sound!\r\nThat saved a wretch like me!\r\n'
               u'I once was lost, but now am found;\r\nWas blind, but now I see.', u'v1'),
              (u'\'Twas grace that taught my heart to fear,\r\nAnd grace my fears relieved.\r\n'
               u'How precious did that grace appear,\r\nThe hour I first believed.', u'v2'),
              (u'The Lord has promised good to me,\r\nHis Word my hope secures.\r\n'
               u'He will my shield and portion be\r\nAs long as life endures.', u'v3'),
              (u'Thro\' many dangers, toils and snares\r\nI have already come.\r\n'
               u'\'Tis grace that brought me safe thus far,\r\nAnd grace will lead me home.', u'v4'),
              (u'When we\'ve been there ten thousand years,\r\nBright shining as the sun,\r\n'
               u'We\'ve no less days to sing God\'s praise,\r\nThan when we first begun.', u'v5')],
         u'topics': [u'Assurance', u'Grace', u'Praise', u'Salvation'],
         u'comments': u'\n\n\n',
         u'song_book_name': u'Demonstration Songs',
         u'song_number': 0,
         u'verse_order_list': []},
    u'Beautiful Garden Of Prayer.sbsong':
        {u'title': u'Beautiful Garden Of Prayer (Demonstration)',
        u'authors': [u'Eleanor Allen Schroll', u'James H. Fillmore'],
        u'copyright': u'Public Domain ',
        u'ccli_number': 60252,
        u'verses':
           [(u'There\'s a garden where Jesus is waiting,\r\nThere\'s a place that is wondrously fair.\r\n'
             u'For it glows with the light of His presence,\r\n\'Tis the beautiful garden of prayer.', u'v1'),
            (u'There\'s a garden where Jesus is waiting,\r\nAnd I go with my burden and care.\r\n'
             u'Just to learn from His lips, words of comfort,\r\nIn the beautiful garden of prayer.', u'v2'),
            (u'There\'s a garden where Jesus is waiting,\r\nAnd He bids you to come meet Him there,\r\n'
             u'Just to bow and receive a new blessing,\r\nIn the beautiful garden of prayer.', u'v3'),
            (u'O the beautiful garden, the garden of prayer,\r\nO the beautiful garden of prayer.\r\n'
             u'There my Savior awaits, and He opens the gates\r\nTo the beautiful garden of prayer.', u'c1')],
        u'topics': [u'Devotion', u'Prayer'],
        u'comments': u'',
        u'song_book_name': u'',
        u'song_number': 0,
        u'verse_order_list': []}}


class TestSongShowPlusImport(TestCase):
    """
    Test the functions in the :mod:`songshowplusimport` module.
    """
    def create_importer_test(self):
        """
        Test creating an instance of the SongShow Plus file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = SongShowPlusImport(mocked_manager)

            # THEN: The importer object should not be None
            self.assertIsNotNone(importer, u'Import should not be none')

    def invalid_import_source_test(self):
        """
        Test SongShowPlusImport.doImport handles different invalid import_source values
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = SongShowPlusImport(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = True

            # WHEN: Import source is not a list
            for source in [u'not a list', 0]:
                importer.import_source = source

                # THEN: doImport should return none and the progress bar maximum should not be set.
                self.assertIsNone(importer.doImport(), u'doImport should return None when import_source is not a list')
                self.assertEquals(mocked_import_wizard.progress_bar.setMaximum.called, False,
                                  u'setMaxium on import_wizard.progress_bar should not have been called')

    def valid_import_source_test(self):
        """
        Test SongShowPlusImport.doImport handles different invalid import_source values
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = SongShowPlusImport(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = True

            # WHEN: Import source is a list
            importer.import_source = [u'List', u'of', u'files']

            # THEN: doImport should return none and the progress bar setMaximum should be called with the length of
            #       import_source.
            self.assertIsNone(importer.doImport(),
                u'doImport should return None when import_source is a list and stop_import_flag is True')
            mocked_import_wizard.progress_bar.setMaximum.assert_called_with(len(importer.import_source))

    def to_openlp_verse_tag_test(self):
        """
        Test to_openlp_verse_tag method by simulating adding a verse
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            importer = SongShowPlusImport(mocked_manager)

            # WHEN: Supplied with the following arguments replicating verses being added
            test_values = [(u'Verse 1', VerseType.tags[VerseType.Verse] + u'1'),
                (u'Verse 2', VerseType.tags[VerseType.Verse] + u'2'),
                (u'verse1', VerseType.tags[VerseType.Verse] + u'1'),
                (u'Verse', VerseType.tags[VerseType.Verse] + u'1'),
                (u'Verse1', VerseType.tags[VerseType.Verse] + u'1'),
                (u'chorus 1', VerseType.tags[VerseType.Chorus] + u'1'),
                (u'bridge 1', VerseType.tags[VerseType.Bridge] + u'1'),
                (u'pre-chorus 1', VerseType.tags[VerseType.PreChorus] + u'1'),
                (u'different 1', VerseType.tags[VerseType.Other] + u'1'),
                (u'random 1', VerseType.tags[VerseType.Other] + u'2')]

            # THEN: The returned value should should correlate with the input arguments
            for original_tag, openlp_tag in test_values:
                self.assertEquals(importer.to_openlp_verse_tag(original_tag), openlp_tag,
                    u'SongShowPlusImport.to_openlp_verse_tag should return "%s" when called with "%s"'
                    % (openlp_tag, original_tag))

    def to_openlp_verse_tag_verse_order_test(self):
        """
        Test to_openlp_verse_tag method by simulating adding a verse to the verse order
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            importer = SongShowPlusImport(mocked_manager)

            # WHEN: Supplied with the following arguments replicating a verse order being added
            test_values = [(u'Verse 1', VerseType.tags[VerseType.Verse] + u'1'),
                (u'Verse 2', VerseType.tags[VerseType.Verse] + u'2'),
                (u'verse1', VerseType.tags[VerseType.Verse] + u'1'),
                (u'Verse', VerseType.tags[VerseType.Verse] + u'1'),
                (u'Verse1', VerseType.tags[VerseType.Verse] + u'1'),
                (u'chorus 1', VerseType.tags[VerseType.Chorus] + u'1'),
                (u'bridge 1', VerseType.tags[VerseType.Bridge] + u'1'),
                (u'pre-chorus 1', VerseType.tags[VerseType.PreChorus] + u'1'),
                (u'different 1', VerseType.tags[VerseType.Other] + u'1'),
                (u'random 1', VerseType.tags[VerseType.Other] + u'2'),
                (u'unused 2', None)]

            # THEN: The returned value should should correlate with the input arguments
            for original_tag, openlp_tag in test_values:
                self.assertEquals(importer.to_openlp_verse_tag(original_tag, ignore_unique=True), openlp_tag,
                    u'SongShowPlusImport.to_openlp_verse_tag should return "%s" when called with "%s"'
                    % (openlp_tag, original_tag))

    def file_import_test(self):
        """
        Test the actual import of real song files and check that the imported data is correct.
        """

        # GIVEN: Test files with a mocked out SongImport class, a mocked out "manager", a mocked out "import_wizard",
        #       and mocked out "author", "add_copyright", "add_verse", "finish" methods.
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            for song_file in SONG_TEST_DATA:
                mocked_manager = MagicMock()
                mocked_import_wizard = MagicMock()
                mocked_parse_author = MagicMock()
                mocked_add_copyright = MagicMock()
                mocked_add_verse = MagicMock()
                mocked_finish = MagicMock()
                mocked_finish.return_value = True
                importer = SongShowPlusImport(mocked_manager)
                importer.import_wizard = mocked_import_wizard
                importer.stop_import_flag = False
                importer.parse_author = mocked_parse_author
                importer.addCopyright = mocked_add_copyright
                importer.addVerse = mocked_add_verse
                importer.finish = mocked_finish
                importer.topics = []

                # WHEN: Importing each file
                importer.import_source = [os.path.join(TEST_PATH, song_file)]
                title = SONG_TEST_DATA[song_file][u'title']
                author_calls = SONG_TEST_DATA[song_file][u'authors']
                song_copyright = SONG_TEST_DATA[song_file][u'copyright']
                ccli_number = SONG_TEST_DATA[song_file][u'ccli_number']
                add_verse_calls = SONG_TEST_DATA[song_file][u'verses']
                topics = SONG_TEST_DATA[song_file][u'topics']
                comments = SONG_TEST_DATA[song_file][u'comments']
                song_book_name = SONG_TEST_DATA[song_file][u'song_book_name']
                song_number = SONG_TEST_DATA[song_file][u'song_number']
                verse_order_list = SONG_TEST_DATA[song_file][u'verse_order_list']

                # THEN: doImport should return none, the song data should be as expected, and finish should have been
                #       called.
                self.assertIsNone(importer.doImport(), u'doImport should return None when it has completed')
                self.assertEquals(importer.title, title, u'title for %s should be "%s"' % (song_file, title))
                for author in author_calls:
                    mocked_parse_author.assert_any_call(author)
                if song_copyright:
                    mocked_add_copyright.assert_called_with(song_copyright)
                if ccli_number:
                    self.assertEquals(importer.ccliNumber, ccli_number, u'ccliNumber for %s should be %s'
                        % (song_file, ccli_number))
                for verse_text, verse_tag in add_verse_calls:
                    mocked_add_verse.assert_any_call(verse_text, verse_tag)
                if topics:
                    self.assertEquals(importer.topics, topics, u'topics for %s should be %s' % (song_file, topics))
                if comments:
                    self.assertEquals(importer.comments, comments, u'comments for %s should be "%s"'
                        % (song_file, comments))
                if song_book_name:
                    self.assertEquals(importer.songBookName, song_book_name, u'songBookName for %s should be "%s"'
                        % (song_file, song_book_name))
                if song_number:
                    self.assertEquals(importer.songNumber, song_number, u'songNumber for %s should be %s'
                        % (song_file, song_number))
                if verse_order_list:
                    self.assertEquals(importer.verseOrderList, [], u'verseOrderList for %s should be %s'
                        % (song_file, verse_order_list))
                mocked_finish.assert_called_with()
