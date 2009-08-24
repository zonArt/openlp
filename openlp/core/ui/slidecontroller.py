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
from openlp.core.lib import OpenLPToolbar, translate, buildIcon, Receiver

class SlideList(QtGui.QTableWidget):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    def __init__(self, parent=None, name=None):
        QtGui.QTableWidget.__init__(self, parent.Controller)
        self.parent = parent

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            #here accept the event and do something
            if event.key() == QtCore.Qt.Key_Up:
                self.parent.BaseToolbar.onSlideSelectedPrevious()
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                self.parent.BaseToolbar.onSlideSelectedNext()
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageUp:
                self.parent.BaseToolbar.onSlideSelectedFirst()
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageDown:
                self.parent.BaseToolbar.onSlideSelectedLast()
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

    def __init__(self, parent, isLive=False):
        """
        Set up the Slide Controller.
        """
        self.toolbarList = {}
        QtGui.QWidget.__init__(self, parent)
        self.isLive = isLive
        self.prefix  = u'preview_'
        if isLive:
            self.prefix  = u'live_'
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
        self.Controller.setGeometry(QtCore.QRect(0, 0, 100, 536))
        self.Controller.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
            QtGui.QSizePolicy.Maximum))
        self.ControllerLayout = QtGui.QVBoxLayout(self.Controller)
        self.ControllerLayout.setSpacing(0)
        self.ControllerLayout.setMargin(0)
        # Controller list view
        self.PreviewListWidget = SlideList(self)
        self.PreviewListWidget.setColumnCount(1)
        self.PreviewListWidget.horizontalHeader().setVisible(False)
        self.PreviewListWidget.verticalHeader().setVisible(False)
        self.PreviewListWidget.setColumnWidth(1, self.Controller.width())
        self.PreviewListWidget.isLive = self.isLive
        self.PreviewListWidget.setObjectName(u'PreviewListWidget')
        self.ControllerLayout.addWidget(self.PreviewListWidget)
        # Plugin the Base Toolbar class
        self.BaseToolbar = MasterToolbar(self.isLive)
        self.registerToolbar(u'master', self.BaseToolbar)
        self.Toolbar = self.BaseToolbar.getToolbar()
        self.ControllerLayout.addWidget(self.Toolbar)
        sizeToolbarPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizeToolbarPolicy.setHorizontalStretch(0)
        sizeToolbarPolicy.setVerticalStretch(0)
        sizeToolbarPolicy.setHeightForWidth(
            self.Toolbar.sizePolicy().hasHeightForWidth())
        self.Toolbar.setSizePolicy(sizeToolbarPolicy)
        # Screen preview area
        self.PreviewFrame = QtGui.QFrame(self.Splitter)
        self.PreviewFrame.setGeometry(QtCore.QRect(0, 0, 280, 190))
        self.PreviewFrame.setSizePolicy(QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum))
        self.PreviewFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.PreviewFrame.setFrameShadow(QtGui.QFrame.Sunken)
        self.PreviewFrame.setObjectName(u'PreviewFrame')
        self.grid = QtGui.QGridLayout(self.PreviewFrame)
        self.grid.setMargin(8)
        self.grid.setObjectName(u'grid')
        # Actual preview screen
        self.SlidePreview = QtGui.QLabel(self.parent)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SlidePreview.sizePolicy().hasHeightForWidth())
        self.SlidePreview.setSizePolicy(sizePolicy)
        self.SlidePreview.setFixedSize(QtCore.QSize(250, 210))
        self.SlidePreview.setFrameShape(QtGui.QFrame.Box)
        self.SlidePreview.setFrameShadow(QtGui.QFrame.Plain)
        self.SlidePreview.setLineWidth(1)
        self.SlidePreview.setScaledContents(True)
        self.SlidePreview.setObjectName(u'SlidePreview')
        self.grid.addWidget(self.SlidePreview, 0, 0, 1, 1)
        # Signals
        QtCore.QObject.connect(self.PreviewListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onSlideSelected)
        QtCore.QObject.connect(self.PreviewListWidget,
            QtCore.SIGNAL(u'activated(QModelIndex)'), self.onSlideSelected)
        # Window Event Handlers
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%sslide_first'% self.prefix), self.onSlideSelectedFirst)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%sslide_previous'% self.prefix), self.onSlideSelectedPrevious)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%sslide_next'% self.prefix), self.onSlideSelectedNext)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%sslide_last'% self.prefix), self.onSlideSelectedLast)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%sslide_start_loop'% self.prefix), self.onStartLoop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%sslide_stop_loop'% self.prefix), self.onStopLoop)


    def registerToolbar(self, handle,controller):
        """
        Register a new toolbar with the controller
        ``handle``
            Identifier for the toolbar being stored this should equal the
            plugins name.
        ``controller``
            The toolbar class which should extend MasterToolbar
        """
        #store the handle name in lower case so no probems later
        self.toolbarList[handle.lower()] = controller

    def retrieveToolbar(self, handle):
        """
        Find the toolbar and return master if none present
        Add extra information back into toolbar class
        ``handle``
            Identifier for the toolbar being requested
        """
        try:
            toolbar =  self.toolbarList[handle.lower()]
        except:
            toolbar = self.toolbarList[u'master']
        return toolbar

    def addServiceItem(self, item):
        """
        Method to install the service item into the controller and
        request the correct the toolbar of the plugin
        Called by plugins
        """
        self.BaseToolbar = self.retrieveToolbar(item.shortname)
        self.ControllerLayout.removeWidget(self.Toolbar)
        #remove the old toolbar
        self.Toolbar.clear()
        self.Toolbar = self.BaseToolbar.getToolbar()
        self.ControllerLayout.addWidget(self.Toolbar)
        item.render()
        self.displayServiceManagerItems(item, 0)

    def addServiceManagerItem(self, item, slideno):
        """
        Method to install the service item into the controller and
        request the correct the toolbar of the plugin
        Called by ServiceManager
        """
        self.BaseToolbar = self.retrieveToolbar(item.shortname)
        self.ControllerLayout.removeWidget(self.Toolbar)
        #remove the old toolbar
        self.Toolbar.clear()
        self.Toolbar = self.BaseToolbar.getToolbar()
        self.ControllerLayout.addWidget(self.Toolbar)
        self.displayServiceManagerItems(item, slideno)

    def displayServiceManagerItems(self, serviceitem, slideno):
        """
        Loads a ServiceItem into the system from ServiceManager
        Display the slide number passed
        """
        log.debug(u'add Service Manager Item')
        self.serviceitem = serviceitem
        slide_pixmap = QtGui.QPixmap.fromImage(self.serviceitem.frames[0][u'image'])
        slide_width = 300
        slide_height = slide_width * slide_pixmap.height() / slide_pixmap.width()
        self.PreviewListWidget.clear()
        self.PreviewListWidget.setRowCount(0)
        self.PreviewListWidget.setColumnWidth(0, slide_width)
        for framenumber, frame in enumerate(self.serviceitem.frames):
            self.PreviewListWidget.setRowCount(self.PreviewListWidget.rowCount() + 1)
            pixmap = QtGui.QPixmap.fromImage(frame[u'image'])
            item = QtGui.QTableWidgetItem()
            label = QtGui.QLabel()
            label.setMargin(8)
            label.setScaledContents(True)
            label.setPixmap(pixmap)
            self.PreviewListWidget.setCellWidget(framenumber, 0, label)
            self.PreviewListWidget.setItem(framenumber, 0, item)
            self.PreviewListWidget.setRowHeight(framenumber, slide_height)
        slide_width = self.PreviewListWidget.viewport().size().width()
        self.PreviewListWidget.setColumnWidth(0, slide_width)
        if slideno > self.PreviewListWidget.rowCount():
            self.PreviewListWidget.selectRow(self.PreviewListWidget.rowCount())
        else:
            self.PreviewListWidget.selectRow(slideno)
        self.onSlideSelected()
        self.PreviewListWidget.setFocus()

    #Screen event methods
    def onSlideSelected(self):
        """
        Generate the preview when you click on a slide.
        if this is the Live Controller also display on the screen
        """
        row = self.PreviewListWidget.currentRow()
        if row > -1 and row < self.PreviewListWidget.rowCount():
            label = self.PreviewListWidget.cellWidget(row, 0)
            smallframe = label.pixmap()
            frame = self.serviceitem.frames[row][u'image']
            self.SlidePreview.setPixmap(smallframe)
            if self.isLive:
                self.parent.mainDisplay.frameView(frame)

    def onSlideSelectedFirst(self):
        """
        Go to the first slide.
        """
        print "oSSF"
        self.PreviewListWidget.selectRow(0)
        self.onSlideSelected()

    def onBlankScreen(self):
        """
        Blank the screen.
        """
        self.parent.mainDisplay.blankDisplay()

    def onSlideSelected(self):
        """
        Generate the preview when you click on a slide.
        if this is the Live Controller also display on the screen
        """
        row = self.PreviewListWidget.currentRow()
        if row > -1 and row < self.PreviewListWidget.rowCount():
            label = self.PreviewListWidget.cellWidget(row, 0)
            smallframe = label.pixmap()
            frame = self.serviceitem.frames[row][u'image']
            self.SlidePreview.setPixmap(smallframe)
            if self.isLive:
                self.parent.mainDisplay.frameView(frame)

    def onSlideSelectedNext(self):
        """
        Go to the next slide.
        """
        row = self.PreviewListWidget.currentRow() + 1
        if row == self.PreviewListWidget.rowCount():
            row = 0
        self.PreviewListWidget.selectRow(row)
        self.onSlideSelected()

    def onSlideSelectedPrevious(self):
        """
        Go to the previous slide.
        """
        row = self.PreviewListWidget.currentRow() - 1
        if row == -1:
            row = self.PreviewListWidget.rowCount() - 1
        self.PreviewListWidget.selectRow(row)
        self.onSlideSelected()

    def onSlideSelectedLast(self):
        """
        Go to the last slide.
        """
        self.PreviewListWidget.selectRow(self.PreviewListWidget.rowCount() - 1)
        self.onSlideSelected()

    def onStartLoop(self, value):
        """
        Go to the last slide.
        """
        if self.PreviewListWidget.rowCount() > 1:
            self.timer_id = self.startTimer(int(value) * 1000)

    def onStopLoop(self):
        """
        Go to the last slide.
        """
        self.killTimer(self.timer_id)

    def timerEvent(self, event):
        if event.timerId() == self.timer_id:
            self.onSlideSelectedNext()

class MasterToolbar(QtCore.QObject):
    """
    Class from which all toolbars should extend
    """
    def __init__(self, isLive):
        self.Toolbar = None
        QtCore.QObject.__init__(self)
        self.PreviewListWidget = QtGui.QListWidget()
        self.isLive = isLive
        self.prefix  = u'preview_'
        if isLive:
            self.prefix  = u'live_'

    def getToolbar(self):
        #define toolbar here as it needs to be redefined each time
        #as the clear destroys it.
        self.defineToolbar()
        self.defineZone1()
        self.defineZone2()
        self.defineZone3()
        self.defineZone4()
        self.defineZone5()
        return self.Toolbar

    def defineToolbar(self):
        # Controller toolbar
        self.Toolbar = OpenLPToolbar(self)
        sizeToolbarPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizeToolbarPolicy.setHorizontalStretch(0)
        sizeToolbarPolicy.setVerticalStretch(0)
        sizeToolbarPolicy.setHeightForWidth(
            self.Toolbar.sizePolicy().hasHeightForWidth())
        self.Toolbar.setSizePolicy(sizeToolbarPolicy)

    def defineZone1(self):
        #Dummy Zone
        pass

    def defineZone2(self):
        if self.isLive:
            self.Toolbar.addToolbarButton(u'First Slide',
                u':/slides/slide_first.png',
                translate(u'SlideController', u'Move to first'),
                self.onSlideFirst)
        self.Toolbar.addToolbarButton(u'Previous Slide',
            u':/slides/slide_previous.png',
            translate(u'SlideController', u'Move to previous'),
            self.onSlidePrevious)
        self.Toolbar.addToolbarButton(u'Next Slide',
            u':/slides/slide_next.png',
            translate(u'SlideController', u'Move to next'),
            self.onSlideNext)
        if self.isLive:
            self.Toolbar.addToolbarButton(u'Last Slide',
                u':/slides/slide_last.png',
                translate(u'SlideController', u'Move to last'),
                self.onSlideLast)

    def defineZone3(self):
        #Dummy Zone
        pass

    def defineZone4(self):
        if self.isLive:
            self.Toolbar.addSeparator()
            self.Toolbar.addToolbarButton(u'Close Screen',
                u':/slides/slide_close.png',
                translate(u'SlideController', u'Close Screen'),
                self.onSlideBlank)

    def defineZone5(self):
        #Dummy Zone
        pass

    def onSlideFirst(self):
        Receiver().send_message(u'%sslide_first'% self.prefix)
    def onSlidePrevious(self):
        Receiver().send_message(u'%sslide_previous'% self.prefix)
    def onSlideNext(self):
        Receiver().send_message(u'%sslide_next'% self.prefix)
    def onSlideLast(self):
        Receiver().send_message(u'%sslide_last' % self.prefix)
    def onSlideBlank(self):
        Receiver().send_message(u'%sslide_blank' % self.prefix)
