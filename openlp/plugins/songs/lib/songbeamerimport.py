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
The :mod:`songbeamerimport` module provides the functionality for importing
 SongBeamer songs into the OpenLP database.
"""
import chardet
import codecs
import logging
import os
import re

from openlp.plugins.songs.lib import VerseType
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class SongBeamerTypes(object):
    MarkTypes = {
        u'Refrain': VerseType.Tags[VerseType.Chorus],
        u'Chorus': VerseType.Tags[VerseType.Chorus],
        u'Vers': VerseType.Tags[VerseType.Verse],
        u'Verse': VerseType.Tags[VerseType.Verse],
        u'Strophe': VerseType.Tags[VerseType.Verse],
        u'Intro': VerseType.Tags[VerseType.Intro],
        u'Coda': VerseType.Tags[VerseType.Ending],
        u'Ending': VerseType.Tags[VerseType.Ending],
        u'Bridge': VerseType.Tags[VerseType.Bridge],
        u'Interlude': VerseType.Tags[VerseType.Bridge],
        u'Zwischenspiel': VerseType.Tags[VerseType.Bridge],
        u'Pre-Chorus': VerseType.Tags[VerseType.PreChorus],
        u'Pre-Refrain': VerseType.Tags[VerseType.PreChorus],
        u'Pre-Bridge': VerseType.Tags[VerseType.Other],
        u'Pre-Coda': VerseType.Tags[VerseType.Other],
        u'Unbekannt': VerseType.Tags[VerseType.Other],
        u'Unknown': VerseType.Tags[VerseType.Other],
        u'Unbenannt': VerseType.Tags[VerseType.Other]
    }


class SongBeamerImport(SongImport):
    """
    Import Song Beamer files(s)
    Song Beamer file format is text based
    in the beginning are one or more control tags written
    """
    HTML_TAG_PAIRS = [
        (re.compile(u'<b>'), u'{st}'),
        (re.compile(u'</b>'), u'{/st}'),
        (re.compile(u'<i>'), u'{it}'),
        (re.compile(u'</i>'), u'{/it}'),
        (re.compile(u'<u>'), u'{u}'),
        (re.compile(u'</u>'), u'{/u}'),
        (re.compile(u'<p>'), u'{p}'),
        (re.compile(u'</p>'), u'{/p}'),
        (re.compile(u'<super>'), u'{su}'),
        (re.compile(u'</super>'), u'{/su}'),
        (re.compile(u'<sub>'), u'{sb}'),
        (re.compile(u'</sub>'), u'{/sb}'),
        (re.compile(u'<br.*?>'), u'{br}'),
        (re.compile(u'<[/]?wordwrap>'), u''),
        (re.compile(u'<[/]?strike>'), u''),
        (re.compile(u'<[/]?h.*?>'), u''),
        (re.compile(u'<[/]?s.*?>'), u''),
        (re.compile(u'<[/]?linespacing.*?>'), u''),
        (re.compile(u'<[/]?c.*?>'), u''),
        (re.compile(u'<align.*?>'), u''),
        (re.compile(u'<valign.*?>'), u'')
    ]

    def __init__(self, manager, **kwargs):
        """
        Initialise the Song Beamer importer.
        """
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        """
        Receive a single file or a list of files to import.
        """
        self.importWizard.progressBar.setMaximum(len(self.importSource))
        if not isinstance(self.importSource, list):
            return
        for file in self.importSource:
            # TODO: check that it is a valid SongBeamer file
            if self.stopImportFlag:
                return
            self.setDefaults()
            self.currentVerse = u''
            self.currentVerseType = VerseType.Tags[VerseType.Verse]
            read_verses = False
            file_name = os.path.split(file)[1]
            if os.path.isfile(file):
                detect_file = open(file, u'r')
                details = chardet.detect(detect_file.read())
                detect_file.close()
                infile = codecs.open(file, u'r', details['encoding'])
                song_data = infile.readlines()
                infile.close()
            else:
                continue
            self.title = file_name.split('.sng')[0]
            read_verses = False
            for line in song_data:
                # Just make sure that the line is of the type 'Unicode'.
                line = unicode(line).strip()
                if line.startswith(u'#') and not read_verses:
                    self.parseTags(line)
                elif line.startswith(u'---'):
                    if self.currentVerse:
                        self.replaceHtmlTags()
                        self.addVerse(self.currentVerse, self.currentVerseType)
                        self.currentVerse = u''
                        self.currentVerseType = VerseType.Tags[VerseType.Verse]
                    read_verses = True
                    verse_start = True
                elif read_verses:
                    if verse_start:
                        verse_start = False
                        if not self.checkVerseMarks(line):
                            self.currentVerse = line + u'\n'
                    else:
                        self.currentVerse += line + u'\n'
            if self.currentVerse:
                self.replaceHtmlTags()
                self.addVerse(self.currentVerse, self.currentVerseType)
            if not self.finish():
                self.logError(file)

    def replaceHtmlTags(self):
        """
        This can be called to replace SongBeamer's specific (html) tags with
        OpenLP's specific (html) tags.
        """
        for pair in SongBeamerImport.HTML_TAG_PAIRS:
            self.currentVerse = pair[0].sub(pair[1], self.currentVerse)

    def parseTags(self, line):
        """
        Parses a meta data line.

        ``line``
            The line in the file. It should consist of a tag and a value
            for this tag (unicode)::

                u'#Title=Nearer my God to Thee'
        """
        tag_val = line.split(u'=', 1)
        if len(tag_val) == 1:
            return
        if not tag_val[0] or not tag_val[1]:
            return
        if tag_val[0] == u'#(c)':
            self.addCopyright(tag_val[1])
        elif tag_val[0] == u'#AddCopyrightInfo':
            pass
        elif tag_val[0] == u'#Author':
            self.parseAuthor(tag_val[1])
        elif tag_val[0] == u'#BackgroundImage':
            pass
        elif tag_val[0] == u'#Bible':
            pass
        elif tag_val[0] == u'#Categories':
            self.topics = tag_val[1].split(',')
        elif tag_val[0] == u'#CCLI':
            self.ccliNumber = tag_val[1]
        elif tag_val[0] == u'#Chords':
            pass
        elif tag_val[0] == u'#ChurchSongID':
            pass
        elif tag_val[0] == u'#ColorChords':
            pass
        elif tag_val[0] == u'#Comments':
            self.comments = tag_val[1]
        elif tag_val[0] == u'#Editor':
            pass
        elif tag_val[0] == u'#Font':
            pass
        elif tag_val[0] == u'#FontLang2':
            pass
        elif tag_val[0] == u'#FontSize':
            pass
        elif tag_val[0] == u'#Format':
            pass
        elif tag_val[0] == u'#Format_PreLine':
            pass
        elif tag_val[0] == u'#Format_PrePage':
            pass
        elif tag_val[0] == u'#ID':
            pass
        elif tag_val[0] == u'#Key':
            pass
        elif tag_val[0] == u'#Keywords':
            pass
        elif tag_val[0] == u'#LangCount':
            pass
        elif tag_val[0] == u'#Melody':
            self.parseAuthor(tag_val[1])
        elif tag_val[0] == u'#NatCopyright':
            pass
        elif tag_val[0] == u'#OTitle':
            pass
        elif tag_val[0] == u'#OutlineColor':
            pass
        elif tag_val[0] == u'#OutlinedFont':
            pass
        elif tag_val[0] == u'#QuickFind':
            pass
        elif tag_val[0] == u'#Rights':
            song_book_pub = tag_val[1]
        elif tag_val[0] == u'#Songbook' or tag_val[0] == u'#SongBook':
            book_data = tag_val[1].split(u'/')
            self.songBookName = book_data[0].strip()
            if len(book_data) == 2:
                number = book_data[1].strip()
                self.songNumber = number if number.isdigit() else u''
        elif tag_val[0] == u'#Speed':
            pass
        elif tag_val[0] == u'Tempo':
            pass
        elif tag_val[0] == u'#TextAlign':
            pass
        elif tag_val[0] == u'#Title':
            self.title = unicode(tag_val[1])
        elif tag_val[0] == u'#TitleAlign':
            pass
        elif tag_val[0] == u'#TitleFontSize':
            pass
        elif tag_val[0] == u'#TitleLang2':
            pass
        elif tag_val[0] == u'#TitleLang3':
            pass
        elif tag_val[0] == u'#TitleLang4':
            pass
        elif tag_val[0] == u'#Translation':
            pass
        elif tag_val[0] == u'#Transpose':
            pass
        elif tag_val[0] == u'#TransposeAccidental':
            pass
        elif tag_val[0] == u'#Version':
            pass
        elif tag_val[0] == u'#VerseOrder':
            # TODO: add the verse order.
            pass

    def checkVerseMarks(self, line):
        """
        Check and add the verse's MarkType. Returns ``True`` if the given line
        contains a correct verse mark otherwise ``False``.

        ``line``
            The line to check for marks (unicode).
        """
        marks = line.split(u' ')
        if len(marks) <= 2 and marks[0] in SongBeamerTypes.MarkTypes:
            self.currentVerseType = SongBeamerTypes.MarkTypes[marks[0]]
            if len(marks) == 2:
                # If we have a digit, we append it to current_verse_type.
                if marks[1].isdigit():
                    self.currentVerseType += marks[1]
            return True
        return False
