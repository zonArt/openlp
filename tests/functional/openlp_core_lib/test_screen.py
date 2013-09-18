"""
Package to test the openlp.core.lib.screenlist package.
"""

from unittest import TestCase

from mock import MagicMock
from PyQt4 import QtGui, QtCore

from openlp.core.lib import Registry, ScreenList


SCREEN = {
    'primary': False,
    'number': 1,
    'size': QtCore.QRect(0, 0, 1024, 768)
}


class TestScreenList(TestCase):

    def setUp(self):
        """
        Set up the components need for all tests.
        """
        # Mocked out desktop object
        self.desktop = MagicMock()
        self.desktop.primaryScreen.return_value = SCREEN['primary']
        self.desktop.screenCount.return_value = SCREEN['number']
        self.desktop.screenGeometry.return_value = SCREEN['size']

        self.application = QtGui.QApplication.instance()
        Registry.create()
        self.application.setOrganizationName('OpenLP-tests')
        self.application.setOrganizationDomain('openlp.org')
        self.screens = ScreenList.create(self.desktop)

    def tearDown(self):
        """
        Delete QApplication.
        """
        del self.screens
        del self.application

    def add_desktop_test(self):
        """
        Test the ScreenList.screen_count_changed method to check if new monitors are detected by OpenLP.
        """
        # GIVEN: The screen list at its current size
        old_screen_count = len(self.screens.screen_list)

        # WHEN: We add a new screen
        self.desktop.screenCount.return_value = SCREEN['number'] + 1
        self.screens.screen_count_changed(old_screen_count)

        # THEN: The screen should have been added and the screens should be identical
        new_screen_count = len(self.screens.screen_list)
        assert old_screen_count + 1 == new_screen_count, 'The new_screens list should be bigger'
        assert SCREEN == self.screens.screen_list.pop(), 'The 2nd screen should be identical to the first screen'
