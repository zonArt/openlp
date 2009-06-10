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

from PyQt4 import QtCore, QtGui, QtTest

from time import sleep
from openlp.core.lib import translate

class MainDisplay(QtGui.QWidget):

    def __init__(self, parent , screens):
        QtGui.QWidget.__init__(self, parent)
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
        self.blankFrame= None
        self.alertactive = False
        self.alerttext = u''
        self.alertTab = None

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
        painter = QtGui.QPainter()
        self.blankFrame = QtGui.QImage(screen[u'size'].width(),
            screen[u'size'].height(), QtGui.QImage.Format_ARGB32_Premultiplied)
        painter.begin(self.blankFrame)
        painter.fillRect(self.blankFrame.rect(), QtCore.Qt.black)
        self.frameView(self.blankFrame)

    def frameView(self, frame):
        self.frame = frame
        if not self.displayBlank:
            self.display.setPixmap(QtGui.QPixmap.fromImage(frame))
        elif self.alertactive:
            self.displayAlert()

    def blankDisplay(self):
        if not self.displayBlank:
            self.displayBlank = True
            self.display.setPixmap(self.blankFrame)
        else:
            self.displayBlank = False
            self.frameView(self.frame)

    def alert(self, alertTab, text):
        """
        Called from the Alert Tab
        alertTab = details from AlertTab
        text = display text
        screen = screen number to be displayed on.
        """
        self.alerttext = text
        self.alertTab = alertTab
        if len(text) > 0:
            self.alertactive = True
            self.displayAlert()
            self.alertactive = False

    def displayAlert(self):
        alertframe = QtGui.QPixmap(self.frame)
        painter = QtGui.QPainter(alertframe)
        top = alertframe.rect().height() * 0.9
        painter.fillRect(QtCore.QRect(0, top , alertframe.rect().width(), alertframe.rect().height() - top), QtGui.QColor(self.alertTab.bg_color))
        font = QtGui.QFont()
        font.setFamily(self.alertTab.font_face)
        font.setBold(True)
        font.setPointSize(40)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(self.alertTab.font_color))
        x, y = (0, top)
        metrics=QtGui.QFontMetrics(font)
        painter.drawText(x, y+metrics.height()-metrics.descent()-1, self.alerttext)
        painter.end()
        self.display.setPixmap(alertframe)
        QtTest.QTest.qWait(self.alertTab.timeout*1000)
        self.display.setPixmap(self.frame)
