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
"""
Package to test the openlp.core.lib.projector.pjlink1 package.
"""

from unittest import TestCase

from openlp.core.lib.projector.pjlink1 import PJLink1
from openlp.core.lib.projector.constants import E_PARAMETER, ERROR_STRING

from tests.functional import patch
from tests.resources.projector.data import TEST_PIN, TEST_SALT, TEST_CONNECT_AUTHENTICATE

pjlink_test = PJLink1(name='test', ip='127.0.0.1', pin=TEST_PIN, no_poll=True)


class TestPJLink(TestCase):
    """
    Tests for the PJLink module
    """
    @patch.object(pjlink_test, 'readyRead')
    @patch.object(pjlink_test, 'send_command')
    @patch.object(pjlink_test, 'waitForReadyRead')
    @patch('openlp.core.common.qmd5_hash')
    def authenticated_connection_call_test(self,
                                           mock_qmd5_hash,
                                           mock_waitForReadyRead,
                                           mock_send_command,
                                           mock_readyRead):
        """
        Fix for projector connect with PJLink authentication exception. Ticket 92187.
        """
        # GIVEN: Test object
        pjlink = pjlink_test

        # WHEN: Calling check_login with authentication request:
        pjlink.check_login(data=TEST_CONNECT_AUTHENTICATE)

        # THEN: Should have called qmd5_hash
        self.assertTrue(mock_qmd5_hash.called_with(TEST_SALT,
                                                   "Connection request should have been called with TEST_SALT"))
        self.assertTrue(mock_qmd5_hash.called_with(TEST_PIN,
                                                   "Connection request should have been called with TEST_PIN"))

    def non_standard_class_reply_test(self):
        """
        bugfix 1550891 - CLSS request returns non-standard 'Class N' reply
        """
        # GIVEN: Test object
        pjlink = pjlink_test

        # WHEN: Process non-standard reply
        pjlink.process_clss('Class 1')

        # THEN: Projector class should be set with proper value
        self.assertEquals(pjlink.pjlink_class, '1',
                          'Non-standard class reply should have set proper class')

    @patch.object(pjlink_test, 'change_status')
    def status_change_test(self, mock_change_status):
        """
        Test process_command call with ERR2 (Parameter) status
        """
        # GIVEN: Test object
        pjlink = pjlink_test

        # WHEN: process_command is called with "ERR2" status from projector
        pjlink.process_command('POWR', 'ERR2')

        # THEN: change_status should have called change_status with E_UNDEFINED
        #       as first parameter
        mock_change_status.called_with(E_PARAMETER,
                                       'change_status should have been called with "{}"'.format(
                                           ERROR_STRING[E_PARAMETER]))

    @patch.object(pjlink_test, 'process_inpt')
    def projector_return_ok_test(self, mock_process_inpt):
        """
        Test projector calls process_inpt command when process_command is called with INPT option
        """
        # GIVEN: Test object
        pjlink = pjlink_test

        # WHEN: process_command is called with INST command and 31 input:
        pjlink.process_command('INPT', '31')

        # THEN: process_inpt method should have been called with 31
        mock_process_inpt.called_with('31',
                                      "process_inpt should have been called with 31")
