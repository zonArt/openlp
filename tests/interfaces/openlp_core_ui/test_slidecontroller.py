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
from PyQt4 import QtCore, QtTest

from unittest import TestCase
from openlp.core.common import Registry
from openlp.core.lib import ScreenList

from openlp.core.ui import SlideController

from tests.interfaces import MagicMock, patch
from tests.helpers.testmixin import TestMixin


class TestSlideController(TestCase, TestMixin):

    def setUp(self):
        """
        Create the UI
        """
        self.build_settings()
        self.get_application()
        Registry.create()
        ScreenList.create(self.app.desktop())
        self.mocked_main_window = MagicMock()
        self.mocked_main_window.control_splitter = None
        Registry().register('media_controller', MagicMock())
        Registry().register('service_list', MagicMock())
        Registry().register('main_window', self.mocked_main_window)
        self.slide_controller = SlideController(None)
        self.slide_controller.update_slide_limits = MagicMock()
        self.slide_controller.type_prefix = MagicMock()
        self.slide_controller.category = MagicMock()

    def tearDown(self):
        """
        Clean up
        """
        self.destroy_settings()

    def click_preview_widget_test(self):
        """
        Test that when the preview_widget is clicked then on_slide_selected is called
        """
        # GIVEN: An initialized SlideController with some mocking
        with patch('openlp.core.ui.slidecontroller.create_action') as mocked_create_action:
            mocked_create_action.return_value = None
            self.slide_controller.on_slide_selected = MagicMock()
            self.slide_controller.initialise()

            # WHEN: The preview_widget is clicked
            QtTest.QTest.mouseClick(self.slide_controller.preview_widget, QtCore.Qt.LeftButton)
            QtTest.QTest.mouseClick(self.slide_controller.preview_widget.verticalHeader(), QtCore.Qt.LeftButton)

            # THEN slide_selected should have been called twice
            self.assertEqual(self.slide_controller.on_slide_selected.call_count, 2,
                             'on_slide_selected should have been called 2 times')
