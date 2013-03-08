"""
Package to test the openlp.plugins.songs.forms.editverseform package.
"""
from unittest import TestCase

from PyQt4 import QtGui

from openlp.core.lib import Registry
from openlp.plugins.songs.forms.editverseform import EditVerseForm


class TestEditVerseForm(TestCase):
    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication.instance()
        self.main_window = QtGui.QMainWindow()
        Registry().register(u'main_window', self.main_window)
        self.form = EditVerseForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        del self.app

    def ui_defaults_test(self):
        """
        Test the EditVerseForm defaults are correct
        """
        self.assertEqual(self.form.verseTextEdit.toPlainText(), u'', u'The verse edit box is empty.')