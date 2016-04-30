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
This module contains tests for the lib submodule of the Presentations plugin.
"""
from unittest import TestCase

from openlp.core.common import Registry
from openlp.plugins.bibles.lib.mediaitem import BibleMediaItem
from tests.functional import MagicMock, patch
from tests.helpers.testmixin import TestMixin


class TestMediaItem(TestCase, TestMixin):
    """
    Test the bible mediaitem methods.
    """

    def setUp(self):
        """
        Set up the components need for all tests.
        """
        with patch('openlp.plugins.bibles.lib.mediaitem.MediaManagerItem._setup'),\
                patch('openlp.plugins.bibles.lib.mediaitem.BibleMediaItem.setup_item'):
            self.media_item = BibleMediaItem(None, MagicMock())
        self.setup_application()
        self.mocked_main_window = MagicMock()
        Registry.create()
        Registry().register('main_window', self.mocked_main_window)

    def display_results_no_results_test(self):
        """
        Test the display_results method when called with a single bible, returning no results
        """

        # GIVEN: A mocked build_display_results which returns an empty list
        with patch('openlp.plugins.bibles.lib.BibleMediaItem.build_display_results', **{'return_value': []}) \
                as mocked_build_display_results:
            mocked_list_view = MagicMock()
            self.media_item.search_results = 'results'
            self.media_item.list_view = mocked_list_view

            # WHEN: Calling display_results with a single bible version
            self.media_item.display_results('NIV')

            # THEN: No items should be added to the list, and select all should have been called.
            mocked_build_display_results.assert_called_once_with('NIV', '', 'results')
            self.assertFalse(mocked_list_view.addItem.called)
            mocked_list_view.selectAll.assert_called_once_with()
            self.assertEqual(self.media_item.search_results, {})
            self.assertEqual(self.media_item.second_search_results, {})

    def display_results_two_bibles_no_results_test(self):
        """
        Test the display_results method when called with two bibles, returning no results
        """

        # GIVEN: A mocked build_display_results which returns an empty list
        with patch('openlp.plugins.bibles.lib.BibleMediaItem.build_display_results', **{'return_value': []}) \
                as mocked_build_display_results:
            mocked_list_view = MagicMock()
            self.media_item.search_results = 'results'
            self.media_item.list_view = mocked_list_view

            # WHEN: Calling display_results with two single bible versions
            self.media_item.display_results('NIV', 'GNB')

            # THEN: build_display_results should have been called with two bible versions.
            #       No items should be added to the list, and select all should have been called.
            mocked_build_display_results.assert_called_once_with('NIV', 'GNB', 'results')
            self.assertFalse(mocked_list_view.addItem.called)
            mocked_list_view.selectAll.assert_called_once_with()
            self.assertEqual(self.media_item.search_results, {})
            self.assertEqual(self.media_item.second_search_results, {})

    def display_results_returns_lots_of_results_test_test(self):
            """
            Test the display_results method a large number of results (> 100) are returned
            """

            # GIVEN: A mocked build_display_results which returns a large list of results
            long_list = list(range(100))
            with patch('openlp.plugins.bibles.lib.BibleMediaItem.build_display_results', **{'return_value': long_list})\
                    as mocked_build_display_results:
                mocked_list_view = MagicMock()
                self.media_item.search_results = 'results'
                self.media_item.list_view = mocked_list_view

                # WHEN: Calling display_results
                self.media_item.display_results('NIV', 'GNB')

                # THEN: addItem should have been called 100 times, and the lsit items should not be selected.
                mocked_build_display_results.assert_called_once_with('NIV', 'GNB', 'results')
                self.assertEqual(mocked_list_view.addItem.call_count, 100)
                mocked_list_view.selectAll.assert_called_once_with()
                self.assertEqual(self.media_item.search_results, {})
                self.assertEqual(self.media_item.second_search_results, {})

    def on_quick_search_button_general_test(self):
        """
        Test that general things, which should be called on all Quick searches are called.
        """

        # GIVEN: self.application as self.app, all the required functions
        Registry.create()
        Registry().register('application', self.app)
        self.media_item.quickSearchButton = MagicMock()
        self.app.process_events = MagicMock()
        self.media_item.quickVersionComboBox = MagicMock()
        self.media_item.quickVersionComboBox.currentText = MagicMock()
        self.media_item.quickSecondComboBox = MagicMock()
        self.media_item.quickSecondComboBox.currentText = MagicMock()
        self.media_item.quick_search_edit = MagicMock()
        self.media_item.quick_search_edit.text = MagicMock()
        self.media_item.quickLockButton = MagicMock()
        self.media_item.list_view = MagicMock()
        self.media_item.search_results = MagicMock()
        self.media_item.display_results = MagicMock()
        self.media_item.check_search_result = MagicMock()
        self.app.set_normal_cursor = MagicMock()

        # WHEN: on_quick_search_button is called
        self.media_item.on_quick_search_button()

        # THEN: Search should had been started and finalized properly
        self.assertEqual(1, self.app.process_events.call_count, 'Normal cursor should had been called once')
        self.assertEqual(1, self.media_item.quickVersionComboBox.currentText.call_count, 'Should had been called once')
        self.assertEqual(1, self.media_item.quickSecondComboBox.currentText.call_count, 'Should had been called once')
        self.assertEqual(1, self.media_item.quick_search_edit.text.call_count, 'Text edit Should had been called once')
        self.assertEqual(1, self.media_item.quickLockButton.isChecked.call_count, 'Lock Should had been called once')
        self.assertEqual(1, self.media_item.display_results.call_count, 'Display results Should had been called once')
        self.assertEqual(2, self.media_item.quickSearchButton.setEnabled.call_count, 'Disable and Enable the button')
        self.assertEqual(1, self.media_item.check_search_result.call_count, 'Check results Should had been called once')
        self.assertEqual(1, self.app.set_normal_cursor.call_count, 'Normal cursor should had been called once')
