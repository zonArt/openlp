# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

import os
import logging
from PyQt4 import QtCore, QtGui

class ListWithPreviews(QtCore.QAbstractListModel):
    """
    An abstract list of unicodeings and the preview icon to go with them
    """
    global log
    log = logging.getLogger(u'ListWithPreviews')
    log.info(u'started')

    def __init__(self, new_preview_function=None):
        QtCore.QAbstractListModel.__init__(self)
        # will be a list of (full filename, QPixmap, shortname) tuples
        self.items = []
        self.rowheight = 50
        self.maximagewidth = self.rowheight * 16 / 9.0;
        self.preview_function = new_preview_function

    def make_preview(self, filename):
        if os.path.exists(filename):
            if self.preview_function is not None:
                preview=self.preview_function(filename)
            else:
                preview = QtGui.QImage(filename)
        else:
            preview = None

        if preview is not None:
            w = self.maximagewidth;
            h = self.rowheight
            preview = preview.scaled(w, h, QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation)
            realw = preview.width();
            realh = preview.height()
            # and move it to the centre of the preview space
            p = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32_Premultiplied)
            p.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(p)
            painter.drawImage((w-realw) / 2, (h-realh) / 2, preview)
        else:
            w = self.maximagewidth;
            h = self.rowheight
            p = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32_Premultiplied)
            p.fill(QtCore.Qt.transparent)
        return p

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, filename):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        #log.info(u'insert row %d:%s' % (row,filename))
        # get short filename to display next to image
        filename = unicode(filename)
        (prefix, shortfilename) = os.path.split(filename)
        #log.info(u'shortfilename=%s' % (shortfilename))
        # create a preview image
        p=self.make_preview(filename)
        # finally create the row
        self.items.insert(row, (filename, p, shortfilename))
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, filename):
        self.insertRow(len(self.items), filename)

    def data(self, index, role):
        row = index.row()
        if row > len(self.items):
            # If the last row is selected and deleted, we then get called
            # with an empty row!
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            retval = self.items[row][2]
        elif role == QtCore.Qt.DecorationRole:
            retval = self.items[row][1]
        elif role == QtCore.Qt.ToolTipRole:
            retval = self.items[row][0]
        else:
            retval = QtCore.QVariant()
        if type(retval) is not type(QtCore.QVariant):
            return QtCore.QVariant(retval)
        else:
            return retval

    def getFileList(self):
        filelist = [item[0] for item in self.items];
        return filelist

    def getFilename(self, index):
        row = index.row()
        return self.items[row][0]
