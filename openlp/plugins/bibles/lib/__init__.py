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
"""
The :mod:`lib` module contains all the library functionality for the bibles
plugin.
"""
import logging
import re

from openlp.core.lib import Settings, translate


log = logging.getLogger(__name__)

REFERENCE_MATCHES = {}
REFERENCE_SEPARATORS = {}

class LayoutStyle(object):
    """
    An enumeration for bible screen layout styles.
    """
    VersePerSlide = 0
    VersePerLine = 1
    Continuous = 2


class DisplayStyle(object):
    """
    An enumeration for bible text bracket display styles.
    """
    NoBrackets = 0
    Round = 1
    Curly = 2
    Square = 3


class LanguageSelection(object):
    """
    An enumeration for bible bookname language.
    And standard strings for use throughout the bibles plugin.
    """
    Bible = 0
    Application = 1
    English = 2


class BibleStrings(object):
    """
    Provide standard strings for objects to use.
    """
    __instance__ = None

    def __new__(cls):
        """
        Override the default object creation method to return a single instance.
        """
        if not cls.__instance__:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        """
        These strings should need a good reason to be retranslated elsewhere.
        """
        self.BookNames = {
            u'Gen': translate('BiblesPlugin', 'Genesis'),
            u'Exod': translate('BiblesPlugin', 'Exodus'),
            u'Lev': translate('BiblesPlugin', 'Leviticus'),
            u'Num': translate('BiblesPlugin', 'Numbers'),
            u'Deut': translate('BiblesPlugin', 'Deuteronomy'),
            u'Josh': translate('BiblesPlugin', 'Joshua'),
            u'Judg': translate('BiblesPlugin', 'Judges'),
            u'Ruth': translate('BiblesPlugin', 'Ruth'),
            u'1Sam': translate('BiblesPlugin', '1 Samuel'),
            u'2Sam': translate('BiblesPlugin', '2 Samuel'),
            u'1Kgs': translate('BiblesPlugin', '1 Kings'),
            u'2Kgs': translate('BiblesPlugin', '2 Kings'),
            u'1Chr': translate('BiblesPlugin', '1 Chronicles'),
            u'2Chr': translate('BiblesPlugin', '2 Chronicles'),
            u'Esra': translate('BiblesPlugin', 'Ezra'),
            u'Neh': translate('BiblesPlugin', 'Nehemiah'),
            u'Esth': translate('BiblesPlugin', 'Esther'),
            u'Job': translate('BiblesPlugin', 'Job'),
            u'Ps': translate('BiblesPlugin', 'Psalms'),
            u'Prov': translate('BiblesPlugin', 'Proverbs'),
            u'Eccl': translate('BiblesPlugin', 'Ecclesiastes'),
            u'Song': translate('BiblesPlugin', 'Song of Solomon'),
            u'Isa': translate('BiblesPlugin', 'Isaiah'),
            u'Jer': translate('BiblesPlugin', 'Jeremiah'),
            u'Lam': translate('BiblesPlugin', 'Lamentations'),
            u'Ezek': translate('BiblesPlugin', 'Ezekiel'),
            u'Dan': translate('BiblesPlugin', 'Daniel'),
            u'Hos': translate('BiblesPlugin', 'Hosea'),
            u'Joel': translate('BiblesPlugin', 'Joel'),
            u'Amos': translate('BiblesPlugin', 'Amos'),
            u'Obad': translate('BiblesPlugin', 'Obadiah'),
            u'Jonah': translate('BiblesPlugin', 'Jonah'),
            u'Mic': translate('BiblesPlugin', 'Micah'),
            u'Nah': translate('BiblesPlugin', 'Nahum'),
            u'Hab': translate('BiblesPlugin', 'Habakkuk'),
            u'Zeph': translate('BiblesPlugin', 'Zephaniah'),
            u'Hag': translate('BiblesPlugin', 'Haggai'),
            u'Zech': translate('BiblesPlugin', 'Zechariah'),
            u'Mal': translate('BiblesPlugin', 'Malachi'),
            u'Matt': translate('BiblesPlugin', 'Matthew'),
            u'Mark': translate('BiblesPlugin', 'Mark'),
            u'Luke': translate('BiblesPlugin', 'Luke'),
            u'John': translate('BiblesPlugin', 'John'),
            u'Acts': translate('BiblesPlugin', 'Acts'),
            u'Rom': translate('BiblesPlugin', 'Romans'),
            u'1Cor': translate('BiblesPlugin', '1 Corinthians'),
            u'2Cor': translate('BiblesPlugin', '2 Corinthians'),
            u'Gal': translate('BiblesPlugin', 'Galatians'),
            u'Eph': translate('BiblesPlugin', 'Ephesians'),
            u'Phil': translate('BiblesPlugin', 'Philippians'),
            u'Col': translate('BiblesPlugin', 'Colossians'),
            u'1Thess': translate('BiblesPlugin', '1 Thessalonians'),
            u'2Thess': translate('BiblesPlugin', '2 Thessalonians'),
            u'1Tim': translate('BiblesPlugin', '1 Timothy'),
            u'2Tim': translate('BiblesPlugin', '2 Timothy'),
            u'Titus': translate('BiblesPlugin', 'Titus'),
            u'Phlm': translate('BiblesPlugin', 'Philemon'),
            u'Heb': translate('BiblesPlugin', 'Hebrews'),
            u'Jas': translate('BiblesPlugin', 'James'),
            u'1Pet': translate('BiblesPlugin', '1 Peter'),
            u'2Pet': translate('BiblesPlugin', '2 Peter'),
            u'1John': translate('BiblesPlugin', '1 John'),
            u'2John': translate('BiblesPlugin', '2 John'),
            u'3John': translate('BiblesPlugin', '3 John'),
            u'Jude': translate('BiblesPlugin', 'Jude'),
            u'Rev': translate('BiblesPlugin', 'Revelation'),
            u'Jdt': translate('BiblesPlugin', 'Judith'),
            u'Wis': translate('BiblesPlugin', 'Wisdom'),
            u'Tob': translate('BiblesPlugin', 'Tobit'),
            u'Sir': translate('BiblesPlugin', 'Sirach'),
            u'Bar': translate('BiblesPlugin', 'Baruch'),
            u'1Macc': translate('BiblesPlugin', '1 Maccabees'),
            u'2Macc': translate('BiblesPlugin', '2 Maccabees'),
            u'3Macc': translate('BiblesPlugin', '3 Maccabees'),
            u'4Macc': translate('BiblesPlugin', '4 Maccabees'),
            u'AddDan': translate('BiblesPlugin', 'Rest of Daniel'),
            u'AddEsth': translate('BiblesPlugin', 'Rest of Esther'),
            u'PrMan': translate('BiblesPlugin', 'Prayer of Manasses'),
            u'LetJer': translate('BiblesPlugin', 'Letter of Jeremiah'),
            u'PrAza': translate('BiblesPlugin', 'Prayer of Azariah'),
            u'Sus': translate('BiblesPlugin', 'Susanna'),
            u'Bel': translate('BiblesPlugin', 'Bel'),
            u'1Esdr': translate('BiblesPlugin', '1 Esdras'),
            u'2Esdr': translate('BiblesPlugin', '2 Esdras')
        }


def update_reference_separators():
    """
    Updates separators and matches for parsing and formating scripture
    references.
    """
    default_separators = translate('BiblesPlugin',
        ':|v|V|verse|verses;;-|to;;,|and;;end Double-semicolon delimited separators for parsing references. '
        'Consult the developers for further information.').split(u';;')
    settings = Settings()
    settings.beginGroup(u'bibles')
    custom_separators = [
        settings.value(u'verse separator'),
        settings.value(u'range separator'),
        settings.value(u'list separator'),
        settings.value(u'end separator')]
    settings.endGroup()
    for index, role in enumerate([u'v', u'r', u'l', u'e']):
        if custom_separators[index].strip(u'|') == u'':
            source_string = default_separators[index].strip(u'|')
        else:
            source_string = custom_separators[index].strip(u'|')
        while u'||' in source_string:
            source_string = source_string.replace(u'||', u'|')
        if role != u'e':
            REFERENCE_SEPARATORS[u'sep_%s_display' % role] = source_string.split(u'|')[0]
        # escape reserved characters
        for character in u'\\.^$*+?{}[]()':
            source_string = source_string.replace(character, u'\\' + character)
        # add various unicode alternatives
        source_string = source_string.replace(u'-',
            u'(?:[-\u00AD\u2010\u2011\u2012\u2013\u2014\u2212\uFE63\uFF0D])')
        source_string = source_string.replace(u',', u'(?:[,\u201A])')
        REFERENCE_SEPARATORS[u'sep_%s' % role] = u'\s*(?:%s)\s*' % source_string
        REFERENCE_SEPARATORS[u'sep_%s_default' % role] = default_separators[index]
    # verse range match: (<chapter>:)?<verse>(-((<chapter>:)?<verse>|end)?)?
    range_regex = u'(?:(?P<from_chapter>[0-9]+)%(sep_v)s)?' \
        u'(?P<from_verse>[0-9]+)(?P<range_to>%(sep_r)s(?:(?:(?P<to_chapter>' \
        u'[0-9]+)%(sep_v)s)?(?P<to_verse>[0-9]+)|%(sep_e)s)?)?' % REFERENCE_SEPARATORS
    REFERENCE_MATCHES[u'range'] = re.compile(u'^\s*%s\s*$' % range_regex, re.UNICODE)
    REFERENCE_MATCHES[u'range_separator'] = re.compile(REFERENCE_SEPARATORS[u'sep_l'], re.UNICODE)
    # full reference match: <book>(<range>(,(?!$)|(?=$)))+
    REFERENCE_MATCHES[u'full'] = re.compile(u'^\s*(?!\s)(?P<book>[\d]*[^\d]+)(?<!\s)\s*'
        u'(?P<ranges>(?:%(range_regex)s(?:%(sep_l)s(?!\s*$)|(?=\s*$)))+)\s*$' \
        % dict(REFERENCE_SEPARATORS.items() + [(u'range_regex', range_regex)]), re.UNICODE)

def get_reference_separator(separator_type):
    """
    Provides separators for parsing and formatting scripture references.

    ``separator_type``
        The role and format of the separator.
    """
    if not REFERENCE_SEPARATORS:
        update_reference_separators()
    return REFERENCE_SEPARATORS[separator_type]

def get_reference_match(match_type):
    """
    Provides matches for parsing scripture references strings.

    ``match_type``
        The type of match is ``range_separator``, ``range`` or ``full``.
    """
    if not REFERENCE_MATCHES:
        update_reference_separators()
    return REFERENCE_MATCHES[match_type]

def parse_reference(reference, bible, language_selection, book_ref_id=False):
    """
    This is the next generation über-awesome function that takes a person's
    typed in string and converts it to a list of references to be queried from
    the Bible database files.

    ``reference``
        A string. The Bible reference to parse.

    ``bible``
        A object. The Bible database object.

    ``language_selection``
        An int. The language selection the user has choosen in settings
        section.

    ``book_ref_id``
        A string. The book reference id.

    Returns ``None`` or a reference list.

    The reference list is a list of tuples, with each tuple structured like
    this::

        (book, chapter, from_verse, to_verse)

    For example::

        [(u'John', 3, 16, 18), (u'John', 4, 1, 1)]

    **Reference string details:**

    Each reference starts with the book name and a chapter number. These are
    both mandatory.

    * ``John 3`` refers to Gospel of John chapter 3

    A reference range can be given after a range separator.

    * ``John 3-5`` refers to John chapters 3 to 5

    Single verses can be addressed after a verse separator.

    * ``John 3:16`` refers to John chapter 3 verse 16
    * ``John 3:16-4:3`` refers to John chapter 3 verse 16 to chapter 4 verse 3

    After a verse reference all further single values are treat as verse in
    the last selected chapter.

    * ``John 3:16-18`` refers to John chapter 3 verses 16 to 18

    After a list separator it is possible to refer to additional verses. They
    are build analog to the first ones. This way it is possible to define each
    number of verse references. It is not possible to refer to verses in
    additional books.

    * ``John 3:16,18`` refers to John chapter 3 verses 16 and 18
    * ``John 3:16-18,20`` refers to John chapter 3 verses 16 to 18 and 20
    * ``John 3:16-18,4:1`` refers to John chapter 3 verses 16 to 18 and
      chapter 4 verse 1

    If there is a range separator without further verse declaration the last
    refered chapter is addressed until the end.

    ``range_regex`` is a regular expression which matches for verse range
    declarations:

    ``(?:(?P<from_chapter>[0-9]+)%(sep_v)s)?``
        It starts with a optional chapter reference ``from_chapter`` followed by
        a verse separator.

    ``(?P<from_verse>[0-9]+)``
        The verse reference ``from_verse`` is manditory

    ``(?P<range_to>%(sep_r)s(?:`` ... ``|%(sep_e)s)?)?``
        A ``range_to`` declaration is optional. It starts with a range separator
        and contains optional a chapter and verse declaration or a end
        separator.

    ``(?:(?P<to_chapter>[0-9]+)%(sep_v)s)?``
        The ``to_chapter`` reference with separator is equivalent to group 1.

    ``(?P<to_verse>[0-9]+)``
        The ``to_verse`` reference is equivalent to group 2.

    The full reference is matched against get_reference_match(u'full'). This
    regular expression looks like this:

    ``^\s*(?!\s)(?P<book>[\d]*[^\d]+)(?<!\s)\s*``
        The ``book`` group starts with the first non-whitespace character. There
        are optional leading digits followed by non-digits. The group ends
        before the whitspace in front of the next digit.

    ``(?P<ranges>(?:%(range_regex)s(?:%(sep_l)s(?!\s*$)|(?=\s*$)))+)\s*$``
        The second group contains all ``ranges``. This can be multiple
        declarations of range_regex separated by a list separator.

    """
    log.debug(u'parse_reference("%s")', reference)
    match = get_reference_match(u'full').match(reference)
    if match:
        log.debug(u'Matched reference %s' % reference)
        book = match.group(u'book')
        if not book_ref_id:
            book_ref_id = bible.get_book_ref_id_by_localised_name(book, language_selection)
        elif not bible.get_book_by_book_ref_id(book_ref_id):
            book_ref_id = False
        ranges = match.group(u'ranges')
        range_list = get_reference_match(u'range_separator').split(ranges)
        ref_list = []
        chapter = None
        for this_range in range_list:
            range_match = get_reference_match(u'range').match(this_range)
            from_chapter = range_match.group(u'from_chapter')
            from_verse = range_match.group(u'from_verse')
            has_range = range_match.group(u'range_to')
            to_chapter = range_match.group(u'to_chapter')
            to_verse = range_match.group(u'to_verse')
            if from_chapter:
                from_chapter = int(from_chapter)
            if from_verse:
                from_verse = int(from_verse)
            if to_chapter:
                to_chapter = int(to_chapter)
            if to_verse:
                to_verse = int(to_verse)
            # Fill chapter fields with reasonable values.
            if from_chapter:
                chapter = from_chapter
            elif chapter:
                from_chapter = chapter
            else:
                from_chapter = from_verse
                from_verse = None
            if to_chapter:
                if to_chapter < from_chapter:
                    continue
                else:
                    chapter = to_chapter
            elif to_verse:
                if chapter:
                    to_chapter = chapter
                else:
                    to_chapter = to_verse
                    to_verse = None
            # Append references to the list
            if has_range:
                if not from_verse:
                    from_verse = 1
                if not to_verse:
                    to_verse = -1
                if to_chapter > from_chapter:
                    ref_list.append((book_ref_id, from_chapter, from_verse, -1))
                    for i in range(from_chapter + 1, to_chapter):
                        ref_list.append((book_ref_id, i, 1, -1))
                    ref_list.append((book_ref_id, to_chapter, 1, to_verse))
                elif to_verse >= from_verse or to_verse == -1:
                    ref_list.append((book_ref_id, from_chapter, from_verse, to_verse))
            elif from_verse:
                ref_list.append((book_ref_id, from_chapter, from_verse, from_verse))
            else:
                ref_list.append((book_ref_id, from_chapter, 1, -1))
        return ref_list
    else:
        log.debug(u'Invalid reference: %s' % reference)
        return None


class SearchResults(object):
    """
    Encapsulate a set of search results. This is Bible-type independent.
    """
    def __init__(self, book, chapter, verselist):
        """
        Create the search result object.

        ``book``
            The book of the Bible.

        ``chapter``
            The chapter of the book.

        ``verselist``
            The list of verses for this reading.

        """
        self.book = book
        self.chapter = chapter
        self.verselist = verselist

    def has_verselist(self):
        """
        Returns whether or not the verse list contains verses.
        """
        return len(self.verselist) > 0


from versereferencelist import VerseReferenceList
from manager import BibleManager
from biblestab import BiblesTab
from mediaitem import BibleMediaItem
