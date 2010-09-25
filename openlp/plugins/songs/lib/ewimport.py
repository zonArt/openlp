# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund, Jeffrey Smith                            #
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

import sys
import os
import struct

from openlp.core.lib import translate
from songimport import SongImport

def strip_rtf(blob):
    depth = 0
    control = False
    clear_text = []
    control_word = []
    for c in blob:
        if control:
            # for delimiters, set control to False 
            if c == '{':
                if len(control_word) > 0:
                    depth += 1
                control = False
            elif c == '}':
                if len(control_word) > 0:
                    depth -= 1
                control = False
            elif c == '\\':
                new_control = (len(control_word) > 0)
                control = False
            elif c.isspace():
                control = False
            else:
                control_word.append(c)
                if len(control_word) == 3 and control_word[0] == '\'':
                    control = False
            if not control:
                if len(control_word) == 0:
                    if c == '{' or c == '}' or c == '\\':
                        clear_text.append(c)
                else:
                    control_str = ''.join(control_word)
                    if control_str == 'par' or control_str == 'line':
                        clear_text.append(u'\n')
                    elif control_str == 'tab':
                        clear_text.append(u'\n')
                    elif control_str[0] == '\'':
                        # Really should take RTF character set into account but
                        # for now assume ANSI (Windows-1252) and call it good
                        s = chr(int(control_str[1:3], 16))
                        clear_text.append(s.decode(u'windows-1252'))
                    del control_word[:]
            if c == '\\' and new_control:
                control = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        elif depth > 2:
            continue
        elif c == '\n' or c == '\r':
            continue
        elif c == '\\':
            control = True
        else:
            clear_text.append(c)
    return u''.join(clear_text)

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
        self.import_source = kwargs[u'filename']
        SongImport.__init__(self, manager)

    def do_import(self):
        # Open the DB and MB files if they exist
        import_source_mb = self.import_source.replace('.DB', '.MB')
        if not os.path.isfile(self.import_source):
            return False
        if not os.path.isfile(import_source_mb):
            return False
        db_size = os.path.getsize(self.import_source)
        if db_size < 0x800:
            return False
        db_file = open(self.import_source, 'rb')
        self.memo_file = open(import_source_mb, 'rb')
        # Don't accept files that are clearly not paradox files
        record_size, header_size, block_size, first_block, num_fields \
            = struct.unpack('<hhxb8xh17xh', db_file.read(35))
        if header_size != 0x800 or block_size < 1 or block_size > 4:
            db_file.close()
            self.memo_file.close()
            return False
        # There does not appear to be a _reliable_ way of getting the number
        # of songs/records, so let's use file blocks for measuring progress.
        total_blocks = (db_size - header_size) / (block_size * 1024)
        self.import_wizard.importProgressBar.setMaximum(total_blocks)
        # Read the field description information
        db_file.seek(120)
        field_info = db_file.read(num_fields * 2)
        db_file.seek(4 + (num_fields * 4) + 261, os.SEEK_CUR)
        field_names = db_file.read(header_size - db_file.tell()).split('\0',
            num_fields)
        field_names.pop()
        field_descs = []
        for i,field_name in enumerate(field_names):
            field_type, field_size = struct.unpack_from('BB', field_info, i * 2)
            field_descs.append(FieldDescEntry(field_name, field_type,
                field_size))
        self.set_record_struct(field_descs)
        # Pick out the field description indexes we will need
        success = True
        try:
            fi_title = self.find_field(u'Title')
            fi_author = self.find_field(u'Author')
            fi_copy = self.find_field(u'Copyright')
            fi_admin = self.find_field(u'Administrator')
            fi_words = self.find_field(u'Words')
            fi_ccli = self.find_field(u'Song Number')
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
                if self.stop_import_flag:
                    success = False
                    break
                raw_record = db_file.read(record_size)
                self.fields = self.record_struct.unpack(raw_record)
                self.set_defaults()
                # Get title and update progress bar message
                title = self.get_field(fi_title)
                if title:
                    self.import_wizard.incrementProgressBar(
                        unicode(translate('SongsPlugin.ImportWizardForm',
                            'Importing "%s"...')) % title, 0)
                    self.title = title
                # Get remaining fields
                copy = self.get_field(fi_copy)
                admin = self.get_field(fi_admin)
                ccli = self.get_field(fi_ccli)
                authors = self.get_field(fi_author)
                words = self.get_field(fi_words)
                # Set the SongImport object members
                if copy:
                    self.copyright = copy
                if admin:
                    if copy:
                        self.copyright += u', '
                    self.copyright += \
                        unicode(translate('SongsPlugin.ImportWizardForm',
                            'Administered by %s')) % admin
                if ccli:
                    self.ccli_number = ccli
                if authors:
                    # Split up the authors
                    author_list = authors.split(u'/')
                    if len(author_list) < 2:
                        author_list = authors.split(u';')
                    if len(author_list) < 2:
                        author_list = authors.split(u',')
                    for author_name in author_list:
                        self.add_author(author_name.strip())
                if words:
                    # Format the lyrics
                    words = strip_rtf(words)
                    for verse in words.split(u'\n\n'):
                        self.add_verse(verse.strip(), u'V')
                if self.stop_import_flag:
                    success = False
                    break
                self.finish()
            if not self.stop_import_flag:
                self.import_wizard.incrementProgressBar(u'')
        db_file.close()
        self.memo_file.close()
        return success

    def find_field(self, field_name):
        return [i for i,x in enumerate(self.field_descs) \
            if x.name == field_name][0]

    def set_record_struct(self, field_descs):
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
        self.record_struct = struct.Struct(''.join(fsl))
        self.field_descs = field_descs

    def get_field(self, field_desc_index):
        field = self.fields[field_desc_index]
        field_desc = self.field_descs[field_desc_index]
        # Return None in case of 'blank' entries
        if isinstance(field, str):
            if len(field.rstrip('\0')) == 0:
                return None
        elif field == 0:
            return None
        # Format the field depending on the field type
        if field_desc.type == 1:
            # string
            return field.rstrip('\0').decode(u'windows-1252')
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
            block_start, blob_size = \
                struct.unpack_from('<II', field, len(field)-10)
            sub_block = block_start & 0xff;
            block_start &= ~0xff
            self.memo_file.seek(block_start)
            memo_block_type, = struct.unpack('b', self.memo_file.read(1))
            if memo_block_type == 2:
                self.memo_file.seek(8, os.SEEK_CUR)
            elif memo_block_type == 3:
                if sub_block > 63:
                    return u'';
                self.memo_file.seek(11 + (5 * sub_block), os.SEEK_CUR)
                sub_block_start, = struct.unpack('B', self.memo_file.read(1))
                self.memo_file.seek(block_start + (sub_block_start * 16))
            else:
                return u'';
            return self.memo_file.read(blob_size)
        else:
            return 0