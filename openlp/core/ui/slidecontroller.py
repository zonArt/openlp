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
    List of frames to be displayed on the list and the main display.
    """
    global log
    log = logging.getLogger(u'SlideData')

    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        self.items = []
        self.rowheight = 50
        self.maximagewidth = self.rowheight * 16 / 9.0;
        log.info(u'Starting')

    def clear(self):
        self.items = []

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent=None):
        return len(self.items)

    def insertRow(self, row, frame, framenumber):
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        log.info(u'insert row %d' % row)
        # create a preview image
        frame1 = frame.scaled(QtCore.QSize(280, 210), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        self.items.insert(row, (frame1, framenumber))
        log.info(u'Item loaded')
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row)
        self.items.pop(row)
        self.endRemoveRows()

    def addRow(self, frame, framenumber):
        self.insertRow(len(self.items), frame, framenumber)

    def data(self, index, role):
        row = index.row()
        if row > len(self.items):
            # if the last row is selected and deleted, we then get called with
            # an empty row!
            return QtCore.QVariant()
        if role == QtCore.Qt.DecorationRole:
            retval = self.items[row][0]
        else:
            retval = QtCore.QVariant()
        if type(retval) is not type(QtCore.QVariant):
            return QtCore.QVariant(retval)
        else:
            return retval

    def __iter__(self):
        for item in self.items:
            yield item

    def getValue(self, index):
        row = index.row()
        return self.items[row]

    def getItem(self, row):
        log.info(u'Get Item:%d -> %s' %(row, unicode(self.items)))
        return self.items[row]

    def getList(self):
        filelist = [item[3] for item in self.items];
        return filelist

class SlideList(QtGui.QListView):

    def __init__(self,parent=None,name=None):
        QtGui.QListView.__init__(self,parent.Controller)
        self.parent = parent

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            #here accept the event and do something
            if event.key() == QtCore.Qt.Key_Up:
                self.parent.onSlideSelectedPrevious()
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                self.parent.onSlideSelectedNext()
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageUp:
                self.parent.onSlideSelectedFirst()
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageDown:
                self.parent.onSlideSelectedLast()
                event.accept()
            event.ignore()
        else:
            event.ignore()

class SlideController(QtGui.QWidget):
    """
    SlideController is the slide controller widget. This widget is what the user
    uses to control the displaying of verses/slides/etc on the screen.
    """
    global log
    log = logging.getLogger(u'SlideController')

    def __init__(self,  parent, isLive=False):
        """
        Set up the Slide Controller.
        """
        QtGui.QWidget.__init__(self, parent.mainWindow)
        self.isLive = isLive
        self.parent = parent
        self.Panel = QtGui.QWidget(parent.ControlSplitter)
        self.Splitter = QtGui.QSplitter(self.Panel)
        self.Splitter.setOrientation(QtCore.Qt.Vertical)
        # Layout for holding panel
        self.PanelLayout = QtGui.QVBoxLayout(self.Panel)
        self.PanelLayout.addWidget(self.Splitter)
        self.PanelLayout.setSpacing(0)
        self.PanelLayout.setMargin(0)
        # Actual controller section
        self.Controller = QtGui.QWidget(self.Splitter)
        self.Controller.setGeometry(QtCore.QRect(0, 0, 800, 536))
        self.Controller.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
            QtGui.QSizePolicy.Maximum))
        self.ControllerLayout = QtGui.QVBoxLayout(self.Controller)
        self.ControllerLayout.setSpacing(0)
        self.ControllerLayout.setMargin(0)
        # Controller list view
        self.PreviewListView = SlideList(self)
        self.PreviewListView.setUniformItemSizes(True)
        self.PreviewListView.setIconSize(QtCore.QSize(250, 190))
        self.PreviewListData = SlideData()
        self.PreviewListView.isLive = self.isLive
        if QtCore.QT_VERSION_STR > u'4.4.0':
            self.PreviewListView.setFlow(1)
            self.PreviewListView.setViewMode(1)
        self.PreviewListView.setWrapping(False)
        self.PreviewListView.setModel(self.PreviewListData)
        self.PreviewListView.setSpacing(0)
        self.PreviewListView.setObjectName(u'PreviewListView')
        self.ControllerLayout.addWidget(self.PreviewListView)
        self.defineToolbar()
        # Screen preview area
        self.PreviewFrame = QtGui.QFrame(self.Splitter)
        self.PreviewFrame.setGeometry(QtCore.QRect(0, 0, 250, 190))
        self.PreviewFrame.setSizePolicy(QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum))
        self.PreviewFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.PreviewFrame.setFrameShadow(QtGui.QFrame.Sunken)
        self.PreviewFrame.setObjectName(u'PreviewFrame')
        self.grid = QtGui.QGridLayout(self.PreviewFrame)
        self.grid.setMargin(8)
        self.grid.setObjectName(u'grid')
        # Actual preview screen
        self.SlidePreview = QtGui.QLabel(self.PreviewFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SlidePreview.sizePolicy().hasHeightForWidth())
        self.SlidePreview.setSizePolicy(sizePolicy)
        self.SlidePreview.setMinimumSize(QtCore.QSize(280, 210))
        self.SlidePreview.setFrameShape(QtGui.QFrame.Box)
        self.SlidePreview.setFrameShadow(QtGui.QFrame.Plain)
        self.SlidePreview.setLineWidth(1)
        self.SlidePreview.setScaledContents(True)
        self.SlidePreview.setObjectName(u'SlidePreview')
        self.grid.addWidget(self.SlidePreview, 0, 0, 1, 1)
        # Some events
        QtCore.QObject.connect(self.PreviewListView,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onSlideSelected)
        QtCore.QObject.connect(self.PreviewListView,
            QtCore.SIGNAL(u'activated(QModelIndex)'), self.onSlideSelected)

    def defineToolbar(self):
        # Controller toolbar
        self.Toolbar = OpenLPToolbar(self.Controller)
        sizeToolbarPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizeToolbarPolicy.setHorizontalStretch(0)
        sizeToolbarPolicy.setVerticalStretch(0)
        sizeToolbarPolicy.setHeightForWidth(
            self.Toolbar.sizePolicy().hasHeightForWidth())
        if self.isLive:
            self.Toolbar.addToolbarButton(u'First Slide',
                u':/slides/slide_first.png',
                translate(u'SlideController', u'Move to first'),
                self.onSlideSelectedFirst)
        self.Toolbar.addToolbarButton(u'Last Slide',
            u':/slides/slide_previous.png',
            translate(u'SlideController', u'Move to previous'),
            self.onSlideSelectedPrevious)
        self.Toolbar.addToolbarButton(u'First Slide',
            u':/slides/slide_next.png',
            translate(u'SlideController', u'Move to next'),
            self.onSlideSelectedNext)
        if self.isLive:
            self.Toolbar.addToolbarButton(u'Last Slide',
                u':/slides/slide_last.png',
                translate(u'SlideController', u'Move to last'),
                self.onSlideSelectedLast)
            self.Toolbar.addSeparator()
            self.Toolbar.addToolbarButton(u'Close Screen',
                u':/slides/slide_close.png',
                translate(u'SlideController', u'Close Screen'),
                self.onBlankScreen)
        self.Toolbar.setSizePolicy(sizeToolbarPolicy)
        self.ControllerLayout.addWidget(self.Toolbar)

    def onSlideSelectedFirst(self):
        """
        Go to the first slide.
        """
        row = self.PreviewListData.createIndex(0, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onSlideSelectedNext(self):
        """
        Go to the next slide.
        """
        indexes = self.PreviewListView.selectedIndexes()
        rowNumber = 0
        for index in indexes:
            if index.row() == self.PreviewListData.rowCount() - 1:
                rowNumber = 0
            else:
                rowNumber = index.row() + 1
        row = self.PreviewListData.createIndex(rowNumber, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onSlideSelectedPrevious(self):
        """
        Go to the previous slide.
        """
        indexes = self.PreviewListView.selectedIndexes()
        rowNumber = 0
        for index in indexes:
            if index.row() == 0:
                rowNumber = self.PreviewListData.rowCount() - 1
            else:
                rowNumber  = index.row() - 1
        row = self.PreviewListData.createIndex(rowNumber, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onSlideSelectedLast(self):
        """
        Go to the last slide.
        """
        row = self.PreviewListData.createIndex(
            self.PreviewListData.rowCount() - 1, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def onBlankScreen(self):
        """
        Blank the screen.
        """
        self.mainDisplay.blankDisplay()

    def onSlideSelected(self, index):
        """
        Generate the preview when you click on a slide.
        """
        frame = self.PreviewListData.getValue(index)
        self.previewFrame(frame)

    def previewFrame(self, frame):
        """
        Generates a preview of the current slide.
        """
        self.SlidePreview.setPixmap(QtGui.QPixmap.fromImage(frame[0]))
        if self.isLive:
            no = frame[1]
            LiveFrame = self.serviceitem.frames[no][u'image']
            self.parent.mainDisplay.frameView(LiveFrame)

    def addServiceItem(self, serviceitem):
        """
        Loads a ServiceItem.
        """
        log.debug(u'add Service Item')
        self.serviceitem = serviceitem
        self.serviceitem.render()
        self.PreviewListData.clear()
        framenumber = 0
        for frame in self.serviceitem.frames:
            self.PreviewListData.addRow(frame[u'image'], framenumber)
            framenumber += 1
        row = self.PreviewListData.createIndex(0, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)

    def addServiceManagerItem(self, serviceitem, slideno):
        """
        Loads a ServiceManagerItem.
        """
        log.debug(u'add Service Manager Item')
        self.PreviewListData.clear()
        self.serviceitem = serviceitem
        framenumber = 0
        for frame in self.serviceitem.frames:
            self.PreviewListData.addRow(frame[u'image'], framenumber)
            framenumber += 1
        row = self.PreviewListData.createIndex(slideno, 0)
        if row.isValid():
            self.PreviewListView.selectionModel().setCurrentIndex(row,
                QtGui.QItemSelectionModel.SelectCurrent)
            self.onSlideSelected(row)
