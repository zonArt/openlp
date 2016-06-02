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
This module contains tests for the CSV Bible importer.
"""

import os
import json
from unittest import TestCase

from tests.functional import MagicMock, patch
from openlp.core.common.registry import Registry
from openlp.plugins.alerts.lib.alertsmanager import AlertsManager


class TestAlertManager(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()

    def test_remove_message_text(self):
        """
        Test that Alerts are not triggered with empty strings
        """
        # GIVEN: A valid Alert Manager
        alert_manager = AlertsManager(None)
        alert_manager.display_alert = MagicMock()

        # WHEN: Called with an empty string
        alert_manager.alert_text('')

        # THEN: the display should not have been triggered
        self.assertFalse(alert_manager.display_alert.called, 'The Alert should not have been called')

    def test_trigger_message_text(self):
        """
        Test that Alerts are triggered with a text string
        """
        # GIVEN: A valid Alert Manager
        alert_manager = AlertsManager(None)
        alert_manager.display_alert = MagicMock()

        # WHEN: Called with an empty string
        alert_manager.alert_text(['This is a string'])

        # THEN: the display should have been triggered
        self.assertTrue(alert_manager.display_alert.called, 'The Alert should have been called')

    def test_line_break_message_text(self):
        """
        Test that Alerts are triggered with a text string but line breaks are removed
        """
        # GIVEN: A valid Alert Manager
        alert_manager = AlertsManager(None)
        alert_manager.display_alert = MagicMock()

        # WHEN: Called with an empty string
        alert_manager.alert_text(['This is \n a string'])

        # THEN: the display should have been triggered
        self.assertTrue(alert_manager.display_alert.called, 'The Alert should have been called')
        alert_manager.display_alert.assert_called_once_with('This is   a string')
