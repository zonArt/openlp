"""
    Package to test the openlp.core.ui package.
"""
import sys

from unittest import TestCase
from mock import MagicMock, patch
from openlp.core.ui import starttimeform
from PyQt4 import QtGui, QtTest

class TestStartTimeDialog(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        self.app = QtGui.QApplication(sys.argv)
        self.window = QtGui.QMainWindow()
        self.form = starttimeform.StartTimeForm(self.window)

    def ui_defaults_test(self):
        """
        Test StartTimeDialog defaults
        """
        self.assertEqual(self.form.hourSpinBox.minimum(), 0)
        self.assertEqual(self.form.hourSpinBox.maximum(), 4)
        self.assertEqual(self.form.minuteSpinBox.minimum(), 0)
        self.assertEqual(self.form.minuteSpinBox.maximum(), 59)
        self.assertEqual(self.form.secondSpinBox.minimum(), 0)
        self.assertEqual(self.form.secondSpinBox.maximum(), 59)
        self.assertEqual(self.form.hourFinishSpinBox.minimum(), 0)
        self.assertEqual(self.form.hourFinishSpinBox.maximum(), 4)
        self.assertEqual(self.form.minuteFinishSpinBox.minimum(), 0)
        self.assertEqual(self.form.minuteFinishSpinBox.maximum(), 59)
        self.assertEqual(self.form.secondFinishSpinBox.minimum(), 0)
        self.assertEqual(self.form.secondFinishSpinBox.maximum(), 59)

    def time_display_test(self):
        """
        Test StartTimeDialog display initialisation
        """
        # GIVEN: A service item with with time
        mocked_serviceitem =  MagicMock()
        mocked_serviceitem.start_time = 61
        mocked_serviceitem.end_time = 3701

        # WHEN displaying the UI and pressing enter
        self.form.item = mocked_serviceitem
        with patch(u'openlp.core.lib.QtGui.QDialog') as MockedQtGuiQDialog:
            MockedQtGuiQDialog.return_value = True
            self.form.exec_()

        # THEN the following values are returned
        self.assertEqual(self.form.hourSpinBox.value(), 1)
        self.assertEqual(self.form.minuteSpinBox.value(), 1)
        self.assertEqual(self.form.secondSpinBox.value(), 1)