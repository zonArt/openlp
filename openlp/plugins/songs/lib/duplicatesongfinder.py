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
import difflib

from openlp.plugins.songs.lib.db import Song

class DuplicateSongFinder(object):
    """
    The :class:`DuplicateSongFinder` class provides functionality to search for
    duplicate songs.

    The algorithm is based on the diff algorithm.
    First a diffset is calculated for two songs.
    To compensate for typos all differences that are smaller than a
    limit (<maxTypoSize) and are surrounded by larger equal blocks
    (>minFragmentSize) are removed and the surrounding equal parts are merged.
    Finally two conditions can qualify a song tuple to be a duplicate:
    1. There is a block of equal content that is at least minBlockSize large.
       This condition should hit for all larger songs that have a long enough
       equal part. Even if only one verse is equal this condition should still hit.
    2. Two thirds of the smaller song is contained in the larger song.
       This condition should hit if one of the two songs (or both) is small (smaller
       than the minBlockSize), but most of the song is contained in the other song.
    """

    def __init__(self):
        self.minFragmentSize = 5
        self.minBlockSize = 70
        self.maxTypoSize = 3

    def songsProbablyEqual(self, song1, song2):
        """
        Calculate and return whether two songs are probably equal.

        ``song1``
            The first song to compare.

        ``song2``
            The second song to compare.
        """
        if len(song1.search_lyrics) < len(song2.search_lyrics):
            small = song1.search_lyrics
            large = song2.search_lyrics
        else:
            small = song2.search_lyrics
            large = song1.search_lyrics
        differ = difflib.SequenceMatcher(a=small, b=large)
        diff_tuples = differ.get_opcodes()
        diff_no_typos = self.__removeTypos(diff_tuples)
        #print(diff_no_typos)
        if self.__lengthOfEqualBlocks(diff_no_typos) >= self.minBlockSize or \
                self.__lengthOfLongestEqualBlock(diff_no_typos) > len(small)*2/3:
                    return True
        else:
            return False

    def __opLength(self, opcode):
        """
        Return the length of a given difference.

        ``opcode``
            The difference.
        """
        return max(opcode[2]-opcode[1], opcode[4] - opcode[3])

    def __removeTypos(self, diff):
        """
        Remove typos from a diff set. A typo is a small difference (<maxTypoSize)
        surrounded by larger equal passages (>minFragmentSize).

        ``diff``
            The diff set to remove the typos from.
        """
        #remove typo at beginning of string
        if len(diff) >= 2:
            if diff[0][0] != "equal" and self.__opLength(diff[0]) <= self.maxTypoSize and \
                    self.__opLength(diff[1]) >= self.minFragmentSize:
                        del diff[0]
        #remove typos in the middle of string
        if len(diff) >= 3:
            for index in range(len(diff)-3, -1, -1):
                if self.__opLength(diff[index]) >= self.minFragmentSize and \
                    diff[index+1][0] != "equal" and self.__opLength(diff[index+1]) <= self.maxTypoSize and \
                        self.__opLength(diff[index+2]) >= self.minFragmentSize:
                            del diff[index+1]
        #remove typo at the end of string
        if len(diff) >= 2:
            if self.__opLength(diff[-2]) >= self.minFragmentSize and \
                diff[-1][0] != "equal" and self.__opLength(diff[-1]) <= self.maxTypoSize:
                        del diff[-1]

        #merge fragments
        for index in range(len(diff)-2, -1, -1):
            if diff[index][0] == "equal" and self.__opLength(diff[index]) >= self.minFragmentSize and \
                diff[index+1][0] == "equal" and self.__opLength(diff[index+1]) >= self.minFragmentSize:
                        diff[index] = ("equal", diff[index][1], diff[index+1][2], diff[index][3],
                            diff[index+1][4])
                        del diff[index+1]

        return diff

    def __lengthOfEqualBlocks(self, diff):
        """
        Return the total length of all equal blocks in a diff set.
        Blocks smaller than minBlockSize are not counted.

        ``diff``
            The diff set to return the length for.
        """
        length = 0
        for element in diff:
            if element[0] == "equal" and self.__opLength(element) >= self.minBlockSize:
                length += self.__opLength(element)
        return length

    def __lengthOfLongestEqualBlock(self, diff):
        """
        Return the length of the largest equal block in a diff set.

        ``diff``
            The diff set to return the length for.
        """
        length = 0
        for element in diff:
            if element[0] == "equal" and self.__opLength(element) > length:
                length = self.__opLength(element)
        return length

