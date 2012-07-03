# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2012 Raoul Snyman                                        #
# Portions copyright (c) 2008-2012 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Edwin Lunando, Joshua Miller, Stevan Pettit,  #
# Andreas Preikschat, Mattias Põldaru, Christian Richter, Philip Ridout,      #
# Simon Scudder, Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon      #
# Tibble, Dave Warnock, Frode Woldsund                                        #
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
from openlp.core.utils import CONTROL_CHARS
from db import Author
from ui import SongStrings

WHITESPACE = re.compile(r'[\W_]+', re.UNICODE)
APOSTROPHE = re.compile(u'[\'`’ʻ′]', re.UNICODE)
RTF_STRIPPING_REGEX = re.compile(r'\{\\tx[^}]*\}')

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
        unicode(translate('SongsPlugin.VerseType', 'Verse')),
        unicode(translate('SongsPlugin.VerseType', 'Chorus')),
        unicode(translate('SongsPlugin.VerseType', 'Bridge')),
        unicode(translate('SongsPlugin.VerseType', 'Pre-Chorus')),
        unicode(translate('SongsPlugin.VerseType', 'Intro')),
        unicode(translate('SongsPlugin.VerseType', 'Ending')),
        unicode(translate('SongsPlugin.VerseType', 'Other'))]
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
                'for the correct character representation.\n'
                'Usually you are fine with the preselected choice.'),
            [pair[1] for pair in encodings], recommended_index, False)
    else:
        choice = QtGui.QInputDialog.getItem(None,
            translate('SongsPlugin', 'Character Encoding'),
            translate('SongsPlugin', 'Please choose the character encoding.\n'
                'The encoding is responsible for the correct character '
                'representation.'), [pair[1] for pair in encodings], 0, False)
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
    song.search_title = clean_string(song.title) + u'@' + \
        clean_string(song.alternate_title)
    # Only do this, if we the song is a 1.9.4 song (or older).
    if song.lyrics.find(u'<lyrics language="en">') != -1:
        # Remove the old "language" attribute from lyrics tag (prior to 1.9.5).
        # This is not very important, but this keeps the database clean. This
        # can be removed when everybody has cleaned his songs.
        song.lyrics = song.lyrics.replace(
            u'<lyrics language="en">', u'<lyrics>')
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
            verse_type = VerseType.Tags[VerseType.from_loose_input(
                verse[0][u'type'])]
            sxml.add_verse_to_lyrics(
                verse_type,
                verse[0][u'label'],
                verse[1],
                verse[0].get(u'lang')
            )
            compare_order.append((u'%s%s' % (verse_type, verse[0][u'label'])
                ).upper())
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
                new_order.append(
                    (u'%s%s' % (verse_type, verse_def[1:])).upper())
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
        author = manager.get_object_filtered(
            Author, Author.display_name == name)
        if author is None:
            author = Author.populate(
                display_name=name, last_name=u'', first_name=u'')
        song.authors.append(author)
    if song.copyright:
        song.copyright = CONTROL_CHARS.sub(u'', song.copyright).strip()

def strip_rtf(blob, encoding):
    depth = 0
    control = False
    clear_text = []
    control_word = []

    # workaround for \tx bug: remove one pair of curly braces
    # if \tx is encountered
    match = RTF_STRIPPING_REGEX.search(blob)
    if match:
        # start and end indices of match are curly braces - filter them out
        blob = ''.join([blob[i] for i in xrange(len(blob))
                        if i != match.start() and i !=match.end()])
    for c in blob:
        if control:
            # for delimiters, set control to False
            if c == '{':
                if control_word:
                    depth += 1
                control = False
            elif c == '}':
                if control_word:
                    depth -= 1
                control = False
            elif c == '\\':
                new_control = bool(control_word)
                control = False
            elif c.isspace():
                control = False
            else:
                control_word.append(c)
                if len(control_word) == 3 and control_word[0] == '\'':
                    control = False
            if not control:
                if not control_word:
                    if c == '{' or c == '}' or c == '\\':
                        clear_text.append(c)
                else:
                    control_str = ''.join(control_word)
                    if control_str == 'par' or control_str == 'line':
                        clear_text.append(u'\n')
                    elif control_str == 'tab':
                        clear_text.append(u'\t')
                    # Prefer the encoding specified by the RTF data to that
                    # specified by the Paradox table header
                    # West European encoding
                    elif control_str == 'fcharset0':
                        encoding = u'cp1252'
                    # Greek encoding
                    elif control_str == 'fcharset161':
                        encoding = u'cp1253'
                    # Turkish encoding
                    elif control_str == 'fcharset162':
                        encoding = u'cp1254'
                    # Vietnamese encoding
                    elif control_str == 'fcharset163':
                        encoding = u'cp1258'
                    # Hebrew encoding
                    elif control_str == 'fcharset177':
                        encoding = u'cp1255'
                    # Arabic encoding
                    elif control_str == 'fcharset178':
                        encoding = u'cp1256'
                    # Baltic encoding
                    elif control_str == 'fcharset186':
                        encoding = u'cp1257'
                    # Cyrillic encoding
                    elif control_str == 'fcharset204':
                        encoding = u'cp1251'
                    # Thai encoding
                    elif control_str == 'fcharset222':
                        encoding = u'cp874'
                    # Central+East European encoding
                    elif control_str == 'fcharset238':
                        encoding = u'cp1250'
                    elif control_str[0] == '\'':
                        s = chr(int(control_str[1:3], 16))
                        clear_text.append(s.decode(encoding))
                    del control_word[:]
            if c == '\\' and new_control:
                control = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        elif depth > 2:
            continue
        elif c == '\n' or c == '\r':
            continue
        elif c == '\\':
            control = True
        else:
            clear_text.append(c)
    return u''.join(clear_text)

from xml import OpenLyrics, SongXML
from songstab import SongsTab
from mediaitem import SongMediaItem
