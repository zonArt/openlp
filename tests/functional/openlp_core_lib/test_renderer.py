# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
Package to test the openlp.core.ui.renderer package.
"""
from unittest import TestCase

from PyQt4 import QtCore

from openlp.core.common import Registry
from openlp.core.lib import Renderer, ScreenList

from tests.interfaces import MagicMock

SCREEN = {
    'primary': False,
    'number': 1,
    'size': QtCore.QRect(0, 0, 1024, 768)
}


class TestRenderer(TestCase):

    def setUp(self):
        """
        Set up the components need for all tests
        """
        # Mocked out desktop object
        self.desktop = MagicMock()
        self.desktop.primaryScreen.return_value = SCREEN['primary']
        self.desktop.screenCount.return_value = SCREEN['number']
        self.desktop.screenGeometry.return_value = SCREEN['size']
        self.screens = ScreenList.create(self.desktop)
        Registry.create()

    def tearDown(self):
        """
        Delete QApplication.
        """
        del self.screens

    def initial_renderer_test(self):
        """
        Test the initial renderer state
        """
        # GIVEN: A new renderer instance.
        renderer = Renderer()
        # WHEN: the default renderer is built.
        # THEN: The renderer should be a live controller.
        self.assertEqual(renderer.is_live, True, 'The base renderer should be a live controller')

    def default_screen_layout_test(self):
        """
        Test the default layout calculations
        """
        # GIVEN: A new renderer instance.
        renderer = Renderer()
        # WHEN: given the default screen size has been created.
        # THEN: The renderer have created a default screen.
        self.assertEqual(renderer.width, 1024, 'The base renderer should be a live controller')
        self.assertEqual(renderer.height, 768, 'The base renderer should be a live controller')
        self.assertEqual(renderer.screen_ratio, 0.75, 'The base renderer should be a live controller')
        self.assertEqual(renderer.footer_start, 691, 'The base renderer should be a live controller')

    def _get_start_tags_test(self):
        """
        Test the _get_start_tags() method
        """
        # GIVEN: A new renderer instance. Broken raw_text (missing closing tags).
        renderer = Renderer()
        given_raw_text = '{st}{r}Text text text'
        expected_tuple = ('{st}{r}Text text text{/r}{/st}', '{st}{r}',
                          '<strong><span style="-webkit-text-fill-color:red">')

        # WHEN:
        result = renderer._get_start_tags(given_raw_text)

        # THEN: Check if the correct tuple is returned.
        self.assertEqual(result, expected_tuple), 'A tuple should be returned '
        '(fixed-text, opening tags, html opening tags).'

    def _word_split_test(self):
        """
        Test the _word_split() method
        """
        # GIVEN: A line of text
        renderer = Renderer()
        given_line = 'beginning asdf \n end asdf'
        expected_words = ['beginning', 'asdf', 'end', 'asdf']

        # WHEN: Split the line
        result_words = renderer._words_split(given_line)

        # THEN: The word lists should be the same.
        self.assertListEqual(result_words, expected_words)

        pep_error = 'sdfjalksdjfl kajsdlfj lkasdjflkjaslkdjlkasjdljklsdjflkajsdljalksdflkajsdlfj laskdflkjsdlfkjaslkdflksajdlfk'
