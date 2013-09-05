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

import logging
import re

from lxml import objectify
from lxml.etree import Error, LxmlError

from openlp.core.lib import translate
from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.songimport import SongImport
from openlp.plugins.songs.lib.ui import SongStrings

log = logging.getLogger(__name__)

class OpenSongImport(SongImport):
    """
    Import songs exported from OpenSong

    The format is described loosly on the `OpenSong File Format Specification
    <http://www.opensong.org/d/manual/song_file_format_specification>`_ page on the OpenSong web site. However, it
    doesn't describe the <lyrics> section, so here's an attempt:

    If the first charachter of a line is a space, then the rest of that line is lyrics. If it is not a space the
    following applies.

    Verses can be expressed in one of 2 ways, either in complete verses, or by line grouping, i.e. grouping all line 1's
    of a verse together, all line 2's of a verse together, and so on.

    An example of complete verses::

        <lyrics>
        [v1]
         List of words
         Another Line

        [v2]
         Some words for the 2nd verse
         etc...
        </lyrics>

    The 'v' in the verse specifiers above can be left out, it is implied.

    An example of line grouping::

        <lyrics>
        [V]
        1List of words
        2Some words for the 2nd Verse

        1Another Line
        2etc...
        </lyrics>

    Either or both forms can be used in one song. The number does not necessarily appear at the start of the line.
    Additionally, the [v1] labels can have either upper or lower case Vs.

    Other labels can be used also:

    C
        Chorus

    B
        Bridge

    All verses are imported and tagged appropriately.

    Guitar chords can be provided "above" the lyrics (the line is preceeded by a period "."), and one or more "_" can
    be used to signify long-drawn-out words. Chords and "_" are removed by this importer. For example::

        . A7        Bm
        1 Some____ Words

    The <presentation> tag is used to populate the OpenLP verse display order field. The Author and Copyright tags are
    also imported to the appropriate places.
    """

    def __init__(self, manager, **kwargs):
        """
        Initialise the class.
        """
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        self.import_wizard.progress_bar.setMaximum(len(self.import_source))
        for filename in self.import_source:
            if self.stop_import_flag:
                return
            song_file = open(filename)
            self.doImportFile(song_file)
            song_file.close()

    def doImportFile(self, file):
        """
        Process the OpenSong file - pass in a file-like object, not a file path.
        """
        self.setDefaults()
        try:
            tree = objectify.parse(file)
        except (Error, LxmlError):
            self.logError(file.name, SongStrings.XMLSyntaxError)
            log.exception('Error parsing XML')
            return
        root = tree.getroot()
        if root.tag != 'song':
            self.logError(file.name, str(
                translate('SongsPlugin.OpenSongImport', ('Invalid OpenSong song file. Missing song tag.'))))
            return
        fields = dir(root)
        decode = {
            'copyright': self.addCopyright,
            'ccli': 'ccli_number',
            'author': self.parse_author,
            'title': 'title',
            'aka': 'alternate_title',
            'hymn_number': 'song_number'
        }
        for attr, fn_or_string in list(decode.items()):
            if attr in fields:
                ustring = str(root.__getattr__(attr))
                if isinstance(fn_or_string, str):
                    setattr(self, fn_or_string, ustring)
                else:
                    fn_or_string(ustring)
        if 'theme' in fields and str(root.theme) not in self.topics:
            self.topics.append(str(root.theme))
        if 'alttheme' in fields and str(root.alttheme) not in self.topics:
            self.topics.append(str(root.alttheme))
        # data storage while importing
        verses = {}
        # keep track of verses appearance order
        our_verse_order = []
        # default verse
        verse_tag = VerseType.tags[VerseType.Verse]
        verse_num = '1'
        # for the case where song has several sections with same marker
        inst = 1
        if 'lyrics' in fields:
            lyrics = str(root.lyrics)
        else:
            lyrics = ''
        for this_line in lyrics.split('\n'):
            if not this_line:
                continue
            # skip this line if it is a comment
            if this_line.startswith(';'):
                continue
            # skip guitar chords and page and column breaks
            if this_line.startswith('.') or this_line.startswith('---') or this_line.startswith('-!!'):
                continue
            # verse/chorus/etc. marker
            if this_line.startswith('['):
                # drop the square brackets
                right_bracket = this_line.find(']')
                content = this_line[1:right_bracket].lower()
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
                inst = 1
                if [verse_tag, verse_num, inst] in our_verse_order and verse_num in verses.get(verse_tag, {}):
                    inst = len(verses[verse_tag][verse_num]) + 1
                continue
            # number at start of line.. it's verse number
            if this_line[0].isdigit():
                verse_num = this_line[0]
                this_line = this_line[1:].strip()
            verses.setdefault(verse_tag, {})
            verses[verse_tag].setdefault(verse_num, {})
            if inst not in verses[verse_tag][verse_num]:
                verses[verse_tag][verse_num][inst] = []
                our_verse_order.append([verse_tag, verse_num, inst])
            # Tidy text and remove the ____s from extended words
            this_line = self.tidyText(this_line)
            this_line = this_line.replace('_', '')
            this_line = this_line.replace('|', '\n')
            this_line = this_line.strip()
            verses[verse_tag][verse_num][inst].append(this_line)
        # done parsing
        # add verses in original order
        verse_joints = {}
        for (verse_tag, verse_num, inst) in our_verse_order:
            lines = '\n'.join(verses[verse_tag][verse_num][inst])
            length = 0
            while(length < len(verse_num) and verse_num[length].isnumeric()):
                length += 1
            verse_def = '%s%s' % (verse_tag, verse_num[:length])
            verse_joints[verse_def] = '%s\n[---]\n%s' % (verse_joints[verse_def], lines) \
                if verse_def in verse_joints else lines
        for verse_def, lines in verse_joints.items():
            self.addVerse(lines, verse_def)
        if not self.verses:
            self.addVerse('')
        # figure out the presentation order, if present
        if 'presentation' in fields and root.presentation:
            order = str(root.presentation)
            # We make all the tags in the lyrics lower case, so match that here and then split into a list on the
            # whitespace.
            order = order.lower().split()
            for verse_def in order:
                match = re.match('(\D*)(\d+.*)', verse_def)
                if match is not None:
                    verse_tag = match.group(1)
                    verse_num = match.group(2)
                    if not verse_tag:
                        verse_tag = VerseType.tags[VerseType.Verse]
                else:
                    # Assume it's no.1 if there are no digits
                    verse_tag = verse_def
                    verse_num = '1'
                verse_def = '%s%s' % (verse_tag, verse_num)
                if verse_num in verses.get(verse_tag, {}):
                    self.verseOrderList.append(verse_def)
                else:
                    log.info('Got order %s but not in verse tags, dropping'
                        'this item from presentation order', verse_def)
        if not self.finish():
            self.logError(file.name)
