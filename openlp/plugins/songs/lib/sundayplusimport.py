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

import logging
import os
import re

from openlp.plugins.songs.lib import VerseType, retrieve_windows_encoding
from openlp.plugins.songs.lib import StripRtf
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class SundayPlusImport(SongImport):
    """
    Import Sunday Plus songs

    The format examples can be found attached to bug report at
    <http://support.openlp.org/issues/395>
    """
    HOTKEY_TO_VERSE_TYPE = {
        u'1': u'v1',
        u'2': u'v2',
        u'3': u'v3',
        u'4': u'v4',
        u'5': u'v5',
        u'6': u'v6',
        u'7': u'v7',
        u'8': u'v8',
        u'9': u'v9',
        u'C': u'c',
        u'+': u'b',
        u'Z': u'o'}

    def __init__(self, manager, **kwargs):
        """
        Initialise the class.
        """
        SongImport.__init__(self, manager, **kwargs)
        self.rtf = StripRtf()

    def doImport(self):
        self.importWizard.progressBar.setMaximum(len(self.importSource))
        self.encoding = 'us-ascii'
        for filename in self.importSource:
            if self.stopImportFlag:
                return
            song_file = open(filename)
            self.doImportFile(song_file)
            song_file.close()

    def doImportFile(self, file):
        """
        Process the Sunday Plus file object.
        """
        self.setDefaults()
        if not self.parse(file.read()):
            self.logError(file.name)
            return
        if self.title == '':
            self.title = self.titleFromFilename(file.name)
        if not self.finish():
            self.logError(file.name)

    def parse(self, data, cell = False):
        if len(data) == 0 or data[0:1] != '[' or data[-1] != ']':
            self.logError(u'File is malformed')
            return False
        i = 1
        verse_type = VerseType.Tags[VerseType.Verse]
        while i < len(data):
            # Data is held as #name: value pairs inside groups marked as [].
            # Now we are looking for name.
            if data[i:i+1] == '#':
                name_end = data.find(':', i+1)
                name = data[i+1:name_end]
                i = name_end + 1
                while data[i:i+1] == ' ':
                    i += 1
                if data[i:i+1] == '"':
                    end = data.find('"', i+1)
                    value = data[i+1:end]
                elif data[i:i+1] == '[':
                    j = i
                    inside_quotes = False
                    while j < len(data):
                        char = data[j:j+1]
                        if char == '"':
                            inside_quotes = not inside_quotes
                        elif not inside_quotes and char == ']':
                            end = j + 1
                            break
                        j += 1
                    value = data[i:end]
                else:
                    end = data.find(',', i+1)
                    if data.find('(', i, end) != -1:
                        end = data.find(')', i) + 1
                    value = data[i:end]
                # If we are in the main group.
                if cell == False:
                    if name == 'title':
                        self.title = self.decode(self.unescape(value))
                    elif name == 'Author':
                        author = self.decode(self.unescape(value))
                        if len(author):
                            self.addAuthor(author)
                    elif name == 'Copyright':
                        self.copyright = self.decode(self.unescape(value))
                    elif name[0:4] == 'CELL':
                        self.parse(value, cell = name[4:])
                # We are in a verse group.
                else:
                    if name == 'MARKER_NAME':
                        value = value.strip()
                        if len(value):
                            verse_type = VerseType.Tags[
                                VerseType.from_loose_input(value[0])]
                            if len(value) >= 2 and value[-1] in ['0', '1', '2',
                                '3', '4', '5', '6', '7', '8', '9']:
                                verse_type = "%s%s" % (verse_type, value[-1])
                    elif name == 'Hotkey':
                        # Hotkey always appears after MARKER_NAME, so it
                        # effectively overrides MARKER_NAME, if present.
                        if len(value) and \
                            value in self.HOTKEY_TO_VERSE_TYPE.keys():
                            verse_type = self.HOTKEY_TO_VERSE_TYPE[value]
                    if name == 'rtf':
                        value = self.unescape(value)
                        verse = self.rtf.strip_rtf(value, self.encoding)
                        lines = verse.strip().split('\n')
                        # If any line inside any verse contains CCLI or
                        # only Public Domain, we treat this as special data:
                        # we remove that line and add data to specific field.
                        for i in xrange(len(lines)):
                            lines[i] = lines[i].strip()
                            line = lines[i]
                            if line[:4].lower() == u'ccli':
                                m = re.search(r'[0-9]+', line)
                                if m:
                                    self.ccliNumber = int(m.group(0))
                                    lines.pop(i)
                            elif line.lower() == u'public domain':
                                self.copyright = u'Public Domain'
                                lines.pop(i)
                        self.addVerse('\n'.join(lines).strip(), verse_type)
                if end == -1:
                    break
                i = end + 1
            i += 1
        return True

    def titleFromFilename(self, filename):
        title = os.path.split(filename)[1]
        if title.endswith(u'.ptf'):
            title = title[:-4]
        # For some strange reason all example files names ended with 1-7.
        if title.endswith('1-7'):
            title = title[:-3]
        return title.replace(u'_', u' ')

    def decode(self, blob):
        while True:
            try:
                return unicode(blob, self.encoding)
            except:
                # This is asked again every time the previously chosen
                # encoding does not work.
                self.encoding = retrieve_windows_encoding()

    def unescape(self, text):
        text = text.replace('^^', '"')
        text = text.replace('^', '\'')
        return text.strip()

