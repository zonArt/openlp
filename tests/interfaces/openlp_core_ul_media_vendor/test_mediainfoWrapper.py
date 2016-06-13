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
Package to test the openlp.core.ui.media package.
"""

import os
from unittest import TestCase

from openlp.core.ui.media.vendor.mediainfoWrapper import MediaInfoWrapper

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'media'))

TEST_MEDIA = [['avi_file.avi', 61495], ['mp3_file.mp3', 134426], ['mpg_file.mpg', 9404], ['mp4_file.mp4', 188336]]


class TestMediainfoWrapper(TestCase):

    def test_media_length(self):
        """
        Test the Media Info basic functionality
        """
        for test_data in TEST_MEDIA:
            # GIVEN: a media file
            full_path = os.path.normpath(os.path.join(TEST_PATH, test_data[0]))

            # WHEN the media data is retrieved
            results = MediaInfoWrapper.parse(full_path)

            # THEN you can determine the run time
            self.assertEqual(results.tracks[0].duration, test_data[1], 'The correct duration is returned for ' +
                                                                       test_data[0])
