"""
Package to test the openlp.core.lib.screenlist package.
"""
from unittest import TestCase

#from mock import MagicMock, patch

from openlp.core.lib import ScreenList

from PyQt4 import QtGui

class TestScreenList(object):

    def setUp(self):
        """
        Set up the components need for all tests.
        """
        self.application = QtGui.QApplication([])
        print ScreenList.create(self.application.desktop())
        self.screen_list = ScreenList()

    def tearDown(self):
        """
        Clean up the components needed for the tests.
        """
        del self.application

    def basic_test(self):
        """
        """
        print self.screen_list.get_screen_list()

    def add_desktop_test(self):
        """
        Test to check if new monitors are detected by OpenLP (= plugged in while OpenLP is running).
        """
        pass

