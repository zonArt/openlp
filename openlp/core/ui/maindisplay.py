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
import os

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import Receiver, resize_image
from openlp.core.ui import HideMode

log = logging.getLogger(__name__)


class DisplayManager(QtGui.QWidget):
    """
    Wrapper class to hold the display widgets.
    I will provide API's in future to access the screens allow for
    extra displays to be added.
    """
    def __init__(self, screens):
        QtGui.QWidget.__init__(self)
        self.screens = screens
        self.videoDisplay = VideoDisplay(self, screens)
        self.mainDisplay = MainDisplay(self, screens)

    def setup(self):
        self.videoDisplay.setup()
        self.mainDisplay.setup()

    def close(self):
        self.videoDisplay.close()
        self.mainDisplay.close()


class DisplayWidget(QtGui.QWidget):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    log.info(u'MainDisplay loaded')

    def __init__(self, parent=None, name=None):
        QtGui.QWidget.__init__(self, None)
        self.parent = parent
        self.hotkey_map = {
            QtCore.Qt.Key_Return: 'servicemanager_next_item',
            QtCore.Qt.Key_Space: 'slidecontroller_live_next_noloop',
            QtCore.Qt.Key_Enter: 'slidecontroller_live_next_noloop',
            QtCore.Qt.Key_0: 'servicemanager_next_item',
            QtCore.Qt.Key_Backspace: 'slidecontroller_live_previous_noloop'}

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            #here accept the event and do something
            if event.key() == QtCore.Qt.Key_Up:
                Receiver.send_message(u'slidecontroller_live_previous')
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                Receiver.send_message(u'slidecontroller_live_next')
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageUp:
                Receiver.send_message(u'slidecontroller_live_first')
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageDown:
                Receiver.send_message(u'slidecontroller_live_last')
                event.accept()
            elif event.key() in self.hotkey_map:
                Receiver.send_message(self.hotkey_map[event.key()])
                event.accept()
            elif event.key() == QtCore.Qt.Key_Escape:
                self.resetDisplay()
                event.accept()
            event.ignore()
        else:
            event.ignore()

class MainDisplay(DisplayWidget):
    """
    This is the form that is used to display things on the projector.
    """
    log.info(u'MainDisplay Loaded')

    def __init__(self, parent, screens):
        """
        The constructor for the display form.

        ``parent``
            The parent widget.

        ``screens``
            The list of screens.
        """
        log.debug(u'Initialisation started')
        DisplayWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle(u'OpenLP Display')
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.screens = screens
        self.display_image = QtGui.QLabel(self)
        self.display_image.setScaledContents(True)
        self.display_text = QtGui.QLabel(self)
        self.display_text.setScaledContents(True)
        self.display_alert = QtGui.QLabel(self)
        self.display_alert.setScaledContents(True)
        self.primary = True
        self.displayBlank = False
        self.blankFrame = None
        self.frame = None
        self.firstTime = True
        self.hasTransition = False
        self.mediaBackground = False
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_hide'), self.hideDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'maindisplay_show'), self.showDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_start'), self.hideDisplay)

    def setup(self):
        """
        Sets up the screen on a particular screen.
        """
        log.debug(u'Setup %s for %s ' %(self.screens,
                                         self.screens.monitor_number))
        self.setVisible(False)
        self.screen = self.screens.current
        #Sort out screen locations and sizes
        self.setGeometry(self.screen[u'size'])
        self.display_alert.setGeometry(self.screen[u'size'])
        self.display_image.resize(self.screen[u'size'].width(),
                            self.screen[u'size'].height())
        self.display_text.resize(self.screen[u'size'].width(),
                            self.screen[u'size'].height())
        #Build a custom splash screen
        self.InitialFrame = QtGui.QImage(
            self.screen[u'size'].width(),
            self.screen[u'size'].height(),
            QtGui.QImage.Format_ARGB32_Premultiplied)
        splash_image = QtGui.QImage(u':/graphics/openlp-splash-screen.png')
        painter_image = QtGui.QPainter()
        painter_image.begin(self.InitialFrame)
        painter_image.fillRect(self.InitialFrame.rect(), QtCore.Qt.white)
        painter_image.drawImage(
            (self.screen[u'size'].width() - splash_image.width()) / 2,
            (self.screen[u'size'].height() - splash_image.height()) / 2,
            splash_image)
        self.display_image.setPixmap(QtGui.QPixmap.fromImage(self.InitialFrame))
        self.repaint()
        #Build a Black screen
        painter = QtGui.QPainter()
        self.blankFrame = QtGui.QImage(
            self.screen[u'size'].width(),
            self.screen[u'size'].height(),
            QtGui.QImage.Format_ARGB32_Premultiplied)
        painter.begin(self.blankFrame)
        painter.fillRect(self.blankFrame.rect(), QtCore.Qt.black)
        #build a blank transparent image
        self.transparent = QtGui.QPixmap(self.screen[u'size'].width(),
                                         self.screen[u'size'].height())
        self.transparent.fill(QtCore.Qt.transparent)
        self.display_alert.setPixmap(self.transparent)
        self.display_text.setPixmap(self.transparent)
        self.frameView(self.transparent)
        # To display or not to display?
        if not self.screen[u'primary']:
            self.showFullScreen()
            self.primary = False
        else:
            self.setVisible(False)
            self.primary = True

    def resetDisplay(self):
        log.debug(u'resetDisplay')
        Receiver.send_message(u'slidecontroller_live_stop_loop')
        if self.primary:
            self.setVisible(False)
        else:
            self.showFullScreen()

    def hideDisplay(self):
        log.debug(u'hideDisplay')
        self.display_image.setPixmap(self.transparent)
        self.display_alert.setPixmap(self.transparent)
        self.display_text.setPixmap(self.transparent)
        self.moveToTop()

    def moveToTop(self):
        log.debug(u'moveToTop')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint \
            | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        self.show()

    def showDisplay(self):
        log.debug(u'showDisplay')
        if not self.primary:
            self.setVisible(True)
            self.showFullScreen()
        Receiver.send_message(u'maindisplay_active')

    def addImageWithText(self, frame):
        log.debug(u'addImageWithText')
        frame = resize_image(frame,
                    self.screen[u'size'].width(),
                    self.screen[u'size'].height() )
        self.display_image.setPixmap(QtGui.QPixmap.fromImage(frame))
        self.moveToTop()

    def setAlertSize(self, top, height):
        log.debug(u'setAlertSize')
        self.display_alert.setGeometry(
            QtCore.QRect(0, top,
                        self.screen[u'size'].width(), height))

    def addAlertImage(self, frame, blank=False):
        log.debug(u'addAlertImage')
        if blank:
            self.display_alert.setPixmap(self.transparent)
        else:
            self.display_alert.setPixmap(frame)
        self.moveToTop()

    def frameView(self, frame, transition=False):
        """
        Called from a slide controller to display a frame
        if the alert is in progress the alert is added on top
        ``frame``
            Image frame to be rendered
        """
        log.debug(u'frameView %d' % (self.displayBlank))
        if not self.displayBlank:
            if transition:
                if self.frame is not None:
                    self.display_text.setPixmap(
                        QtGui.QPixmap.fromImage(self.frame))
                    self.repaint()
                self.frame = None
                if frame[u'trans'] is not None:
                    self.display_text.setPixmap(
                        QtGui.QPixmap.fromImage(frame[u'trans']))
                    self.repaint()
                    self.frame = frame[u'trans']
                self.display_text.setPixmap(
                    QtGui.QPixmap.fromImage(frame[u'main']))
                self.display_frame = frame[u'main']
                self.repaint()
            else:
                if isinstance(frame, QtGui.QPixmap):
                    self.display_text.setPixmap(frame)
                else:
                    self.display_text.setPixmap(QtGui.QPixmap.fromImage(frame))
                self.display_frame = frame
            if not self.isVisible() and self.screens.display:
                self.setVisible(True)
                self.showFullScreen()
        else:
            self.waitingFrame = frame
            self.waitingFrameTrans = transition

    def blankDisplay(self, blankType=HideMode.Blank, blanked=True):
        log.debug(u'Blank main Display %d' % blanked)
        if blanked:
            self.displayBlank = True
            if blankType == HideMode.Blank:
                self.display_text.setPixmap(
                    QtGui.QPixmap.fromImage(self.blankFrame))
            elif blankType == HideMode.Theme:
                theme = self.parent.RenderManager.renderer.bg_frame
                if not theme:
                    theme = self.blankFrame
                self.display_text.setPixmap(QtGui.QPixmap.fromImage(theme))
            self.waitingFrame = None
            self.waitingFrameTrans = False
        else:
            self.displayBlank = False
            if self.waitingFrame:
                self.frameView(self.waitingFrame, self.waitingFrameTrans)
            elif self.display_frame:
                self.frameView(self.display_frame)

class VideoDisplay(Phonon.VideoWidget):
    """
    This is the form that is used to display videos on the projector.
    """
    log.info(u'VideoDisplay Loaded')

    def __init__(self, parent, screens,
        aspect=Phonon.VideoWidget.AspectRatioWidget):
        """
        The constructor for the display form.

        ``parent``
            The parent widget.

        ``screens``
            The list of screens.
        """
        log.debug(u'VideoDisplay Initialisation started')
        Phonon.VideoWidget.__init__(self)
        self.setWindowTitle(u'OpenLP Video Display')
        self.parent = parent
        self.screens = screens
        self.mediaObject = Phonon.MediaObject()
        self.setAspectRatio(aspect)
        self.audioObject = Phonon.AudioOutput(Phonon.VideoCategory)
        Phonon.createPath(self.mediaObject, self)
        Phonon.createPath(self.mediaObject, self.audioObject)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_start'), self.onMediaQueue)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_play'), self.onMediaPlay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_pause'), self.onMediaPause)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'videodisplay_stop'), self.onMediaStop)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.setup)

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            #here accept the event and do something
            if event.key() == QtCore.Qt.Key_Escape:
                self.onMediaStop()
                event.accept()
            event.ignore()
        else:
            event.ignore()

    def setup(self):
        """
        Sets up the screen on a particular screen.
        """
        log.debug(u'VideoDisplay Setup %s for %s ' %(self.screens,
             self.screens.monitor_number))
        self.setVisible(False)
        self.screen = self.screens.current
        #Sort out screen locations and sizes
        self.setGeometry(self.screen[u'size'])
        # To display or not to display?
        if not self.screen[u'primary']:
            self.showFullScreen()
            self.primary = False
        else:
            self.setVisible(False)
            self.primary = True

    def onMediaQueue(self, message):
        log.debug(u'VideoDisplay Queue new media message %s' % message)
        file = os.path.join(message[0].get_frame_path(), 
            message[0].get_frame_title())
        source = self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
        self.onMediaPlay()

    def onMediaPlay(self):
        log.debug(u'VideoDisplay Play the new media, Live ')
        self.mediaObject.play()
        self.setVisible(True)
        self.showFullScreen()

    def onMediaPause(self):
        log.debug(u'VideoDisplay Media paused by user')
        self.mediaObject.pause()
        self.show()

    def onMediaStop(self):
        log.debug(u'VideoDisplay Media stopped by user')
        self.mediaObject.stop()
        self.onMediaFinish()

    def onMediaFinish(self):
        log.debug(u'VideoDisplay Reached end of media playlist')
        self.mediaObject.clearQueue()
        self.setVisible(False)
