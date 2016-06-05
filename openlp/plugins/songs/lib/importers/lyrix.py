# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
The :mod:`lyrix` module provides the functionality for importing songs which are
exproted from Lyrix."""

import logging
import re

from openlp.core.common import translate
from openlp.plugins.songs.lib.importers.songimport import SongImport

log = logging.getLogger(__name__)


class LyrixImport(SongImport):
    """
    Import songs exported from Lyrix
    """

    def __init__(self, manager, **kwargs):
        """
        Initialise the class.
        """
        super(LyrixImport, self).__init__(manager, **kwargs)

    def do_import(self):
        """
        Receive a single file or a list of files to import.
        """
        if not isinstance(self.import_source, list):
            return
        self.import_wizard.progress_bar.setMaximum(len(self.import_source))
        for filename in self.import_source:
            if self.stop_import_flag:
                return
            song_file = open(filename, 'rt', encoding='cp1251')
            self.do_import_file(song_file)
            song_file.close()

    def do_import_file(self, file):
        """
        Process the Lyrix file - pass in a file-like object, not a file path.
        """
        self.set_defaults()
        # Setup variables
        line_number = 0
        song_title = 'Standard Song Title'
        ccli = '0'
        current_verse = ''
        verses = []
        author = ''
        copyright = ''
        try:
            # Read the file
            for line in file:
                line = line.strip()
                line_number += 1
                if line_number == 4:
                    song_title = line
                if line_number < 7:
                    continue
                # Detect and get CCLI number
                if line.lower().startswith('ccli'):
                    ccli = re.findall('\d+', line)[0]
                    try:
                        # If the CCLI was found, we are near the end
                        # Find author
                        line = next(file).strip()
                        author = line[line.find(':') + 2:]
                        # Find copyright
                        copyright = next(file).strip()
                    except StopIteration:
                        pass
                    break
                if line == '':
                    if current_verse != '':
                        verses.append(current_verse)
                    current_verse = ''
                else:
                    if current_verse == '':
                        current_verse += line
                    else:
                        current_verse += '\n' + line
        except Exception as e:
            self.log_error(translate('SongsPlugin.LyrixImport', 'File {name}').format(name=file.name),
                           translate('SongsPlugin.LyrixImport', 'Error: {error}').format(error=e))
            return
        self.title = song_title
        self.parse_author(author)
        self.ccli_number = ccli
        self.add_copyright(copyright)
        for verse in verses:
            self.add_verse(verse, 'v')
        if not self.finish():
            self.log_error(file.name)
