# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

log = logging.getLogger(__name__)

class DisplayWidget(QtGui.QWidget):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    log.info(u'MainDisplay loaded')

    def __init__(self, parent=None, name=None):
        QtGui.QWidget.__init__(self, parent)
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
                Receiver.send_message(u'live_slidecontroller_previous')
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                Receiver.send_message(u'live_slidecontroller_next')
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageUp:
                Receiver.send_message(u'live_slidecontroller_first')
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageDown:
                Receiver.send_message(u'live_slidecontroller_last')
                event.accept()
            elif event.key() in self.hotkey_map:
                Receiver.send_message(self.hotkey_map[event.key()]);
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
        log.debug(u'Initilisation started')
        DisplayWidget.__init__(self, None)
        self.parent = parent
        self.setWindowTitle(u'OpenLP Display')
        self.screens = screens
        self.mediaObject = Phonon.MediaObject(self)
        self.video = Phonon.VideoWidget()
        self.video.setVisible(False)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self.mediaObject)
        Phonon.createPath(self.mediaObject, self.video)
        Phonon.createPath(self.mediaObject, self.audio)
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
        self.mediaLoaded = False
        self.hasTransition = False
        self.mediaBackground = False
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'live_slide_hide'), self.hideDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'live_slide_show'), self.showDisplay)
        QtCore.QObject.connect(self.mediaObject,
            QtCore.SIGNAL(u'finished()'), self.onMediaFinish)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_start'), self.onMediaQueue)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_play'), self.onMediaPlay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_pause'), self.onMediaPause)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'media_stop'), self.onMediaStop)

    def setup(self, screenNumber):
        """
        Sets up the screen on a particular screen.
        @param (integer) screen This is the screen number.
        """
        log.debug(u'Setup %s for %s ' %(self.screens, screenNumber))
        self.setVisible(False)
        self.screen = self.screens.current
        #Sort out screen locations and sizes
        self.setGeometry(self.screen[u'size'])
        self.display_alert.setGeometry(self.screen[u'size'])
        self.video.setGeometry(self.screen[u'size'])
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
        #TODO make black when testing finished
        painter.fillRect(self.blankFrame.rect(), QtCore.Qt.red)
        #build a blank transparent image
        self.transparent = QtGui.QPixmap(self.screen[u'size'].width(),
                                         self.screen[u'size'].height())
        self.transparent.fill(QtCore.Qt.transparent)
        self.display_alert.setPixmap(self.transparent)
        self.frameView(self.transparent)
        # To display or not to display?
        if not self.screen[u'primary']:
            self.showFullScreen()
            self.primary = False
        else:
            self.setVisible(False)
            self.primary = True
        Receiver.send_message(u'screen_changed')

    def resetDisplay(self):
        Receiver.send_message(u'stop_display_loop')
        if self.primary:
            self.setVisible(False)
        else:
            self.showFullScreen()

    def hideDisplay(self):
        self.mediaLoaded = True
        self.setVisible(False)

    def showDisplay(self):
        self.mediaLoaded = False
        if not self.primary:
            self.setVisible(True)
            self.showFullScreen()
        Receiver.send_message(u'flush_alert')

    def addImageWithText(self, frame):
        frame = resize_image(frame,
                    self.screen[u'size'].width(),
                    self.screen[u'size'].height() )
        self.display_image.setPixmap(QtGui.QPixmap.fromImage(frame))

    def setAlertSize(self, top, height):
        self.display_alert.setGeometry(
            QtCore.QRect(0, top,
                        self.screen[u'size'].width(), height))

    def addAlertImage(self, frame, blank=False):
        if blank:
            self.display_alert.setPixmap(self.transparent)
        else:
            self.display_alert.setPixmap(frame)

    def frameView(self, frame, transition=False):
        """
        Called from a slide controller to display a frame
        if the alert is in progress the alert is added on top
        ``frame``
            Image frame to be rendered
        """
        if not self.displayBlank:
            if transition:
                if self.frame is not None:
                    self.display_text.setPixmap(QtGui.QPixmap.fromImage(self.frame))
                    self.repaint()
                self.frame = None
                if frame[u'trans'] is not None:
                    self.display_text.setPixmap(QtGui.QPixmap.fromImage(frame[u'trans']))
                    self.repaint()
                    self.frame = frame[u'trans']
                self.display_text.setPixmap(QtGui.QPixmap.fromImage(frame[u'main']))
                self.display_frame = frame[u'main']
                self.repaint()
            else:
                if isinstance(frame, QtGui.QPixmap):
                    self.display_text.setPixmap(frame)
                else:
                    self.display_text.setPixmap(QtGui.QPixmap.fromImage(frame))
                self.display_frame = frame
            if not self.isVisible():
                self.setVisible(True)
                self.showFullScreen()

    def blankDisplay(self, blanked=True):
        if blanked:
            self.displayBlank = True
            self.display_text.setPixmap(QtGui.QPixmap.fromImage(self.blankFrame))
        else:
            self.displayBlank = False
            if self.display_frame:
                self.frameView(self.display_frame)

    def onMediaQueue(self, message):
        log.debug(u'Queue new media message %s' % message)
        self.display_image.close()
        self.display_text.close()
        self.display_alert.close()
        file = os.path.join(message[1], message[2])
        if self.firstTime:
            self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
            self.firstTime = False
        else:
            self.mediaObject.enqueue(Phonon.MediaSource(file))
        self.onMediaPlay()

    def onMediaPlay(self):
        log.debug(u'Play the new media, Live ')
        if not self.mediaLoaded and not self.displayBlank:
            self.blankDisplay()
            self.display_frame = self.blankFrame
        self.firstTime = True
        self.mediaLoaded = True
        self.display_image.hide()
        self.display_text.hide()
        self.display_alert.hide()
        self.video.setFullScreen(True)
        self.video.setVisible(True)
        self.mediaObject.play()
        self.setVisible(True)
        self.hide()

    def onMediaPause(self):
        log.debug(u'Media paused by user')
        self.mediaObject.pause()

    def onMediaStop(self):
        log.debug(u'Media stopped by user')
        self.mediaObject.stop()
        self.onMediaFinish()

    def onMediaFinish(self):
        log.debug(u'Reached end of media playlist')
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        self.mediaLoaded = False
        self.video.setVisible(False)
        self.display_text.show()
        self.display_image.show()
        self.blankDisplay(False)
