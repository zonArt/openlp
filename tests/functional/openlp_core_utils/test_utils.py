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
Functional tests to test the AppLocation class and related methods.
"""
from unittest import TestCase

from openlp.core.utils import _get_user_agent, get_web_page

from tests.functional import MagicMock, patch


class TestUtils(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """
    def get_user_agent_linux_test(self):
        """
        Test that getting a user agent on Linux returns a user agent suitable for Linux
        """
        with patch('openlp.core.utils.sys') as mocked_sys:

            # GIVEN: The system is Linux
            mocked_sys.platform = 'linux2'

            # WHEN: We call _get_user_agent()
            user_agent = _get_user_agent()

            # THEN: The user agent is a Linux (or ChromeOS) user agent
            result = 'Linux' in user_agent or 'CrOS' in user_agent
            self.assertTrue(result, 'The user agent should be a valid Linux user agent')

    def get_user_agent_windows_test(self):
        """
        Test that getting a user agent on Windows returns a user agent suitable for Windows
        """
        with patch('openlp.core.utils.sys') as mocked_sys:

            # GIVEN: The system is Linux
            mocked_sys.platform = 'win32'

            # WHEN: We call _get_user_agent()
            user_agent = _get_user_agent()

            # THEN: The user agent is a Linux (or ChromeOS) user agent
            self.assertIn('Windows', user_agent, 'The user agent should be a valid Windows user agent')

    def get_user_agent_macos_test(self):
        """
        Test that getting a user agent on OS X returns a user agent suitable for OS X
        """
        with patch('openlp.core.utils.sys') as mocked_sys:

            # GIVEN: The system is Linux
            mocked_sys.platform = 'darwin'

            # WHEN: We call _get_user_agent()
            user_agent = _get_user_agent()

            # THEN: The user agent is a Linux (or ChromeOS) user agent
            self.assertIn('Mac OS X', user_agent, 'The user agent should be a valid OS X user agent')

    def get_user_agent_default_test(self):
        """
        Test that getting a user agent on a non-Linux/Windows/OS X platform returns the default user agent
        """
        with patch('openlp.core.utils.sys') as mocked_sys:

            # GIVEN: The system is Linux
            mocked_sys.platform = 'freebsd'

            # WHEN: We call _get_user_agent()
            user_agent = _get_user_agent()

            # THEN: The user agent is a Linux (or ChromeOS) user agent
            self.assertIn('NetBSD', user_agent, 'The user agent should be the default user agent')

    def get_web_page_no_url_test(self):
        """
        Test that sending a URL of None to the get_web_page method returns None
        """
        # GIVEN: A None url
        test_url = None

        # WHEN: We try to get the test URL
        result = get_web_page(test_url)

        # THEN: None should be returned
        self.assertIsNone(result, 'The return value of get_web_page should be None')

    def get_web_page_test(self):
        """
        Test that the get_web_page method works correctly
        """
        with patch('openlp.core.utils.urllib.request.Request') as MockRequest, \
                patch('openlp.core.utils.urllib.request.urlopen') as mock_urlopen, \
                patch('openlp.core.utils._get_user_agent') as mock_get_user_agent, \
                patch('openlp.core.common.Registry') as MockRegistry:
            # GIVEN: Mocked out objects and a fake URL
            mocked_request_object = MagicMock()
            MockRequest.return_value = mocked_request_object
            mocked_page_object = MagicMock()
            mock_urlopen.return_value = mocked_page_object
            mock_get_user_agent.return_value = 'user_agent'
            fake_url = 'this://is.a.fake/url'

            # WHEN: The get_web_page() method is called
            returned_page = get_web_page(fake_url)

            # THEN: The correct methods are called with the correct arguments and a web page is returned
            MockRequest.assert_called_with(fake_url)
            mocked_request_object.add_header.assert_called_with('User-Agent', 'user_agent')
            self.assertEqual(1, mocked_request_object.add_header.call_count,
                             'There should only be 1 call to add_header')
            mock_get_user_agent.assert_called_with()
            mock_urlopen.assert_called_with(mocked_request_object, timeout=30)
            mocked_page_object.geturl.assert_called_with()
            self.assertEqual(0, MockRegistry.call_count, 'The Registry() object should have never been called')
            self.assertEqual(mocked_page_object, returned_page, 'The returned page should be the mock object')

    def get_web_page_with_header_test(self):
        """
        Test that adding a header to the call to get_web_page() adds the header to the request
        """
        with patch('openlp.core.utils.urllib.request.Request') as MockRequest, \
                patch('openlp.core.utils.urllib.request.urlopen') as mock_urlopen, \
                patch('openlp.core.utils._get_user_agent') as mock_get_user_agent:
            # GIVEN: Mocked out objects, a fake URL and a fake header
            mocked_request_object = MagicMock()
            MockRequest.return_value = mocked_request_object
            mocked_page_object = MagicMock()
            mock_urlopen.return_value = mocked_page_object
            mock_get_user_agent.return_value = 'user_agent'
            fake_url = 'this://is.a.fake/url'
            fake_header = ('Fake-Header', 'fake value')

            # WHEN: The get_web_page() method is called
            returned_page = get_web_page(fake_url, header=fake_header)

            # THEN: The correct methods are called with the correct arguments and a web page is returned
            MockRequest.assert_called_with(fake_url)
            mocked_request_object.add_header.assert_called_with(fake_header[0], fake_header[1])
            self.assertEqual(2, mocked_request_object.add_header.call_count,
                             'There should only be 2 calls to add_header')
            mock_get_user_agent.assert_called_with()
            mock_urlopen.assert_called_with(mocked_request_object, timeout=30)
            mocked_page_object.geturl.assert_called_with()
            self.assertEqual(mocked_page_object, returned_page, 'The returned page should be the mock object')

    def get_web_page_with_user_agent_in_headers_test(self):
        """
        Test that adding a user agent in the header when calling get_web_page() adds that user agent to the request
        """
        with patch('openlp.core.utils.urllib.request.Request') as MockRequest, \
                patch('openlp.core.utils.urllib.request.urlopen') as mock_urlopen, \
                patch('openlp.core.utils._get_user_agent') as mock_get_user_agent:
            # GIVEN: Mocked out objects, a fake URL and a fake header
            mocked_request_object = MagicMock()
            MockRequest.return_value = mocked_request_object
            mocked_page_object = MagicMock()
            mock_urlopen.return_value = mocked_page_object
            fake_url = 'this://is.a.fake/url'
            user_agent_header = ('User-Agent', 'OpenLP/2.2.0')

            # WHEN: The get_web_page() method is called
            returned_page = get_web_page(fake_url, header=user_agent_header)

            # THEN: The correct methods are called with the correct arguments and a web page is returned
            MockRequest.assert_called_with(fake_url)
            mocked_request_object.add_header.assert_called_with(user_agent_header[0], user_agent_header[1])
            self.assertEqual(1, mocked_request_object.add_header.call_count,
                             'There should only be 1 call to add_header')
            self.assertEqual(0, mock_get_user_agent.call_count, '_get_user_agent should not have been called')
            mock_urlopen.assert_called_with(mocked_request_object, timeout=30)
            mocked_page_object.geturl.assert_called_with()
            self.assertEqual(mocked_page_object, returned_page, 'The returned page should be the mock object')

    def get_web_page_update_openlp_test(self):
        """
        Test that passing "update_openlp" as true to get_web_page calls Registry().get('app').process_events()
        """
        with patch('openlp.core.utils.urllib.request.Request') as MockRequest, \
                patch('openlp.core.utils.urllib.request.urlopen') as mock_urlopen, \
                patch('openlp.core.utils._get_user_agent') as mock_get_user_agent, \
                patch('openlp.core.utils.Registry') as MockRegistry:
            # GIVEN: Mocked out objects, a fake URL
            mocked_request_object = MagicMock()
            MockRequest.return_value = mocked_request_object
            mocked_page_object = MagicMock()
            mock_urlopen.return_value = mocked_page_object
            mock_get_user_agent.return_value = 'user_agent'
            mocked_registry_object = MagicMock()
            mocked_application_object = MagicMock()
            mocked_registry_object.get.return_value = mocked_application_object
            MockRegistry.return_value = mocked_registry_object
            fake_url = 'this://is.a.fake/url'

            # WHEN: The get_web_page() method is called
            returned_page = get_web_page(fake_url, update_openlp=True)

            # THEN: The correct methods are called with the correct arguments and a web page is returned
            MockRequest.assert_called_with(fake_url)
            mocked_request_object.add_header.assert_called_with('User-Agent', 'user_agent')
            self.assertEqual(1, mocked_request_object.add_header.call_count,
                             'There should only be 1 call to add_header')
            mock_urlopen.assert_called_with(mocked_request_object, timeout=30)
            mocked_page_object.geturl.assert_called_with()
            mocked_registry_object.get.assert_called_with('application')
            mocked_application_object.process_events.assert_called_with()
            self.assertEqual(mocked_page_object, returned_page, 'The returned page should be the mock object')
