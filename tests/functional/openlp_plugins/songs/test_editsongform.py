"""
This module contains tests for the lib submodule of the Songs plugin.
"""
from unittest import TestCase

from PyQt4 import QtCore, QtGui

from openlp.core.common import Registry, Settings
from openlp.core.lib import ServiceItem
from openlp.plugins.songs.forms.editsongform import EditSongForm
from openlp.plugins.songs.lib.db import AuthorType
from tests.functional import patch, MagicMock
from tests.helpers.testmixin import TestMixin


class TestEditSongForm(TestCase, TestMixin):
    """
    Test the functions in the :mod:`lib` module.
    """
    def setUp(self):
        """
        Set up the components need for all tests.
        """
        Registry.create()
        Registry().register('service_list', MagicMock())
        Registry().register('main_window', MagicMock())
        with patch('openlp.plugins.songs.forms.editsongform.EditSongForm.__init__', return_value=None):
            self.edit_song_form = EditSongForm(None, MagicMock(), MagicMock())
        self.setup_application()
        self.build_settings()
        QtCore.QLocale.setDefault(QtCore.QLocale('en_GB'))

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.destroy_settings()

    def validate_matching_tags_test(self):
        # Given a set of tags
        tags = ['{r}', '{/r}', '{bl}', '{/bl}', '{su}', '{/su}']

        # WHEN we validate them
        valid = self.edit_song_form._validate_tags(tags)

        # THEN they should be valid
        self.assertTrue(valid, "The tags list should be valid")

    def validate_nonmatching_tags_test(self):
        # Given a set of tags
        tags = ['{r}', '{/r}', '{bl}', '{/bl}', '{br}', '{su}', '{/su}']

        # WHEN we validate them
        valid = self.edit_song_form._validate_tags(tags)

        # THEN they should be valid
        self.assertTrue(valid, "The tags list should be valid")
