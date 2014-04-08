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

from PyQt4 import QtCore

from openlp.core.common import Registry
from openlp.core.lib import ScreenList
from openlp.core.ui import MainDisplay

from tests.interfaces import MagicMock, patch

SCREEN = {
    'primary': False,
    'number': 1,
    'size': QtCore.QRect(0, 0, 1024, 768)
}


class TestMainDisplay(TestCase):

    def setUp(self):
        """
        Set up the components need for all tests.
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

    def initial_main_display_test(self):
        """
        Test the initial Main Display state .
        """
        # GIVEN: A new slideController instance.
        display = MagicMock()
        display.is_live = True

        # WHEN: the default controller is built.
        main_display = MainDisplay(display)

        # THEN: The controller should not be a live controller.
        self.assertEqual(main_display.is_live, True, 'The main display should be a live controller')

    def set_transparency_enable_test(self):
        """
        Test creating an instance of the MainDisplay class
        """
        # GIVEN: get an instance of MainDisplay
        display = MagicMock()
        main_display = MainDisplay(display)

        # WHEN: We enable transparency
        main_display.set_transparency(True)

        # THEN: There should be a Stylesheet
        self.assertEqual('QGraphicsView {background: transparent; border: 0px;}', main_display.styleSheet(),
                         'MainDisplay instance should be transparent')
        self.assertFalse(main_display.autoFillBackground(),
                         'MainDisplay instance should be without background auto fill')
        self.assertTrue(main_display.testAttribute(QtCore.Qt.WA_TranslucentBackground),
                        'MainDisplay hasnt translucent background')

        # WHEN: We disable transparency
        main_display.set_transparency(False)

        # THEN: The Stylesheet should be empty
        self.assertEqual('QGraphicsView {}', main_display.styleSheet(),
                         'MainDisplay instance should not be transparent')
        self.assertFalse(main_display.testAttribute(QtCore.Qt.WA_TranslucentBackground),
                        'MainDisplay hasnt translucent background')
