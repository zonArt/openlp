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
Functional tests to test the Impress class and related methods.
"""
from unittest import TestCase
import os
from mock import MagicMock, patch, mock_open
from openlp.plugins.presentations.lib.impresscontroller import ImpressController, ImpressDocument, TextType

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources'))

class TestLibModule(TestCase):

    def setUp(self):
        mocked_plugin = MagicMock()
        mocked_plugin.settings_section = 'presentations'
        self.file_name = os.path.join(TEST_PATH,"test.pptx")
        self.ppc = ImpressController(mocked_plugin)
        self.doc = ImpressDocument(self.ppc,self.file_name)

    def verify_installation(self):
        """
        Test the installation of ImpressViewer
        """
        # GIVEN: A boolean value set to true
        # WHEN: We "convert" it to a bool
        isInstalled = self.ppc.check_available()
        # THEN: We should get back a True bool
        assert isInstalled is True, 'The result should be True'

    def create_titles_and_notes_test(self):
        """
        Test ImpressDocument.create_titles_and_notes
        """
        # GIVEN: mocked PresentationController.save_titles_and_notes with 0 pages and the LibreoOffice Document
        self.doc.save_titles_and_notes = MagicMock()
        self.doc.document = MagicMock()
        self.doc.document.getDrawPages.return_value = MagicMock()
        self.doc.document.getDrawPages().getCount.return_value = 0
        # WHEN reading the titles and notes
        self.doc.create_titles_and_notes()
        # THEN save_titles_and_notes should have been called once with empty arrays
        self.doc.save_titles_and_notes.assert_called_once_with([],[])
        # GIVEN: reset mock and set it to 2 pages
        self.doc.save_titles_and_notes.reset_mock()
        self.doc.document.getDrawPages().getCount.return_value = 2
        # WHEN: a new call to create_titles_and_notes
        self.doc.create_titles_and_notes()
        # THEN: save_titles_and_notes should have been called once with two arrays of two elements
        self.doc.save_titles_and_notes.assert_called_once_with(['\n','\n'],[' ',' '])

    def _mock_a_LibreOffice_document(self,pageCount,noteCount,textCount):
        pages = MagicMock()
        page = MagicMock()
        pages.getByIndex.return_value = page
        notesPage = MagicMock()
        notesPage.getCount.return_value = noteCount
        shape = MagicMock()
        shape.supportsService.return_value = True
        shape.getString.return_value = 'Note'
        notesPage.getByIndex.return_value = shape
        page.getNotesPage.return_value = notesPage
        page.getCount.return_value = textCount
        #pageShape.getString.return_value = 'Title'
        #pageShape.getString.side_effect = self._get_string_side_effect
        #page.getByIndex.return_value = pageShape
        page.getByIndex.side_effect = self._get_page_shape_side_effect
        pages.getCount.return_value = pageCount
        document = MagicMock()
        document.getDrawPages.return_value = pages
        document.getByIndex.return_value = page
        return document

    def _get_page_shape_side_effect(*args, **kwargs):
        pageShape = MagicMock()
        pageShape.supportsService.return_value = True
        if args[1] == 0:
            pageShape.getShapeType.return_value = 'com.sun.star.presentation.TitleTextShape'
            pageShape.getString.return_value = 'Title'
        else:
            pageShape.getString.return_value = 'String'
        return pageShape

    def get_text_from_page_out_of_bound_test(self):
        """
        Test ImpressDocument.__get_text_from_page with out-of-bounds index
        """
        # GIVEN: mocked LibreoOffice Document with one slide, two notes and three texts
        self.doc.document = self._mock_a_LibreOffice_document(1,2,3)
        # WHEN: __get_text_from_page is called with an index of 0x00 (index is 1 based)
        result = self.doc._ImpressDocument__get_text_from_page(0,TextType.Notes)
        # THEN: the result should be an empty string
        assert result == '', 'Result should be an empty string'
        # WHEN: regardless of the type of text, index 0x00 is out of bounds
        result = self.doc._ImpressDocument__get_text_from_page(0,TextType.Title)
        # THEN: result should be an empty string
        assert result == '', 'Result should be an empty string'
        # WHEN: when called with 2, it should also be out of bounds
        result = self.doc._ImpressDocument__get_text_from_page(2,TextType.SlideText)
        # THEN: result should be an empty string ... and, getByIndex should have never been called
        assert result == '', 'Result should be an empty string'
        assert self.doc.document.getDrawPages().getByIndex.call_count == 0, 'There should be no call to getByIndex'

    def get_text_from_page_wrong_type_test(self):
        """
        Test ImpressDocument.__get_text_from_page with wrong TextType
        """
        # GIVEN: mocked LibreOffice Document with one slide, two notes and three texts
        self.doc.document = self._mock_a_LibreOffice_document(1,2,3)
        # WHEN: called with TextType 3
        result = self.doc._ImpressDocument__get_text_from_page(1,3)
        # THEN: result should be an empty string
        assert result == '', 'Result should be and empty string'
        assert self.doc.document.getDrawPages().getByIndex.call_count == 0, 'Theres should be no call to getByIndex'

    def get_text_from_page_valid_params_test(self):
        """
        Test ImpressDocument.__get_text_from_page with valid parameters
        """
        # GIVEN: mocked LibreOffice Document with one slide, two notes and three texts
        self.doc.document = self._mock_a_LibreOffice_document(1,2,3)
        # WHEN: __get_text_from_page is called to get the Notes
        result = self.doc._ImpressDocument__get_text_from_page(1,TextType.Notes)
        # THEN: result should be 'Note\nNote\n'
        assert result == 'Note\nNote\n', 'Result should be exactly \'Note\\n\' times the count of notes in the page'
        # WHEN: get the Title
        result = self.doc._ImpressDocument__get_text_from_page(1,TextType.Title)
        # THEN: result should be 'Title\n'
        assert result == 'Title\n', 'Result should be exactly \'Title\\n\''
        # WHEN: get all text
        result = self.doc._ImpressDocument__get_text_from_page(1,TextType.SlideText)
        # THEN: result should be 'Title\nString\nString\n'
        assert result == 'Title\nString\nString\n', 'Result should be exactly \'Title\\nString\\nString\\n\''
