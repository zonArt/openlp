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
import os

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import OpenLPToolbar, Receiver, ServiceItemType, \
    str_to_bool, PluginConfig

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
        self.songsconfig = PluginConfig(u'Songs')
        self.image_list = [
            u'Start Loop',
            u'Stop Loop',
            u'Loop Separator',
            u'Image SpinBox'
        ]
        self.song_edit_list = [
            u'Edit Song',
        ]
        self.timer_id = 0
        self.commandItem = None
        self.songEdit = False
        self.row = 0
        self.Panel = QtGui.QWidget(parent.ControlSplitter)
        # Layout for holding panel
        self.PanelLayout = QtGui.QVBoxLayout(self.Panel)
        self.PanelLayout.setSpacing(0)
        self.PanelLayout.setMargin(0)
        # Type label for the top of the slide controller
        self.TypeLabel = QtGui.QLabel(self.Panel)
        if self.isLive:
            self.TypeLabel.setText(u'<strong>%s</strong>' %
                self.trUtf8(u'Live'))
            self.split = 1
            prefix = u'live_slidecontroller'
        else:
            self.TypeLabel.setText(u'<strong>%s</strong>' %
                self.trUtf8(u'Preview'))
            self.split = 0
            prefix = u'preview_slidecontroller'
        self.TypeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PanelLayout.addWidget(self.TypeLabel)
        # Splitter
        self.Splitter = QtGui.QSplitter(self.Panel)
        self.Splitter.setOrientation(QtCore.Qt.Vertical)
        self.Splitter.setOpaqueResize(False)
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
        self.PreviewListWidget.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.PreviewListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
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
            self.Toolbar.addToolbarButton(
                u'First Slide', u':/slides/slide_first.png',
                self.trUtf8(u'Move to first'), self.onSlideSelectedFirst)
        self.Toolbar.addToolbarButton(
            u'Previous Slide', u':/slides/slide_previous.png',
            self.trUtf8(u'Move to previous'), self.onSlideSelectedPrevious)
        self.Toolbar.addToolbarButton(
            u'Next Slide', u':/slides/slide_next.png',
            self.trUtf8(u'Move to next'), self.onSlideSelectedNext)
        if self.isLive:
            self.Toolbar.addToolbarButton(
                u'Last Slide', u':/slides/slide_last.png',
                self.trUtf8(u'Move to last'), self.onSlideSelectedLast)
        if self.isLive:
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.blankButton = self.Toolbar.addToolbarButton(
                u'Blank Screen', u':/slides/slide_close.png',
                self.trUtf8(u'Blank Screen'), self.onBlankScreen, True)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'live_slide_blank'), self.onBlankDisplay)
        if not self.isLive:
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.Toolbar.addToolbarButton(
                u'Go Live', u':/system/system_live.png',
                self.trUtf8(u'Move to live'), self.onGoLive)
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.Toolbar.addToolbarButton(
                u'Edit Song', u':songs/song_edit.png',
                self.trUtf8(u'Edit and re-preview Song'), self.onEditSong)
        if isLive:
            self.Toolbar.addToolbarSeparator(u'Loop Separator')
            self.Toolbar.addToolbarButton(
                u'Start Loop',  u':/media/media_time.png',
                self.trUtf8(u'Start continuous loop'), self.onStartLoop)
            self.Toolbar.addToolbarButton(
                u'Stop Loop', u':/media/media_stop.png',
                self.trUtf8(u'Stop continuous loop'), self.onStopLoop)
            self.DelaySpinBox = QtGui.QSpinBox()
            self.Toolbar.addToolbarWidget(
                u'Image SpinBox', self.DelaySpinBox)
            self.DelaySpinBox.setSuffix(self.trUtf8(u's'))
            self.DelaySpinBox.setToolTip(self.trUtf8(u'Delay between slides in seconds'))
        self.ControllerLayout.addWidget(self.Toolbar)
        #Build a Media ToolBar
        self.Mediabar = OpenLPToolbar(self)
        self.Mediabar.addToolbarButton(
            u'Media Start',  u':/slides/media_playback_start.png',
            self.trUtf8(u'Start playing media'), self.onMediaPlay)
        self.Mediabar.addToolbarButton(
            u'Media Pause',  u':/slides/media_playback_pause.png',
            self.trUtf8(u'Start playing media'), self.onMediaPause)
        self.Mediabar.addToolbarButton(
            u'Media Stop',  u':/slides/media_playback_stop.png',
            self.trUtf8(u'Start playing media'), self.onMediaStop)
        self.volumeSlider = Phonon.VolumeSlider()
        self.volumeSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
        self.volumeSlider.setObjectName(u'volumeSlider')
        self.Mediabar.addToolbarWidget(
            u'Audio Volume', self.volumeSlider)
        self.ControllerLayout.addWidget(self.Mediabar)
        # Build the Song Toolbar
        if isLive:
            self.Songbar = OpenLPToolbar(self)
            self.Songbar.addToolbarButton(
                u'Bridge',  u':/pages/page_bridge.png',
                self.trUtf8(u'Bridge'),
                self.onSongBarHandler)
            self.Songbar.addToolbarButton(
                u'Chorus',  u':/pages/page_chorus.png',
                self.trUtf8(u'Chorus'),
                self.onSongBarHandler)
            for verse in range(1, 12):
                self.Songbar.addToolbarButton(
                    unicode(verse),  u':/pages/page_%s.png' % verse,
                    unicode(self.trUtf8(u'Verse %s'))%verse,
                    self.onSongBarHandler)
            self.ControllerLayout.addWidget(self.Songbar)
            self.Songbar.setVisible(False)
        # Screen preview area
        self.PreviewFrame = QtGui.QFrame(self.Splitter)
        self.PreviewFrame.setGeometry(QtCore.QRect(0, 0, 300, 225))
        self.PreviewFrame.setSizePolicy(QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Label))
        self.PreviewFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.PreviewFrame.setFrameShadow(QtGui.QFrame.Sunken)
        self.PreviewFrame.setObjectName(u'PreviewFrame')
        self.grid = QtGui.QGridLayout(self.PreviewFrame)
        self.grid.setMargin(8)
        self.grid.setObjectName(u'grid')
        self.SlideLayout = QtGui.QVBoxLayout()
        self.SlideLayout.setSpacing(0)
        self.SlideLayout.setMargin(0)
        self.SlideLayout.setObjectName(u'SlideLayout')
        self.mediaObject = Phonon.MediaObject(self)
        self.video = Phonon.VideoWidget()
        self.video.setVisible(False)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self.mediaObject)
        Phonon.createPath(self.mediaObject, self.video)
        Phonon.createPath(self.mediaObject, self.audio)
        self.SlideLayout.insertWidget(0, self.video)
        # Actual preview screen
        self.SlidePreview = QtGui.QLabel(self)
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
        self.SlideLayout.insertWidget(0, self.SlidePreview)
        self.grid.addLayout(self.SlideLayout, 0, 0, 1, 1)
        # Signals
        QtCore.QObject.connect(self.PreviewListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onSlideSelected)
        QtCore.QObject.connect(self.PreviewListWidget,
            QtCore.SIGNAL(u'activated(QModelIndex)'), self.onSlideSelected)
        if isLive:
            #QtCore.QObject.connect(self.blackPushButton,
            #    QtCore.SIGNAL(u'clicked(bool)'), self.onBlankScreen)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'update_spin_delay'), self.receiveSpinDelay)
            Receiver.send_message(u'request_spin_delay')
        if isLive:
            self.Toolbar.makeWidgetsInvisible(self.image_list)
        else:
            self.Toolbar.makeWidgetsInvisible(self.song_edit_list)
        self.Mediabar.setVisible(False)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_first' % prefix), self.onSlideSelectedFirst)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_next' % prefix), self.onSlideSelectedNext)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_previous' % prefix), self.onSlideSelectedPrevious)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_last' % prefix), self.onSlideSelectedLast)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_change' % prefix), self.onSlideChange)
        QtCore.QObject.connect(self.Splitter,
            QtCore.SIGNAL(u'splitterMoved(int, int)'), self.trackSplitter)

    def widthChanged(self):
        """
        Handle changes of width from the splitter between the live and preview
        controller.  Event only issues when changes have finished
        """
        if not self.commandItem:
            return
        width = self.parent.ControlSplitter.sizes()[self.split]
        height = width * self.parent.RenderManager.screen_ratio
        self.PreviewListWidget.setColumnWidth(0, width)
        for framenumber, frame in enumerate(self.commandItem.frames):
            if frame[u'text']:
                return
            self.PreviewListWidget.setRowHeight(framenumber, height)

    def trackSplitter(self, tab, pos):
        """
        Splitter between the slide list and the preview panel
        """
        pass

    def onSongBarHandler(self):
        request = self.sender().text()
        if request == u'Bridge':
            pass
        elif request == u'Chorus':
            pass
        else:
            #Remember list is 1 out!
            slideno = int(request) - 1
            if slideno > self.PreviewListWidget.rowCount():
                self.PreviewListWidget.selectRow(self.PreviewListWidget.rowCount())
            else:
                self.PreviewListWidget.selectRow(slideno)
            self.onSlideSelected()

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
        self.Toolbar.setVisible(True)
        self.Songbar.setVisible(False)
        self.Mediabar.setVisible(False)
        self.Toolbar.makeWidgetsInvisible(self.image_list)
        if item.isText():
            self.Toolbar.makeWidgetsInvisible(self.image_list)
            if item.isSong() and \
                str_to_bool(self.songsconfig.get_config(u'display songbar', True)):
                for action in self.Songbar.actions:
                    self.Songbar.actions[action].setVisible(False)
                if item.verse_order:
                    verses = item.verse_order.split(u' ')
                    for verse in verses:
                        if not verse or int(verse) > 12:
                            break
                        try:
                            self.Songbar.actions[verse].setVisible(True)
                        except:
                            #More than 20 verses hard luck
                            pass
                    self.Songbar.setVisible(True)
        elif item.isImage():
            #Not sensible to allow loops with 1 frame
            if len(item.frames) > 1:
                self.Toolbar.makeWidgetsVisible(self.image_list)
        elif item.isMedia():
            self.Toolbar.setVisible(False)
            self.Mediabar.setVisible(True)
            self.volumeSlider.setAudioOutput(self.parent.mainDisplay.audio)

    def enablePreviewToolBar(self, item):
        """
        Allows the Preview toolbar to be customised
        """
        self.Toolbar.setVisible(True)
        self.Mediabar.setVisible(False)
        self.Toolbar.makeWidgetsInvisible(self.song_edit_list)
        if item.editEnabled and item.fromPlugin:
            self.Toolbar.makeWidgetsVisible(self.song_edit_list)
        elif item.isMedia():
            self.Toolbar.setVisible(False)
            self.Mediabar.setVisible(True)
            self.volumeSlider.setAudioOutput(self.audio)

    def addServiceItem(self, item):
        """
        Method to install the service item into the controller and
        request the correct the toolbar of the plugin
        Called by plugins
        """
        log.debug(u'addServiceItem')
        #If old item was a command tell it to stop
        if self.commandItem and self.commandItem.isCommand():
            self.onMediaStop()
        self.commandItem = item
        before = time.time()
        item.render()
        log.log(15, u'Rendering took %4s' % (time.time() - before))
        self.enableToolBar(item)
        if item.isCommand():
            if self.isLive:
                Receiver.send_message(u'%s_start' % item.name.lower(), \
                    [item.shortname, item.service_item_path,
                    item.service_frames[0][u'title'], self.isLive])
            else:
                if item.isMedia():
                    self.onMediaStart(item)
        slideno = 0
        if self.songEdit:
            slideno = self.row
        self.songEdit = False
        self.displayServiceManagerItems(item, slideno)

    def replaceServiceManagerItem(self, item):
        """
        Replacement item following a remote edit
        """
        if item.__eq__(self.commandItem):
            self.addServiceManagerItem(item, self.PreviewListWidget.currentRow())

    def addServiceManagerItem(self, item, slideno):
        """
        Method to install the service item into the controller and
        request the correct the toolbar of the plugin
        Called by ServiceManager
        """
        log.debug(u'addServiceManagerItem')
        #If old item was a command tell it to stop
        if self.commandItem and self.commandItem.isCommand():
            self.onMediaStop()
        self.commandItem = item
        self.enableToolBar(item)
        if item.isCommand():
            if self.isLive:
                Receiver.send_message(u'%s_start' % item.name.lower(), \
                    [item.shortname, item.service_item_path,
                    item.service_frames[0][u'title'], slideno, self.isLive])
            else:
                if item.isMedia():
                    self.onMediaStart(item)
        self.displayServiceManagerItems(item, slideno)

    def displayServiceManagerItems(self, serviceitem, slideno):
        """
        Loads a ServiceItem into the system from ServiceManager
        Display the slide number passed
        """
        log.debug(u'displayServiceManagerItems Start')
        width = self.parent.ControlSplitter.sizes()[self.split]
        #Set pointing cursor when we have somthing to point at
        self.PreviewListWidget.setCursor(QtCore.Qt.PointingHandCursor)
        before = time.time()
        self.serviceitem = serviceitem
        self.PreviewListWidget.clear()
        self.PreviewListWidget.setRowCount(0)
        self.PreviewListWidget.setColumnWidth(0, width)
        for framenumber, frame in enumerate(self.serviceitem.frames):
            self.PreviewListWidget.setRowCount(
                self.PreviewListWidget.rowCount() + 1)
            item = QtGui.QTableWidgetItem()
            slide_height = 0
            #It is a Image
            if frame[u'text'] is None:
                label = QtGui.QLabel()
                label.setMargin(4)
                pixmap = self.parent.RenderManager.resize_image(frame[u'image'])
                label.setScaledContents(True)
                label.setPixmap(QtGui.QPixmap.fromImage(pixmap))
                self.PreviewListWidget.setCellWidget(framenumber, 0, label)
                slide_height = width * self.parent.RenderManager.screen_ratio
            else:
                item.setText(frame[u'text'])
            self.PreviewListWidget.setItem(framenumber, 0, item)
            if slide_height != 0:
                self.PreviewListWidget.setRowHeight(framenumber, slide_height)
        if self.serviceitem.frames[0][u'text']:
            self.PreviewListWidget.resizeRowsToContents()
        self.PreviewListWidget.setColumnWidth(
            0, self.PreviewListWidget.viewport().size().width())
        if slideno > self.PreviewListWidget.rowCount():
            self.PreviewListWidget.selectRow(self.PreviewListWidget.rowCount())
        else:
            self.PreviewListWidget.selectRow(slideno)
        self.onSlideSelected()
        self.PreviewListWidget.setFocus()
        log.log(15, u'Display Rendering took %4s' % (time.time() - before))
        if self.serviceitem.audit and self.isLive:
            Receiver.send_message(u'songusage_live', self.serviceitem.audit)
        log.debug(u'displayServiceManagerItems End')

    #Screen event methods
    def onSlideSelectedFirst(self):
        """
        Go to the first slide.
        """
        if self.commandItem and self.commandItem.isCommand():
            Receiver.send_message(u'%s_first'% self.commandItem.name.lower())
            self.updatePreview()
        else:
            self.PreviewListWidget.selectRow(0)
            self.onSlideSelected()

    def onBlankDisplay(self):
        self.blankButton.setChecked(self.parent.mainDisplay.displayBlank)

    def onBlankScreen(self, blanked):
        """
        Blank the screen.
        """
        if self.commandItem and self.commandItem.isCommand():
            if blanked:
                Receiver.send_message(u'%s_blank'% self.commandItem.name.lower())
            else:
                Receiver.send_message(u'%s_unblank'% self.commandItem.name.lower())
        else:
            self.parent.mainDisplay.blankDisplay(blanked)

    def onSlideSelected(self):
        """
        Generate the preview when you click on a slide.
        if this is the Live Controller also display on the screen
        """
        row = self.PreviewListWidget.currentRow()
        self.row = 0
        if row > -1 and row < self.PreviewListWidget.rowCount():
            if self.commandItem.isCommand():
                Receiver.send_message(u'%s_slide'% self.commandItem.name.lower(), [row])
                if self.isLive:
                    self.updatePreview()
            else:
                frame = self.serviceitem.frames[row][u'image']
                before = time.time()
                if frame is None:
                    frame = self.serviceitem.render_individual(row)
                self.SlidePreview.setPixmap(QtGui.QPixmap.fromImage(frame))
                log.log(15, u'Slide Rendering took %4s' % (time.time() - before))
                if self.isLive:
                    self.parent.mainDisplay.frameView(frame)
            self.row = row

    def onSlideChange(self, row):
        """
        The slide has been changed. Update the slidecontroller accordingly
        """
        self.PreviewListWidget.selectRow(row)
        self.updatePreview()

    def updatePreview(self):
        rm = self.parent.RenderManager
        if not rm.screen_list[rm.current_display][u'primary']:
            # Grab now, but try again in a couple of seconds if slide change is slow
            QtCore.QTimer.singleShot(0.5, self.grabMainDisplay)
            QtCore.QTimer.singleShot(2.5, self.grabMainDisplay)
        else:
            label = self.PreviewListWidget.cellWidget(
                self.PreviewListWidget.currentRow(), 0)
            self.SlidePreview.setPixmap(label.pixmap())

    def grabMainDisplay(self):
        rm = self.parent.RenderManager
        winid = QtGui.QApplication.desktop().winId()
        rect = rm.screen_list[rm.current_display][u'size']
        winimg = QtGui.QPixmap.grabWindow(winid, rect.x(),
            rect.y(), rect.width(), rect.height())
        self.SlidePreview.setPixmap(winimg)

    def onSlideSelectedNext(self):
        """
        Go to the next slide.
        """
        if self.commandItem and self.commandItem.isCommand():
            Receiver.send_message(u'%s_next'% self.commandItem.name.lower())
            self.updatePreview()
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
        if self.commandItem and self.commandItem.isCommand():
            Receiver.send_message(
                u'%s_previous'% self.commandItem.name.lower())
            self.updatePreview()
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
        if self.commandItem and self.commandItem.isCommand():
            Receiver.send_message(u'%s_last'% self.commandItem.name.lower())
            self.updatePreview()
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

    def onEditSong(self):
        self.songEdit = True
        Receiver.send_message(u'%s_edit' % self.commandItem.name, u'P:%s' %
            self.commandItem.editId )

    def onGoLive(self):
        """
        If preview copy slide item to live
        """
        row = self.PreviewListWidget.currentRow()
        if row > -1 and row < self.PreviewListWidget.rowCount():
            self.parent.LiveController.addServiceManagerItem(
                self.commandItem, row)

    def onMediaStart(self, item):
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        file = os.path.join(item.service_item_path, item.service_frames[0][u'title'])
        self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
        self.onMediaPlay()

    def onMediaPause(self):
        if self.isLive:
            Receiver.send_message(u'%s_pause'% self.commandItem.name.lower())
        else:
            self.mediaObject.pause()

    def onMediaPlay(self):
        if self.isLive:
            Receiver.send_message(u'%s_play'% self.commandItem.name.lower(), self.isLive)
        else:
            self.SlidePreview.hide()
            self.video.show()
            self.mediaObject.play()

    def onMediaStop(self):
        if self.isLive:
            Receiver.send_message(u'%s_stop'% self.commandItem.name.lower())
        else:
            self.mediaObject.stop()
            self.video.hide()
            self.SlidePreview.clear()
            self.SlidePreview.show()
