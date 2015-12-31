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
This module contains tests for the lib submodule of the Presentations plugin.
"""
from unittest import TestCase

from openlp.core.common import Registry
from openlp.plugins.presentations.lib.mediaitem import MessageListener, PresentationMediaItem
from tests.functional import patch, MagicMock
from tests.helpers.testmixin import TestMixin


class TestMessageListener(TestCase, TestMixin):
    """
    Test the Presentation Message Listener.
    """
    def setUp(self):
        """
        Set up the components need for all tests.
        """
        Registry.create()
        Registry().register('service_manager', MagicMock())
        Registry().register('main_window', MagicMock())
        with patch('openlp.plugins.presentations.lib.mediaitem.MediaManagerItem._setup'), \
                patch('openlp.plugins.presentations.lib.mediaitem.PresentationMediaItem.setup_item'):
            self.media_item = PresentationMediaItem(None, MagicMock, MagicMock())

    @patch('openlp.plugins.presentations.lib.mediaitem.MessageListener._setup')
    def start_presentation_test(self, media_mock):
        """
        Find and chose a controller to play a presentations.
        """
        # GIVEN: A single controller and service item wanting to use the controller
        mock_item = MagicMock()
        mock_item.processor = 'Powerpoint'
        mock_item.get_frame_path.return_value = "test.ppt"
        self.media_item.automatic = False
        mocked_controller = MagicMock()
        mocked_controller.available = True
        mocked_controller.supports = ['ppt']
        controllers = {
            'Powerpoint': mocked_controller
        }
        ml = MessageListener(self.media_item)
        ml.media_item = self.media_item
        ml.controllers = controllers
        ml.preview_handler = MagicMock()
        ml.timer = MagicMock()

        # WHEN: request the presentation to start
        ml.startup([mock_item, False, False, False])

        # THEN: The controllers will be setup.
        self.assertTrue(len(controllers), 'We have loaded a controller')

    @patch('openlp.plugins.presentations.lib.mediaitem.MessageListener._setup')
    def start_presentation_with_no_player_test(self, media_mock):
        """
        Find and chose a controller to play a presentations when the player is not available.
        """
        # GIVEN: A single controller and service item wanting to use the controller
        mock_item = MagicMock()
        mock_item.processor = 'Powerpoint'
        mock_item.get_frame_path.return_value = "test.ppt"
        self.media_item.automatic = False
        mocked_controller = MagicMock()
        mocked_controller.available = True
        mocked_controller.supports = ['ppt']
        mocked_controller1 = MagicMock()
        mocked_controller1.available = False
        mocked_controller1.supports = ['ppt']
        controllers = {
            'Impress': mocked_controller,
            'Powerpoint': mocked_controller1
        }
        ml = MessageListener(self.media_item)
        ml.media_item = self.media_item
        ml.controllers = controllers
        ml.preview_handler = MagicMock()
        ml.timer = MagicMock()

        # WHEN: request the presentation to start
        ml.startup([mock_item, False, False, False])

        # THEN: The controllers will be setup.
        self.assertTrue(len(controllers), 'We have loaded a controller')
