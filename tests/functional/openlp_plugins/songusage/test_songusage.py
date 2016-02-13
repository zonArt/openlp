# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
This module contains tests for the Songusage plugin.
"""
from unittest import TestCase
from openlp.plugins.songusage.songusageplugin import SongUsagePlugin


class TestSongUsage(TestCase):

    def test_about_text(self):
        # GIVEN: The SongUsagePlugin
        # WHEN: Retrieving the about text
        # THEN: about() should return a string object
        self.assertIsInstance(SongUsagePlugin.about(), str)
        # THEN: about() should return a non-empty string
        self.assertNotEquals(len(SongUsagePlugin.about()), 0)
        self.assertNotEquals(len(SongUsagePlugin.about()), 0)
