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
Package to test the openlp.core.ui.slidecontroller package.
"""
import os

from unittest import TestCase

from openlp.core.common import Registry
from openlp.core.ui import ThemeManager

from tests.utils.constants import TEST_RESOURCES_PATH
from tests.interfaces import MagicMock, patch


class TestThemeManager(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        pass

    def initial_theme_manager_test(self):
        """
        Test the initial of theme manager.
        """
        # GIVEN: A new service manager instance.
        ThemeManager(None)

        # WHEN: the default theme manager is built.
        # THEN: The the controller should be registered in the registry.
        self.assertNotEqual(Registry().get('theme_manager'), None, 'The base theme manager should be registered')

    def write_theme_test(self):
        """
        Test that we don't try to overwrite a theme bacground image with itself
        """
        # GIVEN: A new theme manager instance, with mocked builtins.open, shutil.copyfile,
        #        theme, check_directory_exists and thememanager-attributes.
        with patch('builtins.open') as mocked_open, \
                patch('openlp.core.ui.thememanager.shutil.copyfile') as mocked_copyfile, \
                patch('openlp.core.ui.thememanager.check_directory_exists') as mocked_check_directory_exists:
            mocked_open.return_value = MagicMock()
            theme_manager = ThemeManager(None)
            theme_manager.old_background_image = None
            theme_manager.generate_and_save_image = MagicMock()
            theme_manager.path = ''
            mocked_theme = MagicMock()
            mocked_theme.theme_name = 'themename'
            mocked_theme.extract_formatted_xml = MagicMock()
            mocked_theme.extract_formatted_xml.return_value = 'fake_theme_xml'.encode()

            # WHEN: Calling _write_theme with path to the same image, but the path written slightly different
            file_name1 = os.path.join(TEST_RESOURCES_PATH, 'church.jpg')
            # Do replacement from end of string to avoid problems with path start
            file_name2 = file_name1[::-1].replace(os.sep, os.sep + os.sep, 2)[::-1]
            theme_manager._write_theme(mocked_theme, file_name1, file_name2)

            # THEN: The mocked_copyfile should not have been called
            self.assertFalse(mocked_copyfile.called, 'shutil.copyfile should not be called')
