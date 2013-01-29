"""
    Package to test the openlp.core.ui package.
"""
from unittest import TestCase

from mock import patch
from openlp.core.lib import Registry
from openlp.core.ui import servicenoteform
from PyQt4 import QtCore, QtGui, QtTest

class TestStartNoteDialog(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        registry = Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register(u'main_window', self.main_window)
        self.form = servicenoteform.ServiceNoteForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        del self.app

    def basic_display_test(self):
        """
        Test Service Note form functionality
        """
        # GIVEN: A dialog with an empty text box
        self.form.text_edit.setPlainText(u'')

        # WHEN displaying the UI and pressing enter
        with patch(u'PyQt4.QtGui.QDialog') as mocked_exec:
            self.form.exec_()
        okWidget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(okWidget, QtCore.Qt.LeftButton)

        # THEN the following input text is returned
        self.assertEqual(self.form.text_edit.toPlainText(), u'', u'The returned text should be empty')

        # WHEN displaying the UI, having set the text and pressing enter
        text = u'OpenLP is the best worship software'
        self.form.text_edit.setPlainText(text)
        with patch(u'PyQt4.QtGui.QDialog') as mocked_exec:
            self.form.exec_()
        okWidget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(okWidget, QtCore.Qt.LeftButton)

        # THEN the following text is returned
        self.assertEqual(self.form.text_edit.toPlainText(), text, u'The text originally entered should still be there')

        # WHEN displaying the UI, having set the text and pressing enter
        self.form.text_edit.setPlainText(u'')
        with patch(u'PyQt4.QtGui.QDialog') as mocked_exec:
            self.form.exec_()
            self.form.text_edit.setPlainText(text)
        okWidget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(okWidget, QtCore.Qt.LeftButton)

        # THEN the following text is returned
        self.assertEqual(self.form.text_edit.toPlainText(), text, u'The new text should be returned')