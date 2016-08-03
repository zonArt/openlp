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
Package to test the openlp.core.lib.languages package.
"""
from unittest import TestCase

from openlp.core.common import languages


class TestLanguages(TestCase):

    def languages_type_test(self):
        """
        Test the languages variable type
        """

        # GIVEN: The languages module
        # WHEN: Accessing the languages variable
        # THEN: It should be of type list
        self.assertIsInstance(languages.languages, list, 'languages.languages should be of type list')

    def language_selection_languages_type_test(self):
        """
        Test the selection of a language
        """

        # GIVEN: A list of languages from the languages module
        # WHEN: Selecting the first item
        language = languages.languages[0]

        # THEN: It should be an instance of the Language namedtuple
        self.assertIsInstance(language, languages.Language)
        self.assertEqual(language.id, 1)
        self.assertEqual(language.name, '(Afan) Oromo')
        self.assertEqual(language.code, 'om')

    def get_language_name_test(self):
        """
        Test get_language() when supplied with a language name.
        """

        # GIVEN: A language name, in capitals
        # WHEN: Calling get_language with it
        language = languages.get_language('YORUBA')

        # THEN: The Language found using that name should be returned
        self.assertIsInstance(language, languages.Language)
        self.assertEqual(language.id, 137)
        self.assertEqual(language.name, 'Yoruba')
        self.assertEqual(language.code, 'yo')

    def get_language_code_test(self):
        """
        Test get_language() when supplied with a language code.
        """

        # GIVEN: A language code in capitals
        # WHEN: Calling get_language with it
        language = languages.get_language('IA')

        # THEN: The Language found using that code should be returned
        self.assertIsInstance(language, languages.Language)
        self.assertEqual(language.id, 51)
        self.assertEqual(language.name, 'Interlingua')
        self.assertEqual(language.code, 'ia')

    def get_language_invalid_test(self):
        """
        Test get_language() when supplied with a string which is not a valid language name or code.
        """

        # GIVEN: A language code
        # WHEN: Calling get_language with it
        language = languages.get_language('qwerty')

        # THEN: None should be returned
        self.assertIsNone(language)

    def get_language_invalid__none_test(self):
        """
        Test get_language() when supplied with a string which is not a valid language name or code.
        """

        # GIVEN: A language code
        # WHEN: Calling get_language with it
        language = languages.get_language(None)

        # THEN: None should be returned
        self.assertIsNone(language)