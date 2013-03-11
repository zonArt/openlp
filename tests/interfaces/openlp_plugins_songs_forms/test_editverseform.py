"""
Package to test the openlp.plugins.songs.forms.editverseform package.
"""
from unittest import TestCase

from PyQt4 import QtCore, QtGui, QtTest

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
        # GIVEN: An EditVerseForm instance
        # WHEN: The form is shown
        # THEN: The default value is correct
        self.assertEqual(self.form.verse_text_edit.toPlainText(), u'', u'The verse edit box is empty.')

    def insert_verse_test(self):
        """
        Test that inserting a verse works as it should.
        """
        # GIVEN: An instance of the EditVerseForm
        # WHEN: The Insert button is clicked
        QtTest.QTest.mouseClick(self.form.insert_button, QtCore.Qt.LeftButton)

        # THEN: The verse text edit should have a Verse:1 in it
        self.assertIn(u'---[Verse:1]---', self.form.verse_text_edit.toPlainText(),
                      u'The verse text edit should have a verse identifier')