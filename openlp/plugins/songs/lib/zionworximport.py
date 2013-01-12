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
The :mod:`zionworximport` module provides the functionality for importing
ZionWorx songs into the OpenLP database.
"""
import csv
import logging

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

# Used to strip control chars (except 10=LF, 13=CR)
CONTROL_CHARS_MAP = dict.fromkeys(range(10) + [11, 12] + range(14,32) + [127])

class ZionWorxImport(SongImport):
    """
    The :class:`ZionWorxImport` class provides the ability to import songs
    from ZionWorx, via a dump of the ZionWorx database to a CSV file.

    ZionWorx song database fields:

    * ``SongNum`` Song ID. (Discarded by importer)
    * ``Title1`` Main Title.
    * ``Title2`` Alternate Title.
    * ``Lyrics`` Song verses, separated by blank lines.
    * ``Writer`` Song author(s).
    * ``Copyright`` Copyright information
    * ``Keywords`` (Discarded by importer)
    * ``DefaultStyle`` (Discarded by importer)

    ZionWorx has no native export function; it uses the proprietary TurboDB
    database engine. The TurboDB vendor, dataWeb, provides tools which can
    export TurboDB tables to other formats, such as freeware console tool
    TurboDB Data Exchange which is available for Windows and Linux. This command
    exports the ZionWorx songs table to a CSV file:

    ``tdbdatax MainTable.dat songstable.csv -fsdf -s, -qd``

    * -f  Table format: ``sdf`` denotes text file.
    * -s  Separator character between fields.
    * -q  Quote character surrounding fields. ``d`` denotes double-quote.

    CSV format expected by importer:

    * Field separator character is comma ``,``
    * Fields surrounded by double-quotes ``"``. This enables fields (such as
      Lyrics) to include new-lines and commas. Double-quotes within a field
      are denoted by two double-quotes ``""``
    * Note: This is the default format of the Python ``csv`` module.

    """
    def doImport(self):
        """
        Receive a CSV file (from a ZionWorx database dump) to import.
        """
        with open(self.importSource, 'rb') as songs_file:
            field_names = [u'SongNum', u'Title1', u'Title2', u'Lyrics', u'Writer', u'Copyright', u'Keywords',
                u'DefaultStyle']
            songs_reader = csv.DictReader(songs_file, field_names)
            try:
                records = list(songs_reader)
            except csv.Error, e:
                self.logError(translate('SongsPlugin.ZionWorxImport', 'Error reading CSV file.'),
                    translate('SongsPlugin.ZionWorxImport', 'Line %d: %s') % (songs_reader.line_num, e))
                return
            num_records = len(records)
            log.info(u'%s records found in CSV file' % num_records)
            self.importWizard.progressBar.setMaximum(num_records)
            for index, record in enumerate(records, 1):
                if self.stopImportFlag:
                    return
                self.setDefaults()
                try:
                    self.title = self._decode(record[u'Title1'])
                    if record[u'Title2']:
                        self.alternateTitle = self._decode(record[u'Title2'])
                    self.parseAuthor(self._decode(record[u'Writer']))
                    self.addCopyright(self._decode(record[u'Copyright']))
                    lyrics = self._decode(record[u'Lyrics'])
                except UnicodeDecodeError, e:
                    self.logError(translate('SongsPlugin.ZionWorxImport', 'Record %d' % index),
                        translate('SongsPlugin.ZionWorxImport', 'Decoding error: %s') % e)
                    continue
                except TypeError, e:
                    self.logError(translate(
                        'SongsPlugin.ZionWorxImport', 'File not valid ZionWorx CSV format.'), u'TypeError: %s' % e)
                    return
                verse = u''
                for line in lyrics.splitlines():
                    if line and not line.isspace():
                        verse += line + u'\n'
                    elif verse:
                        self.addVerse(verse)
                        verse = u''
                if verse:
                    self.addVerse(verse)
                title = self.title
                if not self.finish():
                    self.logError(translate('SongsPlugin.ZionWorxImport', 'Record %d') % index
                        + (u': "' + title + u'"' if title else u''))

    def _decode(self, str):
        """
        Decodes CSV input to unicode, stripping all control characters (except
        new lines).
        """
        # This encoding choice seems OK. ZionWorx has no option for setting the
        # encoding for its songs, so we assume encoding is always the same.
        return unicode(str, u'cp1252').translate(CONTROL_CHARS_MAP)
