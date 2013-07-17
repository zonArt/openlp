"""
This module contains tests for the lib submodule of the Presentations plugin.
"""
import os
from tempfile import mkstemp
from unittest import TestCase

from mock import patch, MagicMock

from PyQt4 import QtGui

from openlp.core.lib import Registry

from openlp.plugins.presentations.lib.mediaitem import PresentationMediaItem


class TestMediaItem(TestCase):
    """
    Test the mediaitem methods.
    """
    def setUp(self):
        """
        Set up the components need for all tests.
        """
        Registry.create()
        Registry().register(u'service_manager', MagicMock())
        Registry().register(u'main_window', MagicMock())

        with patch('openlp.plugins.presentations.lib.mediaitem.PresentationMediaItem.__init__') as mocked_init:
            mocked_init.return_value = None
            self.media_item = PresentationMediaItem(MagicMock(), MagicMock, MagicMock(), MagicMock())

        self.application = QtGui.QApplication.instance()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.application

    def build_file_mask_string_test(self):
        """
        Test the build_file_mask_string() method
        """
        # GIVEN: Different controllers.
        impress_controller = MagicMock()
        impress_controller.enabled.return_value = True
        impress_controller.supports = [u'odp']
        impress_controller.also_supports = [u'ppt']
        presentation_controller = MagicMock()
        presentation_controller.enabled.return_value = True
        presentation_controller.supports = [u'ppt']
        presentation_controller.also_supports = []
        presentation_viewer_controller = MagicMock()
        presentation_viewer_controller.enabled.return_value = False
        # Mock the controllers.
        self.media_item.controllers = {
            u'Impress': impress_controller,
            u'Powerpoint': presentation_controller,
            u'Powerpoint Viewer': presentation_viewer_controller
        }

        # WHEN: Build the file mask.
        with patch('openlp.plugins.presentations.lib.mediaitem.translate') as mocked_translate:
            mocked_translate.side_effect = lambda module, string_to_translate: string_to_translate
            self.media_item.build_file_mask_string()

        # THEN: The file mask should be generated.
        assert self.media_item.on_new_file_masks == u'Presentations (*.odp *.ppt )', \
            u'The file mask should contain the odp and ppt extensions'


