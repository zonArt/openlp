"""
This module contains tests for the editverseform of the Songs plugin.
"""
from unittest import TestCase

from PyQt4 import QtCore, QtGui

from openlp.core.common import Registry, Settings
from openlp.core.lib import ServiceItem
from openlp.plugins.songs.forms.editverseform import EditVerseForm
from openlp.plugins.songs.lib.db import AuthorType
from tests.functional import patch, MagicMock
from tests.helpers.testmixin import TestMixin


class TestEditVerseForm(TestCase, TestMixin):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Set up the components need for all tests.
        """
        self.edit_verse_form = EditVerseForm(None)
        self.setup_application()
        self.build_settings()
        QtCore.QLocale.setDefault(QtCore.QLocale('en_GB'))

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.destroy_settings()

    def update_suggested_verse_number_test(self):
        """
        Test if the update_suggested_verse_number method changes the value of
        the verse number if has_single_verse is True
        """
        # GIVEN some input values
        self.edit_verse_form.has_single_verse = True
        self.edit_verse_form.verse_type_combo_box.currentIndex = MagicMock(return_value = 0)
        self.edit_verse_form.verse_text_edit.toPlainText = MagicMock(return_value = 'Text')
        self.edit_verse_form.verse_number_box.setValue(3)
        

        # WHEN the method is called
        self.edit_verse_form.update_suggested_verse_number()
        
        # THEN the verse number must not be changed
        self.assertEqual(3, self.edit_verse_form.verse_number_box.value(), 'The verse number should be 3')
