"""
Package to test the openlp.core.lib.screenlist package.
"""
import copy
from unittest import TestCase

from mock import MagicMock
from PyQt4 import QtGui, QtCore

from openlp.core.lib import Registry, ScreenList


SCREEN = {
    u'primary': False,
    u'number': 1,
    u'size': QtCore.QRect(0, 0, 1024, 768)
}


class TestScreenList(TestCase):

    def setUp(self):
        """
        Set up the components need for all tests.
        """
        # Mocked out desktop object
        self.desktop = MagicMock()
        self.desktop.primaryScreen.return_value = SCREEN[u'primary']
        self.desktop.screenCount.return_value = SCREEN[u'number']
        self.desktop.screenGeometry.return_value = SCREEN[u'size']

        self.application = QtGui.QApplication.instance()
        Registry.create()
        self.application.setOrganizationName(u'OpenLP-tests')
        self.application.setOrganizationDomain(u'openlp.org')
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
        self.desktop.screenCount.return_value = SCREEN[u'number'] + 1
        self.screens.screen_count_changed(old_screen_count)

        # THEN: The screen should have been added and the screens should be identical
        new_screen_count = len(self.screens.screen_list)
        assert old_screen_count + 1 == new_screen_count, u'The new_screens list should be bigger'
        assert SCREEN == self.screens.screen_list.pop(), u'The 2nd screen should be identical to the first screen'
