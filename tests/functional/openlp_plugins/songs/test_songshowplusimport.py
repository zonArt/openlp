"""
This module contains tests for the OpenLP song importer.
"""

import os
from unittest import TestCase
from mock import call, patch, MagicMock

from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.songshowplusimport import SongShowPlusImport

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'../../../resources'))

class TestSongShowPlusFileImport(TestCase):
    """
    Test the functions in the :mod:`lib` module.
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

    def toOpenLPVerseTag_test(self):
        """
        Test toOpenLPVerseTag method
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
                self.assertEquals(importer.toOpenLPVerseTag(original_tag), openlp_tag,
                    u'SongShowPlusImport.toOpenLPVerseTag should return "%s" when called with "%s"'
                    % (openlp_tag, original_tag))

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
                self.assertEquals(importer.toOpenLPVerseTag(original_tag, ignore_unique=True), openlp_tag,
                    u'SongShowPlusImport.toOpenLPVerseTag should return "%s" when called with "%s"'
                    % (openlp_tag, original_tag))




    def import_source_test(self):
        """
        Test creating an instance of the SongShow Plus file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            importer = SongShowPlusImport(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = True

            # WHEN: Import source is a string
            importer.import_source = u'not a list'

            # THEN: doImport should return none and the progress bar maximum should not be set.
            self.assertIsNone(importer.doImport(), u'doImport should return None when import_source is not a list')
            self.assertEquals(mocked_import_wizard.progress_bar.setMaximum.called, False,
                u'setMaxium on import_wizard.progress_bar should not have been called')

            # WHEN: Import source is an int
            importer.import_source = 0

            # THEN: doImport should return none and the progress bar maximum should not be set.
            self.assertIsNone(importer.doImport(), u'doImport should return None when import_source is not a list')
            self.assertEquals(mocked_import_wizard.progress_bar.setMaximum.called, False,
                u'setMaxium on import_wizard.progress_bar should not have been called')

            # WHEN: Import source is a list
            importer.import_source = [u'List', u'of', u'files']

            # THEN: doImport should return none and the progress bar maximum should be set.
            self.assertIsNone(importer.doImport(),
                u'doImport should return None when import_source is a list and stop_import_flag is True')
            mocked_import_wizard.progress_bar.setMaximum.assert_called_with(
                len(importer.import_source))

    def file_import_test(self):
        """
        Test creating an instance of the SongShow Plus file importer
        """

        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
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

            # WHEN: Import source is a string
            importer.import_source = [os.path.join(TEST_PATH, u'Amazing Grace.sbsong')]

            # THEN: doImport should return none and the progress bar maximum should not be set.
            self.assertIsNone(importer.doImport(), u'doImport should return None when import_source is not a list')
            self.assertEquals(importer.title, u'Amazing Grace (Demonstration)',
                              u'Title for Amazing Grace.sbsong should be "Amazing Grace (Demonstration)"')
            calls = [call(u'John Newton'), call(u'Edwin Excell'), call(u'John P. Rees')]
            mocked_parse_author.assert_has_calls(calls)
            mocked_add_copyright.assert_called_with(u'Public Domain ')
            self.assertEquals(importer.ccliNumber, 22025, u'ccliNumber should be set as 22025 for Amazing Grace.sbsong')
            calls = [call(u'Amazing grace! How sweet the sound!\r\nThat saved a wretch like me!\r\n'
                          u'I once was lost, but now am found;\r\nWas blind, but now I see.', u'v1'),
                     call(u"'Twas grace that taught my heart to fear,\r\nAnd grace my fears relieved.\r\n"
                          u"How precious did that grace appear,\r\nThe hour I first believed.", u'v2'),
                     call(u'The Lord has promised good to me,\r\nHis Word my hope secures.\r\n'
                          u'He will my shield and portion be\r\nAs long as life endures.', u'v3'),
                     call(u"Thro' many dangers, toils and snares\r\nI have already come.\r\n"
                          u"'Tis grace that brought me safe thus far,\r\nAnd grace will lead me home.", u'v4'),
                     call(u"When we've been there ten thousand years,\r\nBright shining as the sun,\r\n"
                          u"We've no less days to sing God's praise,\r\nThan when we first begun.", u'v5')]
            mocked_add_verse.assert_has_calls(calls)
            self.assertEquals(importer.topics, [u'Assurance', u'Grace', u'Praise', u'Salvation'])
            self.assertEquals(importer.comments, u'\n\n\n', u'comments should be "\\n\\n\\n" Amazing Grace.sbsong')
            self.assertEquals(importer.songBookName, u'Demonstration Songs', u'songBookName should be '
                u'"Demonstration Songs"')
            self.assertEquals(importer.songNumber, 0, u'songNumber should be 0')
            self.assertEquals(importer.verseOrderList, [], u'verseOrderList should be empty')
            mocked_finish.assert_called_with()