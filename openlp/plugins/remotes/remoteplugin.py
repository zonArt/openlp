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
import sys

from PyQt4 import QtNetwork, QtGui, QtCore

from openlp.core.lib import Plugin, Receiver
from openlp.plugins.remotes.lib import RemoteTab

class RemotesPlugin(Plugin):

    global log
    log = logging.getLogger(u'RemotesPlugin')
    log.info(u'Remote Plugin loaded')

    def __init__(self, plugin_helpers):
        # Call the parent constructor
        Plugin.__init__(self, u'Remotes', u'1.9.0', plugin_helpers)
        self.weight = -1

    def check_pre_conditions(self):
        """
        Check to see if remotes is required
        """
        log.debug('check_pre_conditions')
        #Lets see if Remote is required
        if int(self.config.get_config(u'startup', 0)) == 2:
            return True
        else:
            return False

    def initialise(self):
        self.server = QtNetwork.QUdpSocket()
        self.server.bind(int(self.config.get_config(u'remote port', 4316)))
        QtCore.QObject.connect(self.server,
            QtCore.SIGNAL(u'readyRead()'), self.readData)

    def get_settings_tab(self):
        """
        Create the settings Tab
        """
        return RemoteTab()

    def readData(self):
        log.info(u'Remoted data has arrived')
        while self.server.hasPendingDatagrams():
            datagram,  host, port = self.server.readDatagram(
                self.server.pendingDatagramSize())
            self.handle_datagram(datagram)

    def handle_datagram(self, datagram):
        log.info(u'Sending event %s ',  datagram)
        pos = datagram.find(u':')
        event = unicode(datagram[:pos].lower())

        if event == u'alert':
            Receiver().send_message(u'alert_text', unicode(datagram[pos + 1:]))
        if event == u'next_slide':
            Receiver().send_message(u'live_slide_next')



