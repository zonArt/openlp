# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
        # enable drop
        QtCore.QObject.connect(self.upButton, QtCore.SIGNAL(u'clicked()'),
            self.onItemUp)
        QtCore.QObject.connect(self.downButton, QtCore.SIGNAL(u'clicked()'),
            self.onItemDown)
        QtCore.QObject.connect(self.deleteButton, QtCore.SIGNAL(u'clicked()'),
            self.onItemDelete)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'accepted()'),
            self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            self.reject)

    def setServiceItem(self, item):
        self.item = item
        self.itemList = []
        if self.item.is_image():
            self.data = True
            for frame in self.item._raw_frames:
                self.itemList.append(frame)
        self.loadData()

    def getServiceItem(self):
        if self.data:
            self.item._raw_frames = []
            if self.item.is_image():
                for item in self.itemList:
                    self.item.add_from_image(item[u'path'], item[u'title'],
                        item[u'image'])
            self.item.render()
        return self.item

    def loadData(self):
        self.listWidget.clear()
        for frame in self.itemList:
            item_name = QtGui.QListWidgetItem(frame[u'title'])
            self.listWidget.addItem(item_name)

    def onItemDelete(self):
        """
        Delete the selected row
        """
        items = self.listWidget.selectedItems()
        for item in items:
            row =  self.listWidget.row(item)
            self.itemList.remove(self.itemList[row])
            self.loadData()

    def onItemUp(self):
        """
        Move the selected row up in the list
        """
        items = self.listWidget.selectedItems()
        for item in items:
            row =  self.listWidget.row(item)
            if row > 0:
                temp = self.itemList[row]
                self.itemList.remove(self.itemList[row])
                self.itemList.insert(row - 1, temp)
                self.loadData()

    def onItemDown(self):
        """
        Move the selected row down in the list
        """
        items = self.listWidget.selectedItems()
        for item in items:
            row =  self.listWidget.row(item)
            if row < len(self.itemList) and row is not -1:
                temp = self.itemList[row]
                self.itemList.remove(self.itemList[row])
                self.itemList.insert(row + 1, temp)
                self.loadData()
