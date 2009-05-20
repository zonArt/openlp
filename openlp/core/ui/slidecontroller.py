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

from openlp.core.lib import OpenLPToolbar, translate

class SlideData(QtCore.QAbstractListModel):
    """
    Tree of items for an order of Theme.
    Includes methods for reading and writing the contents to an OOS file
    Root contains a list of ThemeItems
    """
    global log
    log=logging.getLogger(u'SlideData')

    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        self.items = []
        self.rowheight = 50
        self.maximagewidth = self.rowheight * 16/9.0;
        log.info(u'Starting')

    def clear(self):
        self.items = []

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent=None):
        return len(self.items)

    def insertRow(self, row, frame, framenumber):
        self.beginInsertRows(QtCore.QModelIndex(),row,row)
        log.info(u'insert row %d' % row)
        # create a preview image
        frame1 = frame.scaled(QtCore.QSize(300,225),  QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.items.insert(row,(frame1, framenumber))
        log.info(u'Items: %s' % self.items)
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row,row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, frame, framenumber):
        self.insertRow(len(self.items), frame, framenumber)

    def data(self, index, role):
        row=index.row()
        if row > len(self.items): # if the last row is selected and deleted, we then get called with an empty row!
            return QtCore.QVariant()
        if role == QtCore.Qt.DecorationRole:
            retval= self.items[row][0]
        else:
            retval= QtCore.QVariant()
        if type(retval) is not type(QtCore.QVariant):
            return QtCore.QVariant(retval)
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

    def __init__(self, control_splitter, isLive):
        QtGui.QWidget.__init__(self)
        self.isLive = isLive
        self.Panel = QtGui.QWidget(control_splitter)
        self.Splitter = QtGui.QSplitter(self.Panel)
        self.Splitter.setOrientation(QtCore.Qt.Vertical)

        self.PanelLayout = QtGui.QVBoxLayout(self.Panel)
        self.PanelLayout.addWidget(self.Splitter)
        self.PanelLayout.setSpacing(50)
        self.PanelLayout.setMargin(0)

        self.Controller = QtGui.QScrollArea(self.Splitter)
        self.Controller.setGeometry(QtCore.QRect(0, 0, 700, 536))
        self.Controller.setWidgetResizable(True)
        self.Controller.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtGui.QWidget(self.Controller)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 700, 536))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.PreviewListView = QtGui.QListView(self.scrollAreaWidgetContents)
        self.PreviewListData = SlideData()
        self.PreviewListView.isLive = self.isLive
        self.PreviewListView.setModel(self.PreviewListData)
        self.PreviewListView.setSelectionRectVisible(True)
        self.PreviewListView.setSpacing(5)
        self.PreviewListView.setObjectName("PreviewListView")

        self.gridLayout.addWidget(self.PreviewListView, 0, 0, 1, 1)
        self.Controller.setWidget(self.scrollAreaWidgetContents)

        self.Toolbar = OpenLPToolbar(self.Splitter)
        sizeToolbarPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizeToolbarPolicy.setHorizontalStretch(0)
        sizeToolbarPolicy.setVerticalStretch(0)
        sizeToolbarPolicy.setHeightForWidth(self.Toolbar.sizePolicy().hasHeightForWidth())

        if self.isLive:
            self.Toolbar.addToolbarButton(u'First Slide', u':/slides/slide_first.png',
            translate(u'SlideController', u'Move to first'), self.onSlideSelectedFirst)
        self.Toolbar.addToolbarButton(u'Last Slide', u':/slides/slide_previous.png',
            translate(u'SlideController', u'Move to previous'), self.onSlideSelectedPrevious)
        self.Toolbar.addToolbarButton(u'First Slide', u':/slides/slide_next.png',
            translate(u'SlideController', u'Move to next'), self.onSlideSelectedNext)
        if self.isLive:
            self.Toolbar.addToolbarButton(u'Last Slide', u':/slides/slide_last.png',
                translate(u'SlideController', u'Move to last'), self.onSlideSelectedLast)
            self.Toolbar.addSeparator()
            self.Toolbar.addToolbarButton(u'Close Screen', u':/slides/slide_close.png',
                translate(u'SlideController', u'Close Screen'), self.onBlankScreen)

        self.Toolbar.setSizePolicy(sizeToolbarPolicy)

        self.PreviewFrame = QtGui.QFrame(self.Splitter)
        self.PreviewFrame.setGeometry(QtCore.QRect(50, 270, 250, 190))
        self.PreviewFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.PreviewFrame.setFrameShadow(QtGui.QFrame.Sunken)
        self.PreviewFrame.setObjectName(u'PreviewFrame')

        self.grid = QtGui.QGridLayout(self.PreviewFrame)
        self.grid.setMargin(10)
        self.grid.setObjectName(u'grid')

        self.SlidePreview = QtGui.QLabel(self.PreviewFrame)
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
        self.SlidePreview.setObjectName(u'SlidePreview')
        self.grid.addWidget(self.SlidePreview, 0, 0, 1, 1)

        QtCore.QObject.connect(self.PreviewListView,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onSlideSelected)
        QtCore.QObject.connect(self.PreviewListView,
            QtCore.SIGNAL(u'activated(QModelIndex)'), self.onSlideSelected)

    def onSlideSelectedFirst(self):
        row = self.PreviewListData.createIndex(0, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row, QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onSlideSelectedNext(self):
        indexes = self.PreviewListView.selectedIndexes()
        rowNumber = 0
        for index in indexes:
            if index.row() == self.PreviewListData.rowCount() - 1:
                rowNumber = 0
            else:
                rowNumber = index.row() + 1
        row = self.PreviewListData.createIndex(rowNumber , 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row, QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onSlideSelectedPrevious(self):
        indexes = self.PreviewListView.selectedIndexes()
        rowNumber = 0
        for index in indexes:
            if index.row() == 0:
                rowNumber = self.PreviewListData.rowCount() - 1
            else:
                rowNumber  = index.row() - 1
        row = self.PreviewListData.createIndex(rowNumber , 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row, QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onSlideSelectedLast(self):
        row = self.PreviewListData.createIndex(self.PreviewListData.rowCount() - 1 , 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row, QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onBlankScreen(self):
        self.mainDisplay.blankDisplay()

    def onSlideSelected(self, index):
        frame = self.PreviewListData.getValue(index)
        self.previewFrame(frame)

    def previewFrame(self, frame):
        self.SlidePreview.setPixmap(frame[0])
        if self.isLive:
            no = frame[1]
            LiveFrame = self.serviceitem.frames[no][u'image']
            self.mainDisplay.frameView(LiveFrame)

    def addServiceItem(self, serviceitem):
        log.debug(u'addServiceItem')
        self.serviceitem = serviceitem
        self.serviceitem.render()
        self.PreviewListData.clear()
        framenumber = 0
        for frame in self.serviceitem.frames:
            self.PreviewListData.addRow(frame[u'image'], framenumber)
            framenumber += 1

        row = self.PreviewListData.createIndex(0, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row, QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def addServiceManagerItem(self, serviceitem, slideno):
        self.addServiceItem(serviceitem)
        row = self.PreviewListData.createIndex(slideno, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row, QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)
