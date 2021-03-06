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
Package to test the openlp.core.ui.lib.listpreviewwidget package.
"""
from unittest import TestCase

from PyQt5 import QtGui

from openlp.core.common import Settings
from openlp.core.ui.lib.listpreviewwidget import ListPreviewWidget
from openlp.core.lib import ImageSource, ServiceItem

from tests.functional import MagicMock, patch, call


class TestListPreviewWidget(TestCase):

    def setUp(self):
        """
        Mock out stuff for all the tests
        """
        # Mock self.parent().width()
        self.parent_patcher = patch('openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.parent')
        self.mocked_parent = self.parent_patcher.start()
        self.mocked_parent.width.return_value = 100
        self.addCleanup(self.parent_patcher.stop)

        # Mock Settings().value()
        self.Settings_patcher = patch('openlp.core.ui.lib.listpreviewwidget.Settings')
        self.mocked_Settings = self.Settings_patcher.start()
        self.mocked_Settings_obj = MagicMock()
        self.mocked_Settings_obj.value.return_value = None
        self.mocked_Settings.return_value = self.mocked_Settings_obj
        self.addCleanup(self.Settings_patcher.stop)

        # Mock self.viewport().width()
        self.viewport_patcher = patch('openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.viewport')
        self.mocked_viewport = self.viewport_patcher.start()
        self.mocked_viewport_obj = MagicMock()
        self.mocked_viewport_obj.width.return_value = 200
        self.mocked_viewport.return_value = self.mocked_viewport_obj
        self.addCleanup(self.viewport_patcher.stop)

    def test_new_list_preview_widget(self):
        """
        Test that creating an instance of ListPreviewWidget works
        """
        # GIVEN: A ListPreviewWidget class

        # WHEN: An object is created
        list_preview_widget = ListPreviewWidget(None, 1)

        # THEN: The object is not None, and the _setup() method was called.
        self.assertIsNotNone(list_preview_widget, 'The ListPreviewWidget object should not be None')
        self.assertEquals(list_preview_widget.screen_ratio, 1, 'Should not be called')

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.image_manager')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    def test_replace_service_item_thumbs(self, mocked_setRowHeight, mocked_resizeRowsToContents,
                                         mocked_image_manager):
        """
        Test that thubmails for different slides are loaded properly in replace_service_item.
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        different ServiceItem(s), an ImageManager, and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = 0
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        # Mock Image service item
        mocked_img_service_item = MagicMock()
        mocked_img_service_item.is_text.return_value = False
        mocked_img_service_item.is_media.return_value = False
        mocked_img_service_item.is_command.return_value = False
        mocked_img_service_item.is_capable.return_value = False
        mocked_img_service_item.get_frames.return_value = [{'title': None, 'path': 'TEST1', 'image': 'FAIL'},
                                                           {'title': None, 'path': 'TEST2', 'image': 'FAIL'}]
        # Mock Command service item
        mocked_cmd_service_item = MagicMock()
        mocked_cmd_service_item.is_text.return_value = False
        mocked_cmd_service_item.is_media.return_value = False
        mocked_cmd_service_item.is_command.return_value = True
        mocked_cmd_service_item.is_capable.return_value = True
        mocked_cmd_service_item.get_frames.return_value = [{'title': None, 'path': 'FAIL', 'image': 'TEST3'},
                                                           {'title': None, 'path': 'FAIL', 'image': 'TEST4'}]
        # Mock image_manager
        mocked_image_manager.get_image.return_value = QtGui.QImage()

        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)

        # WHEN: replace_service_item is called
        list_preview_widget.replace_service_item(mocked_img_service_item, 200, 0)
        list_preview_widget.replace_service_item(mocked_cmd_service_item, 200, 0)

        # THEN: The ImageManager should be called in the appriopriate manner for each service item.
        self.assertEquals(mocked_image_manager.get_image.call_count, 4, 'Should be called once for each slide')
        calls = [call('TEST1', ImageSource.ImagePlugin), call('TEST2', ImageSource.ImagePlugin),
                 call('TEST3', ImageSource.CommandPlugins), call('TEST4', ImageSource.CommandPlugins)]
        mocked_image_manager.get_image.assert_has_calls(calls)

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    def test_replace_recalculate_layout_text(self, mocked_setRowHeight, mocked_resizeRowsToContents):
        """
        Test if "Max height for non-text slides..." enabled, txt slides unchanged in replace_service_item & __recalc...
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        a text ServiceItem and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = 100
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        # Mock text service item
        service_item = MagicMock()
        service_item.is_text.return_value = True
        service_item.get_frames.return_value = [{'title': None, 'text': None, 'verseTag': None},
                                                {'title': None, 'text': None, 'verseTag': None}]
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)
        list_preview_widget.replace_service_item(service_item, 200, 0)
        # Change viewport width before forcing a resize
        self.mocked_viewport_obj.width.return_value = 400

        # WHEN: __recalculate_layout() is called (via resizeEvent)
        list_preview_widget.resizeEvent(None)

        # THEN: setRowHeight() should not be called, while resizeRowsToContents() should be called twice
        #       (once each in __recalculate_layout and replace_service_item)
        self.assertEquals(mocked_resizeRowsToContents.call_count, 2, 'Should be called')
        self.assertEquals(mocked_setRowHeight.call_count, 0, 'Should not be called')

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    def test_replace_recalculate_layout_img(self, mocked_setRowHeight, mocked_resizeRowsToContents):
        """
        Test if "Max height for non-text slides..." disabled, img slides unchanged in replace_service_item & __recalc...
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        an image ServiceItem and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = 0
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        # Mock image service item
        service_item = MagicMock()
        service_item.is_text.return_value = False
        service_item.is_capable.return_value = False
        service_item.get_frames.return_value = [{'title': None, 'path': None, 'image': None},
                                                {'title': None, 'path': None, 'image': None}]
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)
        list_preview_widget.replace_service_item(service_item, 200, 0)
        # Change viewport width before forcing a resize
        self.mocked_viewport_obj.width.return_value = 400

        # WHEN: __recalculate_layout() is called (via resizeEvent)
        list_preview_widget.resizeEvent(None)
        self.mocked_Settings_obj.value.return_value = None
        list_preview_widget.resizeEvent(None)

        # THEN: resizeRowsToContents() should not be called, while setRowHeight() should be called
        #       twice for each slide.
        self.assertEquals(mocked_resizeRowsToContents.call_count, 0, 'Should not be called')
        self.assertEquals(mocked_setRowHeight.call_count, 6, 'Should be called 3 times for each slide')
        calls = [call(0, 200), call(1, 200), call(0, 400), call(1, 400), call(0, 400), call(1, 400)]
        mocked_setRowHeight.assert_has_calls(calls)

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    def test_replace_recalculate_layout_img_max(self, mocked_setRowHeight, mocked_resizeRowsToContents):
        """
        Test if "Max height for non-text slides..." enabled, img slides resized in replace_service_item & __recalc...
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        an image ServiceItem and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = 100
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        # Mock image service item
        service_item = MagicMock()
        service_item.is_text.return_value = False
        service_item.is_capable.return_value = False
        service_item.get_frames.return_value = [{'title': None, 'path': None, 'image': None},
                                                {'title': None, 'path': None, 'image': None}]
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)
        list_preview_widget.replace_service_item(service_item, 200, 0)
        # Change viewport width before forcing a resize
        self.mocked_viewport_obj.width.return_value = 400

        # WHEN: __recalculate_layout() is called (via resizeEvent)
        list_preview_widget.resizeEvent(None)

        # THEN: resizeRowsToContents() should not be called, while setRowHeight() should be called
        #       twice for each slide.
        self.assertEquals(mocked_resizeRowsToContents.call_count, 0, 'Should not be called')
        self.assertEquals(mocked_setRowHeight.call_count, 4, 'Should be called twice for each slide')
        calls = [call(0, 100), call(1, 100), call(0, 100), call(1, 100)]
        mocked_setRowHeight.assert_has_calls(calls)

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    def test_replace_recalculate_layout_img_auto(self, mocked_setRowHeight, mocked_resizeRowsToContents):
        """
        Test if "Max height for non-text slides..." auto, img slides resized in replace_service_item & __recalc...
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        an image ServiceItem and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = -4
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        self.mocked_viewport_obj.height.return_value = 600
        # Mock image service item
        service_item = MagicMock()
        service_item.is_text.return_value = False
        service_item.is_capable.return_value = False
        service_item.get_frames.return_value = [{'title': None, 'path': None, 'image': None},
                                                {'title': None, 'path': None, 'image': None}]
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)
        list_preview_widget.replace_service_item(service_item, 200, 0)
        # Change viewport width before forcing a resize
        self.mocked_viewport_obj.width.return_value = 400

        # WHEN: __recalculate_layout() is called (via screen_size_changed)
        list_preview_widget.screen_size_changed(1)
        self.mocked_viewport_obj.height.return_value = 200
        list_preview_widget.screen_size_changed(1)

        # THEN: resizeRowsToContents() should not be called, while setRowHeight() should be called
        #       twice for each slide.
        self.assertEquals(mocked_resizeRowsToContents.call_count, 0, 'Should not be called')
        self.assertEquals(mocked_setRowHeight.call_count, 6, 'Should be called 3 times for each slide')
        calls = [call(0, 100), call(1, 100), call(0, 150), call(1, 150), call(0, 100), call(1, 100)]
        mocked_setRowHeight.assert_has_calls(calls)

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.cellWidget')
    def test_row_resized_text(self, mocked_cellWidget, mocked_setRowHeight, mocked_resizeRowsToContents):
        """
        Test if "Max height for non-text slides..." enabled, text-based slides not affected in row_resized.
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        a text ServiceItem and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = 100
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        # Mock text service item
        service_item = MagicMock()
        service_item.is_text.return_value = True
        service_item.get_frames.return_value = [{'title': None, 'text': None, 'verseTag': None},
                                                {'title': None, 'text': None, 'verseTag': None}]
        # Mock self.cellWidget().children().setMaximumWidth()
        mocked_cellWidget_child = MagicMock()
        mocked_cellWidget_obj = MagicMock()
        mocked_cellWidget_obj.children.return_value = [None, mocked_cellWidget_child]
        mocked_cellWidget.return_value = mocked_cellWidget_obj
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)
        list_preview_widget.replace_service_item(service_item, 200, 0)

        # WHEN: row_resized() is called
        list_preview_widget.row_resized(0, 100, 150)

        # THEN: self.cellWidget(row, 0).children()[1].setMaximumWidth() should not be called
        self.assertEquals(mocked_cellWidget_child.setMaximumWidth.call_count, 0, 'Should not be called')

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.cellWidget')
    def test_row_resized_img(self, mocked_cellWidget, mocked_setRowHeight, mocked_resizeRowsToContents):
        """
        Test if "Max height for non-text slides..." disabled, image-based slides not affected in row_resized.
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        an image ServiceItem and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = 0
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        # Mock image service item
        service_item = MagicMock()
        service_item.is_text.return_value = False
        service_item.is_capable.return_value = False
        service_item.get_frames.return_value = [{'title': None, 'path': None, 'image': None},
                                                {'title': None, 'path': None, 'image': None}]
        # Mock self.cellWidget().children().setMaximumWidth()
        mocked_cellWidget_child = MagicMock()
        mocked_cellWidget_obj = MagicMock()
        mocked_cellWidget_obj.children.return_value = [None, mocked_cellWidget_child]
        mocked_cellWidget.return_value = mocked_cellWidget_obj
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)
        list_preview_widget.replace_service_item(service_item, 200, 0)

        # WHEN: row_resized() is called
        list_preview_widget.row_resized(0, 100, 150)
        self.mocked_Settings_obj.value.return_value = None
        list_preview_widget.row_resized(0, 100, 150)

        # THEN: self.cellWidget(row, 0).children()[1].setMaximumWidth() should not be called
        self.assertEquals(mocked_cellWidget_child.setMaximumWidth.call_count, 0, 'Should not be called')

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.cellWidget')
    def test_row_resized_img_max(self, mocked_cellWidget, mocked_setRowHeight, mocked_resizeRowsToContents):
        """
        Test if "Max height for non-text slides..." enabled, image-based slides are scaled in row_resized.
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        an image ServiceItem and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = 100
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        # Mock image service item
        service_item = MagicMock()
        service_item.is_text.return_value = False
        service_item.is_capable.return_value = False
        service_item.get_frames.return_value = [{'title': None, 'path': None, 'image': None},
                                                {'title': None, 'path': None, 'image': None}]
        # Mock self.cellWidget().children().setMaximumWidth()
        mocked_cellWidget_child = MagicMock()
        mocked_cellWidget_obj = MagicMock()
        mocked_cellWidget_obj.children.return_value = [None, mocked_cellWidget_child]
        mocked_cellWidget.return_value = mocked_cellWidget_obj
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)
        list_preview_widget.replace_service_item(service_item, 200, 0)

        # WHEN: row_resized() is called
        list_preview_widget.row_resized(0, 100, 150)

        # THEN: self.cellWidget(row, 0).children()[1].setMaximumWidth() should be called
        mocked_cellWidget_child.setMaximumWidth.assert_called_once_with(150)

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.resizeRowsToContents')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.setRowHeight')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.cellWidget')
    def test_row_resized_setting_changed(self, mocked_cellWidget, mocked_setRowHeight, mocked_resizeRowsToContents):
        """
        Test if "Max height for non-text slides..." enabled while item live, program doesn't crash on row_resized.
        """
        # GIVEN: A setting to adjust "Max height for non-text slides in slide controller",
        #        an image ServiceItem and a ListPreviewWidget.

        # Mock Settings().value('advanced/slide max height')
        self.mocked_Settings_obj.value.return_value = 0
        # Mock self.viewport().width()
        self.mocked_viewport_obj.width.return_value = 200
        # Mock image service item
        service_item = MagicMock()
        service_item.is_text.return_value = False
        service_item.is_capable.return_value = False
        service_item.get_frames.return_value = [{'title': None, 'path': None, 'image': None},
                                                {'title': None, 'path': None, 'image': None}]
        # Mock self.cellWidget().children()
        mocked_cellWidget_obj = MagicMock()
        mocked_cellWidget_obj.children.return_value = None
        mocked_cellWidget.return_value = mocked_cellWidget_obj
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)
        list_preview_widget.replace_service_item(service_item, 200, 0)
        self.mocked_Settings_obj.value.return_value = 100

        # WHEN: row_resized() is called
        list_preview_widget.row_resized(0, 100, 150)

        # THEN: self.cellWidget(row, 0).children()[1].setMaximumWidth() should fail
        self.assertRaises(Exception)

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.selectRow')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.scrollToItem')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.item')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.slide_count')
    def test_autoscroll_setting_invalid(self, mocked_slide_count, mocked_item, mocked_scrollToItem, mocked_selectRow):
        """
        Test if 'advanced/autoscrolling' setting None or invalid, that no autoscrolling occurs on change_slide().
        """
        # GIVEN: A setting for autoscrolling and a ListPreviewWidget.
        # Mock Settings().value('advanced/autoscrolling')
        self.mocked_Settings_obj.value.return_value = None
        # Mocked returns
        mocked_slide_count.return_value = 1
        mocked_item.return_value = None
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)

        # WHEN: change_slide() is called
        list_preview_widget.change_slide(0)
        self.mocked_Settings_obj.value.return_value = 1
        list_preview_widget.change_slide(0)
        self.mocked_Settings_obj.value.return_value = {'fail': 1}
        list_preview_widget.change_slide(0)
        self.mocked_Settings_obj.value.return_value = {'dist': 1, 'fail': 1}
        list_preview_widget.change_slide(0)
        self.mocked_Settings_obj.value.return_value = {'dist': 'fail', 'pos': 1}
        list_preview_widget.change_slide(0)
        self.mocked_Settings_obj.value.return_value = {'dist': 1, 'pos': 'fail'}
        list_preview_widget.change_slide(0)

        # THEN: no further functions should be called
        self.assertEquals(mocked_slide_count.call_count, 0, 'Should not be called')
        self.assertEquals(mocked_scrollToItem.call_count, 0, 'Should not be called')
        self.assertEquals(mocked_selectRow.call_count, 0, 'Should not be called')
        self.assertEquals(mocked_item.call_count, 0, 'Should not be called')

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.selectRow')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.scrollToItem')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.item')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.slide_count')
    def test_autoscroll_dist_bounds(self, mocked_slide_count, mocked_item, mocked_scrollToItem, mocked_selectRow):
        """
        Test if 'advanced/autoscrolling' setting asks to scroll beyond list bounds, that it does not beyond.
        """
        # GIVEN: A setting for autoscrolling and a ListPreviewWidget.
        # Mock Settings().value('advanced/autoscrolling')
        self.mocked_Settings_obj.value.return_value = {'dist': -1, 'pos': 1}
        # Mocked returns
        mocked_slide_count.return_value = 1
        mocked_item.return_value = None
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)

        # WHEN: change_slide() is called
        list_preview_widget.change_slide(0)
        self.mocked_Settings_obj.value.return_value = {'dist': 1, 'pos': 1}
        list_preview_widget.change_slide(0)

        # THEN: no further functions should be called
        self.assertEquals(mocked_slide_count.call_count, 3, 'Should be called')
        self.assertEquals(mocked_scrollToItem.call_count, 2, 'Should be called')
        self.assertEquals(mocked_selectRow.call_count, 2, 'Should be called')
        self.assertEquals(mocked_item.call_count, 2, 'Should be called')
        calls = [call(0, 0), call(0, 0)]
        mocked_item.assert_has_calls(calls)

    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.selectRow')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.scrollToItem')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.item')
    @patch(u'openlp.core.ui.lib.listpreviewwidget.ListPreviewWidget.slide_count')
    def test_autoscroll_normal(self, mocked_slide_count, mocked_item, mocked_scrollToItem, mocked_selectRow):
        """
        Test if 'advanced/autoscrolling' setting valid, autoscrolling called as expected.
        """
        # GIVEN: A setting for autoscrolling and a ListPreviewWidget.
        # Mock Settings().value('advanced/autoscrolling')
        self.mocked_Settings_obj.value.return_value = {'dist': -1, 'pos': 1}
        # Mocked returns
        mocked_slide_count.return_value = 3
        mocked_item.return_value = None
        # init ListPreviewWidget and load service item
        list_preview_widget = ListPreviewWidget(None, 1)

        # WHEN: change_slide() is called
        list_preview_widget.change_slide(1)
        self.mocked_Settings_obj.value.return_value = {'dist': 0, 'pos': 1}
        list_preview_widget.change_slide(1)
        self.mocked_Settings_obj.value.return_value = {'dist': 1, 'pos': 1}
        list_preview_widget.change_slide(1)

        # THEN: no further functions should be called
        self.assertEquals(mocked_slide_count.call_count, 3, 'Should be called')
        self.assertEquals(mocked_scrollToItem.call_count, 3, 'Should be called')
        self.assertEquals(mocked_selectRow.call_count, 3, 'Should be called')
        self.assertEquals(mocked_item.call_count, 3, 'Should be called')
        calls = [call(0, 0), call(1, 0), call(2, 0)]
        mocked_item.assert_has_calls(calls)
