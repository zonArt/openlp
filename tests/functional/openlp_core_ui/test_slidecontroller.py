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

from openlp.core.ui import SlideController

from tests.interfaces import MagicMock, patch


class TestSlideController(TestCase):

    def initial_slide_controller_test(self):
        """
        Test the initial slide controller state .
        """
        # GIVEN: A new slideController instance.
        slide_controller = SlideController(None)
        # WHEN: No SlideItem has been added yet.
        # THEN: The count of items should be zero.
        self.assertEqual(slide_controller.is_live, False, 'The base slide controller should not be a live controller')

    def toggle_blank_test(self):
        """
        Test the setting of the display blank icons by display type.
        """
        # GIVEN: A new slideController instance.
        slide_controller = SlideController(None)
        service_item = MagicMock()
        toolbar = MagicMock()
        toolbar.set_widget_visible = self.dummy_widget_visible
        slide_controller.toolbar = toolbar
        slide_controller.service_item = service_item

        # WHEN a text based service item is used
        slide_controller.service_item.is_text = MagicMock(return_value=True)
        slide_controller.set_blank_menu()

         # THEN: then call set up the toolbar to blank the display screen.
        self.assertEqual(len(self.test_widget), 3, 'There should be three icons to display on the screen')

        # WHEN a non text based service item is used
        slide_controller.service_item.is_text = MagicMock(return_value=False)
        slide_controller.set_blank_menu()

         # THEN: then call set up the toolbar to blank the display screen.
        self.assertEqual(len(self.test_widget), 2, 'There should be only two icons to display on the screen')

    def dummy_widget_visible(self, widget, visible=True):
        self.test_widget = widget
