# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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

from openlp.core.ui.wizard import WizardStrings
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class SongBeamerTypes(object):
    MarkTypes = {
        u'Refrain': u'C',
        u'Chorus': u'C',
        u'Vers': u'V',
        u'Verse': u'V',
        u'Strophe': u'V',
        u'Intro': u'I',
        u'Coda': u'E',
        u'Ending': u'E',
        u'Bridge': u'B',
        u'Interlude': u'B',
        u'Zwischenspiel': u'B',
        u'Pre-Chorus': u'P',
        u'Pre-Refrain': u'P',
        u'Pre-Bridge': u'O',
        u'Pre-Coda': u'O',
        u'Unbekannt': u'O',
        u'Unknown': u'O',
        u'Unbenannt': u'O'
        }


class SongBeamerImport(SongImport):
    """
    Import Song Beamer files(s)
    Song Beamer file format is text based
    in the beginning are one or more control tags written
    """
    def __init__(self, master_manager, **kwargs):
        """
        Initialise the import.

        ``master_manager``
            The song manager for the running OpenLP installation.
        """
        SongImport.__init__(self, master_manager)
        if kwargs.has_key(u'filename'):
            self.import_source = kwargs[u'filename']
        if kwargs.has_key(u'filenames'):
            self.import_source = kwargs[u'filenames']
        log.debug(self.import_source)

    def do_import(self):
        """
        Receive a single file or a list of files to import.
        """
        if isinstance(self.import_source, list):
            self.import_wizard.progressBar.setMaximum(
                len(self.import_source))
            for file in self.import_source:
                # TODO: check that it is a valid SongBeamer file
                self.set_defaults()
                self.current_verse = u''
                self.current_verse_type = u'V'
                read_verses = False
                file_name = os.path.split(file)[1]
                self.import_wizard.incrementProgressBar(
                    WizardStrings.ImportingType % file_name, 0)
                if os.path.isfile(file):
                    detect_file = open(file, u'r')
                    details = chardet.detect(detect_file.read(2048))
                    detect_file.close()
                    infile = codecs.open(file, u'r', details['encoding'])
                    songData = infile.readlines()
                    infile.close()
                else:
                    return False
                self.title = file_name.split('.sng')[0]
                read_verses = False
                for line in songData:
                    # Just make sure that the line is of the type 'Unicode'.
                    line = unicode(line).strip()
                    if line.startswith(u'#') and not read_verses:
                        self.parse_tags(line)
                    elif line.startswith(u'---'):
                        if self.current_verse:
                            self.replace_html_tags()
                            self.add_verse(self.current_verse,
                                self.current_verse_type)
                            self.current_verse = u''
                            self.current_verse_type = u'V'
                        read_verses = True
                        verse_start = True
                    elif read_verses:
                        if verse_start:
                            verse_start = False
                            if not self.check_verse_marks(line):
                                self.current_verse = line + u'\n'
                        else:
                            self.current_verse += line + u'\n'
                if self.current_verse:
                    self.replace_html_tags()
                    self.add_verse(self.current_verse, self.current_verse_type)
                if self.check_complete():
                    self.finish()
                self.import_wizard.incrementProgressBar(
                    WizardStrings.ImportingType % file_name)
            return True

    def replace_html_tags(self):
        """
        This can be called to replace SongBeamer's specific (html) tags with
        OpenLP's specific (html) tags.
        """
        tag_pairs = [
            (u'<b>', u'{st}'),
            (u'</b>', u'{/st}'),
            (u'<i>', u'{it}'),
            (u'</i>', u'{/it}'),
            (u'<u>', u'{u}'),
            (u'</u>', u'{/u}'),
            (u'<p>', u'{p}'),
            (u'</p>', u'{/p}'),
            (u'<super>', u'{su}'),
            (u'</super>', u'{/su}'),
            (u'<sub>', u'{sb}'),
            (u'</sub>', u'{/sb}'),
            (u'<[/]?br.*?>', u'{st}'),
            (u'<[/]?wordwrap>', u''),
            (u'<[/]?strike>', u''),
            (u'<[/]?h.*?>', u''),
            (u'<[/]?s.*?>', u''),
            (u'<[/]?linespacing.*?>', u''),
            (u'<[/]?c.*?>', u''),
            (u'<align.*?>', u''),
            (u'<valign.*?>', u'')
            ]
        for pair in tag_pairs:
            self.current_verse = re.compile(pair[0]).sub(pair[1],
                self.current_verse)

    def parse_tags(self, line):
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
            self.add_copyright(tag_val[1])
        elif tag_val[0] == u'#AddCopyrightInfo':
            pass
        elif tag_val[0] == u'#Author':
            self.parse_author(tag_val[1])
        elif tag_val[0] == u'#BackgroundImage':
            pass
        elif tag_val[0] == u'#Bible':
            pass
        elif tag_val[0] == u'#Categories':
            self.topics = line.split(',')
        elif tag_val[0] == u'#CCLI':
            self.ccli_number = tag_val[1]
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
            self.parse_author(tag_val[1])
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
        elif tag_val[0] == u'#Songbook':
            book_num = tag_val[1].split(' / ')
            self.song_book_name = book_num[0]
            if len(book_num) == book_num[1]:
                self.song_number = u''
        elif tag_val[0] == u'#Speed':
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

    def check_verse_marks(self, line):
        """
        Check and add the verse's MarkType. Returns ``True`` if the given line
        contains a correct verse mark otherwise ``False``.

        ``line``
            The line to check for marks (unicode).
        """
        marks = line.split(u' ')
        if len(marks) <= 2 and marks[0] in SongBeamerTypes.MarkTypes:
            self.current_verse_type = SongBeamerTypes.MarkTypes[marks[0]]
            if len(marks) == 2:
                # If we have a digit, we append it to current_verse_type.
                if marks[1].isdigit():
                    self.current_verse_type += marks[1]
            return True
        else:
            return False
