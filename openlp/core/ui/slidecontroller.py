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

import logging
import time

from PyQt4 import QtCore, QtGui
from openlp.core.lib import OpenLPToolbar, translate, Receiver, ServiceType

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
    SlideController is the slide controller widget. This widget is what the
    user uses to control the displaying of verses/slides/etc on the screen.
    """
    global log
    log = logging.getLogger(u'SlideController')

    def __init__(self, parent, settingsmanager, isLive=False):
        """
        Set up the Slide Controller.
        """
        QtGui.QWidget.__init__(self, parent)
        self.settingsmanager = settingsmanager
        self.isLive = isLive
        self.parent = parent
        self.image_list = [
            u'Start Loop', u'Stop Loop', u'Loop Separator', u'Image SpinBox']
        self.timer_id = 0
        self.commandItem = None
        self.Panel = QtGui.QWidget(parent.ControlSplitter)
        # Layout for holding panel
        self.PanelLayout = QtGui.QVBoxLayout(self.Panel)
        self.PanelLayout.setSpacing(0)
        self.PanelLayout.setMargin(0)
        # Type label for the top of the slide controller
        self.TypeLabel = QtGui.QLabel(self.Panel)
        if self.isLive:
            self.TypeLabel.setText(u'<strong>%s</strong>' % translate(u'SlideController', u'Live'))
        else:
            self.TypeLabel.setText(u'<strong>%s</strong>' % translate(u'SlideController', u'Preview'))
        self.TypeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PanelLayout.addWidget(self.TypeLabel)
        # Splitter
        self.Splitter = QtGui.QSplitter(self.Panel)
        self.Splitter.setOrientation(QtCore.Qt.Vertical)
        self.PanelLayout.addWidget(self.Splitter)
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
        # Build the full toolbar
        self.Toolbar = OpenLPToolbar(self)
        sizeToolbarPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizeToolbarPolicy.setHorizontalStretch(0)
        sizeToolbarPolicy.setVerticalStretch(0)
        sizeToolbarPolicy.setHeightForWidth(
            self.Toolbar.sizePolicy().hasHeightForWidth())
        self.Toolbar.setSizePolicy(sizeToolbarPolicy)
        if self.isLive:
            self.Toolbar.addToolbarButton(u'First Slide',
                u':/slides/slide_first.png',
                translate(u'SlideController', u'Move to first'),
                self.onSlideSelectedFirst)
        self.Toolbar.addToolbarButton(u'Previous Slide',
            u':/slides/slide_previous.png',
            translate(u'SlideController', u'Move to previous'),
            self.onSlideSelectedPrevious)
        self.Toolbar.addToolbarButton(u'Next Slide',
            u':/slides/slide_next.png',
            translate(u'SlideController', u'Move to next'),
            self.onSlideSelectedNext)
        if self.isLive:
            self.Toolbar.addToolbarButton(u'Last Slide',
                u':/slides/slide_last.png',
                translate(u'SlideController', u'Move to last'),
                self.onSlideSelectedLast)
        if self.isLive:
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.blackPushButton = self.Toolbar.addPushButton(
                u':/slides/slide_close.png')
        if not self.isLive:
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.Toolbar.addToolbarButton(u'Go Live',
                u':/system/system_live.png',
                translate(u'SlideController', u'Move to live'),
                self.onGoLive)
        if isLive:
            self.Toolbar.addToolbarSeparator(u'Loop Separator')
            self.Toolbar.addToolbarButton(u'Start Loop',
                u':/media/media_time.png',
                translate(u'SlideController', u'Start continuous loop'),
                self.onStartLoop)
            self.Toolbar.addToolbarButton(u'Stop Loop',
                u':/media/media_stop.png',
                translate(u'SlideController', u'Stop continuous loop'),
                self.onStopLoop)
            self.DelaySpinBox = QtGui.QSpinBox()
            self.Toolbar.addToolbarWidget(u'Image SpinBox', self.DelaySpinBox)
            self.DelaySpinBox.setSuffix(translate(u'SlideController', u's'))

        self.ControllerLayout.addWidget(self.Toolbar)
        # Screen preview area
        self.PreviewFrame = QtGui.QFrame(self.Splitter)
        self.PreviewFrame.setGeometry(QtCore.QRect(0, 0, 300, 225))
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
        self.SlidePreview.setFixedSize(
            QtCore.QSize(self.settingsmanager.slidecontroller_image, 225))
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
        if isLive:
            QtCore.QObject.connect(self.blackPushButton,
                QtCore.SIGNAL(u'toggled(bool)'), self.onBlankScreen)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'update_spin_delay'), self.receiveSpinDelay)
            Receiver().send_message(u'request_spin_delay')
        if isLive:
            self.Toolbar.makeWidgetsInvisible(self.image_list)
        else:
            pass

    def receiveSpinDelay(self, value):
        self.DelaySpinBox.setValue(int(value))

    def enableToolBar(self, item):
        """
        Allows the toolbars to be reconfigured based on Controller Type
        and ServiceItem Type
        """
        if self.isLive:
            self.enableLiveToolBar(item)
        else:
            self.enablePreviewToolBar(item)

    def enableLiveToolBar(self, item):
        """
        Allows the live toolbar to be customised
        """
        if item.service_item_type == ServiceType.Text:
            self.Toolbar.makeWidgetsInvisible(self.image_list)
        elif item.service_item_type == ServiceType.Image:
            #Not sensible to allow loops with 1 frame
            if len(item.frames) > 1:
                self.Toolbar.makeWidgetsVisible(self.image_list)
            else:
                self.Toolbar.makeWidgetsInvisible(self.image_list)

    def enablePreviewToolBar(self, item):
        """
        Allows the Preview toolbar to be customised
        """
        pass

    def addServiceItem(self, item):
        """
        Method to install the service item into the controller and
        request the correct the toolbar of the plugin
        Called by plugins
        """
        log.debug(u'addServiceItem')
        #If old item was a command tell it to stop
        if self.commandItem is not None and \
            self.commandItem.service_item_type == ServiceType.Command:
            Receiver().send_message(u'%s_stop'% self.commandItem.name.lower())
        self.commandItem = item
        before = time.time()
        item.render()
        log.info(u'Rendering took %4s' % (time.time() - before))
        self.enableToolBar(item)
        if item.service_item_type == ServiceType.Command:
            Receiver().send_message(u'%s_start' % item.name.lower(), \
                [item.shortname, item.service_item_path,
                item.service_frames[0][u'title']])
        else:
            self.displayServiceManagerItems(item, 0)

    def addServiceManagerItem(self, item, slideno):
        """
        Method to install the service item into the controller and
        request the correct the toolbar of the plugin
        Called by ServiceManager
        """
        log.debug(u'addServiceItem')
        #If old item was a command tell it to stop
        if self.commandItem is not None and \
            self.commandItem.service_item_type == ServiceType.Command:
            Receiver().send_message(u'%s_stop'% self.commandItem.name.lower())
        self.commandItem = item
        self.enableToolBar(item)
        if item.service_item_type == ServiceType.Command:
            Receiver().send_message(u'%s_start' % item.name.lower(), \
                [item.shortname, item.service_item_path,
                item.service_frames[0][u'title'], slideno])
        else:
            self.displayServiceManagerItems(item, slideno)

    def displayServiceManagerItems(self, serviceitem, slideno):
        """
        Loads a ServiceItem into the system from ServiceManager
        Display the slide number passed
        """
        log.debug(u'displayServiceManagerItems Start')
        before = time.time()
        self.serviceitem = serviceitem
        self.PreviewListWidget.clear()
        self.PreviewListWidget.setRowCount(0)
        self.PreviewListWidget.setColumnWidth(
            0, self.settingsmanager.slidecontroller_image)
        for framenumber, frame in enumerate(self.serviceitem.frames):
            self.PreviewListWidget.setRowCount(
                self.PreviewListWidget.rowCount() + 1)
            item = QtGui.QTableWidgetItem()
            label = QtGui.QLabel()
            label.setMargin(8)
            #It is a Image
            if frame[u'text'] is None:
                pixmap = self.parent.RenderManager.resize_image(frame[u'image'])
                label.setScaledContents(True)
                label.setPixmap(QtGui.QPixmap.fromImage(pixmap))
            else:
                label.setText(frame[u'text'])
            self.PreviewListWidget.setCellWidget(framenumber, 0, label)
            self.PreviewListWidget.setItem(framenumber, 0, item)
            slide_height = self.settingsmanager.slidecontroller_image * \
                self.parent.RenderManager.screen_ratio
            self.PreviewListWidget.setRowHeight(framenumber, slide_height)
        self.PreviewListWidget.setColumnWidth(
            0, self.PreviewListWidget.viewport().size().width())
        if slideno > self.PreviewListWidget.rowCount():
            self.PreviewListWidget.selectRow(self.PreviewListWidget.rowCount())
        else:
            self.PreviewListWidget.selectRow(slideno)
        self.onSlideSelected()
        self.PreviewListWidget.setFocus()
        log.info(u'Display Rendering took %4s' % (time.time() - before))
        if self.serviceitem.audit != u'':
            Receiver().send_message(u'audit_live', self.serviceitem.audit)
        log.debug(u'displayServiceManagerItems End')

    #Screen event methods
    def onSlideSelectedFirst(self):
        """
        Go to the first slide.
        """
        if self.commandItem.service_item_type == ServiceType.Command:
            Receiver().send_message(u'%s_first'% self.commandItem.name.lower())
        else:
            self.PreviewListWidget.selectRow(0)
            self.onSlideSelected()

    def onBlankScreen(self, blanked):
        """
        Blank the screen.
        """
        if self.commandItem.service_item_type == ServiceType.Command:
            if blanked:
                Receiver().send_message(u'%s_blank'% self.commandItem.name.lower())
            else:
                Receiver().send_message(u'%s_unblank'% self.commandItem.name.lower())
        else:          
            self.parent.mainDisplay.blankDisplay()

    def onSlideSelected(self):
        """
        Generate the preview when you click on a slide.
        if this is the Live Controller also display on the screen
        """
        row = self.PreviewListWidget.currentRow()
        if row > -1 and row < self.PreviewListWidget.rowCount():
            if self.commandItem.service_item_type == ServiceType.Command:
                Receiver().send_message(u'%s_slide'% self.commandItem.name.lower(), [row])                
            else:
                #label = self.PreviewListWidget.cellWidget(row, 0)
                frame = self.serviceitem.frames[row][u'image']
                before = time.time()
                if frame is None:
                    frame = self.serviceitem.render_individual(row)
                self.SlidePreview.setPixmap(QtGui.QPixmap.fromImage(frame))
                log.info(u'Slide Rendering took %4s' % (time.time() - before))
                if self.isLive:
                    self.parent.mainDisplay.frameView(frame)

    def onSlideSelectedNext(self):
        """
        Go to the next slide.
        """
        if self.commandItem.service_item_type == ServiceType.Command:
            Receiver().send_message(u'%s_next'% self.commandItem.name.lower())
        else:
            row = self.PreviewListWidget.currentRow() + 1
            if row == self.PreviewListWidget.rowCount():
                row = 0
            self.PreviewListWidget.selectRow(row)
            self.onSlideSelected()

    def onSlideSelectedPrevious(self):
        """
        Go to the previous slide.
        """
        if self.commandItem.service_item_type == ServiceType.Command:
            Receiver().send_message(
                u'%s_previous'% self.commandItem.name.lower())
        else:
            row = self.PreviewListWidget.currentRow() - 1
            if row == -1:
                row = self.PreviewListWidget.rowCount() - 1
            self.PreviewListWidget.selectRow(row)
            self.onSlideSelected()

    def onSlideSelectedLast(self):
        """
        Go to the last slide.
        """
        if self.commandItem.service_item_type == ServiceType.Command:
            Receiver().send_message(u'%s_last'% self.commandItem.name.lower())
        else:
            self.PreviewListWidget.selectRow(self.PreviewListWidget.rowCount() - 1)
            self.onSlideSelected()

    def onStartLoop(self):
        """
        Start the timer loop running and store the timer id
        """
        if self.PreviewListWidget.rowCount() > 1:
            self.timer_id = self.startTimer(
                int(self.DelaySpinBox.value()) * 1000)

    def onStopLoop(self):
        """
        Stop the timer loop running
        """
        self.killTimer(self.timer_id)

    def timerEvent(self, event):
        """
        If the timer event is for this window select next slide
        """
        if event.timerId() == self.timer_id:
            self.onSlideSelectedNext()

    def onGoLive(self):
        """
        If preview copy slide item to live
        """
        row = self.PreviewListWidget.currentRow()
        if row > -1 and row < self.PreviewListWidget.rowCount():
            self.parent.LiveController.addServiceManagerItem(
                self.commandItem, row)
