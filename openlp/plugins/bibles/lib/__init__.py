# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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

log = logging.getLogger(__name__)

# English:
BIBLE_SEPARATORS = {u'sep_v': r'\s*:\s*', u'sep_r': r'\s*-\s*', u'sep_l': r','}
# German:
#BIBLE_SEPARATORS = {u'sep_v': r'\s*,\s*', u'sep_r': r'\s*-\s*', u'sep_l': r'\.'}

# RegEx for a verse span: (<chapter>:)?<verse>(-(<chapter>:)?<verse>?)?
BIBLE_RANGE_REGEX = str(r'(?:(?P<from_chapter>[0-9]+)%(sep_v)s)?'
    r'(?P<from_verse>[0-9]+)(?P<range_to>%(sep_r)s(?:(?:(?P<to_chapter>[0-9]+)'
    r'%(sep_v)s)?(?P<to_verse>[0-9]+))?)?' % BIBLE_SEPARATORS)

BIBLE_RANGE = re.compile(r'^\s*' + BIBLE_RANGE_REGEX + r'\s*$', re.UNICODE)

BIBLE_RANGE_SPLIT = re.compile(BIBLE_SEPARATORS[u'sep_l'])

# RegEx for a reference <book>(<range>(,|(?=$)))+
BIBLE_REFERENCE = re.compile(str(r'^\s*(?!\s)(?P<book>[\d]*[^\d]+)(?<!\s)\s*'
    r'(?P<ranges>(?:' + BIBLE_RANGE_REGEX + r'(?:%(sep_l)s|(?=\s*$)))+)\s*$') %
    BIBLE_SEPARATORS, re.UNICODE)

def parse_reference(reference):
    """
    This is the next generation über-awesome function that takes a person's
    typed in string and converts it to a reference list, a list of references to
    be queried from the Bible database files.

#####
    This is a user manual like description, how the references are working.

    - Each reference starts with the book name. A chapter name is manditory.
        ``John 3`` refers to Gospel of John chapter 3
    - A reference range can be given after a range seperator.
        ``John 3-5`` refers to John chapters 3 to 5
    - Single verses can be addressed after a verse seperator
        ``John 3:16`` refers to John chapter 3 verse 16
        ``John 3:16-4:3`` refers to John chapter 3 verse 16 to chapter 4 verse 3
    - After a verse reference all further single values are treat as verse in
      the last selected chapter.
        ``John 3:16-18`` refers to John chapter 3 verses 16 to 18
    - After a list separator it is possible to refer to additional verses. They
      are build analog to the first ones. This way it is possible to define each
      number of verse references. It is not possible to refer to verses in
      additional books.
        ``John 3:16,18`` refers to John chapter 3 verses 16 and 18
        ``John 3:16-18,20`` refers to John chapter 3 verses 16 to 18 to 20
        ``John 3:16-18,4:1`` refers to John chapter 3 verses 16 to 18 and
        chapter 3 verse 1
    - If there is a range separator without further verse declaration the last
      refered chapter is addressed until the end.
#####

    The ``BIBLE_RANGE`` regular expression produces match groups for verse range
    declarations:

    1. ``(?:(?P<from_chapter>[0-9]+)%(sep_v)s)?'
        It starts with a optional chapter reference ``from_chapter`` followed by
        a verse separator.
    2. ``(?P<from_verse>[0-9]+)``
        The verse reference ``from_verse`` is manditory
    3.  ``(?P<range_to>%(sep_r)s(?:`` ...  ``)?)?``
        A ``range_to`` declaration is optional. It starts with a range seperator
        and contains a optional chapter and verse declaration
    4.  ``(?:(?P<to_chapter>[0-9]+)%(sep_v)s)?``
        The ``to_chapter`` reference with seperator is equivalent to group 1.
    5. ``(?P<to_verse>[0-9]+)?)?``
        The ``to_verse`` reference is equivalent to group 2.

    The ``BIBLE_REFERENCE`` regular expression produces matched groups for the
    whole reference string:

    1. ``^\s*(?!\s)(?P<book>[\d]*[^\d]+)(?<!\s)\s*``
        The ``book`` group starts with the first non-whitespace character. There
        are optional leading digits followed by non-digits. The group ends
        before the whitspace in front of the next digit.
    2. ``(?P<ranges>(?:`` + BIBLE_RANGE_REGEX +
        ``(?:%(sep_l)s|(?=\s*$)))+)\s*$``
        The sechon group contains all ``ranges``. This can be multiple
        declarations of a BIBLE_RANGE separated by a list separator.

    ``BIBLE_SEPARATORS`` is a dict which defines the separator formats. It might
    be used to localize the bible references.

    The reference list is a list of tuples, with each tuple structured like
    this::

        (book, chapter, from_verse, to_verse)

    ``reference``
        The bible reference to parse.

    Returns None or a reference list.
    """
 
    log.debug('parse_reference("%s")', reference)
    match = BIBLE_REFERENCE.match(reference)
    if match:
        log.debug(u'Matched reference %s' % reference)
        book = match.group(u'book')
        ranges = BIBLE_RANGE_SPLIT.split(match.group(u'ranges'))
        ref_list = []
        chapter = 0
        for this_range in ranges:
            range_match = BIBLE_RANGE.match(this_range)
            from_chapter = range_match.group('from_chapter')
            from_verse = range_match.group('from_verse')
            has_range = range_match.group('range_to')
            to_chapter = range_match.group('to_chapter')
            to_verse = range_match.group('to_verse')
            if from_chapter:
                from_chapter = int(from_chapter)
            if from_verse:
                from_verse = int(from_verse)
            if to_chapter:
                to_chapter = int(to_chapter)
            if to_verse:
                to_verse = int(to_verse)
            # Fill chapters with reasonable values.
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
            # Append references to the list
            if has_range:
                if not from_verse:
                    from_verse = 1
                if not to_verse:
                    to_verse = -1
                if to_chapter > from_chapter:
                    ref_list.append((book, from_chapter, from_verse, -1))
                    for i in range(int(from_chapter) + 1, int(to_chapter) - 1):
                        ref_list.append((book, i, 1, -1))
                    ref_list.append((book, to_chapter, 1, to_verse))
                elif to_verse >= from_verse:
                    ref_list.append((book, from_chapter, from_verse, to_verse))
            elif from_verse:
                ref_list.append((book, from_chapter, from_verse, from_verse))
            else:
                ref_list.append((book, from_chapter, 1, -1))
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
