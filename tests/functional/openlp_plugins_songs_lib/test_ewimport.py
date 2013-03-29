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

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'../../../resources'))

class TestFieldDesc:
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size

TEST_DATA_ENCODING = u'cp1252'
TEST_FIELD_DESCS = [TestFieldDesc(u'Title', 1, 50),
                    TestFieldDesc(u'Text Percentage Bottom', 3, 2),
                    TestFieldDesc(u'RecID', 4, 4),
                    TestFieldDesc(u'Default Background', 9, 1),
                    TestFieldDesc(u'Words', 12, 250),
                    TestFieldDesc(u'BK Bitmap', 13, 10),
                    TestFieldDesc(u'Last Modified', 21, 10)]
TEST_FIELDS = ['A Heart Like Thine\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0', 32868, 2147483750,
    129, '{\\rtf1\\ansi\\deff0\\deftab254{\\fonttbl{\\f0\\fnil\\fcharset0 Arial;}{\\f1\\fnil\\fcharset0 Verdana;}}'
    '{\\colortbl\\red0\\green0\\blue0;\\red255\\green0\\blue0;\\red0\\green128\\blue0;\\red0\\green0\\blue255;'
    '\\red255\\green255\\blue0;\\red255\\green0\\blue255;\\red128\\g��\7\0f\r\0\0\1\0', '\0\0\0\0\0\0\0\0\0\0', 0]
#22

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
        type = 1
        size = 50

        # WHEN: A FieldDescEntry object is created.
        field_desc_entry = FieldDescEntry(name, type, size)

        # THEN:
        self.assertIsNotNone(field_desc_entry, u'Import should not be none')
        self.assertEquals(field_desc_entry.name, name, u'FieldDescEntry.name should be the same as the name argument')
        self.assertEquals(field_desc_entry.type, type, u'FieldDescEntry.type should be the same as the type argument')
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

    def find_field_test(self):
        """
        Test finding a field in a given list using the :mod:`findField`
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
            mocked_struct.Struct.assert_called_with('>50sHIB250s10sQ')

    def get_field_test(self):


        # GIVEN: A mocked out SongImport class, a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'):
            mocked_manager = MagicMock()
            importer = EasyWorshipSongImport(mocked_manager)
            importer.encoding = TEST_DATA_ENCODING

            # WHEN: Supplied with string with just NULL bytes, or an int with the value 0
            importer.fields = TEST_FIELDS
            importer.fieldDescs = TEST_FIELD_DESCS
            field_results = [(0, 'A Heart Like Thine'), (1, 100), (2, 102L), (3, True), (5, None), (6, None)]

            # THEN: getField should return None
            for field_index, result in field_results:
                self.assertEquals(importer.getField(field_index), result,
                    u'getField should return "%s" when called with "%s"' % (result, TEST_FIELDS[field_index]))

        # GIVEN: A mocked out SongImport class, a mocked out "manager"
        with patch(u'openlp.plugins.songs.lib.ewimport.SongImport'), \
             patch(u'openlp.plugins.songs.lib.ewimport.SongImport'):
            mocked_manager = MagicMock()
            mocked
            importer = EasyWorshipSongImport(mocked_manager)
            importer.encoding = TEST_DATA_ENCODING

            # WHEN: Supplied with string with just NULL bytes, or an int with the value 0
            importer.fields = TEST_FIELDS
            importer.fieldDescs = TEST_FIELD_DESCS
            field_results = [(4, u'I dunno')]

            # THEN: getField should return None
            for field_index, result in field_results:
                self.assertEquals(importer.getField(field_index), result)

             #                     u'getField should return "%s" when called with "%s"' % (result, TEST_FIELDS[field_index]))


# TODO: Write doImport Tests

# TODO: Write getField Tests