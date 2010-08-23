# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund, Derek Scotney                            #
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

from songimport import SongImport

log = logging.getLogger(__name__)

class SongSelectFileImportError(Exception):
    pass

class SongSelectFileImport(object):
    """
    Import songs from CCLI SongSelect files in both .txt and .usr formats
    http://www.ccli.com

    The format of the .txt format is:
    ==========
    Song Title
    <>
    Description of following text (Verse/Chorus) and number
    <verse/chorus lyrics>
    <>
    <>
    Next text block description (etc)
    <verse/chorus lyrics>
    <>
    <>
    CCLI Number (e.g.CCLI-Liednummer: 2672885)
    Copyright "|" delimited (e.g. © 1999 Integrity's Hosanna! Music | LenSongs Publishing)
    Authors "|" delimited (e.g. Lenny LeBlanc | Paul Baloche)
    Licencing info (e.g. For use solely with the SongSelect Terms of Use.  All rights Reserved.  www.ccli.com)
    CCLI Licence number (e.g. CCL-Liedlizenznummer: 14 / CCLI License No. 14)
    ==========

    The format of the .usr format is:
    ==========
    [File]
    Type=SongSelect Import File
    Version=3.0
    [S A2672885]
    Title=Above All
    Author=LeBlanc, Lenny | Baloche, Paul
    Copyright=1999 Integrity's Hosanna! Music | LenSongs Publishing (Verwaltet von Gerth Medien Musikverlag) | (Verwaltet von Gerth Medien Musikverlag)
    Admin=Gerth Medien Musikverlag
    Themes=Cross/tKingship/tMajesty/tRedeemer
    Keys=A
    Fields=Vers 1/tVers 2/tChorus 1/tAndere 1
    Words=Above all powers.... [/n = CR, /n/t = CRLF]
    ==========

    """
    
    def __init__(self, songmanager):
        """
        Initialise the class. Requires a songmanager class which
        is passed to SongImport for writing song to disk
        """
        self.songmanager = songmanager
        self.song = None

    def do_import(self, filename, commit=True):
        """
        Import either a .usr or a .txt SongSelect file
        If the commit parameter is set False,
        the import will not be committed to the database
        (useful for test scripts)
        """
        self.song_import = SongImport(self.songmanager)

        lines = []
        filename = unicode(filename)
        if os.path.isfile(filename):
            detect_file = open(filename, u'r')
            details = chardet.detect(detect_file.read(2048))
            detect_file.close()
            infile = codecs.open(filename, u'r', details['encoding'])
            lines = infile.readlines()

            ext = os.path.splitext(filename)[1]
            if ext.lower() == ".usr":
                log.info('SongSelect .usr format file found %s', filename)
                self.do_import_usr_file(lines)
                if commit:
                    self.finish()
            elif ext.lower() == ".txt":
                log.info('SongSelect .txt format file found %s', filename)
                self.do_import_txt_file(lines)
                if commit:
                    self.finish()
            else:
                log.info(u'Extension %s is not valid', filename)
                pass


    def do_import_usr_file(self, textList):
        """
        Process the USR file - pass in a list of lines
        """

        n = 0 # line number
        lyrics = []

        for line in textList:
            n += 1
            if line.startswith(u'Title='):
                sname = line[6:].strip()
            elif line.startswith(u'Author='):
                sauthor = line[7:].strip()
            elif line.startswith(u'Copyright='):
                scopyright = line[10:].strip()
            elif line.startswith(u'[S A'):
                sccli = line[4:-3].strip()
            elif line.startswith(u'Fields='):
            #Fields contain single line indicating verse, chorus, etc,
            #/t delimited, same as with words field. store seperately
            #and process at end.
                sfields = line[7:].strip()
            elif line.startswith(u'Words='):
                swords = line[6:].strip()
            #Unhandled usr keywords:Type, Version, Admin, Themes, Keys

        #Process Fields and words sections
        fieldlst = sfields.split(u'/t')
        wordslst = swords.split(u'/t')
        for i in range(0, len(fieldlst)):
            if fieldlst[i].startswith(u'Ver'): #Verse
                vtype = u'V'
            elif fieldlst[i].startswith(u'Ch'): #Chorus
                vtype = u'C'
            elif fieldlst[i].startswith(u'Br'): #Bridge
                vtype = u'B'
            else: #Other
                vtype = u'O'
            vcontent = unicode(wordslst[i])
            vcontent = vcontent.replace("/n",  "\n")
            self.song_import.add_verse(vcontent, vtype);

        #Handle multiple authors
        lst = sauthor.split(u'/')
        if len(lst) < 2:
            lst = sauthor.split(u'|')
        for author in lst:
            seperated = author.split(u',')
            self.song_import.add_author(seperated[1].strip() + " " + seperated[0].strip())

        self.song_import.title = sname
        self.song_import.copyright = scopyright
        self.song_import.ccli_number = sccli


    def do_import_txt_file(self, textList):
        """
        Process the TXT file - pass in a list of lines
        """

        n = 0
        vcontent = u''
        scomments = u''
        scopyright = u'';
        verse_start = False

        for line in textList:
            ln = line.strip()
            if (len(ln)== 0):
                if (n==0):
                    continue
                elif (verse_start == True):
                    self.song_import.add_verse(vcontent, vtype)
                    vcontent = ''
                    verse_start = False
            else:
                if (n==0): #n=0, song title
                    sname = ln
                    n += 1
                elif (n==1): #n=1, verses
                    if ln.startswith(u'CCLI'): #n=1, ccli number, first line after verses
                        n += 1
                        cparts = ln.split(' ')
                        sccli = cparts[len(cparts)-1]
                    elif (verse_start == False):
                        # We have the verse descriptor
                        parts = ln.split(' ')
                        if (len(parts) == 2):
                            if parts[0].startswith(u'Ver'): #Verse
                                vtype = u'V'
                            elif parts[0].startswith(u'Ch'): #Chorus
                                vtype = u'C'
                            elif parts[0].startswith(u'Br'): #Bridge
                                vtype = u'B'
                            else:
                                vtype = u'O'
                            vnumber = parts[1]
                        else:
                            vtype = u'O'
                            vnumber = 1
                        verse_start = True
                    else:
                        # We have verse content or the start of the last part
                        # Add l so as to keep the CRLF
                        vcontent = vcontent + line
                else:
                    if (n==2): #n=2, copyright
                        n += 1
                        scopyright = ln
                    elif (n==3): #n=3, authors
                        n += 1
                        sauthor = ln
                    elif (n==4) and (not ln.startswith(u'CCL')): #n=4, comments lines before last line
                        scomments = scomments + ln
        # split on known separators
        alist = sauthor.split(u'/')
        if len(alist) < 2:
            alist = sauthor.split(u'|')
        self.song_import.authors = alist
        self.song_import.title = sname
        self.song_import.copyright = scopyright
        self.song_import.ccli_number = sccli
        self.song_import.comments = scomments


    def finish(self):
        """ Separate function, allows test suite to not pollute database"""
        self.song_import.finish()
