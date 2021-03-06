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

from openlp.core import Registry
from openlp.plugins.media.mediaplugin import MediaPlugin, process_check_binary

from tests.functional import MagicMock, patch
from tests.helpers.testmixin import TestMixin


class MediaPluginTest(TestCase, TestMixin):
    """
    Test the media plugin
    """
    def setUp(self):
        Registry.create()

    @patch(u'openlp.plugins.media.mediaplugin.Plugin.initialise')
    @patch(u'openlp.plugins.media.mediaplugin.Settings')
    def test_initialise(self, _mocked_settings, mocked_initialise):
        """
        Test that the initialise() method overwrites the built-in one, but still calls it
        """
        # GIVEN: A media plugin instance and a mocked settings object
        media_plugin = MediaPlugin()
        mocked_settings = MagicMock()
        mocked_settings.get_files_from_config.return_value = True  # Not the real value, just need something "true-ish"
        _mocked_settings.return_value = mocked_settings

        # WHEN: initialise() is called
        media_plugin.initialise()

        # THEN: The settings should be upgraded and the base initialise() method should be called
        mocked_initialise.assert_called_with()

    def test_about_text(self):
        # GIVEN: The MediaPlugin
        # WHEN: Retrieving the about text
        # THEN: about() should return a string object
        self.assertIsInstance(MediaPlugin.about(), str)
        # THEN: about() should return a non-empty string
        self.assertNotEquals(len(MediaPlugin.about()), 0)

    @patch('openlp.plugins.media.mediaplugin.check_binary_exists')
    def test_process_check_binary_pass(self, mocked_checked_binary_exists):
        """
        Test that the Process check returns true if found
        """
        # GIVEN: A media plugin instance
        # WHEN: function is called with the correct name
        mocked_checked_binary_exists.return_value = str.encode('MediaInfo Command line')
        result = process_check_binary('MediaInfo')

        # THEN: The the result should be True
        self.assertTrue(result, 'Mediainfo should have been found')

    @patch('openlp.plugins.media.mediaplugin.check_binary_exists')
    def test_process_check_binary_fail(self, mocked_checked_binary_exists):
        """
        Test that the Process check returns false if not found
        """
        # GIVEN: A media plugin instance
        # WHEN: function is called with the wrong name
        mocked_checked_binary_exists.return_value = str.encode('MediaInfo1 Command line')
        result = process_check_binary("MediaInfo1")

        # THEN: The the result should be True
        self.assertFalse(result, "Mediainfo should not have been found")
