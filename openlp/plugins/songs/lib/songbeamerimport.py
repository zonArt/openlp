# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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
import os
import re
import logging

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
        u'Unknown': u'O'
        }

class SongBeamerImport(SongImport):
    """
    """

    def __init__(self, master_manager, **kwargs):
        """
        Initialise the import.

        ``master_manager``
            The song manager for the running OpenLP installation.
        """
        SongImport.__init__(self, master_manager)
        self.master_manager = master_manager
        if kwargs.has_key(u'filename'):
            self.import_source = kwargs[u'filename']
        if kwargs.has_key(u'filenames'):
            self.import_source = kwargs[u'filenames']
        log.debug(self.import_source)

    def do_import(self):
        """
        Recieve a single file, or a list of files to import.
        """
        
        if isinstance(self.import_source,  list):
            self.import_wizard.importProgressBar.setMaximum(
                len(self.import_source))
            for file in self.import_source:
                # TODO: check that it is a valid SongBeamer file
                self.current_verse = u'' 
                self.current_verse_type = u'V'
                self.file_name = os.path.split(file)[1]
                self.import_wizard.incrementProgressBar(
                    "Importing %s" % (self.file_name),  0)
                self.songFile = open(file, 'r')
                self.songData = self.songFile.read().decode('utf8')
                self.songData = self.songData.splitlines()
                self.songFile.close()
                for line in self.songData:
                    if line.startswith('#'):
                        log.debug(u'find tag: %s' % line)
                        if not self.parse_tags(line):
                            return False
                    elif line.startswith('---'):
                        log.debug(u'find ---')
                        if len(self.current_verse) > 0:
                            self.add_verse(self.current_verse, self.current_verse_type)
                            self.current_verse = u'' 
                            self.current_verse_type = u'V'
                        self.read_verse = True
                        self.verse_start = True
                    elif self.read_verse:
                        if self.verse_start:
                            self.check_verse_marks(line)
                            self.verse_start = False
                        else:
                            self.current_verse += u'%s\n' % line
                if len(self.current_verse) > 0:
                    self.add_verse(self.current_verse, self.current_verse_type)
                self.finish()
                self.import_wizard.incrementProgressBar(
                    "Importing %s" % (self.file_name))
            return True
            
    def parse_tags(self, line):
        tag_val = line.split('=')
        if len(tag_val[0]) == 0 or \
            len(tag_val[1]) == 0:
            return True
        if tag_val[0] == '#(c)':
            self.add_copyright(tag_val[1])
        elif tag_val[0] == '#AddCopyrightInfo':
            pass
        elif tag_val[0] == '#Author':
            #TODO split Authors
            self.add_author(tag_val[1])
        elif tag_val[0] == '#BackgroundImage':
            pass
        elif tag_val[0] == '#Bible':
            pass
        elif tag_val[0] == '#Categories':
            pass
        elif tag_val[0] == '#CCLI':
            self.ccli_number = tag_val[1]
        elif tag_val[0] == '#Chords':
            pass
        elif tag_val[0] == '#ChurchSongID':
            pass
        elif tag_val[0] == '#ColorChords':
            pass
        elif tag_val[0] == '#Comments':
            self.comments = tag_val[1]
        elif tag_val[0] == '#Editor':
            pass
        elif tag_val[0] == '#Font':
            pass
        elif tag_val[0] == '#FontLang2':
            pass
        elif tag_val[0] == '#FontSize':
            pass
        elif tag_val[0] == '#Format':
            pass
        elif tag_val[0] == '#Format_PreLine':
            pass
        elif tag_val[0] == '#Format_PrePage':
            pass
        elif tag_val[0] == '#ID':
            pass
        elif tag_val[0] == '#Key':
            pass
        elif tag_val[0] == '#Keywords':
            pass
        elif tag_val[0] == '#LangCount':
            pass
        elif tag_val[0] == '#Melody':
            #TODO split Authors
            self.add_author(tag_val[1])
        elif tag_val[0] == '#NatCopyright':
            pass
        elif tag_val[0] == '#OTitle':
            pass
        elif tag_val[0] == '#OutlineColor':
            pass
        elif tag_val[0] == '#OutlinedFont':
            pass
        elif tag_val[0] == '#QuickFind':
            pass
        elif tag_val[0] == '#Rights':
            song_book_pub = tag_val[1]
        elif tag_val[0] == '#Songbook':
            book_num = tag_val[1].split(' / ')
            self.song_book_name = book_num[0]
            if len(book_num) == book_num[1]:
                self.song_number = u''
        elif tag_val[0] == '#Speed':
            pass
        elif tag_val[0] == '#TextAlign':
            pass
        elif tag_val[0] == '#Title':
            self.title = u'%s' % tag_val[1]
        elif tag_val[0] == '#TitleAlign':
            pass
        elif tag_val[0] == '#TitleFontSize':
            pass
        elif tag_val[0] == '#TitleLang2':
            pass
        elif tag_val[0] == '#TitleLang3':
            pass
        elif tag_val[0] == '#TitleLang4':
            pass
        elif tag_val[0] == '#Translation':
            pass
        elif tag_val[0] == '#Transpose':
            pass
        elif tag_val[0] == '#TransposeAccidental':
            pass
        elif tag_val[0] == '#Version':
            pass
        else:
            pass
        return True
                
        
    def check_verse_marks(self, line):
        marks = line.split(' ')
        if len(marks) <= 2 and \
            marks[0] in SongBeamerTypes.MarkTypes:
            self.current_verse_type = SongBeamerTypes.MarkTypes[marks[0]]
            if len(marks) == 2:
                #TODO: may check, because of only digits are allowed
                self.current_verse_type += marks[1]
