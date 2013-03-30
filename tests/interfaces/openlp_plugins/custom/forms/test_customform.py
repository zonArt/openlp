"""
Module to test the custom edit form.
"""
from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtGui, QtTest, QtCore

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
        Test the load_custom() method.
        """
        # GIVEN: A mocked QDialog.exec_() method
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            # WHEN: Show the dialog and create a new custom item.
            self.form.exec_()
            self.form.load_custom(0)

            #THEN: The line edits should not contain any text.
            self.assertEqual(self.form.title_edit.text(), u'', u'The title edit should be empty')
            self.assertEqual(self.form.credit_edit.text(), u'', u'The credit edit should be empty')


    def on_add_button_clicked_test(self):
        """
        Test the on_add_button_clicked_test method / add_button button.
        """
        # GIVEN: A mocked QDialog.exec_() method
        with patch(u'PyQt4.QtGui.QDialog.exec_') as mocked_exec:
            # WHEN: Show the dialog and add a new slide.
            self.form.exec_()
            QtTest.QTest.mouseClick(self.form.add_button, QtCore.Qt.LeftButton)
            #THEN: One slide should be added.
            assert self.form.slide_list_view.count() == 1, u'There should be one slide added.'
