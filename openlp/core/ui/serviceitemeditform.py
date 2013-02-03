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
The service item edit dialog
"""
from PyQt4 import QtCore, QtGui
from openlp.core.lib import Registry

from serviceitemeditdialog import Ui_ServiceItemEditDialog


class ServiceItemEditForm(QtGui.QDialog, Ui_ServiceItemEditDialog):
    """
    This is the form that is used to edit the verses of the song.
    """
    def __init__(self):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, self.main_window)
        self.setupUi(self)
        self.item_list = []
        QtCore.QObject.connect(self.list_widget, QtCore.SIGNAL(u'currentRowChanged(int)'),
            self.on_current_row_changed)

    def set_service_item(self, item):
        """
        Set the service item to be edited.
        """
        self.item = item
        self.item_list = []
        if self.item.is_image():
            self.data = True
            for frame in self.item._raw_frames:
                self.item_list.append(frame)
        self.load_data()
        self.list_widget.setCurrentItem(self.list_widget.currentItem())

    def get_service_item(self):
        """
        Get the modified service item.
        """
        if self.data:
            self.item._raw_frames = []
            if self.item.is_image():
                for item in self.item_list:
                    self.item.add_from_image(item[u'path'], item[u'title'])
            self.item.render()
        return self.item

    def load_data(self):
        """
        Loads the image list.
        """
        self.list_widget.clear()
        for frame in self.item_list:
            item_name = QtGui.QListWidgetItem(frame[u'title'])
            self.list_widget.addItem(item_name)

    def on_delete_button_clicked(self):
        """
        Delete the current row.
        """
        item = self.list_widget.currentItem()
        if not item:
            return
        row = self.list_widget.row(item)
        self.item_list.pop(row)
        self.load_data()
        if row == self.list_widget.count():
            self.list_widget.setCurrentRow(row - 1)
        else:
            self.list_widget.setCurrentRow(row)

    def on_up_button_clicked(self):
        """
        Move the current row up in the list.
        """
        self.__move_item(u'up')

    def on_down_button_clicked(self):
        """
        Move the current row down in the list
        """
        self.__move_item(u'down')

    def __move_item(self, direction=u''):
        """
        Move the current item.
        """
        if not direction:
            return
        item = self.list_widget.currentItem()
        if not item:
            return
        row = self.list_widget.row(item)
        temp = self.item_list[row]
        self.item_list.pop(row)
        if direction == u'up':
            row -= 1
        else:
            row += 1
        self.item_list.insert(row, temp)
        self.load_data()
        self.list_widget.setCurrentRow(row)

    def on_current_row_changed(self, row):
        """
        Called when the currentRow has changed.

        ``row``
            The row number (int).
        """
        # Disable all buttons, as no row is selected or only one image is left.
        if row == -1 or self.list_widget.count() == 1:
            self.down_button.setEnabled(False)
            self.up_button.setEnabled(False)
            self.delete_button.setEnabled(False)
        else:
            # Check if we are at the end of the list.
            if self.list_widget.count() == row + 1:
                self.down_button.setEnabled(False)
            else:
                self.down_button.setEnabled(True)
            # Check if we are at the beginning of the list.
            if row == 0:
                self.up_button.setEnabled(False)
            else:
                self.up_button.setEnabled(True)
            self.delete_button.setEnabled(True)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, u'_main_window'):
            self._main_window = Registry().get(u'main_window')
        return self._main_window

    main_window = property(_get_main_window)