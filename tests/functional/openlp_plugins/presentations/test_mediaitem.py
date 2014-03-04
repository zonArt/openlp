# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
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
"""
This module contains tests for the lib submodule of the Presentations plugin.
"""
from unittest import TestCase

from PyQt4 import QtGui

from openlp.core.common import Registry
from openlp.plugins.presentations.lib.mediaitem import PresentationMediaItem
from tests.functional import patch, MagicMock


class TestMediaItem(TestCase):
    """
    Test the mediaitem methods.
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
        self.application = QtGui.QApplication.instance()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application

    def build_file_mask_string_test(self):
        """
        Test the build_file_mask_string() method
        """
        # GIVEN: Different controllers.
        impress_controller = MagicMock()
        impress_controller.enabled.return_value = True
        impress_controller.supports = ['odp']
        impress_controller.also_supports = ['ppt']
        presentation_controller = MagicMock()
        presentation_controller.enabled.return_value = True
        presentation_controller.supports = ['ppt']
        presentation_controller.also_supports = []
        presentation_viewer_controller = MagicMock()
        presentation_viewer_controller.enabled.return_value = False
        pdf_controller = MagicMock()
        pdf_controller.enabled.return_value = True
        pdf_controller.supports = ['pdf']
        pdf_controller.also_supports = ['xps']
        # Mock the controllers.
        self.media_item.controllers = {
            'Impress': impress_controller,
            'Powerpoint': presentation_controller,
            'Powerpoint Viewer': presentation_viewer_controller,
            'Pdf': pdf_controller
        }

        # WHEN: Build the file mask.
        with patch('openlp.plugins.presentations.lib.mediaitem.translate') as mocked_translate:
            mocked_translate.side_effect = lambda module, string_to_translate: string_to_translate
            self.media_item.build_file_mask_string()

        # THEN: The file mask should be generated correctly
        self.assertIn('*.odp', self.media_item.on_new_file_masks, 'The file mask should contain the odp extension')
        self.assertIn('*.ppt', self.media_item.on_new_file_masks, 'The file mask should contain the ppt extension')
        self.assertIn('*.pdf', self.media_item.on_new_file_masks, 'The file mask should contain the pdf extension')
        self.assertIn('*.xps', self.media_item.on_new_file_masks, 'The file mask should contain the xps extension')
