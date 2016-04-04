# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
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
Package to test the openlp.core.common.versionchecker package.
"""
from unittest import TestCase

from openlp.core.common.settings import Settings
from openlp.core.common.versionchecker import VersionThread
from tests.functional import MagicMock, patch
from tests.helpers.testmixin import TestMixin


class TestVersionchecker(TestMixin, TestCase):

    def setUp(self):
        """
        Create an instance and a few example actions.
        """
        self.build_settings()

    def tearDown(self):
        """
        Clean up
        """
        self.destroy_settings()

    def version_thread_triggered_test(self):
        """
        Test the version thread call does not trigger UI
        :return:
        """
        # GIVEN: a equal version setup and the data is not today.
        mocked_main_window = MagicMock()
        Settings().setValue('core/last version test', '1950-04-01')
        # WHEN: We check to see if the version is different .
        with patch('PyQt5.QtCore.QThread'),\
                patch('openlp.core.common.versionchecker.get_application_version') as mocked_get_application_version:
            mocked_get_application_version.return_value = {'version': '1.0.0', 'build': '', 'full': '2.0.4'}
            version_thread = VersionThread(mocked_main_window)
            version_thread.run()
        # THEN: If the version has changed the main window is notified
        self.assertTrue(mocked_main_window.openlp_version_check.emit.called,
                        'The main windows should have been notified')