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

from openlp.core.common import add_actions
from tests.functional import MagicMock, patch


class TestInit(TestCase):
    """
    A test suite to test out various methods around the common __init__ class.
    """

    def add_actions_empty_list_test(self):
        """
        Test that no actions are added when the list is empty
        """
        # GIVEN: a mocked action list, and an empty list
        mocked_target = MagicMock()
        empty_list = []

        # WHEN: The empty list is added to the mocked target
        add_actions(mocked_target, empty_list)

        # THEN: The add method on the mocked target is never called
        self.assertEqual(0, mocked_target.addSeparator.call_count, 'addSeparator method should not have been called')
        self.assertEqual(0, mocked_target.addAction.call_count, 'addAction method should not have been called')

    def add_actions_none_action_test(self):
        """
        Test that a separator is added when a None action is in the list
        """
        # GIVEN: a mocked action list, and a list with None in it
        mocked_target = MagicMock()
        separator_list = [None]

        # WHEN: The list is added to the mocked target
        add_actions(mocked_target, separator_list)

        # THEN: The addSeparator method is called, but the addAction method is never called
        mocked_target.addSeparator.assert_called_with()
        self.assertEqual(0, mocked_target.addAction.call_count, 'addAction method should not have been called')

    def add_actions_add_action_test(self):
        """
        Test that an action is added when a valid action is in the list
        """
        # GIVEN: a mocked action list, and a list with an action in it
        mocked_target = MagicMock()
        action_list = ['action']

        # WHEN: The list is added to the mocked target
        add_actions(mocked_target, action_list)

        # THEN: The addSeparator method is not called, and the addAction method is called
        self.assertEqual(0, mocked_target.addSeparator.call_count, 'addSeparator method should not have been called')
        mocked_target.addAction.assert_called_with('action')

    def add_actions_action_and_none_test(self):
        """
        Test that an action and a separator are added when a valid action and None are in the list
        """
        # GIVEN: a mocked action list, and a list with an action and None in it
        mocked_target = MagicMock()
        action_list = ['action', None]

        # WHEN: The list is added to the mocked target
        add_actions(mocked_target, action_list)

        # THEN: The addSeparator method is called, and the addAction method is called
        mocked_target.addSeparator.assert_called_with()
        mocked_target.addAction.assert_called_with('action')
