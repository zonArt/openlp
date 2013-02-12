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

from openlp.plugins.songs.lib.duplicatesongfinder import DuplicateSongFinder

class TestLib(TestCase):
    def duplicate_song_removal_test(self):
        full_lyrics =u'''amazing grace how sweet the sound that saved a wretch like me i once was lost but now am found was
        blind but now i see  twas grace that taught my heart to fear and grace my fears relieved how precious did that grace
        appear the hour i first believed  through many dangers toils and snares i have already come tis grace that brought
        me safe thus far and grace will lead me home  the lord has promised good to me his word my hope secures he will my
        shield and portion be as long as life endures  yea when this flesh and heart shall fail and mortal life shall cease
        i shall possess within the veil a life of joy and peace  when weve been here ten thousand years bright shining as
        the sun weve no less days to sing gods praise than when weve first begun'''
        short_lyrics =u'''twas grace that taught my heart to fear and grace my fears relieved how precious did that grace
        appear the hour i first believed'''
        error_lyrics =u'''amazing grace how sweet the sound that saved a wretch like me i once was lost but now am found was
        blind but now i see  twas grace that taught my heart to fear and grace my fears relieved how precious did that grace
        appear the hour i first believedxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx snares i have already come tis grace that brought
        me safe thus far and grace will lead me home  the lord has promised good to me his word my hope secures he will my
        shield andwhen this flcsh and heart shall fail and mortal life shall cease
        i shall possess within the veila lifeofjoy and peace  when weve been here ten thousand years bright shining as
        the sun weve no less days to sing gods praise than when weve first begun'''
        different_lyrics=u'''on a hill far away stood an old rugged cross the emblem of suffering and shame and i love that
        old cross where the dearest and best for a world of lost sinners was slain  so ill cherish the old rugged cross till
        my trophies at last i lay down i will cling to the old rugged cross and exchange it some day for a crown'''
        dsf = DuplicateSongFinder()
        song1 = MagicMock()
        song2 = MagicMock()
        
        song1.search_lyrics = full_lyrics
        song2.search_lyrics = full_lyrics
        assert dsf.songsProbablyEqual(song1, song2) is True, u'The result should be True'
        song1.search_lyrics = full_lyrics
        song2.search_lyrics = short_lyrics
        assert dsf.songsProbablyEqual(song1, song2) is True, u'The result should be True'
        song1.search_lyrics = full_lyrics
        song2.search_lyrics = error_lyrics
        assert dsf.songsProbablyEqual(song1, song2) is True, u'The result should be True'
        song1.search_lyrics = full_lyrics
        song2.search_lyrics = different_lyrics
        assert dsf.songsProbablyEqual(song1, song2) is False, u'The result should be False'
