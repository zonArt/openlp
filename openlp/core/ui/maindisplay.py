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

from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon

from openlp.core.lib import Receiver, str_to_bool

class DisplayLabel(QtGui.QWidget):
    """
    Customised version of QTableWidget which can respond to keyboard
    events.
    """
    def __init__(self, parent=None, name=None):
        QQtGui.QWidget.__init__(self, parent)
        self.parent = parent

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            #here accept the event and do something
            if event.key() == QtCore.Qt.Key_Up:
                Receiver().send_message(u'slidecontroller_previous')
                event.accept()
            elif event.key() == QtCore.Qt.Key_Down:
                Receiver().send_message(u'slidecontroller_next')
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageUp:
                Receiver().send_message(u'slidecontroller_first')
                event.accept()
            elif event.key() == QtCore.Qt.Key_PageDown:
                Receiver().send_message(u'slidecontroller_last')
                event.accept()
            elif event.key() == QtCore.Qt.Key_Escape:
                self.resetDisplay()
                event.accept()
            event.ignore()
        else:
            event.ignore()

class MainDisplay(DisplayLabel):
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
        QtGui.QWidget.__init__(self, None)
        self.parent = parent
        self.setWindowTitle(u'OpenLP Display')
        self.screens = screens
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.layout.setObjectName(u'layout')
        self.mediaObject = Phonon.MediaObject(self)
        self.video = Phonon.VideoWidget()
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self.mediaObject)
        self.video.setFullScreen(True)
        Phonon.createPath(self.mediaObject, self.video)
        Phonon.createPath(self.mediaObject, self.audio)
        self.layout.insertWidget(0, self.video)
        self.display = QtGui.QLabel(self)
        self.display.setScaledContents(True)
        self.layout.insertWidget(0, self.display)
        self.displayBlank = False
        self.blankFrame = None
        self.frame = None
        self.alertactive = False
        self.alertTab = None
        self.timer_id = 0
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'live_slide_blank'), self.blankDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'alert_text'), self.displayAlert)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_start'), self.hideDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_stop'), self.showDisplay)
        QtCore.QObject.connect(self.mediaObject, QtCore.SIGNAL(u'finished()'),
            self.onMediaFinish)

    def setup(self, screenNumber):
        """
        Sets up the screen on a particular screen.
        @param (integer) screen This is the screen number.
        """
        log.debug(u'Setup %s for %s ' %(self.screens, screenNumber) )
        screen = self.screens[screenNumber]
        if screen[u'number'] != screenNumber:
            # We will most probably never actually hit this bit, but just in
            # case the index in the list doesn't match the screen number, we
            # search for it.
            for scrn in self.screens:
                if scrn[u'number'] == screenNumber:
                    screen = scrn
                    break
        self.setGeometry(screen[u'size'])
        if not screen[u'primary']:
            self.showFullScreen()
            self.primary = False
        else:
            self.setVisible(False)
            self.primary = True
        #Build a custom splash screen
        if str_to_bool(self.parent.generalConfig.get_config(u'show splash', u'True')):
            self.InitialFrame = QtGui.QImage(
                screen[u'size'].width(), screen[u'size'].height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
            splash_image = QtGui.QImage(u':/graphics/openlp-splash-screen.png')
            painter_image = QtGui.QPainter()
            painter_image.begin(self.InitialFrame)
            painter_image.fillRect(self.InitialFrame.rect(), QtCore.Qt.white)
            painter_image.drawImage(
                (screen[u'size'].width() - splash_image.width()) / 2,
                (screen[u'size'].height() - splash_image.height()) / 2,
                splash_image)
            self.frameView(self.InitialFrame)
        #Build a Black screen
        painter = QtGui.QPainter()
        self.blankFrame = QtGui.QImage(
            screen[u'size'].width(), screen[u'size'].height(),
            QtGui.QImage.Format_ARGB32_Premultiplied)
        painter.begin(self.blankFrame)
        painter.fillRect(self.blankFrame.rect(), QtCore.Qt.black)

    def resetDisplay(self):
        if self.primary:
            self.setVisible(False)

    def hideDisplay(self):
        self.setVisible(False)

    def showDisplay(self):
        if not self.primary:
            self.setVisible(True)

    def frameView(self, frame):
        """
        Called from a slide controller to display a frame
        if the alert is in progress the alert is added on top
        ``frame``
            Image frame to be rendered
        """
        self.frame = frame
        if self.timer_id != 0 :
            self.displayAlert()
        elif not self.displayBlank:
            self.display.setPixmap(QtGui.QPixmap.fromImage(frame))
            if not self.isVisible():
                self.setVisible(True)
                self.showFullScreen()

    def blankDisplay(self):
        if not self.displayBlank:
            self.displayBlank = True
            self.display.setPixmap(QtGui.QPixmap.fromImage(self.blankFrame))
        else:
            self.displayBlank = False
            if self.frame is not None:
                self.frameView(self.frame)
        self.parent.generalConfig.set_config(u'Screen Blank',self.displayBlank)

    def displayAlert(self, text=u''):
        """
        Called from the Alert Tab to display an alert

        ``text``
            display text
        """
        alertTab = self.parent.settingsForm.AlertsTab
        alertframe = QtGui.QPixmap.fromImage(self.frame)
        painter = QtGui.QPainter(alertframe)
        top = alertframe.rect().height() * 0.9
        painter.fillRect(
            QtCore.QRect(
                0, top, alertframe.rect().width(),
                alertframe.rect().height() - top),
            QtGui.QColor(alertTab.bg_color))
        font = QtGui.QFont()
        font.setFamily(alertTab.font_face)
        font.setBold(True)
        font.setPointSize(40)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(alertTab.font_color))
        x, y = (0, top)
        metrics = QtGui.QFontMetrics(font)
        painter.drawText(
            x, y + metrics.height() - metrics.descent() - 1, text)
        painter.end()
        self.display.setPixmap(alertframe)
        # check to see if we have a timer running
        if self.timer_id == 0:
            self.timer_id = self.startTimer(int(alertTab.timeout) * 1000)

    def timerEvent(self, event):
        if event.timerId() == self.timer_id:
            self.display.setPixmap(QtGui.QPixmap.fromImage(self.frame))
            self.killTimer(self.timer_id)
            self.timer_id = 0

    def queueMedia(self, item, firstItem=True):
        if firstItem:
            self.mediaObject.setCurrentSource(Phonon.MediaSource(item))
        else:
            self.mediaObject.enqueue(Phonon.MediaSource(item))

    def playMedia(self):
        self.display.close()
        self.mediaObject.play()

    def stopMedia(self):
        self.mediaObject.stop()

    def onMediaFinish(self):
        self.mediaObject.stop()
        self.video.close()
        self.display = QtGui.QLabel(self)
        self.display.setScaledContents(True)
        self.layout.insertWidget(0, self.display)

    def mediaFinished(self):
        pass
