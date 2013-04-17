# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

"""
This module contains tests for the EasyWorship song importer.
"""

import os
from unittest import TestCase
from mock import patch, MagicMock

from openlp.plugins.songs.lib.ewimport import EasyWorshipSongImport, FieldDescEntry

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'../../../resources/easyworshipsongs'))
SONG_TEST_DATA = [{u'title': u'Amazing Grace',
                   u'authors': [u'John Newton'],
                   u'copyright': u'Public Domain',
                   u'ccli_number': 0,
                   u'verses':
                       [(u'Amazing grace how sweet the sound,\nThat saved a wretch like me;\n'
                         u'I once was lost, but now am found\nWas blind, but now I see.', u'v1'),
                        (u'T\'was grace that taught my heart to fear,\nAnd grace my fears relieved;\n'
                         u'How precious did that grace appear\nThe hour I first believed.', u'v2'),
                        (u'Through many dangers, toil and snares,\nI have already come;\n'
                         u'\'Tis grace has brought me safe thus far,\nAnd grace will lead me home.', u'v3'),
                        (u'When we\'ve been there ten thousand years\nBright shining as the sun,\n'
                         u'We\'ve no less days to sing God\'s praise\nThan when we\'ve first begun.', u'v4')],
                   u'verse_order_list': []},
                  {u'title': u'Beautiful Garden Of Prayer',
                   u'authors': [u'Eleanor Allen Schroll James H. Fillmore'],
                   u'copyright': u'Public Domain',
                   u'ccli_number': 0,
                   u'verses':
                       [(u'O the beautiful garden, the garden of prayer,\nO the beautiful garden of prayer.\n'
                         u'There my Savior awaits, and He opens the gates\nTo the beautiful garden of prayer.', u'c1'),
                        (u'There\'s a garden where Jesus is waiting,\nThere\'s a place that is wondrously fair.\n'
                         u'For it glows with the light of His presence,\n\'Tis the beautiful garden of prayer.', u'v1'),
                        (u'There\'s a garden where Jesus is waiting,\nAnd I go with my burden and care.\n'
                         u'Just to learn from His lips, words of comfort,\nIn the beautiful garden of prayer.', u'v2'),
                        (u'There\'s a garden where Jesus is waiting,\nAnd He bids you to come meet Him there,\n'
                         u'Just to bow and receive a new blessing,\nIn the beautiful garden of prayer.', u'v3')],
                   u'verse_order_list': []}]

class EasyWorshipSongImportLogger(EasyWorshipSongImport):
    """
    This class logs changes in the title instance variable
    """
    _title_assignment_list = []

    def __init__(self, manager):
        EasyWorshipSongImport.__init__(self, manager)

    @property
    def title(self):
        return self._title_assignment_list[-1]

    @title.setter
    def title(self, title):
        self._title_assignment_list.append(title)

class TestFieldDesc:
    def __init__(self, name, field_type, size):
        self.name = name
        self.type = field_type
        self.size = size

TEST_DATA_ENCODING = u'cp1252'
CODE_PAGE_MAPPINGS = [(852, u'cp1250'), (737, u'cp1253'), (775, u'cp1257'), (855, u'cp1251'), (857, u'cp1254'),
    (866,  u'cp1251'), (869, u'cp1253'), (862, u'cp1255'), (874, u'cp874')]
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

    def find_non_existing_field_test(self):
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

            # WHEN: Supplied with some test data and known results
            importer.fields = TEST_FIELDS
            importer.fieldDescs = TEST_FIELD_DESCS
            field_results = [(0, 'A Heart Like Thine'), (1, 100), (2, 102L), (3, True), (6, None), (7, None)]

            # THEN: getField should return the known results
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
        Test the :mod:`doImport` module opens the correct files
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

    def do_import_database_validity_test(self):
        """
        Test the :mod:`doImport` module handles invalid database files correctly
        """
        # GIVEN: A mocked out SongImport class, os.path and a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.ewimport.os.path') as mocked_os_path:
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            mocked_os_path.isfile.return_value = True
            importer.import_source = u'Songs.DB'

            # WHEN: DB file size is less than 0x800
            mocked_os_path.getsize.return_value = 0x7FF

            # THEN: doImport should return None having called os.path.isfile
            self.assertIsNone(importer.doImport(), u'doImport should return None when db_size is less than 0x800')
            mocked_os_path.getsize.assert_any_call(u'Songs.DB')

    def do_import_memo_validty_test(self):
        """
        Test the :mod:`doImport` module handles invalid memo files correctly
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.ewimport.os.path') as mocked_os_path, \
            patch(u'__builtin__.open') as mocked_open, \
            patch(u'openlp.plugins.songs.lib.ewimport.struct') as mocked_struct:
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            mocked_os_path.isfile.return_value = True
            mocked_os_path.getsize.return_value = 0x800
            importer.import_source = u'Songs.DB'

            # WHEN: Unpacking first 35 bytes of Memo file
            struct_unpack_return_values = [(0, 0x700, 2, 0, 0), (0, 0x800, 0, 0, 0), (0, 0x800, 5, 0, 0)]
            mocked_struct.unpack.side_effect = struct_unpack_return_values

            # THEN: doImport should return None having called closed the open files db and memo files.
            for effect in struct_unpack_return_values:
                self.assertIsNone(importer.doImport(), u'doImport should return None when db_size is less than 0x800')
                self.assertEqual(mocked_open().close.call_count, 2,
                    u'The open db and memo files should have been closed')
                mocked_open().close.reset_mock()
                self.assertIs(mocked_open().seek.called, False, u'db_file.seek should not have been called.')

    def code_page_to_encoding_test(self):
        """
        Test the :mod:`doImport` converts the code page to the encoding correctly
        """
        # GIVEN: A mocked out SongImport class, a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.ewimport.os.path') as mocked_os_path, \
            patch(u'__builtin__.open'), patch(u'openlp.plugins.songs.lib.ewimport.struct') as mocked_struct, \
            patch(u'openlp.plugins.songs.lib.ewimport.retrieve_windows_encoding') as mocked_retrieve_windows_encoding:
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            mocked_os_path.isfile.return_value = True
            mocked_os_path.getsize.return_value = 0x800
            importer.import_source = u'Songs.DB'

            # WHEN: Unpacking the code page
            for code_page, encoding in CODE_PAGE_MAPPINGS:
                struct_unpack_return_values = [(0, 0x800, 2, 0, 0), (code_page, )]
                mocked_struct.unpack.side_effect = struct_unpack_return_values
                mocked_retrieve_windows_encoding.return_value = False

                # THEN: doImport should return None having called retrieve_windows_encoding with the correct encoding.
                self.assertIsNone(importer.doImport(), u'doImport should return None when db_size is less than 0x800')
                mocked_retrieve_windows_encoding.assert_call(encoding)

    def file_import_test(self):
        """
        Test the actual import of real song files and check that the imported data is correct.
        """

        # GIVEN: Test files with a mocked out SongImport class, a mocked out "manager", a mocked out "import_wizard",
        #       and mocked out "author", "add_copyright", "add_verse", "finish" methods.
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'), \
            patch(u'openlp.plugins.songs.lib.ewimport.retrieve_windows_encoding') as mocked_retrieve_windows_encoding:
            mocked_retrieve_windows_encoding.return_value = u'cp1252'
            mocked_manager = MagicMock()
            mocked_import_wizard = MagicMock()
            mocked_add_author = MagicMock()
            mocked_add_verse = MagicMock()
            mocked_finish = MagicMock()
            mocked_title = MagicMock()
            mocked_finish.return_value = True
            importer = EasyWorshipSongImportLogger(mocked_manager)
            importer.import_wizard = mocked_import_wizard
            importer.stop_import_flag = False
            importer.addAuthor = mocked_add_author
            importer.addVerse = mocked_add_verse
            importer.title = mocked_title
            importer.finish = mocked_finish
            importer.topics = []

            # WHEN: Importing each file
            importer.import_source = os.path.join(TEST_PATH, u'Songs.DB')

            # THEN: doImport should return none, the song data should be as expected, and finish should have been
            #       called.
            self.assertIsNone(importer.doImport(), u'doImport should return None when it has completed')
            for song_data in SONG_TEST_DATA:
                print mocked_title.mocked_calls()
                title = song_data[u'title']
                author_calls = song_data[u'authors']
                song_copyright = song_data[u'copyright']
                ccli_number = song_data[u'ccli_number']
                add_verse_calls = song_data[u'verses']
                verse_order_list = song_data[u'verse_order_list']
                self.assertIn(title, importer._title_assignment_list, u'title for %s should be "%s"' % (title, title))
                for author in author_calls:
                    mocked_add_author.assert_any_call(author)
                if song_copyright:
                    self.assertEqual(importer.copyright, song_copyright)
                if ccli_number:
                    self.assertEquals(importer.ccliNumber, ccli_number, u'ccliNumber for %s should be %s'
                                                                        % (title, ccli_number))
                for verse_text, verse_tag in add_verse_calls:
                    mocked_add_verse.assert_any_call(verse_text, verse_tag)
                if verse_order_list:
                    self.assertEquals(importer.verseOrderList, verse_order_list, u'verseOrderList for %s should be %s'
                                                                   % (title, verse_order_list))
                mocked_finish.assert_called_with()
