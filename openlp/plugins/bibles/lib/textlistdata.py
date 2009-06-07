# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import logging

from PyQt4 import QtCore, QtGui


class TextListData(QtCore.QAbstractListModel):
    """
    An abstract list of strings
    """
    global log
    log = logging.getLogger(u'TextListData')
    log.info(u'started')

    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        # will be a list of (database id , title) tuples
        self.items = []

    def resetStore(self):
        #reset list so can be reloaded
        self.items = []

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, id, title):
        self.beginInsertRows(QtCore.QModelIndex(),row,row)
        log.debug(u'insert row %d:%s for id %d' % (row,title, id))
        self.items.insert(row, (id, title))
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, id, title):
        self.insertRow(len(self.items), id, title)

    def data(self, index, role):
        row = index.row()
        # if the last row is selected and deleted, we then get called with an empty row!
        if row > len(self.items):
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            retval = self.items[row][1]
        else:
            retval = QtCore.QVariant()
        if type(retval) is not type(QtCore.QVariant):
            return QtCore.QVariant(retval)
        else:
            return retval

    def getIdList(self):
        filelist = [item[0] for item in self.items];
        return filelist

    def getValue(self, index):
        row = index.row()
        return self.items[row][1]

    def deleteRow(self, index):
        row = index.row()
        self.removeRow(row)
