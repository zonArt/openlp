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
import chardet
import csv
import logging
import re

from openlp.core.common import translate
from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.songimport.songimport import SongImport

log = logging.getLogger(__name__)

EMPTY_STR = 'NULL'


class WorshipAssistantImport(SongImport):
    """
    The :class:`WorshipAssistantImport` class provides the ability to import songs
    from Worship Assistant, via a dump of the database to a CSV file.

    The following fields are in the exported CSV file:

    * ``SONGNR`` Song ID (Discarded by importer)
    * ``TITLE`` Song title
    * ``AUTHOR`` Song author.
    * ``COPYRIGHT`` Copyright information
    * ``FIRSTLINE`` Unknown (Discarded by importer)
    * ``PRIKEY`` Primary chord key (Discarded by importer)
    * ``ALTKEY`` Alternate chord key (Discarded by importer)
    * ``TEMPO`` Tempo (Discarded by importer)
    * ``FOCUS`` Unknown (Discarded by importer)
    * ``THEME`` Theme (Discarded by importer)
    * ``SCRIPTURE`` Associated scripture (Discarded by importer)
    * ``ACTIVE`` Boolean value (Discarded by importer)
    * ``SONGBOOK`` Boolean value (Discarded by importer)
    * ``TIMESIG`` Unknown (Discarded by importer)
    * ``INTRODUCED`` Date the song was created (Discarded by importer)
    * ``LASTUSED`` Date the song was last used (Discarded by importer)
    * ``TIMESUSED`` How many times the song was used (Discarded by importer)
    * ``CCLINR`` CCLI Number
    * ``USER1`` User Field 1 (Discarded by importer)
    * ``USER2`` User Field 2 (Discarded by importer)
    * ``USER3`` User Field 3 (Discarded by importer)
    * ``USER4`` User Field 4 (Discarded by importer)
    * ``USER5`` User Field 5 (Discarded by importer)
    * ``ROADMAP`` Verse order used for the presentation
    * ``FILELINK1`` Associated file 1 (Discarded by importer)
    * ``OVERMAP`` Verse order used for printing (Discarded by importer)
    * ``FILELINK2`` Associated file 2 (Discarded by importer)
    * ``LYRICS`` The song lyrics used for printing (Discarded by importer, LYRICS2 is used instead)
    * ``INFO`` Unknown (Discarded by importer)
    * ``LYRICS2`` The song lyrics used for the presentation
    * ``BACKGROUND`` Custom background (Discarded by importer)
    """
    def do_import(self):
        """
        Receive a CSV file to import.
        """
        # Get encoding
        detect_file = open(self.import_source, 'rb')
        detect_content = detect_file.read()
        details = chardet.detect(detect_content)
        detect_file.close()
        songs_file = open(self.import_source, 'r', encoding=details['encoding'])
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
            # Ensure that all keys are uppercase
            record = dict((field.upper(), value) for field, value in record.items())
            # The CSV file has a line in the middle of the file where the headers are repeated.
            #  We need to skip this line.
            if record['TITLE'] == "TITLE" and record['AUTHOR'] == 'AUTHOR' and record['LYRICS2'] == 'LYRICS2':
                continue
            self.set_defaults()
            verse_order_list = []
            try:
                self.title = record['TITLE']
                if record['AUTHOR'] != EMPTY_STR:
                    self.parse_author(record['AUTHOR'])
                    print(record['AUTHOR'])
                if record['COPYRIGHT'] != EMPTY_STR:
                    self.add_copyright(record['COPYRIGHT'])
                if record['CCLINR'] != EMPTY_STR:
                    self.ccli_number = record['CCLINR']
                if record['ROADMAP'] != EMPTY_STR:
                    verse_order_list = record['ROADMAP'].split(',')
                lyrics = record['LYRICS2']
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
                if line.startswith('['):  # verse marker
                    # drop the square brackets
                    right_bracket = line.find(']')
                    content = line[1:right_bracket].lower()
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
                    # Update verse order when the verse name has changed
                    if content != verse_tag + verse_num:
                        for i in range(len(verse_order_list)):
                            if verse_order_list[i].lower() == content.lower():
                                verse_order_list[i] = verse_tag + verse_num
                elif line and not line.isspace():
                    verse += line + '\n'
                elif verse:
                    self.add_verse(verse, verse_tag+verse_num)
                    verse = ''
            if verse:
                self.add_verse(verse, verse_tag+verse_num)
            if verse_order_list:
                self.verse_order_list = verse_order_list
            if not self.finish():
                self.log_error(translate('SongsPlugin.WorshipAssistantImport', 'Record %d') % index
                               + (': "' + self.title + '"' if self.title else ''))
            songs_file.close()
