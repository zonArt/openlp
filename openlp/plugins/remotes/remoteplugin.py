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

from PyQt4 import QtNetwork, QtCore

from openlp.core.lib import Plugin, Receiver
from openlp.plugins.remotes.lib import RemoteTab

class RemotesPlugin(Plugin):

    global log
    log = logging.getLogger(u'RemotesPlugin')
    log.info(u'Remote Plugin loaded')

    def __init__(self, plugin_helpers):
        Plugin.__init__(self, u'Remotes', u'1.9.0', plugin_helpers)
        self.weight = -1
        self.server = None

    def can_be_disabled(self):
        return True

    def initialise(self):
        log.debug(u'initialise')
        Plugin.initialise(self)
        self.insert_toolbox_item()
        self.server = QtNetwork.QUdpSocket()
        self.server.bind(int(self.config.get_config(u'remote port', 4316)))
        QtCore.QObject.connect(self.server,
            QtCore.SIGNAL(u'readyRead()'), self.readData)

    def finalise(self):
        log.debug(u'finalise')
        self.remove_toolbox_item()
        if self.server:
            self.server.close()

    def get_settings_tab(self):
        """
        Create the settings Tab
        """
        return RemoteTab(self.name)

    def readData(self):
        log.info(u'Remoted data has arrived')
        while self.server.hasPendingDatagrams():
            datagram, host, port = self.server.readDatagram(
                self.server.pendingDatagramSize())
            self.handle_datagram(datagram)

    def handle_datagram(self, datagram):
        log.info(u'Sending event %s ', datagram)
        pos = datagram.find(u':')
        event = unicode(datagram[:pos].lower())
        if event == u'alert':
            Receiver().send_message(u'alert_text', unicode(datagram[pos + 1:]))
        if event == u'next_slide':
            Receiver().send_message(u'live_slide_next')

    def about(self):
        about_text = self.trUtf8(u'<b>Remote Plugin</b><br>This plugin '
            u'provides the ability to send messages to a running version of '
            u'openlp on a different computer.<br>The Primary use for this '
            u'would be to send alerts from a creche')
        return about_text
