# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2016 OpenLP Developers                                   #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
Package to test the openlp.core.ui.slidecontroller package.
"""
import os
from unittest import TestCase

import PyQt5

from openlp.core.common import Registry, ThemeLevel
from openlp.core.lib import ServiceItem, ServiceItemType, ItemCapabilities
from openlp.core.ui import ServiceManager

from tests.functional import MagicMock, patch


class TestServiceManager(TestCase):
    """
    Test the service manager
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()

    def test_initial_service_manager(self):
        """
        Test the initial of service manager.
        """
        # GIVEN: A new service manager instance.
        ServiceManager(None)
        # WHEN: the default service manager is built.
        # THEN: The the controller should be registered in the registry.
        self.assertNotEqual(Registry().get('service_manager'), None, 'The base service manager should be registered')

    def test_create_basic_service(self):
        """
        Test the create basic service array
        """
        # GIVEN: A new service manager instance.
        service_manager = ServiceManager(None)
        # WHEN: when the basic service array is created.
        service_manager._save_lite = False
        service_manager.service_theme = 'test_theme'
        service = service_manager.create_basic_service()[0]
        # THEN: The controller should be registered in the registry.
        self.assertNotEqual(service, None, 'The base service should be created')
        self.assertEqual(service['openlp_core']['service-theme'], 'test_theme', 'The test theme should be saved')
        self.assertEqual(service['openlp_core']['lite-service'], False, 'The lite service should be saved')

    def test_supported_suffixes(self):
        """
        Test the create basic service array
        """
        # GIVEN: A new service manager instance.
        service_manager = ServiceManager(None)
        # WHEN: a suffix is added as an individual or a list.
        service_manager.supported_suffixes('txt')
        service_manager.supported_suffixes(['pptx', 'ppt'])
        # THEN: The suffixes should be available to test.
        self.assertEqual('txt' in service_manager.suffixes, True, 'The suffix txt should be in the list')
        self.assertEqual('ppt' in service_manager.suffixes, True, 'The suffix ppt should be in the list')
        self.assertEqual('pptx' in service_manager.suffixes, True, 'The suffix pptx should be in the list')

    def test_build_context_menu(self):
        """
        Test the creation of a context menu from a null service item.
        """
        # GIVEN: A new service manager instance and a default service item.
        service_manager = ServiceManager(None)
        item = MagicMock()
        item.parent.return_value = False
        item.data.return_value = 0
        service_manager.service_manager_list = MagicMock()
        service_manager.service_manager_list.itemAt.return_value = item
        service_item = ServiceItem(None)
        service_manager.service_items.insert(1, {'service_item': service_item})
        service_manager.edit_action = MagicMock()
        service_manager.rename_action = MagicMock()
        service_manager.create_custom_action = MagicMock()
        service_manager.maintain_action = MagicMock()
        service_manager.notes_action = MagicMock()
        service_manager.time_action = MagicMock()
        service_manager.auto_start_action = MagicMock()
        service_manager.auto_play_slides_menu = MagicMock()
        service_manager.auto_play_slides_once = MagicMock()
        service_manager.auto_play_slides_loop = MagicMock()
        service_manager.timed_slide_interval = MagicMock()
        service_manager.theme_menu = MagicMock()
        service_manager.menu = MagicMock()
        # WHEN I define a context menu
        service_manager.context_menu(1)
        # THEN the following calls should have occurred.
        self.assertEqual(service_manager.edit_action.setVisible.call_count, 1, 'Should have been called once')
        self.assertEqual(service_manager.rename_action.setVisible.call_count, 1, 'Should have been called once')
        self.assertEqual(service_manager.create_custom_action.setVisible.call_count, 1, 'Should have been called once')
        self.assertEqual(service_manager.maintain_action.setVisible.call_count, 1, 'Should have been called once')
        self.assertEqual(service_manager.notes_action.setVisible.call_count, 1, 'Should have been called once')
        self.assertEqual(service_manager.time_action.setVisible.call_count, 1, 'Should have been called once')
        self.assertEqual(service_manager.auto_start_action.setVisible.call_count, 1, 'Should have been called once')
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 1,
                         'Should have been called once')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.theme_menu.menuAction().setVisible.call_count, 1,
                         'Should have been called once')

    def test_build_song_context_menu(self):
        """
        Test the creation of a context menu from service item of type text from Songs.
        """
        # GIVEN: A new service manager instance and a default service item.
        mocked_renderer = MagicMock()
        mocked_renderer.theme_level = ThemeLevel.Song
        Registry().register('plugin_manager', MagicMock())
        Registry().register('renderer', mocked_renderer)
        service_manager = ServiceManager(None)
        item = MagicMock()
        item.parent.return_value = False
        item.data.return_value = 0
        service_manager.service_manager_list = MagicMock()
        service_manager.service_manager_list.itemAt.return_value = item
        service_item = ServiceItem(None)
        for capability in [ItemCapabilities.CanEdit, ItemCapabilities.CanPreview, ItemCapabilities.CanLoop,
                           ItemCapabilities.OnLoadUpdate, ItemCapabilities.AddIfNewItem,
                           ItemCapabilities.CanSoftBreak]:
            service_item.add_capability(capability)
        service_item.service_item_type = ServiceItemType.Text
        service_item.edit_id = 1
        service_item._display_frames.append(MagicMock())
        service_manager.service_items.insert(1, {'service_item': service_item})
        service_manager.edit_action = MagicMock()
        service_manager.rename_action = MagicMock()
        service_manager.create_custom_action = MagicMock()
        service_manager.maintain_action = MagicMock()
        service_manager.notes_action = MagicMock()
        service_manager.time_action = MagicMock()
        service_manager.auto_start_action = MagicMock()
        service_manager.auto_play_slides_menu = MagicMock()
        service_manager.auto_play_slides_once = MagicMock()
        service_manager.auto_play_slides_loop = MagicMock()
        service_manager.timed_slide_interval = MagicMock()
        service_manager.theme_menu = MagicMock()
        service_manager.menu = MagicMock()
        # WHEN I define a context menu
        service_manager.context_menu(1)
        # THEN the following calls should have occurred.
        self.assertEqual(service_manager.edit_action.setVisible.call_count, 2, 'Should have be called twice')
        self.assertEqual(service_manager.rename_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.create_custom_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.maintain_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.notes_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.time_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_start_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 1,
                         'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.theme_menu.menuAction().setVisible.call_count, 2,
                         'Should have be called twice')
        # THEN we add a 2nd display frame
        service_item._display_frames.append(MagicMock())
        service_manager.context_menu(1)
        # THEN the following additional calls should have occurred.
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 2,
                         'Should have be called twice')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 1, 'Should have be called once')

    def test_build_bible_context_menu(self):
        """
        Test the creation of a context menu from service item of type text from Bibles.
        """
        # GIVEN: A new service manager instance and a default service item.
        mocked_renderer = MagicMock()
        mocked_renderer.theme_level = ThemeLevel.Song
        Registry().register('plugin_manager', MagicMock())
        Registry().register('renderer', mocked_renderer)
        service_manager = ServiceManager(None)
        item = MagicMock()
        item.parent.return_value = False
        item.data.return_value = 0
        service_manager.service_manager_list = MagicMock()
        service_manager.service_manager_list.itemAt.return_value = item
        service_item = ServiceItem(None)
        for capability in [ItemCapabilities.NoLineBreaks, ItemCapabilities.CanPreview,
                           ItemCapabilities.CanLoop, ItemCapabilities.CanWordSplit,
                           ItemCapabilities.CanEditTitle]:
            service_item.add_capability(capability)
        service_item.service_item_type = ServiceItemType.Text
        service_item.edit_id = 1
        service_item._display_frames.append(MagicMock())
        service_manager.service_items.insert(1, {'service_item': service_item})
        service_manager.edit_action = MagicMock()
        service_manager.rename_action = MagicMock()
        service_manager.create_custom_action = MagicMock()
        service_manager.maintain_action = MagicMock()
        service_manager.notes_action = MagicMock()
        service_manager.time_action = MagicMock()
        service_manager.auto_start_action = MagicMock()
        service_manager.auto_play_slides_menu = MagicMock()
        service_manager.auto_play_slides_once = MagicMock()
        service_manager.auto_play_slides_loop = MagicMock()
        service_manager.timed_slide_interval = MagicMock()
        service_manager.theme_menu = MagicMock()
        service_manager.menu = MagicMock()
        # WHEN I define a context menu
        service_manager.context_menu(1)
        # THEN the following calls should have occurred.
        self.assertEqual(service_manager.edit_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.rename_action.setVisible.call_count, 2, 'Should have be called twice')
        self.assertEqual(service_manager.create_custom_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.maintain_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.notes_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.time_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_start_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 1,
                         'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.theme_menu.menuAction().setVisible.call_count, 2,
                         'Should have be called twice')
        # THEN we add a 2nd display frame
        service_item._display_frames.append(MagicMock())
        service_manager.context_menu(1)
        # THEN the following additional calls should have occurred.
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 2,
                         'Should have be called twice')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 1, 'Should have be called once')

    def test_build_custom_context_menu(self):
        """
        Test the creation of a context menu from service item of type text from Custom.
        """
        # GIVEN: A new service manager instance and a default service item.
        mocked_renderer = MagicMock()
        mocked_renderer.theme_level = ThemeLevel.Song
        Registry().register('plugin_manager', MagicMock())
        Registry().register('renderer', mocked_renderer)
        service_manager = ServiceManager(None)
        item = MagicMock()
        item.parent.return_value = False
        item.data.return_value = 0
        service_manager.service_manager_list = MagicMock()
        service_manager.service_manager_list.itemAt.return_value = item
        service_item = ServiceItem(None)
        service_item.add_capability(ItemCapabilities.CanEdit)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.CanSoftBreak)
        service_item.add_capability(ItemCapabilities.OnLoadUpdate)
        service_item.service_item_type = ServiceItemType.Text
        service_item.edit_id = 1
        service_item._display_frames.append(MagicMock())
        service_manager.service_items.insert(1, {'service_item': service_item})
        service_manager.edit_action = MagicMock()
        service_manager.rename_action = MagicMock()
        service_manager.create_custom_action = MagicMock()
        service_manager.maintain_action = MagicMock()
        service_manager.notes_action = MagicMock()
        service_manager.time_action = MagicMock()
        service_manager.auto_start_action = MagicMock()
        service_manager.auto_play_slides_menu = MagicMock()
        service_manager.auto_play_slides_once = MagicMock()
        service_manager.auto_play_slides_loop = MagicMock()
        service_manager.timed_slide_interval = MagicMock()
        service_manager.theme_menu = MagicMock()
        service_manager.menu = MagicMock()
        # WHEN I define a context menu
        service_manager.context_menu(1)
        # THEN the following calls should have occurred.
        self.assertEqual(service_manager.edit_action.setVisible.call_count, 2, 'Should have be called twice')
        self.assertEqual(service_manager.rename_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.create_custom_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.maintain_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.notes_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.time_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_start_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.theme_menu.menuAction().setVisible.call_count, 2,
                          'Should have be called twice')
        # THEN we add a 2nd display frame
        service_item._display_frames.append(MagicMock())
        service_manager.context_menu(1)
        # THEN the following additional calls should have occurred.
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 2,
                          'Should have be called twice')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 1, 'Should have be called once')

    def test_build_image_context_menu(self):
        """
        Test the creation of a context menu from service item of type Image from Image.
        """
        # GIVEN: A new service manager instance and a default service item.
        Registry().register('plugin_manager', MagicMock())
        Registry().register('renderer', MagicMock())
        service_manager = ServiceManager(None)
        item = MagicMock()
        item.parent.return_value = False
        item.data.return_value = 0
        service_manager.service_manager_list = MagicMock()
        service_manager.service_manager_list.itemAt.return_value = item
        service_item = ServiceItem(None)
        service_item.add_capability(ItemCapabilities.CanMaintain)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.CanAppend)
        service_item.add_capability(ItemCapabilities.CanEditTitle)
        service_item.service_item_type = ServiceItemType.Image
        service_item.edit_id = 1
        service_item._raw_frames.append(MagicMock())
        service_manager.service_items.insert(1, {'service_item': service_item})
        service_manager.edit_action = MagicMock()
        service_manager.rename_action = MagicMock()
        service_manager.create_custom_action = MagicMock()
        service_manager.maintain_action = MagicMock()
        service_manager.notes_action = MagicMock()
        service_manager.time_action = MagicMock()
        service_manager.auto_start_action = MagicMock()
        service_manager.auto_play_slides_menu = MagicMock()
        service_manager.auto_play_slides_once = MagicMock()
        service_manager.auto_play_slides_loop = MagicMock()
        service_manager.timed_slide_interval = MagicMock()
        service_manager.theme_menu = MagicMock()
        service_manager.menu = MagicMock()
        # WHEN I define a context menu
        service_manager.context_menu(1)
        # THEN the following calls should have occurred.
        self.assertEqual(service_manager.edit_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.rename_action.setVisible.call_count, 2, 'Should have be called twice')
        self.assertEqual(service_manager.create_custom_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.maintain_action.setVisible.call_count, 2, 'Should have be called twice')
        self.assertEqual(service_manager.notes_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.time_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_start_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.theme_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')
        # THEN we add a 2nd display frame and regenerate the menu.
        service_item._raw_frames.append(MagicMock())
        service_manager.context_menu(1)
        # THEN the following additional calls should have occurred.
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 2,
                          'Should have be called twice')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 1, 'Should have be called once')

    def test_build_media_context_menu(self):
        """
        Test the creation of a context menu from service item of type Command from Media.
        """
        # GIVEN: A new service manager instance and a default service item.
        Registry().register('plugin_manager', MagicMock())
        Registry().register('renderer', MagicMock())
        service_manager = ServiceManager(None)
        item = MagicMock()
        item.parent.return_value = False
        item.data.return_value = 0
        service_manager.service_manager_list = MagicMock()
        service_manager.service_manager_list.itemAt.return_value = item
        service_item = ServiceItem(None)
        service_item.add_capability(ItemCapabilities.CanAutoStartForLive)
        service_item.add_capability(ItemCapabilities.CanEditTitle)
        service_item.add_capability(ItemCapabilities.RequiresMedia)
        service_item.service_item_type = ServiceItemType.Command
        service_item.edit_id = 1
        service_item._raw_frames.append(MagicMock())
        service_manager.service_items.insert(1, {'service_item': service_item})
        service_manager.edit_action = MagicMock()
        service_manager.rename_action = MagicMock()
        service_manager.create_custom_action = MagicMock()
        service_manager.maintain_action = MagicMock()
        service_manager.notes_action = MagicMock()
        service_manager.time_action = MagicMock()
        service_manager.auto_start_action = MagicMock()
        service_manager.auto_play_slides_menu = MagicMock()
        service_manager.auto_play_slides_once = MagicMock()
        service_manager.auto_play_slides_loop = MagicMock()
        service_manager.timed_slide_interval = MagicMock()
        service_manager.theme_menu = MagicMock()
        service_manager.menu = MagicMock()
        # WHEN I define a context menu
        service_manager.context_menu(1)
        # THEN the following calls should have occurred.
        self.assertEqual(service_manager.edit_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.rename_action.setVisible.call_count, 2, 'Should have be called twice')
        self.assertEqual(service_manager.create_custom_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.maintain_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.notes_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.time_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_start_action.setVisible.call_count, 2, 'Should have be called twice')
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.theme_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')
        # THEN I change the length of the media and regenerate the menu.
        service_item.set_media_length(5)
        service_manager.context_menu(1)
        # THEN the following additional calls should have occurred.
        self.assertEqual(service_manager.time_action.setVisible.call_count, 3, 'Should have be called three times')

    def test_build_presentation_pdf_context_menu(self):
        """
        Test the creation of a context menu from service item of type Command with PDF from Presentation.
        """
        # GIVEN: A new service manager instance and a default service item.
        Registry().register('plugin_manager', MagicMock())
        Registry().register('renderer', MagicMock())
        service_manager = ServiceManager(None)
        item = MagicMock()
        item.parent.return_value = False
        item.data.return_value = 0
        service_manager.service_manager_list = MagicMock()
        service_manager.service_manager_list.itemAt.return_value = item
        service_item = ServiceItem(None)
        service_item.add_capability(ItemCapabilities.CanMaintain)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.CanAppend)
        service_item.service_item_type = ServiceItemType.Command
        service_item.edit_id = 1
        service_item._raw_frames.append(MagicMock())
        service_manager.service_items.insert(1, {'service_item': service_item})
        service_manager.edit_action = MagicMock()
        service_manager.rename_action = MagicMock()
        service_manager.create_custom_action = MagicMock()
        service_manager.maintain_action = MagicMock()
        service_manager.notes_action = MagicMock()
        service_manager.time_action = MagicMock()
        service_manager.auto_start_action = MagicMock()
        service_manager.auto_play_slides_menu = MagicMock()
        service_manager.auto_play_slides_once = MagicMock()
        service_manager.auto_play_slides_loop = MagicMock()
        service_manager.timed_slide_interval = MagicMock()
        service_manager.theme_menu = MagicMock()
        service_manager.menu = MagicMock()
        # WHEN I define a context menu
        service_manager.context_menu(1)
        # THEN the following calls should have occurred.
        self.assertEqual(service_manager.edit_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.rename_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.create_custom_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.maintain_action.setVisible.call_count, 2, 'Should have be called twice')
        self.assertEqual(service_manager.notes_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.time_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_start_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.theme_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')

    def test_build_presentation_non_pdf_context_menu(self):
        """
        Test the creation of a context menu from service item of type Command with Impress from Presentation.
        """
        # GIVEN: A new service manager instance and a default service item.
        Registry().register('plugin_manager', MagicMock())
        Registry().register('renderer', MagicMock())
        service_manager = ServiceManager(None)
        item = MagicMock()
        item.parent.return_value = False
        item.data.return_value = 0
        service_manager.service_manager_list = MagicMock()
        service_manager.service_manager_list.itemAt.return_value = item
        service_item = ServiceItem(None)
        service_item.add_capability(ItemCapabilities.ProvidesOwnDisplay)
        service_item.service_item_type = ServiceItemType.Command
        service_item.edit_id = 1
        service_item._raw_frames.append(MagicMock())
        service_manager.service_items.insert(1, {'service_item': service_item})
        service_manager.edit_action = MagicMock()
        service_manager.rename_action = MagicMock()
        service_manager.create_custom_action = MagicMock()
        service_manager.maintain_action = MagicMock()
        service_manager.notes_action = MagicMock()
        service_manager.time_action = MagicMock()
        service_manager.auto_start_action = MagicMock()
        service_manager.auto_play_slides_menu = MagicMock()
        service_manager.auto_play_slides_once = MagicMock()
        service_manager.auto_play_slides_loop = MagicMock()
        service_manager.timed_slide_interval = MagicMock()
        service_manager.theme_menu = MagicMock()
        service_manager.menu = MagicMock()
        # WHEN I define a context menu
        service_manager.context_menu(1)
        # THEN the following calls should have occurred.
        self.assertEqual(service_manager.edit_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.rename_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.create_custom_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.maintain_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.notes_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.time_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_start_action.setVisible.call_count, 1, 'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')
        self.assertEqual(service_manager.auto_play_slides_once.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.auto_play_slides_loop.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.timed_slide_interval.setChecked.call_count, 0, 'Should not be called')
        self.assertEqual(service_manager.theme_menu.menuAction().setVisible.call_count, 1,
                          'Should have be called once')

    @patch(u'openlp.core.ui.servicemanager.Settings')
    @patch(u'PyQt5.QtCore.QTimer.singleShot')
    def test_single_click_preview_true(self, mocked_singleShot, MockedSettings):
        """
        Test that when "Preview items when clicked in Service Manager" enabled the preview timer starts
        """
        # GIVEN: A setting to enable "Preview items when clicked in Service Manager" and a service manager.
        mocked_settings = MagicMock()
        mocked_settings.value.return_value = True
        MockedSettings.return_value = mocked_settings
        service_manager = ServiceManager(None)
        # WHEN: on_single_click_preview() is called
        service_manager.on_single_click_preview()
        # THEN: timer should have been started
        mocked_singleShot.assert_called_with(PyQt5.QtWidgets.QApplication.instance().doubleClickInterval(),
                                             service_manager.on_single_click_preview_timeout)

    @patch(u'openlp.core.ui.servicemanager.Settings')
    @patch(u'PyQt5.QtCore.QTimer.singleShot')
    def test_single_click_preview_false(self, mocked_singleShot, MockedSettings):
        """
        Test that when "Preview items when clicked in Service Manager" disabled the preview timer doesn't start
        """
        # GIVEN: A setting to enable "Preview items when clicked in Service Manager" and a service manager.
        mocked_settings = MagicMock()
        mocked_settings.value.return_value = False
        MockedSettings.return_value = mocked_settings
        service_manager = ServiceManager(None)
        # WHEN: on_single_click_preview() is called
        service_manager.on_single_click_preview()
        # THEN: timer should not be started
        self.assertEqual(mocked_singleShot.call_count, 0, 'Should not be called')

    @patch(u'openlp.core.ui.servicemanager.Settings')
    @patch(u'PyQt5.QtCore.QTimer.singleShot')
    @patch(u'openlp.core.ui.servicemanager.ServiceManager.make_live')
    def test_single_click_preview_double(self, mocked_make_live, mocked_singleShot, MockedSettings):
        """
        Test that when a double click has registered the preview timer doesn't start
        """
        # GIVEN: A setting to enable "Preview items when clicked in Service Manager" and a service manager.
        mocked_settings = MagicMock()
        mocked_settings.value.return_value = True
        MockedSettings.return_value = mocked_settings
        service_manager = ServiceManager(None)
        # WHEN: on_single_click_preview() is called following a double click
        service_manager.on_double_click_live()
        service_manager.on_single_click_preview()
        # THEN: timer should not be started
        mocked_make_live.assert_called_with()
        self.assertEqual(mocked_singleShot.call_count, 0, 'Should not be called')

    @patch(u'openlp.core.ui.servicemanager.ServiceManager.make_preview')
    def test_single_click_timeout_single(self, mocked_make_preview):
        """
        Test that when a single click has been registered, the item is sent to preview
        """
        # GIVEN: A service manager.
        service_manager = ServiceManager(None)
        # WHEN: on_single_click_preview() is called
        service_manager.on_single_click_preview_timeout()
        # THEN: make_preview() should have been called
        self.assertEqual(mocked_make_preview.call_count, 1, 'ServiceManager.make_preview() should have been called once')

    @patch(u'openlp.core.ui.servicemanager.ServiceManager.make_preview')
    @patch(u'openlp.core.ui.servicemanager.ServiceManager.make_live')
    def test_single_click_timeout_double(self, mocked_make_live, mocked_make_preview):
        """
        Test that when a double click has been registered, the item does not goes to preview
        """
        # GIVEN: A service manager.
        service_manager = ServiceManager(None)
        # WHEN: on_single_click_preview() is called after a double click
        service_manager.on_double_click_live()
        service_manager.on_single_click_preview_timeout()
        # THEN: make_preview() should not have been called
        self.assertEqual(mocked_make_preview.call_count, 0, 'ServiceManager.make_preview() should not be called')

    @patch(u'openlp.core.ui.servicemanager.shutil.copy')
    @patch(u'openlp.core.ui.servicemanager.zipfile')
    @patch(u'openlp.core.ui.servicemanager.ServiceManager.save_file_as')
    def test_save_file_raises_permission_error(self, mocked_save_file_as, mocked_zipfile, mocked_shutil_copy):
        """
        Test that when a PermissionError is raised when trying to save a file, it is handled correctly
        """
        # GIVEN: A service manager, a service to save
        mocked_main_window = MagicMock()
        mocked_main_window.service_manager_settings_section = 'servicemanager'
        Registry().register('main_window', mocked_main_window)
        Registry().register('application', MagicMock())
        service_manager = ServiceManager(None)
        service_manager._file_name = os.path.join('temp', 'filename.osz')
        service_manager._save_lite = False
        service_manager.service_items = []
        service_manager.service_theme = 'Default'
        service_manager.service_manager_list = MagicMock()
        mocked_save_file_as.return_value = True
        mocked_zipfile.ZipFile.return_value = MagicMock()
        mocked_shutil_copy.side_effect = PermissionError

        # WHEN: The service is saved and a PermissionError is thrown
        result = service_manager.save_file()

        # THEN: The "save_as" method is called to save the service
        self.assertTrue(result)
        mocked_save_file_as.assert_called_with()

    @patch(u'openlp.core.ui.servicemanager.shutil.copy')
    @patch(u'openlp.core.ui.servicemanager.zipfile')
    @patch(u'openlp.core.ui.servicemanager.ServiceManager.save_file_as')
    def test_save_local_file_raises_permission_error(self, mocked_save_file_as, mocked_zipfile, mocked_shutil_copy):
        """
        Test that when a PermissionError is raised when trying to save a local file, it is handled correctly
        """
        # GIVEN: A service manager, a service to save
        mocked_main_window = MagicMock()
        mocked_main_window.service_manager_settings_section = 'servicemanager'
        Registry().register('main_window', mocked_main_window)
        Registry().register('application', MagicMock())
        service_manager = ServiceManager(None)
        service_manager._file_name = os.path.join('temp', 'filename.osz')
        service_manager._save_lite = False
        service_manager.service_items = []
        service_manager.service_theme = 'Default'
        mocked_save_file_as.return_value = True
        mocked_zipfile.ZipFile.return_value = MagicMock()
        mocked_shutil_copy.side_effect = PermissionError

        # WHEN: The service is saved and a PermissionError is thrown
        result = service_manager.save_local_file()

        # THEN: The "save_as" method is called to save the service
        self.assertTrue(result)
        mocked_save_file_as.assert_called_with()

