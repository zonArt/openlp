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

    def basic_display_test(self):
        """
        Test FileRenameForm functionality
        """
        # GIVEN: FileRenameForm with no ARGS

        # WHEN displaying the UI
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            self.form.exec_()

        # THEN the window title is set as
        self.assertEqual(self.form.windowTitle(), u'File Rename', u'The window title should be "File Rename"')

        # GIVEN: FileRenameForm with False ARG
        false_arg = False

        # WHEN displaying the UI
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            self.form.exec_(false_arg)

        # THEN the window title is set as
        self.assertEqual(self.form.windowTitle(), u'File Rename', u'The window title should be "File Rename"')

        # GIVEN: FileRenameForm with False ARG
        true_arg = True

        # WHEN displaying the UI and pressing enter
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            self.form.exec_(true_arg)

        # THEN the window title is set as
        self.assertEqual(self.form.windowTitle(), u'File Copy', u'The window title should be "File Copy"')

        # GIVEN: FileRenameForm with defaults

        # WHEN displaying the UI
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            self.form.exec_()

        # THEN the lineEdit should have focus
        self.assertEqual(self.form.fileNameEdit.hasFocus(), True, u'fileNameEdit should have focus.')



        # Regression test for bug1067251
        # GIVEN: FileRenameForm with defaults

        # WHEN displaying the UI
       # with patch(u'PyQt4.QtGui.QDialog') as mocked_exec:
        #    self.form.exec_()

        # THEN the lineEdit should have focus
        #self.assertEqual(self.form.fileNameEdit.hasFocus(), u'File Rename', u'The window title should be "File Rename"')