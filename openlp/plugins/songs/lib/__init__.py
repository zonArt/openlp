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

from PyQt4 import QtGui
from openlp.core.lib import translate

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
    Tags = [
        u'v',
        u'c',
        u'b',
        u'p',
        u'i',
        u'e',
        u'o']
    Names = [
        u'Verse',
        u'Chorus',
        u'Bridge',
        u'Pre-Chorus',
        u'Intro',
        u'Ending',
        u'Other']
    Translations = [
        unicode(translate('SongsPlugin.VerseType', 'Verse')),
        unicode(translate('SongsPlugin.VerseType', 'Chorus')),
        unicode(translate('SongsPlugin.VerseType', 'Bridge')),
        unicode(translate('SongsPlugin.VerseType', 'Pre-Chorus')),
        unicode(translate('SongsPlugin.VerseType', 'Intro')),
        unicode(translate('SongsPlugin.VerseType', 'Ending')),
        unicode(translate('SongsPlugin.VerseType', 'Other'))]

    @staticmethod
    def tag(verse_type):
        """
        Return a string for a given VerseType tag

        ``verse_type``
            The verse type to return a string for
        """
        if isinstance(verse_type, int):
            try:
                return VerseType.Tags[verse_type]
            except:
                return
        elif verse_type[0].lower() in VerseType.Tags:
            return verse_type[0].lower()

    @staticmethod
    def to_string(verse_type):
        """
        Return a string for a given VerseType Name

        ``verse_type``
            The type to return a string for
        """
        if isinstance(verse_type, int):
            try:
                return VerseType.Names[verse_type]
            except:
                return
        else:
            verse_type = verse_type[0].lower()
            for num, tag in enumerate(VerseType.Tags):
                if verse_type == tag:
                    return VerseType.Names[num]

    @staticmethod
    def to_translated_string(verse_type):
        """
        Return a string for a given VerseType Name

        ``verse_type``
            The type to return a string for
        """
        if isinstance(verse_type, int):
            try:
                return VerseType.Translations[verse_type]
            except:
                return
        else:
            verse_type = verse_type[0].lower()
            for num, tag in enumerate(VerseType.Tags):
                if verse_type == tag:
                    return VerseType.Translations[num]

    @staticmethod
    def from_tag(verse_type):
        """
        Return the VerseType for a given tag

        ``verse_type``
            The string to return a VerseType for
        """
        verse_type = verse_type[0].lower()
        for num, string in enumerate(VerseType.Tags):
            if verse_type == string:
                return num

    @staticmethod
    def from_translated_tag(verse_type):
        """
        Return the VerseType for a given tag

        ``verse_type``
            The string to return a VerseType for
        """
        verse_type = verse_type[0].lower()
        for num, string in enumerate(VerseType.Translations):
            if verse_type == string[0].lower():
                return num

    @staticmethod
    def from_string(verse_type):
        """
        Return the VerseType for a given string

        ``verse_type``
            The string to return a VerseType for
        """
        verse_type = verse_type.lower()
        for num, string in enumerate(VerseType.Names):
            if verse_type == string.lower():
                return num

    @staticmethod
    def from_translated_string(verse_type):
        """
        Return the VerseType for a given string

        ``verse_type``
            The string to return a VerseType for
        """
        verse_type = verse_type.lower()
        for num, translation in enumerate(VerseType.Translations):
            if verse_type == translation.lower():
                return num

    @staticmethod
    def from_loose_input(verse_type):
        """
        Return the VerseType for a given string, Other if not found

        ``verse_type``
            The string to return a VerseType for
        """
        verseIndex = None
        if len(verse_type) > 1:
            verseIndex = VerseType.from_translated_string(verse_type)
            if verseIndex is None:
                verseIndex = VerseType.from_string(verse_type)
        if verseIndex is None:
            verseIndex = VerseType.from_translated_tag(verse_type)
        elif verseIndex is None:
            verseIndex = VerseType.from_tag(verse_type)
        return verseIndex

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

from xml import OpenLyrics, SongXML
from songstab import SongsTab
from mediaitem import SongMediaItem
