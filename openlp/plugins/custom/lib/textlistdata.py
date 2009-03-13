import logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class TextListData(QAbstractListModel):
    """
    An abstract list of strings 
    """
    global log
    log=logging.getLogger("TextListData")
    log.info("started")

    def __init__(self):
        QAbstractListModel.__init__(self)
        self.items=[] # will be a list of (database id , title) tuples

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, id, title):
        self.beginInsertRows(QModelIndex(),row,row)
        log.debug("insert row %d:%s for id %d"%(row,title, id))
        self.items.insert(row, (id, title))
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, id, title):
        self.insertRow(len(self.items), id, title)

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

    def getIdList(self):
        filelist = [item[0] for item in self.items];
        return filelist

    def getId(self, index):
        row = index.row()
        return self.item[row][0]
        
if __name__=="__main__":
    sxml=TextListData()        
