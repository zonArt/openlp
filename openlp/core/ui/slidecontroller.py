# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
import time
import copy

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import OpenLPToolbar, Receiver, resize_image, \
    ItemCapabilities, translate
from openlp.core.lib.ui import UiStrings, shortcut_action
from openlp.core.ui import HideMode, MainDisplay, ScreenList
from openlp.core.utils.actions import ActionList, CategoryOrder

log = logging.getLogger(__name__)

class SlideList(QtGui.QTableWidget):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    def __init__(self, parent=None, name=None):
        QtGui.QTableWidget.__init__(self, parent.controller)


class SlideController(QtGui.QWidget):
    """
    SlideController is the slide controller widget. This widget is what the
    user uses to control the displaying of verses/slides/etc on the screen.
    """
    def __init__(self, parent, isLive=False):
        """
        Set up the Slide Controller.
        """
        QtGui.QWidget.__init__(self, parent)
        self.isLive = isLive
        self.display = None
        self.screens = ScreenList.get_instance()
        self.ratio = float(self.screens.current[u'size'].width()) / \
            float(self.screens.current[u'size'].height())
        self.imageManager = self.parent().imageManager
        self.loopList = [
            u'Play Slides Menu',
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
        self.panel = QtGui.QWidget(parent.controlSplitter)
        self.slideList = {}
        # Layout for holding panel
        self.panelLayout = QtGui.QVBoxLayout(self.panel)
        self.panelLayout.setSpacing(0)
        self.panelLayout.setMargin(0)
        # Type label for the top of the slide controller
        self.typeLabel = QtGui.QLabel(self.panel)
        if self.isLive:
            self.typeLabel.setText(UiStrings().Live)
            self.split = 1
            self.typePrefix = u'live'
        else:
            self.typeLabel.setText(UiStrings().Preview)
            self.split = 0
            self.typePrefix = u'preview'
        self.typeLabel.setStyleSheet(u'font-weight: bold; font-size: 12pt;')
        self.typeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.panelLayout.addWidget(self.typeLabel)
        # Splitter
        self.splitter = QtGui.QSplitter(self.panel)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.panelLayout.addWidget(self.splitter)
        # Actual controller section
        self.controller = QtGui.QWidget(self.splitter)
        self.controller.setGeometry(QtCore.QRect(0, 0, 100, 536))
        self.controller.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
            QtGui.QSizePolicy.Maximum))
        self.controllerLayout = QtGui.QVBoxLayout(self.controller)
        self.controllerLayout.setSpacing(0)
        self.controllerLayout.setMargin(0)
        # Controller list view
        self.previewListWidget = SlideList(self)
        self.previewListWidget.setColumnCount(1)
        self.previewListWidget.horizontalHeader().setVisible(False)
        self.previewListWidget.setColumnWidth(0, self.controller.width())
        self.previewListWidget.isLive = self.isLive
        self.previewListWidget.setObjectName(u'PreviewListWidget')
        self.previewListWidget.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.previewListWidget.setSelectionMode(
            QtGui.QAbstractItemView.SingleSelection)
        self.previewListWidget.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.previewListWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.previewListWidget.setAlternatingRowColors(True)
        self.controllerLayout.addWidget(self.previewListWidget)
        # Build the full toolbar
        self.toolbar = OpenLPToolbar(self)
        sizeToolbarPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizeToolbarPolicy.setHorizontalStretch(0)
        sizeToolbarPolicy.setVerticalStretch(0)
        sizeToolbarPolicy.setHeightForWidth(
            self.toolbar.sizePolicy().hasHeightForWidth())
        self.toolbar.setSizePolicy(sizeToolbarPolicy)
        self.previousItem = self.toolbar.addToolbarButton(
            translate('OpenLP.SlideController', 'Previous Slide'),
            u':/slides/slide_previous.png',
            translate('OpenLP.SlideController', 'Move to previous.'),
            self.onSlideSelectedPrevious,
            shortcuts=[QtCore.Qt.Key_Up, QtCore.Qt.Key_PageUp],
            context=QtCore.Qt.WidgetWithChildrenShortcut)
        self.nextItem = self.toolbar.addToolbarButton(
            translate('OpenLP.SlideController', 'Next Slide'),
            u':/slides/slide_next.png',
            translate('OpenLP.SlideController', 'Move to next.'),
            self.onSlideSelectedNext,
            shortcuts=[QtCore.Qt.Key_Down, QtCore.Qt.Key_PageDown],
            context=QtCore.Qt.WidgetWithChildrenShortcut)
        self.toolbar.addToolbarSeparator(u'Close Separator')
        if self.isLive:
            # Hide Menu
            self.hideMenu = QtGui.QToolButton(self.toolbar)
            self.hideMenu.setText(translate('OpenLP.SlideController', 'Hide'))
            self.hideMenu.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
            self.toolbar.addToolbarWidget(u'Hide Menu', self.hideMenu)
            self.hideMenu.setMenu(QtGui.QMenu(
                translate('OpenLP.SlideController', 'Hide'), self.toolbar))
            self.blankScreen = shortcut_action(self.hideMenu, u'blankScreen',
                [QtCore.Qt.Key_Period], self.onBlankDisplay,
                u':/slides/slide_blank.png', False, UiStrings().LiveToolbar)
            self.blankScreen.setText(
                translate('OpenLP.SlideController', 'Blank Screen'))
            self.themeScreen = shortcut_action(self.hideMenu, u'themeScreen',
                [QtGui.QKeySequence(u'T')], self.onThemeDisplay,
                u':/slides/slide_theme.png', False, UiStrings().LiveToolbar)
            self.themeScreen.setText(
                translate('OpenLP.SlideController', 'Blank to Theme'))
            self.desktopScreen = shortcut_action(self.hideMenu,
                u'desktopScreen', [QtGui.QKeySequence(u'D')],
                self.onHideDisplay, u':/slides/slide_desktop.png', False,
                UiStrings().LiveToolbar)
            self.desktopScreen.setText(
                translate('OpenLP.SlideController', 'Show Desktop'))
            self.hideMenu.setDefaultAction(self.blankScreen)
            self.hideMenu.menu().addAction(self.blankScreen)
            self.hideMenu.menu().addAction(self.themeScreen)
            self.hideMenu.menu().addAction(self.desktopScreen)
            self.toolbar.addToolbarSeparator(u'Loop Separator')
            # Play Slides Menu
            self.playSlidesMenu = QtGui.QToolButton(self.toolbar)
            self.playSlidesMenu.setText(translate('OpenLP.SlideController',
                'Play Slides'))
            self.playSlidesMenu.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
            self.toolbar.addToolbarWidget(u'Play Slides Menu',
                self.playSlidesMenu)
            self.playSlidesMenu.setMenu(QtGui.QMenu(
                translate('OpenLP.SlideController', 'Play Slides'),
                self.toolbar))
            self.playSlidesLoop = shortcut_action(self.playSlidesMenu,
                u'playSlidesLoop', [], self.onPlaySlidesLoop,
                u':/media/media_time.png', False, UiStrings().LiveToolbar)
            self.playSlidesLoop.setText(
                translate('OpenLP.SlideController', 'Play Slides in Loop'))
            self.playSlidesOnce = shortcut_action(self.playSlidesMenu,
                u'playSlidesOnce', [], self.onPlaySlidesOnce,
                u':/media/media_time.png', False, UiStrings().LiveToolbar)
            self.playSlidesOnce.setText(
                translate('OpenLP.SlideController', 'Play Slides to End'))
            if QtCore.QSettings().value(self.parent().generalSettingsSection +
                u'/enable slide loop', QtCore.QVariant(True)).toBool():
                self.playSlidesMenu.setDefaultAction(self.playSlidesLoop)
            else:
                self.playSlidesMenu.setDefaultAction(self.playSlidesOnce)
            self.playSlidesMenu.menu().addAction(self.playSlidesLoop)
            self.playSlidesMenu.menu().addAction(self.playSlidesOnce)
            # Loop Delay Spinbox
            self.delaySpinBox = QtGui.QSpinBox()
            self.delaySpinBox.setRange(1, 180)
            self.toolbar.addToolbarWidget(u'Image SpinBox', self.delaySpinBox)
            self.delaySpinBox.setSuffix(UiStrings().Seconds)
            self.delaySpinBox.setToolTip(translate('OpenLP.SlideController',
                'Delay between slides in seconds.'))
        else:
            self.toolbar.addToolbarButton(
                # Does not need translating - control string.
                u'Go Live', u':/general/general_live.png',
                translate('OpenLP.SlideController', 'Move to live.'),
                self.onGoLive)
            self.toolbar.addToolbarButton(
                # Does not need translating - control string.
                u'Add to Service', u':/general/general_add.png',
                translate('OpenLP.SlideController', 'Add to Service.'),
                self.onPreviewAddToService)
            self.toolbar.addToolbarSeparator(u'Close Separator')
            self.toolbar.addToolbarButton(
                # Does not need translating - control string.
                u'Edit Song', u':/general/general_edit.png',
                translate('OpenLP.SlideController',
                'Edit and reload song preview.'),
                self.onEditSong)
        self.controllerLayout.addWidget(self.toolbar)
        # Build a Media ToolBar
        self.mediabar = OpenLPToolbar(self)
        self.mediabar.addToolbarButton(
            u'Media Start', u':/slides/media_playback_start.png',
            translate('OpenLP.SlideController', 'Start playing media.'),
            self.onMediaPlay)
        self.mediabar.addToolbarButton(
            u'Media Pause', u':/slides/media_playback_pause.png',
            translate('OpenLP.SlideController', 'Start playing media.'),
            self.onMediaPause)
        self.mediabar.addToolbarButton(
            u'Media Stop', u':/slides/media_playback_stop.png',
            translate('OpenLP.SlideController', 'Start playing media.'),
            self.onMediaStop)
        if self.isLive:
            # Build the Song Toolbar
            self.songMenu = QtGui.QToolButton(self.toolbar)
            self.songMenu.setText(translate('OpenLP.SlideController', 'Go To'))
            self.songMenu.setPopupMode(QtGui.QToolButton.InstantPopup)
            self.toolbar.addToolbarWidget(u'Song Menu', self.songMenu)
            self.songMenu.setMenu(QtGui.QMenu(
                translate('OpenLP.SlideController', 'Go To'), self.toolbar))
            self.toolbar.makeWidgetsInvisible([u'Song Menu'])
            # Build the volumeSlider.
            self.volumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
            self.volumeSlider.setTickInterval(1)
            self.volumeSlider.setTickPosition(QtGui.QSlider.TicksAbove)
            self.volumeSlider.setMinimum(0)
            self.volumeSlider.setMaximum(10)
        else:
            # Build the seekSlider.
            self.seekSlider = Phonon.SeekSlider()
            self.seekSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
            self.seekSlider.setObjectName(u'seekSlider')
            self.mediabar.addToolbarWidget(u'Seek Slider', self.seekSlider)
            self.volumeSlider = Phonon.VolumeSlider()
        self.volumeSlider.setGeometry(QtCore.QRect(90, 260, 221, 24))
        self.volumeSlider.setObjectName(u'volumeSlider')
        self.mediabar.addToolbarWidget(u'Audio Volume', self.volumeSlider)
        self.controllerLayout.addWidget(self.mediabar)
        # Screen preview area
        self.previewFrame = QtGui.QFrame(self.splitter)
        self.previewFrame.setGeometry(QtCore.QRect(0, 0, 300, 300 * self.ratio))
        self.previewFrame.setMinimumHeight(100)
        self.previewFrame.setSizePolicy(QtGui.QSizePolicy(
            QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored,
            QtGui.QSizePolicy.Label))
        self.previewFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.previewFrame.setFrameShadow(QtGui.QFrame.Sunken)
        self.previewFrame.setObjectName(u'PreviewFrame')
        self.grid = QtGui.QGridLayout(self.previewFrame)
        self.grid.setMargin(8)
        self.grid.setObjectName(u'grid')
        self.slideLayout = QtGui.QVBoxLayout()
        self.slideLayout.setSpacing(0)
        self.slideLayout.setMargin(0)
        self.slideLayout.setObjectName(u'SlideLayout')
        if not self.isLive:
            self.mediaObject = Phonon.MediaObject(self)
            self.video = Phonon.VideoWidget()
            self.video.setVisible(False)
            self.audio = Phonon.AudioOutput(Phonon.VideoCategory,
                self.mediaObject)
            Phonon.createPath(self.mediaObject, self.video)
            Phonon.createPath(self.mediaObject, self.audio)
            self.video.setGeometry(QtCore.QRect(0, 0, 300, 225))
            self.slideLayout.insertWidget(0, self.video)
        # Actual preview screen
        self.slidePreview = QtGui.QLabel(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.slidePreview.sizePolicy().hasHeightForWidth())
        self.slidePreview.setSizePolicy(sizePolicy)
        self.slidePreview.setFrameShape(QtGui.QFrame.Box)
        self.slidePreview.setFrameShadow(QtGui.QFrame.Plain)
        self.slidePreview.setLineWidth(1)
        self.slidePreview.setScaledContents(True)
        self.slidePreview.setObjectName(u'SlidePreview')
        self.slideLayout.insertWidget(0, self.slidePreview)
        self.grid.addLayout(self.slideLayout, 0, 0, 1, 1)
        # Signals
        QtCore.QObject.connect(self.previewListWidget,
            QtCore.SIGNAL(u'clicked(QModelIndex)'), self.onSlideSelected)
        if self.isLive:
            QtCore.QObject.connect(self.volumeSlider,
                QtCore.SIGNAL(u'sliderReleased()'), self.mediaVolume)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'maindisplay_active'), self.updatePreview)
            QtCore.QObject.connect(Receiver.get_receiver(),
                QtCore.SIGNAL(u'slidecontroller_live_spin_delay'),
                self.receiveSpinDelay)
            self.toolbar.makeWidgetsInvisible(self.loopList)
        else:
            QtCore.QObject.connect(self.previewListWidget,
                QtCore.SIGNAL(u'doubleClicked(QModelIndex)'),
                self.onGoLiveClick)
            self.toolbar.makeWidgetsInvisible(self.songEditList)
        self.mediabar.setVisible(False)
        if self.isLive:
            self.setLiveHotkeys(self)
            self.__addActionsToWidget(self.previewListWidget)
        else:
            self.setPreviewHotkeys()
            self.previewListWidget.addActions(
                [self.nextItem,
                self.previousItem])
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

    def setPreviewHotkeys(self, parent=None):
        self.previousItem.setObjectName(u'previousItemPreview')
        self.nextItem.setObjectName(u'nextItemPreview')
        action_list = ActionList.get_instance()
        action_list.add_action(self.previousItem)
        action_list.add_action(self.nextItem)

    def setLiveHotkeys(self, parent=None):
        self.previousItem.setObjectName(u'previousItemLive')
        self.nextItem.setObjectName(u'nextItemLive')
        action_list = ActionList.get_instance()
        action_list.add_category(
            UiStrings().LiveToolbar, CategoryOrder.standardToolbar)
        action_list.add_action(self.previousItem)
        action_list.add_action(self.nextItem)
        self.previousService = shortcut_action(parent, u'previousService',
            [QtCore.Qt.Key_Left], self.servicePrevious,
            category=UiStrings().LiveToolbar,
            context=QtCore.Qt.WidgetWithChildrenShortcut)
        self.previousService.setText(
            translate('OpenLP.SlideController', 'Previous Service'))
        self.nextService = shortcut_action(parent, 'nextService',
            [QtCore.Qt.Key_Right], self.serviceNext,
            category=UiStrings().LiveToolbar,
            context=QtCore.Qt.WidgetWithChildrenShortcut)
        self.nextService.setText(
            translate('OpenLP.SlideController', 'Next Service'))
        self.escapeItem = shortcut_action(parent, 'escapeItem',
            [QtCore.Qt.Key_Escape], self.liveEscape,
            category=UiStrings().LiveToolbar,
            context=QtCore.Qt.WidgetWithChildrenShortcut)
        self.escapeItem.setText(
            translate('OpenLP.SlideController', 'Escape Item'))

    def liveEscape(self):
        self.display.setVisible(False)
        self.display.videoStop()

    def servicePrevious(self):
        time.sleep(0.1)
        Receiver.send_message('servicemanager_previous_item')

    def serviceNext(self):
        time.sleep(0.1)
        Receiver.send_message('servicemanager_next_item')

    def screenSizeChanged(self):
        """
        Settings dialog has changed the screen size of adjust output and
        screen previews.
        """
        # rebuild display as screen size changed
        if self.display:
            self.display.close()
        self.display = MainDisplay(self, self.imageManager, self.isLive)
        self.display.alertTab = self.alertTab
        self.display.setup()
        if self.isLive:
            self.__addActionsToWidget(self.display)
        # The SlidePreview's ratio.
        self.ratio = float(self.screens.current[u'size'].width()) / \
            float(self.screens.current[u'size'].height())
        self.previewSizeChanged()
        if self.serviceItem:
            self.refreshServiceItem()

    def __addActionsToWidget(self, widget):
        widget.addActions([
            self.previousItem, self.nextItem,
            self.previousService, self.nextService,
            self.escapeItem])

    def previewSizeChanged(self):
        """
        Takes care of the SlidePreview's size. Is called when one of the the
        splitters is moved or when the screen size is changed. Note, that this
        method is (also) called frequently from the mainwindow *paintEvent*.
        """
        if self.ratio < float(self.previewFrame.width()) / float(
            self.previewFrame.height()):
            # We have to take the height as limit.
            max_height = self.previewFrame.height() - self.grid.margin() * 2
            self.slidePreview.setFixedSize(QtCore.QSize(max_height * self.ratio,
                max_height))
        else:
            # We have to take the width as limit.
            max_width = self.previewFrame.width() - self.grid.margin() * 2
            self.slidePreview.setFixedSize(QtCore.QSize(max_width,
                max_width / self.ratio))
        # Make sure that the frames have the correct size.
        self.previewListWidget.setColumnWidth(0,
            self.previewListWidget.viewport().size().width())
        if self.serviceItem:
            # Sort out songs, bibles, etc.
            if self.serviceItem.is_text():
                self.previewListWidget.resizeRowsToContents()
            else:
                # Sort out image heights.
                width = self.parent().controlSplitter.sizes()[self.split]
                for framenumber in range(len(self.serviceItem.get_frames())):
                    self.previewListWidget.setRowHeight(
                        framenumber, width / self.ratio)

    def onSongBarHandler(self):
        request = unicode(self.sender().text())
        slideno = self.slideList[request]
        self.__updatePreviewSelection(slideno)
        self.slideSelected()

    def receiveSpinDelay(self, value):
        """
        Adjusts the value of the ``delaySpinBox`` to the given one.
        """
        self.delaySpinBox.setValue(int(value))

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
        # Work-around for OS X, hide and then show the toolbar
        # See bug #791050
        self.toolbar.hide()
        self.mediabar.setVisible(False)
        self.toolbar.makeWidgetsInvisible([u'Song Menu'])
        self.toolbar.makeWidgetsInvisible(self.loopList)
        if item.is_text():
            if QtCore.QSettings().value(
                self.parent().songsSettingsSection + u'/display songbar',
                QtCore.QVariant(True)).toBool() and len(self.slideList) > 0:
                self.toolbar.makeWidgetsVisible([u'Song Menu'])
        if item.is_capable(ItemCapabilities.AllowsLoop) and \
            len(item.get_frames()) > 1:
            self.toolbar.makeWidgetsVisible(self.loopList)
        if item.is_media():
            self.toolbar.setVisible(False)
            self.mediabar.setVisible(True)
        else:
            # Work-around for OS X, hide and then show the toolbar
            # See bug #791050
            self.toolbar.show()

    def enablePreviewToolBar(self, item):
        """
        Allows the Preview toolbar to be customised
        """
        # Work-around for OS X, hide and then show the toolbar
        # See bug #791050
        self.toolbar.hide()
        self.mediabar.setVisible(False)
        self.toolbar.makeWidgetsInvisible(self.songEditList)
        if item.is_capable(ItemCapabilities.AllowsEdit) and item.from_plugin:
            self.toolbar.makeWidgetsVisible(self.songEditList)
        elif item.is_media():
            self.toolbar.setVisible(False)
            self.mediabar.setVisible(True)
            self.volumeSlider.setAudioOutput(self.audio)
        if not item.is_media():
            # Work-around for OS X, hide and then show the toolbar
            # See bug #791050
            self.toolbar.show()

    def refreshServiceItem(self):
        """
        Method to update the service item if the screen has changed
        """
        log.debug(u'refreshServiceItem live = %s' % self.isLive)
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
            self._processItem(item, self.previewListWidget.currentRow())

    def addServiceManagerItem(self, item, slideno):
        """
        Method to install the service item into the controller and
        request the correct toolbar for the plugin.
        Called by ServiceManager
        """
        log.debug(u'addServiceManagerItem live = %s' % self.isLive)
        # If no valid slide number is specified we take the first one.
        if slideno == -1:
            slideno = 0
        # If service item is the same as the current on only change slide
        if item.__eq__(self.serviceItem):
            self.__checkUpdateSelectedSlide(slideno)
            self.slideSelected()
            return
        self._processItem(item, slideno)

    def _processItem(self, serviceItem, slideno):
        """
        Loads a ServiceItem into the system from ServiceManager
        Display the slide number passed
        """
        log.debug(u'processManagerItem live = %s' % self.isLive)
        self.onStopLoop()
        old_item = self.serviceItem
        # take a copy not a link to the servicemeanager copy.
        self.serviceItem = copy.copy(serviceItem)
        if old_item and self.isLive and old_item.is_capable(
            ItemCapabilities.ProvidesOwnDisplay):
            self._resetBlank()
        Receiver.send_message(u'%s_start' % serviceItem.name.lower(),
            [serviceItem, self.isLive, self.hideMode(), slideno])
        self.slideList = {}
        width = self.parent().controlSplitter.sizes()[self.split]
        self.previewListWidget.clear()
        self.previewListWidget.setRowCount(0)
        self.previewListWidget.setColumnWidth(0, width)
        if self.isLive:
            self.songMenu.menu().clear()
        row = 0
        text = []
        for framenumber, frame in enumerate(self.serviceItem.get_frames()):
            self.previewListWidget.setRowCount(
                self.previewListWidget.rowCount() + 1)
            item = QtGui.QTableWidgetItem()
            slideHeight = 0
            if self.serviceItem.is_text():
                if frame[u'verseTag']:
                    # These tags are already translated.
                    verse_def = frame[u'verseTag']
                    verse_def = u'%s%s' % (verse_def[0], verse_def[1:])
                    two_line_def = u'%s\n%s' % (verse_def[0], verse_def[1:])
                    row = two_line_def
                    if self.isLive:
                        if verse_def not in self.slideList:
                            self.slideList[verse_def] = framenumber
                            self.songMenu.menu().addAction(verse_def,
                                self.onSongBarHandler)
                else:
                    row += 1
                item.setText(frame[u'text'])
            else:
                label = QtGui.QLabel()
                label.setMargin(4)
                label.setScaledContents(True)
                if self.serviceItem.is_command():
                    image = QtGui.QImage(frame[u'image'])
                else:
                    # If current slide set background to image
                    if framenumber == slideno:
                        self.serviceItem.bg_image_bytes = \
                            self.imageManager.get_image_bytes(frame[u'title'])
                    image = self.imageManager.get_image(frame[u'title'])
                label.setPixmap(QtGui.QPixmap.fromImage(image))
                self.previewListWidget.setCellWidget(framenumber, 0, label)
                slideHeight = width * self.parent().renderer.screen_ratio
                row += 1
            text.append(unicode(row))
            self.previewListWidget.setItem(framenumber, 0, item)
            if slideHeight != 0:
                self.previewListWidget.setRowHeight(framenumber, slideHeight)
        self.previewListWidget.setVerticalHeaderLabels(text)
        if self.serviceItem.is_text():
            self.previewListWidget.resizeRowsToContents()
        self.previewListWidget.setColumnWidth(0,
            self.previewListWidget.viewport().size().width())
        self.__updatePreviewSelection(slideno)
        self.enableToolBar(serviceItem)
        # Pass to display for viewing.
        # Postpone image build, we need to do this later to avoid the theme
        # flashing on the screen
        if not self.serviceItem.is_image():
            self.display.buildHtml(self.serviceItem)
        if serviceItem.is_media():
            self.onMediaStart(serviceItem)
        self.slideSelected(True)
        self.previewListWidget.setFocus()
        if old_item:
            # Close the old item after the new one is opened
            # This avoids the service theme/desktop flashing on screen
            # However opening a new item of the same type will automatically
            # close the previous, so make sure we don't close the new one.
            if old_item.is_command() and not serviceItem.is_command():
                Receiver.send_message(u'%s_stop' %
                    old_item.name.lower(), [old_item, self.isLive])
            if old_item.is_media() and not serviceItem.is_media():
                self.onMediaClose()
        Receiver.send_message(u'slidecontroller_%s_started' % self.typePrefix,
            [serviceItem])

    def __updatePreviewSelection(self, slideno):
        """
        Utility method to update the selected slide in the list.
        """
        if slideno > self.previewListWidget.rowCount():
            self.previewListWidget.selectRow(
                self.previewListWidget.rowCount() - 1)
        else:
            self.__checkUpdateSelectedSlide(slideno)

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
                    (self.previewListWidget.currentRow() == framenumber)
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
            self.previewListWidget.selectRow(0)
            self.slideSelected()

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
            self.__checkUpdateSelectedSlide(index)
            self.slideSelected()

    def mainDisplaySetBackground(self):
        """
        Allow the main display to blank the main display at startup time
        """
        log.debug(u'mainDisplaySetBackground live = %s' % self.isLive)
        display_type = QtCore.QSettings().value(
            self.parent().generalSettingsSection + u'/screen blank',
            QtCore.QVariant(u'')).toString()
        if not self.display.primary:
            # Order done to handle initial conversion
            if display_type == u'themed':
                self.onThemeDisplay(True)
            elif display_type == u'hidden':
                self.onHideDisplay(True)
            elif display_type == u'blanked':
                self.onBlankDisplay(True)
            else:
                Receiver.send_message(u'maindisplay_show')

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

    def onBlankDisplay(self, checked=None):
        """
        Handle the blank screen button actions
        """
        if checked is None:
            checked = self.blankScreen.isChecked()
        log.debug(u'onBlankDisplay %s' % checked)
        self.hideMenu.setDefaultAction(self.blankScreen)
        self.blankScreen.setChecked(checked)
        self.themeScreen.setChecked(False)
        self.desktopScreen.setChecked(False)
        if checked:
            QtCore.QSettings().setValue(
                self.parent().generalSettingsSection + u'/screen blank',
                QtCore.QVariant(u'blanked'))
        else:
            QtCore.QSettings().remove(
                self.parent().generalSettingsSection + u'/screen blank')
        self.blankPlugin()
        self.updatePreview()

    def onThemeDisplay(self, checked=None):
        """
        Handle the Theme screen button
        """
        if checked is None:
            checked = self.themeScreen.isChecked()
        log.debug(u'onThemeDisplay %s' % checked)
        self.hideMenu.setDefaultAction(self.themeScreen)
        self.blankScreen.setChecked(False)
        self.themeScreen.setChecked(checked)
        self.desktopScreen.setChecked(False)
        if checked:
            QtCore.QSettings().setValue(
                self.parent().generalSettingsSection + u'/screen blank',
                QtCore.QVariant(u'themed'))
        else:
            QtCore.QSettings().remove(
                self.parent().generalSettingsSection + u'/screen blank')
        self.blankPlugin()
        self.updatePreview()

    def onHideDisplay(self, checked=None):
        """
        Handle the Hide screen button
        """
        if checked is None:
            checked = self.desktopScreen.isChecked()
        log.debug(u'onHideDisplay %s' % checked)
        self.hideMenu.setDefaultAction(self.desktopScreen)
        self.blankScreen.setChecked(False)
        self.themeScreen.setChecked(False)
        self.desktopScreen.setChecked(checked)
        if checked:
            QtCore.QSettings().setValue(
                self.parent().generalSettingsSection + u'/screen blank',
                QtCore.QVariant(u'hidden'))
        else:
            QtCore.QSettings().remove(
                self.parent().generalSettingsSection + u'/screen blank')
        self.hidePlugin(checked)
        self.updatePreview()

    def blankPlugin(self):
        """
        Blank/Hide the display screen within a plugin if required.
        """
        hide_mode = self.hideMode()
        log.debug(u'blankPlugin %s ', hide_mode)
        if self.serviceItem is not None:
            if hide_mode:
                if not self.serviceItem.is_command():
                    Receiver.send_message(u'maindisplay_hide', hide_mode)
                Receiver.send_message(u'%s_blank'
                    % self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive, hide_mode])
            else:
                if not self.serviceItem.is_command():
                    Receiver.send_message(u'maindisplay_show')
                Receiver.send_message(u'%s_unblank'
                    % self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive])
        else:
            if hide_mode:
                Receiver.send_message(u'maindisplay_hide', hide_mode)
            else:
                Receiver.send_message(u'maindisplay_show')

    def hidePlugin(self, hide):
        """
        Tell the plugin to hide the display screen.
        """
        log.debug(u'hidePlugin %s ', hide)
        if self.serviceItem is not None:
            if hide:
                Receiver.send_message(u'maindisplay_hide', HideMode.Screen)
                Receiver.send_message(u'%s_hide'
                    % self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive])
            else:
                if not self.serviceItem.is_command():
                    Receiver.send_message(u'maindisplay_show')
                Receiver.send_message(u'%s_unblank'
                    % self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive])
        else:
            if hide:
                Receiver.send_message(u'maindisplay_hide', HideMode.Screen)
            else:
                Receiver.send_message(u'maindisplay_show')

    def onSlideSelected(self, start=False):
        """
        Slide selected in controller
        """
        self.slideSelected()

    def slideSelected(self, start=False):
        """
        Generate the preview when you click on a slide.
        if this is the Live Controller also display on the screen
        """
        row = self.previewListWidget.currentRow()
        self.selectedRow = 0
        if row > -1 and row < self.previewListWidget.rowCount():
            if self.serviceItem.is_command():
                if self.isLive and not start:
                    Receiver.send_message(
                        u'%s_slide' % self.serviceItem.name.lower(),
                        [self.serviceItem, self.isLive, row])
                self.updatePreview()
            else:
                toDisplay = self.serviceItem.get_rendered_frame(row)
                if self.serviceItem.is_text():
                    frame = self.display.text(toDisplay)
                else:
                    if start:
                        self.display.buildHtml(self.serviceItem, toDisplay)
                        frame = self.display.preview()
                    else:
                        frame = self.display.image(toDisplay)
                    # reset the store used to display first image
                    self.serviceItem.bg_image_bytes = None
                self.slidePreview.setPixmap(QtGui.QPixmap.fromImage(frame))
            self.selectedRow = row
            self.__checkUpdateSelectedSlide(row)
        Receiver.send_message(u'slidecontroller_%s_changed' % self.typePrefix,
            row)

    def onSlideChange(self, row):
        """
        The slide has been changed. Update the slidecontroller accordingly
        """
        self.__checkUpdateSelectedSlide(row)
        self.updatePreview()
        Receiver.send_message(u'slidecontroller_%s_changed' % self.typePrefix,
            row)

    def updatePreview(self):
        """
        This updates the preview frame, for example after changing a slide or
        using *Blank to Theme*.
        """
        log.debug(u'updatePreview %s ' % self.screens.current[u'primary'])
        if not self.screens.current[u'primary'] and self.serviceItem and \
            self.serviceItem.is_capable(ItemCapabilities.ProvidesOwnDisplay):
            # Grab now, but try again in a couple of seconds if slide change
            # is slow
            QtCore.QTimer.singleShot(0.5, self.grabMainDisplay)
            QtCore.QTimer.singleShot(2.5, self.grabMainDisplay)
        else:
            self.slidePreview.setPixmap(
                QtGui.QPixmap.fromImage(self.display.preview()))

    def grabMainDisplay(self):
        """
        Creates an image of the current screen and updates the preview frame.
        """
        winid = QtGui.QApplication.desktop().winId()
        rect = self.screens.current[u'size']
        winimg = QtGui.QPixmap.grabWindow(winid, rect.x(),
            rect.y(), rect.width(), rect.height())
        self.slidePreview.setPixmap(winimg)

    def onSlideSelectedNext(self, wrap=None):
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
            row = self.previewListWidget.currentRow() + 1
            if row == self.previewListWidget.rowCount():
                if wrap is None:
                    wrap = QtCore.QSettings().value(
                        self.parent().generalSettingsSection +
                        u'/enable slide loop', QtCore.QVariant(True)).toBool()
                if wrap:
                    row = 0
                else:
                    row = self.previewListWidget.rowCount() - 1
            self.__checkUpdateSelectedSlide(row)
            self.slideSelected()

    def onSlideSelectedPrevious(self):
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
            row = self.previewListWidget.currentRow() - 1
            if row == -1:
                if QtCore.QSettings().value(self.parent().generalSettingsSection
                    + u'/enable slide loop', QtCore.QVariant(True)).toBool():
                    row = self.previewListWidget.rowCount() - 1
                else:
                    row = 0
            self.__checkUpdateSelectedSlide(row)
            self.slideSelected()

    def __checkUpdateSelectedSlide(self, row):
        if row + 1 < self.previewListWidget.rowCount():
            self.previewListWidget.scrollToItem(
                self.previewListWidget.item(row + 1, 0))
        self.previewListWidget.selectRow(row)

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
            self.previewListWidget.selectRow(
                        self.previewListWidget.rowCount() - 1)
            self.slideSelected()

    def onToggleLoop(self):
        """
        Toggles the loop state.
        """
        if self.playSlidesLoop.isChecked() or self.playSlidesOnce.isChecked():
            self.onStartLoop()
        else:
            self.onStopLoop()

    def onStartLoop(self):
        """
        Start the timer loop running and store the timer id
        """
        if self.previewListWidget.rowCount() > 1:
            self.timer_id = self.startTimer(
                int(self.delaySpinBox.value()) * 1000)

    def onStopLoop(self):
        """
        Stop the timer loop running
        """
        if self.timer_id != 0:
            self.killTimer(self.timer_id)
            self.timer_id = 0

    def onPlaySlidesLoop(self, checked=None):
        """
        Start or stop 'Play Slides in Loop'
        """
        if checked is None:
            checked = self.playSlidesLoop.isChecked()
        else:
            self.playSlidesLoop.setChecked(checked)
        log.debug(u'onPlaySlidesLoop %s' % checked)
        self.playSlidesMenu.setDefaultAction(self.playSlidesLoop)
        self.playSlidesOnce.setChecked(False)
        self.onToggleLoop()

    def onPlaySlidesOnce(self, checked=None):
        """
        Start or stop 'Play Slides to End'
        """
        if checked is None:
            checked = self.playSlidesOnce.isChecked()
        else:
            self.playSlidesOnce.setChecked(checked)
        log.debug(u'onPlaySlidesOnce %s' % checked)
        self.playSlidesMenu.setDefaultAction(self.playSlidesOnce)
        self.playSlidesLoop.setChecked(False)
        self.onToggleLoop()

    def timerEvent(self, event):
        """
        If the timer event is for this window select next slide
        """
        if event.timerId() == self.timer_id:
            self.onSlideSelectedNext(self.playSlidesLoop.isChecked())

    def onEditSong(self):
        """
        From the preview display requires the service Item to be editied
        """
        self.songEdit = True
        Receiver.send_message(u'%s_edit' % self.serviceItem.name.lower(),
            u'P:%s' % self.serviceItem.edit_id)

    def onPreviewAddToService(self):
        """
        From the preview display request the Item to be added to service
        """
        if self.serviceItem:
            self.parent().serviceManagerContents.addServiceItem(
                self.serviceItem)

    def onGoLiveClick(self):
        """
        triggered by clicking the Preview slide items
        """
        if QtCore.QSettings().value(u'advanced/double click live',
            QtCore.QVariant(False)).toBool():
            # Live and Preview have issues if we have video or presentations
            # playing in both at the same time.
            if self.serviceItem.is_command():
                Receiver.send_message(u'%s_stop' %
                    self.serviceItem.name.lower(),
                    [self.serviceItem, self.isLive])
            if self.serviceItem.is_media():
                self.onMediaClose()
            self.onGoLive()

    def onGoLive(self):
        """
        If preview copy slide item to live
        """
        row = self.previewListWidget.currentRow()
        if row > -1 and row < self.previewListWidget.rowCount():
            if self.serviceItem.from_service:
                Receiver.send_message('servicemanager_preview_live',
                    u'%s:%s' % (self.serviceItem._uuid, row))
            else:
                self.parent().liveController.addServiceManagerItem(
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
            self.slidePreview.hide()
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
        self.slidePreview.clear()
        self.slidePreview.show()

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
        self.slidePreview.clear()
        self.slidePreview.show()

    def _resetBlank(self):
        """
        Used by command items which provide their own displays to reset the
        screen hide attributes
        """
        hide_mode = self.hideMode()
        if hide_mode == HideMode.Blank:
            self.onBlankDisplay(True)
        elif hide_mode == HideMode.Theme:
            self.onThemeDisplay(True)
        elif hide_mode == HideMode.Screen:
            self.onHideDisplay(True)
        else:
            self.hidePlugin(False)

    def hideMode(self):
        """
        Determine what the hide mode should be according to the blank button
        """
        if not self.isLive:
            return None
        elif self.blankScreen.isChecked():
            return HideMode.Blank
        elif self.themeScreen.isChecked():
            return HideMode.Theme
        elif self.desktopScreen.isChecked():
            return HideMode.Screen
        else:
            return None
