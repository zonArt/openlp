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
Functional tests to test the PowerPointController class and related methods.
"""
import os
if os.name == 'nt':
    import pywintypes
import shutil
from unittest import TestCase
from tempfile import mkdtemp

from tests.functional import patch, MagicMock
from tests.helpers.testmixin import TestMixin

from openlp.plugins.presentations.lib.powerpointcontroller import PowerpointController, PowerpointDocument


class TestPowerpointController(TestCase, TestMixin):
    """
    Test the PowerpointController Class
    """

    def setUp(self):
        """
        Set up the patches and mocks need for all tests.
        """
        self.get_application()
        self.build_settings()
        self.mock_plugin = MagicMock()
        self.temp_folder = mkdtemp()
        self.mock_plugin.settings_section = self.temp_folder

    def tearDown(self):
        """
        Stop the patches
        """
        self.destroy_settings()
        shutil.rmtree(self.temp_folder)

    def constructor_test(self):
        """
        Test the Constructor from the PowerpointController
        """
        # GIVEN: No presentation controller
        controller = None

        # WHEN: The presentation controller object is created
        controller = PowerpointController(plugin=self.mock_plugin)

        # THEN: The name of the presentation controller should be correct
        self.assertEqual('Powerpoint', controller.name,
                         'The name of the presentation controller should be correct')


class TestPowerpointDocument(TestCase):
    """
    Test the PowerpointDocument Class
    """

    def setUp(self):
        """
        Set up the patches and mocks need for all tests.
        """
        self.powerpoint_document_stop_presentation_patcher = patch(
            'openlp.plugins.presentations.lib.powerpointcontroller.PowerpointDocument.stop_presentation')
        self.presentation_document_get_temp_folder_patcher = patch(
            'openlp.plugins.presentations.lib.powerpointcontroller.PresentationDocument.get_temp_folder')
        self.presentation_document_setup_patcher = patch(
            'openlp.plugins.presentations.lib.powerpointcontroller.PresentationDocument._setup')
        self.mock_powerpoint_document_stop_presentation = self.powerpoint_document_stop_presentation_patcher.start()
        self.mock_presentation_document_get_temp_folder = self.presentation_document_get_temp_folder_patcher.start()
        self.mock_presentation_document_setup = self.presentation_document_setup_patcher.start()
        self.mock_controller = MagicMock()
        self.mock_presentation = MagicMock()
        self.mock_presentation_document_get_temp_folder.return_value = 'temp folder'

    def tearDown(self):
        """
        Stop the patches
        """
        self.powerpoint_document_stop_presentation_patcher.stop()
        self.presentation_document_get_temp_folder_patcher.stop()
        self.presentation_document_setup_patcher.stop()

    def show_error_msg_test(self):
        """
        Test the PowerpointDocument.show_error_msg() method gets called on com exception
        """
        if os.name == 'nt':
            # GIVEN: A PowerpointDocument with mocked controller and presentation
            with patch('openlp.plugins.presentations.lib.powerpointcontroller.critical_error_message_box') as \
                    mocked_critical_error_message_box:
                instance = PowerpointDocument(self.mock_controller, self.mock_presentation)
                instance.presentation = MagicMock()
                instance.presentation.SlideShowWindow.View.GotoSlide = MagicMock(side_effect=pywintypes.com_error('1'))

                # WHEN: Calling goto_slide which will throw an exception
                instance.goto_slide(42)

                # THEN: mocked_critical_error_message_box should have been called
                mocked_critical_error_message_box.assert_called_with('Error', 'An error occurred in the Powerpoint '
                                                                     'integration and the presentation will be stopped.'
                                                                     ' Restart the presentation if you wish to '
                                                                     'present it.')
