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
Package to test the openlp.core.lib.theme package.
"""
from unittest import TestCase
import os

from openlp.core.lib.theme import ThemeXML


class TestThemeXML(TestCase):
    """
    Test the ThemeXML class
    """
    def test_new_theme(self):
        """
        Test the ThemeXML constructor
        """
        # GIVEN: The ThemeXML class
        # WHEN: A theme object is created
        default_theme = ThemeXML()

        # THEN: The default values should be correct
        self.assertEqual('#000000', default_theme.background_border_color, 'background_border_color should be "#000000"')
        self.assertEqual('solid', default_theme.background_type, 'background_type should be "solid"')
        self.assertEqual(0, default_theme.display_vertical_align, 'display_vertical_align should be 0')
        self.assertEqual('Arial', default_theme.font_footer_name, 'font_footer_name should be "Arial"')
        self.assertFalse(default_theme.font_main_bold, 'font_main_bold should be False')
        self.assertEqual(47, len(default_theme.__dict__), 'The theme should have 47 attributes')

    def test_expand_json(self):
        """
        Test the expand_json method
        """
        # GIVEN: A ThemeXML object and some JSON to "expand"
        theme = ThemeXML()
        theme_json = {
            'background': {
                'border_color': '#000000',
                'type': 'solid'
            },
            'display': {
                'vertical_align': 0
            },
            'font': {
                'footer': {
                    'bold': False
                },
                'main': {
                    'name': 'Arial'
                }
            }
        }

        # WHEN: ThemeXML.expand_json() is run
        theme.expand_json(theme_json)

        # THEN: The attributes should be set on the object
        self.assertEqual('#000000', theme.background_border_color, 'background_border_color should be "#000000"')
        self.assertEqual('solid', theme.background_type, 'background_type should be "solid"')
        self.assertEqual(0, theme.display_vertical_align, 'display_vertical_align should be 0')
        self.assertFalse(theme.font_footer_bold, 'font_footer_bold should be False')
        self.assertEqual('Arial', theme.font_main_name, 'font_main_name should be "Arial"')

    def test_extend_image_filename(self):
        """
        Test the extend_image_filename method
        """
        # GIVEN: A theme object
        theme = ThemeXML()
        theme.theme_name = 'MyBeautifulTheme   '
        theme.background_filename = '    video.mp4'
        theme.background_type = 'video'
        path = os.path.expanduser('~')

        # WHEN: ThemeXML.extend_image_filename is run
        theme.extend_image_filename(path)

        # THEN: The filename of the background should be correct
        expected_filename = os.path.join(path, 'MyBeautifulTheme', 'video.mp4')
        self.assertEqual(expected_filename, theme.background_filename)
        self.assertEqual('MyBeautifulTheme', theme.theme_name)

