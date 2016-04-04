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
import os
from unittest import TestCase

from openlp.core.utils import clean_filename, delete_file, get_filesystem_encoding, \
    split_filename, _get_user_agent, get_web_page

from tests.functional import MagicMock, patch


class TestUtils(TestCase):
    """
    A test suite to test out various methods around the AppLocation class.
    """

    def get_filesystem_encoding_sys_function_not_called_test(self):
        """
        Test the get_filesystem_encoding() function does not call the sys.getdefaultencoding() function
        """
        # GIVEN: sys.getfilesystemencoding returns "cp1252"
        with patch('openlp.core.utils.sys.getfilesystemencoding') as mocked_getfilesystemencoding, \
                patch('openlp.core.utils.sys.getdefaultencoding') as mocked_getdefaultencoding:
            mocked_getfilesystemencoding.return_value = 'cp1252'

            # WHEN: get_filesystem_encoding() is called
            result = get_filesystem_encoding()

            # THEN: getdefaultencoding should have been called
            mocked_getfilesystemencoding.assert_called_with()
            self.assertEqual(0, mocked_getdefaultencoding.called, 'getdefaultencoding should not have been called')
            self.assertEqual('cp1252', result, 'The result should be "cp1252"')

    def get_filesystem_encoding_sys_function_is_called_test(self):
        """
        Test the get_filesystem_encoding() function calls the sys.getdefaultencoding() function
        """
        # GIVEN: sys.getfilesystemencoding returns None and sys.getdefaultencoding returns "utf-8"
        with patch('openlp.core.utils.sys.getfilesystemencoding') as mocked_getfilesystemencoding, \
                patch('openlp.core.utils.sys.getdefaultencoding') as mocked_getdefaultencoding:
            mocked_getfilesystemencoding.return_value = None
            mocked_getdefaultencoding.return_value = 'utf-8'

            # WHEN: get_filesystem_encoding() is called
            result = get_filesystem_encoding()

            # THEN: getdefaultencoding should have been called
            mocked_getfilesystemencoding.assert_called_with()
            mocked_getdefaultencoding.assert_called_with()
            self.assertEqual('utf-8', result, 'The result should be "utf-8"')

    def split_filename_with_file_path_test(self):
        """
        Test the split_filename() function with a path to a file
        """
        # GIVEN: A path to a file.
        if os.name == 'nt':
            file_path = 'C:\\home\\user\\myfile.txt'
            wanted_result = ('C:\\home\\user', 'myfile.txt')
        else:
            file_path = '/home/user/myfile.txt'
            wanted_result = ('/home/user', 'myfile.txt')
        with patch('openlp.core.utils.os.path.isfile') as mocked_is_file:
            mocked_is_file.return_value = True

            # WHEN: Split the file name.
            result = split_filename(file_path)

            # THEN: A tuple should be returned.
            self.assertEqual(wanted_result, result, 'A tuple with the dir and file name should have been returned')

    def split_filename_with_dir_path_test(self):
        """
        Test the split_filename() function with a path to a directory
        """
        # GIVEN: A path to a dir.
        if os.name == 'nt':
            file_path = 'C:\\home\\user\\mydir'
            wanted_result = ('C:\\home\\user\\mydir', '')
        else:
            file_path = '/home/user/mydir'
            wanted_result = ('/home/user/mydir', '')
        with patch('openlp.core.utils.os.path.isfile') as mocked_is_file:
            mocked_is_file.return_value = False

            # WHEN: Split the file name.
            result = split_filename(file_path)

            # THEN: A tuple should be returned.
            self.assertEqual(wanted_result, result,
                             'A two-entry tuple with the directory and file name (empty) should have been returned.')

    def clean_filename_test(self):
        """
        Test the clean_filename() function
        """
        # GIVEN: A invalid file name and the valid file name.
        invalid_name = 'A_file_with_invalid_characters_[\\/:\*\?"<>\|\+\[\]%].py'
        wanted_name = 'A_file_with_invalid_characters______________________.py'

        # WHEN: Clean the name.
        result = clean_filename(invalid_name)

        # THEN: The file name should be cleaned.
        self.assertEqual(wanted_name, result, 'The file name should not contain any special characters.')

    def delete_file_no_path_test(self):
        """
        Test the delete_file function when called with out a valid path
        """
        # GIVEN: A blank path
        # WEHN: Calling delete_file
        result = delete_file('')

        # THEN: delete_file should return False
        self.assertFalse(result, "delete_file should return False when called with ''")

    def delete_file_path_success_test(self):
        """
        Test the delete_file function when it successfully deletes a file
        """
        # GIVEN: A mocked os which returns True when os.path.exists is called
        with patch('openlp.core.utils.os', **{'path.exists.return_value': False}):

            # WHEN: Calling delete_file with a file path
            result = delete_file('path/file.ext')

            # THEN: delete_file should return True
            self.assertTrue(result, 'delete_file should return True when it successfully deletes a file')

    def delete_file_path_no_file_exists_test(self):
        """
        Test the delete_file function when the file to remove does not exist
        """
        # GIVEN: A mocked os which returns False when os.path.exists is called
        with patch('openlp.core.utils.os', **{'path.exists.return_value': False}):

            # WHEN: Calling delete_file with a file path
            result = delete_file('path/file.ext')

            # THEN: delete_file should return True
            self.assertTrue(result, 'delete_file should return True when the file doesnt exist')

    def delete_file_path_exception_test(self):
        """
        Test the delete_file function when os.remove raises an exception
        """
        # GIVEN: A mocked os which returns True when os.path.exists is called and raises an OSError when os.remove is
        #       called.
        with patch('openlp.core.utils.os', **{'path.exists.return_value': True, 'path.exists.side_effect': OSError}), \
                patch('openlp.core.utils.log') as mocked_log:

            # WHEN: Calling delete_file with a file path
            result = delete_file('path/file.ext')

            # THEN: delete_file should log and exception and return False
            self.assertEqual(mocked_log.exception.call_count, 1)
            self.assertFalse(result, 'delete_file should return False when os.remove raises an OSError')

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
                patch('openlp.core.common.Registry') as MockRegistry:
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
