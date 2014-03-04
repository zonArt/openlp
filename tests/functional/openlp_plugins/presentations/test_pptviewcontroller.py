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
"""
This module contains tests for the pptviewcontroller module of the Presentations plugin.
"""
import os
from unittest import TestCase

from tests.functional import MagicMock, patch

from openlp.plugins.presentations.lib.pptviewcontroller import PptviewDocument

#TODO: Items left to test
#   PptviewController
#       __init__
#       check_availablecheck_installed
#       start_process(self)
#       kill


class TestPptviewDocument(TestCase):
    """
    Test the PptviewDocument Class
    """
    #TODO: Items left to test
    #   PptviewDocument
    #       __init__
    #       create_thumbnails
    #       close_presentation
    #       is_loaded
    #       is_active
    #       blank_screen
    #       unblank_screen
    #       is_blank
    #       stop_presentation
    #       start_presentation
    #       get_slide_number
    #       get_slide_count
    #       goto_slide
    #       next_step
    #       previous_step

    def setUp(self):
        """
        Set up the patches and mocks need for all tests.
        """
        self.os_patcher = patch('openlp.plugins.presentations.lib.pptviewcontroller.os')
        self.pptview_document_create_thumbnails_patcher = patch(
            'openlp.plugins.presentations.lib.pptviewcontroller.PptviewDocument.create_thumbnails')
        self.pptview_document_stop_presentation_patcher = patch(
            'openlp.plugins.presentations.lib.pptviewcontroller.PptviewDocument.stop_presentation')
        self.presentation_document_get_temp_folder_patcher = patch(
            'openlp.plugins.presentations.lib.pptviewcontroller.PresentationDocument.get_temp_folder')
        self.presentation_document_setup_patcher = patch(
            'openlp.plugins.presentations.lib.pptviewcontroller.PresentationDocument._setup')
        self.screen_list_patcher = patch('openlp.plugins.presentations.lib.pptviewcontroller.ScreenList')
        self.rect_patcher = MagicMock()

        self.mock_os = self.os_patcher.start()
        self.mock_pptview_document_create_thumbnails = self.pptview_document_create_thumbnails_patcher.start()
        self.mock_pptview_document_stop_presentation = self.pptview_document_stop_presentation_patcher.start()
        self.mock_presentation_document_get_temp_folder = self.presentation_document_get_temp_folder_patcher.start()
        self.mock_presentation_document_setup = self.presentation_document_setup_patcher.start()
        self.mock_rect = self.rect_patcher.start()
        self.mock_screen_list = self.screen_list_patcher.start()

        self.mock_controller = MagicMock()
        self.mock_presentation = MagicMock()

        self.mock_presentation_document_get_temp_folder.return_value = 'temp folder'

    def tearDown(self):
        """
        Stop the patches
        """
        self.os_patcher.stop()
        self.pptview_document_create_thumbnails_patcher.stop()
        self.pptview_document_stop_presentation_patcher.stop()
        self.presentation_document_get_temp_folder_patcher.stop()
        self.presentation_document_setup_patcher.stop()
        self.rect_patcher.stop()
        self.screen_list_patcher.stop()

    def load_presentation_succesfull_test(self):
        """
        Test the PptviewDocument.load_presentation() method when the PPT is successfully opened
        """
        # GIVEN: A reset mocked_os
        self.mock_os.reset()

        # WHEN: The temporary directory exists and OpenPPT returns successfully (not -1)
        self.mock_os.path.isdir.return_value = True
        self.mock_controller.process.OpenPPT.return_value = 0
        instance = PptviewDocument(self.mock_controller, self.mock_presentation)
        instance.filepath = 'test\path.ppt'

        if os.name == 'nt':
            result = instance.load_presentation()

            # THEN: PptviewDocument.load_presentation should return True
            self.assertTrue(result)

    def load_presentation_un_succesfull_test(self):
        """
        Test the PptviewDocument.load_presentation() method when the temporary directory does not exist and the PPT is
        not successfully opened
        """
        # GIVEN: A reset mocked_os
        self.mock_os.reset()

        # WHEN: The temporary directory does not exist and OpenPPT returns unsuccessfully (-1)
        self.mock_os.path.isdir.return_value = False
        self.mock_controller.process.OpenPPT.return_value = -1
        instance = PptviewDocument(self.mock_controller, self.mock_presentation)
        instance.filepath = 'test\path.ppt'
        if os.name == 'nt':
            result = instance.load_presentation()

            # THEN: The temporary directory should be created and PptviewDocument.load_presentation should return False
            self.mock_os.makedirs.assert_called_once_with('temp folder')
            self.assertFalse(result)
