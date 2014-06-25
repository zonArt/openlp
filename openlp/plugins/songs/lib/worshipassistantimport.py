# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
The :mod:`worshipassistantimport` module provides the functionality for importing
Worship Assistant songs into the OpenLP database.
"""
import csv
import logging
import re

from openlp.core.common import translate
from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

# Used to strip control chars (except 10=LF, 13=CR)
CONTROL_CHARS_MAP = dict.fromkeys(list(range(10)) + [11, 12] + list(range(14, 32)) + [127])


class WorshipAssistantImport(SongImport):
    """
    The :class:`WorshipAssistantImport` class provides the ability to import songs
    from Worship Assistant, via a dump of the database to a CSV file.

    The following fields are in the exported CSV file:

    * ``SONGNR`` Song ID (Discarded by importer)
    * ``TITLE`` Song title
    * ``AUTHOR`` Song author. May containt multiple authors.
    * ``COPYRIGHT`` Copyright information
    * ``FIRSTLINE`` Unknown (Discarded by importer)
    * ``PRIKEY`` Primary chord key
    * ``ALTKEY`` Alternate chord key
    * ``TEMPO`` Tempo
    * ``FOCUS`` Unknown (Discarded by importer)
    * ``THEME`` Theme (Discarded by importer)
    * ``SCRIPTURE`` Associated scripture (Discarded by importer)
    * ``ACTIVE`` Boolean value (Discarded by importer)
    * ``SONGBOOK`` Boolean value (Discarded by importer)
    * ``TIMESIG`` Unknown (Discarded by importer)
    * ``INTRODUCED`` Date the song was created (Discarded by importer)
    * ``LASTUSED`` Date the song was last used (Discarded by importer)
    * ``TIMESUSED`` How many times the song was used (Discarded by importer)
    * ``TIMESUSED`` How many times the song was used (Discarded by importer)
    * ``CCLINR`` CCLI Number
    * ``USER1`` User Field 1 (Discarded by importer)
    * ``USER2`` User Field 2 (Discarded by importer)
    * ``USER3`` User Field 3 (Discarded by importer)
    * ``USER4`` User Field 4 (Discarded by importer)
    * ``USER5`` User Field 5 (Discarded by importer)
    * ``ROADMAP`` Verse order
    * ``FILELINK1`` Associated file 1 (Discarded by importer)
    * ``OVERMAP`` Unknown (Discarded by importer)
    * ``FILELINK2`` Associated file 2 (Discarded by importer)
    * ``LYRICS`` The song lyrics as plain text (Discarded by importer)
    * ``INFO`` Unknown (Discarded by importer)
    * ``LYRICS2`` The song lyrics with verse numbers
    * ``BACKGROUND`` Unknown (Discarded by importer)
    """
    def do_import(self):
        """
        Receive a CSV file to import.
        """
        with open(self.import_source, 'r', encoding='latin-1') as songs_file:
            songs_reader = csv.DictReader(songs_file)
            try:
                records = list(songs_reader)
            except csv.Error as e:
                self.log_error(translate('SongsPlugin.WorshipAssistantImport', 'Error reading CSV file.'),
                               translate('SongsPlugin.WorshipAssistantImport', 'Line %d: %s') %
                               (songs_reader.line_num, e))
                return
            num_records = len(records)
            log.info('%s records found in CSV file' % num_records)
            self.import_wizard.progress_bar.setMaximum(num_records)
            for index, record in enumerate(records, 1):
                if self.stop_import_flag:
                    return
                # The CSV file has a line in the middle of the file where the headers are repeated.
                #  We need to skip this line.
                if record['TITLE'] == "TITLE" and record['AUTHOR'] == 'AUTHOR' and record['LYRICS2'] == 'LYRICS2':
                    continue
                self.set_defaults()
                try:
                    self.title = self._decode(record['TITLE'])
                    self.parse_author(self._decode(record['AUTHOR']))
                    self.add_copyright(self._decode(record['COPYRIGHT']))
                    lyrics = self._decode(record['LYRICS2'])
                except UnicodeDecodeError as e:
                    self.log_error(translate('SongsPlugin.WorshipAssistantImport', 'Record %d' % index),
                                   translate('SongsPlugin.WorshipAssistantImport', 'Decoding error: %s') % e)
                    continue
                except TypeError as e:
                    self.log_error(translate('SongsPlugin.WorshipAssistantImport',
                                             'File not valid WorshipAssistant CSV format.'), 'TypeError: %s' % e)
                    return
                verse = ''
                for line in lyrics.splitlines():
                    if line.startswith('['): # verse marker
                        # drop the square brackets
                        right_bracket = line.find(']')
                        content = line[1:right_bracket].lower()
                        # have we got any digits? If so, verse number is everything from the digits to the end (openlp does not
                        # have concept of part verses, so just ignore any non integers on the end (including floats))
                        match = re.match('(\D*)(\d+)', content)
                        if match is not None:
                            verse_tag = match.group(1)
                            verse_num = match.group(2)
                        else:
                            # otherwise we assume number 1 and take the whole prefix as the verse tag
                            verse_tag = content
                            verse_num = '1'
                        verse_index = VerseType.from_loose_input(verse_tag) if verse_tag else 0
                        verse_tag = VerseType.tags[verse_index]
                    elif line and not line.isspace():
                        verse += line + '\n'
                    elif verse:
                        self.add_verse(verse, verse_tag+verse_num)
                        verse = ''
                if verse:
                    self.add_verse(verse, verse_tag+verse_num)
                if not self.finish():
                    self.log_error(translate('SongsPlugin.ZionWorxImport', 'Record %d') % index
                                   + (': "' + self.title + '"' if self.title else ''))

    def _decode(self, str):
        """
        Decodes CSV input to unicode, stripping all control characters (except new lines).
        """
        # This encoding choice seems OK. ZionWorx has no option for setting the
        # encoding for its songs, so we assume encoding is always the same.
        return str
        #return str(str, 'cp1252').translate(CONTROL_CHARS_MAP)
