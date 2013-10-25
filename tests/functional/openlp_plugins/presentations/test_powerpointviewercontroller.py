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
Functional tests to test the PptviewController class and related methods.
"""
from unittest import TestCase
import os
from mock import MagicMock, patch, mock_open
from openlp.plugins.presentations.lib.pptviewcontroller import PptviewController, PptviewDocument

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources'))

class TestLibModule(TestCase):

    def setUp(self):
        mocked_plugin = MagicMock()
        mocked_plugin.settings_section = 'presentations'
        self.ppc = PptviewController(mocked_plugin)
        self.file_name = os.path.join(TEST_PATH,"test.pptx")
        self.doc = PptviewDocument(self.ppc,self.file_name)

    #add _test to the function name to enable test
    def verify_installation(self):
        """
        Test the installation of PowerpointViewer
        """
        # GIVEN: A boolean value set to true
        # WHEN: We "convert" it to a bool
        isInstalled = self.ppc.check_available()
        # THEN: We should get back a True bool
        assert isInstalled is True, u'The result should be True'

    # add _test to the following if necessary to enable test
    # I don't have powerpointviewer to verify
    def verify_loading_document(self):
        """
        Test loading a document in PowerpointViewer
        """             
        # GIVEN: the filename
        print(self.file_name)
        # WHEN: loading the filename
        self.doc = PptviewDocument(self.ppc,self.file_name)
        self.doc.load_presentation()
        result = self.doc.is_loaded()
        # THEN: result should be true
        assert result is True, 'The result should be True'

    # disabled
    def verify_titles(self):
        """
        Test reading the titles from PowerpointViewer
        """
        # GIVEN:
        self.doc = PptviewDocument(self.ppc,self.file_name)
        self.doc.create_titles_and_notes()
        # WHEN reading the titles and notes
        titles,notes = self.doc.get_titles_and_notes()
        print("titles: ".join(titles))
        print("notes: ".join(notes))
        # THEN there should be exactly 5 titles and 5 notes
        assert len(titles)==5, 'There should be five titles'
        assert len(notes)==5, 'Theres should be five notes'

    def create_titles_and_notes_test(self):
        """
        Test PowerpointController.create_titles_and_notes
        """
        # GIVEN: mocked PresentationController.save_titles_and_notes 
        self.doc.save_titles_and_notes = MagicMock()
        # WHEN reading the titles and notes
        self.doc.create_titles_and_notes()
        # THEN save_titles_and_notes should have been called once with empty arrays
        self.doc.save_titles_and_notes.assert_called_once_with(['Test 1\n', '\n', 'Test 2\n', 'Test 4\n', 'Test 3\n'], ['Notes for slide 1', 'Inserted', 'Notes for slide 2', 'Notes \nfor slide 4', 'Notes for slide 3'])

    def create_titles_and_notes_nonexistent_file_test(self):
        """
        Test PowerpointController.create_titles_and_notes with nonexistent file
        """
        # GIVEN: mocked PresentationController.save_titles_and_notes and an nonexistent file
        with patch('builtins.open') as mocked_open, \
            patch('openlp.plugins.presentations.lib.pptviewcontroller.os.path.exists') as mocked_exists:
            mocked_exists.return_value = False
            self.doc = PptviewDocument(self.ppc,'Idontexist.pptx')
            self.doc.save_titles_and_notes = MagicMock()
            # WHEN: reading the titles and notes
            self.doc.create_titles_and_notes()
            # THEN:
            self.doc.save_titles_and_notes.assert_called_once_with(None,None)
            mocked_exists.assert_any_call('Idontexist.pptx')
        
    def create_titles_and_notes_invalid_file_test(self):
        """
        Test PowerpointController.create_titles_and_notes with invalid file
        """
        # GIVEN: mocked PresentationController.save_titles_and_notes and an invalid file
        with patch('builtins.open', mock_open(read_data='this is a test')) as mocked_open, \
             patch('openlp.plugins.presentations.lib.pptviewcontroller.os.path.exists') as mocked_exists, \
             patch('openlp.plugins.presentations.lib.pptviewcontroller.zipfile.is_zipfile') as mocked_is_zf:
            mocked_is_zf.return_value = False
            mocked_exists.return_value = True
            mocked_open.filesize = 10
            self.doc = PptviewDocument(self.ppc,os.path.join(TEST_PATH,"test.ppt"))
            self.doc.save_titles_and_notes = MagicMock()
            # WHEN: reading the titles and notes
            self.doc.create_titles_and_notes()
            # THEN:
            self.doc.save_titles_and_notes.assert_called_once_with(None,None)
            assert mocked_is_zf.call_count == 1
            