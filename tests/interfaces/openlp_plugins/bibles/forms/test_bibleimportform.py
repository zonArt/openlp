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
Package to test the openlp.plugins.bibles.forms.bibleimportform package.
"""
from unittest import TestCase

from PyQt5 import QtWidgets

from openlp.core.common import Registry
import openlp.plugins.bibles.forms.bibleimportform as bibleimportform

from tests.helpers.testmixin import TestMixin
from tests.functional import MagicMock, patch


class TestBibleImportForm(TestCase, TestMixin):
    """
    Test the BibleImportForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        bibleimportform.PYSWORD_AVAILABLE = False
        self.form = bibleimportform.BibleImportForm(self.main_window, MagicMock(), MagicMock())

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    @patch('openlp.plugins.bibles.forms.bibleimportform.CWExtract.get_bibles_from_http')
    @patch('openlp.plugins.bibles.forms.bibleimportform.BGExtract.get_bibles_from_http')
    @patch('openlp.plugins.bibles.forms.bibleimportform.BSExtract.get_bibles_from_http')
    def on_web_update_button_clicked_test(self, mocked_bsextract, mocked_bgextract, mocked_cwextract):
        """
        Test that on_web_update_button_clicked handles problems correctly
        """
        # GIVEN: Some mocked GUI components and mocked bibleextractors
        self.form.web_source_combo_box = MagicMock()
        self.form.web_translation_combo_box = MagicMock()
        self.form.web_update_button = MagicMock()
        self.form.web_progress_bar = MagicMock()
        mocked_bsextract.return_value = None
        mocked_bgextract.return_value = None
        mocked_cwextract.return_value = None

        # WHEN: Running on_web_update_button_clicked
        self.form.on_web_update_button_clicked()

        # THEN: The webbible list should still be empty
        self.assertEqual(self.form.web_bible_list, {}, 'The webbible list should be empty')

    def custom_init_test(self):
        """
        Test that custom_init works as expected if pysword is unavailable
        """
        # GIVEN: A mocked sword_tab_widget
        self.form.sword_tab_widget = MagicMock()

        # WHEN: Running custom_init
        self.form.custom_init()

        # THEN: sword_tab_widget.setDisabled(True) should have been called
        self.form.sword_tab_widget.setDisabled.assert_called_with(True)
