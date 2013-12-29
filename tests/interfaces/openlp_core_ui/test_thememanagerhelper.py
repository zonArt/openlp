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
Interface tests to test the thememanagerhelper class and related methods.
"""
import os
from unittest import TestCase
from tempfile import mkstemp

from openlp.core.common import Settings
from openlp.core.ui import ThemeManagerHelper
from tests.functional import patch, MagicMock


class TestThemeManagerHelper(TestCase):
    """
    Test the functions in the ThemeManagerHelp[er module
    """
    def setUp(self):
        """
        Create the UI
        """
        fd, self.ini_file = mkstemp('.ini')
        Settings().set_filename(self.ini_file)
        self.helper = ThemeManagerHelper()
        self.helper.settings_section = "themes"

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        os.unlink(self.ini_file)
        os.unlink(Settings().fileName())

    def test_initialise(self):
        """
        Test the thememanagerhelper initialise - basic test
        """
        # GIVEN: A new a call to initialise
        Settings().setValue('themes/global theme', 'my_theme')
        self.helper.build_theme_path = MagicMock()
        self.helper.load_first_time_themes = MagicMock()

        # WHEN: the initialistion is run
        self.helper.initialise()

        # THEN:
        self.assertEqual(1, self.helper.build_theme_path.call_count,
                         'The function build_theme_path should have been called')
        self.assertEqual(1, self.helper.load_first_time_themes.call_count,
                         'The function load_first_time_themes should have been called only once')
        self.assertEqual(self.helper.global_theme, 'my_theme',
                         'The global theme should have been set to my_theme')

    def test_build_theme_path(self):
        """
        Test the thememanagerhelper build_theme_path - basic test
        """
        # GIVEN: A new a call to initialise
        with patch('openlp.core.common.applocation.check_directory_exists') as mocked_check_directory_exists:
            # GIVEN: A mocked out Settings class and a mocked out AppLocation.get_directory()
            mocked_check_directory_exists.return_value = True
        Settings().setValue('themes/global theme', 'my_theme')

        self.helper.theme_form = MagicMock()
        #self.helper.load_first_time_themes = MagicMock()

        # WHEN: the build_theme_path is run
        self.helper.build_theme_path()

        # THEN:
        self.assertEqual(self.helper.path, self.helper.theme_form.path,
                         'The theme path and the main path should be the same value')