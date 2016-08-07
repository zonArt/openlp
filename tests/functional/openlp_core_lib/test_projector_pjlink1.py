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
from openlp.core.lib.projector.constants import E_PARAMETER, ERROR_STRING, S_OFF, S_STANDBY, S_WARMUP, S_ON, \
    S_COOLDOWN, PJLINK_POWR_STATUS

from tests.functional import patch, MagicMock
from tests.resources.projector.data import TEST_PIN, TEST_SALT, TEST_CONNECT_AUTHENTICATE, TEST_HASH

pjlink_test = PJLink1(name='test', ip='127.0.0.1', pin=TEST_PIN, no_poll=True)


class TestPJLink(TestCase):
    """
    Tests for the PJLink module
    """
    @patch.object(pjlink_test, 'readyRead')
    @patch.object(pjlink_test, 'send_command')
    @patch.object(pjlink_test, 'waitForReadyRead')
    @patch('openlp.core.common.qmd5_hash')
    def test_authenticated_connection_call(self, mock_qmd5_hash, mock_waitForReadyRead, mock_send_command,
                                           mock_readyRead):
        """
        Ticket 92187: Fix for projector connect with PJLink authentication exception.
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

    def test_projector_class(self):
        """
        Test class version from projector
        """
        # GIVEN: Test object
        pjlink = pjlink_test

        # WHEN: Process class response
        pjlink.process_clss('1')

        # THEN: Projector class should be set to 1
        self.assertEquals(pjlink.pjlink_class, '1',
                          'Projector should have returned class=1')

    def test_non_standard_class_reply(self):
        """
        Bugfix 1550891: CLSS request returns non-standard 'Class N' reply
        """
        # GIVEN: Test object
        pjlink = pjlink_test

        # WHEN: Process non-standard reply
        pjlink.process_clss('Class 1')

        # THEN: Projector class should be set with proper value
        self.assertEquals(pjlink.pjlink_class, '1',
                          'Non-standard class reply should have set proper class')

    @patch.object(pjlink_test, 'change_status')
    def test_status_change(self, mock_change_status):
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
    def test_projector_return_ok(self, mock_process_inpt):
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

    @patch.object(pjlink_test, 'projectorReceivedData')
    def test_projector_process_lamp(self, mock_projectorReceivedData):
        """
        Test status lamp on/off and hours
        """
        # GIVEN: Test object
        pjlink = pjlink_test

        # WHEN: Call process_command with lamp data
        pjlink.process_command('LAMP', '22222 1')

        # THEN: Lamp should have been set with status=ON and hours=22222
        self.assertEquals(pjlink.lamp[0]['On'], True,
                          'Lamp power status should have been set to TRUE')
        self.assertEquals(pjlink.lamp[0]['Hours'], 22222,
                          'Lamp hours should have been set to 22222')

    @patch.object(pjlink_test, 'projectorReceivedData')
    def test_projector_process_multiple_lamp(self, mock_projectorReceivedData):
        """
        Test status multiple lamp on/off and hours
        """
        # GIVEN: Test object
        pjlink = pjlink_test

        # WHEN: Call process_command with lamp data
        pjlink.process_command('LAMP', '11111 1 22222 0 33333 1')

        # THEN: Lamp should have been set with proper lamp status
        self.assertEquals(len(pjlink.lamp), 3,
                          'Projector should have 3 lamps specified')
        self.assertEquals(pjlink.lamp[0]['On'], True,
                          'Lamp 1 power status should have been set to TRUE')
        self.assertEquals(pjlink.lamp[0]['Hours'], 11111,
                          'Lamp 1 hours should have been set to 11111')
        self.assertEquals(pjlink.lamp[1]['On'], False,
                          'Lamp 2 power status should have been set to FALSE')
        self.assertEquals(pjlink.lamp[1]['Hours'], 22222,
                          'Lamp 2 hours should have been set to 22222')
        self.assertEquals(pjlink.lamp[2]['On'], True,
                          'Lamp 3 power status should have been set to TRUE')
        self.assertEquals(pjlink.lamp[2]['Hours'], 33333,
                          'Lamp 3 hours should have been set to 33333')

    @patch.object(pjlink_test, 'projectorReceivedData')
    def test_projector_process_power_on(self, mock_projectorReceivedData):
        """
        Test status power to ON
        """
        # GIVEN: Test object and preset
        pjlink = pjlink_test
        pjlink.power = S_STANDBY

        # WHEN: Call process_command with turn power on command
        pjlink.process_command('POWR', PJLINK_POWR_STATUS[S_ON])

        # THEN: Power should be set to ON
        self.assertEquals(pjlink.power, S_ON, 'Power should have been set to ON')

    @patch.object(pjlink_test, 'projectorReceivedData')
    def test_projector_process_power_off(self, mock_projectorReceivedData):
        """
        Test status power to STANDBY
        """
        # GIVEN: Test object and preset
        pjlink = pjlink_test
        pjlink.power = S_ON

        # WHEN: Call process_command with turn power on command
        pjlink.process_command('POWR', PJLINK_POWR_STATUS[S_STANDBY])

        # THEN: Power should be set to STANDBY
        self.assertEquals(pjlink.power, S_STANDBY, 'Power should have been set to STANDBY')

    @patch.object(pjlink_test, 'projectorUpdateIcons')
    def test_projector_process_avmt_closed_unmuted(self, mock_projectorReceivedData):
        """
        Test avmt status shutter closed and audio muted
        """
        # GIVEN: Test object
        pjlink = pjlink_test
        pjlink.shutter = False
        pjlink.mute = True

        # WHEN: Called with setting shutter closed and mute off
        pjlink.process_avmt('11')

        # THEN: Shutter should be True and mute should be False
        self.assertTrue(pjlink.shutter, 'Shutter should have been set to closed')
        self.assertFalse(pjlink.mute, 'Audio should be off')

    @patch.object(pjlink_test, 'projectorUpdateIcons')
    def test_projector_process_avmt_open_muted(self, mock_projectorReceivedData):
        """
        Test avmt status shutter open and mute on
        """
        # GIVEN: Test object
        pjlink = pjlink_test
        pjlink.shutter = True
        pjlink.mute = False

        # WHEN: Called with setting shutter closed and mute on
        pjlink.process_avmt('21')

        # THEN: Shutter should be closed and mute should be True
        self.assertFalse(pjlink.shutter, 'Shutter should have been set to closed')
        self.assertTrue(pjlink.mute, 'Audio should be off')

    @patch.object(pjlink_test, 'projectorUpdateIcons')
    def test_projector_process_avmt_open_unmuted(self, mock_projectorReceivedData):
        """
        Test avmt status shutter open and mute off off
        """
        # GIVEN: Test object
        pjlink = pjlink_test
        pjlink.shutter = True
        pjlink.mute = True

        # WHEN: Called with setting shutter to closed and mute on
        pjlink.process_avmt('30')

        # THEN: Shutter should be closed and mute should be True
        self.assertFalse(pjlink.shutter, 'Shutter should have been set to open')
        self.assertFalse(pjlink.mute, 'Audio should be on')

    @patch.object(pjlink_test, 'projectorUpdateIcons')
    def test_projector_process_avmt_closed_muted(self, mock_projectorReceivedData):
        """
        Test avmt status shutter closed and mute off
        """
        # GIVEN: Test object
        pjlink = pjlink_test
        pjlink.shutter = False
        pjlink.mute = False

        # WHEN: Called with setting shutter to closed and mute on
        pjlink.process_avmt('31')

        # THEN: Shutter should be closed and mute should be True
        self.assertTrue(pjlink.shutter, 'Shutter should have been set to closed')
        self.assertTrue(pjlink.mute, 'Audio should be on')

    def test_projector_process_input(self):
        """
        Test input source status shows current input
        """
        # GIVEN: Test object
        pjlink = pjlink_test
        pjlink.source = '0'

        # WHEN: Called with input source
        pjlink.process_inpt('1')

        # THEN: Input selected should reflect current input
        self.assertEquals(pjlink.source, '1', 'Input source should be set to "1"')

    def test_projector_reset_information(self):
        """
        Test reset_information() resets all information and stops timers
        """
        # GIVEN: Test object and test data
        pjlink = pjlink_test
        pjlink.power = S_ON
        pjlink.pjlink_name = 'OPENLPTEST'
        pjlink.manufacturer = 'PJLINK'
        pjlink.model = '1'
        pjlink.shutter = True
        pjlink.mute = True
        pjlink.lamp = True
        pjlink.fan = True
        pjlink.source_available = True
        pjlink.other_info = 'ANOTHER TEST'
        pjlink.send_queue = True
        pjlink.send_busy = True
        pjlink.timer = MagicMock()
        pjlink.socket_timer = MagicMock()

        # WHEN: reset_information() is called
        with patch.object(pjlink.timer, 'stop') as mock_timer:
            with patch.object(pjlink.socket_timer, 'stop') as mock_socket_timer:
                pjlink.reset_information()

        # THEN: All information should be reset and timers stopped
        self.assertEquals(pjlink.power, S_OFF, 'Projector power should be OFF')
        self.assertIsNone(pjlink.pjlink_name, 'Projector pjlink_name should be None')
        self.assertIsNone(pjlink.manufacturer, 'Projector manufacturer should be None')
        self.assertIsNone(pjlink.model, 'Projector model should be None')
        self.assertIsNone(pjlink.shutter, 'Projector shutter should be None')
        self.assertIsNone(pjlink.mute, 'Projector shuttter should be None')
        self.assertIsNone(pjlink.lamp, 'Projector lamp should be None')
        self.assertIsNone(pjlink.fan, 'Projector fan should be None')
        self.assertIsNone(pjlink.source_available, 'Projector source_available should be None')
        self.assertIsNone(pjlink.source, 'Projector source should be None')
        self.assertIsNone(pjlink.other_info, 'Projector other_info should be None')
        self.assertEquals(pjlink.send_queue, [], 'Projector send_queue should be an empty list')
        self.assertFalse(pjlink.send_busy, 'Projector send_busy should be False')
        self.assertTrue(mock_timer.called, 'Projector timer.stop()  should have been called')
        self.assertTrue(mock_socket_timer.called, 'Projector socket_timer.stop() should have been called')

    @patch.object(pjlink_test, 'send_command')
    @patch.object(pjlink_test, 'waitForReadyRead')
    @patch.object(pjlink_test, 'projectorAuthentication')
    @patch.object(pjlink_test, 'timer')
    @patch.object(pjlink_test, 'socket_timer')
    def test_bug_1593882_no_pin_authenticated_connection(self, mock_socket_timer,
                                                         mock_timer,
                                                         mock_authentication,
                                                         mock_ready_read,
                                                         mock_send_command):
        """
        Test bug 1593882 no pin and authenticated request exception
        """
        # GIVEN: Test object and mocks
        pjlink = pjlink_test
        pjlink.pin = None
        mock_ready_read.return_value = True

        # WHEN: call with authentication request and pin not set
        pjlink.check_login(data=TEST_CONNECT_AUTHENTICATE)

        # THEN: No Authentication signal should have been sent
        mock_authentication.emit.assert_called_with(pjlink.name)

    @patch.object(pjlink_test, 'waitForReadyRead')
    @patch.object(pjlink_test, 'state')
    @patch.object(pjlink_test, '_send_command')
    @patch.object(pjlink_test, 'timer')
    @patch.object(pjlink_test, 'socket_timer')
    def test_bug_1593883_pjlink_authentication(self, mock_socket_timer,
                                               mock_timer,
                                               mock_send_command,
                                               mock_state,
                                               mock_waitForReadyRead):
        """
        Test bugfix 1593883 pjlink authentication
        """
        # GIVEN: Test object and data
        pjlink = pjlink_test
        pjlink.pin = TEST_PIN
        mock_state.return_value = pjlink.ConnectedState
        mock_waitForReadyRead.return_value = True

        # WHEN: Athenticated connection is called
        pjlink.check_login(data=TEST_CONNECT_AUTHENTICATE)

        # THEN: send_command should have the proper authentication
        self.assertEquals("{test}".format(test=mock_send_command.call_args),
                          "call(data='{hash}%1CLSS ?\\r')".format(hash=TEST_HASH))
