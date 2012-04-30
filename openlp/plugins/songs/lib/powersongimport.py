# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import re

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class PowerSongImport(SongImport):
    """
    The :class:`PowerSongImport` class provides the ability to import song files
    from PowerSong.

    **PowerSong Song File Format:**

    * Encoded as UTF-8.
    * The file has a number of fields, with the song metadata fields first,
      followed by the lyrics fields.

    Fields:
        Each field begins with one of four labels, each of which begin with one
        non-printing byte:

        * ``ENQ`` (0x05) ``TITLE``
        * ``ACK`` (0x06) ``AUTHOR``
        * ``CR`` (0x0d) ``COPYRIGHTLINE``
        * ``EOT`` (0x04) ``PART``

        The field label is separated from the field contents by one random byte.
        Each field ends at the next field label, or at the end of the file.

    Metadata fields:
        * Every PowerSong file begins with a TITLE field.
        * This is followed by zero or more AUTHOR fields.
        * The next field is always COPYRIGHTLINE, but it may be empty (in which
          case the byte following the label is the null byte 0x00).
          When the field contents are not empty, the first byte is 0xc2 and
          should be discarded.
          This field may contain a CCLI number at the end: e.g. "CCLI 176263"

    Lyrics fields:
        * The COPYRIGHTLINE field is followed by zero or more PART fields, each
          of which contains one verse.
        * Lines have Windows line endings ``CRLF`` (0x0d, 0x0a).
        * There is no concept of verse types.

    Valid extensions for a PowerSong song file are:
        * .song
    """

    def __init__(self, manager, **kwargs):
        """
        Initialise the PowerSong importer.
        """
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        """
        Receive a single file or a list of files to import.
        """
        if isinstance(self.importSource, list):
            self.importWizard.progressBar.setMaximum(len(self.importSource))
            for file in self.importSource:
                if self.stopImportFlag:
                    return
                self.setDefaults()
                with open(file, 'rb') as song_file:
                    # Check file is valid PowerSong song format
                    if song_file.read(6) != u'\x05TITLE':
                        self.logError(file, unicode(
                            translate('SongsPlugin.PowerSongSongImport',
                            ('Invalid PowerSong song file. Missing '
                                '"\x05TITLE" header.'))))
                        continue
                    song_data = unicode(song_file.read(), u'utf-8', u'replace')
                    # Extract title and author fields
                    first_part, sep, song_data = song_data.partition(
                        u'\x0DCOPYRIGHTLINE')
                    if not sep:
                        self.logError(file, unicode(
                            translate('SongsPlugin.PowerSongSongImport',
                                ('Invalid PowerSong song file. Missing '
                                 '"\x0DCOPYRIGHTLINE" string.'))))
                        continue
                    title_authors = first_part.split(u'\x06AUTHOR')
                    # Get the song title
                    self.title = self.stripControlChars(title_authors[0][1:])
                    # Extract the author(s)
                    for author in title_authors[1:]:
                        self.parseAuthor(self.stripControlChars(author[1:]))
                    # Get copyright and CCLI number
                    copyright, sep, song_data = song_data.partition(
                        u'\x04PART')
                    if not sep:
                        self.logError(file, unicode(
                            translate('SongsPlugin.PowerSongSongImport',
                                ('No verses found. Missing '
                                 '"\x04PART" string.'))))
                        continue
                    copyright, sep, ccli_no = copyright[1:].rpartition(u'CCLI ')
                    if not sep:
                        copyright = ccli_no
                        ccli_no = u''
                    if copyright:
                        if copyright[0] == u'\u00c2':
                            copyright = copyright[1:]
                        self.addCopyright(self.stripControlChars(
                            copyright.rstrip(u'\n')))
                    if ccli_no:
                        ccli_no = ccli_no.strip()
                        if ccli_no.isdigit():
                            self.ccliNumber = self.stripControlChars(ccli_no)
                    # Get the verse(s)
                    verses = song_data.split(u'\x04PART')
                    for verse in verses:
                        self.addVerse(self.stripControlChars(verse[1:]))
                if not self.finish():
                    self.logError(file)

    def stripControlChars(self, text):
        """
        Get rid of ASCII control characters.

        Illegals chars are ASCII code points 0-31 and 127, except:
            * ``HT`` (0x09) - Tab
            * ``LF`` (0x0a) - Line feed
            * ``CR`` (0x0d) - Carriage return
        """
        ILLEGAL_CHARS = u'([\x00-\x08\x0b-\x0c\x0e-\x1f\x7f])'
        return re.sub(ILLEGAL_CHARS, '', text)