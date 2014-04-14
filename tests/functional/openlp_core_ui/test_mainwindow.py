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
Package to test openlp.core.ui.mainwindow package.
"""
import os

from unittest import TestCase

from openlp.core.ui.mainwindow import MainWindow
from openlp.core.common.registry import Registry
from tests.utils.constants import TEST_RESOURCES_PATH
from tests.helpers.testmixin import TestMixin
from tests.functional import MagicMock, patch


class TestMainWindow(TestCase, TestMixin):

    def setUp(self):
        Registry.create()
        self.registry = Registry()
        self.get_application()
        # Mock cursor busy/normal methods.
        self.app.set_busy_cursor = MagicMock()
        self.app.set_normal_cursor = MagicMock()
        self.app.args = []
        Registry().register('application', self.app)
        # Mock classes and methods used by mainwindow.
        with patch('openlp.core.ui.mainwindow.SettingsForm') as mocked_settings_form, \
                patch('openlp.core.ui.mainwindow.ImageManager') as mocked_image_manager, \
                patch('openlp.core.ui.mainwindow.LiveController') as mocked_live_controller, \
                patch('openlp.core.ui.mainwindow.PreviewController') as mocked_preview_controller, \
                patch('openlp.core.ui.mainwindow.OpenLPDockWidget') as mocked_dock_widget, \
                patch('openlp.core.ui.mainwindow.QtGui.QToolBox') as mocked_q_tool_box_class, \
                patch('openlp.core.ui.mainwindow.QtGui.QMainWindow.addDockWidget') as mocked_add_dock_method, \
                patch('openlp.core.ui.mainwindow.ThemeManager') as mocked_theme_manager, \
                patch('openlp.core.ui.mainwindow.Renderer') as mocked_renderer:
            self.main_window = MainWindow()

    def tearDown(self):
        del self.main_window

    def cmd_line_file_test(self):
        """
        Test that passing a service file from the command line loads the service.
        """
        # GIVEN a service as an argument to openlp
        service = os.path.join(TEST_RESOURCES_PATH, 'service', 'test.osz')
        self.main_window.arguments = [service]
        with patch('openlp.core.ui.servicemanager.ServiceManager.load_file') as mocked_load_path:

            # WHEN the argument is processed
            self.main_window.open_cmd_line_files()

            # THEN the service from the arguments is loaded
            mocked_load_path.assert_called_with(service), 'load_path should have been called with the service\'s path'

    def cmd_line_arg_test(self):
        """
        Test that passing a non service file does nothing.
        """
        # GIVEN a non service file as an argument to openlp
        service = os.path.join('openlp.py')
        self.main_window.arguments = [service]
        with patch('openlp.core.ui.servicemanager.ServiceManager.load_file') as mocked_load_path:

            # WHEN the argument is processed
            self.main_window.open_cmd_line_files()

            # THEN the file should not be opened
            assert not mocked_load_path.called, 'load_path should not have been called'
