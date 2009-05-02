# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

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
import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SlideData(QAbstractListModel):
    """
    Tree of items for an order of Theme.
    Includes methods for reading and writing the contents to an OOS file
    Root contains a list of ThemeItems
    """
    global log
    log=logging.getLogger(u'SlideData')

    def __init__(self):
        QAbstractListModel.__init__(self)
        self.items=[]
        self.rowheight=50
        self.maximagewidth=self.rowheight*16/9.0;
        log.info(u'Starting')

    def clearItems(self):
        self.items=[]

    def rowCount(self, parent):
        return len(self.items)

    def insertRow(self, row, frame, text):
        self.beginInsertRows(QModelIndex(),row,row)
        log.info(u'insert row %d' % row)
        # create a preview image
        self.items.insert(row,(frame, text))
        log.info(u'Items: %s' % self.items)
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, frame, text):
        self.insertRow(len(self.items), frame, text)

    def data(self, index, role):
        row=index.row()
        if row > len(self.items): # if the last row is selected and deleted, we then get called with an empty row!
            return QVariant()
        if role==Qt.DisplayRole:
            retval= self.items[row][1]
        elif role == Qt.DecorationRole:
            retval= self.items[row][0]
        else:
            retval= QVariant()
#         log.info("Returning"+ str(retval))
        if type(retval) is not type(QVariant):
            return QVariant(retval)
        else:
            return retval

    def __iter__(self):
        for i in self.items:
            yield i

    def getValue(self, index):
        row = index.row()
        return self.items[row]

    def getItem(self, row):
        log.info(u'Get Item:%d -> %s' %(row, str(self.items)))
        return self.items[row]

    def getList(self):
        filelist = [item[3] for item in self.items];
        return filelist


class SlideController(QtGui.QWidget):
    global log
    log=logging.getLogger(u'SlideController')

    def __init__(self, control_splitter):
        QtGui.QWidget.__init__(self)
        self.Pane = QtGui.QWidget(control_splitter)
        self.Splitter = QtGui.QSplitter(self.Pane)
        self.Splitter.setOrientation(QtCore.Qt.Vertical)

        self.PaneLayout = QtGui.QVBoxLayout(self.Pane)
        self.PaneLayout.addWidget(self.Splitter)
        self.PaneLayout.setSpacing(50)
        self.PaneLayout.setMargin(0)

        #self.VerseListView = QtGui.QListWidget(customEditDialog)
        #self.VerseListView.setObjectName("VerseListView")
        #self.horizontalLayout_4.addWidget(self.VerseListView)

        self.Controller = QtGui.QScrollArea(self.Splitter)
        self.Controller.setWidgetResizable(True)

         #self.ControllerContents = QtGui.QWidget(self.Controller)
        #self.ControllerContents.setGeometry(QtCore.QRect(0, 0, 228, 536))

        self.CustomListView = QtGui.QListView(self.Splitter)
        self.CustomListView.setAlternatingRowColors(True)
        self.CustomListData = SlideData()
        self.CustomListView.setModel(self.CustomListData)
        self.Controller.setGeometry(QtCore.QRect(0, 0, 828, 536))
        #self.Controller.setWidget(self.ControllerContents)


        self.Controller.setWidget(self.CustomListView)

        self.SlidePreview = QtGui.QLabel(self.Splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SlidePreview.sizePolicy().hasHeightForWidth())
        self.SlidePreview.setSizePolicy(sizePolicy)
        self.SlidePreview.setMinimumSize(QtCore.QSize(250, 190))
        self.SlidePreview.setFrameShape(QtGui.QFrame.WinPanel)
        self.SlidePreview.setFrameShadow(QtGui.QFrame.Sunken)
        self.SlidePreview.setLineWidth(1)
        self.SlidePreview.setScaledContents(True)
        self.SlidePreview.setObjectName("SlidePreview")

    def previewFrame(self, frame):
        #self.SlidePreview.setPixmap(frame)

       # imageLabel = QtGui.QLabel()
        #imageLabel.setPixmap(frame)
       # self.Controller.setWidget(imageLabel)
       pass

    def addServiceItem(self, serviceitem):
        self.serviceitem = serviceitem
        self.serviceitem.render()
        print self.serviceitem.frames
        for frame in self.serviceitem.frames:
            self.CustomListData.addRow(frame, u'some text')

    def render(self):
        pass
