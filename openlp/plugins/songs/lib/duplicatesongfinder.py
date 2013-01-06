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
import logging
import difflib

from openlp.core.lib import translate
from openlp.plugins.songs.lib.db import Song
from openlp.plugins.songs.lib.ui import SongStrings

log = logging.getLogger(__name__)

class DuplicateSongFinder(object):
    """
    The :class:`DuplicateSongFinder` class provides functionality to search for
    and remove duplicate songs.
    """

    def __init__(self):
        self.minFragmentSize = 5
        self.minBlockSize = 70
        self.maxTypoSize = 3

    def songsProbablyEqual(self, song1, song2):
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
        return max(opcode[2]-opcode[1], opcode[4] - opcode[3])

    def __removeTypos(self, diff):
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
        length = 0
        for element in diff:
            if element[0] == "equal" and self.__opLength(element) >= self.minBlockSize:
                length += self.__opLength(element)
        return length

    def __lengthOfLongestEqualBlock(self, diff):
        length = 0
        for element in diff:
            if element[0] == "equal" and self.__opLength(element) > length:
                length = self.__opLength(element)
        return length
