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
The :mod:`songproimport` module provides the functionality for importing SongPro
songs into the OpenLP database.
"""
import re
import os
import logging

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport

log = logging.getLogger(__name__)

class SongProImport(SongImport):
    """
    The :class:`SongProImport` class provides the ability to import song files
    from SongPro export files.

    **SongPro Song File Format:**

    SongPro has the option to export under its File menu
    This produces files containing single or multiple songs
    The file is text with lines tagged with # followed by an identifier.
    This is documented here: http://creationsoftware.com/ImportIdentifiers.php
    An example here: http://creationsoftware.com/ExampleImportingManySongs.txt

    #A - next line is the Song Author
    #B - the lines following until next tagged line are the "Bridge" words
        (can be in rtf or plain text) which we map as B1
    #C - the lines following until next tagged line are the chorus words
        (can be in rtf or plain text)
        which we map as C1
    #D - the lines following until next tagged line are the "Ending" words
        (can be in rtf or plain text) which we map as E1
    #E - this song ends here, so we process the song -
        and start again at the next line
    #G - next line is the Group
    #M - next line is the Song Number
    #N - next line are Notes
    #R - next line is the SongCopyright
    #O - next line is the Verse Sequence
    #T - next line is the Song Title
    #1 - #7 the lines following until next tagged line are the verse x words
        (can be in rtf or plain text)
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the SongPro importer.
        """
        SongImport.__init__(self, manager, **kwargs)

    def doImport(self):
        """
        Receive a single file or a list of files to import.
        """
        with open(self.importSource, 'r') as songs_file:
            self.importWizard.progressBar.setMaximum(0)
            tag = u''
            text = u''
            for file_line in songs_file:
                if self.stopImportFlag:
                    break
                file_line = unicode(file_line, u'cp1252')
                file_text = file_line.rstrip()
                if file_text and file_text[0] == u'#':
                    self.processSection(tag, text.rstrip())
                    tag = file_text[1:]
                    text = u''
                else:
                    text += file_line

    def processSection(self, tag, text):
        """
        Process a section of the song, i.e. title, verse etc.
        """
        if tag == u'T':
            self.setDefaults()
            if text:
                self.title = text
            self.importWizard.incrementProgressBar(u'Processing song ' + text,
                0)
            return
        elif tag == u'E':
            self.finish()
            return
        if u'rtf1' in text:
            text = striprtf(text).rstrip()
        if not text:
            return
        if tag == u'A':
            self.parseAuthor(text)
        elif tag in [u'B', u'C']:
            self.addVerse(text, tag)
        elif tag == u'D':
            self.addVerse(text, u'E')
        elif tag == u'G':
            self.topics.append(text)
        elif tag == u'M':
            matches = re.findall(r'\d+', text)
            if matches:
                self.songNumber = matches[-1]
                self.songBookName = text[:text.rfind(self.songNumber)]
        elif tag == u'N':
            self.comments = text
        elif tag == u'O':
            for char in text:
                if char == u'C':
                    self.verseOrderList.append(u'C1')
                elif char == u'B':
                    self.verseOrderList.append(u'B1')
                elif char == u'D':
                    self.verseOrderList.append(u'E1')
                elif u'1' <= char <= '7':
                    self.verseOrderList.append(u'V' + char)
        elif tag == u'R':
            self.addCopyright(text)
        elif u'1' <= tag <= u'7':
            self.addVerse(text, u'V' + tag[1:])

# replace with mahfiaz's shared one when his import is merged
def striprtf(text):
   pattern = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
   # control words which specify a "destionation".
   destinations = frozenset((
      'aftncn','aftnsep','aftnsepc','annotation','atnauthor','atndate','atnicn','atnid',
      'atnparent','atnref','atntime','atrfend','atrfstart','author','background',
      'bkmkend','bkmkstart','blipuid','buptim','category','colorschememapping',
      'colortbl','comment','company','creatim','datafield','datastore','defchp','defpap',
      'do','doccomm','docvar','dptxbxtext','ebcend','ebcstart','factoidname','falt',
      'fchars','ffdeftext','ffentrymcr','ffexitmcr','ffformat','ffhelptext','ffl',
      'ffname','ffstattext','field','file','filetbl','fldinst','fldrslt','fldtype',
      'fname','fontemb','fontfile','fonttbl','footer','footerf','footerl','footerr',
      'footnote','formfield','ftncn','ftnsep','ftnsepc','g','generator','gridtbl',
      'header','headerf','headerl','headerr','hl','hlfr','hlinkbase','hlloc','hlsrc',
      'hsv','htmltag','info','keycode','keywords','latentstyles','lchars','levelnumbers',
      'leveltext','lfolevel','linkval','list','listlevel','listname','listoverride',
      'listoverridetable','listpicture','liststylename','listtable','listtext',
      'lsdlockedexcept','macc','maccPr','mailmerge','maln','malnScr','manager','margPr',
      'mbar','mbarPr','mbaseJc','mbegChr','mborderBox','mborderBoxPr','mbox','mboxPr',
      'mchr','mcount','mctrlPr','md','mdeg','mdegHide','mden','mdiff','mdPr','me',
      'mendChr','meqArr','meqArrPr','mf','mfName','mfPr','mfunc','mfuncPr','mgroupChr',
      'mgroupChrPr','mgrow','mhideBot','mhideLeft','mhideRight','mhideTop','mhtmltag',
      'mlim','mlimloc','mlimlow','mlimlowPr','mlimupp','mlimuppPr','mm','mmaddfieldname',
      'mmath','mmathPict','mmathPr','mmaxdist','mmc','mmcJc','mmconnectstr',
      'mmconnectstrdata','mmcPr','mmcs','mmdatasource','mmheadersource','mmmailsubject',
      'mmodso','mmodsofilter','mmodsofldmpdata','mmodsomappedname','mmodsoname',
      'mmodsorecipdata','mmodsosort','mmodsosrc','mmodsotable','mmodsoudl',
      'mmodsoudldata','mmodsouniquetag','mmPr','mmquery','mmr','mnary','mnaryPr',
      'mnoBreak','mnum','mobjDist','moMath','moMathPara','moMathParaPr','mopEmu',
      'mphant','mphantPr','mplcHide','mpos','mr','mrad','mradPr','mrPr','msepChr',
      'mshow','mshp','msPre','msPrePr','msSub','msSubPr','msSubSup','msSubSupPr','msSup',
      'msSupPr','mstrikeBLTR','mstrikeH','mstrikeTLBR','mstrikeV','msub','msubHide',
      'msup','msupHide','mtransp','mtype','mvertJc','mvfmf','mvfml','mvtof','mvtol',
      'mzeroAsc','mzeroDesc','mzeroWid','nesttableprops','nextfile','nonesttables',
      'objalias','objclass','objdata','object','objname','objsect','objtime','oldcprops',
      'oldpprops','oldsprops','oldtprops','oleclsid','operator','panose','password',
      'passwordhash','pgp','pgptbl','picprop','pict','pn','pnseclvl','pntext','pntxta',
      'pntxtb','printim','private','propname','protend','protstart','protusertbl','pxe',
      'result','revtbl','revtim','rsidtbl','rxe','shp','shpgrp','shpinst',
      'shppict','shprslt','shptxt','sn','sp','staticval','stylesheet','subject','sv',
      'svb','tc','template','themedata','title','txe','ud','upr','userprops',
      'wgrffmtfilter','windowcaption','writereservation','writereservhash','xe','xform',
      'xmlattrname','xmlattrvalue','xmlclose','xmlname','xmlnstbl',
      'xmlopen',
   ))
   # Translation of some special characters.
   specialchars = {
      'par': '\n',
      'sect': '\n\n',
      'page': '\n\n',
      'line': '\n',
      'tab': '\t',
      'emdash': u'\u2014',
      'endash': u'\u2013',
      'emspace': u'\u2003',
      'enspace': u'\u2002',
      'qmspace': u'\u2005',
      'bullet': u'\u2022',
      'lquote': u'\u2018',
      'rquote': u'\u2019',
      'ldblquote': u'\201C',
      'rdblquote': u'\u201D',
   }
   stack = []
   ignorable = False       # Whether this group (and all inside it) are "ignorable".
   ucskip = 1              # Number of ASCII characters to skip after a unicode character.
   curskip = 0             # Number of ASCII characters left to skip
   out = []                # Output buffer.
   for match in pattern.finditer(text):
      word,arg,hex,char,brace,tchar = match.groups()
      if brace:
         curskip = 0
         if brace == '{':
            # Push state
            stack.append((ucskip,ignorable))
         elif brace == '}':
            # Pop state
            ucskip,ignorable = stack.pop()
      elif char: # \x (not a letter)
         curskip = 0
         if char == '~':
            if not ignorable:
                out.append(u'\xA0')
         elif char in '{}\\':
            if not ignorable:
               out.append(char)
         elif char == '*':
            ignorable = True
      elif word: # \foo
         curskip = 0
         if word in destinations:
            ignorable = True
         elif ignorable:
            pass
         elif word in specialchars:
            out.append(specialchars[word])
         elif word == 'uc':
            ucskip = int(arg)
         elif word == 'u':
            c = int(arg)
            if c < 0: c += 0x10000
            if c > 127: out.append(unichr(c))
            else: out.append(chr(c))
            curskip = ucskip
      elif hex: # \'xx
         if curskip > 0:
            curskip -= 1
         elif not ignorable:
            c = int(hex,16)
            if c > 127: out.append(unichr(c))
            else: out.append(chr(c))
      elif tchar:
         if curskip > 0:
            curskip -= 1
         elif not ignorable:
            out.append(tchar)
   return ''.join(out)
