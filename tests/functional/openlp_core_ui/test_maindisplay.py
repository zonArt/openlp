# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann, Dmitriy Marmyshev      #
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
Package to test the openlp.core.lib.maindisplay package.
"""
from unittest import TestCase

from mock import MagicMock

from openlp.core.ui.maindisplay import MainDisplay


class TestMainDisplay(TestCase):
    """
    Test the functions in the :mod:`MainDisplay` module.
    """
    #TODO: The following classes still need tests written for
    #   - Display
    #   - MainDisplay
    #   - AudioPlayer

    def setUp(self):
        self.main_dispaly_patcher = patch('openlp.core.ui.maindisplay.MainDisplay')
        self.mocked_main_dispaly = self.main_dispaly_patcher.start()
        self.mocked_main_dispaly.__init__()

        #.setAutoFillBackground, .setStyleSheet, .setAttribute, .repaint


    def tearDown(self):
        self.main_dispaly_patcher.stop()



    def set_transparency_enable_test(self):
        """
        Test creating an instance of the MainDisplay class
        """
        # GIVEN: Reset mocks: MainDisplay.__init__, MainDisplay.setAutoFillBackground, etc. And an instance of MainDisplay
        #self.mocked_main_dispaly.__init__()

        # WHEN: MainDispaly.set_transparency is called with a true value"
        self.mocked_main_dispaly.set_transparency(True)

        # THEN: MainDisplay.setAutoFillBackground, MainDisplay.setStyleSheet, MainDisplay.setAttribute,
        # MainDisplay.repaint should have been called with known values"
        assert self.mocked_main_dispaly.StyleSheet != "QGraphicsView {background: transparent; border: 0px;}", \
            'MainDisplay instance should be transparent'
