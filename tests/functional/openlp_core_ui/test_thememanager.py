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
Package to test the openlp.core.ui.thememanager package.
"""
import zipfile
import os

from unittest import TestCase
from tests.interfaces import MagicMock

from openlp.core.ui import ThemeManager

RESOURCES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'themes'))


class TestThemeManager(TestCase):

    def export_theme_test(self):
        """
        Test exporting a theme .
        """
        # GIVEN: A new ThemeManager instance.
        theme_manager = ThemeManager()
        theme_manager.path = RESOURCES_PATH
        zipfile.ZipFile.__init__ = MagicMock()
        zipfile.ZipFile.__init__.return_value = None
        zipfile.ZipFile.write = MagicMock()

        # WHEN: The theme is exported
        theme_manager._export_theme('/some/path', 'Default')

        # THEN: The zipfile should be created at the given path
        zipfile.ZipFile.__init__.assert_called_with('/some/path/Default.otz', 'w')
        zipfile.ZipFile.write.assert_called_with(os.path.join(RESOURCES_PATH, 'Default', 'Default.xml'),
                                                 'Default/Default.xml')
