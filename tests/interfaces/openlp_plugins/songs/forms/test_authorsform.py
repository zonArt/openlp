"""
Package to test the openlp.plugins.songs.forms.authorsform package.
"""
from unittest import TestCase

from PyQt4 import QtGui

from openlp.core.lib import Registry
from openlp.plugins.songs.forms.authorsform import AuthorsForm


class TestAuthorsForm(TestCase):
    """
    Test the AuthorsForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = AuthorsForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        del self.app

    def ui_defaults_test(self):
        """
        Test the AuthorForm defaults are correct
        """
        self.assertEqual(self.form.first_name_edit.text(), '', 'The first name edit should be empty')
        self.assertEqual(self.form.last_name_edit.text(), '', 'The last name edit should be empty')
        self.assertEqual(self.form.display_edit.text(), '', 'The display name edit should be empty')

    def get_first_name_property_test(self):
        """
        Test that getting the first name property on the AuthorForm works correctly
        """
        # GIVEN: A first name to set
        first_name = 'John'

        # WHEN: The first_name_edit's text is set
        self.form.first_name_edit.setText(first_name)

        # THEN: The first_name property should have the correct value
        self.assertEqual(self.form.first_name, first_name, 'The first name property should be correct')

    def set_first_name_property_test(self):
        """
        Test that setting the first name property on the AuthorForm works correctly
        """
        # GIVEN: A first name to set
        first_name = 'James'

        # WHEN: The first_name property is set
        self.form.first_name = first_name

        # THEN: The first_name_edit should have the correct value
        self.assertEqual(self.form.first_name_edit.text(), first_name, 'The first name should be set correctly')

    def get_last_name_property_test(self):
        """
        Test that getting the last name property on the AuthorForm works correctly
        """
        # GIVEN: A last name to set
        last_name = 'Smith'

        # WHEN: The last_name_edit's text is set
        self.form.last_name_edit.setText(last_name)

        # THEN: The last_name property should have the correct value
        self.assertEqual(self.form.last_name, last_name, 'The last name property should be correct')

    def set_last_name_property_test(self):
        """
        Test that setting the last name property on the AuthorForm works correctly
        """
        # GIVEN: A last name to set
        last_name = 'Potter'

        # WHEN: The last_name property is set
        self.form.last_name = last_name

        # THEN: The last_name_edit should have the correct value
        self.assertEqual(self.form.last_name_edit.text(), last_name, 'The last name should be set correctly')

    def get_display_name_property_test(self):
        """
        Test that getting the display name property on the AuthorForm works correctly
        """
        # GIVEN: A display name to set
        display_name = 'John'

        # WHEN: The display_name_edit's text is set
        self.form.display_edit.setText(display_name)

        # THEN: The display_name property should have the correct value
        self.assertEqual(self.form.display_name, display_name, 'The display name property should be correct')

    def set_display_name_property_test(self):
        """
        Test that setting the display name property on the AuthorForm works correctly
        """
        # GIVEN: A display name to set
        display_name = 'John'

        # WHEN: The display_name property is set
        self.form.display_name = display_name

        # THEN: The display_name_edit should have the correct value
        self.assertEqual(self.form.display_edit.text(), display_name, 'The display name should be set correctly')

