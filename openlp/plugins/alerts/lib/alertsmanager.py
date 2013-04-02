# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The :mod:`~openlp.plugins.alerts.lib.alertsmanager` module contains the part of
the plugin which manages storing and displaying of alerts.
"""

import logging

from PyQt4 import QtCore

from openlp.core.lib import Receiver, translate

log = logging.getLogger(__name__)

class AlertsManager(QtCore.QObject):
    """
    AlertsManager manages the settings of Alerts.
    """
    log.info(u'Alert Manager loaded')

    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        self.screen = None
        self.timer_id = 0
        self.alertList = []
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'live_display_active'), self.generateAlert)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'alerts_text'), self.onAlertText)

    def onAlertText(self, message):
        """
        Called via a alerts_text event. Message is single element array
        containing text
        """
        if message:
            self.displayAlert(message[0])

    def displayAlert(self, text=u''):
        """
        Called from the Alert Tab to display an alert

        ``text``
            display text
        """
        log.debug(u'display alert called %s' % text)
        if text:
            self.alertList.append(text)
            if self.timer_id != 0:
                Receiver.send_message(u'mainwindow_status_text',
                    translate('AlertsPlugin.AlertsManager', 'Alert message created and displayed.'))
                return
            Receiver.send_message(u'mainwindow_status_text', u'')
            self.generateAlert()

    def generateAlert(self):
        """
        Format and request the Alert and start the timer
        """
        log.debug(u'Generate Alert called')
        if not self.alertList:
            return
        text = self.alertList.pop(0)
        alertTab = self.parent().settingsTab
        self.parent().liveController.display.alert(text, alertTab.location)
        # Check to see if we have a timer running.
        if self.timer_id == 0:
            self.timer_id = self.startTimer(int(alertTab.timeout) * 1000)

    def timerEvent(self, event):
        """
        Time has finished so if our time then request the next Alert
        if there is one and reset the timer.

        ``event``
            the QT event that has been triggered.
        """
        log.debug(u'timer event')
        if event.timerId() == self.timer_id:
            alertTab = self.parent().settingsTab
            self.parent().liveController.display.alert(u'', alertTab.location)
        self.killTimer(self.timer_id)
        self.timer_id = 0
        self.generateAlert()
