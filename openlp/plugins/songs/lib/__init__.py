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
import re

from PyQt4 import QtGui

from openlp.core.lib import translate
from openlp.core.utils import CONTROL_CHARS, locale_direct_compare
from db import Author
from ui import SongStrings

WHITESPACE = re.compile(r'[\W_]+', re.UNICODE)
APOSTROPHE = re.compile(u'[\'`’ʻ′]', re.UNICODE)
PATTERN = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'"
    r"([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
# RTF control words which specify a "destination" to be ignored.
DESTINATIONS = frozenset((
    u'aftncn', u'aftnsep', u'aftnsepc', u'annotation', u'atnauthor',
    u'atndate', u'atnicn', u'atnid', u'atnparent', u'atnref', u'atntime',
    u'atrfend', u'atrfstart', u'author', u'background', u'bkmkend',
    u'bkmkstart', u'blipuid', u'buptim', u'category',
    u'colorschememapping', u'colortbl', u'comment', u'company', u'creatim',
    u'datafield', u'datastore', u'defchp', u'defpap', u'do', u'doccomm',
    u'docvar', u'dptxbxtext', u'ebcend', u'ebcstart', u'factoidname',
    u'falt', u'fchars', u'ffdeftext', u'ffentrymcr', u'ffexitmcr',
    u'ffformat', u'ffhelptext', u'ffl', u'ffname', u'ffstattext', u'field',
    u'file', u'filetbl', u'fldinst', u'fldrslt', u'fldtype', u'fname',
    u'fontemb', u'fontfile', u'footer', u'footerf', u'footerl', u'footerr',
    u'footnote', u'formfield', u'ftncn', u'ftnsep', u'ftnsepc', u'g',
    u'generator', u'gridtbl', u'header', u'headerf', u'headerl',
    u'headerr', u'hl', u'hlfr', u'hlinkbase', u'hlloc', u'hlsrc', u'hsv',
    u'htmltag', u'info', u'keycode', u'keywords', u'latentstyles',
    u'lchars', u'levelnumbers', u'leveltext', u'lfolevel', u'linkval',
    u'list', u'listlevel', u'listname', u'listoverride',
    u'listoverridetable', u'listpicture', u'liststylename', u'listtable',
    u'listtext', u'lsdlockedexcept', u'macc', u'maccPr', u'mailmerge',
    u'maln', u'malnScr', u'manager', u'margPr', u'mbar', u'mbarPr',
    u'mbaseJc', u'mbegChr', u'mborderBox', u'mborderBoxPr', u'mbox',
    u'mboxPr', u'mchr', u'mcount', u'mctrlPr', u'md', u'mdeg', u'mdegHide',
    u'mden', u'mdiff', u'mdPr', u'me', u'mendChr', u'meqArr', u'meqArrPr',
    u'mf', u'mfName', u'mfPr', u'mfunc', u'mfuncPr', u'mgroupChr',
    u'mgroupChrPr', u'mgrow', u'mhideBot', u'mhideLeft', u'mhideRight',
    u'mhideTop', u'mhtmltag', u'mlim', u'mlimloc', u'mlimlow',
    u'mlimlowPr', u'mlimupp', u'mlimuppPr', u'mm', u'mmaddfieldname',
    u'mmath', u'mmathPict', u'mmathPr', u'mmaxdist', u'mmc', u'mmcJc',
    u'mmconnectstr', u'mmconnectstrdata', u'mmcPr', u'mmcs',
    u'mmdatasource', u'mmheadersource', u'mmmailsubject', u'mmodso',
    u'mmodsofilter', u'mmodsofldmpdata', u'mmodsomappedname',
    u'mmodsoname', u'mmodsorecipdata', u'mmodsosort', u'mmodsosrc',
    u'mmodsotable', u'mmodsoudl', u'mmodsoudldata', u'mmodsouniquetag',
    u'mmPr', u'mmquery', u'mmr', u'mnary', u'mnaryPr', u'mnoBreak',
    u'mnum', u'mobjDist', u'moMath', u'moMathPara', u'moMathParaPr',
    u'mopEmu', u'mphant', u'mphantPr', u'mplcHide', u'mpos', u'mr',
    u'mrad', u'mradPr', u'mrPr', u'msepChr', u'mshow', u'mshp', u'msPre',
    u'msPrePr', u'msSub', u'msSubPr', u'msSubSup', u'msSubSupPr', u'msSup',
    u'msSupPr', u'mstrikeBLTR', u'mstrikeH', u'mstrikeTLBR', u'mstrikeV',
    u'msub', u'msubHide', u'msup', u'msupHide', u'mtransp', u'mtype',
    u'mvertJc', u'mvfmf', u'mvfml', u'mvtof', u'mvtol', u'mzeroAsc',
    u'mzFrodesc', u'mzeroWid', u'nesttableprops', u'nextfile',
    u'nonesttables', u'objalias', u'objclass', u'objdata', u'object',
    u'objname', u'objsect', u'objtime', u'oldcprops', u'oldpprops',
    u'oldsprops', u'oldtprops', u'oleclsid', u'operator', u'panose',
    u'password', u'passwordhash', u'pgp', u'pgptbl', u'picprop', u'pict',
    u'pn', u'pnseclvl', u'pntext', u'pntxta', u'pntxtb', u'printim',
    u'private', u'propname', u'protend', u'protstart', u'protusertbl',
    u'pxe', u'result', u'revtbl', u'revtim', u'rsidtbl', u'rxe', u'shp',
    u'shpgrp', u'shpinst', u'shppict', u'shprslt', u'shptxt', u'sn', u'sp',
    u'staticval', u'stylesheet', u'subject', u'sv', u'svb', u'tc',
    u'template', u'themedata', u'title', u'txe', u'ud', u'upr',
    u'userprops', u'wgrffmtfilter', u'windowcaption', u'writereservation',
    u'writereservhash', u'xe', u'xform', u'xmlattrname', u'xmlattrvalue',
    u'xmlclose', u'xmlname', u'xmlnstbl', u'xmlopen'))
# Translation of some special characters.
SPECIAL_CHARS = {
    u'par': u'\n',
    u'sect': u'\n\n',
    # Required page and column break.
    # Would be good if we could split verse into subverses here.
    u'page': u'\n\n',
    u'column': u'\n\n',
    # Soft breaks.
    u'softpage': u'[---]',
    u'softcol': u'[---]',
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
    u'rdblquote': u'\u201D',
    u'ltrmark': u'\u200E',
    u'rtlmark': u'\u200F',
    u'zwj': u'\u200D',
    u'zwnj': u'\u200C'}
CHARSET_MAPPING = {
    u'fcharset0': u'cp1252',
    u'fcharset161': u'cp1253',
    u'fcharset162': u'cp1254',
    u'fcharset163': u'cp1258',
    u'fcharset177': u'cp1255',
    u'fcharset178': u'cp1256',
    u'fcharset186': u'cp1257',
    u'fcharset204': u'cp1251',
    u'fcharset222': u'cp874',
    u'fcharset238': u'cp1250'}


class VerseType(object):
    """
    VerseType provides an enumeration for the tags that may be associated
    with verses in songs.
    """
    Verse = 0
    Chorus = 1
    Bridge = 2
    PreChorus = 3
    Intro = 4
    Ending = 5
    Other = 6

    Names = [
        u'Verse',
        u'Chorus',
        u'Bridge',
        u'Pre-Chorus',
        u'Intro',
        u'Ending',
        u'Other']
    Tags = [name[0].lower() for name in Names]

    TranslatedNames = [
        translate('SongsPlugin.VerseType', 'Verse'),
        translate('SongsPlugin.VerseType', 'Chorus'),
        translate('SongsPlugin.VerseType', 'Bridge'),
        translate('SongsPlugin.VerseType', 'Pre-Chorus'),
        translate('SongsPlugin.VerseType', 'Intro'),
        translate('SongsPlugin.VerseType', 'Ending'),
        translate('SongsPlugin.VerseType', 'Other')]
    TranslatedTags = [name[0].lower() for name in TranslatedNames]

    @staticmethod
    def translated_tag(verse_tag, default=Other):
        """
        Return the translated UPPERCASE tag for a given tag,
        used to show translated verse tags in UI

        ``verse_tag``
            The string to return a VerseType for

        ``default``
            Default return value if no matching tag is found
        """
        verse_tag = verse_tag[0].lower()
        for num, tag in enumerate(VerseType.Tags):
            if verse_tag == tag:
                return VerseType.TranslatedTags[num].upper()
        if default in VerseType.TranslatedTags:
            return VerseType.TranslatedTags[default].upper()

    @staticmethod
    def translated_name(verse_tag, default=Other):
        """
        Return the translated name for a given tag

        ``verse_tag``
            The string to return a VerseType for

        ``default``
            Default return value if no matching tag is found
        """
        verse_tag = verse_tag[0].lower()
        for num, tag in enumerate(VerseType.Tags):
            if verse_tag == tag:
                return VerseType.TranslatedNames[num]
        if default in VerseType.TranslatedNames:
            return VerseType.TranslatedNames[default]

    @staticmethod
    def from_tag(verse_tag, default=Other):
        """
        Return the VerseType for a given tag

        ``verse_tag``
            The string to return a VerseType for

        ``default``
            Default return value if no matching tag is found
        """
        verse_tag = verse_tag[0].lower()
        for num, tag in enumerate(VerseType.Tags):
            if verse_tag == tag:
                return num
        return default

    @staticmethod
    def from_translated_tag(verse_tag, default=Other):
        """
        Return the VerseType for a given tag

        ``verse_tag``
            The string to return a VerseType for

        ``default``
            Default return value if no matching tag is found
        """
        verse_tag = verse_tag[0].lower()
        for num, tag in enumerate(VerseType.TranslatedTags):
            if verse_tag == tag:
                return num
        return default

    @staticmethod
    def from_string(verse_name, default=Other):
        """
        Return the VerseType for a given string

        ``verse_name``
            The string to return a VerseType for

        ``default``
            Default return value if no matching tag is found
        """
        verse_name = verse_name.lower()
        for num, name in enumerate(VerseType.Names):
            if verse_name == name.lower():
                return num
        return default

    @staticmethod
    def from_translated_string(verse_name):
        """
        Return the VerseType for a given string

        ``verse_name``
            The string to return a VerseType for
        """
        verse_name = verse_name.lower()
        for num, translation in enumerate(VerseType.TranslatedNames):
            if verse_name == translation.lower():
                return num

    @staticmethod
    def from_loose_input(verse_name, default=Other):
        """
        Return the VerseType for a given string

        ``verse_name``
            The string to return a VerseType for

        ``default``
            Default return value if no matching tag is found
        """
        if len(verse_name) > 1:
            verse_index = VerseType.from_translated_string(verse_name)
            if verse_index is None:
                verse_index = VerseType.from_string(verse_name, default)
        elif len(verse_name) == 1:
            verse_index = VerseType.from_translated_tag(verse_name, None)
            if verse_index is None:
                verse_index = VerseType.from_tag(verse_name, default)
        else:
            return default
        return verse_index


def retrieve_windows_encoding(recommendation=None):
    """
    Determines which encoding to use on an information source. The process uses
    both automated detection, which is passed to this method as a
    recommendation, and user confirmation to return an encoding.

    ``recommendation``
        A recommended encoding discovered programmatically for the user to
        confirm.
    """
    # map chardet result to compatible windows standard code page
    codepage_mapping = {'IBM866': u'cp866', 'TIS-620': u'cp874',
        'SHIFT_JIS': u'cp932', 'GB2312': u'cp936', 'HZ-GB-2312': u'cp936',
        'EUC-KR': u'cp949', 'Big5': u'cp950', 'ISO-8859-2': u'cp1250',
        'windows-1250': u'cp1250', 'windows-1251': u'cp1251',
        'windows-1252': u'cp1252', 'ISO-8859-7': u'cp1253',
        'windows-1253': u'cp1253', 'ISO-8859-8': u'cp1255',
        'windows-1255': u'cp1255'}
    if recommendation in codepage_mapping:
        recommendation = codepage_mapping[recommendation]

    # Show dialog for encoding selection
    encodings = [(u'cp1256', translate('SongsPlugin', 'Arabic (CP-1256)')),
        (u'cp1257', translate('SongsPlugin', 'Baltic (CP-1257)')),
        (u'cp1250', translate('SongsPlugin', 'Central European (CP-1250)')),
        (u'cp1251', translate('SongsPlugin', 'Cyrillic (CP-1251)')),
        (u'cp1253', translate('SongsPlugin', 'Greek (CP-1253)')),
        (u'cp1255', translate('SongsPlugin', 'Hebrew (CP-1255)')),
        (u'cp932', translate('SongsPlugin', 'Japanese (CP-932)')),
        (u'cp949', translate('SongsPlugin', 'Korean (CP-949)')),
        (u'cp936', translate('SongsPlugin', 'Simplified Chinese (CP-936)')),
        (u'cp874', translate('SongsPlugin', 'Thai (CP-874)')),
        (u'cp950', translate('SongsPlugin', 'Traditional Chinese (CP-950)')),
        (u'cp1254', translate('SongsPlugin', 'Turkish (CP-1254)')),
        (u'cp1258', translate('SongsPlugin', 'Vietnam (CP-1258)')),
        (u'cp1252', translate('SongsPlugin', 'Western European (CP-1252)'))]
    recommended_index = -1
    if recommendation:
        for index in range(len(encodings)):
            if recommendation == encodings[index][0]:
                recommended_index = index
                break
    if recommended_index > 0:
        choice = QtGui.QInputDialog.getItem(None,
            translate('SongsPlugin', 'Character Encoding'),
            translate('SongsPlugin', 'The codepage setting is responsible\n'
                'for the correct character representation.\nUsually you are fine with the preselected choice.'),
            [pair[1] for pair in encodings], recommended_index, False)
    else:
        choice = QtGui.QInputDialog.getItem(None,
            translate('SongsPlugin', 'Character Encoding'),
            translate('SongsPlugin', 'Please choose the character encoding.\n'
                'The encoding is responsible for the correct character representation.'),
                [pair[1] for pair in encodings], 0, False)
    if not choice[1]:
        return None
    return filter(lambda item: item[1] == choice[0], encodings)[0][0]


def clean_string(string):
    """
    Strips punctuation from the passed string to assist searching
    """
    return WHITESPACE.sub(u' ', APOSTROPHE.sub(u'', string)).lower()


def clean_title(title):
    """
    Cleans the song title by removing Unicode control chars groups C0 & C1,
    as well as any trailing spaces
    """
    return CONTROL_CHARS.sub(u'', title).rstrip()


def clean_song(manager, song):
    """
    Cleans the search title, rebuilds the search lyrics, adds a default author
    if the song does not have one and other clean ups. This should always
    called when a new song is added or changed.

    ``manager``
        The song's manager.

    ``song``
        The song object.
    """
    if isinstance(song.title, buffer):
        song.title = unicode(song.title)
    if isinstance(song.alternate_title, buffer):
        song.alternate_title = unicode(song.alternate_title)
    if isinstance(song.lyrics, buffer):
        song.lyrics = unicode(song.lyrics)
    if song.title:
        song.title = clean_title(song.title)
    else:
        song.title = u''
    if song.alternate_title:
        song.alternate_title = clean_title(song.alternate_title)
    else:
        song.alternate_title = u''
    song.search_title = clean_string(song.title) + u'@' + clean_string(song.alternate_title)
    # Only do this, if we the song is a 1.9.4 song (or older).
    if song.lyrics.find(u'<lyrics language="en">') != -1:
        # Remove the old "language" attribute from lyrics tag (prior to 1.9.5).
        # This is not very important, but this keeps the database clean. This
        # can be removed when everybody has cleaned his songs.
        song.lyrics = song.lyrics.replace(u'<lyrics language="en">', u'<lyrics>')
        verses = SongXML().get_verses(song.lyrics)
        song.search_lyrics = u' '.join([clean_string(verse[1])
            for verse in verses])
        # We need a new and clean SongXML instance.
        sxml = SongXML()
        # Rebuild the song's verses, to remove any wrong verse names (for
        # example translated ones), which might have been added prior to 1.9.5.
        # List for later comparison.
        compare_order = []
        for verse in verses:
            verse_type = VerseType.Tags[VerseType.from_loose_input(verse[0][u'type'])]
            sxml.add_verse_to_lyrics(
                verse_type,
                verse[0][u'label'],
                verse[1],
                verse[0].get(u'lang')
            )
            compare_order.append((u'%s%s' % (verse_type, verse[0][u'label'])).upper())
            if verse[0][u'label'] == u'1':
                compare_order.append(verse_type.upper())
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        # Rebuild the verse order, to convert translated verse tags, which might
        # have been added prior to 1.9.5.
        if song.verse_order:
            order = CONTROL_CHARS.sub(u'', song.verse_order).strip().split()
        else:
            order = []
        new_order = []
        for verse_def in order:
            verse_type = VerseType.Tags[
                VerseType.from_loose_input(verse_def[0])]
            if len(verse_def) > 1:
                new_order.append((u'%s%s' % (verse_type, verse_def[1:])).upper())
            else:
                new_order.append(verse_type.upper())
        song.verse_order = u' '.join(new_order)
        # Check if the verse order contains tags for verses which do not exist.
        for order in new_order:
            if order not in compare_order:
                song.verse_order = u''
                break
    else:
        verses = SongXML().get_verses(song.lyrics)
        song.search_lyrics = u' '.join([clean_string(verse[1])
            for verse in verses])

    # The song does not have any author, add one.
    if not song.authors:
        name = SongStrings.AuthorUnknown
        author = manager.get_object_filtered(Author, Author.display_name == name)
        if author is None:
            author = Author.populate(display_name=name, last_name=u'', first_name=u'')
        song.authors.append(author)
    if song.copyright:
        song.copyright = CONTROL_CHARS.sub(u'', song.copyright).strip()


def get_encoding(font, font_table, default_encoding, failed=False):
    """
    Finds an encoding to use. Asks user, if necessary.

    ``font``
    The number of currently active font.

    ``font_table``
    Dictionary of fonts and respective encodings.

    ``default_encoding``
    The default encoding to use when font_table is empty or no font is used.

    ``failed``
    A boolean indicating whether the previous encoding didn't work.
    """
    encoding = None
    if font in font_table:
        encoding = font_table[font]
    if not encoding and default_encoding:
        encoding = default_encoding
    if not encoding or failed:
        encoding = retrieve_windows_encoding()
        default_encoding = encoding
    font_table[font] = encoding
    return encoding, default_encoding


def strip_rtf(text, default_encoding=None):
    """
    This function strips RTF control structures and returns an unicode string.

    Thanks to Markus Jarderot (MizardX) for this code, used by permission.
    http://stackoverflow.com/questions/188545

    ``text``
    RTF-encoded text, a string.

    ``default_encoding``
    Default encoding to use when no encoding is specified.
    """
    # Current font is the font tag we last met.
    font = u''
    # Character encoding is defined inside fonttable.
    # font_table could contain eg u'0': u'cp1252'
    font_table = {u'': u''}
    # Stack of things to keep track of when entering/leaving groups.
    stack = []
    # Whether this group (and all inside it) are "ignorable".
    ignorable = False
    # Number of ASCII characters to skip after an unicode character.
    ucskip = 1
    # Number of ASCII characters left to skip.
    curskip = 0
    # Output buffer.
    out = []
    for match in PATTERN.finditer(text):
        word, arg, hex, char, brace, tchar = match.groups()
        if brace:
            curskip = 0
            if brace == u'{':
                # Push state
                stack.append((ucskip, ignorable, font))
            elif brace == u'}':
                # Pop state
                ucskip, ignorable, font = stack.pop()
        # \x (not a letter)
        elif char:
            curskip = 0
            if char == u'~' and not ignorable:
                out.append(u'\xA0')
            elif char in u'{}\\' and not ignorable:
                out.append(char)
            elif char == u'-' and not ignorable:
                out.append(u'\u00AD')
            elif char == u'_' and not ignorable:
                out.append(u'\u2011')
            elif char == u'*':
                ignorable = True
        # \command
        elif word:
            curskip = 0
            if word in DESTINATIONS:
                ignorable = True
            elif word in SPECIAL_CHARS:
                out.append(SPECIAL_CHARS[word])
            elif word == u'uc':
                ucskip = int(arg)
            elif word == u' ':
                c = int(arg)
                if c < 0:
                    c += 0x10000
                out.append(unichr(c))
                curskip = ucskip
            elif word == u'fonttbl':
                ignorable = True
            elif word == u'f':
                font = arg
            elif word == u'ansicpg':
                font_table[font] = 'cp' + arg
            elif word == u'fcharset' and font not in font_table and word + arg in CHARSET_MAPPING:
                # \ansicpg overrides \fcharset, if present.
                font_table[font] = CHARSET_MAPPING[word + arg]
        # \'xx
        elif hex:
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                charcode = int(hex, 16)
                failed = False
                while True:
                    try:
                        encoding, default_encoding = get_encoding(font, font_table, default_encoding, failed=failed)
                        if not encoding:
                            return None
                        out.append(chr(charcode).decode(encoding))
                    except UnicodeDecodeError:
                        failed = True
                    else:
                        break
        elif tchar:
            if curskip > 0:
                curskip -= 1
            elif not ignorable:
                out.append(tchar)
    text = u''.join(out)
    return text, default_encoding


def natcmp(a, b):
    """
    Natural string comparison which mimics the behaviour of Python's internal
    cmp function.
    """
    if len(a) <= len(b):
        for i, key in enumerate(a):
            if isinstance(key, int) and isinstance(b[i], int):
                result = cmp(key, b[i])
            elif isinstance(key, int) and not isinstance(b[i], int):
                result = locale_direct_compare(str(key), b[i])
            elif not isinstance(key, int) and isinstance(b[i], int):
                result = locale_direct_compare(key, str(b[i]))
            else:
                result = locale_direct_compare(key, b[i])
            if result != 0:
                return result
        if len(a) == len(b):
            return 0
        else:
            return -1
    else:
        for i, key in enumerate(b):
            if isinstance(a[i], int) and isinstance(key, int):
                result = cmp(a[i], key)
            elif isinstance(a[i], int) and not isinstance(key, int):
                result = locale_direct_compare(str(a[i]), key)
            elif not isinstance(a[i], int) and isinstance(key, int):
                result = locale_direct_compare(a[i], str(key))
            else:
                result = locale_direct_compare(a[i], key)
            if result != 0:
                return result
        return 1

from xml import OpenLyrics, SongXML
from songstab import SongsTab
from mediaitem import SongMediaItem
