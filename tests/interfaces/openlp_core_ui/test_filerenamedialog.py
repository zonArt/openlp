"""
    Package to test the openlp.core.ui package.
"""
from unittest import TestCase

from mock import MagicMock, patch
from openlp.core.lib import Registry
from openlp.core.ui import filerenameform
from PyQt4 import QtGui, QtTest


class TestStartFileRenameForm(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = filerenameform.FileRenameForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        del self.app

    def window_title_test(self):
        """
        Test the windowTitle of the FileRenameDialog
        """
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
