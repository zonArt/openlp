"""
Module to test the custom edit form.
"""
from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtGui

from openlp.core.lib import Registry
# Import needed due to import problems.
from openlp.plugins.custom.lib.mediaitem import CustomMediaItem
from openlp.plugins.custom.forms.editcustomform import EditCustomForm


class TestCustomFrom(TestCase):
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
        Registry().register(u'main_window', self.main_window)
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

    def load_custom_test(self):
        """
        Test the EditCustomForm defaults are correct
        """
        # GIVEN: A mocked QDialog.exec_() method
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            # WHEN: Show the dialog and create a new custom item.
            self.form.exec_()
            self.form.load_custom(0)

            #THEN: The line edits should not contain any text.
            self.assertEqual(self.form.title_edit.text(), u'', u'The title edit should be empty')
            self.assertEqual(self.form.credit_edit.text(), u'', u'The credit edit should be empty')

