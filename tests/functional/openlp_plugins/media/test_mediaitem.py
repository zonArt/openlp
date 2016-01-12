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
Test the media plugin
"""
from unittest import TestCase

from openlp.core import Registry, Settings
from openlp.plugins.media.mediaplugin import MediaPlugin
from openlp.plugins.media.lib.mediaitem import MediaMediaItem
from openlp.core.ui.media.mediacontroller import MediaController

from PyQt5 import QtCore

from tests.functional import MagicMock, patch
from tests.helpers.testmixin import TestMixin

__default_settings__ = {
    'media/media auto start': QtCore.Qt.Unchecked,
    'media/media files': []
}


class MediaItemTest(TestCase, TestMixin):
    """
    Test the media item for Media
    """

    def setUp(self):
        """
        Set up the components need for all tests.
        """
        with patch('openlp.plugins.media.lib.mediaitem.MediaManagerItem.__init__'),\
                patch('openlp.plugins.media.lib.mediaitem.MediaMediaItem.setup'):
            self.media_item = MediaMediaItem(None, MagicMock())
            self.media_item.settings_section = 'media'
        self.setup_application()
        self.build_settings()
        Settings().extend_default_settings(__default_settings__)

    def tearDown(self):
        """
        Clean up after the tests
        """
        self.destroy_settings()

    def test_search_found(self):
        """
        Media Remote Search Successful find
        """
        # GIVEN: The Mediaitem set up a list of media
        Settings().setValue(self.media_item.settings_section + '/media files', ['test.mp3', 'test.mp4'])
        # WHEN: Retrieving the test file
        result = self.media_item.search('test.mp4', False)
        # THEN: a file should be found
        self.assertEqual(result, [['test.mp4', 'test.mp4']], 'The result file contain the file name')

    def test_search_not_found(self):
        """
        Media Remote Search not find
        """
        # GIVEN: The Mediaitem set up a list of media
        Settings().setValue(self.media_item.settings_section + '/media files', ['test.mp3', 'test.mp4'])
        # WHEN: Retrieving the test file
        result = self.media_item.search('test.mpx', False)
        # THEN: a file should be found
        self.assertEqual(result, [], 'The result file should be empty')
