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
Functional tests to test the PowerPointController class and related methods.
"""
from unittest import TestCase
import os
from mock import MagicMock, patch
from openlp.plugins.presentations.lib.powerpointcontroller import PowerpointController, PowerpointDocument

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources'))

class TestLibModule(TestCase):

    def setUp(self):
        mocked_plugin = MagicMock()
        mocked_plugin.settings_section = 'presentations'
        self.ppc = PowerpointController(mocked_plugin)
        self.file_name = os.path.join(TEST_PATH,"test.pptx")
        self.doc = PowerpointDocument(self.ppc,self.file_name)
        self.doc.presentation_deleted()
        
    def verify_installation_test(self):
        """
        Test the installation of Powerpoint
        """
        # GIVEN: A boolean value set to true
        # WHEN: We "convert" it to a bool
        isInstalled = self.ppc.check_available()
        # THEN: We should get back a True bool
        assert isInstalled is True, u'The result should be True'

    # add _test to the following if necessary
    def verify_loading_document(self):
        """
        Test loading a document in PowerPoint
        """             
        # GIVEN: the filename
        print(self.file_name)
        # WHEN: loading the filename
        self.doc = PowerpointDocument(self.ppc,self.file_name)
        self.doc.load_presentation()
        result = self.doc.is_loaded()
        # THEN: result should be true
        assert result is True, u'The result should be True'

    def verify_titles_test(self):
        """
        Test reading the titles from PowerPoint
        """
        # GIVEN:
        self.doc = PowerpointDocument(self.ppc,self.file_name)
        self.doc.load_presentation()
        self.doc.create_titles_and_notes()
        #self.doc.load_presentation()
        # WHEN reading the titles and notes
        titles,notes = self.doc.get_titles_and_notes()
        print("titles: ".join(titles))
        print("notes: ".join(notes))
        # THEN there should be exactly 5 titles and 5 notes
        assert len(titles)==5, u'There should be five titles'
        assert len(notes)==5, u'Theres should be five notes'
        