"""
Package to test the openlp.plugins.songs.forms.editsongform package.
"""
from mock import MagicMock
from unittest import TestCase

from PyQt4 import QtGui

from openlp.core.lib import Registry
from openlp.plugins.songs.forms.editsongform import EditSongForm


class TestEditSongForm(TestCase):
    """
    Test the EditSongForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register(u'main_window', self.main_window)
        Registry().register(u'theme_manager', MagicMock())
        self.form = EditSongForm(MagicMock(), self.main_window, MagicMock())

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        del self.app

    def ui_defaults_(self):
        """
        Test that the EditSongForm defaults are correct
        """
        self.assertFalse(self.form.verse_edit_button.isEnabled(), u'The verse edit button should not be enabled')
        self.assertFalse(self.form.verse_delete_button.isEnabled(), u'The verse delete button should not be enabled')
        self.assertFalse(self.form.author_remove_button.isEnabled(), u'The author remove button should not be enabled')
        self.assertFalse(self.form.topic_remove_button.isEnabled(), u'The topic remove button should not be enabled')

    def is_verse_edit_form_executed_t(self):
        pass

    def verse_order_warning_hidden_test(self):
        """
        Test if the verse order warning lable is visible, when a verse order is specified
        """
        # GIVEN: Mocked methods.
        mocked_row_count = MagicMock()
        mocked_row_count.return_value = 1
        self.form.verse_list_widget.rowCount = mocked_row_count
        # Mock out the verse.
        mocked_verse = MagicMock()
        self.form.verse_list_widget.item = mocked_verse
        mocked_verse_data_method = MagicMock()
        mocked_verse_data_method.return_value = u'V1'
        mocked_verse.data = mocked_verse_data_method
        mocked_item_method = MagicMock()
        mocked_item_method.return_value = mocked_verse
        mocked_extract_verse_order_method = MagicMock()
        mocked_extract_verse_order_method.return_value = [u'V1']
        self.form._extract_verse_order = mocked_extract_verse_order_method

        # WHEN: Call the method.
        self.form.on_verse_order_text_changed(u'V1')

        # THEN: The warning lable should be hidden.
        assert not self.form.warning_label.isVisible(), u'The warning lable should be hidden.'

    def bug_1170435_no_text_test(self):
        """
        Regression test for bug 1170435 (test if lable hidden, when no verse order is specified)
        """
        # GIVEN: Mocked methods.
        mocked_row_count = MagicMock()
        mocked_row_count.return_value = 0
        self.form.verse_list_widget.rowCount = mocked_row_count
        # Mock out the verse. (We want a verse type to be returned).
        mocked_verse = MagicMock()
        self.form.verse_list_widget.item = mocked_verse
        mocked_verse_data_method = MagicMock()
        mocked_verse_data_method.return_value = u'V1'
        mocked_verse.data = mocked_verse_data_method
        mocked_item_method = MagicMock()
        mocked_item_method.return_value = mocked_verse
        mocked_extract_verse_order_method = MagicMock()
        mocked_extract_verse_order_method.return_value = []
        self.form._extract_verse_order = mocked_extract_verse_order_method

        # WHEN: Call the method.
        self.form.on_verse_order_text_changed(u'')

        # THEN: The warning lable should be hidden.
        assert  not self.form.warning_label.isVisible(), \
            u'The lable should be visible because the verse order was left empty.'
