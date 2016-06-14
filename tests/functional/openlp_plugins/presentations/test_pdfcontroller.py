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
This module contains tests for the PdfController
"""
import os
import shutil
from unittest import TestCase, SkipTest
from tempfile import mkdtemp
from PyQt5 import QtCore, QtGui

from openlp.plugins.presentations.lib.pdfcontroller import PdfController, PdfDocument
from tests.functional import MagicMock, patch
from openlp.core.common import Settings
from openlp.core.lib import ScreenList
from tests.utils.constants import TEST_RESOURCES_PATH
from tests.helpers.testmixin import TestMixin

__default_settings__ = {
    'presentations/enable_pdf_program': False,
    'presentations/thumbnail_scheme': ''
}

SCREEN = {
    'primary': False,
    'number': 1,
    'size': QtCore.QRect(0, 0, 1024, 768)
}


class TestPdfController(TestCase, TestMixin):
    """
    Test the PdfController.
    """
    def setUp(self):
        """
        Set up the components need for all tests.
        """
        self.setup_application()
        self.build_settings()
        # Mocked out desktop object
        self.desktop = MagicMock()
        self.desktop.primaryScreen.return_value = SCREEN['primary']
        self.desktop.screenCount.return_value = SCREEN['number']
        self.desktop.screenGeometry.return_value = SCREEN['size']
        self.screens = ScreenList.create(self.desktop)
        Settings().extend_default_settings(__default_settings__)
        self.temp_folder = mkdtemp()
        self.thumbnail_folder = mkdtemp()
        self.mock_plugin = MagicMock()
        self.mock_plugin.settings_section = self.temp_folder

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.screens
        self.destroy_settings()
        shutil.rmtree(self.thumbnail_folder)
        shutil.rmtree(self.temp_folder)

    def test_constructor(self):
        """
        Test the Constructor from the PdfController
        """
        # GIVEN: No presentation controller
        controller = None

        # WHEN: The presentation controller object is created
        controller = PdfController(plugin=self.mock_plugin)

        # THEN: The name of the presentation controller should be correct
        self.assertEqual('Pdf', controller.name, 'The name of the presentation controller should be correct')

    def test_load_pdf(self):
        """
        Test loading of a Pdf using the PdfController
        """
        # GIVEN: A Pdf-file
        test_file = os.path.join(TEST_RESOURCES_PATH, 'presentations', 'pdf_test1.pdf')

        # WHEN: The Pdf is loaded
        controller = PdfController(plugin=self.mock_plugin)
        if not controller.check_available():
            raise SkipTest('Could not detect mudraw or ghostscript, so skipping PDF test')
        controller.temp_folder = self.temp_folder
        controller.thumbnail_folder = self.thumbnail_folder
        document = PdfDocument(controller, test_file)
        loaded = document.load_presentation()

        # THEN: The load should succeed and we should be able to get a pagecount
        self.assertTrue(loaded, 'The loading of the PDF should succeed.')
        self.assertEqual(3, document.get_slide_count(), 'The pagecount of the PDF should be 3.')

    def test_load_pdf_pictures(self):
        """
        Test loading of a Pdf and check size of generate pictures
        """
        # GIVEN: A Pdf-file
        test_file = os.path.join(TEST_RESOURCES_PATH, 'presentations', 'pdf_test1.pdf')

        # WHEN: The Pdf is loaded
        controller = PdfController(plugin=self.mock_plugin)
        if not controller.check_available():
            raise SkipTest('Could not detect mudraw or ghostscript, so skipping PDF test')
        controller.temp_folder = self.temp_folder
        controller.thumbnail_folder = self.thumbnail_folder
        document = PdfDocument(controller, test_file)
        loaded = document.load_presentation()

        # THEN: The load should succeed and pictures should be created and have been scales to fit the screen
        self.assertTrue(loaded, 'The loading of the PDF should succeed.')
        image = QtGui.QImage(os.path.join(self.temp_folder, 'pdf_test1.pdf', 'mainslide001.png'))
        # Based on the converter used the resolution will differ a bit
        if controller.gsbin:
            self.assertEqual(760, image.height(), 'The height should be 760')
            self.assertEqual(537, image.width(), 'The width should be 537')
        else:
            self.assertEqual(768, image.height(), 'The height should be 768')
            self.assertEqual(543, image.width(), 'The width should be 543')

    @patch('openlp.plugins.presentations.lib.pdfcontroller.check_binary_exists')
    def test_process_check_binary_mudraw(self, mocked_check_binary_exists):
        """
        Test that the correct output from mudraw is detected
        """
        # GIVEN: A mocked check_binary_exists that returns mudraw output
        mudraw_output = (b'usage: mudraw [options] input [pages]\n\t-o -\toutput filename (%d for page number)n\t\tsupp'
                         b'orted formats: pgm, ppm, pam, png, pbmn\t-p -\tpasswordn\t-r -\tresolution in dpi (default: '
                         b'72)n\t-w -\twidth (in pixels) (maximum width if -r is specified)n\t-h -\theight (in pixels) '
                         b'(maximum height if -r is specified)')
        mocked_check_binary_exists.return_value = mudraw_output

        # WHEN: Calling process_check_binary
        ret = PdfController.process_check_binary('test')

        # THEN: mudraw should be detected
        self.assertEqual('mudraw', ret, 'mudraw should have been detected')

    @patch('openlp.plugins.presentations.lib.pdfcontroller.check_binary_exists')
    def test_process_check_binary_new_motool(self, mocked_check_binary_exists):
        """
        Test that the correct output from the new mutool is detected
        """
        # GIVEN: A mocked check_binary_exists that returns new mutool output
        new_mutool_output = (b'usage: mutool <command> [options]\n\tdraw\t-- convert document\n\trun\t-- run javascript'
                             b'\n\tclean\t-- rewrite pdf file\n\textract\t-- extract font and image resources\n\tinfo\t'
                             b'-- show information about pdf resources\n\tpages\t-- show information about pdf pages\n'
                             b'\tposter\t-- split large page into many tiles\n\tshow\t-- show internal pdf objects\n\t'
                             b'create\t-- create pdf document\n\tmerge\t-- merge pages from multiple pdf sources into a'
                             b'new pdf\n')
        mocked_check_binary_exists.return_value = new_mutool_output

        # WHEN: Calling process_check_binary
        ret = PdfController.process_check_binary('test')

        # THEN: mutool should be detected
        self.assertEqual('mutool', ret, 'mutool should have been detected')

    @patch('openlp.plugins.presentations.lib.pdfcontroller.check_binary_exists')
    def test_process_check_binary_old_motool(self, mocked_check_binary_exists):
        """
        Test that the output from the old mutool is not accepted
        """
        # GIVEN: A mocked check_binary_exists that returns old mutool output
        old_mutool_output = (b'usage: mutool <command> [options]\n\tclean\t-- rewrite pdf file\n\textract\t-- extract '
                             b'font and image resources\n\tinfo\t-- show information about pdf resources\n\tposter\t-- '
                             b'split large page into many tiles\n\tshow\t-- show internal pdf objects')
        mocked_check_binary_exists.return_value = old_mutool_output

        # WHEN: Calling process_check_binary
        ret = PdfController.process_check_binary('test')

        # THEN: mutool should be detected
        self.assertIsNone(ret, 'old mutool should not be accepted!')

    @patch('openlp.plugins.presentations.lib.pdfcontroller.check_binary_exists')
    def test_process_check_binary_gs(self, mocked_check_binary_exists):
        """
        Test that the correct output from gs is detected
        """
        # GIVEN: A mocked check_binary_exists that returns gs output
        gs_output = (b'GPL Ghostscript 9.19 (2016-03-23)\nCopyright (C) 2016 Artifex Software, Inc.  All rights reserv'
                     b'ed.\nUsage: gs [switches] [file1.ps file2.ps ...]')
        mocked_check_binary_exists.return_value = gs_output

        # WHEN: Calling process_check_binary
        ret = PdfController.process_check_binary('test')

        # THEN: mutool should be detected
        self.assertEqual('gs', ret, 'mutool should have been detected')
