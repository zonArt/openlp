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
from unittest import TestCase

from openlp.core.common import Registry
from openlp.core.ui import ServiceManager

from tests.interfaces import MagicMock, patch


class TestServiceManager(TestCase):

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

    def initial_service_manager_test(self):
        """
        Test the initial of service manager.
        """
        # GIVEN: A new service manager instance.
        ServiceManager(None)
        # WHEN: the default service manager is built.
        # THEN: The the controller should be registered in the registry.
        self.assertNotEqual(Registry().get('service_manager'), None, 'The base service manager should be registered')

    def create_basic_service_test(self):
        """
        Test the create basic service array
        """
        # GIVEN: A new service manager instance.
        service_manager = ServiceManager(None)
        # WHEN: when the basic service array is created.
        service_manager._save_lite = False
        service_manager.service_theme = 'test_theme'
        service = service_manager.create_basic_service()[0]
        # THEN: The the controller should be registered in the registry.
        self.assertNotEqual(service, None, 'The base service should be created')
        self.assertEqual(service['openlp_core']['service-theme'], 'test_theme', 'The test theme should be saved')
        self.assertEqual(service['openlp_core']['lite-service'], False, 'The lite service should be saved')
