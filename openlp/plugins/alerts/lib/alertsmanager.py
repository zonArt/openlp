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
The :mod:`~openlp.plugins.alerts.lib.alertsmanager` module contains the part of the plugin which manages storing and
displaying of alerts.
"""

import logging

from PyQt4 import QtCore

from openlp.core.lib import Registry, translate


log = logging.getLogger(__name__)


class AlertsManager(QtCore.QObject):
    """
    AlertsManager manages the settings of Alerts.
    """
    log.info('Alert Manager loaded')

    def __init__(self, parent):
        super(AlertsManager, self).__init__(parent)
        Registry().register('alerts_manager', self)
        self.timer_id = 0
        self.alert_list = []
        Registry().register_function('live_display_active', self.generate_alert)
        Registry().register_function('alerts_text', self.alert_text)
        QtCore.QObject.connect(self, QtCore.SIGNAL('alerts_text'), self.alert_text)

    def alert_text(self, message):
        """
        Called via a alerts_text event. Message is single element array containing text.
        """
        if message:
            self.display_alert(message[0])

    def display_alert(self, text=''):
        """
        Called from the Alert Tab to display an alert.

        ``text``
            display text
        """
        log.debug('display alert called %s' % text)
        if text:
            self.alert_list.append(text)
            if self.timer_id != 0:
                self.main_window.show_status_message(
                    translate('AlertsPlugin.AlertsManager', 'Alert message created and displayed.'))
                return
            self.main_window.show_status_message('')
            self.generate_alert()

    def generate_alert(self):
        """
        Format and request the Alert and start the timer.
        """
        log.debug('Generate Alert called')
        if not self.alert_list:
            return
        text = self.alert_list.pop(0)
        alert_tab = self.parent().settings_tab
        self.live_controller.display.alert(text, alert_tab.location)
        # Check to see if we have a timer running.
        if self.timer_id == 0:
            self.timer_id = self.startTimer(int(alert_tab.timeout) * 1000)

    def timerEvent(self, event):
        """
        Time has finished so if our time then request the next Alert if there is one and reset the timer.

        ``event``
            the QT event that has been triggered.
        """
        log.debug('timer event')
        if event.timerId() == self.timer_id:
            alertTab = self.parent().settings_tab
            self.live_controller.display.alert('', alertTab.location)
        self.killTimer(self.timer_id)
        self.timer_id = 0
        self.generate_alert()

    def _get_live_controller(self):
        """
        Adds the live controller to the class dynamically
        """
        if not hasattr(self, '_live_controller'):
            self._live_controller = Registry().get('live_controller')
        return self._live_controller

    live_controller = property(_get_live_controller)

    def _get_main_window(self):
        """
        Adds the main window to the class dynamically
        """
        if not hasattr(self, '_main_window'):
            self._main_window = Registry().get('main_window')
        return self._main_window

    main_window = property(_get_main_window)
