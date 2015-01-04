# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 Raoul Snyman                                        #
# Portions copyright (c) 2008-2015 Tim Bentley, Gerald Britton, Jonathan      #
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
import shutil
from unittest import TestCase
from tempfile import mkdtemp

from tests.functional import patch, MagicMock
from tests.helpers.testmixin import TestMixin
from tests.utils.constants import TEST_RESOURCES_PATH

from openlp.plugins.presentations.lib.powerpointcontroller import PowerpointController, PowerpointDocument,\
    _get_text_from_shapes
from openlp.core.common import is_win

if is_win():
    import pywintypes


class TestPowerpointController(TestCase, TestMixin):
    """
    Test the PowerpointController Class
    """

    def setUp(self):
        """
        Set up the patches and mocks need for all tests.
        """
        self.setup_application()
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


class TestPowerpointDocument(TestCase, TestMixin):
    """
    Test the PowerpointDocument Class
    """

    def setUp(self):
        """
        Set up the patches and mocks need for all tests.
        """
        self.setup_application()
        self.build_settings()
        self.mock_plugin = MagicMock()
        self.temp_folder = mkdtemp()
        self.mock_plugin.settings_section = self.temp_folder
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
        self.file_name = os.path.join(TEST_RESOURCES_PATH, 'presentations', 'test.pptx')
        self.real_controller = PowerpointController(self.mock_plugin)

    def tearDown(self):
        """
        Stop the patches
        """
        self.powerpoint_document_stop_presentation_patcher.stop()
        self.presentation_document_get_temp_folder_patcher.stop()
        self.presentation_document_setup_patcher.stop()
        self.destroy_settings()
        shutil.rmtree(self.temp_folder)

    def show_error_msg_test(self):
        """
        Test the PowerpointDocument.show_error_msg() method gets called on com exception
        """
        if is_win():
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

    # add _test to the following if necessary
    def verify_loading_document(self):
        """
        Test loading a document in PowerPoint
        """
        if is_win() and self.real_controller.check_available():
            # GIVEN: A PowerpointDocument and a presentation
            doc = PowerpointDocument(self.real_controller, self.file_name)

            # WHEN: loading the filename
            doc.load_presentation()
            result = doc.is_loaded()

            # THEN: result should be true
            self.assertEqual(result, True, 'The result should be True')
        else:
            self.skipTest('Powerpoint not available, skipping test.')

    def create_titles_and_notes_test(self):
        """
        Test creating the titles from PowerPoint
        """
        if is_win() and self.real_controller.check_available():
            # GIVEN: mocked save_titles_and_notes, _get_text_from_shapes and two mocked slides
            self.doc = PowerpointDocument(self.real_controller, self.file_name)
            self.doc.save_titles_and_notes = MagicMock()
            self.doc._PowerpointDocument__get_text_from_shapes = MagicMock()
            slide = MagicMock()
            slide.Shapes.Title.TextFrame.TextRange.Text = 'SlideText'
            pres = MagicMock()
            pres.Slides = [slide, slide]
            self.doc.presentation = pres

            # WHEN reading the titles and notes
            self.doc.create_titles_and_notes()

            # THEN the save should have been called exactly once with 2 titles and 2 notes
            self.doc.save_titles_and_notes.assert_called_once_with(['SlideText\n', 'SlideText\n'], [' ', ' '])
        else:
            self.skipTest('Powerpoint not available, skipping test.')

    def create_titles_and_notes_with_no_slides_test(self):
        """
        Test creating the titles from PowerPoint when it returns no slides
        """
        if is_win() and self.real_controller.check_available():
            # GIVEN: mocked save_titles_and_notes, _get_text_from_shapes and two mocked slides
            doc = PowerpointDocument(self.real_controller, self.file_name)
            doc.save_titles_and_notes = MagicMock()
            doc._PowerpointDocument__get_text_from_shapes = MagicMock()
            pres = MagicMock()
            pres.Slides = []
            doc.presentation = pres

            # WHEN reading the titles and notes
            doc.create_titles_and_notes()

            # THEN the save should have been called exactly once with empty titles and notes
            doc.save_titles_and_notes.assert_called_once_with([], [])
        else:
            self.skipTest('Powerpoint not available, skipping test.')

    def get_text_from_shapes_test(self):
        """
        Test getting text from powerpoint shapes
        """
        # GIVEN: mocked shapes
        shape = MagicMock()
        shape.PlaceholderFormat.Type = 2
        shape.HasTextFrame = shape.TextFrame.HasText = True
        shape.TextFrame.TextRange.Text = 'slideText'
        shapes = [shape, shape]

        # WHEN: getting the text
        result = _get_text_from_shapes(shapes)

        # THEN: it should return the text
        self.assertEqual(result, 'slideText\nslideText\n', 'result should match \'slideText\nslideText\n\'')

    def get_text_from_shapes_with_no_shapes_test(self):
        """
        Test getting text from powerpoint shapes with no shapes
        """
        # GIVEN: empty shapes array
        shapes = []

        # WHEN: getting the text
        result = _get_text_from_shapes(shapes)

        # THEN: it should not fail but return empty string
        self.assertEqual(result, '', 'result should be empty')
