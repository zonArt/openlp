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

BIBLE_REFERENCE = re.compile(
    r'^([\w ]+?) *([0-9]+)'          # Initial book and chapter
    r'(?: *[:|v|V] *([0-9]+))?'      # Verse for first chapter
    r'(?: *- *([0-9]+|end$))?'       # Range for verses or chapters
    r'(?:(?:,([0-9]+))?'             # Second chapter
    r' *[,|:|v|V] *([0-9]+|end$)'    # More range for verses or chapters
    r'(?: *- *([0-9]+|end$))?)?$',   # End of second verse range
    re.UNICODE)

def check_end(match_group):
    """
    Check if a regular expression match group contains the text u'end' or
    should be converted to an int.

    ``match_group``
        The match group to check.
    """
    if match_group == u'end':
        return -1
    else:
        return int(match_group)

def parse_reference(reference):
    """
    This is the über-awesome function that takes a person's typed in string
    and converts it to a reference list, a list of references to be queried
    from the Bible database files.

    BIBLE_REFERENCE regular expression produces the following match groups:
    0     This is a special group consisting of the whole string that matched.
    1     [\w ]+            The book the reference is from.
    2     [0-9]+            The first (or only) chapter in the reference.
    3     None|[0-9]+       None or the only verse or the first verse in a
                            verse range or the start verse in a chapter range.
    4     None|[0-9]+|end   None or the end verse of the first verse range or
                            the end chapter of a chapter range.
    5     None|[0-9]+       None or the second chapter in multiple
                            (non-ranged) chapters.
    6     None|[0-9]+|end   None, the start of the second verse range or the
                            end of a chapter range.
    7     None|[0-9]+|end   None or the end of the second verse range.

    The reference list is a list of tuples, with each tuple structured like
    this::
        (book, chapter, start_verse, end_verse)

    ``reference``
        The bible reference to parse.

    Returns None or a reference list.
    """
    reference = reference.strip()
    log.debug('parse_reference("%s")', reference)
    unified_ref_list = []
    match = BIBLE_REFERENCE.match(reference)
    if match:
        log.debug(u'Matched reference %s' % reference)
        book = match.group(1)
        chapter = int(match.group(2))
        if match.group(7):
            # Two verse ranges
            vr1_start = int(match.group(3))
            vr1_end = int(match.group(4))
            unified_ref_list.append((book, chapter, vr1_start, vr1_end))
            vr2_start = int(match.group(6))
            vr2_end = check_end(match.group(7))
            if match.group(5):
                # One verse range per chapter
                chapter2 = int(match.group(5))
                unified_ref_list.append((book, chapter2, vr2_start, vr2_end))
            else:
                unified_ref_list.append((book, chapter, vr2_start, vr2_end))
        elif match.group(6):
            # Chapter range with verses
            if match.group(3):
                vr1_start = int(match.group(3))
            else:
                vr1_start = 1
            if match.group(2) == match.group(4):
                vr1_end = int(match.group(6))
                unified_ref_list.append((book, chapter, vr1_start, vr1_end))
            else:
                vr1_end = -1
                unified_ref_list.append((book, chapter, vr1_start, vr1_end))
                vr2_end = check_end(match.group(6))
                if int(match.group(4)) > chapter:
                    for x in range(chapter + 1, int(match.group(4)) + 1):
                        if x == int(match.group(4)):
                            unified_ref_list.append((book, x, 1, vr2_end))
                        else:
                            unified_ref_list.append((book, x, 1, -1))
        elif match.group(4):
            # Chapter range or chapter and verse range
            if match.group(3):
                vr1_start = int(match.group(3))
                vr1_end = check_end(match.group(4))
                if vr1_end == -1 or vr1_end > vr1_start:
                    unified_ref_list.append((book, chapter, vr1_start, vr1_end))
                else:
                    log.debug(u'Ambiguous reference: %s' % reference)
                    return None
            elif match.group(4) != u'end':
                for x in range(chapter, int(match.group(4)) + 1):
                    unified_ref_list.append((book, x, 1, -1))
            else:
                log.debug(u'Unsupported reference: %s' % reference)
                return None
        elif match.group(3):
            # Single chapter and verse
            verse = int(match.group(3))
            unified_ref_list.append((book, chapter, verse, verse))
        else:
            # Single chapter
            unified_ref_list.append((book, chapter, -1, -1))
    else:
        log.debug(u'Invalid reference: %s' % reference)
        return None
    return unified_ref_list


class SearchResults(object):
    """
    Encapsulate a set of search results. This is Bible-type independant.
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
