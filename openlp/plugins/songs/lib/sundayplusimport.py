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
import re

from lxml import objectify
from lxml.etree import Error, LxmlError
from os.path import split

from openlp.plugins.songs.lib import VerseType, retrieve_windows_encoding
from openlp.plugins.songs.lib.songimport import SongImport
from openlp.plugins.songs.lib.ui import SongStrings

log = logging.getLogger(__name__)

class SundayPlusImport(SongImport):
    """
    Import Sunday Plus songs

    The format examples can be found attached to bug report at
    <http://support.openlp.org/issues/395>
    """
    hotkey_to_verse_type = {
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
            self.title = self.title_from_filename(file.name)
        if not self.finish():
            self.logError(file.name)

    def parse(self, data, cell = False):
        if data[0] != '[' and data[-1] != ']':
            self.logError(u'File is malformed')
            return False
        i = 1
        verse_type = VerseType.Tags[VerseType.Verse]
        while i < len(data):
            byte = data[i]
            if byte == '#':
                end = data.find(':', i+1)
                name = data[i+1:end]
                i = end + 1
                while data[i] == ' ':
                    i += 1
                if data[i] == '"':
                    end = data.find('"', i+1)
                    value = data[i+1:end]
                elif data[i] == '[':
                    j = i
                    inside_quotes = False
                    while j < len(data):
                        char = data[j]
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
                        # effectivetly overrides MARKER_NAME, if present.
                        if len(value) and \
                            value in self.hotkey_to_verse_type.keys():
                            verse_type = self.hotkey_to_verse_type[value]
                    if name == 'rtf':
                        value = self.unescape(value)
                        verse = self.strip_rtf(value, self.encoding).strip()
                        lines = verse.split('\n')
                        for i in xrange(len(lines)):
                            lines[i] = lines[i].strip()
                            line = lines[i]
                            if line[:4] in u'CCLI':
                                m = re.search(r'[0-9]+', line)
                                if m:
                                    self.ccliNumber = int(m.group(0))
                                    lines.pop(i)
                            elif line.lower() == u'public domain':
                                lines.pop(i)
                        self.addVerse('\n'.join(lines).strip(), verse_type)
                if end == -1:
                    break
                i = end + 1
            i += 1
        return True

    def title_from_filename(self, filename):
        filename = split(filename)[1]
        if len(filename) > 4 and filename[-4:].lower() == u'.ptf':
            title = filename[:-4]
        else:
            title = filename
        if title[-3:] == '1-7':
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

    def strip_rtf(self, text, encoding):
        # Thanks to Markus Jarderot (MizardX) for this code, used by permission
        # <http://stackoverflow.com/questions/188545/regular-expression-for-
        # extracting-text-from-an-rtf-string>
        pattern = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'"
            r"([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
        # Control words which specify a "destination" and we can ignore it.
        destinations = frozenset((
            'aftncn', 'aftnsep', 'aftnsepc', 'annotation', 'atnauthor', 
            'atndate', 'atnicn', 'atnid', 'atnparent', 'atnref', 'atntime',
            'atrfend', 'atrfstart', 'author', 'background', 'bkmkend',
            'bkmkstart', 'blipuid', 'buptim', 'category', 'colorschememapping',
            'colortbl', 'comment', 'company', 'creatim', 'datafield',
            'datastore', 'defchp', 'defpap', 'do', 'doccomm', 'docvar',
            'dptxbxtext', 'ebcend', 'ebcstart', 'factoidname', 'falt', 'fchars',
            'ffdeftext', 'ffentrymcr', 'ffexitmcr', 'ffformat', 'ffhelptext',
            'ffl', 'ffname', 'ffstattext', 'field', 'file', 'filetbl',
            'fldinst', 'fldrslt', 'fldtype', 'fname', 'fontemb', 'fontfile', 
            'footer', 'footerf', 'footerl', 'footerr', 'footnote',
            'formfield', 'ftncn', 'ftnsep', 'ftnsepc', 'g', 'generator',
            'gridtbl', 'header', 'headerf', 'headerl', 'headerr', 'hl', 'hlfr',
            'hlinkbase', 'hlloc', 'hlsrc', 'hsv', 'htmltag', 'info', 'keycode',
            'keywords', 'latentstyles', 'lchars', 'levelnumbers', 'leveltext',
            'lfolevel', 'linkval', 'list', 'listlevel', 'listname',
            'listoverride', 'listoverridetable', 'listpicture', 'liststylename',
            'listtable', 'listtext', 'lsdlockedexcept', 'macc', 'maccPr', 
            'mailmerge', 'maln', 'malnScr', 'manager', 'margPr', 'mbar',
            'mbarPr', 'mbaseJc', 'mbegChr', 'mborderBox', 'mborderBoxPr',
            'mbox', 'mboxPr', 'mchr', 'mcount', 'mctrlPr', 'md', 'mdeg', 
            'mdegHide', 'mden', 'mdiff', 'mdPr', 'me', 'mendChr', 'meqArr',
            'meqArrPr', 'mf', 'mfName', 'mfPr', 'mfunc', 'mfuncPr', 'mgroupChr',
            'mgroupChrPr', 'mgrow', 'mhideBot', 'mhideLeft', 'mhideRight',
            'mhideTop', 'mhtmltag', 'mlim', 'mlimloc', 'mlimlow', 'mlimlowPr',
            'mlimupp', 'mlimuppPr', 'mm', 'mmaddfieldname', 'mmath',
            'mmathPict', 'mmathPr', 'mmaxdist', 'mmc', 'mmcJc', 'mmconnectstr',
            'mmconnectstrdata', 'mmcPr', 'mmcs', 'mmdatasource',
            'mmheadersource', 'mmmailsubject', 'mmodso', 'mmodsofilter',
            'mmodsofldmpdata', 'mmodsomappedname', 'mmodsoname',
            'mmodsorecipdata', 'mmodsosort', 'mmodsosrc', 'mmodsotable',
            'mmodsoudl', 'mmodsoudldata', 'mmodsouniquetag', 'mmPr', 'mmquery',
            'mmr', 'mnary', 'mnaryPr', 'mnoBreak', 'mnum', 'mobjDist', 'moMath',
            'moMathPara', 'moMathParaPr', 'mopEmu', 'mphant', 'mphantPr',
            'mplcHide', 'mpos', 'mr', 'mrad', 'mradPr', 'mrPr', 'msepChr',
            'mshow', 'mshp', 'msPre', 'msPrePr', 'msSub', 'msSubPr', 'msSubSup',
            'msSubSupPr', 'msSup', 'msSupPr', 'mstrikeBLTR', 'mstrikeH',
            'mstrikeTLBR', 'mstrikeV', 'msub', 'msubHide', 'msup', 'msupHide',
            'mtransp', 'mtype', 'mvertJc', 'mvfmf', 'mvfml', 'mvtof', 'mvtol',
            'mzeroAsc', 'mzeroDesc', 'mzeroWid', 'nesttableprops', 'nextfile',
            'nonesttables', 'objalias', 'objclass', 'objdata', 'object',
            'objname', 'objsect', 'objtime', 'oldcprops', 'oldpprops',
            'oldsprops', 'oldtprops', 'oleclsid', 'operator', 'panose',
            'password', 'passwordhash', 'pgp', 'pgptbl', 'picprop', 'pict',
            'pn', 'pnseclvl', 'pntext', 'pntxta', 'pntxtb', 'printim',
            'private', 'propname', 'protend', 'protstart', 'protusertbl', 'pxe',
            'result', 'revtbl', 'revtim', 'rsidtbl', 'rxe', 'shp', 'shpgrp',
            'shpinst', 'shppict', 'shprslt', 'shptxt', 'sn', 'sp', 'staticval',
            'stylesheet', 'subject', 'sv', 'svb', 'tc', 'template', 'themedata',
            'title', 'txe', 'ud', 'upr', 'userprops', 'wgrffmtfilter',
            'windowcaption', 'writereservation', 'writereservhash', 'xe',
            'xform', 'xmlattrname', 'xmlattrvalue', 'xmlclose', 'xmlname',
            'xmlnstbl', 'xmlopen'))
        # Translation of some special characters.
        specialchars = {
            u'par': u'\n',
            u'sect': u'\n\n',
            u'page': u'\n\n',
            u'line': u'\n',
            u'tab': u'\t',
            u'emdash': u'\u2014',
            u'endash': u'\u2013',
            u'emspace': u'\u2003',
            u'enspace': u'\u2002',
            u'qmspace': u'\u2005',
            u'bullet': u'\u2022',
            u'lquote': u'\u2018',
            u'rquote': u'\u2019',
            u'ldblquote': u'\u201C',
            u'rdblquote': u'\u201D'}
        charset_mapping = {
            # Thai encoding
            'fcharset222': u'cp874',
            'ansicpg874': u'cp874',
            # Central+East European encoding
            'fcharset238': u'cp1250',
            'ansicpg1250': u'cp1250',
            # Cyrillic encoding
            'fcharset204': u'cp1251',
            'ansicpg1251': u'cp1251',
            # West European encoding
            'fcharset0': u'cp1252',
            'ansicpg1252': u'cp1252',
            # Greek encoding
            'fcharset161': u'cp1253',
            'ansicpg1253': u'cp1253',
            # Turkish encoding
            'fcharset162': u'cp1254',
            'ansicpg1254': u'cp1254',
            # Hebrew encoding
            'fcharset177': u'cp1255',
            'ansicpg1255': u'cp1255',
            # Arabic encoding
            'fcharset178': u'cp1256',
            'ansicpg1256': u'cp1256',
            # Baltic encoding
            'fcharset186': u'cp1257',
            'ansicpg1257': u'cp1257',
            # Vietnamese encoding
            'fcharset163': u'cp1258',
            'ansicpg1258': u'cp1258'}
        charsets = charset_mapping.keys()
        # Character encoding is defined together with fonts.
        # font_table could contain eg '0': 'cp1252'
        font_table = {}
        stack = []
        # Whether this group (and all inside it) are "ignorable".
        ignorable = False
        # Whether we are inside the font table.
        inside_font_table = False
        current_font = ''
        # Number of ASCII characters to skip after an unicode character.
        ucskip = 1
        # Number of ASCII characters left to skip.
        curskip = 0
        # Output buffer.
        out = []
        for match in pattern.finditer(text):
            word, arg, hex, char, brace, tchar = match.groups()
            if brace:
                curskip = 0
                if brace == u'{':
                    # Push state
                    stack.append((ucskip, ignorable, inside_font_table))
                elif brace == u'}':
                    # Pop state
                    ucskip, ignorable, inside_font_table = stack.pop()
            # \x (not a letter)
            elif char:
                curskip = 0
                if char == '~':
                    if not ignorable:
                        out.append(u'\xA0')
                elif char in u'{}\\':
                    if not ignorable:
                        out.append(char)
                elif char == u'*':
                    ignorable = True
            # \foo
            elif word:
                curskip = 0
                if word in destinations:
                    ignorable = True
                elif word in specialchars:
                    out.append(specialchars[word])
                elif word == u'uc':
                    ucskip = int(arg)
                elif word == u'u':
                    c = int(arg)
                    if c < 0:
                        c += 0x10000
                    out.append(unichr(c))
                    curskip = ucskip
                elif word == 'fonttbl':
                    inside_font_table = True
                    ignorable = True
                elif word == 'f':
                    current_font = arg
                    if not inside_font_table:
                        encoding = font_table[arg]
                elif word in ('ansicpg', 'fcharset'):
                    if inside_font_table:
                        font_table[current_font] = charset_mapping[word + arg]
                    else:
                        encoding = charset_mapping[word + arg]
            # \'xx
            elif hex:
                if curskip > 0:
                    curskip -= 1
                elif not ignorable:
                    c = int(hex, 16)
                    out.append(chr(c).decode(encoding))
            elif tchar:
                if curskip > 0:
                    curskip -= 1
                elif not ignorable:
                    out.append(tchar)
        return ''.join(out)

