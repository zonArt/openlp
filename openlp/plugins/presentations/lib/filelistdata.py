# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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
import os
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class FileListData(QAbstractListModel):
    """
    An abstract list of strings and the preview icon to go with them
    """
    global log
    log=logging.getLogger(u'FileListData')
    log.info(u'started')

    def __init__(self):
        QAbstractListModel.__init__(self)
        self.items=[] # will be a list of (full filename shortname) tuples

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, filename):
        self.beginInsertRows(QModelIndex(),row,row)
        log.info(u'insert row %d:%s'%(row,filename))
        # get short filename to display next to image
        (prefix, shortfilename) = os.path.split(unicode(filename))
        log.info(u'shortfilename=%s'%(shortfilename))
        # create a preview image
        self.items.insert(row, (filename, shortfilename))
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, filename):
        self.insertRow(len(self.items), filename)

    def data(self, index, role):
        row=index.row()
        if row > len(self.items): # if the last row is selected and deleted, we then get called with an empty row!
            return QVariant()
        if role==Qt.DisplayRole:
            retval= self.items[row][1]
#        elif role == Qt.DecorationRole:
#            retval= self.items[row][1]
        elif role == Qt.ToolTipRole:
            retval= self.items[row][0]
        else:
            retval= QVariant()
#         log.info(u'Returning"+ unicode(retval))
        if type(retval) is not type(QVariant):
            return QVariant(retval)
        else:
            return retval

    def getFileList(self):
        filelist = [item[0] for item in self.items];
        return filelist

    def getFilename(self, index):
        row = index.row()
        return self.items[row][0]
