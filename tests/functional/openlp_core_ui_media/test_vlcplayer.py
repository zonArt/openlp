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
Package to test the openlp.core.ui.media.vlcplayer package.
"""
import os
import sys

from unittest import TestCase
from tests.functional import patch

from openlp.core.ui.media.vlcplayer import get_vlc


class TestVLCPlayer(TestCase):
    """
    Test the functions in the :mod:`vlcplayer` module.
    """

    @patch('openlp.core.ui.media.vlcplayer.is_macosx')
    def fix_vlc_22_plugin_path_test(self, mocked_is_macosx):
        """
        Test that on OS X we set the VLC plugin path to fix a bug in the VLC module
        """
        # GIVEN: We're on OS X and we don't have the VLC plugin path set
        mocked_is_macosx.return_value = True
        if 'VLC_PLUGIN_PATH' in os.environ:
            del os.environ['VLC_PLUGIN_PATH']
        if 'openlp.core.ui.media.vendor.vlc' in sys.modules:
            del sys.modules['openlp.core.ui.media.vendor.vlc']

        # WHEN: An checking if the player is available
        get_vlc()

        # THEN: The extra environment variable should be there
        self.assertIn('VLC_PLUGIN_PATH', os.environ,
                      'The plugin path should be in the environment variables')
        self.assertEqual('/Applications/VLC.app/Contents/MacOS/plugins', os.environ['VLC_PLUGIN_PATH'])

    @patch.dict(os.environ)
    @patch('openlp.core.ui.media.vlcplayer.is_macosx')
    def not_osx_fix_vlc_22_plugin_path_test(self, mocked_is_macosx):
        """
        Test that on Linux or some other non-OS X we do not set the VLC plugin path
        """
        # GIVEN: We're not on OS X and we don't have the VLC plugin path set
        mocked_is_macosx.return_value = False
        if 'VLC_PLUGIN_PATH' in os.environ:
            del os.environ['VLC_PLUGIN_PATH']
        if 'openlp.core.ui.media.vendor.vlc' in sys.modules:
            del sys.modules['openlp.core.ui.media.vendor.vlc']

        # WHEN: An checking if the player is available
        get_vlc()

        # THEN: The extra environment variable should NOT be there
        self.assertNotIn('VLC_PLUGIN_PATH', os.environ,
                         'The plugin path should NOT be in the environment variables')
