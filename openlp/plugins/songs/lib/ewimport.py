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
The :mod:`ewimport` module provides the functionality for importing
EasyWorship song databases into the current installation database.
"""

import os
import struct
import re

from openlp.core.lib import translate
from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib import retrieve_windows_encoding, strip_rtf
from .songimport import SongImport

RTF_STRIPPING_REGEX = re.compile(r'\{\\tx[^}]*\}')
# regex: at least two newlines, can have spaces between them
SLIDE_BREAK_REGEX = re.compile(r'\n *?\n[\n ]*')
NUMBER_REGEX = re.compile(r'[0-9]+')
NOTE_REGEX = re.compile(r'\(.*?\)')


class FieldDescEntry:
    def __init__(self, name, field_type, size):
        self.name = name
        self.field_type = field_type
        self.size = size


class FieldType(object):
    """
    An enumeration class for different field types that can be expected in an EasyWorship song file.
    """
    String = 1
    Int16 = 3
    Int32 = 4
    Logical = 9
    Memo = 0x0c
    Blob = 0x0d
    Timestamp = 0x15


class EasyWorshipSongImport(SongImport):
    """
    The :class:`EasyWorshipSongImport` class provides OpenLP with the
    ability to import EasyWorship song files.
    """
    def __init__(self, manager, **kwargs):
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        # Open the DB and MB files if they exist
        import_source_mb = self.import_source.replace('.DB', '.MB')
        if not os.path.isfile(self.import_source) or not os.path.isfile(import_source_mb):
            return
        db_size = os.path.getsize(self.import_source)
        if db_size < 0x800:
            return
        db_file = open(self.import_source, 'rb')
        self.memoFile = open(import_source_mb, 'rb')
        # Don't accept files that are clearly not paradox files
        record_size, header_size, block_size, first_block, num_fields = struct.unpack('<hhxb8xh17xh', db_file.read(35))
        if header_size != 0x800 or block_size < 1 or block_size > 4:
            db_file.close()
            self.memoFile.close()
            return
        # Take a stab at how text is encoded
        self.encoding = 'cp1252'
        db_file.seek(106)
        code_page, = struct.unpack('<h', db_file.read(2))
        if code_page == 852:
            self.encoding = 'cp1250'
        # The following codepage to actual encoding mappings have not been
        # observed, but merely guessed. Actual example files are needed.
        elif code_page == 737:
            self.encoding = 'cp1253'
        elif code_page == 775:
            self.encoding = 'cp1257'
        elif code_page == 855:
            self.encoding = 'cp1251'
        elif code_page == 857:
            self.encoding = 'cp1254'
        elif code_page == 866:
            self.encoding = 'cp1251'
        elif code_page == 869:
            self.encoding = 'cp1253'
        elif code_page == 862:
            self.encoding = 'cp1255'
        elif code_page == 874:
            self.encoding = 'cp874'
        self.encoding = retrieve_windows_encoding(self.encoding)
        if not self.encoding:
            return
        # Read the field description information
        db_file.seek(120)
        field_info = db_file.read(num_fields * 2)
        db_file.seek(4 + (num_fields * 4) + 261, os.SEEK_CUR)
        field_names = db_file.read(header_size - db_file.tell()).split(b'\0', num_fields)
        field_names.pop()
        field_descs = []
        for i, field_name in enumerate(field_names):
            field_type, field_size = struct.unpack_from('BB', field_info, i * 2)
            field_descs.append(FieldDescEntry(field_name, field_type, field_size))
        self.setRecordStruct(field_descs)
        # Pick out the field description indexes we will need
        try:
            success = True
            fi_title = self.findField(b'Title')
            fi_author = self.findField(b'Author')
            fi_copy = self.findField(b'Copyright')
            fi_admin = self.findField(b'Administrator')
            fi_words = self.findField(b'Words')
            fi_ccli = self.findField(b'Song Number')
        except IndexError:
            # This is the wrong table
            success = False
        # There does not appear to be a _reliable_ way of getting the number of songs/records, so loop through the file
        # blocks and total the number of records. Store the information in a list so we dont have to do all this again.
        cur_block = first_block
        total_count = 0
        block_list = []
        while cur_block != 0 and success:
            cur_block_pos = header_size + ((cur_block - 1) * 1024 * block_size)
            db_file.seek(cur_block_pos)
            cur_block, rec_count = struct.unpack('<h2xh', db_file.read(6))
            rec_count = (rec_count + record_size) // record_size
            block_list.append((cur_block_pos, rec_count))
            total_count += rec_count
        self.import_wizard.progress_bar.setMaximum(total_count)
        for block in block_list:
            cur_block_pos, rec_count = block
            db_file.seek(cur_block_pos + 6)
            # Loop through each record within the current block
            for i in range(rec_count):
                if self.stop_import_flag:
                    break
                raw_record = db_file.read(record_size)
                self.fields = self.recordStruct.unpack(raw_record)
                self.setDefaults()
                self.title = self.getField(fi_title).decode()
                # Get remaining fields.
                copy = self.getField(fi_copy)
                admin = self.getField(fi_admin)
                ccli = self.getField(fi_ccli)
                authors = self.getField(fi_author)
                words = self.getField(fi_words)
                # Set the SongImport object members.
                if copy:
                    self.copyright = copy.decode()
                if admin:
                    if copy:
                        self.copyright += ', '
                    self.copyright += translate('SongsPlugin.EasyWorshipSongImport',
                                                'Administered by %s') % admin.decode()
                if ccli:
                    self.ccliNumber = ccli.decode()
                if authors:
                    # Split up the authors
                    author_list = authors.split(b'/')
                    if len(author_list) < 2:
                        author_list = authors.split(b';')
                    if len(author_list) < 2:
                        author_list = authors.split(b',')
                    for author_name in author_list:
                        self.addAuthor(author_name.decode().strip())
                if words:
                    # Format the lyrics
                    result = strip_rtf(words.decode(), self.encoding)
                    if result is None:
                        return
                    words, self.encoding = result
                    verse_type = VerseType.tags[VerseType.Verse]
                    for verse in SLIDE_BREAK_REGEX.split(words):
                        verse = verse.strip()
                        if not verse:
                            continue
                        verse_split = verse.split('\n', 1)
                        first_line_is_tag = False
                        # EW tags: verse, chorus, pre-chorus, bridge, tag,
                        # intro, ending, slide
                        for tag in VerseType.tags + ['tag', 'slide']:
                            tag = tag.lower()
                            ew_tag = verse_split[0].strip().lower()
                            if ew_tag.startswith(tag):
                                verse_type = tag[0]
                                if tag == 'tag' or tag == 'slide':
                                    verse_type = VerseType.tags[VerseType.Other]
                                first_line_is_tag = True
                                number_found = False
                                # check if tag is followed by number and/or note
                                if len(ew_tag) > len(tag):
                                    match = NUMBER_REGEX.search(ew_tag)
                                    if match:
                                        number = match.group()
                                        verse_type += number
                                        number_found = True
                                    match = NOTE_REGEX.search(ew_tag)
                                    if match:
                                        self.comments += ew_tag + '\n'
                                if not number_found:
                                    verse_type += '1'
                                break
                        self.addVerse(verse_split[-1].strip() if first_line_is_tag else verse, verse_type)
                if len(self.comments) > 5:
                    self.comments += str(translate('SongsPlugin.EasyWorshipSongImport',
                        '\n[above are Song Tags with notes imported from EasyWorship]'))
                if self.stop_import_flag:
                    break
                if not self.finish():
                    self.logError(self.import_source)
        db_file.close()
        self.memoFile.close()

    def findField(self, field_name):
        return [i for i, x in enumerate(self.fieldDescs) if x.name == field_name][0]

    def setRecordStruct(self, field_descs):
        # Begin with empty field struct list
        fsl = ['>']
        for field_desc in field_descs:
            if field_desc.field_type == FieldType.String:
                fsl.append('%ds' % field_desc.size)
            elif field_desc.field_type == FieldType.Int16:
                fsl.append('H')
            elif field_desc.field_type == FieldType.Int32:
                fsl.append('I')
            elif field_desc.field_type == FieldType.Logical:
                fsl.append('B')
            elif field_desc.field_type == FieldType.Memo:
                fsl.append('%ds' % field_desc.size)
            elif field_desc.field_type == FieldType.Blob:
                fsl.append('%ds' % field_desc.size)
            elif field_desc.field_type == FieldType.Timestamp:
                fsl.append('Q')
            else:
                fsl.append('%ds' % field_desc.size)
        self.recordStruct = struct.Struct(''.join(fsl))
        self.fieldDescs = field_descs

    def getField(self, field_desc_index):
        field = self.fields[field_desc_index]
        field_desc = self.fieldDescs[field_desc_index]
        # Return None in case of 'blank' entries
        if isinstance(field, bytes):
            if not field.rstrip(b'\0'):
                return None
        elif field == 0:
            return None
        # Format the field depending on the field type
        if field_desc.field_type == FieldType.String:
            return field.rstrip(b'\0')
        elif field_desc.field_type == FieldType.Int16:
            return field ^ 0x8000
        elif field_desc.field_type == FieldType.Int32:
            return field ^ 0x80000000
        elif field_desc.field_type == FieldType.Logical:
            return (field ^ 0x80 == 1)
        elif field_desc.field_type == FieldType.Memo or field_desc.field_type == FieldType.Blob:
            block_start, blob_size = struct.unpack_from('<II', field, len(field)-10)
            sub_block = block_start & 0xff
            block_start &= ~0xff
            self.memoFile.seek(block_start)
            memo_block_type, = struct.unpack('b', self.memoFile.read(1))
            if memo_block_type == 2:
                self.memoFile.seek(8, os.SEEK_CUR)
            elif memo_block_type == 3:
                if sub_block > 63:
                    return b''
                self.memoFile.seek(11 + (5 * sub_block), os.SEEK_CUR)
                sub_block_start, = struct.unpack('B', self.memoFile.read(1))
                self.memoFile.seek(block_start + (sub_block_start * 16))
            else:
                return b''
            return self.memoFile.read(blob_size)
        else:
            return 0
