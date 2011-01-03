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
"""
The :mod:`lib` module contains all the library functionality for the bibles
plugin.
"""
import logging
import re

from openlp.core.lib import translate

log = logging.getLogger(__name__)

def get_reference_match(match_type):
    local_separator = unicode(translate('BiblesPlugin',
        ':;;\\s*[:vV]\\s*;;-;;\\s*-\\s*;;,;;\\s*,\\s*;;end',
        'Seperators for parsing references. There are 7 values separated each '
        'by two semicolons. Verse, range and list separators have each one '
        'display symbol which appears on slides and in the GUI and a regular '
        'expression for detecting this symbols.\n'
        'Please ask a developer to double check your translation or make '
        'yourself familar with regular experssions on: '
        'http://docs.python.org/library/re.html')
        ).split(u';;')
    separators = {
        u'sep_v_display': local_separator[0], u'sep_v': local_separator[1],
        u'sep_r_display': local_separator[2], u'sep_r': local_separator[3],
        u'sep_l_display': local_separator[4], u'sep_l': local_separator[5],
        u'sep_e': local_separator[6]}
    # verse range match: (<chapter>:)?<verse>(-((<chapter>:)?<verse>|end)?)?
    range_string = str(r'(?:(?P<from_chapter>[0-9]+)%(sep_v)s)?(?P<from_verse>'
        r'[0-9]+)(?P<range_to>%(sep_r)s(?:(?:(?P<to_chapter>[0-9]+)%(sep_v)s)?'
        r'(?P<to_verse>[0-9]+)|%(sep_e)s)?)?') % separators
    if match_type == u'range':
        return re.compile(r'^\s*' + range_string + r'\s*$', re.UNICODE)
    elif match_type == u'range_separator':
        return re.compile(separators[u'sep_l'])
    elif match_type == u'full':
        # full reference match: <book>(<range>(,|(?=$)))+
        return re.compile(str(r'^\s*(?!\s)(?P<book>[\d]*[^\d]+)(?<!\s)\s*'
            r'(?P<ranges>(?:' + range_string + r'(?:%(sep_l)s|(?=\s*$)))+)\s*$')
                % separators, re.UNICODE)
    else:
        return separators[match_type]

def parse_reference(reference):
    """
    This is the next generation über-awesome function that takes a person's
    typed in string and converts it to a reference list, a list of references to
    be queried from the Bible database files.

    This is a user manual like description, how the references are working.

    - Each reference starts with the book name. A chapter name is manditory.
        ``John 3`` refers to Gospel of John chapter 3
    - A reference range can be given after a range separator.
        ``John 3-5`` refers to John chapters 3 to 5
    - Single verses can be addressed after a verse separator
        ``John 3:16`` refers to John chapter 3 verse 16
        ``John 3:16-4:3`` refers to John chapter 3 verse 16 to chapter 4 verse 3
    - After a verse reference all further single values are treat as verse in
      the last selected chapter.
        ``John 3:16-18`` refers to John chapter 3 verses 16 to 18
    - After a list separator it is possible to refer to additional verses.  They
      are build analog to the first ones.  This way it is possible to define
      each number of verse references.  It is not possible to refer to verses in
      additional books.
        ``John 3:16,18`` refers to John chapter 3 verses 16 and 18
        ``John 3:16-18,20`` refers to John chapter 3 verses 16 to 18 and 20
        ``John 3:16-18,4:1`` refers to John chapter 3 verses 16 to 18 and
        chapter 3 verse 1
    - If there is a range separator without further verse declaration the last
      refered chapter is addressed until the end.

    ``range_string`` is a regular expression which matches for verse range
    declarations:

    1. ``(?:(?P<from_chapter>[0-9]+)%(sep_v)s)?'
        It starts with a optional chapter reference ``from_chapter`` followed by
        a verse separator.
    2. ``(?P<from_verse>[0-9]+)``
        The verse reference ``from_verse`` is manditory
    3.  ``(?P<range_to>%(sep_r)s(?:`` ... ``|%(sep_e)s)?)?``
        A ``range_to`` declaration is optional. It starts with a range separator
        and contains optional a chapter and verse declaration or a end
        separator.
    4.  ``(?:(?P<to_chapter>[0-9]+)%(sep_v)s)?``
        The ``to_chapter`` reference with separator is equivalent to group 1.
    5. ``(?P<to_verse>[0-9]+)``
        The ``to_verse`` reference is equivalent to group 2.

    The full reference is matched against get_reference_match(u'full').  This
    regular expression looks like this:

    1. ``^\s*(?!\s)(?P<book>[\d]*[^\d]+)(?<!\s)\s*``
        The ``book`` group starts with the first non-whitespace character.  There
        are optional leading digits followed by non-digits. The group ends
        before the whitspace in front of the next digit.
    2. ``(?P<ranges>(?:`` + range_string + ``(?:%(sep_l)s|(?=\s*$)))+)\s*$``
        The second group contains all ``ranges``.  This can be multiple
        declarations of a range_string separated by a list separator.

    The reference list is a list of tuples, with each tuple structured like
    this::

        (book, chapter, from_verse, to_verse)

    ``reference``
        The bible reference to parse.

    Returns None or a reference list.
    """
    log.debug(u'parse_reference("%s")', reference)
    match = get_reference_match(u'full').match(reference)
    if match:
        log.debug(u'Matched reference %s' % reference)
        book = match.group(u'book')
        bookname_dict = get_system_bookname_dict()
        if book.lower() in bookname_dict:
            book = bookname_dict[book.lower()]
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
                    ref_list.append((book, from_chapter, from_verse, -1))
                    for i in range(from_chapter + 1, to_chapter - 1):
                        ref_list.append((book, i, 1, -1))
                    ref_list.append((book, to_chapter, 1, to_verse))
                elif to_verse >= from_verse or to_verse == -1:
                    ref_list.append((book, from_chapter, from_verse, to_verse))
            elif from_verse:
                ref_list.append((book, from_chapter, from_verse, from_verse))
            else:
                ref_list.append((book, from_chapter, 1, -1))
        return ref_list
    else:
        log.debug(u'Invalid reference: %s' % reference)
        return None

def get_local_bookname_dict():
    raw_dict = get_raw_bookname_dict()
    local_bookname_dict = {}
    for key in raw_dict.keys():
        local_bookname_dict[key] = raw_dict[key][0]
    return local_bookname_dict

def get_system_bookname_dict():
    raw_dict = get_raw_bookname_dict()
    system_bookname_dict = {}
    for key in raw_dict.keys():
        for alias in raw_dict[key]:
            system_bookname_dict[alias.lower()] = key
    return system_bookname_dict

def get_raw_bookname_dict():
    raw_bookname_dict = {u'Genesis': translate('BiblesPlugin', 'Genesis;;Gen'),
        u'Exodus': translate('BiblesPlugin', 'Exodus;;Exod'),
        u'Leviticus': translate('BiblesPlugin', 'Leviticus;;Lev'),
        u'Numbers': translate('BiblesPlugin', 'Numbers;;Num'),
        u'Deuteronomy': translate('BiblesPlugin', 'Deuteronomy;;Deut'),
        u'Joshua': translate('BiblesPlugin', 'Joshua;;Josh'),
        u'Judges': translate('BiblesPlugin', 'Judges;;Judg'),
        u'Ruth': translate('BiblesPlugin', 'Ruth;;Ruth'),
        u'1 Samuel': translate('BiblesPlugin', '1 Samuel;;1Sam'),
        u'2 Samuel': translate('BiblesPlugin', '2 Samuel;;2Sam'),
        u'1 Kings': translate('BiblesPlugin', '1 Kings;;1Kgs'),
        u'2 Kings': translate('BiblesPlugin', '2 Kings;;2Kgs'),
        u'1 Chronicles': translate('BiblesPlugin', '1 Chronicles;;1Chr'),
        u'2 Chronicles': translate('BiblesPlugin', '2 Chronicles;;2Chr'),
        u'Ezra': translate('BiblesPlugin', 'Ezra;;Ezra'),
        u'Nehemiah': translate('BiblesPlugin', 'Nehemiah;;Neh'),
        u'Esther': translate('BiblesPlugin', 'Esther;;Esth'),
        u'Job': translate('BiblesPlugin', 'Job;;Job'),
        u'Psalms': translate('BiblesPlugin', 'Psalms;;Ps'),
        u'Proverbs': translate('BiblesPlugin', 'Proverbs;;Prov'),
        u'Ecclesiastes': translate('BiblesPlugin', 'Ecclesiastes;;Eccl'),
        u'Song of Songs': translate('BiblesPlugin', 'Song of Songs;;Song'),
        u'Isaiah': translate('BiblesPlugin', 'Isaiah;;Isa'),
        u'Jeremiah': translate('BiblesPlugin', 'Jeremiah;;Jer'),
        u'Lamentations': translate('BiblesPlugin', 'Lamentations;;Lam'),
        u'Ezekiel': translate('BiblesPlugin', 'Ezekiel;;Ezek'),
        u'Daniel': translate('BiblesPlugin', 'Daniel;;Dan'),
        u'Hosea': translate('BiblesPlugin', 'Hosea;;Hos'),
        u'Joel': translate('BiblesPlugin', 'Joel;;Joel'),
        u'Amos': translate('BiblesPlugin', 'Amos;;Amos'),
        u'Obad': translate('BiblesPlugin', 'Obad;;Obad'),
        u'Jonah': translate('BiblesPlugin', 'Jonah;;Jonah'),
        u'Micah': translate('BiblesPlugin', 'Micah;;Mic'),
        u'Naham': translate('BiblesPlugin', 'Naham;;Nah'),
        u'Habakkuk': translate('BiblesPlugin', 'Habakkuk;;Hab'),
        u'Zephaniah': translate('BiblesPlugin', 'Zephaniah;;Zeph'),
        u'Haggai': translate('BiblesPlugin', 'Haggai;;Hag'),
        u'Zechariah': translate('BiblesPlugin', 'Zechariah;;Zech'),
        u'Malachi': translate('BiblesPlugin', 'Malachi;;Mal'),
        u'Matthew': translate('BiblesPlugin', 'Matthew;;Matt'),
        u'Mark': translate('BiblesPlugin', 'Mark;;Mark'),
        u'Luke': translate('BiblesPlugin', 'Luke;;Luke'),
        u'John': translate('BiblesPlugin', 'John;;John'),
        u'Acts': translate('BiblesPlugin', 'Acts;;Acts'),
        u'Romans': translate('BiblesPlugin', 'Romans;;Rom'),
        u'1 Corinthians': translate('BiblesPlugin', '1 Corinthians;;1Cor'),
        u'2 Corinthians': translate('BiblesPlugin', '2 Corinthians;;2Cor'),
        u'Galatians': translate('BiblesPlugin', 'Galatians;;Gal'),
        u'Ephesians': translate('BiblesPlugin', 'Ephesians;;Eph'),
        u'Philippians': translate('BiblesPlugin', 'Philippians;;Phil'),
        u'Colossians': translate('BiblesPlugin', 'Colossians;;Col'),
        u'1 Thessalonians': translate('BiblesPlugin',
            '1 Thessalonians;;1Thess'),
        u'2 Thessalonians': translate('BiblesPlugin',
            '2 Thessalonians;;2Thess'),
        u'1 Timothy': translate('BiblesPlugin', '1 Timothy;;1Tim'),
        u'2 Timothy': translate('BiblesPlugin', '2 Timothy;;2Tim'),
        u'Titus': translate('BiblesPlugin', 'Titus;;Titus'),
        u'Philemon': translate('BiblesPlugin', 'Philemon;;Phlm'),
        u'Hebrews': translate('BiblesPlugin', 'Hebrews;;Heb'),
        u'James': translate('BiblesPlugin', 'James;;Jas'),
        u'1 Peter': translate('BiblesPlugin', '1 Peter;;1Pet'),
        u'2 Peter': translate('BiblesPlugin', '2 Peter;;2Pet'),
        u'1 John': translate('BiblesPlugin', '1 John;;1John'),
        u'2 John': translate('BiblesPlugin', '2 John;;2John'),
        u'3 John': translate('BiblesPlugin', '3 John;;3John'),
        u'Jude': translate('BiblesPlugin', 'Jude;;Jude'),
        u'Revelation': translate('BiblesPlugin', 'Revelation;;Rev')}
    for key in raw_bookname_dict.keys():
        raw_bookname_dict[key] = unicode(raw_bookname_dict[key]).split(u';;')
    return raw_bookname_dict


class SearchResults(object):
    """
    Encapsulate a set of search results.  This is Bible-type independent.
    """
    def __init__(self, book, chapter, verselist):
        """
        Create the search result object.

        ``book``
            The book of the Bible.

        ``chapter``
            The chapter of the book.

        ``verselist``
            The list of verses for this reading
        """
        self.book = book
        self.chapter = chapter
        self.verselist = verselist

    def has_verselist(self):
        """
        Returns whether or not the verse list contains verses.
        """
        return len(self.verselist) > 0


from manager import BibleManager
from biblestab import BiblesTab
from mediaitem import BibleMediaItem
