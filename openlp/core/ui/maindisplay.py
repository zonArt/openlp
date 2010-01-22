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
import time

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import Receiver

class DisplayWidget(QtGui.QWidget):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    global log
    log = logging.getLogger(u'MainDisplay')
    log.info(u'MainDisplay loaded')

    def __init__(self, parent=None, name=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent

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
    global log
    log = logging.getLogger(u'MainDisplay')
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
        self.display = QtGui.QLabel(self)
        self.display.setScaledContents(True)
        self.alertDisplay = QtGui.QLabel(self)
        self.alertDisplay.setScaledContents(True)
        self.primary = True
        self.displayBlank = False
        self.blankFrame = None
        self.frame = None
        self.timer_id = 0
        self.firstTime = True
        self.mediaLoaded = False
        self.hasTransition = False
        self.alertList = []
        self.mediaBackground = False
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'alert_text'), self.displayAlert)
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
            QtCore.SIGNAL(u'media_pause'), self.onMediaPaws)
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
        self.alertScreenPosition = self.screen[u'size'].height() * 0.9
        self.alertHeight = self.screen[u'size'].height() - self.alertScreenPosition
        self.alertDisplay.setGeometry(
            QtCore.QRect(0, self.alertScreenPosition,
                        self.screen[u'size'].width(),self.alertHeight))
        self.video.setGeometry(self.screen[u'size'])
        self.display.resize(self.screen[u'size'].width(),
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
        self.frameView(self.InitialFrame)
        #Build a Black screen
        painter = QtGui.QPainter()
        self.blankFrame = QtGui.QImage(
            self.screen[u'size'].width(),
            self.screen[u'size'].height(),
            QtGui.QImage.Format_ARGB32_Premultiplied)
        painter.begin(self.blankFrame)
        painter.fillRect(self.blankFrame.rect(), QtCore.Qt.red)
        #buid a blank transparent image
        self.transparent = QtGui.QPixmap(self.screen[u'size'].width(),
                                         self.screen[u'size'].height())
        self.transparent.fill(QtCore.Qt.transparent)
        # To display or not to display?
        if not self.screen[u'primary']:
            self.showFullScreen()
            self.primary = False
        else:
            self.setVisible(False)
            self.primary = True

    def resetDisplay(self):
        if self.primary:
            self.setVisible(False)

    def hideDisplay(self):
        self.setVisible(False)

    def showDisplay(self):
        if not self.primary:
            self.setVisible(True)

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
                    self.display.setPixmap(QtGui.QPixmap.fromImage(self.frame))
                    self.repaint()
                self.frame = None
                if frame[u'trans'] is not None:
                    self.display.setPixmap(QtGui.QPixmap.fromImage(frame[u'trans']))
                    self.repaint()
                    self.frame = frame[u'trans']
                self.display.setPixmap(QtGui.QPixmap.fromImage(frame[u'main']))
                self.repaint()
            else:
                self.display.setPixmap(QtGui.QPixmap.fromImage(frame))
            if not self.isVisible():
                self.setVisible(True)
                self.showFullScreen()

    def blankDisplay(self, blanked=True):
        if blanked:
            self.displayBlank = True
            self.display.setPixmap(QtGui.QPixmap.fromImage(self.blankFrame))
        else:
            self.displayBlank = False
            if self.frame:
                self.frameView(self.frame)
        if blanked != self.parent.LiveController.blankButton.isChecked():
            self.parent.LiveController.blankButton.setChecked(self.displayBlank)
        self.parent.generalConfig.set_config(u'screen blank', self.displayBlank)

    def displayAlert(self, text=u''):
        """
        Called from the Alert Tab to display an alert

        ``text``
            display text
        """
        log.debug(u'display alert called %s' % text)
        self.alertList.append(text)
        if self.timer_id != 0:
            return
        self.generateAlert()

    def generateAlert(self):
        log.debug(u'Generate Alert called')
        if len(self.alertList) == 0:
            return
        text = self.alertList.pop(0)
        alertTab = self.parent.settingsForm.AlertsTab
        alertframe = \
            QtGui.QPixmap(self.screen[u'size'].width(), self.alertHeight)
        alertframe.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(alertframe)
        painter.fillRect(alertframe.rect(), QtCore.Qt.transparent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(
            QtCore.QRect(
                0, 0, alertframe.rect().width(),
                alertframe.rect().height()),
            QtGui.QColor(alertTab.bg_color))
        font = QtGui.QFont()
        font.setFamily(alertTab.font_face)
        font.setBold(True)
        font.setPointSize(40)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(alertTab.font_color))
        x, y = (0, 0)
        metrics = QtGui.QFontMetrics(font)
        painter.drawText(
            x, y + metrics.height() - metrics.descent() - 1, text)
        painter.end()
        self.alertDisplay.setPixmap(alertframe)
        self.alertDisplay.setVisible(True)
        # check to see if we have a timer running
        if self.timer_id == 0:
            self.timer_id = self.startTimer(int(alertTab.timeout) * 1000)

    def timerEvent(self, event):
        if event.timerId() == self.timer_id:
            self.alertDisplay.setPixmap(self.transparent)
        self.killTimer(self.timer_id)
        self.timer_id = 0
        self.generateAlert()

    def onMediaQueue(self, message):
        log.debug(u'Queue new media message %s' % message)
        self.display.close()
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
        self.firstTime = True
        self.mediaLoaded = True
        self.display.hide()
        self.video.setFullScreen(True)
        self.video.setVisible(True)
        self.mediaObject.play()
        if self.primary:
            self.setVisible(True)

    def onMediaPaws(self):
        log.debug(u'Media paused by user')
        self.mediaObject.pause()

    def onMediaStop(self):
        log.debug(u'Media stopped by user')
        self.mediaObject.stop()

    def onMediaFinish(self):
        log.debug(u'Reached end of media playlist')
        if self.primary:
            self.setVisible(False)
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        self.mediaLoaded = False
        self.video.setVisible(False)
        self.display.show()
