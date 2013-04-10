# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

"""
This module contains tests for the EasyWorship song importer.
"""

import os
from unittest import TestCase
from mock import call, patch, MagicMock

from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.ewimport import EasyWorshipSongImport, FieldDescEntry

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'../../../resources/easyworshipsongs'))
SONG_TEST_DATA = [{u'title': u'Amazing Grace (Demonstration)',
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
                   u'verse_order_list': []}]


class TestFieldDesc:
    def __init__(self, name, field_type, size):
        self.name = name
        self.type = field_type
        self.size = size

TEST_DATA_ENCODING = u'cp1252'
TEST_FIELD_DESCS = [TestFieldDesc(u'Title', 1, 50), TestFieldDesc(u'Text Percentage Bottom', 3, 2),
    TestFieldDesc(u'RecID', 4, 4), TestFieldDesc(u'Default Background', 9, 1), TestFieldDesc(u'Words', 12, 250),
    TestFieldDesc(u'Words', 12, 250), TestFieldDesc(u'BK Bitmap', 13, 10), TestFieldDesc(u'Last Modified', 21, 10)]
TEST_FIELDS = ['A Heart Like Thine\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0', 32868, 2147483750,
    129, '{\\rtf1\\ansi\\deff0\\deftab254{\\fonttbl{\\f0\\fnil\\fcharset0 Arial;}{\\f1\\fnil\\fcharset0 Verdana;}}'
    '{\\colortbl\\red0\\green0\\blue0;\\red255\\green0\\blue0;\\red0\\green128\\blue0;\\red0\\green0\\blue255;'
    '\\red255\\green255\\blue0;\\red255\\green0\\blue255;\\red128\\g��\7\0f\r\0\0\1\0',
    '{\\rtf1\\ansi\\deff0\\deftab254{\\fonttbl{\\f0\\fnil\\fcharset0 Arial;}{\\f1\\fnil\\fcharset0 Verdana;}}'
    '{\\colortbl\\red0\\green0\\blue0;\\red255\\green0\\blue0;\\red0\\green128\\blue0;\\red0\\green0\\blue255;\\red255'
    '\\green255\\blue0;\\red255\\green0\\blue255;\\red128\\g>�\6\0�\6\0\0\1\0', '\0\0\0\0\0\0\0\0\0\0', 0]
GET_MEMO_FIELD_TEST_RESULTS = [
    (4, u'\2', {u'return': u'\2',u'read': (1, 3430), u'seek': (507136, (8, os.SEEK_CUR))}),
    (4, u'\3', {u'return': u'', u'read': (1, ), u'seek': (507136, )}),
    (5, u'\3', {u'return': u'\3', u'read': (1, 1725), u'seek': (3220111360L, (41L, os.SEEK_CUR), 3220111408L)}),
    (5, u'\4', {u'return': u'', u'read': (), u'seek': ()})]

class TestEasyWorshipSongImport(TestCase):
    """
    Test the functions in the :mod:`ewimport` module.
    """
    def create_field_desc_entry_test(self):
        """
        Test creating an instance of the :class`FieldDescEntry` class.
        """
        # GIVEN: Set arguments
        name = u'Title'
        field_type = 1
        size = 50

        # WHEN: A FieldDescEntry object is created.
        field_desc_entry = FieldDescEntry(name, field_type, size)

        # THEN:
        self.assertIsNotNone(field_desc_entry, u'Import should not be none')
        self.assertEquals(field_desc_entry.name, name, u'FieldDescEntry.name should be the same as the name argument')
        self.assertEquals(field_desc_entry.type, field_type,
            u'FieldDescEntry.type should be the same as the typeargument')
        self.assertEquals(field_desc_entry.size, size, u'FieldDescEntry.size should be the same as the size argument')

    def create_importer_test(self):
        """
        Test creating an instance of the EasyWorship file importer
        """
        # GIVEN: A mocked out SongImport class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'):
            mocked_manager = MagicMock()

            # WHEN: An importer object is created
            importer = EasyWorshipSongImport(mocked_manager)

            # THEN: The importer object should not be None
            self.assertIsNotNone(importer, u'Import should not be none')

    def find_field_exists_test(self):
        """
        Test finding an existing field in a given list using the :mod:`findField`
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a list of field descriptions
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'):
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            importer.fieldDescs = TEST_FIELD_DESCS

            # WHEN: Given a field name that exists
            existing_fields = [u'Title', u'Text Percentage Bottom', u'RecID', u'Default Background', u'Words',
                u'BK Bitmap', u'Last Modified']

            # THEN: The item corresponding the index returned should have the same name attribute
            for field_name in existing_fields:
                self.assertEquals(importer.fieldDescs[importer.findField(field_name)].name, field_name)

    def find_field_non_exists_test(self):
        """
        Test finding an non-existing field in a given list using the :mod:`findField`
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and a list of field descriptions
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'):
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            importer.fieldDescs = TEST_FIELD_DESCS

            # WHEN: Given a field name that does not exist
            non_existing_fields = [u'BK Gradient Shading', u'BK Gradient Variant', u'Favorite', u'Copyright']

            # THEN: The importer object should not be None
            for field_name in non_existing_fields:
                self.assertRaises(IndexError, importer.findField, field_name)

    def set_record_struct_test(self):
        """
        Test the :mod:`setRecordStruct` module
        """
        # GIVEN: A mocked out SongImport class, a mocked out struct class, and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.ewimport.struct') as mocked_struct:
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)

            # WHEN: Called with a list of field descriptions

            # THEN: setRecordStruct should return None and structStruct should be called with a value representing
            #       the list of field descriptions
            self.assertIsNone(importer.setRecordStruct(TEST_FIELD_DESCS), u'setRecordStruct should return None')
            mocked_struct.Struct.assert_called_with('>50sHIB250s250s10sQ')

    def get_field_test(self):
        """
        Test the :mod:`getField` module
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager" and an encoding
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'):
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            importer.encoding = TEST_DATA_ENCODING

            # WHEN: Supplied with string with just NULL bytes, or an int with the value 0
            importer.fields = TEST_FIELDS
            importer.fieldDescs = TEST_FIELD_DESCS
            field_results = [(0, 'A Heart Like Thine'), (1, 100), (2, 102L), (3, True), (6, None), (7, None)]

            # THEN: getField should return None
            for field_index, result in field_results:
                self.assertEquals(importer.getField(field_index), result,
                    u'getField should return "%s" when called with "%s"' % (result, TEST_FIELDS[field_index]))

    def get_memo_field_test(self):
        """
        Test the :mod:`getField` module
        """
        for test_results in GET_MEMO_FIELD_TEST_RESULTS:
            # GIVEN: A mocked out SongImport class, a mocked out "manager", a mocked out memo_file and an encoding
            with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'):
                mocked_manager = MagicMock()
                mocked_memo_file = MagicMock()
                importer = EasyWorshipSongImport(mocked_manager)
                importer.memoFile = mocked_memo_file
                importer.encoding = TEST_DATA_ENCODING

                # WHEN: Supplied with test fields and test field descriptions
                importer.fields = TEST_FIELDS
                importer.fieldDescs = TEST_FIELD_DESCS
                field_index = test_results[0]
                mocked_memo_file.read.return_value = test_results[1]
                get_field_result = test_results[2][u'return']
                get_field_read_calls = test_results[2][u'read']
                get_field_seek_calls = test_results[2][u'seek']

                # THEN: getField should return the appropriate value with the appropriate mocked objects being called
                self.assertEquals(importer.getField(field_index), get_field_result)
                for call in get_field_read_calls:
                    mocked_memo_file.read.assert_any_call(call)
                for call in get_field_seek_calls:
                    if isinstance(call, (int, long)):
                        mocked_memo_file.seek.assert_any_call(call)
                    else:
                        mocked_memo_file.seek.assert_any_call(call[0], call[1])

    def do_import_source_test(self):
        """
        Test the :mod:`doImport` module
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.ewimport.os.path') as mocked_os_path:
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            mocked_os_path.isfile.return_value = False

            # WHEN: Supplied with an import source
            importer.import_source = u'Songs.DB'

            # THEN: doImport should return None having called os.path.isfile
            self.assertIsNone(importer.doImport(), u'doImport should return None')
            mocked_os_path.isfile.assert_any_call(u'Songs.DB')
            mocked_os_path.isfile.assert_any_call(u'Songs.MB')

    def do_import_source_validity_test(self):
        """
        Test the :mod:`doImport` module
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.ewimport.os.path') as mocked_os_path, \
            patch(u'__builtin__.open') as mocked_open:
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            mocked_os_path.isfile.return_value = True
            importer.import_source = u'Songs.DB'

            # WHEN: DB file size is less than 0x800
            mocked_os_path.getsize.return_value = 0x7FF

            # THEN: doImport should return None having called os.path.isfile
            self.assertIsNone(importer.doImport(), u'doImport should return None when db_size is less than 0x800')
            mocked_os_path.getsize.assert_any_call(u'Songs.DB')


    def file_import_test(self):
        """
        Test the actual import of real song files and check that the imported data is correct.
        """

        # GIVEN: Test files with a mocked out SongImport class, a mocked out "manager", a mocked out "import_wizard",
        #       and mocked out "author", "add_copyright", "add_verse", "finish" methods.
        with patch(u'openlp.plugins.songs.lib.songshowplusimport.SongImport'):
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            mocked_parse_author = MagicMock()
            mocked_add_copyright = MagicMock()
            mocked_add_verse = MagicMock()
            mocked_finish = MagicMock()
            mocked_finish.return_value = True
            importer = EasyWorshipSongImport(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = False
            importer.parse_author = mocked_parse_author
            importer.addCopyright = mocked_add_copyright
            importer.addVerse = mocked_add_verse
            importer.finish = mocked_finish
            importer.topics = []

            # WHEN: Importing each file
            importer.import_source = [os.path.join(TEST_PATH, u'Songs.DB')]
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

            # Open the DB and MB files if they exist
    #        import_source_mb = self.import_source.replace('.DB', '.MB')
     #       if not (os.path.isfile(self.import_source) or os.path.isfile(import_source_mb)):
      #          return
       #     db_size = os.path.getsize(self.import_source)
        #    if db_size < 0x800:
         #       return
    # TODO: Write doImport Tests