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
Package to test the openlp.core.ui.firsttimeform package.
"""
from configparser import ConfigParser
from unittest import TestCase

from openlp.core.common import Registry
from openlp.core.ui.firsttimeform import FirstTimeForm

from tests.functional import MagicMock, patch
from tests.helpers.testmixin import TestMixin

FAKE_CONFIG = b"""
[general]
base url = http://example.com/frw/
[songs]
directory = songs
[bibles]
directory = bibles
[themes]
directory = themes
"""


class TestFirstTimeForm(TestCase, TestMixin):

    def setUp(self):
        self.setup_application()
        self.app.setApplicationVersion('0.0')
        Registry.create()
        Registry().register('application', self.app)

    def basic_initialise_test(self):
        """
        Test if we can intialise the FirstTimeForm without a config file
        """
        # GIVEN: A mocked get_web_page, a First Time Wizard and an expected screen object
        with patch('openlp.core.ui.firsttimeform.get_web_page') as mocked_get_web_page:
            first_time_form = FirstTimeForm(None)
            expected_screens = MagicMock()
            expected_web_url = 'http://openlp.org/files/frw/'
            expected_user_agent = 'OpenLP/0.0'
            mocked_get_web_page.return_value = None

            # WHEN: The First Time Wizard is initialised
            first_time_form.initialize(expected_screens)

            # THEN: The First Time Form web configuration file should be accessible and parseable
            self.assertEqual(expected_screens, first_time_form.screens, 'The screens should be correct')
            self.assertEqual(expected_web_url, first_time_form.web, 'The base path of the URL should be correct')
            self.assertIsInstance(first_time_form.config, ConfigParser, 'The config object should be a ConfigParser')
            mocked_get_web_page.assert_called_with(expected_web_url + 'download.cfg',
                                                   header=('User-Agent', expected_user_agent))

    def config_initialise_test(self):
        """
        Test if we can intialise the FirstTimeForm with a config file
        """
        # GIVEN: A mocked get_web_page, a First Time Wizard and an expected screen object
        with patch('openlp.core.ui.firsttimeform.get_web_page') as mocked_get_web_page:
            first_time_form = FirstTimeForm(None)
            expected_web_url = 'http://openlp.org/files/frw/'
            expected_songs_url = 'http://example.com/frw/songs/'
            expected_bibles_url = 'http://example.com/frw/bibles/'
            expected_themes_url = 'http://example.com/frw/themes/'
            expected_user_agent = 'OpenLP/0.0'
            mocked_get_web_page.return_value.read.return_value = FAKE_CONFIG

            # WHEN: The First Time Wizard is initialised
            first_time_form.initialize(MagicMock())

            # THEN: The First Time Form web configuration file should be accessible and parseable
            self.assertIsInstance(first_time_form.config, ConfigParser, 'The config object should be a ConfigParser')
            mocked_get_web_page.assert_called_with(expected_web_url + 'download.cfg',
                                                   header=('User-Agent', expected_user_agent))
            self.assertEqual(expected_songs_url, first_time_form.songs_url, 'The songs URL should be correct')
            self.assertEqual(expected_bibles_url, first_time_form.bibles_url, 'The bibles URL should be correct')
            self.assertEqual(expected_themes_url, first_time_form.themes_url, 'The themes URL should be correct')
