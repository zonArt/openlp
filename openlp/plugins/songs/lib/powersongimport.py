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
The :mod:`powersongimport` module provides the functionality for importing
PowerSong songs into the OpenLP database.
"""
import logging
import fnmatch
import os

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class PowerSongImport(SongImport):
    """
    The :class:`PowerSongImport` class provides the ability to import song files
    from PowerSong.

    **PowerSong 1.0 Song File Format:**

    The file has a number of label-field (think key-value) pairs.

    Label and Field strings:

        * Every label and field is a variable length string preceded by an
          integer specifying it's byte length.
        * Integer is 32-bit but is encoded in 7-bit format to save space. Thus
          if length will fit in 7 bits (ie <= 127) it takes up only one byte.

    Metadata fields:

        * Every PowerSong file has a TITLE field.
        * There is zero or more AUTHOR fields.
        * There is always a COPYRIGHTLINE label, but its field may be empty.
          This field may also contain a CCLI number: e.g. "CCLI 176263".

    Lyrics fields:

        * Each verse is contained in a PART field.
        * Lines have Windows line endings ``CRLF`` (0x0d, 0x0a).
        * There is no concept of verse types.

    Valid extensions for a PowerSong song file are:

        * .song
    """
    @staticmethod
    def isValidSource(import_source):
        """
        Checks if source is a PowerSong 1.0 folder:
            * is a directory
            * contains at least one *.song file
        """
        if os.path.isdir(import_source):
            for file in os.listdir(import_source):
                if fnmatch.fnmatch(file, u'*.song'):
                    return True
        return False

    def doImport(self):
        """
        Receive either a list of files or a folder (unicode) to import.
        """
        from importer import SongFormat
        PS_string = SongFormat.get(SongFormat.PowerSong, u'name')
        if isinstance(self.importSource, unicode):
            if os.path.isdir(self.importSource):
                dir = self.importSource
                self.importSource = []
                for file in os.listdir(dir):
                    if fnmatch.fnmatch(file, u'*.song'):
                        self.importSource.append(os.path.join(dir, file))
            else:
                self.importSource = u''
        if not self.importSource or not isinstance(self.importSource, list):
            self.logError(translate('SongsPlugin.PowerSongImport', 'No songs to import.'),
                translate('SongsPlugin.PowerSongImport', 'No %s files found.') % PS_string)
            return
        self.importWizard.progressBar.setMaximum(len(self.importSource))
        for file in self.importSource:
            if self.stopImportFlag:
                return
            self.setDefaults()
            parse_error = False
            with open(file, 'rb') as song_data:
                while True:
                    try:
                        label = self._readString(song_data)
                        if not label:
                            break
                        field = self._readString(song_data)
                    except ValueError:
                        parse_error = True
                        self.logError(os.path.basename(file), unicode(
                            translate('SongsPlugin.PowerSongImport', 'Invalid %s file. Unexpected byte value.')) %
                                PS_string)
                        break
                    else:
                        if label == u'TITLE':
                            self.title = field.replace(u'\n', u' ')
                        elif label == u'AUTHOR':
                            self.parseAuthor(field)
                        elif label == u'COPYRIGHTLINE':
                            found_copyright = True
                            self._parseCopyrightCCLI(field)
                        elif label == u'PART':
                            self.addVerse(field)
            if parse_error:
                continue
            # Check that file had TITLE field
            if not self.title:
                self.logError(os.path.basename(file), unicode(
                    translate('SongsPlugin.PowerSongImport', 'Invalid %s file. Missing "TITLE" header.')) % PS_string)
                continue
            # Check that file had COPYRIGHTLINE label
            if not found_copyright:
                self.logError(self.title, unicode(
                    translate('SongsPlugin.PowerSongImport', 'Invalid %s file. Missing "COPYRIGHTLINE" header.')) %
                        PS_string)
                continue
            # Check that file had at least one verse
            if not self.verses:
                self.logError(self.title, unicode(
                    translate('SongsPlugin.PowerSongImport', 'Verses not found. Missing "PART" header.')))
                continue
            if not self.finish():
                self.logError(self.title)

    def _readString(self, file_object):
        """
        Reads in next variable-length string.
        """
        string_len = self._read7BitEncodedInteger(file_object)
        return unicode(file_object.read(string_len), u'utf-8', u'ignore')

    def _read7BitEncodedInteger(self, file_object):
        """
        Reads in a 32-bit integer in compressed 7-bit format.

        Accomplished by reading the integer 7 bits at a time. The high bit
        of the byte when set means to continue reading more bytes.
        If the integer will fit in 7 bits (ie <= 127), it only takes up one
        byte. Otherwise, it may take up to 5 bytes.

        Reference: .NET method System.IO.BinaryReader.Read7BitEncodedInt
        """
        val = 0
        shift = 0
        i = 0
        while True:
            # Check for corrupted stream (since max 5 bytes per 32-bit integer)
            if i == 5:
                raise ValueError
            byte = self._readByte(file_object)
            # Strip high bit and shift left
            val += (byte & 0x7f) << shift
            shift += 7
            high_bit_set = byte & 0x80
            if not high_bit_set:
                break
            i += 1
        return val

    def _readByte(self, file_object):
        """
        Reads in next byte as an unsigned integer

        Note: returns 0 at end of file.
        """
        byte_str = file_object.read(1)
        # If read result is empty, then reached end of file
        if not byte_str:
            return 0
        else:
            return ord(byte_str)

    def _parseCopyrightCCLI(self, field):
        """
        Look for CCLI song number, and get copyright
        """
        copyright, sep, ccli_no = field.rpartition(u'CCLI')
        if not sep:
            copyright = ccli_no
            ccli_no = u''
        if copyright:
            self.addCopyright(copyright.rstrip(u'\n').replace(u'\n', u' '))
        if ccli_no:
            ccli_no = ccli_no.strip(u' :')
            if ccli_no.isdigit():
                self.ccliNumber = ccli_no
