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
from PyQt4 import QtCore, QtGui

from time import sleep
from openlp.core.lib import translate,  Receiver

class MainDisplay(QtGui.QWidget):
    """
    This is the form that is used to display things on the projector.
    """
    global log
    log=logging.getLogger(u'MainDisplay')
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
        self.display = QtGui.QLabel(self)
        self.display.setScaledContents(True)
        self.layout.addWidget(self.display)
        self.displayBlank = False
        self.blankFrame = None
        self.alertactive = False
        self.alertTab = None
        self.timer_id = 0
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'live_slide_blank'), self.blankDisplay)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'alert_text'), self.displayAlert)

    def setup(self, screenNumber):
        """
        Sets up the screen on a particular screen.
        @param (integer) screen This is the screen number.
        """
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
        else:
            self.showMinimized()
        #Build a custom splash screen
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

    def blankDisplay(self):
        if not self.displayBlank:
            self.displayBlank = True
            self.display.setPixmap(QtGui.QPixmap.fromImage(self.blankFrame))
        else:
            self.displayBlank = False
            self.frameView(self.frame)

    def displayAlert(self,  text=u''):
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
            QtCore.QRect(0, top, alertframe.rect().width(), alertframe.rect().height() - top),
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
