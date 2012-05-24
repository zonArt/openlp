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
The :mod:`zionworximport` module provides the functionality for importing
ZionWorx songs into the OpenLP database.
"""
import csv
import logging

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class ZionWorxImport(SongImport):
    """
    The :class:`ZionWorxImport` class provides the ability to import songs
    from ZionWorx, via a dump of the ZionWorx database to a CSV file.

    ZionWorx song database fields:

        * ``SongNum`` Song ID. Discarded by importer.
        * ``Title1`` Main Title.
        * ``Title2`` Alternate Title.
        * ``Lyrics`` Song verses, separated by blank lines.
        * ``Writer`` Song author(s).
        * ``Copyright`` Copyright information
        * ``Keywords`` Discarded by importer.
        * ``DefaultStyle`` Discarded by importer.

    ZionWorx has no native export function; it uses the proprietary TurboDB
    database engine. The TurboDB vendor, dataWeb, provides tools which can
    export TurboDB tables to other formats, such as freeware console tool
    TurboDB Data Exchange which is available for Windows and Linux. This command
    exports the ZionWorx songs table to a CSV file:

    ``tdbdatax MainTable.dat songstable.csv -fsdf -s, -qd``

        * ``-f`` Table format: ``sdf`` denotes text file.
        * ``-s`` Separator character between fields.
        * ``-q`` Quote character surrounding fields. ``d`` denotes double-quote.

    CSV format expected by importer:

        * Fields separated by comma ``,``
        * Fields surrounded by double-quotes ``"``. This enables fields (such as
          Lyrics) to include new-lines and commas. Double-quotes within a field
          are denoted by two double-quotes ``""``
        * Note: This is the default format of the Python ``csv`` module.

    """

    def doImport(self):
        """
        Receive a CSV file (from a ZionWorx database dump) to import.
        """
        if not os.path.isfile(self.importSource):
            self.logError(unicode(translate('SongsPlugin.ZionWorxImport',
                'No songs to import.')),
                unicode(translate('SongsPlugin.ZionWorxImport',
                    'No %s CSV file found.' % WizardStrings.ZW)))
            return
        with open(self.importSource, 'rb') as songs_file:
            songs_reader = csv.reader(songs_file)
            try:
                num_records = sum(1 for _ in songs_reader)
            except csv.Error, e:
                self.logError(unicode(translate('SongsPlugin.ZionWorxImport',
                    'Error reading CSV file.')),
                    unicode(translate('SongsPlugin.ZionWorxImport',
                    'Line %d: %s' % songs_reader.line_num, e)))
            log.debug(u'%s records found in CSV file' % num_records)
            self.importWizard.progressBar.setMaximum(num_records)
            fieldnames = [u'SongNum', u'Title1', u'Title2', u'Lyrics',
                u'Writer', u'Copyright', u'Keywords', u'DefaultStyle']
            songs_reader_dict= csv.DictReader(songs_file, fieldnames)
            try:
                for record in songs_reader_dict:
                    if self.stopImportFlag:
                        return
                    self.setDefaults()
                    self.title = unicode(record[u'Title1'])
                    if record[u'Title2']:
                        self.alternateTitle = unicode(record[u'Title2'])
                    self.parseAuthor(unicode(record[u'Writer']))
                    self.addCopyright(unicode(record[u'Copyright']))
                    self.processSongText(unicode(record[u'Lyrics']))
                    if not self.finish():
                        self.logError(self.title)
            except csv.Error, e:
                self.logError(unicode(translate('SongsPlugin.ZionWorxImport',
                    'Error reading CSV file.')),
                    unicode(translate('SongsPlugin.ZionWorxImport',
                    'Line %d: %s' % songs_reader_dict.line_num, e)))
