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

from openlp.core.common import Registry, Settings
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

    def on_quick_reference_search_test(self):
        """
        BOOM BOOM BANANAS
        """

        # GIVEN: A mocked build_display_results which returns an empty list
        self.media_item.quickVersionComboBox = MagicMock()
        self.media_item.quickSecondComboBox = MagicMock()
        self.media_item.quick_search_edit = MagicMock()

        #mocked_text = self.media_item()
        #mocked_text.text.return_value = 'Gen. 1'
        #self.media_item.text = mocked_text
        #self.media_item.text.return_value = 'Gen. 1'
        # self.mocked_main_window.information_message = MagicMock()

        self.media_item.search_results = MagicMock()
        self.media_item.advancedSearchButton = MagicMock()
        self.media_item.advancedSearchButton.setEnabled = MagicMock()

        # WHEN: Calling display_results with a single bible version
        self.media_item.banana()

        # THEN: No items should be added to the list, and select all should have been called.
        # self.assertEqual(0, self.mocked_main_window.information_message, 'lama')
        # mocked_media_item.assert_called_with(mocked_main_window.information_message)
        # self.mocked_text.text.assert_called_with('Gen. 1')
        # mocked_process_item.assert_called_once_with(mocked_item, 7)
        self.media_item.advancedSearchButton.setEnabled.assert_called_once_with(True)


    """
    def on_quick_reference_search_test(self):

        Test the display_results method a large number of results (> 100) are returned


        # GIVEN: A mocked build_display_results which returns a large list of results
        media_item = BibleMediaItem(MagicMock)

        # WHEN: Calling display_results
        #self.media_item.on_quick_reference_search()

        # THEN: addItem should have been called 100 times, and the lsit items should not be selected.
    """