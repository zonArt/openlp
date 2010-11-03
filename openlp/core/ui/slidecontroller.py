# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
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
import os

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.ui import HideMode, MainDisplay
from openlp.core.lib import OpenLPToolbar, Receiver, resize_image, \
    ItemCapabilities, translate

log = logging.getLogger(__name__)

class SlideList(QtGui.QTableWidget):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    def __init__(self, parent=None, name=None):
        QtGui.QTableWidget.__init__(self, parent.Controller)
        self.parent = parent
        self.hotkeyMap = {
           QtCore.Qt.Key_Return: 'servicemanager_next_item',
           QtCore.Qt.Key_Space: 'slidecontroller_live_next_noloop',
           QtCore.Qt.Key_Enter: 'slidecontroller_live_next_noloop',
           QtCore.Qt.Key_0: 'servicemanager_next_item',
           QtCore.Qt.Key_Backspace: 'slidecontroller_live_previous_noloop'}

    def keyPressEvent(self, event):
        if isinstance(event, QtGui.QKeyEvent):
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
            elif event.key() in self.hotkeyMap and self.parent.isLive:
                Receiver.send_message(self.hotkeyMap[event.key()])
                event.accept()
            event.ignore()
        else:
            event.ignore()

class SlideController(QtGui.QWidget):
    """
    SlideController is the slide controller widget. This widget is what the
    user uses to control the displaying of verses/slides/etc on the screen.
    """
    def __init__(self, parent, settingsmanager, screens, isLive=False):
        """
        Set up the Slide Controller.
        """
        QtGui.QWidget.__init__(self, parent)
        self.settingsmanager = settingsmanager
        self.isLive = isLive
        self.parent = parent
        self.screens = screens
        self.ratio = float(self.screens.current[u'size'].width()) / \
            float(self.screens.current[u'size'].height())
        self.display = MainDisplay(self, screens, isLive)
        self.loopList = [
            u'Start Loop',
            u'Loop Separator',
            u'Image SpinBox'
        ]
        self.songEditList = [
            u'Edit Song',
        ]
        self.volume = 10
        self.timer_id = 0
        self.songEdit = False
        self.selectedRow = 0
        self.serviceItem = None
        self.alertTab = None
        self.Panel = QtGui.QWidget(parent.ControlSplitter)
        self.slideList = {}
        # Layout for holding panel
        self.PanelLayout = QtGui.QVBoxLayout(self.Panel)
        self.PanelLayout.setSpacing(0)
        self.PanelLayout.setMargin(0)
        # Type label for the top of the slide controller
        self.TypeLabel = QtGui.QLabel(self.Panel)
        if self.isLive:
            self.TypeLabel.setText(translate('OpenLP.SlideController', 'Live'))
            self.split = 1
            self.typePrefix = u'live'
        else:
            self.TypeLabel.setText(translate('OpenLP.SlideController',
                'Preview'))
            self.split = 0
            self.typePrefix = u'preview'
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
        self.PreviewListWidget.setColumnCount(1)
        self.PreviewListWidget.horizontalHeader().setVisible(False)
        self.PreviewListWidget.setColumnWidth(
            0, self.Controller.width())
        self.PreviewListWidget.isLive = self.isLive
        self.PreviewListWidget.setObjectName(u'PreviewListWidget')
        self.PreviewListWidget.setSelectionBehavior(1)
        self.PreviewListWidget.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.PreviewListWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
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
        self.Toolbar.addToolbarButton(
            u'Previous Slide', u':/slides/slide_previous.png',
            translate('OpenLP.SlideController', 'Move to previous'),
            self.onSlideSelectedPrevious)
        self.Toolbar.addToolbarButton(
            u'Next Slide', u':/slides/slide_next.png',
            translate('OpenLP.SlideController', 'Move to next'),
            self.onSlideSelectedNext)
        if self.isLive:
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.HideMenu = QtGui.QToolButton(self.Toolbar)
            self.HideMenu.setText(translate('OpenLP.SlideController', 'Hide'))
            self.HideMenu.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
            self.Toolbar.addToolbarWidget(u'Hide Menu', self.HideMenu)
            self.HideMenu.setMenu(QtGui.QMenu(
                translate('OpenLP.SlideController', 'Hide'), self.Toolbar))
            self.BlankScreen = QtGui.QAction(QtGui.QIcon(
                u':/slides/slide_blank.png'),
                translate('OpenLP.SlideController',
                    'Blank Screen'), self.HideMenu)
            self.BlankScreen.setCheckable(True)
            QtCore.QObject.connect(self.BlankScreen,
                QtCore.SIGNAL("triggered(bool)"), self.onBlankDisplay)
            self.ThemeScreen = QtGui.QAction(QtGui.QIcon(
                u':/slides/slide_theme.png'),
                translate('OpenLP.SlideController',
                    'Blank to Theme'), self.HideMenu)
            self.ThemeScreen.setCheckable(True)
            QtCore.QObject.connect(self.ThemeScreen,
                QtCore.SIGNAL("triggered(bool)"), self.onThemeDisplay)
            if self.screens.display_count > 1:
                self.DesktopScreen = QtGui.QAction(QtGui.QIcon(
                    u':/slides/slide_desktop.png'),
                    translate('OpenLP.SlideController',
                        'Show Desktop'), self.HideMenu)
                self.DesktopScreen.setCheckable(True)
                QtCore.QObject.connect(self.DesktopScreen,
                    QtCore.SIGNAL("triggered(bool)"), self.onHideDisplay)
            self.HideMenu.setDefaultAction(self.BlankScreen)
            self.HideMenu.menu().addAction(self.BlankScreen)
            self.HideMenu.menu().addAction(self.ThemeScreen)
            if self.screens.display_count > 1:
                self.HideMenu.menu().addAction(self.DesktopScreen)
        if not self.isLive:
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.Toolbar.addToolbarButton(
                u'Go Live', u':/general/general_live.png',
                translate('OpenLP.SlideController', 'Move to live'),
                self.onGoLive)
            self.Toolbar.addToolbarSeparator(u'Close Separator')
            self.Toolbar.addToolbarButton(
                u'Edit Song', u':/general/general_edit.png',
                translate('OpenLP.SlideController',
                'Edit and reload song preview'),
                self.onEditSong)
        if isLive:
            self.Toolbar.addToolbarSeparator(u'Loop Separator')
            self.Toolbar.addToolbarButton(
                u'Start Loop', u':/media/media_time.png',
                translate('OpenLP.SlideController', 'Start continuous loop'),
                self.onStartLoop)
            self.Toolbar.addToolbarButton(
                u'Stop Loop', u':/media/media_stop.png',
                translate('OpenLP.SlideController', 'Stop continuous loop'),
                self.onStopLoop)
            self.DelaySpinBox = QtGui.QSpinBox()
            self.DelaySpinBox.setMinimum(1)
            self.DelaySpinBox.setMaximum(180)
            self.Toolbar.addToolbarWidget(
                u'Image SpinBox', self.DelaySpinBox)
            self.DelaySpinBox.setSuffix(translate('OpenLP.SlideController',
                's'))
            self.DelaySpinBox.setToolTip(translate('OpenLP.SlideController',
                'Delay between slides in seconds'))
        self.ControllerLayout.addWidget(self.Toolbar)
        # Build a Media ToolBar
        self.Mediabar = OpenLPToolbar(self)
        self.Mediabar.addToolbarButton(
            u'Media Start', u':/slides/media_playback_start.png',
            translate('OpenLP.SlideController', 'Start playing media'),
            self.onMediaPlay)
        self.Mediabar.addToolbarButton(
            u'Media Pause', u':/slides/media_playback_pause.png',
            translate('OpenLP.SlideController', 'Start playing media'),
            self.onMediaPause)
        self.Mediabar.addToolbarButton(
            u'Media Stop', u':/slides/media_playback_stop.png',
            translate('OpenLP.SlideController', 'Start playing media'),
            self.onMediaStop)
        if not self.isLive:
            self.seekSlider = Phonon.SeekSlider()
            self.seekSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
            self.seekSlider.setObjectName(u'seekSlider')
            self.Mediabar.addToolbarWidget(
                u'Seek Slider', self.seekSlider)
            self.volumeSlider = Phonon.VolumeSlider()
            self.volumeSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
            self.volumeSlider.setObjectName(u'volumeSlider')
            self.Mediabar.addToolbarWidget(u'Audio Volume', self.volumeSlider)
        else:
            self.volumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
            self.volumeSlider.setTickInterval(1)
            self.volumeSlider.setTickPosition(QtGui.QSlider.TicksAbove)
            self.volumeSlider.setMinimum(0)
            self.volumeSlider.setMaximum(10)
            self.volumeSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
            self.volumeSlider.setObjectName(u'volumeSlider')
            self.Mediabar.addToolbarWidget(u'Audio Volume', self.volumeSlider)
        self.ControllerLayout.addWidget(self.Mediabar)
        # Build the Song Toolbar
        if isLive:
            self.SongMenu = QtGui.QToolButton(self.Toolbar)
            self.SongMenu.setText(translate('OpenLP.SlideController',
                'Go To'))
            self.SongMenu.setPopupMode(QtGui.QToolButton.InstantPopup)
            self.Toolbar.addToolbarWidget(u'Song Menu', self.SongMenu)
            self.SongMenu.setMenu(QtGui.QMenu(
                translate('OpenLP.SlideController', 'Go To'),
                self.Toolbar))
            self.Toolbar.makeWidgetsInvisible([u'Song Menu'])
        # Screen preview area
        self.PreviewFrame = QtGui.QFrame(self.Splitter)
        self.PreviewFrame.setGeometry(QtCore.QRect(0, 0, 300, 225))
        self.PreviewFrame.setSizePolicy(QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum,
            QtGui.QSizePolicy.Label))
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
            self.settingsmanager.slidecontroller_image / self.ratio))
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
        if not self.isLive:
            if QtCore.QSettings().value(u'advanced/double click live',
                QtCore.QVariant(False)).toBool():
                QtCore.QObject.connect(self.PreviewListWidget,
                    QtCore.SIGNAL(u'doubleClicked(QModelIndex)'), self.onGoLive)
        if isLive:
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'slidecontroller_live_spin_delay'),
                    self.receiveSpinDelay)
        if isLive:
            self.Toolbar.makeWidgetsInvisible(self.loopList)
            self.Toolbar.actions[u'Stop Loop'].setVisible(False)
        else:
            self.Toolbar.makeWidgetsInvisible(self.songEditList)
        self.Mediabar.setVisible(False)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_stop_loop' % self.typePrefix),
            self.onStopLoop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_first' % self.typePrefix),
            self.onSlideSelectedFirst)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_next' % self.typePrefix),
            self.onSlideSelectedNext)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_previous' % self.typePrefix),
            self.onSlideSelectedPrevious)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_next_noloop' % self.typePrefix),
            self.onSlideSelectedNextNoloop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_previous_noloop' %
            self.typePrefix),
            self.onSlideSelectedPreviousNoloop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_last' % self.typePrefix),
            self.onSlideSelectedLast)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_change' % self.typePrefix),
            self.onSlideChange)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_set' % self.typePrefix),
            self.onSlideSelectedIndex)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_blank' % self.typePrefix),
            self.onSlideBlank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_unblank' % self.typePrefix),
            self.onSlideUnblank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_%s_text_request' % self.typePrefix),
            self.onTextRequest)
        QtCore.QObject.connect(self.Splitter,
            QtCore.SIGNAL(u'splitterMoved(int, int)'), self.trackSplitter)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.refreshServiceItem)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_screen_changed'), self.screenSizeChanged)
        if self.isLive:
            QtCore.QObject.connect(self.volumeSlider,
                QtCore.SIGNAL(u'sliderReleased()'), self.mediaVolume)

    def screenSizeChanged(self):
        """
        Settings dialog has changed the screen size of adjust output and
        screen previews
        """
        log.debug(u'screenSizeChanged live = %s' % self.isLive)
        # rebuild display as screen size changed
        self.display = MainDisplay(self, self.screens, self.isLive)
        self.display.imageManager = self.parent.RenderManager.image_manager
        self.display.alertTab = self.alertTab
        self.ratio = float(self.screens.current[u'size'].width()) / \
            float(self.screens.current[u'size'].height())
        self.display.setup()
        self.SlidePreview.setFixedSize(
            QtCore.QSize(self.settingsmanager.slidecontroller_image,
            self.settingsmanager.slidecontroller_image / self.ratio))

    def widthChanged(self):
        """
        Handle changes of width from the splitter between the live and preview
        controller.  Event only issues when changes have finished
        """
        log.debug(u'widthChanged live = %s' % self.isLive)
        width = self.parent.ControlSplitter.sizes()[self.split]
        height = width * self.parent.RenderManager.screen_ratio
        self.PreviewListWidget.setColumnWidth(0, width)
        # Sort out image heights (Songs, bibles excluded)
        if self.serviceItem and not self.serviceItem.is_text():
            for framenumber in range(len(self.serviceItem.get_frames())):
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
            self.PreviewListWidget.selectRow(
                self.PreviewListWidget.rowCount() - 1)
        else:
            if slideno + 1 < self.PreviewListWidget.rowCount():
                self.PreviewListWidget.scrollToItem(
                    self.PreviewListWidget.item(slideno + 1, 0))
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
        self.Toolbar.makeWidgetsInvisible(self.loopList)
        self.Toolbar.actions[u'Stop Loop'].setVisible(False)
        if item.is_text():
            if QtCore.QSettings().value(
                self.parent.songsSettingsSection + u'/show songbar',
                QtCore.QVariant(True)).toBool() and len(self.slideList) > 0:
                self.Toolbar.makeWidgetsVisible([u'Song Menu'])
        if item.is_capable(ItemCapabilities.AllowsLoop) and \
            len(item.get_frames()) > 1:
            self.Toolbar.makeWidgetsVisible(self.loopList)
        if item.is_media():
            self.Toolbar.setVisible(False)
            self.Mediabar.setVisible(True)

    def enablePreviewToolBar(self, item):
        """
        Allows the Preview toolbar to be customised
        """
        self.Toolbar.setVisible(True)
        self.Mediabar.setVisible(False)
        self.Toolbar.makeWidgetsInvisible(self.songEditList)
        if item.is_capable(ItemCapabilities.AllowsEdit) and item.from_plugin:
            self.Toolbar.makeWidgetsVisible(self.songEditList)
        elif item.is_media():
            self.Toolbar.setVisible(False)
            self.Mediabar.setVisible(True)
            self.volumeSlider.setAudioOutput(self.audio)

    def refreshServiceItem(self):
        """
        Method to update the service item if the screen has changed
        """
        log.debug(u'refreshServiceItem live = %s' % self.isLive)
        if self.serviceItem:
            if self.serviceItem.is_text() or self.serviceItem.is_image():
                item = self.serviceItem
                item.render()
                self._processItem(item, self.selectedRow)

    def addServiceItem(self, item):
        """
        Method to install the service item into the controller
        Called by plugins
        """
        log.debug(u'addServiceItem live = %s' % self.isLive)
        item.render()
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
        log.debug(u'addServiceManagerItem live = %s' % self.isLive)
        # If service item is the same as the current on only change slide
        if item.__eq__(self.serviceItem):
            if slideno + 1 < self.PreviewListWidget.rowCount():
                self.PreviewListWidget.scrollToItem(
                    self.PreviewListWidget.item(slideno + 1, 0))
            self.PreviewListWidget.selectRow(slideno)
            self.onSlideSelected()
            return
        self._processItem(item, slideno)

    def _processItem(self, serviceItem, slideno):
        """
        Loads a ServiceItem into the system from ServiceManager
        Display the slide number passed
        """
        log.debug(u'processManagerItem live = %s' % self.isLive)
        self.onStopLoop()
        # If old item was a command tell it to stop
        if self.serviceItem:
            if self.serviceItem.is_command():
                Receiver.send_message(u'%s_stop' %
                    self.serviceItem.name.lower(), [serviceItem, self.isLive])
            if self.serviceItem.is_media():
                self.onMediaClose()
        if self.isLive:
            blanked = self.BlankScreen.isChecked()
        else:
            blanked = False
        Receiver.send_message(u'%s_start' % serviceItem.name.lower(),
            [serviceItem, self.isLive, blanked, slideno])
        self.slideList = {}
        width = self.parent.ControlSplitter.sizes()[self.split]
        # Set pointing cursor when we have somthing to point at
        self.PreviewListWidget.setCursor(QtCore.Qt.PointingHandCursor)
        self.serviceItem = serviceItem
        self.PreviewListWidget.clear()
        self.PreviewListWidget.setRowCount(0)
        self.PreviewListWidget.setColumnWidth(0, width)
        if self.isLive:
            self.SongMenu.menu().clear()
        row = 0
        text = []
        for framenumber, frame in enumerate(self.serviceItem.get_frames()):
            self.PreviewListWidget.setRowCount(
                self.PreviewListWidget.rowCount() + 1)
            item = QtGui.QTableWidgetItem()
            slideHeight = 0
            if self.serviceItem.is_text():
                if frame[u'verseTag']:
                    bits = frame[u'verseTag'].split(u':')
                    tag = u'%s\n%s' % (bits[0][0], bits[1][0:] )
                    tag1 = u'%s%s' % (bits[0][0], bits[1][0:] )
                    row = tag
                    if self.isLive:
                        if tag1 not in self.slideList:
                            self.slideList[tag1] = framenumber
                            self.SongMenu.menu().addAction(tag1,
                                self.onSongBarHandler)
                else:
                    row += 1
                item.setText(frame[u'text'])
            else:
                label = QtGui.QLabel()
                label.setMargin(4)
                label.setScaledContents(True)
                if self.serviceItem.is_command():
                    image = resize_image(frame[u'image'],
                        self.parent.RenderManager.width,
                        self.parent.RenderManager.height)
                else:
                    image = self.parent.RenderManager.image_manager. \
                            get_image(frame[u'title'])
                label.setPixmap(QtGui.QPixmap.fromImage(image))
                self.PreviewListWidget.setCellWidget(framenumber, 0, label)
                slideHeight = width * self.parent.RenderManager.screen_ratio
                row += 1
            text.append(unicode(row))
            self.PreviewListWidget.setItem(framenumber, 0, item)
            if slideHeight != 0:
                self.PreviewListWidget.setRowHeight(framenumber, slideHeight)
        self.PreviewListWidget.setVerticalHeaderLabels(text)
        if self.serviceItem.is_text():
            self.PreviewListWidget.resizeRowsToContents()
        self.PreviewListWidget.setColumnWidth(0,
            self.PreviewListWidget.viewport().size().width())
        if slideno > self.PreviewListWidget.rowCount():
            self.PreviewListWidget.selectRow(
                self.PreviewListWidget.rowCount() - 1)
        else:
            if slideno + 1 < self.PreviewListWidget.rowCount():
                self.PreviewListWidget.scrollToItem(
                    self.PreviewListWidget.item(slideno + 1, 0))
            self.PreviewListWidget.selectRow(slideno)
        self.enableToolBar(serviceItem)
        # Pass to display for viewing
        self.display.buildHtml(self.serviceItem)
        if serviceItem.is_media():
            self.onMediaStart(serviceItem)
        self.onSlideSelected()
        self.PreviewListWidget.setFocus()
        Receiver.send_message(u'slidecontroller_%s_started' % self.typePrefix,
            [serviceItem])

    def onTextRequest(self):
        """
        Return the text for the current item in controller
        """
        data = []
        if self.serviceItem:
            for framenumber, frame in enumerate(self.serviceItem.get_frames()):
                dataItem = {}
                if self.serviceItem.is_text():
                    dataItem[u'tag'] = unicode(frame[u'verseTag'])
                    dataItem[u'text'] = unicode(frame[u'html'])
                else:
                    dataItem[u'tag'] = unicode(framenumber)
                    dataItem[u'text'] = u''
                dataItem[u'selected'] = \
                    (self.PreviewListWidget.currentRow() == framenumber)
                data.append(dataItem)
        Receiver.send_message(u'slidecontroller_%s_text_response'
            % self.typePrefix, data)

    # Screen event methods
    def onSlideSelectedFirst(self):
        """
        Go to the first slide.
        """
        if not self.serviceItem:
            return
        if self.serviceItem.is_command():
            Receiver.send_message(u'%s_first' % self.serviceItem.name.lower(),
                [self.serviceItem, self.isLive])
            self.updatePreview()
        else:
            self.PreviewListWidget.selectRow(0)
            self.onSlideSelected()

    def onSlideSelectedIndex(self, message):
        """
        Go to the requested slide
        """
        index = int(message[0])
        if not self.serviceItem:
            return
        if self.serviceItem.is_command():
            Receiver.send_message(u'%s_slide' % self.serviceItem.name.lower(),
                [self.serviceItem, self.isLive, index])
            self.updatePreview()
        else:
            if index + 1 < self.PreviewListWidget.rowCount():
                self.PreviewListWidget.scrollToItem(
                    self.PreviewListWidget.item(index + 1, 0))
            self.PreviewListWidget.selectRow(index)
            self.onSlideSelected()

    def mainDisplaySetBackground(self):
        """
        Allow the main display to blank the main display at startup time
        """
        log.debug(u'mainDisplaySetBackground live = %s' % self.isLive)
        if not self.display.primary:
            self.onHideDisplay(True)

    def onSlideBlank(self):
        """
        Handle the slidecontroller blank event
        """
        self.onBlankDisplay(True)

    def onSlideUnblank(self):
        """
        Handle the slidecontroller unblank event
        """
        self.onBlankDisplay(False)

    def onBlankDisplay(self, checked):
        """
        Handle the blank screen button actions
        """
        log.debug(u'onBlankDisplay %s' % checked)
        self.HideMenu.setDefaultAction(self.BlankScreen)
        self.BlankScreen.setChecked(checked)
        self.ThemeScreen.setChecked(False)
        if self.screens.display_count > 1:
            self.DesktopScreen.setChecked(False)
        QtCore.QSettings().setValue(
            self.parent.generalSettingsSection + u'/screen blank',
            QtCore.QVariant(checked))
        if checked:
            Receiver.send_message(u'maindisplay_hide', HideMode.Blank)
        else:
            Receiver.send_message(u'maindisplay_show')
        self.blankPlugin(checked)

    def onThemeDisplay(self, checked):
        """
        Handle the Theme screen button
        """
        log.debug(u'onThemeDisplay %s' % checked)
        self.HideMenu.setDefaultAction(self.ThemeScreen)
        self.BlankScreen.setChecked(False)
        self.ThemeScreen.setChecked(checked)
        if self.screens.display_count > 1:
            self.DesktopScreen.setChecked(False)
        if checked:
            Receiver.send_message(u'maindisplay_hide', HideMode.Theme)
        else:
            Receiver.send_message(u'maindisplay_show')
        self.blankPlugin(checked)

    def onHideDisplay(self, checked):
        """
        Handle the Hide screen button
        """
        log.debug(u'onHideDisplay %s' % checked)
        self.HideMenu.setDefaultAction(self.DesktopScreen)
        self.BlankScreen.setChecked(False)
        self.ThemeScreen.setChecked(False)
        if self.screens.display_count > 1:
            self.DesktopScreen.setChecked(checked)
        if checked:
            Receiver.send_message(u'maindisplay_hide', HideMode.Screen)
        else:
            Receiver.send_message(u'maindisplay_show')
        self.hidePlugin(checked)

    def blankPlugin(self, blank):
        """
        Blank the display screen within a plugin if required.
        """
        log.debug(u'blankPlugin %s ', blank)
        if self.serviceItem is not None:
            if blank:
                Receiver.send_message(u'%s_blank'
                    % self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive])
            else:
                Receiver.send_message(u'%s_unblank'
                    % self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive])

    def hidePlugin(self, hide):
        """
        Tell the plugin to hide the display screen.
        """
        log.debug(u'hidePlugin %s ', hide)
        if self.serviceItem is not None:
            if hide:
                Receiver.send_message(u'%s_hide'
                    % self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive])
            else:
                Receiver.send_message(u'%s_unblank'
                    % self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive])

    def onSlideSelected(self):
        """
        Generate the preview when you click on a slide.
        if this is the Live Controller also display on the screen
        """
        row = self.PreviewListWidget.currentRow()
        self.selectedRow = 0
        if row > -1 and row < self.PreviewListWidget.rowCount():
            if self.serviceItem.is_command():
                if self.isLive:
                    Receiver.send_message(
                        u'%s_slide' % self.serviceItem.name.lower(),
                        [self.serviceItem, self.isLive, row])
                self.updatePreview()
            else:
                toDisplay = self.serviceItem.get_rendered_frame(row)
                if self.serviceItem.is_text():
                    frame = self.display.text(toDisplay)
                else:
                    frame = self.display.image(toDisplay)
                self.SlidePreview.setPixmap(QtGui.QPixmap.fromImage(frame))
            self.selectedRow = row
        Receiver.send_message(u'slidecontroller_%s_changed' % self.typePrefix,
            row)

    def onSlideChange(self, row):
        """
        The slide has been changed. Update the slidecontroller accordingly
        """
        if row + 1 < self.PreviewListWidget.rowCount():
            self.PreviewListWidget.scrollToItem(
                self.PreviewListWidget.item(row + 1, 0))
        self.PreviewListWidget.selectRow(row)
        self.updatePreview()
        Receiver.send_message(u'slidecontroller_%s_changed' % self.typePrefix,
            row)

    def updatePreview(self):
        if not self.screens.current[u'primary']:
            # Grab now, but try again in a couple of seconds if slide change
            # is slow
            QtCore.QTimer.singleShot(0.5, self.grabMainDisplay)
            QtCore.QTimer.singleShot(2.5, self.grabMainDisplay)
        else:
            label = self.PreviewListWidget.cellWidget(
                self.PreviewListWidget.currentRow(), 1)
            if label:
                self.SlidePreview.setPixmap(label.pixmap())

    def grabMainDisplay(self):
        winid = QtGui.QApplication.desktop().winId()
        rect = self.screens.current[u'size']
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
        Receiver.send_message(u'%s_next' % self.serviceItem.name.lower(),
            [self.serviceItem, self.isLive])
        if self.serviceItem.is_command() and self.isLive:
            self.updatePreview()
        else:
            row = self.PreviewListWidget.currentRow() + 1
            if row == self.PreviewListWidget.rowCount():
                if loop:
                    row = 0
                else:
                    Receiver.send_message('servicemanager_next_item')
                    return
            if row + 1 < self.PreviewListWidget.rowCount():
                self.PreviewListWidget.scrollToItem(
                    self.PreviewListWidget.item(row + 1, 0))
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
        Receiver.send_message(u'%s_previous' % self.serviceItem.name.lower(),
            [self.serviceItem, self.isLive])
        if self.serviceItem.is_command() and self.isLive:
            self.updatePreview()
        else:
            row = self.PreviewListWidget.currentRow() - 1
            if row == -1:
                if loop:
                    row = self.PreviewListWidget.rowCount() - 1
                else:
                    row = 0
            if row + 1 < self.PreviewListWidget.rowCount():
                self.PreviewListWidget.scrollToItem(
                    self.PreviewListWidget.item(row + 1, 0))
            self.PreviewListWidget.selectRow(row)
            self.onSlideSelected()

    def onSlideSelectedLast(self):
        """
        Go to the last slide.
        """
        if not self.serviceItem:
            return
        Receiver.send_message(u'%s_last' % self.serviceItem.name.lower(),
            [self.serviceItem, self.isLive])
        if self.serviceItem.is_command():
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
            self.Toolbar.actions[u'Stop Loop'].setVisible(True)
            self.Toolbar.actions[u'Start Loop'].setVisible(False)

    def onStopLoop(self):
        """
        Stop the timer loop running
        """
        if self.timer_id != 0:
            self.killTimer(self.timer_id)
            self.timer_id = 0
            self.Toolbar.actions[u'Start Loop'].setVisible(True)
            self.Toolbar.actions[u'Stop Loop'].setVisible(False)

    def timerEvent(self, event):
        """
        If the timer event is for this window select next slide
        """
        if event.timerId() == self.timer_id:
            self.onSlideSelectedNext()

    def onEditSong(self):
        """
        From the preview display requires the service Item to be editied
        """
        self.songEdit = True
        Receiver.send_message(u'%s_edit' % self.serviceItem.name.lower(),
            u'P:%s' % self.serviceItem.editId)

    def onGoLive(self):
        """
        If preview copy slide item to live
        """
        row = self.PreviewListWidget.currentRow()
        if row > -1 and row < self.PreviewListWidget.rowCount():
            self.parent.LiveController.addServiceManagerItem(
                self.serviceItem, row)

    def onMediaStart(self, item):
        """
        Respond to the arrival of a media service item
        """
        log.debug(u'SlideController onMediaStart')
        file = os.path.join(item.get_frame_path(), item.get_frame_title())
        if self.isLive:
            self.display.video(file, self.volume)
            self.volumeSlider.setValue(self.volume)
        else:
            self.mediaObject.stop()
            self.mediaObject.clearQueue()
            self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
            self.seekSlider.setMediaObject(self.mediaObject)
            self.seekSlider.show()
            self.onMediaPlay()

    def mediaVolume(self):
        """
        Respond to the release of Volume Slider
        """
        log.debug(u'SlideController mediaVolume')
        self.volume = self.volumeSlider.value()
        self.display.videoVolume(self.volume)

    def onMediaPause(self):
        """
        Respond to the Pause from the media Toolbar
        """
        log.debug(u'SlideController onMediaPause')
        if self.isLive:
            self.display.videoPause()
        else:
            self.mediaObject.pause()

    def onMediaPlay(self):
        """
        Respond to the Play from the media Toolbar
        """
        log.debug(u'SlideController onMediaPlay')
        if self.isLive:
            self.display.videoPlay()
        else:
            self.SlidePreview.hide()
            self.video.show()
            self.mediaObject.play()

    def onMediaStop(self):
        """
        Respond to the Stop from the media Toolbar
        """
        log.debug(u'SlideController onMediaStop')
        if self.isLive:
            self.display.videoStop()
        else:
            self.mediaObject.stop()
            self.video.hide()
        self.SlidePreview.clear()
        self.SlidePreview.show()

    def onMediaClose(self):
        """
        Respond to a request to close the Video
        """
        log.debug(u'SlideController onMediaStop')
        if self.isLive:
            self.display.resetVideo()
        else:
            self.mediaObject.stop()
            self.mediaObject.clearQueue()
            self.video.hide()
        self.SlidePreview.clear()
        self.SlidePreview.show()
