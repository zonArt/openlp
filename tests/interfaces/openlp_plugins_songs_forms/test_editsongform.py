"""
Package to test the openlp.plugins.songs.forms.editsongform package.
"""
from mock import MagicMock
from unittest import TestCase

from PyQt4 import QtGui

from openlp.core.lib import Registry
from openlp.plugins.songs.forms.editsongform import EditSongForm


class TestEditSongForm(TestCase):
    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.app = QtGui.QApplication.instance()
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

    def ui_defaults_test(self):
        """
        Test that the EditSongForm defaults are correct
        """
        self.assertFalse(self.form.verse_edit_button.isEnabled(), u'The verse edit button should not be enabled')
        self.assertFalse(self.form.verse_delete_button.isEnabled(), u'The verse delete button should not be enabled')
        self.assertFalse(self.form.author_remove_button.isEnabled(), u'The author remove button should not be enabled')
        self.assertFalse(self.form.topic_remove_button.isEnabled(), u'The topic remove button should not be enabled')
