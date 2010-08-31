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

class CCLIFileImportError(Exception):
    pass

class CCLIFileImport(SongImport):
    """
    The :class:`CCLIFileImport` class provides OpenLP with the
    ability to import CCLI SongSelect song files in both .txt and
    .usr formats. See http://www.ccli.com
    """

    def __init__(self, manager, **kwargs):
        """
        Initialise the import.

        ``manager``
            The song manager for the running OpenLP installation.
        ``filenames``
            The files to be imported.
        """
        SongImport.__init__(self, manager)
        if u'filenames' in kwargs:
            self.filenames = kwargs[u'filenames']
            log.debug(self.filenames)
        else:
            raise KeyError(u'Keyword argument "filenames" not supplied.')            

    def do_import(self):
        """
        Import either a .usr or a .txt SongSelect file
        """
        log.debug(u'Starting CCLI File Import')
        song_total = len(self.filenames)
        self.import_wizard.importProgressBar.setMaximum(song_total)
        song_count = 1        
        for filename in self.filenames:
            self.import_wizard.incrementProgressBar(
                u'Importing song %s of %s' % (song_count, song_total))            
            filename = unicode(filename) 
            log.debug(u'Importing CCLI File: %s', filename)
            lines = []
            if os.path.isfile(filename):
                detect_file = open(filename, u'r')
                details = chardet.detect(detect_file.read(2048))
                detect_file.close()
                infile = codecs.open(filename, u'r', details['encoding'])
                lines = infile.readlines()
                ext = os.path.splitext(filename)[1]
                if ext.lower() == ".usr":
                    log.info(u'SongSelect .usr format file found %s: ' ,  filename)
                    self.do_import_usr_file(lines)
                elif ext.lower() == ".txt":
                    log.info(u'SongSelect .txt format file found %s: ', filename)
                    self.do_import_txt_file(lines)
                else:
                    log.info(u'Extension %s is not valid', filename)
                    pass
                song_count += 1
            if self.stop_import_flag:
                return False  
        return True

    def do_import_usr_file(self, textList):
        """
        The :method:`do_import_usr_file` method provides OpenLP
        with the ability to import CCLI SongSelect songs in
        *USR* file format   
        
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
            Contains a | delimited list of the  song authors 
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
        lyrics = []
        new_song = SongImport(self.manager)
        for line in textList:
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
            #Unhandled usr keywords:Type,Version,Admin,Themes,Keys
        #Process Fields and words sections
        fieldlst = sfields.split(u'/t')
        wordslst = swords.split(u'/t')
        for counter in range(0, len(fieldlst)):
            if fieldlst[counter].startswith(u'Ver'):
                vtype = u'V'
            elif fieldlst[counter].startswith(u'Ch'):
                vtype = u'C'
            elif fieldlst[counter].startswith(u'Br'):
                vtype = u'B'
            else: #Other
                vtype = u'O'
            vcontent = unicode(wordslst[counter])
            vcontent = vcontent.replace("/n",  "\n")
            if (len(vcontent) > 0):                
                new_song.add_verse(vcontent, vtype);
        #Handle multiple authors
        lst = sauthor.split(u'/')
        if len(lst) < 2:
            lst = sauthor.split(u'|')
        for author in lst:
            seperated = author.split(u',')
            new_song.add_author(seperated[1].strip() + " " + seperated[0].strip())
        new_song.title = sname
        new_song.copyright = scopyright
        new_song.ccli_number = sccli
        new_song.finish()

    def do_import_txt_file(self, textList):
        """
        The :method:`do_import_txt_file` method provides OpenLP
        with the ability to import CCLI SongSelect songs in
        *TXT* file format   
                
        ``textList``
            An array of strings containing the txt file content. 

        **SongSelect .txt file format**

        ``Song Title``
            Contains the song title

        <Empty line>

        ``Title of following verse/chorus and number``
            e.g. Verse 1, Chorus 1

        ``Verse/Chorus lyrics``

        <Empty line>

        <Empty line>

        ``Title of next verse/chorus (repeats)``

        ``Verse/Chorus lyrics``

        <Empty line>

        <Empty line>

        ``Song CCLI Number``
            e.g. CCLI Number (e.g.CCLI-Liednummer: 2672885)
        ``Song Copyright``
            e.g. © 1999 Integrity's Hosanna! Music | LenSongs Publishing
        ``Song Authors``    
            e.g. Lenny LeBlanc | Paul Baloche
        ``Licencing info``
            e.g. For use solely with the SongSelect Terms of Use.  
            All rights Reserved.  www.ccli.com
        ``CCLI Licence number of user``    
            e.g. CCL-Liedlizenznummer: 14 / CCLI License No. 14   
        """
        log.debug(u'TXT file text: %s', textList)
        new_song = SongImport(self.manager)
        lnum = 0
        vcontent = u''
        scomments = u''
        scopyright = u'';
        verse_start = False
        for line in textList:
            line = line.strip()
            if not line:
                if (lnum==0):
                    continue
                elif verse_start:
                      if vcontent:
                        new_song.add_verse(vcontent, vtype)
                        vcontent = ''
                        verse_start = False
            else:
                #lnum=0, song title
                if (lnum==0):
                    sname = line
                    lnum += 1
                #lnum=1, verses    
                elif (lnum==1):
                    #lnum=1, ccli number, first line after verses
                    if line.startswith(u'CCLI'):
                        lnum += 1
                        cparts = line.split(' ')
                        sccli = cparts[len(cparts)-1]
                    elif (verse_start == False):
                        # We have the verse descriptor
                        parts = line.split(' ')
                        if (len(parts) == 2):
                            if parts[0].startswith(u'Ver'):
                                vtype = u'V'
                            elif parts[0].startswith(u'Ch'):
                                vtype = u'C'
                            elif parts[0].startswith(u'Br'):
                                vtype = u'B'
                            else:
                                vtype = u'O'
                            vnumber = parts[1]
                        else:
                            vtype = u'O'
                            vnumber = 1
                        verse_start = True
                    else:
                        # We have verse content or the start of the
                        # last part. Add l so as to keep the CRLF
                        vcontent = vcontent + line
                else:
                    #lnum=2, copyright
                    if (lnum==2):
                        lnum += 1
                        scopyright = line
                    #n=3, authors    
                    elif (lnum==3):
                        lnum += 1
                        sauthor = line
                     #lnum=4, comments lines before last line    
                    elif (lnum==4) and (not line.startswith(u'CCL')):
                        scomments = scomments + line
        # split on known separators
        alist = sauthor.split(u'/')
        if len(alist) < 2:
            alist = sauthor.split(u'|')
        new_song.authors = alist
        new_song.title = sname
        new_song.copyright = scopyright
        new_song.ccli_number = sccli
        new_song.comments = scomments
        new_song.finish()
        
