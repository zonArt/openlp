# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from PyQt4 import QtCore, QtGui

from serviceitemeditdialog import Ui_ServiceItemEditDialog

class ServiceItemEditForm(QtGui.QDialog, Ui_ServiceItemEditDialog):
    """
    This is the form that is used to edit the verses of the song.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.itemList = []
        QtCore.QObject.connect(self.listWidget,
            QtCore.SIGNAL(u'currentRowChanged(int)'), self.onCurrentRowChanged)

    def setServiceItem(self, item):
        self.item = item
        self.itemList = []
        if self.item.is_image():
            self.data = True
            for frame in self.item._raw_frames:
                self.itemList.append(frame)
        self.loadData()
        self.listWidget.setCurrentItem(self.listWidget.currentItem())

    def getServiceItem(self):
        if self.data:
            self.item._raw_frames = []
            if self.item.is_image():
                for item in self.itemList:
                    self.item.add_from_image(item[u'path'], item[u'title'])
            self.item.render()
        return self.item

    def loadData(self):
        """
        Loads the image list.
        """
        self.listWidget.clear()
        for frame in self.itemList:
            item_name = QtGui.QListWidgetItem(frame[u'title'])
            self.listWidget.addItem(item_name)

    def onDeleteButtonClicked(self):
        """
        Delete the current row.
        """
        item = self.listWidget.currentItem()
        if not item:
            return
        row = self.listWidget.row(item)
        self.itemList.pop(row)
        self.loadData()
        if row == self.listWidget.count():
            self.listWidget.setCurrentRow(row - 1)
        else:
            self.listWidget.setCurrentRow(row)

    def onUpButtonClicked(self):
        """
        Move the current row up in the list.
        """
        self.__moveItem(u'up')

    def onDownButtonClicked(self):
        """
        Move the current row down in the list
        """
        self.__moveItem(u'down')

    def __moveItem(self, direction=u''):
        """
        Move the current item.
        """
        if not direction:
            return
        item = self.listWidget.currentItem()
        if not item:
            return
        row = self.listWidget.row(item)
        temp = self.itemList[row]
        self.itemList.pop(row)
        if direction == u'up':
            row -= 1
        else:
            row += 1
        self.itemList.insert(row, temp)
        self.loadData()
        self.listWidget.setCurrentRow(row)

    def onCurrentRowChanged(self, row):
        """
        Called when the currentRow has changed.

        ``row``
            The row number (int).
        """
        # Disable all buttons, as no row is selected or only one image is left.
        if row == -1 or self.listWidget.count() == 1:
            self.downButton.setEnabled(False)
            self.upButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
        else:
            # Check if we are at the end of the list.
            if self.listWidget.count() == row + 1:
                self.downButton.setEnabled(False)
            else:
                self.downButton.setEnabled(True)
            # Check if we are at the beginning of the list.
            if row == 0:
                self.upButton.setEnabled(False)
            else:
                self.upButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
