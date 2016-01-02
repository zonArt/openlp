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
        # GIVEN: The SongFormat class
        # WHEN: Retrieving the format list
        # THEN: All SongFormats should be returned
        self.assertEquals(len(SongFormat.get_format_list()), len(SongFormat.__attributes__),
                "The returned SongFormats don't match the stored ones")

    def test_get_attributed_no_attributes(self):
        # GIVEN: A SongFormat
        # WHEN: Retrieving all attributes of a SongFormat
        for song_format in SongFormat.get_format_list():
            # THEN: All attributes associated with the SongFormat should be returned
            self.assertEquals(SongFormat.get(song_format), SongFormat.__attributes__[song_format],
                    "The returned attributes don't match the stored ones")

    def test_get_attributed_single_attribute(self):
        # GIVEN: A SongFormat
        for song_format in SongFormat.get_format_list():
            # WHEN: Retrieving an attribute that overrides the default values
            for attribute in SongFormat.get(song_format).keys():
                # THEN: Return the attribute
                self.assertEquals(SongFormat.get(song_format, attribute), SongFormat.get(song_format)[attribute],
                        "The returned attribute doesn't match the stored one")
            # WHEN: Retrieving an attribute that was not overridden
            for attribute in SongFormat.__defaults__.keys():
                if attribute not in SongFormat.get(song_format).keys():
                    # THEN: Return the default value
                    self.assertEquals(SongFormat.get(song_format, attribute), SongFormat.__defaults__[attribute],
                            "The returned attribute does not match the default values stored")

    def test_get_attributed_multiple_attributes(self):
        # GIVEN: A SongFormat
        # WHEN: Retrieving multiple attributes at the same time
        for song_format in SongFormat.get_format_list():
            # THEN: Return all attributes that were specified
            self.assertEquals(len(SongFormat.get(song_format, 'canDisable', 'availability')), 2,
                    "Did not return the correct number of attributes when retrieving multiple attributes at once")

