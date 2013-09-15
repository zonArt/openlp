"""
    Package to test the openlp.core.ui.listpreviewwidget.
"""

from unittest import TestCase
from mock import MagicMock, patch

from PyQt4 import QtGui

from openlp.core.lib import Registry, ServiceItem
from openlp.core.ui import listpreviewwidget
from tests.utils.osdinteraction import read_service_from_file


class TestListPreviewWidget(TestCase):

    def setUp(self):
        """
        Create the UI.
        """
        Registry.create()
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        self.image = QtGui.QImage(1, 1, QtGui.QImage.Format_RGB32)
        self.image_manager = MagicMock()
        self.image_manager.get_image.return_value = self.image
        Registry().register('image_manager', self.image_manager)
        self.preview_widget = listpreviewwidget.ListPreviewWidget(self.main_window, 2)

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault.
        """
        del self.preview_widget
        del self.main_window
        del self.app

    def initial_slide_count_test(self):
        """
        Test the inital slide count.
        """
        # GIVEN: A new ListPreviewWidget instance.
        # WHEN: No SlideItem has been added yet.
        # THEN: The count of items should be zero.
        self.assertEqual(self.preview_widget.slide_count(), 0, 'The slide list should be empty.')

    def initial_slide_number_test(self):
        """
        Test the inital slide number.
        """
        # GIVEN: A new ListPreviewWidget instance.
        # WHEN: No SlideItem has been added yet.
        # THEN: The number of the current item should be -1.
        self.assertEqual(self.preview_widget.current_slide_number(), -1, 'The slide number should be -1.')

    def replace_service_item_test(self):
        """
        Test item counts and current number with a service item.
        """
        # GIVEN: A ServiceItem with two frames.
        service_item = ServiceItem(None)
        service = read_service_from_file('serviceitem_image_3.osj')
        with patch('os.path.exists'):
            service_item.set_from_service(service[0])
        # WHEN: Added to the preview widget.
        self.preview_widget.replace_service_item(service_item, 1, 1)
        # THEN: The slide count and number should fit.
        self.assertEqual(self.preview_widget.slide_count(), 2, 'The slide count should be 2.')
        self.assertEqual(self.preview_widget.current_slide_number(), 1, 'The current slide number should  be 1.')

    def change_slide_test(self):
        """
        Test the change_slide method.
        """
        # GIVEN: A ServiceItem with two frames content.
        service_item = ServiceItem(None)
        service = read_service_from_file('serviceitem_image_3.osj')
        with patch('os.path.exists'):
            service_item.set_from_service(service[0])
        # WHEN: Added to the preview widget and switched to the second frame.
        self.preview_widget.replace_service_item(service_item, 1, 0)
        self.preview_widget.change_slide(1)
        # THEN: The current_slide_number should reflect the change.
        self.assertEqual(self.preview_widget.current_slide_number(), 1, 'The current slide number should  be 1.')
