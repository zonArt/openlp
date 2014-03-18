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
Test the registry properties
"""
from unittest import TestCase

from openlp.core.common import Registry, RegistryProperties
from tests.functional import MagicMock


class TestRegistryProperties(TestCase, RegistryProperties):
    """
    Test the functions in the ThemeManager module
    """
    def setUp(self):
        """
        Create the Register
        """
        Registry.create()

    def no_application_test(self):
        """
        Test property if no registry value assigned
        """
        # GIVEN an Empty Registry
        # WHEN there is no Application
        # THEN the application should be none
        self.assertEquals(self.application, None, 'The application value should be None')

    def application_test(self):
        """
        Test property if registry value assigned
        """
        # GIVEN an Empty Registry
        application = MagicMock()
        # WHEN the application is registered
        Registry().register('application', application)
        # THEN the application should be none
        self.assertEquals(self.application, application, 'The application value should match')