# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

from openlp.core.lib import ItemCapabilities

class HideMode(object):
    """
    This is basically an enumeration class which specifies the mode of a Bible.
    Mode refers to whether or not a Bible in OpenLP is a full Bible or needs to
    be downloaded from the Internet on an as-needed basis.
    """
    Blank = 1
    Theme = 2

from openlp.core.lib import OpenLPToolbar, Receiver, str_to_bool, \
    PluginConfig, resize_image

log = logging.getLogger(__name__)

class SlideList(QtGui.QTableWidget):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    def __init__(self, parent=None, name=None):
        QtGui.QTableWidget.__init__(self, parent.Controller)
        self.parent = parent
        self.hotkey_map = {QtCore.Qt.Key_Return: 'servicemanager_next_item',
                           QtCore.Qt.Key_Space: 'live_slidecontroller_next_noloop',
                           QtCore.Qt.Key_Enter: 'live_slidecontroller_next_noloop',
                           QtCore.Qt.Key_0: 'servicemanager_next_item',
                           QtCore.Qt.Key_Backspace: 'live_slidecontroller_previous_noloop'}

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
            elif event.key() in self.hotkey_map and self.parent.isLive:
                Receiver.send_message(self.hotkey_map[event.key()])
                event.accept()
            event.ignore()
        else:
            event.ignore()

class SlideController(QtGui.QWidget):
    """
    SlideController is the slide controller widget. This widget is what the
    user uses to control the displaying of verses/slides/etc on the screen.
    """
    def __init__(self, parent, settingsmanager, isLive=False):
        """
        Set up the Slide Controller.
        """
        QtGui.QWidget.__init__(self, parent)
        self.settingsmanager = settingsmanager
        self.isLive = isLive
        self.parent = parent
        self.songsconfig = PluginConfig(u'Songs')
        self.loop_list = [
            u'Start Loop',
            u'Stop Loop',
            u'Loop Separator',
            u'Image SpinBox'
        ]
        self.song_edit_list = [
            u'Edit Song',
        ]
        if isLive:
            self.labelWidth = 20
        else:
            self.labelWidth = 0
        self.timer_id = 0
        self.songEdit = False
        self.selectedRow = 0
        self.serviceItem = None
        self.Panel = QtGui.QWidget(parent.ControlSplitter)
        self.slideList = {}
        # Layout for holding panel
        self.PanelLayout = QtGui.QVBoxLayout(self.Panel)
        self.PanelLayout.setSpacing(0)
        self.PanelLayout.setMargin(0)
        # Type label for the top of the slide controller
        self.TypeLabel = QtGui.QLabel(self.Panel)
        if self.isLive:
            self.TypeLabel.setText(self.trUtf8('Live'))
            self.split = 1
            prefix = u'live_slidecontroller'
        else:
            self.TypeLabel.setText(self.trUtf8('Preview'))
            self.split = 0
            prefix = u'preview_slidecontroller'
        self.TypeLabel.setStyleSheet(u'font-weight: bold; font-size: 12pt;')
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
        self.PreviewListWidget.setColumnCount(2)
        self.PreviewListWidget.horizontalHeader().setVisible(False)
        self.PreviewListWidget.verticalHeader().setVisible(False)
        self.PreviewListWidget.setColumnWidth(1, self.labelWidth)
        self.PreviewListWidget.setColumnWidth(1, self.Controller.width() - self.labelWidth)
        self.PreviewListWidget.isLive = self.isLive
        self.PreviewListWidget.setObjectName(u'PreviewListWidget')
        self.PreviewListWidget.setSelectionBehavior(1)
        self.PreviewListWidget.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.PreviewListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PreviewListWidget.setAlternatingRowColors(True)
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
                self.trUtf8('Move to first'), self.onSlideSelectedFirst)
        self.Toolbar.addToolbarButton(
            u'Previous Slide', u':/slides/slide_previous.png',
            self.trUtf8('Move to previous'), self.onSlideSelectedPrevious)
        self.Toolbar.addToolbarButton(
            u'Next Slide', u':/slides/slide_next.png',
            self.trUtf8('Move to next'), self.onSlideSelectedNext)
        if self.isLive:
            self.Toolbar.addToolbarButton(
                u'Last Slide', u':/slides/slide_last.png',
                self.trUtf8('Move to last'), self.onSlideSelectedLast)
        if self.isLive:
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.blankButton = self.Toolbar.addToolbarButton(
                u'Blank Screen', u':/slides/slide_blank.png',
                self.trUtf8('Blank Screen'), self.onBlankDisplay, True)
            self.themeButton = self.Toolbar.addToolbarButton(
                u'Display Theme', u':/slides/slide_theme.png',
                self.trUtf8('Theme Screen'), self.onThemeDisplay, True)
            self.hideButton = self.Toolbar.addToolbarButton(
                u'Hide screen', u':/slides/slide_desktop.png',
                self.trUtf8('Hide Screen'), self.onHideDisplay, True)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'live_slide_blank'), self.blankScreen)
        if not self.isLive:
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.Toolbar.addToolbarButton(
                u'Go Live', u':/general/general_live.png',
                self.trUtf8('Move to live'), self.onGoLive)
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.Toolbar.addToolbarButton(
                u'Edit Song', u':/general/general_edit.png',
                self.trUtf8('Edit and re-preview Song'), self.onEditSong)
        if isLive:
            self.Toolbar.addToolbarSeparator(u'Loop Separator')
            self.Toolbar.addToolbarButton(
                u'Start Loop',  u':/media/media_time.png',
                self.trUtf8('Start continuous loop'), self.onStartLoop)
            self.Toolbar.addToolbarButton(
                u'Stop Loop', u':/media/media_stop.png',
                self.trUtf8('Stop continuous loop'), self.onStopLoop)
            self.DelaySpinBox = QtGui.QSpinBox()
            self.DelaySpinBox.setMinimum(1)
            self.DelaySpinBox.setMaximum(180)
            self.Toolbar.addToolbarWidget(
                u'Image SpinBox', self.DelaySpinBox)
            self.DelaySpinBox.setSuffix(self.trUtf8('s'))
            self.DelaySpinBox.setToolTip(self.trUtf8('Delay between slides in seconds'))
        self.ControllerLayout.addWidget(self.Toolbar)
        #Build a Media ToolBar
        self.Mediabar = OpenLPToolbar(self)
        self.Mediabar.addToolbarButton(
            u'Media Start',  u':/slides/media_playback_start.png',
            self.trUtf8('Start playing media'), self.onMediaPlay)
        self.Mediabar.addToolbarButton(
            u'Media Pause',  u':/slides/media_playback_pause.png',
            self.trUtf8('Start playing media'), self.onMediaPause)
        self.Mediabar.addToolbarButton(
            u'Media Stop',  u':/slides/media_playback_stop.png',
            self.trUtf8('Start playing media'), self.onMediaStop)
        if not self.isLive:
            self.seekSlider = Phonon.SeekSlider()
            self.seekSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
            self.seekSlider.setObjectName(u'seekSlider')
            self.Mediabar.addToolbarWidget(
                u'Seek Slider', self.seekSlider)
        self.volumeSlider = Phonon.VolumeSlider()
        self.volumeSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
        self.volumeSlider.setObjectName(u'volumeSlider')
        self.Mediabar.addToolbarWidget(
            u'Audio Volume', self.volumeSlider)
        self.ControllerLayout.addWidget(self.Mediabar)
        # Build the Song Toolbar
        if isLive:
            self.SongMenu = QtGui.QToolButton(self.Toolbar)
            self.SongMenu.setText(self.trUtf8('Go to Verse'))
            self.SongMenu.setPopupMode(QtGui.QToolButton.InstantPopup)
            self.Toolbar.addToolbarWidget(u'Song Menu', self.SongMenu)
            self.SongMenu.setMenu(QtGui.QMenu(self.trUtf8('Go to Verse'), self.Toolbar))
            self.Toolbar.makeWidgetsInvisible([u'Song Menu'])
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
        if not self.isLive:
            self.video.setGeometry(QtCore.QRect(0, 0, 300, 225))
            self.video.setVisible(False)
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
            QtCore.QSize(self.settingsmanager.slidecontroller_image,
                         self.settingsmanager.slidecontroller_image / 1.3 ))
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
        if isLive:
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'update_spin_delay'), self.receiveSpinDelay)
            Receiver.send_message(u'request_spin_delay')
        if isLive:
            self.Toolbar.makeWidgetsInvisible(self.loop_list)
        else:
            self.Toolbar.makeWidgetsInvisible(self.song_edit_list)
        self.Mediabar.setVisible(False)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'stop_display_loop'), self.onStopLoop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_first' % prefix), self.onSlideSelectedFirst)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_next' % prefix), self.onSlideSelectedNext)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_previous' % prefix), self.onSlideSelectedPrevious)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_next_noloop' % prefix), self.onSlideSelectedNextNoloop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_previous_noloop' % prefix),
            self.onSlideSelectedPreviousNoloop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_last' % prefix), self.onSlideSelectedLast)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'%s_change' % prefix), self.onSlideChange)
        QtCore.QObject.connect(self.Splitter,
            QtCore.SIGNAL(u'splitterMoved(int, int)'), self.trackSplitter)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.refreshServiceItem)

    def widthChanged(self):
        """
        Handle changes of width from the splitter between the live and preview
        controller.  Event only issues when changes have finished
        """
        width = self.parent.ControlSplitter.sizes()[self.split]
        height = width * self.parent.RenderManager.screen_ratio
        self.PreviewListWidget.setColumnWidth(0, self.labelWidth)
        self.PreviewListWidget.setColumnWidth(1, width - self.labelWidth)
        #Sort out image hights (Songs , bibles excluded)
        if self.serviceItem and not self.serviceItem.is_text():
            for framenumber, frame in enumerate(self.serviceItem.get_frames()):
                self.PreviewListWidget.setRowHeight(framenumber, height)

    def trackSplitter(self, tab, pos):
        """
        Splitter between the slide list and the preview panel
        """
        pass

    def onSongBarHandler(self):
        request = unicode(self.sender().text())
        slideno = self.slideList[request]
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
        self.Mediabar.setVisible(False)
        self.Toolbar.makeWidgetsInvisible([u'Song Menu'])
        self.Toolbar.makeWidgetsInvisible(self.loop_list)
        if item.is_text():
            self.Toolbar.makeWidgetsInvisible(self.loop_list)
            if str_to_bool(self.songsconfig.get_config(u'show songbar', True)) \
                and len(self.slideList) > 0:
                self.Toolbar.makeWidgetsVisible([u'Song Menu'])
        if item.is_capable(ItemCapabilities.AllowsLoop) and \
            len(item.get_frames()) > 1:
                self.Toolbar.makeWidgetsVisible(self.loop_list)
        if item.is_media():
            self.Toolbar.setVisible(False)
            self.Mediabar.setVisible(True)
            #self.volumeSlider.setAudioOutput(self.parent.mainDisplay.videoDisplay.audio)

    def enablePreviewToolBar(self, item):
        """
        Allows the Preview toolbar to be customised
        """
        self.Toolbar.setVisible(True)
        self.Mediabar.setVisible(False)
        self.Toolbar.makeWidgetsInvisible(self.song_edit_list)
        if item.is_capable(ItemCapabilities.AllowsEdit) and item.from_plugin:
            self.Toolbar.makeWidgetsVisible(self.song_edit_list)
        elif item.is_media():
            self.Toolbar.setVisible(False)
            self.Mediabar.setVisible(True)
            self.volumeSlider.setAudioOutput(self.audio)

    def refreshServiceItem(self):
        """
        Method to update the service item if the screen has changed
        """
        log.debug(u'refreshServiceItem')
        if self.serviceItem:
            if self.serviceItem.is_text() or self.serviceItem.is_image():
                item = self.serviceItem
                item.render()
                self.addServiceManagerItem(item, self.selectedRow)

    def addServiceItem(self, item):
        """
        Method to install the service item into the controller
        Called by plugins
        """
        log.debug(u'addServiceItem')
        before = time.time()
        item.render()
        log.log(15, u'Rendering took %4s' % (time.time() - before))
        slideno = 0
        if self.songEdit:
            slideno = self.selectedRow
        self.songEdit = False
        self._processItem(item, slideno)

    def replaceServiceManagerItem(self, item):
        """
        Replacement item following a remote edit
        """
        if item.__eq__(self.serviceItem):
            self._processItem(item, self.PreviewListWidget.currentRow())

    def addServiceManagerItem(self, item, slideno):
        """
        Method to install the service item into the controller and
        request the correct toolbar for the plugin.
        Called by ServiceManager
        """
        log.debug(u'addServiceManagerItem')
        #If service item is the same as the current on only change slide
        if item.__eq__(self.serviceItem):
            self.PreviewListWidget.selectRow(slideno)
            self.onSlideSelected()
            return
        self._processItem(item, slideno)

    def _processItem(self, serviceItem, slideno):
        """
        Loads a ServiceItem into the system from ServiceManager
        Display the slide number passed
        """
        log.debug(u'processsManagerItem')
        #If old item was a command tell it to stop
        if self.serviceItem and self.serviceItem.is_command():
            self.onMediaStop()
        if serviceItem.is_media():
            self.onMediaStart(serviceItem)
        elif serviceItem.is_command():
            if self.isLive:
                blanked = self.blankButton.isChecked()
            else:
                blanked = False
            Receiver.send_message(u'%s_start' % serviceItem.name.lower(), \
                [serviceItem.title, serviceItem.get_frame_path(),
                serviceItem.get_frame_title(), slideno, self.isLive, blanked])
        self.slideList = {}
        width = self.parent.ControlSplitter.sizes()[self.split]
        #Set pointing cursor when we have somthing to point at
        self.PreviewListWidget.setCursor(QtCore.Qt.PointingHandCursor)
        before = time.time()
        self.serviceItem = serviceItem
        self.PreviewListWidget.clear()
        self.PreviewListWidget.setRowCount(0)
        self.PreviewListWidget.setColumnWidth(0, self.labelWidth)
        self.PreviewListWidget.setColumnWidth(1, width - self.labelWidth)
        if self.isLive:
            self.SongMenu.menu().clear()
        row = 0
        for framenumber, frame in enumerate(self.serviceItem.get_frames()):
            self.PreviewListWidget.setRowCount(
                self.PreviewListWidget.rowCount() + 1)
            rowitem = QtGui.QTableWidgetItem()
            item = QtGui.QTableWidgetItem()
            slide_height = 0
            #It is a based Text Render
            if self.serviceItem.is_text():
                if self.isLive and frame[u'verseTag'] is not None:
                    #only load the slot once
                    bits = frame[u'verseTag'].split(u':')
                    tag = None
                    #If verse handle verse number else tag only
                    if bits[0] == self.trUtf8('Verse') or \
                        bits[0] == self.trUtf8('Chorus'):
                        tag = u'%s\n%s' % (bits[0][0], bits[1][0:] )
                        tag1 = u'%s%s' % (bits[0][0], bits[1][0:] )
                        row = tag
                    else:
                        tag = bits[0]
                        tag1 = tag
                        row = bits[0][0:1]
                    if tag1 not in self.slideList:
                        self.slideList[tag1] = framenumber
                        self.SongMenu.menu().addAction(self.trUtf8(u'%s'%tag1),
                            self.onSongBarHandler)
                else:
                    row += 1
                item.setText(frame[u'text'])
            else:
                label = QtGui.QLabel()
                label.setMargin(4)
                pixmap = resize_image(frame[u'image'],
                                      self.parent.RenderManager.width,
                                      self.parent.RenderManager.height)
                label.setScaledContents(True)
                label.setPixmap(QtGui.QPixmap.fromImage(pixmap))
                self.PreviewListWidget.setCellWidget(framenumber, 1, label)
                slide_height = width * self.parent.RenderManager.screen_ratio
                row += 1
            rowitem.setText(unicode(row))
            rowitem.setTextAlignment(QtCore.Qt.AlignVCenter)
            self.PreviewListWidget.setItem(framenumber, 0, rowitem)
            self.PreviewListWidget.setItem(framenumber, 1, item)
            if slide_height != 0:
                self.PreviewListWidget.setRowHeight(framenumber, slide_height)
        if self.serviceItem.is_text():
            self.PreviewListWidget.resizeRowsToContents()
        self.PreviewListWidget.setColumnWidth(0, self.labelWidth)
        self.PreviewListWidget.setColumnWidth(1,
                        self.PreviewListWidget.viewport().size().width() - self.labelWidth )
        if slideno > self.PreviewListWidget.rowCount():
            self.PreviewListWidget.selectRow(self.PreviewListWidget.rowCount())
        else:
            self.PreviewListWidget.selectRow(slideno)
        self.enableToolBar(serviceItem)
        self.onSlideSelected()
        self.PreviewListWidget.setFocus()
        log.log(15, u'Display Rendering took %4s' % (time.time() - before))
        if self.isLive:
            self.serviceItem.request_audit()

    #Screen event methods
    def onSlideSelectedFirst(self):
        """
        Go to the first slide.
        """
        if not self.serviceItem:
            return
        if self.serviceItem.is_command():
            Receiver.send_message(u'%s_first'% \
                self.serviceItem.name.lower(), self.isLive)
            self.updatePreview()
        else:
            self.PreviewListWidget.selectRow(0)
            self.onSlideSelected()

    def onBlankDisplay(self, force=False):
        """
        Handle the blank screen button
        """
        log.debug(u'onBlankDisplay %d' % force)
        if force:
            self.blankButton.setChecked(True)
        self.blankScreen(HideMode.Blank, self.blankButton.isChecked())
        self.parent.generalConfig.set_config(u'screen blank',
                                            self.blankButton.isChecked())

    def onThemeDisplay(self, force=False):
        """
        Handle the Theme screen button
        """
        log.debug(u'onThemeDisplay %d' % force)
        if force:
            self.themeButton.setChecked(True)
        self.blankScreen(HideMode.Theme, self.themeButton.isChecked())

    def onHideDisplay(self, force=False):
        """
        Handle the Hide screen button
        """
        log.debug(u'onHideDisplay %d' % force)
        if force:
            self.hideButton.setChecked(True)
        if self.hideButton.isChecked():
            self.parent.mainDisplay.hideDisplay()
        else:
            self.parent.mainDisplay.showDisplay()

    def blankScreen(self, blankType, blanked=False):
        """
        Blank the display screen.
        """
        if self.serviceItem is not None:
            if self.serviceItem.is_command():
                if blanked:
                    Receiver.send_message(u'%s_blank'% self.serviceItem.name.lower())
                else:
                    Receiver.send_message(u'%s_unblank'% self.serviceItem.name.lower())
            else:
                self.parent.mainDisplay.blankDisplay(blankType, blanked)
        else:
            self.parent.mainDisplay.blankDisplay(blankType, blanked)

    def onSlideSelected(self):
        """
        Generate the preview when you click on a slide.
        if this is the Live Controller also display on the screen
        """
        row = self.PreviewListWidget.currentRow()
        self.selectedRow = 0
        if row > -1 and row < self.PreviewListWidget.rowCount():
            if self.serviceItem.is_command() and self.isLive:
                Receiver.send_message(u'%s_slide'% \
                    self.serviceItem.name.lower(), u'%s:%s' % (row, self.isLive))
                self.updatePreview()
            else:
                before = time.time()
                frame = self.serviceItem.get_rendered_frame(row)
                if isinstance(frame, QtGui.QImage):
                    self.SlidePreview.setPixmap(QtGui.QPixmap.fromImage(frame))
                else:
                    if isinstance(frame[u'main'], basestring):
                        self.SlidePreview.setPixmap(QtGui.QPixmap(frame[u'main']))
                    else:
                        self.SlidePreview.setPixmap(QtGui.QPixmap.fromImage(frame[u'main']))
                log.log(15, u'Slide Rendering took %4s' % (time.time() - before))
                if self.isLive:
                    self.parent.displayManager.mainDisplay.frameView(frame, True)
            self.selectedRow = row

    def onSlideChange(self, row):
        """
        The slide has been changed. Update the slidecontroller accordingly
        """
        self.PreviewListWidget.selectRow(row)
        self.updatePreview()

    def updatePreview(self):
        rm = self.parent.RenderManager
        if not rm.screens.current[u'primary']:
            # Grab now, but try again in a couple of seconds if slide change is slow
            QtCore.QTimer.singleShot(0.5, self.grabMainDisplay)
            QtCore.QTimer.singleShot(2.5, self.grabMainDisplay)
        else:
            label = self.PreviewListWidget.cellWidget(
                self.PreviewListWidget.currentRow(), 1)
            self.SlidePreview.setPixmap(label.pixmap())

    def grabMainDisplay(self):
        rm = self.parent.RenderManager
        winid = QtGui.QApplication.desktop().winId()
        rect = rm.screens.current[u'size']
        winimg = QtGui.QPixmap.grabWindow(winid, rect.x(),
            rect.y(), rect.width(), rect.height())
        self.SlidePreview.setPixmap(winimg)

    def onSlideSelectedNextNoloop(self):
        self.onSlideSelectedNext(False)

    def onSlideSelectedNext(self, loop=True):
        """
        Go to the next slide.
        """
        if not self.serviceItem:
            return
        if self.serviceItem.is_command():
            Receiver.send_message(u'%s_next' % \
                self.serviceItem.name.lower(), self.isLive)
            self.updatePreview()
        else:
            row = self.PreviewListWidget.currentRow() + 1
            if row == self.PreviewListWidget.rowCount():
                if loop:
                    row = 0
                else:
                    Receiver.send_message('servicemanager_next_item')
                    return
            self.PreviewListWidget.selectRow(row)
            self.onSlideSelected()

    def onSlideSelectedPreviousNoloop(self):
        self.onSlideSelectedPrevious(False)

    def onSlideSelectedPrevious(self, loop=True):
        """
        Go to the previous slide.
        """
        if not self.serviceItem:
            return
        if self.serviceItem.is_command():
            Receiver.send_message(
                u'%s_previous'% self.serviceItem.name.lower(),  self.isLive)
            self.updatePreview()
        else:
            row = self.PreviewListWidget.currentRow() - 1
            if row == -1:
                if loop:
                    row = self.PreviewListWidget.rowCount() - 1
                else:
                    row = 0
            self.PreviewListWidget.selectRow(row)
            self.onSlideSelected()

    def onSlideSelectedLast(self):
        """
        Go to the last slide.
        """
        if not self.serviceItem:
            return
        if self.serviceItem.is_command():
            Receiver.send_message(u'%s_last' % \
                self.serviceItem.name.lower(), self.isLive)
            self.updatePreview()
        else:
            self.PreviewListWidget.selectRow(
                        self.PreviewListWidget.rowCount() - 1)
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
        Receiver.send_message(u'%s_edit' % self.serviceItem.name, u'P:%s' %
            self.serviceItem.editId )

    def onGoLive(self):
        """
        If preview copy slide item to live
        """
        row = self.PreviewListWidget.currentRow()
        if row > -1 and row < self.PreviewListWidget.rowCount():
            self.parent.LiveController.addServiceManagerItem(
                self.serviceItem, row)

    def onMediaStart(self, item):
        if self.isLive:
            Receiver.send_message(u'%s_start' % item.name.lower(), \
                [item.title, item.get_frame_path(),
                item.get_frame_title(), self.isLive, self.blankButton.isChecked()])
        else:
            self.mediaObject.stop()
            self.mediaObject.clearQueue()
            file = os.path.join(item.get_frame_path(), item.get_frame_title())
            self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
            self.seekSlider.setMediaObject(self.mediaObject)
            self.seekSlider.show()
            self.onMediaPlay()

    def onMediaPause(self):
        if self.isLive:
            Receiver.send_message(u'%s_pause'% self.serviceItem.name.lower())
        else:
            self.mediaObject.pause()

    def onMediaPlay(self):
        if self.isLive:
            Receiver.send_message(u'%s_play'% self.serviceItem.name.lower(), self.isLive)
        else:
            self.SlidePreview.hide()
            self.video.show()
            self.mediaObject.play()

    def onMediaStop(self):
        if self.isLive:
            Receiver.send_message(u'%s_stop'% self.serviceItem.name.lower(), self.isLive)
        else:
            self.mediaObject.stop()
            self.video.hide()
        self.SlidePreview.clear()
        self.SlidePreview.show()
