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
Package to test the openlp.core.ui.settingsform package.
"""
from PyQt4 import QtGui
from unittest import TestCase

from openlp.core.common import Registry
from openlp.core.ui.settingsform import SettingsForm

from tests.functional import MagicMock, patch


class TestSettingsForm(TestCase):

    def setUp(self):
        """
        Set up a few things for the tests
        """
        Registry.create()

    def insert_tab_visible_test(self):
        """
        Test that the insert_tab() method works correctly when a visible tab is inserted
        """
        # GIVEN: A mocked tab and a Settings Form
        settings_form = SettingsForm(None)
        general_tab = MagicMock()
        general_tab.tab_title = 'mock'
        general_tab.tab_title_visible = 'Mock'
        general_tab.icon_path = ':/icon/openlp-logo-16x16.png'

        # WHEN: We insert the general tab
        with patch.object(settings_form.stacked_layout, 'addWidget') as mocked_add_widget, \
                patch.object(settings_form.setting_list_widget, 'addItem') as mocked_add_item:
            settings_form.insert_tab(general_tab, is_visible=True)

            # THEN: The general tab should have been inserted into the stacked layout and an item inserted into the list
            mocked_add_widget.assert_called_with(general_tab)
            self.assertEqual(1, mocked_add_item.call_count, 'addItem should have been called')

    def insert_tab_not_visible_test(self):
        """
        Test that the insert_tab() method works correctly when a tab that should not be visible is inserted
        """
        # GIVEN: A general tab and a Settings Form
        settings_form = SettingsForm(None)
        general_tab = MagicMock()
        general_tab.tab_title = 'mock'

        # WHEN: We insert the general tab
        with patch.object(settings_form.stacked_layout, 'addWidget') as mocked_add_widget, \
                patch.object(settings_form.setting_list_widget, 'addItem') as mocked_add_item:
            settings_form.insert_tab(general_tab, is_visible=False)

            # THEN: The general tab should have been inserted, but no list item should have been inserted into the list
            mocked_add_widget.assert_called_with(general_tab)
            self.assertEqual(0, mocked_add_item.call_count, 'addItem should not have been called')

    def list_item_changed_invalid_item_test(self):
        """
        Test that the list_item_changed() slot handles a non-existent item
        """
        # GIVEN: A mocked tab inserted into a Settings Form
        settings_form = SettingsForm(None)
        general_tab = QtGui.QWidget(None)
        general_tab.tab_title = 'mock'
        general_tab.tab_title_visible = 'Mock'
        general_tab.icon_path = ':/icon/openlp-logo-16x16.png'
        settings_form.insert_tab(general_tab, is_visible=True)

        with patch.object(settings_form.stacked_layout, 'count') as mocked_count:
            # WHEN: The list_item_changed() slot is called with an invalid item index
            settings_form.list_item_changed(100)

            # THEN: The rest of the method should not have been called
            self.assertEqual(0, mocked_count.call_count, 'The count method of the stacked layout should not be called')
