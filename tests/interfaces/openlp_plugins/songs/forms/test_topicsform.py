"""
Package to test the openlp.plugins.songs.forms.topicsform package.
"""
from unittest import TestCase

from PyQt4 import QtGui

from openlp.core.lib import Registry
from openlp.plugins.songs.forms.topicsform import TopicsForm


class TestTopicsForm(TestCase):
    """
    Test the TopicsForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = TopicsForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        del self.app

    def ui_defaults_test(self):
        """
        Test the TopicsForm defaults are correct
        """
        self.assertEqual(self.form.name_edit.text(), '', 'The first name edit should be empty')

    def get_name_property_test(self):
        """
        Test that getting the name property on the TopicsForm works correctly
        """
        # GIVEN: A topic name to set
        topic_name = 'Salvation'

        # WHEN: The name_edit's text is set
        self.form.name_edit.setText(topic_name)

        # THEN: The name property should have the correct value
        self.assertEqual(self.form.name, topic_name, 'The name property should be correct')

    def set_name_property_test(self):
        """
        Test that setting the name property on the TopicsForm works correctly
        """
        # GIVEN: A topic name to set
        topic_name = 'James'

        # WHEN: The name property is set
        self.form.name = topic_name

        # THEN: The name_edit should have the correct value
        self.assertEqual(self.form.name_edit.text(), topic_name, 'The topic name should be set correctly')
