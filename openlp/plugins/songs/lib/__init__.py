# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Jeffrey Smith, Maikel            #
# Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund                    #
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
from db import Author
from ui import SongStrings

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
    def translated_tag(verse_tag, strict=False):
        """
        Return the translated UPPERCASE tag for a given tag,
        used to show translated verse tags in UI

        ``verse_tag``
            The string to return a VerseType for

        ``strict``
            Determines if the default Other or None should be returned
        """
        if strict:
            not_found_value = None
        else:
            not_found_value = VerseType.TranslatedTags[VerseType.Other].upper()
        verse_tag = verse_tag[0].lower()
        for num, tag in enumerate(VerseType.Tags):
            if verse_tag == tag:
                return VerseType.TranslatedTags[num].upper()
        return not_found_value

    @staticmethod
    def translated_name(verse_tag, strict=False):
        """
        Return the translated name for a given tag

        ``verse_tag``
            The string to return a VerseType for

        ``strict``
            Determines if the default Other or None should be returned
        """
        if strict:
            not_found_value = None
        else:
            not_found_value = VerseType.TranslatedNames[VerseType.Other]
        verse_tag = verse_tag[0].lower()
        for num, tag in enumerate(VerseType.Tags):
            if verse_tag == tag:
                return VerseType.TranslatedNames[num]
        return not_found_value

    @staticmethod
    def from_tag(verse_tag, strict=False):
        """
        Return the VerseType for a given tag

        ``verse_tag``
            The string to return a VerseType for

        ``strict``
            Determines if the default Other or None should be returned
        """
        if strict:
            no_return_value = None
        else:
            no_return_value = VerseType.Other
        verse_tag = verse_tag[0].lower()
        for num, tag in enumerate(VerseType.Tags):
            if verse_tag == tag:
                return num
        return no_return_value

    @staticmethod
    def from_translated_tag(verse_tag):
        """
        Return the VerseType for a given tag

        ``verse_tag``
            The string to return a VerseType for
        """
        verse_tag = verse_tag[0].lower()
        for num, tag in enumerate(VerseType.TranslatedTags):
            if verse_tag == tag:
                return num

    @staticmethod
    def from_string(verse_name):
        """
        Return the VerseType for a given string

        ``verse_name``
            The string to return a VerseType for
        """
        verse_name = verse_name.lower()
        for num, name in enumerate(VerseType.Names):
            if verse_name == name.lower():
                return num

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
    def from_loose_input(verse_name):
        """
        Return the VerseType for a given string, Other if not found

        ``verse_name``
            The string to return a VerseType for
        """
        verse_index = None
        if len(verse_name) > 1:
            verse_index = VerseType.from_translated_string(verse_name)
            if verse_index is None:
                verse_index = VerseType.from_string(verse_name)
        if verse_index is None:
            verse_index = VerseType.from_translated_tag(verse_name)
        if verse_index is None:
            verse_index = VerseType.from_tag(verse_name)
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
    song.title = song.title.rstrip() if song.title else u''
    if song.alternate_title is None:
        song.alternate_title = u''
    song.alternate_title = song.alternate_title.strip()
    whitespace = re.compile(r'\W+', re.UNICODE)
    song.search_title = (whitespace.sub(u' ', song.title).strip() + u'@' +
        whitespace.sub(u' ', song.alternate_title).strip()).strip().lower()
    # Only do this, if we the song is a 1.9.4 song (or older).
    if song.lyrics.find(u'<lyrics language="en">') != -1:
        # Remove the old "language" attribute from lyrics tag (prior to 1.9.5).
        # This is not very important, but this keeps the database clean. This
        # can be removed when everybody has cleaned his songs.
        song.lyrics = song.lyrics.replace(
            u'<lyrics language="en">', u'<lyrics>')
        verses = SongXML().get_verses(song.lyrics)
        lyrics = u' '.join([whitespace.sub(u' ', verse[1]) for verse in verses])
        song.search_lyrics = lyrics.lower()
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
                verse[0][u'lang'] if verse[0].has_key(u'lang') else None
            )
            compare_order.append((u'%s%s' % (verse_type, verse[0][u'label'])
                ).upper())
            if verse[0][u'label'] == u'1':
                compare_order.append(verse_type.upper())
        song.lyrics = unicode(sxml.extract_xml(), u'utf-8')
        # Rebuild the verse order, to convert translated verse tags, which might
        # have been added prior to 1.9.5.
        if song.verse_order:
            order = song.verse_order.strip().split()
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
    # The song does not have any author, add one.
    if not song.authors:
        name = SongStrings.AuthorUnknown
        author = manager.get_object_filtered(
            Author, Author.display_name == name)
        if author is None:
            author = Author.populate(
                display_name=name, last_name=u'', first_name=u'')
        song.authors.append(author)

from xml import OpenLyrics, SongXML
from songstab import SongsTab
from mediaitem import SongMediaItem
