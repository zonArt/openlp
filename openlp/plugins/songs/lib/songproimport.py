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
The :mod:`songproimport` module provides the functionality for importing SongPro
songs into the OpenLP database.
"""
import re

from openlp.plugins.songs.lib import strip_rtf
from openlp.plugins.songs.lib.songimport import SongImport

class SongProImport(SongImport):
    """
    The :class:`SongProImport` class provides the ability to import song files
    from SongPro export files.

    **SongPro Song File Format:**

    SongPro has the option to export under its File menu
    This produces files containing single or multiple songs
    The file is text with lines tagged with # followed by an identifier.
    This is documented here: http://creationsoftware.com/ImportIdentifiers.php
    An example here: http://creationsoftware.com/ExampleImportingManySongs.txt

    #A - next line is the Song Author
    #B - the lines following until next tagged line are the "Bridge" words
        (can be in rtf or plain text) which we map as B1
    #C - the lines following until next tagged line are the chorus words
        (can be in rtf or plain text)
        which we map as C1
    #D - the lines following until next tagged line are the "Ending" words
        (can be in rtf or plain text) which we map as E1
    #E - this song ends here, so we process the song -
        and start again at the next line
    #G - next line is the Group
    #M - next line is the Song Number
    #N - next line are Notes
    #R - next line is the SongCopyright
    #O - next line is the Verse Sequence
    #T - next line is the Song Title
    #1 - #7 the lines following until next tagged line are the verse x words
        (can be in rtf or plain text)
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the SongPro importer.
        """
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        """
        Receive a single file or a list of files to import.
        """
        self.encoding = None
        with open(self.import_source, 'r') as songs_file:
            self.import_wizard.progress_bar.setMaximum(0)
            tag = ''
            text = ''
            for file_line in songs_file:
                if self.stop_import_flag:
                    break
                file_line = str(file_line, 'cp1252')
                file_text = file_line.rstrip()
                if file_text and file_text[0] == '#':
                    self.processSection(tag, text.rstrip())
                    tag = file_text[1:]
                    text = ''
                else:
                    text += file_line

    def processSection(self, tag, text):
        """
        Process a section of the song, i.e. title, verse etc.
        """
        if tag == 'T':
            self.setDefaults()
            if text:
                self.title = text
            return
        elif tag == 'E':
            self.finish()
            return
        if 'rtf1' in text:
            result = strip_rtf(text, self.encoding)
            if result is None:
                return
            text, self.encoding = result
            text = text.rstrip()
        if not text:
            return
        if tag == 'A':
            self.parse_author(text)
        elif tag in ['B', 'C']:
            self.addVerse(text, tag)
        elif tag == 'D':
            self.addVerse(text, 'E')
        elif tag == 'G':
            self.topics.append(text)
        elif tag == 'M':
            matches = re.findall(r'\d+', text)
            if matches:
                self.songNumber = matches[-1]
                self.songBookName = text[:text.rfind(self.songNumber)]
        elif tag == 'N':
            self.comments = text
        elif tag == 'O':
            for char in text:
                if char == 'C':
                    self.verseOrderList.append('C1')
                elif char == 'B':
                    self.verseOrderList.append('B1')
                elif char == 'D':
                    self.verseOrderList.append('E1')
                elif '1' <= char <= '7':
                    self.verseOrderList.append('V' + char)
        elif tag == 'R':
            self.addCopyright(text)
        elif '1' <= tag <= '7':
            self.addVerse(text, 'V' + tag[1:])
