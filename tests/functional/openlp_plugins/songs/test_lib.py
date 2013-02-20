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

from unittest import TestCase

from mock import MagicMock

from openlp.plugins.songs.lib.songcompare import songs_probably_equal, _remove_typos, _op_length, \
    _length_of_equal_blocks, _length_of_longest_equal_block

class TestLib(TestCase):
    def setUp(self):
        """
        Mock up two songs and provide a set of lyrics for the songs_probably_equal tests.
        """
        self.full_lyrics =u'''amazing grace how sweet the sound that saved a wretch like me i once was lost but now am
            found was blind but now i see  twas grace that taught my heart to fear and grace my fears relieved how
            precious did that grace appear the hour i first believed  through many dangers toils and snares i have already
            come tis grace that brought me safe thus far and grace will lead me home'''
        self.short_lyrics =u'''twas grace that taught my heart to fear and grace my fears relieved how precious did that
            grace appear the hour i first believed'''
        self.error_lyrics =u'''amazing how sweet the trumpet that saved a wrench like me i once was losst but now am
            found waf blind but now i see  it was grace that taught my heart to fear and grace my fears relieved how
            precious did that grace appppppppear the hour i first believedxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx snares i have
            already come to this grace that brought me safe so far and grace will lead me home'''
        self.different_lyrics=u'''on a hill far away stood an old rugged cross the emblem of suffering and shame and i love
            that old cross where the dearest and best for a world of lost sinners was slain  so ill cherish the old rugged
            cross till my trophies at last i lay down i will cling to the old rugged cross and exchange it some day for a
            crown'''
        self.song1 = MagicMock()
        self.song2 = MagicMock()


    def songs_probably_equal_same_song_test(self):
        """
        Test the songs_probably_equal function with twice the same song.
        """
        #GIVEN: Two equal songs.
        self.song1.search_lyrics = self.full_lyrics
        self.song2.search_lyrics = self.full_lyrics
        
        #WHEN: We compare those songs for equality.
        result = songs_probably_equal(self.song1, self.song2)
        
        #THEN: The result should be True.
        assert result == True, u'The result should be True'


    def songs_probably_equal_short_song_test(self):
        """
        Test the songs_probably_equal function with a song and a shorter version of the same song.
        """
        #GIVEN: A song and a short version of the same song.
        self.song1.search_lyrics = self.full_lyrics
        self.song2.search_lyrics = self.short_lyrics
        
        #WHEN: We compare those songs for equality.
        result = songs_probably_equal(self.song1, self.song2)
        
        #THEN: The result should be True.
        assert result == True, u'The result should be True'


    def songs_probably_equal_error_song_test(self):
        """
        Test the songs_probably_equal function with a song and a  very erroneous version of the same song.
        """
        #GIVEN: A song and the same song with lots of errors.
        self.song1.search_lyrics = self.full_lyrics
        self.song2.search_lyrics = self.error_lyrics
        
        #WHEN: We compare those songs for equality.
        result = songs_probably_equal(self.song1, self.song2)
        
        #THEN: The result should be True.
        assert result == True, u'The result should be True'


    def songs_probably_equal_different_song_test(self):
        """
        Test the songs_probably_equal function with two different songs.
        """
        #GIVEN: Two different songs.
        self.song1.search_lyrics = self.full_lyrics
        self.song2.search_lyrics = self.different_lyrics
        
        #WHEN: We compare those songs for equality.
        result = songs_probably_equal(self.song1, self.song2)
        
        #THEN: The result should be False.
        assert result == False, u'The result should be False'


    def remove_typos_beginning_test(self):
        """
        Test the _remove_typos function with a typo at the beginning.
        """
        #GIVEN: A diffset with a difference at the beginning.
        diff = [('replace', 0, 2, 0, 1), ('equal', 2, 11, 1, 10)]

        #WHEN: We remove the typos in there.
        result = _remove_typos(diff)

        #THEN: There should be no typos at the beginning anymore.
        assert len(result) == 1, u'The result should contain only one element.'
        assert result[0][0] == 'equal', u'The result should contain an equal element.'


    def remove_typos_beginning_negated_test(self):
        """
        Test the _remove_typos function with a large difference at the beginning.
        """
        #GIVEN: A diffset with a large difference at the beginning.
        diff = [('replace', 0, 20, 0, 1), ('equal', 20, 29, 1, 10)]

        #WHEN: We remove the typos in there.
        result = _remove_typos(diff)

        #THEN: There diff should not have changed.
        assert result == diff


    def remove_typos_end_test(self):
        """
        Test the _remove_typos function with a typo at the end.
        """
        #GIVEN: A diffset with a difference at the end.
        diff = [('equal', 0, 10, 0, 10), ('replace', 10, 12, 10, 11)]

        #WHEN: We remove the typos in there.
        result = _remove_typos(diff)

        #THEN: There should be no typos at the end anymore.
        assert len(result) == 1, u'The result should contain only one element.'
        assert result[0][0] == 'equal', u'The result should contain an equal element.'


    def remove_typos_end_negated_test(self):
        """
        Test the _remove_typos function with a large difference at the end.
        """
        #GIVEN: A diffset with a large difference at the end.
        diff = [('equal', 0, 10, 0, 10), ('replace', 10, 20, 10, 1)]

        #WHEN: We remove the typos in there.
        result = _remove_typos(diff)

        #THEN: There diff should not have changed.
        assert result == diff


    def remove_typos_middle_test(self):
        """
        Test the _remove_typos function with a typo in the middle.
        """
        #GIVEN: A diffset with a difference in the middle.
        diff = [('equal', 0, 10, 0, 10), ('replace', 10, 12, 10, 11), ('equal', 12, 22, 11, 21)]

        #WHEN: We remove the typos in there.
        result = _remove_typos(diff)

        #THEN: There should be no typos in the middle anymore. The remaining equals should have been merged.
        assert len(result) is 1, u'The result should contain only one element.'
        assert result[0][0] == 'equal', u'The result should contain an equal element.'
        assert result[0][1] == 0, u'The start indices should be kept.'
        assert result[0][2] == 22, u'The stop indices should be kept.'
        assert result[0][3] == 0, u'The start indices should be kept.'
        assert result[0][4] == 21, u'The stop indices should be kept.'


    def remove_typos_beginning_negated_test(self):
        """
        Test the _remove_typos function with a large difference in the middle.
        """
        #GIVEN: A diffset with a large difference in the middle.
        diff = [('equal', 0, 10, 0, 10), ('replace', 10, 20, 10, 11), ('equal', 20, 30, 11, 21)]

        #WHEN: We remove the typos in there.
        result = _remove_typos(diff)

        #THEN: There diff should not have changed.
        assert result == diff


    def op_length_test(self):
        """
        Test the _op_length function.
        """
        #GIVEN: A diff entry.
        diff_entry = ('replace', 0, 2, 4, 14)

        #WHEN: We calculate the length of that diff.
        result = _op_length(diff_entry)

        #THEN: The maximum length should be returned.
        assert result == 10, u'The length should be 10.'


    def length_of_equal_blocks_test(self):
        """
        Test the _length_of_equal_blocks function.
        """
        #GIVEN: A diff.
        diff = [('equal', 0, 100, 0, 100), ('replace', 100, 110, 100, 110), ('equal', 110, 120, 110, 120), \
                ('replace', 120, 200, 120, 200), ('equal', 200, 300, 200, 300)]

        #WHEN: We calculate the length of that diffs equal blocks.
        result = _length_of_equal_blocks(diff)

        #THEN: The total length should be returned. Note: Equals smaller 70 are ignored.
        assert result == 200, u'The length should be 200.'


    def length_of_longest_equal_block_test(self):
        """
        Test the _length_of_longest_equal_block function.
        """
        #GIVEN: A diff.
        diff = [('equal', 0, 100, 0, 100), ('replace', 100, 110, 100, 110), ('equal', 200, 500, 200, 500)]

        #WHEN: We calculate the length of that diffs longest equal block.
        result = _length_of_longest_equal_block(diff)

        #THEN: The total correct length should be returned.
        assert result == 300, u'The length should be 300.'