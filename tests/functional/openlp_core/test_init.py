# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 OpenLP Developers                                   #
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

import sys
from unittest import TestCase

from openlp.core import parse_options
from tests.helpers.testmixin import TestMixin


class TestInitFunctions(TestMixin, TestCase):

    def parse_options_basic_test(self):
        """
        Test the parse options process works

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = []
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, 'warning', 'The log level should be set to warning')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, [], 'The service file should be blank')

    def parse_options_debug_test(self):
        """
        Test the parse options process works for debug only

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['-l debug']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, ' debug', 'The log level should be set to debug')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, [], 'The service file should be blank')

    def parse_options_debug_and_portable_test(self):
        """
        Test the parse options process works for debug and portable

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['--portable']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, 'warning', 'The log level should be set to warning')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertTrue(args.portable, 'The portable flag should be set to true')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, [], 'The service file should be blank')

    def parse_options_all_no_file_test(self):
        """
        Test the parse options process works with two options

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['-l debug', '-d']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertTrue(args.dev_version, 'The dev_version flag should be True')
        self.assertEquals(args.loglevel, ' debug', 'The log level should be set to debug')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, [], 'The service file should be blank')

    def parse_options_file_test(self):
        """
        Test the parse options process works with a file

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['dummy_temp']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, 'warning', 'The log level should be set to warning')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, 'dummy_temp', 'The service file should not be blank')

    def parse_options_file_and_debug_test(self):
        """
        Test the parse options process works with a file

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['-l debug', 'dummy_temp']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertFalse(args.dev_version, 'The dev_version flag should be False')
        self.assertEquals(args.loglevel, ' debug', 'The log level should be set to debug')
        self.assertFalse(args.no_error_form, 'The no_error_form should be set to False')
        self.assertFalse(args.portable, 'The portable flag should be set to false')
        self.assertEquals(args.style, None, 'There are no style flags to be processed')
        self.assertEquals(args.rargs, 'dummy_temp', 'The service file should not be blank')

    def parse_options_two_files_test(self):
        """
        Test the parse options process works with a file

        """
        # GIVEN: a a set of system arguments.
        sys.argv[1:] = ['dummy_temp', 'dummy_temp2']
        # WHEN: We we parse them to expand to options
        args = parse_options()
        # THEN: the following fields will have been extracted.
        self.assertEquals(args, None, 'The args should be None')
