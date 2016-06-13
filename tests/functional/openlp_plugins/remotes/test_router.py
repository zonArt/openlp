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
This module contains tests for the lib submodule of the Remotes plugin.
"""
import os
import urllib.request
from unittest import TestCase

from openlp.core.common import Settings, Registry
from openlp.core.ui import ServiceManager
from openlp.plugins.remotes.lib.httpserver import HttpRouter
from tests.functional import MagicMock, patch, mock_open
from tests.helpers.testmixin import TestMixin

__default_settings__ = {
    'remotes/twelve hour': True,
    'remotes/port': 4316,
    'remotes/https port': 4317,
    'remotes/https enabled': False,
    'remotes/user id': 'openlp',
    'remotes/password': 'password',
    'remotes/authentication enabled': False,
    'remotes/ip address': '0.0.0.0'
}

TEST_PATH = os.path.abspath(os.path.dirname(__file__))


class TestRouter(TestCase, TestMixin):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.build_settings()
        Settings().extend_default_settings(__default_settings__)
        self.service_manager = ServiceManager()
        self.router = HttpRouter()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.destroy_settings()

    def test_password_encrypter(self):
        """
        Test hash userid and password function
        """
        # GIVEN: A default configuration
        Settings().setValue('remotes/user id', 'openlp')
        Settings().setValue('remotes/password', 'password')

        # WHEN: called with the defined userid
        router = HttpRouter()
        router.initialise()
        test_value = 'b3BlbmxwOnBhc3N3b3Jk'

        # THEN: the function should return the correct password
        self.assertEqual(router.auth, test_value,
                         'The result for make_sha_hash should return the correct encrypted password')

    def test_process_http_request(self):
        """
        Test the router control functionality
        """
        # GIVEN: A testing set of Routes
        mocked_function = MagicMock()
        test_route = [
            (r'^/stage/api/poll$', {'function': mocked_function, 'secure': False}),
        ]
        self.router.routes = test_route
        self.router.command = 'GET'

        # WHEN: called with a poll route
        function, args = self.router.process_http_request('/stage/api/poll', None)

        # THEN: the function should have been called only once
        self.assertEqual(mocked_function, function['function'], 'The mocked function should match defined value.')
        self.assertFalse(function['secure'], 'The mocked function should not require any security.')

    def test_process_secure_http_request(self):
        """
        Test the router control functionality
        """
        # GIVEN: A testing set of Routes
        mocked_function = MagicMock()
        test_route = [
            (r'^/stage/api/poll$', {'function': mocked_function, 'secure': True}),
        ]
        self.router.routes = test_route
        self.router.settings_section = 'remotes'
        Settings().setValue('remotes/authentication enabled', True)
        self.router.path = '/stage/api/poll'
        self.router.auth = ''
        self.router.headers = {'Authorization': None}
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()
        self.router.command = 'GET'

        # WHEN: called with a poll route
        self.router.do_post_processor()

        # THEN: the function should have been called only once
        self.router.send_response.assert_called_once_with(401)
        self.assertEqual(self.router.send_header.call_count, 5, 'The header should have been called five times.')

    def test_get_content_type(self):
        """
        Test the get_content_type logic
        """
        # GIVEN: a set of files and their corresponding types
        headers = [
            ['test.html', 'text/html'], ['test.css', 'text/css'],
            ['test.js', 'application/javascript'], ['test.jpg', 'image/jpeg'],
            ['test.gif', 'image/gif'], ['test.ico', 'image/x-icon'],
            ['test.png', 'image/png'], ['test.whatever', 'text/plain'],
            ['test', 'text/plain'], ['', 'text/plain'],
            [os.path.join(TEST_PATH, 'test.html'), 'text/html']]

        # WHEN: calling each file type
        for header in headers:
            ext, content_type = self.router.get_content_type(header[0])

            # THEN: all types should match
            self.assertEqual(content_type, header[1], 'Mismatch of content type')

    def test_main_poll(self):
        """
        Test the main poll logic
        """
        # GIVEN: a defined router with two slides
        Registry.create()
        Registry().register('live_controller', MagicMock)
        router = HttpRouter()
        router.send_response = MagicMock()
        router.send_header = MagicMock()
        router.end_headers = MagicMock()
        router.live_controller.slide_count = 2

        # WHEN: main poll called
        results = router.main_poll()

        # THEN: the correct response should be returned
        self.assertEqual(results.decode('utf-8'), '{"results": {"slide_count": 2}}',
                         'The resulting json strings should match')

    def test_serve_file_without_params(self):
        """
        Test the serve_file method without params
        """
        # GIVEN: mocked environment
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()
        self.router.html_dir = os.path.normpath('test/dir')
        self.router.template_vars = MagicMock()

        # WHEN: call serve_file with no file_name
        self.router.serve_file()

        # THEN: it should return a 404
        self.router.send_response.assert_called_once_with(404)
        self.assertEqual(self.router.end_headers.call_count, 1, 'end_headers called once')

    def test_serve_file_with_valid_params(self):
        """
        Test the serve_file method with an existing file
        """
        # GIVEN: mocked environment
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()
        self.router.html_dir = os.path.normpath('test/dir')
        self.router.template_vars = MagicMock()
        with patch('openlp.core.lib.os.path.exists') as mocked_exists, \
                patch('builtins.open', mock_open(read_data='123')):
            mocked_exists.return_value = True

            # WHEN: call serve_file with an existing html file
            self.router.serve_file(os.path.normpath('test/dir/test.html'))

            # THEN: it should return a 200 and the file
            self.router.send_response.assert_called_once_with(200)
            self.router.send_header.assert_called_once_with('Content-type', 'text/html')
            self.assertEqual(self.router.end_headers.call_count, 1, 'end_headers called once')

    def test_serve_file_with_partial_params(self):
        """
        Test the serve_file method with an existing file
        """
        # GIVEN: mocked environment
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()
        self.router.html_dir = os.path.normpath('test/dir')
        self.router.template_vars = MagicMock()
        with patch('openlp.core.lib.os.path.exists') as mocked_exists, \
                patch('builtins.open', mock_open(read_data='123')):
            mocked_exists.return_value = True

            # WHEN: call serve_file with an existing html file
            self.router.serve_file(os.path.normpath('test/dir/test'))

            # THEN: it should return a 200 and the file
            self.router.send_response.assert_called_once_with(200)
            self.router.send_header.assert_called_once_with('Content-type', 'text/html')
            self.assertEqual(self.router.end_headers.call_count, 1, 'end_headers called once')

    def test_serve_thumbnail_without_params(self):
        """
        Test the serve_thumbnail routine without params
        """
        # GIVEN: mocked environment
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()

        # WHEN: I request a thumbnail
        self.router.serve_thumbnail()

        # THEN: The headers should be set correctly
        self.router.send_response.assert_called_once_with(404)
        self.assertEqual(self.router.send_response.call_count, 1, 'Send response should be called once')
        self.assertEqual(self.router.end_headers.call_count, 1, 'end_headers should be called once')

    def test_serve_thumbnail_with_invalid_params(self):
        """
        Test the serve_thumbnail routine with invalid params
        """
        # GIVEN: Mocked send_header, send_response, end_headers and wfile
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()

        # WHEN: pass a bad controller
        self.router.serve_thumbnail('badcontroller', 'tecnologia 1.pptx/slide1.png')

        # THEN: a 404 should be returned
        self.assertEqual(len(self.router.send_header.mock_calls), 4, 'header should be called 4 times')
        self.assertEqual(len(self.router.send_response.mock_calls), 1, 'One response')
        self.assertEqual(len(self.router.wfile.mock_calls), 1, 'Once call to write to the socket')
        self.router.send_response.assert_called_once_with(404)

        # WHEN: pass a bad filename
        self.router.send_response.reset_mock()
        self.router.serve_thumbnail('presentations', 'tecnologia 1.pptx/badfilename.png')

        # THEN: return a 404
        self.router.send_response.assert_called_once_with(404)

        # WHEN: a dangerous URL is passed
        self.router.send_response.reset_mock()
        self.router.serve_thumbnail('presentations', '../tecnologia 1.pptx/slide1.png')

        # THEN: return a 404
        self.router.send_response.assert_called_once_with(404)

    def test_serve_thumbnail_with_valid_params(self):
        """
        Test the serve_thumbnail routine with valid params
        """
        # GIVEN: Mocked send_header, send_response, end_headers and wfile
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()
        mocked_image_manager = MagicMock()
        Registry().register('image_manager', mocked_image_manager)
        file_name = 'another%20test/slide1.png'
        full_path = os.path.normpath(os.path.join('thumbnails', file_name))
        width = 120
        height = 90
        with patch('openlp.core.lib.os.path.exists') as mocked_exists, \
                patch('builtins.open', mock_open(read_data='123')), \
                patch('openlp.plugins.remotes.lib.httprouter.AppLocation') as mocked_location, \
                patch('openlp.plugins.remotes.lib.httprouter.image_to_byte') as mocked_image_to_byte:
            mocked_exists.return_value = True
            mocked_image_to_byte.return_value = '123'
            mocked_location.get_section_data_path.return_value = ''

            # WHEN: pass good controller and filename
            self.router.serve_thumbnail('presentations', '{0}x{1}'.format(width, height), file_name)

            # THEN: a file should be returned
            self.assertEqual(self.router.send_header.call_count, 1, 'One header')
            self.assertEqual(self.router.send_response.call_count, 1, 'Send response called once')
            self.assertEqual(self.router.end_headers.call_count, 1, 'end_headers called once')
            mocked_exists.assert_called_with(urllib.parse.unquote(full_path))
            self.assertEqual(mocked_image_to_byte.call_count, 1, 'Called once')
            mocked_image_manager.add_image.assert_any_call(os.path.normpath(os.path.join('thumbnails', 'another test',
                                                                                         'slide1.png')),
                                                           'slide1.png', None, width, height)
            mocked_image_manager.get_image.assert_any_call(os.path.normpath(os.path.join('thumbnails', 'another test',
                                                                                         'slide1.png')),
                                                           'slide1.png', width, height)

    def test_remote_next(self):
        """
        Test service manager receives remote next click properly (bug 1407445)
        """
        # GIVEN: initial setup and mocks
        self.router.routes = [(r'^/api/service/(.*)$', {'function': self.router.service, 'secure': False})]
        self.router.request_data = False
        mocked_next_item = MagicMock()
        self.service_manager.next_item = mocked_next_item
        with patch.object(self.service_manager, 'setup_ui'), \
                patch.object(self.router, 'do_json_header'):
            self.service_manager.bootstrap_initialise()
            self.app.processEvents()

            # WHEN: Remote next is received
            self.router.service(action='next')
            self.app.processEvents()

            # THEN: service_manager.next_item() should have been called
            self.assertTrue(mocked_next_item.called, 'next_item() should have been called in service_manager')

    def test_remote_previous(self):
        """
        Test service manager receives remote previous click properly (bug 1407445)
        """
        # GIVEN: initial setup and mocks
        self.router.routes = [(r'^/api/service/(.*)$', {'function': self.router.service, 'secure': False})]
        self.router.request_data = False
        mocked_previous_item = MagicMock()
        self.service_manager.previous_item = mocked_previous_item
        with patch.object(self.service_manager, 'setup_ui'), \
                patch.object(self.router, 'do_json_header'):
            self.service_manager.bootstrap_initialise()
            self.app.processEvents()

            # WHEN: Remote next is received
            self.router.service(action='previous')
            self.app.processEvents()

            # THEN: service_manager.next_item() should have been called
            self.assertTrue(mocked_previous_item.called, 'previous_item() should have been called in service_manager')

    def test_remote_stage_personal_html(self):
        """
        Test the stage url with a parameter after loaded a url/stage.html file
        """
        # GIVEN: initial route
        self.router.config_dir = ''
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()
        self.router._process_file = MagicMock()

        # WHEN: I call stage with a suffix
        self.router.stages('stages', 'trb')

        # THEN: we should use the specific stage file instance
        self.router._process_file.assert_called_with(os.path.join('trb', 'stage.html'))

    def test_remote_stage_personal_css(self):
        """
        Test the html with reference stages/trb/trb.css then loaded a stages/trb/trb.css file
        """
        # GIVEN: initial route
        self.router.config_dir = ''
        self.router.send_response = MagicMock()
        self.router.send_header = MagicMock()
        self.router.end_headers = MagicMock()
        self.router.wfile = MagicMock()
        self.router._process_file = MagicMock()

        # WHEN: I call stage with a suffix
        self.router.stages('stages', 'stages/trb/trb.css')

        # THEN: we should use the specific stage file instance
        self.router._process_file.assert_called_with(os.path.join('trb', 'trb.css'))
