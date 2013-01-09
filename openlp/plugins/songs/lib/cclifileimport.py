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
import os
import chardet
import codecs

from openlp.core.lib import translate
from openlp.plugins.songs.lib import VerseType
from songimport import SongImport

log = logging.getLogger(__name__)

class CCLIFileImport(SongImport):
    """
    The :class:`CCLIFileImport` class provides OpenLP with the ability to import
    CCLI SongSelect song files in both .txt and .usr formats. See
    `<http://www.ccli.com/>`_ for more details.
    """

    def __init__(self, manager, **kwargs):
        """
        Initialise the import.

        ``manager``
            The song manager for the running OpenLP installation.

        ``filenames``
            The files to be imported.
        """
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        """
        Import either a ``.usr`` or a ``.txt`` SongSelect file.
        """
        log.debug(u'Starting CCLI File Import')
        self.importWizard.progressBar.setMaximum(len(self.importSource))
        for filename in self.importSource:
            filename = unicode(filename)
            log.debug(u'Importing CCLI File: %s', filename)
            lines = []
            if os.path.isfile(filename):
                detect_file = open(filename, u'r')
                detect_content = detect_file.read(2048)
                try:
                    unicode(detect_content, u'utf-8')
                    details = {'confidence': 1, 'encoding': 'utf-8'}
                except UnicodeDecodeError:
                    details = chardet.detect(detect_content)
                detect_file.close()
                infile = codecs.open(filename, u'r', details['encoding'])
                if not infile.read(1) == u'\ufeff':
                    # not UTF or no BOM was found
                    infile.seek(0)
                lines = infile.readlines()
                infile.close()
                ext = os.path.splitext(filename)[1]
                if ext.lower() == u'.usr':
                    log.info(u'SongSelect .usr format file found: %s', filename)
                    if not self.doImportUsrFile(lines):
                        self.logError(filename)
                elif ext.lower() == u'.txt':
                    log.info(u'SongSelect .txt format file found: %s', filename)
                    if not self.doImportTxtFile(lines):
                        self.logError(filename)
                else:
                    self.logError(filename,
                        translate('SongsPlugin.CCLIFileImport', 'The file does not have a valid extension.'))
                    log.info(u'Extension %s is not valid', filename)
            if self.stopImportFlag:
                return

    def doImportUsrFile(self, textList):
        """
        The :func:`doImport_usr_file` method provides OpenLP with the ability
        to import CCLI SongSelect songs in *USR* file format.

        ``textList``
            An array of strings containing the usr file content.

        **SongSelect .usr file format**

        ``[File]``
            USR file format first line

        ``Type=``
            Indicates the file type
            e.g. *Type=SongSelect Import File*

        ``Version=3.0``
            File format version

        ``[S A2672885]``
            Contains the CCLI Song number e.g. *2672885*

        ``Title=``
            Contains the song title (e.g. *Title=Above All*)

        ``Author=``
            Contains a | delimited list of the song authors
            e.g. *Author=LeBlanc, Lenny | Baloche, Paul*

        ``Copyright=``
            Contains a | delimited list of the song copyrights
            e.g. Copyright=1999 Integrity's Hosanna! Music |
            LenSongs Publishing (Verwaltet von Gerth Medien
            Musikverlag)

        ``Admin=``
            Contains the song administrator
            e.g. *Admin=Gerth Medien Musikverlag*

        ``Themes=``
            Contains a /t delimited list of the song themes
            e.g. *Themes=Cross/tKingship/tMajesty/tRedeemer*

        ``Keys=``
            Contains the keys in which the music is played??
            e.g. *Keys=A*

        ``Fields=``
            Contains a list of the songs fields in order /t delimited
            e.g. *Fields=Vers 1/tVers 2/tChorus 1/tAndere 1*

        ``Words=``
            Contains the songs various lyrics in order as shown by the
            *Fields* description
            e.g. *Words=Above all powers....* [/n = CR, /n/t = CRLF]

        """
        log.debug(u'USR file text: %s', textList)
        song_author = u''
        song_topics = u''
        for line in textList:
            if line.startswith(u'[S '):
                ccli, line = line.split(u']', 1)
                if ccli.startswith(u'[S A'):
                    self.ccliNumber = ccli[4:].strip()
                else:
                    self.ccliNumber = ccli[3:].strip()
            if line.startswith(u'Title='):
                self.title = line[6:].strip()
            elif line.startswith(u'Author='):
                song_author = line[7:].strip()
            elif line.startswith(u'Copyright='):
                self.copyright = line[10:].strip()
            elif line.startswith(u'Themes='):
                song_topics = line[7:].strip().replace(u' | ', u'/t')
            elif line.startswith(u'Fields='):
                # Fields contain single line indicating verse, chorus, etc,
                # /t delimited, same as with words field. store seperately
                # and process at end.
                song_fields = line[7:].strip()
            elif line.startswith(u'Words='):
                song_words = line[6:].strip()
            # Unhandled usr keywords: Type, Version, Admin, Keys
        # Process Fields and words sections.
        check_first_verse_line = False
        field_list = song_fields.split(u'/t')
        words_list = song_words.split(u'/t')
        for counter in range(len(field_list)):
            if field_list[counter].startswith(u'Ver'):
                verse_type = VerseType.Tags[VerseType.Verse]
            elif field_list[counter].startswith(u'Ch'):
                verse_type = VerseType.Tags[VerseType.Chorus]
            elif field_list[counter].startswith(u'Br'):
                verse_type = VerseType.Tags[VerseType.Bridge]
            else:
                verse_type = VerseType.Tags[VerseType.Other]
                check_first_verse_line = True
            verse_text = unicode(words_list[counter])
            verse_text = verse_text.replace(u'/n', u'\n')
            verse_text = verse_text.replace(u' | ', u'\n')
            verse_lines = verse_text.split(u'\n', 1)
            if check_first_verse_line:
                if verse_lines[0].startswith(u'(PRE-CHORUS'):
                    verse_type = VerseType.Tags[VerseType.PreChorus]
                    log.debug(u'USR verse PRE-CHORUS: %s', verse_lines[0])
                    verse_text = verse_lines[1]
                elif verse_lines[0].startswith(u'(BRIDGE'):
                    verse_type = VerseType.Tags[VerseType.Bridge]
                    log.debug(u'USR verse BRIDGE')
                    verse_text = verse_lines[1]
                elif verse_lines[0].startswith(u'('):
                    verse_type = VerseType.Tags[VerseType.Other]
                    verse_text = verse_lines[1]
            if verse_text:
                self.addVerse(verse_text, verse_type)
            check_first_verse_line = False
        # Handle multiple authors
        author_list = song_author.split(u'/')
        if len(author_list) < 2:
            author_list = song_author.split(u'|')
        for author in author_list:
            separated = author.split(u',')
            if len(separated) > 1:
                author = u' '.join(map(unicode.strip, reversed(separated)))
            self.addAuthor(author.strip())
        self.topics = [topic.strip() for topic in song_topics.split(u'/t')]
        return self.finish()

    def doImportTxtFile(self, textList):
        """
        The :func:`doImport_txt_file` method provides OpenLP with the ability
        to import CCLI SongSelect songs in *TXT* file format.

        ``textList``
            An array of strings containing the txt file content.

        SongSelect .txt file format::

            Song Title                  # Contains the song title
            <Empty line>
            Verse type and number       # e.g. Verse 1, Chorus 1
            Verse lyrics
            <Empty line>
            <Empty line>
            Verse type and number (repeats)
            Verse lyrics
            <Empty line>
            <Empty line>
            Song CCLI number
                # e.g. CCLI Number (e.g.CCLI-Liednummer: 2672885)
            Song copyright (if it begins ©, otherwise after authors)
                # e.g. © 1999 Integrity's Hosanna! Music | LenSongs Publishing
            Song authors                # e.g. Lenny LeBlanc | Paul Baloche
            Licencing info
                # e.g. For use solely with the SongSelect Terms of Use.
            All rights Reserved.  www.ccli.com
            CCLI Licence number of user
                # e.g. CCL-Liedlizenznummer: 14 / CCLI License No. 14

        """
        log.debug(u'TXT file text: %s', textList)
        line_number = 0
        check_first_verse_line = False
        verse_text = u''
        song_author = u''
        verse_start = False
        for line in textList:
            clean_line = line.strip()
            if not clean_line:
                if line_number == 0:
                    continue
                elif verse_start:
                    if verse_text:
                        self.addVerse(verse_text, verse_type)
                        verse_text = u''
                        verse_start = False
            else:
                #line_number=0, song title
                if line_number == 0:
                    self.title = clean_line
                    line_number += 1
                #line_number=1, verses
                elif line_number == 1:
                    #line_number=1, ccli number, first line after verses
                    if clean_line.startswith(u'CCLI'):
                        line_number += 1
                        ccli_parts = clean_line.split(' ')
                        self.ccliNumber = ccli_parts[len(ccli_parts) - 1]
                    elif not verse_start:
                        # We have the verse descriptor
                        verse_desc_parts = clean_line.split(u' ')
                        if len(verse_desc_parts) == 2:
                            if verse_desc_parts[0].startswith(u'Ver'):
                                verse_type = VerseType.Tags[VerseType.Verse]
                            elif verse_desc_parts[0].startswith(u'Ch'):
                                verse_type = VerseType.Tags[VerseType.Chorus]
                            elif verse_desc_parts[0].startswith(u'Br'):
                                verse_type = VerseType.Tags[VerseType.Bridge]
                            else:
                                # we need to analyse the next line for
                                # verse type, so set flag
                                verse_type = VerseType.Tags[VerseType.Other]
                                check_first_verse_line = True
                            verse_number = verse_desc_parts[1]
                        else:
                            verse_type = VerseType.Tags[VerseType.Other]
                            verse_number = 1
                        verse_start = True
                    else:
                        # check first line for verse type
                        if check_first_verse_line:
                            if line.startswith(u'(PRE-CHORUS'):
                                verse_type = VerseType.Tags[VerseType.PreChorus]
                            elif line.startswith(u'(BRIDGE'):
                                verse_type = VerseType.Tags[VerseType.Bridge]
                            # Handle all other misc types
                            elif line.startswith(u'('):
                                verse_type = VerseType.Tags[VerseType.Other]
                            else:
                                verse_text = verse_text + line
                            check_first_verse_line = False
                        else:
                            # We have verse content or the start of the
                            # last part. Add l so as to keep the CRLF
                            verse_text = verse_text + line
                else:
                    #line_number=2, copyright
                    if line_number == 2:
                        line_number += 1
                        if clean_line.startswith(u'©'):
                            self.copyright = clean_line
                        else:
                            song_author = clean_line
                    #n=3, authors
                    elif line_number == 3:
                        line_number += 1
                        if song_author:
                            self.copyright = clean_line
                        else:
                            song_author = clean_line
                    #line_number=4, comments lines before last line
                    elif line_number == 4 and not clean_line.startswith(u'CCL'):
                        self.comments += clean_line
        # split on known separators
        author_list = song_author.split(u'/')
        if len(author_list) < 2:
            author_list = song_author.split(u'|')
        # Clean spaces before and after author names.
        for author_name in author_list:
            self.addAuthor(author_name.strip())
        return self.finish()
