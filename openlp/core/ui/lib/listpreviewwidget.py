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
The :mod:`listpreviewwidget` is a widget that lists the slides in the slide controller.
It is based on a QTableWidget but represents its contents in list form.
"""

from PyQt5 import QtCore, QtGui, QtWidgets

from openlp.core.common import RegistryProperties, Settings
from openlp.core.lib import ImageSource, ItemCapabilities, ServiceItem


class ListPreviewWidget(QtWidgets.QTableWidget, RegistryProperties):
    """
    A special type of QTableWidget which lists the slides in the slide controller

    :param parent:
    :param screen_ratio:
    """

    def __init__(self, parent, screen_ratio):
        """
        Initializes the widget to default state.

        An empty ``ServiceItem`` is used by default. replace_service_manager_item() needs to be called to make this
        widget display something.
        """
        super(QtWidgets.QTableWidget, self).__init__(parent)
        self._setup(screen_ratio)

    def _setup(self, screen_ratio):
        """
        Set up the widget
        """
        self.setColumnCount(1)
        self.horizontalHeader().setVisible(False)
        self.setColumnWidth(0, self.parent().width())
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setAlternatingRowColors(True)
        # Initialize variables.
        self.service_item = ServiceItem()
        self.screen_ratio = screen_ratio
        self.auto_row_height = 100
        # Connect signals
        self.verticalHeader().sectionResized.connect(self.row_resized)

    def resizeEvent(self, event):
        """
        Overloaded method from QTableWidget. Will recalculate the layout.
        """
        self.__recalculate_layout()

    def __recalculate_layout(self):
        """
        Recalculates the layout of the table widget. It will set height and width
        of the table cells. QTableWidget does not adapt the cells to the widget size on its own.
        """
        self.setColumnWidth(0, self.viewport().width())
        if self.service_item:
            # Sort out songs, bibles, etc.
            if self.service_item.is_text():
                self.resizeRowsToContents()
            # Sort out image heights.
            else:
                height = self.viewport().width() // self.screen_ratio
                max_img_row_height = Settings().value('advanced/slide max height')
                # Adjust for row height cap if in use.
                if isinstance(max_img_row_height, int):
                    if max_img_row_height > 0 and height > max_img_row_height:
                        height = max_img_row_height
                    elif max_img_row_height < 0:
                        # If auto setting, show that number of slides, or if the resulting slides too small, 100px.
                        # E.g. If setting is -4, 4 slides will be visible, unless those slides are < 100px high.
                        self.auto_row_height = max(self.viewport().height() / (-1 * max_img_row_height), 100)
                        height = min(height, self.auto_row_height)
                # Apply new height to slides
                for frame_number in range(len(self.service_item.get_frames())):
                    self.setRowHeight(frame_number, height)

    def row_resized(self, row, old_height, new_height):
        """
        Will scale non-image slides.
        """
        # Only for non-text slides when row height cap in use
        max_img_row_height = Settings().value('advanced/slide max height')
        if self.service_item.is_text() or not isinstance(max_img_row_height, int) or max_img_row_height == 0:
            return
        # Get and validate label widget containing slide & adjust max width
        try:
            self.cellWidget(row, 0).children()[1].setMaximumWidth(new_height * self.screen_ratio)
        except:
            return

    def screen_size_changed(self, screen_ratio):
        """
        This method is called whenever the live screen size changes, which then makes a layout recalculation necessary

        :param screen_ratio: The new screen ratio
        """
        self.screen_ratio = screen_ratio
        self.__recalculate_layout()

    def replace_service_item(self, service_item, width, slide_number):
        """
        Replace the current preview items with the ones in service_item and display the given slide

        :param service_item: The service item to insert
        :param width: The width of the column
        :param slide_number: The slide number to pre-select
        """
        self.service_item = service_item
        self.setRowCount(0)
        self.clear()
        self.setColumnWidth(0, width)
        row = 0
        text = []
        for frame_number, frame in enumerate(self.service_item.get_frames()):
            self.setRowCount(self.slide_count() + 1)
            item = QtWidgets.QTableWidgetItem()
            slide_height = 0
            if self.service_item.is_text():
                if frame['verseTag']:
                    # These tags are already translated.
                    verse_def = frame['verseTag']
                    verse_def = '%s%s' % (verse_def[0], verse_def[1:])
                    two_line_def = '%s\n%s' % (verse_def[0], verse_def[1:])
                    row = two_line_def
                else:
                    row += 1
                item.setText(frame['text'])
            else:
                label = QtWidgets.QLabel()
                label.setContentsMargins(4, 4, 4, 4)
                if self.service_item.is_media():
                    label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                else:
                    label.setScaledContents(True)
                if self.service_item.is_command():
                    if self.service_item.is_capable(ItemCapabilities.HasThumbnails):
                        image = self.image_manager.get_image(frame['image'], ImageSource.CommandPlugins)
                        pixmap = QtGui.QPixmap.fromImage(image)
                    else:
                        pixmap = QtGui.QPixmap(frame['image'])
                else:
                    image = self.image_manager.get_image(frame['path'], ImageSource.ImagePlugin)
                    pixmap = QtGui.QPixmap.fromImage(image)
                pixmap.setDevicePixelRatio(label.devicePixelRatio())
                label.setPixmap(pixmap)
                slide_height = width // self.screen_ratio
                # Setup and validate row height cap if in use.
                max_img_row_height = Settings().value('advanced/slide max height')
                if isinstance(max_img_row_height, int) and max_img_row_height != 0:
                    if max_img_row_height > 0 and slide_height > max_img_row_height:
                        # Manual Setting
                        slide_height = max_img_row_height
                    elif max_img_row_height < 0 and slide_height > self.auto_row_height:
                        # Auto Setting
                        slide_height = self.auto_row_height
                    label.setMaximumWidth(slide_height * self.screen_ratio)
                    label.resize(slide_height * self.screen_ratio, slide_height)
                    # Build widget with stretch padding
                    container = QtWidgets.QWidget()
                    hbox = QtWidgets.QHBoxLayout()
                    hbox.setContentsMargins(0, 0, 0, 0)
                    hbox.addWidget(label, stretch=1)
                    hbox.addStretch(0)
                    container.setLayout(hbox)
                    # Add to table
                    self.setCellWidget(frame_number, 0, container)
                else:
                    # Add to table
                    self.setCellWidget(frame_number, 0, label)
                row += 1
            text.append(str(row))
            self.setItem(frame_number, 0, item)
            if slide_height:
                self.setRowHeight(frame_number, slide_height)
        self.setVerticalHeaderLabels(text)
        if self.service_item.is_text():
            self.resizeRowsToContents()
        self.setColumnWidth(0, self.viewport().width())
        self.change_slide(slide_number)

    def change_slide(self, slide):
        """
        Switches to the given row.
        """
        # Retrieve setting
        autoscrolling = Settings().value('advanced/autoscrolling')
        # Check if auto-scroll disabled (None) and validate value as dict containing 'dist' and 'pos'
        # 'dist' represents the slide to scroll to relative to the new slide (-1 = previous, 0 = current, 1 = next)
        # 'pos' represents the vert position of of the slide (0 = in view, 1 = top, 2 = middle, 3 = bottom)
        if not (isinstance(autoscrolling, dict) and 'dist' in autoscrolling and 'pos' in autoscrolling and
                isinstance(autoscrolling['dist'], int) and isinstance(autoscrolling['pos'], int)):
            return
        # prevent scrolling past list bounds
        scroll_to_slide = slide + autoscrolling['dist']
        if scroll_to_slide < 0:
            scroll_to_slide = 0
        if scroll_to_slide >= self.slide_count():
            scroll_to_slide = self.slide_count() - 1
        # Scroll to item if possible.
        self.scrollToItem(self.item(scroll_to_slide, 0), autoscrolling['pos'])
        self.selectRow(slide)

    def current_slide_number(self):
        """
        Returns the position of the currently active item. Will return -1 if the widget is empty.
        """
        return super(ListPreviewWidget, self).currentRow()

    def slide_count(self):
        """
        Returns the number of slides this widget holds.
        """
        return super(ListPreviewWidget, self).rowCount()
