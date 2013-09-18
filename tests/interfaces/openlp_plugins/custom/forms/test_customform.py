"""
Module to test the EditCustomForm.
"""
from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtGui, QtTest, QtCore

from openlp.core.lib import Registry
# Import needed due to import problems.
from openlp.plugins.custom.lib.mediaitem import CustomMediaItem
from openlp.plugins.custom.forms.editcustomform import EditCustomForm


class TestEditCustomForm(TestCase):
    """
    Test the EditCustomForm.
    """
    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register('main_window', self.main_window)
        media_item = MagicMock()
        manager = MagicMock()
        self.form = EditCustomForm(media_item, self.main_window, manager)

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        del self.app

    def load_themes_test(self):
        """
        Test the load_themes() method.
        """
        # GIVEN: A theme list.
        theme_list = ['First Theme', 'Second Theme']

        # WHEN: Show the dialog and add pass a theme list.
        self.form.load_themes(theme_list)

        # THEN: There should be three items in the combo box.
        assert self.form.theme_combo_box.count() == 3, 'There should be three items (themes) in the combo box.'

    def load_custom_test(self):
        """
        Test the load_custom() method.
        """
        # WHEN: Create a new custom item.
        self.form.load_custom(0)

        # THEN: The line edits should not contain any text.
        self.assertEqual(self.form.title_edit.text(), '', 'The title edit should be empty')
        self.assertEqual(self.form.credit_edit.text(), '', 'The credit edit should be empty')


    def on_add_button_clicked_test(self):
        """
        Test the on_add_button_clicked_test method / add_button button.
        """
        # GIVEN: A mocked QDialog.exec_() method
        with patch('PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            # WHEN: Add a new slide.
            QtTest.QTest.mouseClick(self.form.add_button, QtCore.Qt.LeftButton)

            # THEN: One slide should be added.
            assert self.form.slide_list_view.count() == 1, 'There should be one slide added.'

    def validate_not_valid_part1_test(self):
        """
        Test the _validate() method.
        """
        # GIVEN: Mocked methods.
        with patch('openlp.plugins.custom.forms.editcustomform.critical_error_message_box') as \
                mocked_critical_error_message_box:
            self.form.title_edit.displayText = MagicMock(return_value='')
            mocked_setFocus = MagicMock()
            self.form.title_edit.setFocus = mocked_setFocus

            # WHEN: Call the method.
            result = self.form._validate()

            # THEN: The validate method should have returned False.
            assert not result, 'The _validate() method should have retured False'
            mocked_setFocus.assert_called_with()
            mocked_critical_error_message_box.assert_called_with(message='You need to type in a title.')

    def validate_not_valid_part2_test(self):
        """
        Test the _validate() method.
        """
        # GIVEN: Mocked methods.
        with patch('openlp.plugins.custom.forms.editcustomform.critical_error_message_box') as \
                mocked_critical_error_message_box:
            self.form.title_edit.displayText = MagicMock(return_value='something')
            self.form.slide_list_view.count = MagicMock(return_value=0)

            # WHEN: Call the method.
            result = self.form._validate()

            # THEN: The validate method should have returned False.
            assert not result, 'The _validate() method should have retured False'
            mocked_critical_error_message_box.assert_called_with(message='You need to add at least one slide.')
