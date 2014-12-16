"""
This module contains tests for the lib submodule of the Songs plugin.
"""
from unittest import TestCase

from PyQt4 import QtCore, QtGui

from openlp.core.common import Registry, Settings
from openlp.core.lib import ServiceItem, PluginStatus
from openlp.plugins.custom.lib import CustomMediaItem
from tests.functional import patch, MagicMock
from tests.helpers.testmixin import TestMixin


class TestMediaItem(TestCase, TestMixin):
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
        with patch('openlp.core.lib.mediamanageritem.MediaManagerItem._setup'), \
                patch('openlp.core.lib.mediamanageritem.MediaManagerItem.setup_item'), \
                patch('openlp.plugins.custom.forms.editcustomform.EditCustomForm.__init__'), \
                patch('openlp.plugins.custom.lib.mediaitem.CustomMediaItem.setup_item'):
            self.media_item = CustomMediaItem(None, MagicMock())
        self.setup_application()
        self.build_settings()
        QtCore.QLocale.setDefault(QtCore.QLocale('en_GB'))

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        self.destroy_settings()

    def service_load_inactive_test(self):
        """
        Test the service load in custom with a default service item
        """
        # GIVEN: An empty Service Item
        service_item = ServiceItem(None)

        # WHEN: I search for the custom in the database
        item = self.media_item.service_load(service_item)

        # THEN: the processing should be ignored
        self.assertEqual(item, None, 'The Service item is inactive so processing should be bypassed')

    def service_load_basic_custom_test(self):
        """
        Test the service load in custom with a default service item
        """
        # GIVEN: An empty Service Item and an active plugin
        service_item = ServiceItem(None)
        self.media_item.plugin = MagicMock()
        self.media_item.plugin.status = PluginStatus.Active
        self.media_item.plugin.db_manager = MagicMock()
        self.media_item.plugin.db_manager.get_object_filtered = MagicMock()
        self.media_item.plugin.db_manager.get_object_filtered.return_value = None

        with patch('openlp.plugins.custom.lib.db.CustomSlide'):
            # WHEN: I search for the custom in the database
            item = self.media_item.service_load(service_item)

            # THEN: the processing should be ignored
            self.assertEqual(item, None, 'The Service item is inactive so processing should be bypassed')
