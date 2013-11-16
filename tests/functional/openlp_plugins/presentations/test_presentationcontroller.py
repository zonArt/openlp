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
This module contains tests for the presentationcontroller module of the Presentations plugin.
"""

from unittest import TestCase

from tests.functional import MagicMock, patch

from openlp.plugins.presentations.lib.presentationcontroller import PresentationDocument

# TODO: Items left to test
#   PresentationController
#       __init__
#       enabled
#       is_available
#       check_available
#       start_process
#       kill
#       add_document
#       remove_doc
#       close_presentation
#       _get_plugin_manager


class TestPptviewDocument(TestCase):
    """
    Test the PptviewDocument Class
    """
    # TODO: Items left to test
    #   PresentationDocument
    #       __init__
    #       load_presentation
    #       presentation_deleted
    #       get_file_name
    #       get_thumbnail_folder
    #       get_temp_folder
    #       check_thumbnails
    #       close_presentation
    #       is_active
    #       is_loaded
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
    #       convert_thumbnail
    #       get_thumbnail_path
    #       poll_slidenumber
    #       get_slide_text
    #       get_slide_notes

    def setUp(self):
        """
        Set up the patches and mocks need for all tests.
        """
        self.check_directory_exists_patcher = patch(
            'openlp.plugins.presentations.lib.presentationcontroller.check_directory_exists')
        self.get_thumbnail_folder_patcher = patch(
            'openlp.plugins.presentations.lib.presentationcontroller.PresentationDocument.get_thumbnail_folder')
        self._setup_patcher = patch(
            'openlp.plugins.presentations.lib.presentationcontroller.PresentationDocument._setup')

        self.mock_check_directory_exists = self.check_directory_exists_patcher.start()
        self.mock_get_thumbnail_folder = self.get_thumbnail_folder_patcher.start()
        self.mock_setup = self._setup_patcher.start()

        self.mock_controller = MagicMock()

        self.mock_get_thumbnail_folder.return_value = 'returned/path/'

    def tearDown(self):
        """
        Stop the patches
        """
        self.check_directory_exists_patcher.stop()
        self.get_thumbnail_folder_patcher.stop()
        self._setup_patcher.stop()

    def initalise_presentation_document_test(self):
        """
        Test the PresentationDocument __init__ method when initalising the PresentationDocument Class
        """
        # GIVEN: A reset mock_setup and mocked controller
        self.mock_setup.reset()

        # WHEN: Creating an instance of PresentationDocument
        instance = PresentationDocument(self.mock_controller, 'Name')

        # THEN: PresentationDocument.__init__ should have been called with the correct arguments
        self.mock_setup.assert_called_once_with('Name')

    def presentation_document_setup_test(self):
        """
        Test the PresentationDocument _setup method when initalising the PresentationDocument Class
        """
        self._setup_patcher.stop()

        # GIVEN: A  mocked controller, patched check_directory_exists_patcher and patched get_thumbnail_folder method

        # WHEN: Creating an instance of PresentationDocument
        instance = PresentationDocument(self.mock_controller, 'Name')

        # THEN: check_directory_exists should have been called with the correct arguments
        self.mock_check_directory_exists.assert_called_once_with('returned/path/')

        self._setup_patcher.start()
