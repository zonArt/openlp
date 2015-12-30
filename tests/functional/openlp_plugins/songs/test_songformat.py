# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 OpenLP Developers                                   #
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
This module contains tests for the SongFormat class
"""
from unittest import TestCase

from openlp.plugins.songs.lib.importer import SongFormat


class TestSongFormat(TestCase):

    def test_get_format_list(self):
        self.assertEquals(len(SongFormat.get_format_list()), len(SongFormat.__attributes__))

    def test_get_attributed_no_attributes(self):
        for song_format in SongFormat.get_format_list():
            self.assertEquals(SongFormat.__attributes__[song_format], SongFormat.get(song_format))

    def test_get_attributed_single_attribute(self):
        for song_format in SongFormat.get_format_list():
            for attribute in SongFormat.get(song_format).keys():
                self.assertEquals(SongFormat.get(song_format, attribute),
                        SongFormat.get(song_format)[attribute])
            for attribute in SongFormat.__defaults__.keys():
                if attribute not in SongFormat.get(song_format).keys():
                    self.assertEquals(SongFormat.get(song_format, attribute),
                            SongFormat.__defaults__[attribute])

    def test_get_attributed_multiple_attributes(self):
        for song_format in SongFormat.get_format_list():
            self.assertEquals(2, len(SongFormat.get(song_format, 'canDisable', 'availability')))

