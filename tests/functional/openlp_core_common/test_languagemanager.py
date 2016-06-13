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

from tests.functional import patch
from openlp.core.common.languagemanager import get_locale_key, get_natural_key


class TestLanguageManager(TestCase):
    """
    A test suite to test out various methods around the common __init__ class.
    """

    def test_get_locale_key(self):
        """
        Test the get_locale_key(string) function
        """
        with patch('openlp.core.common.languagemanager.LanguageManager.get_language') as mocked_get_language:
            # GIVEN: The language is German
            # 0x00C3 (A with diaresis) should be sorted as "A". 0x00DF (sharp s) should be sorted as "ss".
            mocked_get_language.return_value = 'de'
            unsorted_list = ['Auszug', 'Aushang', '\u00C4u\u00DFerung']

            # WHEN: We sort the list and use get_locale_key() to generate the sorting keys
            sorted_list = sorted(unsorted_list, key=get_locale_key)

            # THEN: We get a properly sorted list
            self.assertEqual(['Aushang', '\u00C4u\u00DFerung', 'Auszug'], sorted_list,
                             'Strings should be sorted properly')

    def test_get_natural_key(self):
        """
        Test the get_natural_key(string) function
        """
        with patch('openlp.core.common.languagemanager.LanguageManager.get_language') as mocked_get_language:
            # GIVEN: The language is English (a language, which sorts digits before letters)
            mocked_get_language.return_value = 'en'
            unsorted_list = ['item 10a', 'item 3b', '1st item']

            # WHEN: We sort the list and use get_natural_key() to generate the sorting keys
            sorted_list = sorted(unsorted_list, key=get_natural_key)

            # THEN: We get a properly sorted list
            self.assertEqual(['1st item', 'item 3b', 'item 10a'], sorted_list, 'Numbers should be sorted naturally')
