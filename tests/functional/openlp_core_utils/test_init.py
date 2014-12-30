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
Package to test the openlp.core.utils.actions package.
"""
from unittest import TestCase

from openlp.core.common.settings import Settings
from openlp.core.utils import VersionThread, get_application_version, get_uno_command
from tests.functional import MagicMock, patch
from tests.helpers.testmixin import TestMixin


class TestInitFunctions(TestMixin, TestCase):

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
        with patch('PyQt4.QtCore.QThread'),\
                patch('openlp.core.utils.get_application_version') as mocked_get_application_version:
            mocked_get_application_version.return_value = {'version': '1.0.0', 'build': '', 'full': '2.0.4'}
            version_thread = VersionThread(mocked_main_window)
            version_thread.run()
        # THEN: If the version has changed the main window is notified
        self.assertTrue(mocked_main_window.emit.called, 'The main windows should have been notified')

    def get_uno_command_libreoffice_command_exists_test(self):
        """
        Test the ``get_uno_command`` function uses the libreoffice command when available.
        :return:
        """

        # GIVEN: A patched 'which' method which returns a path when called with 'libreoffice'
        with patch('openlp.core.utils.which',
                   **{'side_effect': lambda command: {'libreoffice': '/usr/bin/libreoffice'}[command]}):

            # WHEN: Calling get_uno_command
            result = get_uno_command()

            # THEN: The command 'libreoffice' should be called with the appropriate parameters
            self.assertEquals(result, 'libreoffice --nologo --norestore --minimized --nodefault --nofirststartwizard'
                                       ' "--accept=pipe,name=openlp_pipe;urp;"')

    def get_uno_command_only_soffice_command_exists_test(self):
        """
        Test the ``get_uno_command`` function uses the soffice command when the libreoffice command is not available.
        :return:
        """

        # GIVEN: A patched 'which' method which returns None when called with 'libreoffice' and a path when called with
        #        'soffice'
        with patch('openlp.core.utils.which',
                   **{'side_effect': lambda command: {'libreoffice': None, 'soffice': '/usr/bin/soffice'}[command]}):

            # WHEN: Calling get_uno_command
            result = get_uno_command()

            # THEN: The command 'soffice' should be called with the appropriate parameters
            self.assertEquals(result, 'soffice --nologo --norestore --minimized --nodefault --nofirststartwizard'
                                       ' "--accept=pipe,name=openlp_pipe;urp;"')

    def get_uno_command_when_no_command_exists_test(self):
        """
        Test the ``get_uno_command`` function raises an FileNotFoundError when neither the libreoffice or soffice
        commands are available.
        :return:
        """

        # GIVEN: A patched 'which' method which returns None
        with patch('openlp.core.utils.which', **{'return_value': None}):

            # WHEN: Calling get_uno_command

            # THEN: a FileNotFoundError exception should be raised
            self.assertRaises(FileNotFoundError, get_uno_command)

    def get_uno_command_connection_type_test(self):
        """
        Test the ``get_uno_command`` function when the connection type is anything other than pipe.
        :return:
        """

        # GIVEN: A patched 'which' method which returns 'libreoffice'
        with patch('openlp.core.utils.which', **{'return_value': 'libreoffice'}):

            # WHEN: Calling get_uno_command with a connection type other than pipe
            result = get_uno_command('socket')

            # THEN: The connection parameters should be set for socket
            self.assertEqual(result, 'libreoffice --nologo --norestore --minimized --nodefault --nofirststartwizard'
                                     ' "--accept=socket,host=localhost,port=2002;urp;"')
