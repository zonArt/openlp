"""
    Package to test the openlp.core.ui package.
"""
from unittest import TestCase

from mock import patch
from openlp.core.lib import Registry
from openlp.core.ui import filerenameform
from PyQt4 import QtCore, QtGui, QtTest

class TestStartFileRenameForm(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        registry = Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register(u'main_window', self.main_window)
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
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec:

            # WHEN: The form is executed with no args
            self.form.exec_()

            # THEN: the window title is set correctly
            self.assertEqual(self.form.windowTitle(), u'File Rename', u'The window title should be "File Rename"')

            # WHEN: The form is executed with False arg
            self.form.exec_(False)

            # THEN: the window title is set correctly
            self.assertEqual(self.form.windowTitle(), u'File Rename', u'The window title should be "File Rename"')

            # WHEN: The form is executed with True arg
            self.form.exec_(True)

            # THEN: the window title is set correctly
            self.assertEqual(self.form.windowTitle(), u'File Copy', u'The window title should be "File Copy"')

    def line_edit_focus_test(self):
        """
        Regression test for bug1067251
        Test that the fileNameEdit setFocus has called with True when executed
        """
        # GIVEN: A mocked QLineEdit class
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec, \
            patch(u'PyQt4.QtGui.QLineEdit') as mocked_line_edit:

            # WHEN: The form is executed with no args
            self.form.exec_()

            # THEN: the setFocus method of the fileNameEdit has been called with True
            mocked_line_edit.setFocus.assert_called_with()
