# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
The :mod:`wowimport` module provides the functionality for importing Words of 
Worship songs into the OpenLP database.
"""
import os
import logging

from openlp.plugins.songs.lib.songimport import SongImport

BLOCK_TYPES = (u'V',  u'C',  u'B')

log = logging.getLogger(__name__)

class WowImport(SongImport):
    """
    The :class:`WowImport` class provides the ability to import song files from 
    Words of Worship.

    Words Of Worship Song File Format
    `````````````````````````````````
    
    The Words Of Worship song file format is as follows:

    * The song title is the file name minus the extension.
    * The song has a header, a number of blocks, followed by footer containing 
    the author and the copyright.
    * A block can be a verse, chorus or bridge.
    
    File Header:
        Bytes are counted from one, i.e. the first byte is byte 1. These bytes,
        up to the 56 byte, can change but no real meaning has been found. The
        56th byte specifies how many blocks there are. The first block starts
        with byte 83 after the "CSongDoc::CBlock" declaration.

    Blocks:
        Each block has a starting header, some lines of text, and an ending
        footer. Each block starts with 4 bytes, the first byte specifies how
        many lines are in that block, the next three bytes are null bytes.

        Each block ends with 4 bytes, the first of which defines what type of
        block it is, and the rest which are null bytes:

        * ``NUL`` (\x00) - Verse
        * ``SOH`` (\x01) - Chorus
        * ``STX`` (\x02) - Bridge

        Blocks are seperated by two bytes. The first byte is ``SOH`` (\x01),
        and the second byte is ``€`` (\x80).

    Lines:
        Each line starts with a byte which specifies how long that line is,
        the line text, and ends with a null byte.

  
    Footer:
        The footer follows on after the last block, the first byte specifies 
        the length of the author text, followed by the author text, if 
        this byte is null, then there is no author text. The byte after the 
        author text specifies the length of the copyright text, followed 
        by the copyright text. 
        
        The file is ended with four null bytes.
    
    Valid extensions for a Words of Worship song file are:
    
    * .wsg
    * .wow-song
    """

    def __init__(self, master_manager, **kwargs):
        """
        Initialise the import.

        ``master_manager``
            The song manager for the running OpenLP installation.
        """
        SongImport.__init__(self, master_manager)
        self.master_manager = master_manager
        if kwargs.has_key(u'filename'):
            self.import_source = kwargs[u'filename']
        if kwargs.has_key(u'filenames'):
            self.import_source = kwargs[u'filenames']
        log.debug(self.import_source)

    def do_import(self):
        """
        Recieve a single file, or a list of files to import.
        """
        
        if isinstance(self.import_source,  list):
            self.import_wizard.importProgressBar.setMaximum(
                len(self.import_source))
            for file in self.import_source:
                # TODO: check that it is a valid words of worship file (could 
                # check header for WoW File Song Word)
                self.author = u''
                self.copyright = u''
                # Get the song title
                self.file_name = os.path.split(file)[1]
                self.import_wizard.incrementProgressBar(
                    "Importing %s" % (self.file_name),  0)
                self.title = self.file_name.rpartition(u'.')[0]
                self.songData = open(file, 'rb')
                # Seek to byte which stores number of blocks in the song
                self.songData.seek(56) 
                self.no_of_blocks = ord(self.songData.read(1))
                # Seek to the beging of the first block
                self.songData.seek(82) 
                for block in range(self.no_of_blocks):
                    self.lines_to_read = ord(self.songData.read(1))
                    # Skip 3 nulls to the beginnig of the 1st line
                    self.songData.seek(3, os.SEEK_CUR) 
                    self.block_text = u''
                    while self.lines_to_read:
                        self.length_of_line = ord(self.songData.read(1))
                        self.line_text = unicode(
                            self.songData.read(self.length_of_line), u'cp1252')
                        self.songData.seek(1, os.SEEK_CUR)
                        if self.block_text != u'':
                            self.block_text += u'\n'
                        self.block_text += self.line_text
                        self.lines_to_read -= 1
                    self.block_type = BLOCK_TYPES[ord(self.songData.read(1))]
                    # Skip 3 nulls at the end of the block
                    self.songData.seek(3, os.SEEK_CUR)
                    # Blocks are seperated by 2 bytes, skip them, but not if 
                    # this is the last block!
                    if (block + 1) < self.no_of_blocks:
                        self.songData.seek(2, os.SEEK_CUR)
                    self.add_verse(self.block_text, self.block_type)
                # Now to extact the author
                self.author_length = ord(self.songData.read(1))
                if self.author_length != 0:
                    self.author = unicode(
                        self.songData.read(self.author_length), u'cp1252')
                # Finally the copyright
                self.copyright_length = ord(self.songData.read(1))
                if self.copyright_length != 0:
                    self.copyright = unicode(
                        self.songData.read(self.copyright_length), u'cp1252')
                self.parse_author(self.author)
                self.add_copyright(self.copyright)
                self.songData.close()
                self.finish()
                self.import_wizard.incrementProgressBar(
                    "Importing %s" % (self.file_name))
            return True
            
