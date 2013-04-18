# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
The :mod:`slidecontroller` module contains the most important part of OpenLP - the slide controller
"""

from PyQt4 import QtCore, QtGui

from openlp.core.lib import ImageSource, Registry, ServiceItem


class ListPreviewWidget(QtGui.QTableWidget):
    def __init__(self, parent, screen_ratio):
        super(QtGui.QTableWidget, self).__init__(parent)
        self.service_item = ServiceItem()
        self.screen_ratio = screen_ratio

        self.setColumnCount(1)
        self.horizontalHeader().setVisible(False)
        self.setColumnWidth(0, parent.width())
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setAlternatingRowColors(True)

    def resizeEvent(self, QResizeEvent):
        self.__recalculate_layout()

    def __recalculate_layout(self):
        self.setColumnWidth(0, self.viewport().width())
        if self.service_item:
            # Sort out songs, bibles, etc.
            if self.service_item.is_text():
                self.resizeRowsToContents()
            else:
                # Sort out image heights.
                for framenumber in range(len(self.service_item.get_frames())):
                    #self.setRowHeight(framenumber, width / ratio)
                    height = self.viewport().width() / self.screen_ratio
                    self.setRowHeight(framenumber, height)

    #width = self.main_window.controlSplitter.sizes()[self.split]
    def screen_size_changed(self, screen_ratio):
        self.screen_ratio = screen_ratio
        self.__recalculate_layout()

    def set_active(self, active):
        if active:
            self.show()
        else:
            self.hide()

    def replace_service_manager_item(self, service_item, width, slideno):
        """
        Loads a ServiceItem into the system from ServiceManager
        Display the slide number passed
        """
        self.service_item = service_item
        self.clear()
        self.setRowCount(0)
        self.setColumnWidth(0, width)
        row = 0
        text = []
        for framenumber, frame in enumerate(self.service_item.get_frames()):
            self.setRowCount(self.rowCount() + 1)
            item = QtGui.QTableWidgetItem()
            slideHeight = 0
            if self.service_item.is_text():
                if frame[u'verseTag']:
                    # These tags are already translated.
                    verse_def = frame[u'verseTag']
                    verse_def = u'%s%s' % (verse_def[0], verse_def[1:])
                    two_line_def = u'%s\n%s' % (verse_def[0], verse_def[1:])
                    row = two_line_def
                else:
                    row += 1
                item.setText(frame[u'text'])
            else:
                label = QtGui.QLabel()
                label.setMargin(4)
                if self.service_item.is_media():
                    label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                else:
                    label.setScaledContents(True)
                if self.service_item.is_command():
                    label.setPixmap(QtGui.QPixmap(frame[u'image']))
                else:
                    # If current slide set background to image
                    if framenumber == slideno:
                        self.service_item.bg_image_bytes = self.image_manager.get_image_bytes(frame[u'path'],
                                                                                              ImageSource.ImagePlugin)
                    image = self.image_manager.get_image(frame[u'path'], ImageSource.ImagePlugin)
                    label.setPixmap(QtGui.QPixmap.fromImage(image))
                self.setCellWidget(framenumber, 0, label)
                slideHeight = width / self.screen_ratio
                row += 1
            text.append(unicode(row))
            self.setItem(framenumber, 0, item)
            if slideHeight:
                self.setRowHeight(framenumber, slideHeight)
        self.setVerticalHeaderLabels(text)
        if self.service_item.is_text():
            self.resizeRowsToContents()
        self.setColumnWidth(0, self.viewport().width())
        #stuff happens here, perhaps the setFocus() has to happen later...
        self.setFocus()

    def update_preview_selection(self, row):
        """
        Utility method to update the selected slide in the list.
        """
        if row >= self.rowCount():
            self.selectRow(self.rowCount() - 1)
        else:
            self.check_update_selected_slide(row)

    def check_update_selected_slide(self, row):
        """
        Check if this slide has been updated
        """
        if row + 1 < self.rowCount():
            self.scrollToItem(self.item(row + 1, 0))
        self.selectRow(row)

    def currentRow(self):
        return super(ListPreviewWidget, self).currentRow()

    def rowCount(self):
        return super(ListPreviewWidget, self).rowCount()

    def _get_image_manager(self):
        """
        Adds the image manager to the class dynamically
        """
        if not hasattr(self, u'_image_manager'):
            self._image_manager = Registry().get(u'image_manager')
        return self._image_manager

    image_manager = property(_get_image_manager)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)

