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

class ListPreviewWidget(object):
    def __init__(self, parent, is_live):
        # Controller list view
        self.is_live = is_live
        self.preview_table_widget = QtGui.QTableWidget(parent)
        self.preview_table_widget.setColumnCount(1)
        self.preview_table_widget.horizontalHeader().setVisible(False)
        self.preview_table_widget.setColumnWidth(0, parent.width())
        self.preview_table_widget.setObjectName(u'preview_table_widget')
        self.preview_table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.preview_table_widget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.preview_table_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.preview_table_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.preview_table_widget.setAlternatingRowColors(True)
        self.service_item = ServiceItem()
        self.clicked = QtCore.pyqtSignal()
        self.double_clicked = QtCore.pyqtSignal()
        if not self.is_live:
            self.preview_table_widget.doubleClicked.connect(self.double_clicked)
        self.preview_table_widget.clicked.connect(self.clicked)

    def clicked(self):
        self.clicked.emit()

    def double_clicked(self):
        self.double_clicked.emit()

    def get_preview_widget(self):
        return self.preview_table_widget

    def set_active(self, active):
        if active:
            self.preview_table_widget.show()
        else:
            self.preview_table_widget.hide()

    def preview_size_changed(self, width, ratio):
        """
        Takes care of the SlidePreview's size. Is called when one of the the
        splitters is moved or when the screen size is changed. Note, that this
        method is (also) called frequently from the mainwindow *paintEvent*.
        """
        self.preview_table_widget.setColumnWidth(0, self.preview_table_widget.viewport().size().width())
        if self.service_item:
            # Sort out songs, bibles, etc.
            if self.service_item.is_text():
                self.preview_table_widget.resizeRowsToContents()
            else:
                # Sort out image heights.
                for framenumber in range(len(self.service_item.get_frames())):
                    self.preview_table_widget.setRowHeight(framenumber, width / ratio)

    def replace_service_manager_item(self, service_item, width, ratio):
        """
        Loads a ServiceItem into the system from ServiceManager
        Display the slide number passed
        """
        self.service_item = service_item
        self.preview_table_widget.clear()
        self.preview_table_widget.setRowCount(0)
        self.preview_table_widget.setColumnWidth(0, width)
        row = 0
        text = []
        for framenumber, frame in enumerate(self.service_item.get_frames()):
            self.preview_table_widget.setRowCount(self.preview_table_widget.rowCount() + 1)
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
                self.preview_table_widget.setCellWidget(framenumber, 0, label)
                slideHeight = width / ratio
                row += 1
            text.append(unicode(row))
            self.preview_table_widget.setItem(framenumber, 0, item)
            if slideHeight:
                self.preview_table_widget.setRowHeight(framenumber, slideHeight)
        self.preview_table_widget.setVerticalHeaderLabels(text)
        if self.service_item.is_text():
            self.preview_table_widget.resizeRowsToContents()
        self.preview_table_widget.setColumnWidth(0, self.preview_table_widget.viewport().size().width())
        #stuff happens here, perhaps the setFocus() has to happen later...
        self.preview_table_widget.setFocus()

    def update_preview_selection(self, slideno):
        """
        Utility method to update the selected slide in the list.
        """
        if slideno > self.preview_table_widget.rowCount():
            self.preview_table_widget.selectRow(
                self.preview_table_widget.rowCount() - 1)
        else:
            self.check_update_selected_slide(slideno)

    def check_update_selected_slide(self, row):
        """
        Check if this slide has been updated
        """
        if row + 1 < self.preview_table_widget.rowCount():
            self.preview_table_widget.scrollToItem(self.preview_table_widget.item(row + 1, 0))
        self.preview_table_widget.selectRow(row)

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