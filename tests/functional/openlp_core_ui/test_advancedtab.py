# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 OpenLP Developers                                   #
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
Package to test the openlp.core.ui.advancedtab package.
"""
from unittest import TestCase

from openlp.core.common import Registry
from openlp.core.ui.advancedtab import AdvancedTab
from openlp.core.ui.settingsform import SettingsForm

from tests.helpers.testmixin import TestMixin


class TestAdvancedTab(TestCase, TestMixin):

    def setUp(self):
        """
        Set up a few things for the tests
        """
        Registry.create()

    def test_creation(self):
        """
        Test that Advanced Tab is created.
        """
        # GIVEN: A new Advanced Tab
        settings_form = SettingsForm(None)

        # WHEN: I create an advanced tab
        advanced_tab = AdvancedTab(settings_form)

        # THEN:
        self.assertEqual("Advanced", advanced_tab.tab_title, 'The tab title should be Advanced')

    def test_change_search_as_type(self):
        """
        Test that when search as type is changed custom and song configs are updated
        """
        # GIVEN: A new Advanced Tab
        settings_form = SettingsForm(None)
        advanced_tab = AdvancedTab(settings_form)

        # WHEN: I change search as type check box
        advanced_tab.on_search_as_type_check_box_changed(True)

        # THEN: we should have two post save processed to run
        self.assertEqual(2, len(settings_form.processes), 'Two post save processes should be created')
        self.assertTrue("songs_config_updated" in settings_form.processes, 'The songs plugin should be called')
        self.assertTrue("custom_config_updated" in settings_form.processes, 'The custom plugin should be called')

