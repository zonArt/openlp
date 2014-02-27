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
This module contains tests for the CCLI SongSelect importer.
"""
from unittest import TestCase

from openlp.plugins.songs.lib.songselect import SongSelectImport, LOGIN_URL, LOGOUT_URL, BASE_URL

from tests.functional import MagicMock, patch


class TestSongSelect(TestCase):
    """
    Test the :class:`~openlp.plugins.songs.lib.songselect.SongSelectImport` class
    """
    def constructor_test(self):
        """
        Test that constructing a basic SongSelectImport object works correctly
        """
        # GIVEN: The SongSelectImporter class and a mocked out build_opener
        with patch('openlp.plugins.songs.lib.songselect.build_opener') as mocked_build_opener:
            # WHEN: An object is instantiated
            importer = SongSelectImport(None)

            # THEN: The object should have the correct properties
            self.assertIsNone(importer.db_manager, 'The db_manager should be None')
            self.assertIsNotNone(importer.html_parser, 'There should be a valid html_parser object')
            self.assertIsNotNone(importer.opener, 'There should be a valid opener object')
            self.assertEqual(1, mocked_build_opener.call_count, 'The build_opener method should have been called once')

    def login_fails_test(self):
        """
        Test that when logging in to SongSelect fails, the login method returns False
        """
        # GIVEN: A bunch of mocked out stuff and an importer object
        with patch('openlp.plugins.songs.lib.songselect.build_opener') as mocked_build_opener, \
                patch('openlp.plugins.songs.lib.songselect.BeautifulSoup') as MockedBeautifulSoup:
            mocked_opener = MagicMock()
            mocked_build_opener.return_value = mocked_opener
            mocked_login_page = MagicMock()
            mocked_login_page.find.return_value = {'value': 'blah'}
            MockedBeautifulSoup.return_value = mocked_login_page
            mock_callback = MagicMock()
            importer = SongSelectImport(None)

            # WHEN: The login method is called after being rigged to fail
            result = importer.login('username', 'password', mock_callback)

            # THEN: callback was called 3 times, open was called twice, find was called twice, and False was returned
            self.assertEqual(3, mock_callback.call_count, 'callback should have been called 3 times')
            self.assertEqual(2, mocked_login_page.find.call_count, 'find should have been called twice')
            self.assertEqual(2, mocked_opener.open.call_count, 'opener should have been called twice')
            self.assertFalse(result, 'The login method should have returned False')

    def login_succeeds_test(self):
        """
        Test that when logging in to SongSelect succeeds, the login method returns True
        """
        # GIVEN: A bunch of mocked out stuff and an importer object
        with patch('openlp.plugins.songs.lib.songselect.build_opener') as mocked_build_opener, \
                patch('openlp.plugins.songs.lib.songselect.BeautifulSoup') as MockedBeautifulSoup:
            mocked_opener = MagicMock()
            mocked_build_opener.return_value = mocked_opener
            mocked_login_page = MagicMock()
            mocked_login_page.find.side_effect = [{'value': 'blah'}, None]
            MockedBeautifulSoup.return_value = mocked_login_page
            mock_callback = MagicMock()
            importer = SongSelectImport(None)

            # WHEN: The login method is called after being rigged to fail
            result = importer.login('username', 'password', mock_callback)

            # THEN: callback was called 3 times, open was called twice, find was called twice, and True was returned
            self.assertEqual(3, mock_callback.call_count, 'callback should have been called 3 times')
            self.assertEqual(2, mocked_login_page.find.call_count, 'find should have been called twice')
            self.assertEqual(2, mocked_opener.open.call_count, 'opener should have been called twice')
            self.assertTrue(result, 'The login method should have returned True')

    def logout_test(self):
        """
        Test that when the logout method is called, it logs the user out of SongSelect
        """
        # GIVEN: A bunch of mocked out stuff and an importer object
        with patch('openlp.plugins.songs.lib.songselect.build_opener') as mocked_build_opener:
            mocked_opener = MagicMock()
            mocked_build_opener.return_value = mocked_opener
            importer = SongSelectImport(None)

            # WHEN: The login method is called after being rigged to fail
            importer.logout()

            # THEN: The opener is called once with the logout url
            self.assertEqual(1, mocked_opener.open.call_count, 'opener should have been called once')
            mocked_opener.open.assert_called_with(LOGOUT_URL)

    def search_returns_no_results_test(self):
        """
        Test that when the search finds no results, it simply returns an empty list
        """
        # GIVEN: A bunch of mocked out stuff and an importer object
        with patch('openlp.plugins.songs.lib.songselect.build_opener') as mocked_build_opener, patch(
                'openlp.plugins.songs.lib.songselect.BeautifulSoup') as MockedBeautifulSoup:
            mocked_opener = MagicMock()
            mocked_build_opener.return_value = mocked_opener
            mocked_results_page = MagicMock()
            mocked_results_page.find_all.return_value = []
            MockedBeautifulSoup.return_value = mocked_results_page
            mock_callback = MagicMock()
            importer = SongSelectImport(None)

            # WHEN: The login method is called after being rigged to fail
            results = importer.search('text', 1000, mock_callback)

            # THEN: callback was never called, open was called once, find_all was called once, an empty list returned
            self.assertEqual(0, mock_callback.call_count, 'callback should not have been called')
            self.assertEqual(1, mocked_opener.open.call_count, 'open should have been called once')
            self.assertEqual(1, mocked_results_page.find_all.call_count, 'find_all should have been called once')
            mocked_results_page.find_all.assert_called_with('li', 'result pane')
            self.assertEqual([], results, 'The search method should have returned an empty list')

    def search_returns_two_results_test(self):
        """
        Test that when the search finds 2 results, it simply returns a list with 2 results
        """
        # GIVEN: A bunch of mocked out stuff and an importer object
        with patch('openlp.plugins.songs.lib.songselect.build_opener') as mocked_build_opener, patch(
                'openlp.plugins.songs.lib.songselect.BeautifulSoup') as MockedBeautifulSoup:
            # first search result
            mocked_result1 = MagicMock()
            mocked_result1.find.side_effect = [MagicMock(string='Title 1'), {'href': '/url1'}]
            mocked_result1.find_all.return_value = [MagicMock(string='Author 1-1'), MagicMock(string='Author 1-2')]
            # second search result
            mocked_result2 = MagicMock()
            mocked_result2.find.side_effect = [MagicMock(string='Title 2'), {'href': '/url2'}]
            mocked_result2.find_all.return_value = [MagicMock(string='Author 2-1'), MagicMock(string='Author 2-2')]
            # rest of the stuff
            mocked_opener = MagicMock()
            mocked_build_opener.return_value = mocked_opener
            mocked_results_page = MagicMock()
            mocked_results_page.find_all.side_effect = [[mocked_result1, mocked_result2], []]
            MockedBeautifulSoup.return_value = mocked_results_page
            mock_callback = MagicMock()
            importer = SongSelectImport(None)

            # WHEN: The login method is called after being rigged to fail
            results = importer.search('text', 1000, mock_callback)

            # THEN: callback was never called, open was called once, find_all was called once, an empty list returned
            self.assertEqual(2, mock_callback.call_count, 'callback should have been called twice')
            self.assertEqual(2, mocked_opener.open.call_count, 'open should have been called twice')
            self.assertEqual(2, mocked_results_page.find_all.call_count, 'find_all should have been called twice')
            mocked_results_page.find_all.assert_called_with('li', 'result pane')
            expected_list = [
                {'title': 'Title 1', 'authors': ['Author 1-1', 'Author 1-2'], 'link': BASE_URL + '/url1'},
                {'title': 'Title 2', 'authors': ['Author 2-1', 'Author 2-2'], 'link': BASE_URL + '/url2'}
            ]
            self.assertListEqual(expected_list, results, 'The search method should have returned two songs')

    def search_reaches_max_results_test(self):
        """
        Test that when the search finds MAX (2) results, it simply returns a list with those (2)
        """
        # GIVEN: A bunch of mocked out stuff and an importer object
        with patch('openlp.plugins.songs.lib.songselect.build_opener') as mocked_build_opener, patch(
                'openlp.plugins.songs.lib.songselect.BeautifulSoup') as MockedBeautifulSoup:
            # first search result
            mocked_result1 = MagicMock()
            mocked_result1.find.side_effect = [MagicMock(string='Title 1'), {'href': '/url1'}]
            mocked_result1.find_all.return_value = [MagicMock(string='Author 1-1'), MagicMock(string='Author 1-2')]
            # second search result
            mocked_result2 = MagicMock()
            mocked_result2.find.side_effect = [MagicMock(string='Title 2'), {'href': '/url2'}]
            mocked_result2.find_all.return_value = [MagicMock(string='Author 2-1'), MagicMock(string='Author 2-2')]
            # third search result
            mocked_result3 = MagicMock()
            mocked_result3.find.side_effect = [MagicMock(string='Title 3'), {'href': '/url3'}]
            mocked_result3.find_all.return_value = [MagicMock(string='Author 3-1'), MagicMock(string='Author 3-2')]
            # rest of the stuff
            mocked_opener = MagicMock()
            mocked_build_opener.return_value = mocked_opener
            mocked_results_page = MagicMock()
            mocked_results_page.find_all.side_effect = [[mocked_result1, mocked_result2, mocked_result3], []]
            MockedBeautifulSoup.return_value = mocked_results_page
            mock_callback = MagicMock()
            importer = SongSelectImport(None)

            # WHEN: The login method is called after being rigged to fail
            results = importer.search('text', 2, mock_callback)

            # THEN: callback was never called, open was called once, find_all was called once, an empty list returned
            self.assertEqual(2, mock_callback.call_count, 'callback should have been called twice')
            self.assertEqual(2, mocked_opener.open.call_count, 'open should have been called twice')
            self.assertEqual(2, mocked_results_page.find_all.call_count, 'find_all should have been called twice')
            mocked_results_page.find_all.assert_called_with('li', 'result pane')
            expected_list = [{'title': 'Title 1', 'authors': ['Author 1-1', 'Author 1-2'], 'link': BASE_URL + '/url1'},
                             {'title': 'Title 2', 'authors': ['Author 2-1', 'Author 2-2'], 'link': BASE_URL + '/url2'}]
            self.assertListEqual(expected_list, results, 'The search method should have returned two songs')
