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

from PyQt4 import QtCore, QtGui

from openlp.core.lib import Receiver

log = logging.getLogger(__name__)

class AlertsManager(QtCore.QObject):
    """
    AlertsTab is the Alerts settings tab in the settings dialog.
    """
    log.info(u'Alert Manager loaded')

    def __init__(self, parent):
        QtCore.QObject.__init__(self)
        self.parent = parent
        self.screen = None
        self.timer_id = 0
        self.alertList = []
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'flush_alert'), self.generateAlert)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'alert_text'), self.displayAlert)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'screen_changed'), self.screenChanged)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'config_updated'), self.screenChanged)

    def screenChanged(self):
        log.debug(u'screen changed')
        self.alertTab = self.parent.alertsTab
        self.screen = self.parent.maindisplay.screens.current
        self.font = QtGui.QFont()
        self.font.setFamily(self.alertTab.font_face)
        self.font.setBold(True)
        self.font.setPointSize(self.alertTab.font_size)
        self.metrics = QtGui.QFontMetrics(self.font)
        self.alertHeight = self.metrics.height() + 4
        if self.alertTab.location == 0:
            self.alertScreenPosition = 0
        else:
            self.alertScreenPosition = self.screen[u'size'].height() - self.alertHeight
            self.alertHeight = self.screen[u'size'].height() - self.alertScreenPosition
        self.parent.maindisplay.setAlertSize(self.alertScreenPosition, self.alertHeight)

    def displayAlert(self, text=u''):
        """
        Called from the Alert Tab to display an alert

        ``text``
            display text
        """
        log.debug(u'display alert called %s' % text)
        if not self.screen:
            self.screenChanged()
        self.parent.maindisplay.parent.StatusBar.showMessage(u'')
        self.alertList.append(text)
        if self.timer_id != 0:
            self.parent.maindisplay.parent.StatusBar.showMessage(\
                    self.trUtf8(u'Alert message created and delayed'))
            return
        self.generateAlert()

    def generateAlert(self):
        log.debug(u'Generate Alert called')
        if len(self.alertList) == 0:
            return
        text = self.alertList.pop(0)
        alertTab = self.parent.alertsTab
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
            QtGui.QColor(self.alertTab.bg_color))
        painter.setFont(self.font)
        painter.setPen(QtGui.QColor(self.alertTab.font_color))
        x, y = (0, 2)
        painter.drawText(
            x, y + self.metrics.height() - self.metrics.descent() - 1, text)
        painter.end()
        self.parent.maindisplay.addAlertImage(alertframe)
        # check to see if we have a timer running
        if self.timer_id == 0:
            self.timer_id = self.startTimer(int(alertTab.timeout) * 1000)

    def timerEvent(self, event):
        if event.timerId() == self.timer_id:
            self.parent.maindisplay.addAlertImage(None, True)
        self.killTimer(self.timer_id)
        self.timer_id = 0
        self.generateAlert()
