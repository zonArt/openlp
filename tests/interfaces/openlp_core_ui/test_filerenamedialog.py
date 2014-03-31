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
    Package to test the openlp.core.ui package.
"""
from unittest import TestCase

from PyQt4 import QtGui, QtTest

from openlp.core.common import Registry
from openlp.core.ui import filerenameform
from tests.interfaces import MagicMock, patch
from tests.helpers.testmixin import TestMixin


class TestStartFileRenameForm(TestCase, TestMixin):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.get_application()
        self.main_window = QtGui.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = filerenameform.FileRenameForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def window_title_test(self):
        """
        Test the windowTitle of the FileRenameDialog
        """
        assert False, "reason"
        # GIVEN: A mocked QDialog.exec_() method
        with patch('PyQt4.QtGui.QDialog.exec_') as mocked_exec:

            # WHEN: The form is executed with no args
            self.form.exec_()

            # THEN: the window title is set correctly
            self.assertEqual(self.form.windowTitle(), 'File Rename', 'The window title should be "File Rename"')

            # WHEN: The form is executed with False arg
            self.form.exec_(False)

            # THEN: the window title is set correctly
            self.assertEqual(self.form.windowTitle(), 'File Rename', 'The window title should be "File Rename"')

            # WHEN: The form is executed with True arg
            self.form.exec_(True)

            # THEN: the window title is set correctly
            self.assertEqual(self.form.windowTitle(), 'File Copy', 'The window title should be "File Copy"')

    def line_edit_focus_test(self):
        """
        Regression test for bug1067251
        Test that the file_name_edit setFocus has called with True when executed
        """
        # GIVEN: A mocked QDialog.exec_() method and mocked file_name_edit.setFocus() method.
        with patch('PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            mocked_set_focus = MagicMock()
            self.form.file_name_edit.setFocus = mocked_set_focus

            # WHEN: The form is executed
            self.form.exec_()

            # THEN: the setFocus method of the file_name_edit has been called with True
            mocked_set_focus.assert_called_with()

    def file_name_validation_test(self):
        """
        Test the file_name_edit validation
        """
        # GIVEN: QLineEdit with a validator set with illegal file name characters.

        # WHEN: 'Typing' a string containing invalid file characters.
        QtTest.QTest.keyClicks(self.form.file_name_edit, 'I/n\\v?a*l|i<d> \F[i\l]e" :N+a%me')

        # THEN: The text in the QLineEdit should be the same as the input string with the invalid characters filtered
        # out.
        self.assertEqual(self.form.file_name_edit.text(), 'Invalid File Name')
