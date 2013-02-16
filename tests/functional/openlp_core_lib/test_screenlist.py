"""
Package to test the openlp.core.lib.screenlist package.
"""
import copy
from unittest import TestCase

from PyQt4 import QtGui, QtCore

from openlp.core.lib import ScreenList


class TestScreenList(TestCase):

    def setUp(self):
        """
        Set up the components need for all tests.
        """
        self.application = QtGui.QApplication.instance()
        self.screens = ScreenList.create(self.application.desktop())

    def add_desktop_test(self):
        """
        Test to check if new monitors are detected by OpenLP (= plugged in while OpenLP is running).
        """
        # GIVEN: The screen list.
        old_screens = copy.deepcopy(self.screens.screen_list)

        screen = {
            u'primary': False,
            u'number': 1,
            u'size': QtCore.QRect(0, 0, 1024, 768)
        }
        # Mock the attributes.
        self.screens.desktop.primaryScreen = MagicMock(return_value=screen[u'primary'])
        self.screens.desktop.screenCount = MagicMock(return_value=screen[u'number'] + 1)
        self.screens.desktop.screenGeometry = MagicMock(return_value=screen[u'size'])

        # WHEN: Add a new screen.
        self.screens.screen_count_changed(len(old_screens))

        # THEN: The screen should have been added.
        new_screens = self.screens.screen_list
        assert len(old_screens) + 1 == len(new_screens), u'The new_screens list should be bigger.'

        # THEN: The screens should be identically.
        assert screen == new_screens.pop(), u'The new screen should be identically to the screen defined above.'

