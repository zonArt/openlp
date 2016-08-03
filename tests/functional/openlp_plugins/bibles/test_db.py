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
This module contains tests for the db submodule of the Bibles plugin.
"""

from unittest import TestCase

from openlp.plugins.bibles.lib.db import BibleDB
from tests.functional import MagicMock, patch


class TestBibleDB(TestCase):
    """
    Test the functions in the BibleDB class.
    """

    def test_get_language_canceled(self):
        """
        Test the BibleDB.get_language method when the user rejects the dialog box
        """
        # GIVEN: A mocked LanguageForm with an exec method which returns QtDialog.Rejected and an instance of BibleDB
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'),\
                patch('openlp.plugins.bibles.forms.LanguageForm') as mocked_language_form:

            # The integer value of QtDialog.Rejected is 0. Using the enumeration causes a seg fault for some reason
            mocked_language_form_instance = MagicMock(**{'exec.return_value': 0})
            mocked_language_form.return_value = mocked_language_form_instance
            mocked_parent = MagicMock()
            instance = BibleDB(mocked_parent)
            mocked_wizard = MagicMock()
            instance.wizard = mocked_wizard

            # WHEN: Calling get_language()
            result = instance.get_language()

            # THEN: get_language() should return False
            mocked_language_form.assert_called_once_with(mocked_wizard)
            mocked_language_form_instance.exec.assert_called_once_with(None)
            self.assertFalse(result, 'get_language() should return False if the user rejects the dialog box')

    def test_get_language_accepted(self):
        """
        Test the BibleDB.get_language method when the user accepts the dialog box
        """
        # GIVEN: A mocked LanguageForm with an exec method which returns QtDialog.Accepted an instance of BibleDB and
        #       a combobox with the selected item data as 10
        with patch('openlp.plugins.bibles.lib.db.BibleDB._setup'), \
                patch('openlp.plugins.bibles.lib.db.BibleDB.save_meta'), \
                patch('openlp.plugins.bibles.forms.LanguageForm') as mocked_language_form:

            # The integer value of QtDialog.Accepted is 1. Using the enumeration causes a seg fault for some reason
            mocked_language_form_instance = MagicMock(**{'exec.return_value': 1,
                                                         'language_combo_box.itemData.return_value': 10})
            mocked_language_form.return_value = mocked_language_form_instance
            mocked_parent = MagicMock()
            instance = BibleDB(mocked_parent)
            mocked_wizard = MagicMock()
            instance.wizard = mocked_wizard

            # WHEN: Calling get_language()
            result = instance.get_language('Bible Name')

            # THEN: get_language() should return the id of the selected language in the combo box
            mocked_language_form.assert_called_once_with(mocked_wizard)
            mocked_language_form_instance.exec.assert_called_once_with('Bible Name')
            self.assertEqual(result, 10, 'get_language() should return the id of the language the user has chosen when '
                                         'they accept the dialog box')