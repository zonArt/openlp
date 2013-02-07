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
from songimport import SongImport

RTF_STRIPPING_REGEX = re.compile(r'\{\\tx[^}]*\}')
# regex: at least two newlines, can have spaces between them
SLIDE_BREAK_REGEX = re.compile(r'\n *?\n[\n ]*')
NUMBER_REGEX = re.compile(r'[0-9]+')
NOTE_REGEX = re.compile(r'\(.*?\)')


class FieldDescEntry:
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size


class EasyWorshipSongImport(SongImport):
    """
    The :class:`EasyWorshipSongImport` class provides OpenLP with the
    ability to import EasyWorship song files.
    """
    def __init__(self, manager, **kwargs):
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        # Open the DB and MB files if they exist
        import_source_mb = self.importSource.replace('.DB', '.MB')
        if not os.path.isfile(self.importSource):
            return
        if not os.path.isfile(import_source_mb):
            return
        db_size = os.path.getsize(self.importSource)
        if db_size < 0x800:
            return
        db_file = open(self.importSource, 'rb')
        self.memoFile = open(import_source_mb, 'rb')
        # Don't accept files that are clearly not paradox files
        record_size, header_size, block_size, first_block, num_fields = struct.unpack('<hhxb8xh17xh', db_file.read(35))
        if header_size != 0x800 or block_size < 1 or block_size > 4:
            db_file.close()
            self.memoFile.close()
            return
        # Take a stab at how text is encoded
        self.encoding = u'cp1252'
        db_file.seek(106)
        code_page, = struct.unpack('<h', db_file.read(2))
        if code_page == 852:
            self.encoding = u'cp1250'
        # The following codepage to actual encoding mappings have not been
        # observed, but merely guessed. Actual example files are needed.
        elif code_page == 737:
            self.encoding = u'cp1253'
        elif code_page == 775:
            self.encoding = u'cp1257'
        elif code_page == 855:
            self.encoding = u'cp1251'
        elif code_page == 857:
            self.encoding = u'cp1254'
        elif code_page == 866:
            self.encoding = u'cp1251'
        elif code_page == 869:
            self.encoding = u'cp1253'
        elif code_page == 862:
            self.encoding = u'cp1255'
        elif code_page == 874:
            self.encoding = u'cp874'
        self.encoding = retrieve_windows_encoding(self.encoding)
        if not self.encoding:
            return
        # There does not appear to be a _reliable_ way of getting the number
        # of songs/records, so let's use file blocks for measuring progress.
        total_blocks = (db_size - header_size) / (block_size * 1024)
        self.importWizard.progressBar.setMaximum(total_blocks)
        # Read the field description information
        db_file.seek(120)
        field_info = db_file.read(num_fields * 2)
        db_file.seek(4 + (num_fields * 4) + 261, os.SEEK_CUR)
        field_names = db_file.read(header_size - db_file.tell()).split('\0', num_fields)
        field_names.pop()
        field_descs = []
        for i, field_name in enumerate(field_names):
            field_type, field_size = struct.unpack_from('BB', field_info, i * 2)
            field_descs.append(FieldDescEntry(field_name, field_type, field_size))
        self.setRecordStruct(field_descs)
        # Pick out the field description indexes we will need
        try:
            success = True
            fi_title = self.findField(u'Title')
            fi_author = self.findField(u'Author')
            fi_copy = self.findField(u'Copyright')
            fi_admin = self.findField(u'Administrator')
            fi_words = self.findField(u'Words')
            fi_ccli = self.findField(u'Song Number')
        except IndexError:
            # This is the wrong table
            success = False
        # Loop through each block of the file
        cur_block = first_block
        while cur_block != 0 and success:
            db_file.seek(header_size + ((cur_block - 1) * 1024 * block_size))
            cur_block, rec_count = struct.unpack('<h2xh', db_file.read(6))
            rec_count = (rec_count + record_size) / record_size
            # Loop through each record within the current block
            for i in range(rec_count):
                if self.stopImportFlag:
                    break
                raw_record = db_file.read(record_size)
                self.fields = self.recordStruct.unpack(raw_record)
                self.setDefaults()
                self.title = self.getField(fi_title)
                # Get remaining fields.
                copy = self.getField(fi_copy)
                admin = self.getField(fi_admin)
                ccli = self.getField(fi_ccli)
                authors = self.getField(fi_author)
                words = self.getField(fi_words)
                # Set the SongImport object members.
                if copy:
                    self.copyright = copy
                if admin:
                    if copy:
                        self.copyright += u', '
                    self.copyright += translate('SongsPlugin.EasyWorshipSongImport', 'Administered by %s') % admin
                if ccli:
                    self.ccliNumber = ccli
                if authors:
                    # Split up the authors
                    author_list = authors.split(u'/')
                    if len(author_list) < 2:
                        author_list = authors.split(u';')
                    if len(author_list) < 2:
                        author_list = authors.split(u',')
                    for author_name in author_list:
                        self.addAuthor(author_name.strip())
                if words:
                    # Format the lyrics
                    result = strip_rtf(words, self.encoding)
                    if result is None:
                        return
                    words, self.encoding = result
                    verse_type = VerseType.Tags[VerseType.Verse]
                    for verse in SLIDE_BREAK_REGEX.split(words):
                        verse = verse.strip()
                        if not verse:
                            continue
                        verse_split = verse.split(u'\n', 1)
                        first_line_is_tag = False
                        # EW tags: verse, chorus, pre-chorus, bridge, tag,
                        # intro, ending, slide
                        for type in VerseType.Names+[u'tag', u'slide']:
                            type = type.lower()
                            ew_tag = verse_split[0].strip().lower()
                            if ew_tag.startswith(type):
                                verse_type = type[0]
                                if type == u'tag' or type == u'slide':
                                    verse_type = VerseType.Tags[VerseType.Other]
                                first_line_is_tag = True
                                number_found = False
                                # check if tag is followed by number and/or note
                                if len(ew_tag) > len(type):
                                    match = NUMBER_REGEX.search(ew_tag)
                                    if match:
                                        number = match.group()
                                        verse_type += number
                                        number_found = True
                                    match = NOTE_REGEX.search(ew_tag)
                                    if match:
                                        self.comments += ew_tag + u'\n'
                                if not number_found:
                                    verse_type += u'1'
                                break
                        self.addVerse(
                            verse_split[-1].strip() \
                                if first_line_is_tag else verse,
                            verse_type)
                if len(self.comments) > 5:
                    self.comments += unicode(translate('SongsPlugin.EasyWorshipSongImport',
                        '\n[above are Song Tags with notes imported from EasyWorship]'))
                if self.stopImportFlag:
                    break
                if not self.finish():
                    self.logError(self.importSource)
        db_file.close()
        self.memoFile.close()

    def findField(self, field_name):
        return [i for i, x in enumerate(self.fieldDescs)
            if x.name == field_name][0]

    def setRecordStruct(self, field_descs):
        # Begin with empty field struct list
        fsl = ['>']
        for field_desc in field_descs:
            if field_desc.type == 1:
                # string
                fsl.append('%ds' % field_desc.size)
            elif field_desc.type == 3:
                # 16-bit int
                fsl.append('H')
            elif field_desc.type == 4:
                # 32-bit int
                fsl.append('I')
            elif field_desc.type == 9:
                # Logical
                fsl.append('B')
            elif field_desc.type == 0x0c:
                # Memo
                fsl.append('%ds' % field_desc.size)
            elif field_desc.type == 0x0d:
                # Blob
                fsl.append('%ds' % field_desc.size)
            elif field_desc.type == 0x15:
                # Timestamp
                fsl.append('Q')
            else:
                fsl.append('%ds' % field_desc.size)
        self.recordStruct = struct.Struct(''.join(fsl))
        self.fieldDescs = field_descs

    def getField(self, field_desc_index):
        field = self.fields[field_desc_index]
        field_desc = self.fieldDescs[field_desc_index]
        # Return None in case of 'blank' entries
        if isinstance(field, str):
            if not field.rstrip('\0'):
                return None
        elif field == 0:
            return None
        # Format the field depending on the field type
        if field_desc.type == 1:
            # string
            return field.rstrip('\0').decode(self.encoding)
        elif field_desc.type == 3:
            # 16-bit int
            return field ^ 0x8000
        elif field_desc.type == 4:
            # 32-bit int
            return field ^ 0x80000000
        elif field_desc.type == 9:
            # Logical
            return (field ^ 0x80 == 1)
        elif field_desc.type == 0x0c or field_desc.type == 0x0d:
            # Memo or Blob
            block_start, blob_size = struct.unpack_from('<II', field, len(field)-10)
            sub_block = block_start & 0xff
            block_start &= ~0xff
            self.memoFile.seek(block_start)
            memo_block_type, = struct.unpack('b', self.memoFile.read(1))
            if memo_block_type == 2:
                self.memoFile.seek(8, os.SEEK_CUR)
            elif memo_block_type == 3:
                if sub_block > 63:
                    return u''
                self.memoFile.seek(11 + (5 * sub_block), os.SEEK_CUR)
                sub_block_start, = struct.unpack('B', self.memoFile.read(1))
                self.memoFile.seek(block_start + (sub_block_start * 16))
            else:
                return u''
            return self.memoFile.read(blob_size)
        else:
            return 0
