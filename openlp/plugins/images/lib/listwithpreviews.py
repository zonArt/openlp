import os
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class ListWithPreviews(QAbstractListModel):
    """
    An abstract list of strings and the preview icon to go with them
    """
    global log
    log=logging.getLogger("ListWithPreviews")
    log.info("started")

    def __init__(self):
        QAbstractListModel.__init__(self)
        self.items=[] # will be a list of (full filename, QPixmap, shortname) tuples
        self.rowheight=50
        self.maximagewidth=self.rowheight*16/9.0;

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, filename):
        self.beginInsertRows(QModelIndex(),row,row)
        log.info("insert row %d:%s"%(row,filename))
        # get short filename to display next to image
        (prefix, shortfilename) = os.path.split(str(filename))
        log.info("shortfilename=%s"%(shortfilename))
        # create a preview image
        if os.path.exists(filename):
            preview = QPixmap(str(filename))
            w=self.maximagewidth;h=self.rowheight
            preview = preview.scaled(w,h, Qt.KeepAspectRatio)
            realw=preview.width(); realh=preview.height()
            # and move it to the centre of the preview space
            p=QPixmap(w,h)
            p.fill(Qt.transparent)
            painter=QPainter(p)
            painter.drawPixmap((w-realw)/2,(h-realh)/2,preview)
        else:
            w=self.maximagewidth;h=self.rowheight
            p=QPixmap(w,h)
            p.fill(Qt.transparent)
        # finally create the row
        self.items.insert(row, (filename, p, shortfilename))
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
            retval= self.items[row][2]
        elif role == Qt.DecorationRole:
            retval= self.items[row][1]
        elif role == Qt.ToolTipRole:
            retval= self.items[row][0]
        else:
            retval= QVariant()
#         log.info("Returning"+ str(retval))
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
